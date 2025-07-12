import requests
import allure
import pytest

pytestmark = pytest.mark.smoke

# Login
@allure.parent_suite("Smoke Test")
@allure.title('Login')
def test_login(config, headers):
    global base_url
    base_url = config['base_url']
    assert config != None
    assert headers != None

# Create Project
@allure.parent_suite("Smoke Test")
@allure.title('Create Project')
def test_create_project(config, headers):
    global project_id
    url = f'{base_url}/projects'

    res = requests.put(url, json=config['projects'], headers=headers)
    assert res.status_code == 201
    assert res.json()['title'] == config['projects']['title']
    assert res.json()['description'] == config['projects']['description']

    project_id = res.json()['id']
    # print(project_id)

# Verify Project
@allure.parent_suite("Smoke Test")
@allure.title('Verify Project')
def test_verify_project(config, headers):
    url = f'{base_url}/projects/{project_id}'

    res = requests.get(url, headers=headers)
    assert res.status_code == 200
    assert res.json()['title'] == config['projects']['title']
    assert res.json()['description'] == config['projects']['description'] 

# Add Task
@allure.parent_suite("Smoke Test")
@allure.title('Create Task')
def test_add_task(config, headers):
    global task_id
    # print(project_id)
    url = f'{base_url}/projects/{project_id}/tasks'

    res = requests.put(url, json=config['tasks'], headers=headers)
    # print(res.status_code)
    # print(res.json())
    assert res.status_code == 201
    assert res.json()['title'] == config['tasks']['title']
    assert res.json()['description'] == config['tasks']['description']

    task_id = res.json()['id']

# Verify
@allure.parent_suite("Smoke Test")
@allure.title('Verify Task')
def test_verify_task(config, headers):
    url =  f'{base_url}/tasks/{task_id}'

    res = requests.get(url, headers=headers)
    assert res.status_code == 200
    assert res.json()['title'] == config['tasks']['title']
    assert res.json()['description'] == config['tasks']['description']
    assert res.json()['project_id'] == project_id

# Delete Project
@allure.parent_suite("Smoke Test")
@allure.title('Delete Project')
def test_delete_project(headers):
    url = f'{base_url}/projects/{project_id}'

    res = requests.delete(url, headers=headers)
    assert res.status_code == 200

@allure.parent_suite("Smoke Test")
@allure.title('Verify Deletion')
def test_verify_delete(headers):

    with allure.step("Verify Project Deletion"):
        url = f'{base_url}/projects/{project_id}'

        res = requests.get(url, headers=headers)
        assert res.status_code == 404 

    with allure.step('Verify Task Deletion'):
        url =  f'{base_url}/tasks/{task_id}'

        res = requests.get(url, headers=headers)
        assert res.status_code == 404
