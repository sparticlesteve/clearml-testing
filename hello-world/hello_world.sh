#!/bin/bash

# Basic hello-world test of clearml
echo "Hello world from a ClearML bash task!"
env | grep SLURM

echo "Args: $@"

# Software loading
module load pytorch
module list
