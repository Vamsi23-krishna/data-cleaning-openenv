from tasks.easy_task import get_easy_task 
from tasks.medium_task import get_medium_task
from tasks.hard_task import get_hard_task

def load_all_tasks():
    return [
        get_easy_task(),
        get_medium_task(),
        get_hard_task()
    ]