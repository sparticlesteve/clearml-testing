#!/bin/bash

# Use standard NERSC python environment
module load python

# Install clearml cli
if ! pip show clearml > /dev/null 2>&1; then
    echo "Installing clearml..."
    pip install --no-cache-dir clearml
else
    echo "clearml is already installed."
fi

clearml-task \
    --project clearml-testing \
    --name hello-bash \
    --queue muller \
    --task-type custom \
    --repo https://github.com/sparticlesteve/clearml-testing.git \
    --script hello_world.sh
