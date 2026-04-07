from utils.actions_list import ALLOWED_ACTIONS

def validate_action(action):
    if action.action_type not in ALLOWED_ACTIONS:
        raise ValueError(f"Invalid action: {action.action_type}")