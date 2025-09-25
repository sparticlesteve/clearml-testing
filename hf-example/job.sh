#!/bin/bash

set -x

which python
pip list
#env | grep PYTHON
#env | grep PATH
#env | grep ENV
pwd
ls ../../../bin
export PATH=../../../bin:$PATH

# Environment setup
#module load pytorch/2.6.0

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
    --nproc-per-node=$SLURM_GPUS_PER_NODE \
    --rdzv-backend=c10d \
    --rdzv-endpoint=$MASTER_ADDR:$MASTER_PORT \
    nlp_example.py

echo "SUCCESS"
