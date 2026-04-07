import requests

BASE_URL = "http://127.0.0.1:8001"


def get_values(preview, col):
    if col not in preview:
        return []
    return [v for v in preview[col].values()]


def can_clean_text(preview):
    if "name" not in preview:
        return False
    vals = [v for v in get_values(preview, "name") if isinstance(v, str)]
    if len(vals) < 2:
        return False
    # Check if there's meaningful inconsistency (spacing or casing differences)
    has_whitespace = sum(1 for v in vals if v != v.strip())
    has_mixed_case = sum(1 for v in vals if v.lower() != v.upper() and v != v.lower())
    # Only recommend if at least 50% of values need cleaning
    total = len(vals)
    return (has_whitespace + has_mixed_case) >= (total * 0.5)


def can_normalize_date(preview):
    # Always try date normalization if date column exists
    return "date" in preview


def can_convert_salary(preview):
    # Always try salary conversion if salary column exists
    return "salary" in preview

def can_fill_missing_numeric(preview, missing, col):
    if col not in preview or col not in missing:
        return False
    if missing[col] <= 0:
        return False

    vals = get_values(preview, col)
    if not any(v is None for v in vals):
        return False

    numeric_vals = []
    for v in vals:
        if v is None:
            continue
        try:
            numeric_vals.append(float(v))
        except:
            return False

    return len(numeric_vals) >= 2


def can_remove_duplicates(preview):
    cols = list(preview.keys())
    if not cols:
        return False
    
    data_cols = [c for c in cols if c != 'id']
    if not data_cols:
        return False
    
    rows = list(zip(*[list(preview[c].values()) for c in data_cols]))
    return len(rows) != len(set(rows))


def generate_candidates(observation, blocked_actions):
    preview = observation["preview"]
    missing = observation["missing_values"]
    candidates = []

    # First: Check for structural issues (duplicates) - must run early
    if can_remove_duplicates(preview):
        act = {"action_type": "remove_duplicates", "column": None}
        if (act["action_type"], act["column"]) not in blocked_actions:
            candidates.append(act)

    # Then: Convert salary format (always try if column exists)
    if can_convert_salary(preview):
        act = {"action_type": "convert_salary", "column": "salary"}
        if (act["action_type"], act["column"]) not in blocked_actions:
            candidates.append(act)

    # Normalize dates
    if can_normalize_date(preview):
        act = {"action_type": "normalize_date", "column": "date"}
        if (act["action_type"], act["column"]) not in blocked_actions:
            candidates.append(act)

    # Handle missing values
    if can_fill_missing_numeric(preview, missing, "salary"):
        act = {"action_type": "fill_missing", "column": "salary"}
        if (act["action_type"], act["column"]) not in blocked_actions:
            candidates.append(act)

    if can_fill_missing_numeric(preview, missing, "age"):
        act = {"action_type": "fill_missing", "column": "age"}
        if (act["action_type"], act["column"]) not in blocked_actions:
            candidates.append(act)

    # Clean text (cosmetic)
    if can_clean_text(preview):
        act = {"action_type": "clean_text", "column": "name"}
        if (act["action_type"], act["column"]) not in blocked_actions:
            candidates.append(act)

    return candidates

def run_task(task_id):
    print(f"\nRunning Task {task_id}")

    res = requests.post(f"{BASE_URL}/reset?task_id={task_id}")
    data = res.json()

    observation = data["observation"]
    total_reward = 0
    blocked_actions = set()
    tried_actions = set()

    while True:
        candidates = generate_candidates(observation, blocked_actions)
        candidates = [
            a for a in candidates
            if (a["action_type"], a["column"]) not in tried_actions
        ]

        if not candidates:
            break

        action = candidates[0]
        tried_actions.add((action["action_type"], action["column"]))

        res = requests.post(f"{BASE_URL}/step", json=action)
        result = res.json()

        reward = result["reward"]
        done = result["done"]

        print("Action:", action)
        print("Reward:", reward)

        total_reward += reward
        observation = result["observation"]

        if done:
            break

    print("Total Score:", total_reward)


if __name__ == "__main__":
    for task_id in [0, 1, 2]:
        run_task(task_id)