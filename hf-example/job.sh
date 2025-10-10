#!/bin/bash

set -ex

echo "Initial environment checks:"
which python
#pip list
#env | grep SLURM
#pwd

# Update path to pickup torchrun command
#ls ../../../bin
#export PATH=../../../bin:$PATH

# Module-based environment setup
# Need to clear PYTHONPATH to avoid conflicts
unset PYTHONPATH
module load pytorch/2.6.0

# Install clearml package
pip install clearml

# Python binary tests
which python
python -c "print('hello')"
pip list

# Use scratch for huggingface cache
export HF_HOME=$SCRATCH/cache/huggingface

# Distributed training configuration
export MASTER_ADDR=$(scontrol show hostnames | head -n 1)
export MASTER_PORT=29507

env | grep MASTER

# Other settings
export OMP_NUM_THREADS=8
#export NCCL_DEBUG=INFO

# Launch example with torchrun
torchrun \
    --nnodes=$SLURM_JOB_NUM_NODES \
    --nproc-per-node=${SLURM_GPUS_PER_TASK:-4} \
    --rdzv-backend=c10d \
    --rdzv-endpoint=$MASTER_ADDR:$MASTER_PORT \
    nlp_example.py

echo "SUCCESS"
