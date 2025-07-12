import requests
import allure
import os
import pytest

pytestmark = pytest.mark.sanity

@allure.parent_suite("Sanity Test")
@allure.title('Create Task')
@pytest.mark.order(1)
@pytest.mark.dependency()
def test_create_task(config, headers):
    with allure.step("Create a new project"):

        url = f"{config['base_url']}/projects"

        res = requests.put(url, json=config['projects'], headers=headers)
        allure.attach(str(res.json()), name="Created Project", attachment_type=allure.attachment_type.JSON)
        assert res.status_code == 201
        assert res.json()['title'] == config['projects']['title']
        assert res.json()['description'] == config['projects']['description']

        global project_id, task
        project_id = res.json()['id']

    with allure.step("Create a task inside the project"):

        url = f"{config['base_url']}/projects/{project_id}/tasks"
        res = requests.put(url, json=config['tasks'], headers=headers)
        allure.attach(str(res.json()), name="Created Task", attachment_type=allure.attachment_type.JSON)
        assert res.status_code == 201
        assert res.json()['title'] == config['tasks']['title']
        assert res.json()['description'] == config['tasks']['description']

        task = res.json()



@allure.parent_suite("Sanity Test")
@allure.title('Update Task')
@pytest.mark.order(2)
@pytest.mark.dependency(depends=["test_create_task"])
def test_update_task(config, headers):
    with allure.step("Update and favorite the Task"):
        global task
        url = f"{config['base_url']}/tasks/{task['id']}"

        payload = {
            'description': config['updated_description'],
            'is_favorite': True
        }

        res = requests.post(url, json=payload, headers=headers)
        allure.attach(str(res.json()), name="Task update Response", attachment_type=allure.attachment_type.JSON)
        assert res.status_code == 200
        assert res.json()['description'] == config['updated_description']

        task = res.json()


@allure.parent_suite("Sanity Test")
@allure.title('Favorite Task')
@pytest.mark.order(3)
@pytest.mark.dependency(depends=["test_update_task"])
def test_is_favorite_task(config, headers):
    with allure.step("Get 'Favorite' project tasks views"):
        url = f"{config['base_url']}/projects/-1"

        res = requests.get(url=url, headers=headers)
        allure.attach(str(res.json()), name="'Favorite' Project Response", attachment_type=allure.attachment_type.JSON)
        assert res.status_code == 200
        view = res.json()['views'][0]['id']

    with allure.step("Get tasks in favorites"):
        global task
        url = f"{config['base_url']}/projects/-1/views/{view}/tasks"
        res = requests.get(url=url, headers=headers)
        allure.attach(str(res.json()), name="'Favorite' Project Tasks Response", attachment_type=allure.attachment_type.JSON)
        assert res.status_code == 200

        ids = [task['id'] for task in res.json()]
        project_ids = [task['project_id'] for task in res.json()]

        assert task['id'] in ids
        assert task['project_id'] in project_ids


@allure.parent_suite("Sanity Test")
@allure.title('Attach File in Task')
@pytest.mark.order(4)
@pytest.mark.dependency(depends=["test_create_task"])
def test_attach(config, headers):
    with allure.step("Prepare file for attachment"):
        file_path = os.path.join(os.path.dirname(__file__), "resources", "sample.txt")
        assert os.path.exists(file_path), "Attachment file not found"

    with allure.step("Attach file to task"):
        global task
        url = f"{config['base_url']}/tasks/{task['id']}/attachments"
        with open(file_path, 'rb') as f:
            files = {
                'files': f
            }
            res = requests.put(url, files=files, headers=headers)
            allure.attach(str(res.json()), name="Attach file Response", attachment_type=allure.attachment_type.JSON)
            assert res.status_code == 200
            assert res.json().get("errors") == None



@allure.parent_suite("Sanity Test")
@allure.title('Add Comment')
@pytest.mark.order(5)
@pytest.mark.dependency(depends=["test_create_task"])
def test_comment(config, headers):
    with allure.step("Add comment to task"):
        global task
        url = f"{config['base_url']}/tasks/{task['id']}/comments"
        
        res = requests.put(url, json=config['comments'], headers=headers)
        allure.attach(str(res.json()), name="Add comment Response", attachment_type=allure.attachment_type.JSON)
        assert res.status_code == 201
        assert res.json()['comment'] == config['comments']['comment']


@allure.parent_suite("Sanity Test")
@allure.title('Delete Task and Clean up')
@pytest.mark.order(6)
@pytest.mark.dependency(depends=["test_create_task"])
def test_delete_task(config, headers):
    with allure.step("Delete task"):
        global task
        url = f"{config['base_url']}/tasks/{task['id']}"

        res = requests.delete(url, headers=headers)
        allure.attach(str(res.json()), name="Delete task Response", attachment_type=allure.attachment_type.JSON)
        assert res.status_code == 200
        assert res.json()['message'] == "Successfully deleted."


    with allure.step("Delete Project"):
        url = f"{config['base_url']}/projects/{project_id}"

        res = requests.delete(url, headers=headers)
        allure.attach(str(res.json()), name="Delete project Response", attachment_type=allure.attachment_type.JSON)
        assert res.status_code == 200
        assert res.json()['message'] == "Successfully deleted."
