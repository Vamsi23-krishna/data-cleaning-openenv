"""
Test script to verify all API endpoints are working correctly
"""
import requests
import json
import time
import subprocess
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    """Test basic health endpoint"""
    print("\n Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
        print(" Health endpoint working:", response.json())
        return True
    except Exception as e:
        print(f" Health endpoint failed: {e}")
        return False

def test_reset():
    """Test /reset endpoint"""
    print("\n Testing /reset endpoint...")
    try:
        for task_id in [0, 1, 2]:
            response = requests.post(f"{BASE_URL}/reset?task_id={task_id}")
            assert response.status_code == 200
            data = response.json()
            assert "task" in data
            assert "observation" in data
            print(f" Task {task_id} reset successful: {data['task']}")
        return True
    except Exception as e:
        print(f" Reset endpoint failed: {e}")
        return False

def test_step():
    """Test /step endpoint"""
    print("\n Testing /step endpoint...")
    try:
        # Reset first
        response = requests.post(f"{BASE_URL}/reset?task_id=0")
        observation = response.json()["observation"]
        
        # Try a step action
        action = {"action_type": "fill_missing", "column": "age"}
        response = requests.post(f"{BASE_URL}/step", json=action)
        assert response.status_code == 200
        data = response.json()
        assert "observation" in data
        assert "reward" in data
        assert "done" in data
        print(f" Step endpoint working. Reward: {data['reward']}, Done: {data['done']}")
        return True
    except Exception as e:
        print(f" Step endpoint failed: {e}")
        return False

def test_state():
    """Test /state endpoint"""
    print("\n Testing /state endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/state")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data or "error" not in data
        print(f" State endpoint working")
        return True
    except Exception as e:
        print(f" State endpoint failed: {e}")
        return False

def main():
    print("=" * 60)
    print("API ENDPOINT TESTS")
    print("=" * 60)
    
    # Give server time to start if just started
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            requests.get(f"{BASE_URL}/")
            break
        except requests.exceptions.ConnectionError:
            retry_count += 1
            if retry_count < max_retries:
                print(f" Waiting for server... ({retry_count}/{max_retries})")
                time.sleep(1)
            else:
                print(f"❌ Server not responding at {BASE_URL}")
                print("Please ensure the server is running: uvicorn api.server:app --reload")
                sys.exit(1)
    
    results = {
        "health": test_health(),
        "reset": test_reset(),
        "step": test_step(),
        "state": test_state(),
    }
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for test_name, passed_test in results.items():
        status = " PASS" if passed_test else " FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 60)
    
    return all(results.values())

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
