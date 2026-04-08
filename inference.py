import os
import json
import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")

OPENAI_CLIENT = None
if HF_TOKEN:
    openai_kwargs = {"api_key": HF_TOKEN}
    OPENAI_CLIENT = OpenAI(**openai_kwargs)

if not HF_TOKEN:
    print("WARNING: HF_TOKEN is not set; OpenAI client will be disabled.")

print(
    "CONFIG "
    f"API_BASE_URL={API_BASE_URL} "
    f"MODEL_NAME={MODEL_NAME} "
    f"HF_TOKEN={'set' if HF_TOKEN else 'unset'} "
    f"LOCAL_IMAGE_NAME={LOCAL_IMAGE_NAME}"
)

VALID_ACTIONS = [
    "fill_missing",
    "clean_text",
    "normalize_date",
    "convert_salary",
    "remove_duplicates"
]


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
    has_whitespace = sum(1 for v in vals if v != v.strip())
    has_mixed_case = sum(1 for v in vals if v.lower() != v.upper() and v != v.lower())
    return (has_whitespace + has_mixed_case) >= (len(vals) * 0.5)


def can_normalize_date(preview):
    return "date" in preview


def can_convert_salary(preview):
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
        except Exception:
            return False

    return len(numeric_vals) >= 2


def can_remove_duplicates(preview):
    cols = list(preview.keys())
    if not cols:
        return False

    data_cols = [c for c in cols if c != "id"]
    if not data_cols:
        return False

    rows = list(zip(*[list(preview[c].values()) for c in data_cols]))
    return len(rows) != len(set(rows))


def generate_candidates(observation, blocked_actions):
    preview = observation["preview"]
    missing = observation["missing_values"]
    candidates = []

    if can_remove_duplicates(preview):
        act = {"action_type": "remove_duplicates", "column": None}
        if (act["action_type"], act["column"]) not in blocked_actions:
            candidates.append(act)

    if can_convert_salary(preview):
        act = {"action_type": "convert_salary", "column": "salary"}
        if (act["action_type"], act["column"]) not in blocked_actions:
            candidates.append(act)

    if can_normalize_date(preview):
        act = {"action_type": "normalize_date", "column": "date"}
        if (act["action_type"], act["column"]) not in blocked_actions:
            candidates.append(act)

    if can_fill_missing_numeric(preview, missing, "salary"):
        act = {"action_type": "fill_missing", "column": "salary"}
        if (act["action_type"], act["column"]) not in blocked_actions:
            candidates.append(act)

    if can_fill_missing_numeric(preview, missing, "age"):
        act = {"action_type": "fill_missing", "column": "age"}
        if (act["action_type"], act["column"]) not in blocked_actions:
            candidates.append(act)

    if can_clean_text(preview):
        act = {"action_type": "clean_text", "column": "name"}
        if (act["action_type"], act["column"]) not in blocked_actions:
            candidates.append(act)

    return candidates


def parse_action(response_text):
    try:
        action_data = json.loads(response_text)
        action_type = action_data.get("action_type")
        column = action_data.get("column")
        if action_type not in VALID_ACTIONS:
            return None
        if column in ["null", "None"]:
            column = None
        return {"action_type": action_type, "column": column}
    except Exception:
        return None


def llm_select_action(observation, blocked_actions):
    if not OPENAI_CLIENT:
        return None

    print("STEP llm_select_action")
    prompt = json.dumps({
        "observation": observation,
        "blocked_actions": [list(b) for b in blocked_actions],
        "valid_actions": VALID_ACTIONS,
        "instructions": "Choose one action from valid_actions and return a JSON object with keys action_type and column. Use null for column when action is remove_duplicates."
    })

    try:
        response = OPENAI_CLIENT.responses.create(
            model=MODEL_NAME,
            input=prompt
        )

        text = None
        if hasattr(response, "output_text"):
            text = response.output_text
        elif getattr(response, "output", None):
            output = response.output
            if isinstance(output, list) and len(output) > 0:
                content = output[0].get("content") or []
                if len(content) > 0:
                    text = content[0].get("text")

        if not text:
            return None

        return parse_action(text.strip())
    except Exception:
        return None


def run_task(task_id):
    print("START inference")
    print(f"STEP reset_task task_id={task_id}")

    res = requests.post(f"{API_BASE_URL}/reset?task_id={task_id}")
    data = res.json()

    observation = data["observation"]
    total_reward = 0
    tried_actions = set()
    blocked_actions = set()

    while True:
        action = None
        if OPENAI_CLIENT:
            action = llm_select_action(observation, tried_actions)

        if action is None:
            candidates = generate_candidates(observation, blocked_actions)
            candidates = [
                a for a in candidates
                if (a["action_type"], a["column"]) not in tried_actions
            ]
            if candidates:
                action = candidates[0]

        if action is None:
            break

        print(f"STEP action_selected {json.dumps(action)}")
        tried_actions.add((action["action_type"], action["column"]))

        res = requests.post(f"{API_BASE_URL}/step", json=action)
        result = res.json()

        reward = result["reward"]
        done = result["done"]
        observation = result["observation"]

        print(f"STEP action_result reward={reward} done={done}")
        total_reward += reward

        if done:
            break

    print(f"END inference task_id={task_id} total_reward={total_reward}")
    print("END")


if __name__ == "__main__":
    for task_id in range(3):
        run_task(task_id)
