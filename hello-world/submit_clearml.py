"""ClearML SDK submission of training job"""

import pprint
from typing import Dict, Any

import clearml
from clearml import Task


def get_task_summary(task: Task) -> Dict[str, Any]:
    summary = dict(
        id=task.id,
        task_type=task.task_type,
        project=task.get_project_name(),
        name=task.name,
        status=task.get_status(),
        tags=list(task.get_tags() or []),
        parameters=task.get_parameters_as_dict(),
        user_properties=task.get_user_properties(),
        script=task.get_script(),
    )
    return summary


def main():

    # Starting with hardcoded configuration
    task = Task.create(
        project_name="clearml-testing",
        task_name="hello-python",
        task_type="custom",
        repo="https://github.com/sparticlesteve/clearml-testing.git",
        script="hello-world/hello_python.py",
    )

    # SLURM job settings
    task.set_user_properties(
        num_nodes=2,
    )

    # Print the configuration
    print("\nCREATED NEW TASK:")
    pprint.pprint(get_task_summary(task))

    # Enqueue the task
    enqueue_response = Task.enqueue(
        task=task,
        queue_name="muller",
    )

    print("\nTASK ENQUEUED:")
    pprint.pprint(enqueue_response)

if __name__ == "__main__":
    main()
