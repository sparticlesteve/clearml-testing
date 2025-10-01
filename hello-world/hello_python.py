from clearml import Task

print("Hello world from python")
print(f"Current ClearML Task: {Task.current_task()}")

# Now do the init
task = Task.init("clearml-testing", "hello-python")
print(f"Task initialized: {task}")
print(f"Current ClearML Task: {Task.current_task()}")
