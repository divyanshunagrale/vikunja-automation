import requests
import allure
import pytest

pytestmark = pytest.mark.sanity

@allure.parent_suite("Sanity Test")
@allure.title('Create Project')
@pytest.mark.order(1)
@pytest.mark.dependency()
def test_create_project(config, headers):
    with allure.step("Create project"):
        url = f"{config['base_url']}/projects"

        res = requests.put(url, json=config['projects'], headers=headers)
        allure.attach(str(res.json()), name="Create Project Response", attachment_type=allure.attachment_type.JSON)
        assert res.status_code == 201
        assert res.json()['title'] == config['projects']['title']
        assert res.json()['description'] == config['projects']['description']

        global project
        project = res.json()


@allure.parent_suite("Sanity Test")
@allure.title('Update Project')
@pytest.mark.order(2)
@pytest.mark.dependency(depends=["test_create_project"])
def test_update_project(config, headers):
    with allure.step("Update project"):
        global project
        url = f"{config['base_url']}/projects/{project['id']}"
        project['description'] = config['updated_description']
        res = requests.post(url, json=project, headers=headers)
        allure.attach(str(res.json()), name="Update Project Response", attachment_type=allure.attachment_type.JSON)
        assert res.status_code == 200
        assert res.json()['description'] == config['updated_description']



@allure.parent_suite("Sanity Test")
@allure.title('Delete Project')
@pytest.mark.order(3)
@pytest.mark.dependency(depends=["test_create_project"])
def test_delete_project(config, headers):
    with allure.step("Delete project"):
        global project
        url = f"{config['base_url']}/projects/{project['id']}"
        res = requests.delete(url, headers=headers)
        allure.attach(str(res.json()), name="Delete Project Response", attachment_type=allure.attachment_type.JSON)
        assert res.status_code == 200
        assert res.json()['message'] == "Successfully deleted."
