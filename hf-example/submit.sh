#!/bin/bash

ml python

set -x
clearml-task \
    --project clearml-testing \
    --name hf-example \
    --queue muller \
    --task-type training \
    --repo https://github.com/sparticlesteve/clearml-testing.git \
    --cwd hf-example \
    --binary /bin/bash \
    --script job.sh \
    --args mixed_precision=bf16
