from tasks.task_loader import load_all_tasks

tasks = load_all_tasks()

for task in tasks:
    print("Task:", task["name"])
    print("Difficulty:", task["difficulty"])

    env = task["env"]
    obs = env.reset()

    print("Initial Observation:", obs)
    print("-" * 40)