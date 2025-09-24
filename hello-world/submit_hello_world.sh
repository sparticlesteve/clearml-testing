#!/bin/bash

# Use standard NERSC python environment
module load python

# Install clearml cli
if ! pip show clearml > /dev/null 2>&1; then
    echo "Installing clearml..."
    pip install --no-cache-dir clearml
else
    echo "clearml: already installed"
fi

set -x
clearml-task \
    --project clearml-testing \
    --name hello-bash \
    --queue muller \
    --task-type custom \
    --repo https://github.com/sparticlesteve/clearml-testing.git \
    --force-no-requirements \
    --script hello-world/hello_world.sh \
    --args arg1=value1
