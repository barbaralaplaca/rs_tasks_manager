from curses import wrapper
from urllib import response
import pytest
import requests

base_url = 'http://127.0.0.1:5000'
tasks = []

def add_task_wrapper(func):
    def wrapper():
        new_task_data = {
            "title": "New task",
            "description": "Tasks's description"
        }
        requests.post(f"{base_url}/tasks", json=new_task_data)
    return wrapper

def test_create_task():
    new_task_data = {
        "title": "New task",
        "description": "Tasks's description"
    }
    response = requests.post(f"{base_url}/tasks", json=new_task_data)
    assert response.status_code == 200
    response_json = response.json()
    assert "message" and 'id' in response_json


def test_get_tasks():
    response = requests.get(f"{base_url}/tasks")
    assert response.status_code == 200
    assert "tasks" in response.json()
    assert "total_tasks" in response.json()


@add_task_wrapper
def test_get_task():
    response = requests.get(f"{base_url}/tasks/1")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['id'] == "1"


@add_task_wrapper
def test_update_task():
    payload = {
            "title": "Updated title", 
            "description": "Tasks's description",
            "completed": True
    }
    response = requests.put(f"{base_url}/tasks/1", json=payload)
    assert response.status_code == 200
    response_json = response.json()
    assert "message"in response_json
    assert response_json['title'] == payload['title'] 
    assert response_json['description'] == payload['description'] 
    assert response_json['completed'] == payload['completed'] 


@add_task_wrapper
def test_delete_task():
    tasks = [
        {
            "title": "New task", 
            "description": "Tasks's description",
            "id": 1
        }
    ]
    task_id = tasks[0]['id']
    response = requests.delete(f"{base_url}/tasks/{task_id}")
    assert response.status_code == 204

    response = requests.get(f"{base_url}/tasks/1")
    assert response.status_code == 404

