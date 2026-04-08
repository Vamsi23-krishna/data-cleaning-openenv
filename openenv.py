#!/usr/bin/env python
"""
OpenEnv CLI - Validation and testing tool for Data Cleaning Environment
"""
import sys
import os
import json
import argparse
from pathlib import Path

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

def validate_structure():
    """Validate project structure and required files"""
    print("\n Validating project structure...")
    required_files = [
        'api/server.py',
        'env/environment.py',
        'env/action_handler.py',
        'models/action.py',
        'tasks/task_loader.py',
        'tasks/easy_task.py',
        'tasks/medium_task.py',
        'tasks/hard_task.py',
        'datasets/easy_dirty.csv',
        'datasets/easy_clean.csv',
        'datasets/medium_dirty.csv',
        'datasets/medium_clean.csv',
        'datasets/hard_dirty.csv',
        'datasets/hard_clean.csv',
        'requirements.txt',
        'README.md',
        'Dockerfile',
        'openenv.yaml'
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
        else:
            print(f"   {file}")
    
    if missing:
        print(f"\n   Missing files: {', '.join(missing)}")
        return False
    
    print("   All required files present")
    return True

def validate_imports():
    """Validate that all modules can be imported"""
    print("\n Validating imports...")
    modules_to_test = [
        'api.server',
        'env.environment',
        'env.action_handler',
        'models.action',
        'tasks.task_loader',
        'utils.validators',
        'graders.grader'
    ]
    
    import_errors = []
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"   {module}")
        except Exception as e:
            import_errors.append((module, str(e)))
            print(f"   {module}: {e}")
    
    if import_errors:
        return False
    
    print("   All modules imported successfully")
    return True

def validate_tasks():
    """Validate that all tasks load correctly"""
    print("\n Validating tasks...")
    try:
        from tasks.task_loader import load_all_tasks
        tasks = load_all_tasks()
        
        if len(tasks) != 3:
            print(f"   Expected 3 tasks, got {len(tasks)}")
            return False
        
        for i, task in enumerate(tasks):
            required_keys = ['name', 'description', 'difficulty', 'env']
            missing_keys = [k for k in required_keys if k not in task]
            
            if missing_keys:
                print(f"   Task {i} missing keys: {missing_keys}")
                return False
            
            print(f"   Task {i}: {task['name']}")
        
        print("   All tasks loaded successfully")
        return True
    except Exception as e:
        print(f"   Failed to load tasks: {e}")
        return False

def validate_datasets():
    """Validate that all datasets exist and are readable"""
    print("\n Validating datasets...")
    import pandas as pd
    
    datasets = [
        ('datasets/easy_dirty.csv', 'Easy dirty'),
        ('datasets/easy_clean.csv', 'Easy clean'),
        ('datasets/medium_dirty.csv', 'Medium dirty'),
        ('datasets/medium_clean.csv', 'Medium clean'),
        ('datasets/hard_dirty.csv', 'Hard dirty'),
        ('datasets/hard_clean.csv', 'Hard clean'),
    ]
    
    for path, name in datasets:
        try:
            df = pd.read_csv(path)
            print(f"   {name}: {df.shape[0]} rows, {df.shape[1]} columns")
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            return False
    
    print("   All datasets valid")
    return True

def validate_actions():
    """Validate that all action handlers work"""
    print("\n  Validating actions...")
    from utils.actions_list import ALLOWED_ACTIONS
    
    print(f"  Allowed actions: {', '.join(ALLOWED_ACTIONS)}")
    
    expected_actions = [
        'fill_missing', 'clean_text', 'normalize_date', 
        'convert_salary', 'remove_duplicates'
    ]
    
    missing_actions = [a for a in expected_actions if a not in ALLOWED_ACTIONS]
    if missing_actions:
        print(f"   Missing actions: {missing_actions}")
        return False
    
    print(f"   All {len(ALLOWED_ACTIONS)} actions defined")
    return True

def validate_environment():
    """Validate environment functionality"""
    print("\n Validating environment...")
    try:
        from env.environment import DataCleaningEnv
        from models.action import Action
        
        # Test easy task
        env = DataCleaningEnv('datasets/easy_dirty.csv', 'datasets/easy_clean.csv')
        observation = env.reset()
        
        # Check observation structure
        required_keys = ['preview', 'missing_values', 'steps']
        missing_keys = [k for k in required_keys if k not in observation]
        
        if missing_keys:
            print(f"   Observation missing keys: {missing_keys}")
            return False
        
        print(f"   Environment reset successful")
        
        # Test step
        action = Action(action_type="fill_missing", column="age")
        obs, reward, done, info = env.step(action)
        print(f"   Step executed: reward={reward:.3f}, done={done}")
        
        # Test state
        state = env.state()
        if 'data' not in state or 'steps' not in state:
            print("  ❌ State missing required fields")
            return False
        
        print(f"   Environment state retrieved")
        print("   Environment validation complete")
        return True
    except Exception as e:
        print(f"   Environment validation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def validate_all():
    """Run all validations"""
    print("=" * 60)
    print("OPENENV VALIDATION")
    print("=" * 60)
    
    checks = [
        ("Structure", validate_structure),
        ("Imports", validate_imports),
        ("Actions", validate_actions),
        ("Datasets", validate_datasets),
        ("Tasks", validate_tasks),
        ("Environment", validate_environment),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"   Unexpected error: {e}")
            results[name] = False
    
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    for name, passed in results.items():
        status = " PASS" if passed else " FAIL"
        print(f"{status}: {name}")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    print(f"\nTotal: {passed}/{total} checks passed")
    print("=" * 60)
    
    return all(results.values())

def main():
    parser = argparse.ArgumentParser(description='OpenEnv CLI')
    parser.add_argument('command', choices=['validate'], help='Command to run')
    
    args = parser.parse_args()
    
    if args.command == 'validate':
        success = validate_all()
        sys.exit(0 if success else 1)

if __name__ == '__main__':
    # If no arguments, run validation
    if len(sys.argv) == 1:
        success = validate_all()
        sys.exit(0 if success else 1)
    else:
        main()
