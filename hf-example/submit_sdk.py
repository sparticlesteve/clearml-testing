import pprint
from typing import Dict, Any, Optional, Tuple, Union

import clearml
from clearml import Task

TaskRef = Union[str, Tuple[str, str]]  # task_id OR (project, name)


def get_task(ref: TaskRef) -> Task:
    if isinstance(ref, str):
        return Task.get_task(task_id=ref)
    proj, name = ref
    return Task.get_task(project_name=proj, task_name=name)


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


def create_task(
    task_name: str, project_name: str,
    template_task: Optional[Task] = None,
    num_nodes: Optional[int] = None,
    **kwargs
) -> Task:
    script_defaults = template_task.get_script() if template_task else {}
    argparse_defaults = template_task.get_parameters_as_dict().get('Args', {})

    task = Task.create(
        task_name=task_name,
        project_name=project_name,
        task_type=kwargs.get('task_type', template_task.task_type if template_task else None),
        base_task_id=template_task.id if template_task else None,
        binary=kwargs.get('binary', script_defaults.get('binary', None)),
        script=kwargs.get('script', script_defaults.get('entry_point', None)),
        repo=kwargs.get('repo', script_defaults.get('repository', None)),
        commit=kwargs.get('commit', script_defaults.get('commit', None)),
        working_directory=kwargs.get('working_directory', script_defaults.get('working_dir')),
        argparse_args=argparse_defaults.update(kwargs.get('argparse_args', {})),
        # requirements_file=requirements_file,
        # docker=docker_image,
        # docker_args=docker_args,
        # docker_bash_setup_script=docker_setup_bash,
    )

    # Force-override the name and project
    task.set_name(task_name)
    task.set_project(project_name=project_name)

    # Add additional properties, e.g. for slurm job settings
    properties = template_task.get_user_properties()
    if num_nodes is not None:
        properties.update(num_nodes=num_nodes)
    task.set_user_properties(**properties)

    return task


def main():

    # Retrieve the template task
    template_task = clearml.Task.get_task(
        project_name="clearml-testing",
        task_name="hf-example",
        allow_archived=False,
    )

    # Print out all available details
    print("\nLOADED TEMPLATE TASK:")
    pprint.pprint(get_task_summary(template_task))

    # Create new task
    new_task = create_task(
        project_name="clearml-testing",
        task_name="hf-example-sdk-clone",
        template_task=template_task,
        num_nodes=2,
    )

    # Print out the configuration of the new task
    print("\nCREATED NEW TASK:")
    pprint.pprint(get_task_summary(new_task))

    # Enqueue the task
    enqueue_response = Task.enqueue(
        task=new_task,
        queue_name="muller",
    )

    print("\nTASK ENQUEUED:")
    pprint.pprint(enqueue_response)

if __name__ == '__main__':
    main()

