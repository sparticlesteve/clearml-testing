import os

from clearml import Task
from clearml.automation import PipelineController


def pre_execute_callback(a_pipeline, a_node, param_override):
    """Callback before step execution"""
    print(f"Starting Task id={a_node.task_id()} with parameters: {param_override}")
    return True


def post_execute_callback(a_pipeline, a_node):
    """Callback after step execution"""
    print("Completed Task id={}".format(a_node.task_id()))


# Download data task
task = Task.create(
    project_name="Megatron testing",
    task_name="download-data-step",
    task_type="data_processing",
    repo="https://github.com/sparticlesteve/clearml-testing.git",
    branch="main",
    working_directory="megatron-pipeline",
    packages=["clearml", "transformers", "datasets"],
    script="download_wikitext.py",
    argparse_args=[("data-dir", "/mscratch/sd/d/dasml")],
)

# Test enqueue
Task.enqueue(task=task, queue_name="muller")
