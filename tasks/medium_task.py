from env.environment import DataCleaningEnv

def get_medium_task():
    env = DataCleaningEnv(
        "datasets/medium_dirty.csv",
        "datasets/medium_clean.csv"
    )
    task = {
        "name": "medium_format_cleaning",
        "description": "Normalize dates, text, and salary formats",
        "difficulty": "medium",
        "env": env 
    }
    return task 