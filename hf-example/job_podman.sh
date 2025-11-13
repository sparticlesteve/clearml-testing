#!/bin/bash

set -ex

#env | grep PYTHONPATH
#env | grep PYTHONHOME
unset PYTHONPATH

# Use scratch for huggingface cache
export HF_HOME=$SCRATCH/cache/huggingface

# Distributed training configuration
export MASTER_ADDR=$(scontrol show hostnames | head -n 1)
export MASTER_PORT=29507

# Other settings
export OMP_NUM_THREADS=8
#export NCCL_DEBUG=INFO

# Podman container setup
image=nersc/pytorch:25.06.01
cont_params=(
    --rm --gpu --nccl
    -v .:/workspace
    --env HF_* --env MASTER_*
    --net host
)
#-v $HOME/clearml.conf:/root/clearml.conf:ro
#-e CLEARML_CONFIG_FILE=/root/clearml.conf

# Launch example with podman+torchrun
podman-hpc run ${cont_params[@]} $image \
    bash -c "pip install clearml;
    torchrun \
    --nnodes=$SLURM_JOB_NUM_NODES \
    --nproc-per-node=${SLURM_GPUS_PER_TASK:-4} \
    --rdzv-backend=c10d \
    --rdzv-endpoint=$MASTER_ADDR:$MASTER_PORT \
    nlp_example.py"

echo "SUCCESS"
