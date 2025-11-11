import pprint
import subprocess
from typing import Dict, Any

import clearml
from clearml import Task


def get_git_commit():
    """Return the current git commit hash in the current repo."""
    try:
        args = ["git", "rev-parse", "HEAD"]
        commit = subprocess.check_output(args, stderr=subprocess.DEVNULL).decode().strip()
        return commit
    except subprocess.CalledProcessError:
        return None


def get_task_summary(task: Task) -> Dict[str, Any]:
    summary = dict(
        id=task.id,
        task_type=task.task_type,
        project=task.get_project_name(),
        name=task.name,
        status=task.get_status(),
        tags=list(task.get_tags() or []),
        # parameters=task.get_parameters(),
        parameters=task.get_parameters_as_dict(),
        user_properties=task.get_user_properties(),
        script=task.get_script(),
    )
    return summary


def main():

    # Get the current commit hash
    commit = get_git_commit()
    print(f"using git commit: {commit}")

    # Create a task with some hardcoded configuration
    task = Task.create(
        project_name="clearml-testing",
        task_name="hf-example",
        task_type="training",
        binary="/bin/bash",
        script="job_podman.sh",
        repo="https://github.com/sparticlesteve/clearml-testing.git",
        commit=commit,
        working_directory="hf-example",
        argparse_args="",
        # requirements_file=requirements_file,
        # docker=docker_image,
        # docker_args=docker_args,
        # docker_bash_setup_script=docker_setup_bash,
    )

    # SLURM job settings
    task.set_user_properties(
        num_nodes=1,
    )

    # Print the configuration
    print("\nCREATED TASK:")
    pprint.pprint(get_task_summary(task))

    # Enqueue the task
    enqueue_response = Task.enqueue(
        task=task,
        queue_name="muller",
    )

    print("\nTASK ENQUEUED:")
    pprint.pprint(enqueue_response)


if __name__ == '__main__':
    main()
