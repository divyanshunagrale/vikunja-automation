import requests
import allure
import pytest

pytestmark = pytest.mark.sanity

@allure.parent_suite("Sanity Test")
@allure.title('Create Team')
@pytest.mark.order(1)
@pytest.mark.dependency()
def test_create_team(config, headers):
    with allure.step("Create Team"):
        url = f"{config['base_url']}/teams"

        res = requests.put(url, json=config['teams'], headers=headers)
        allure.attach(str(res.json()), name="Create Team Response", attachment_type=allure.attachment_type.JSON)
        assert res.status_code == 201
        assert res.json()['name'] == config['teams']['name']
        assert res.json()['description'] == config['teams']['description']

        global team
        team = res.json()


@allure.parent_suite("Sanity Test")
@allure.title('Add user 2')
@pytest.mark.order(2)
@pytest.mark.dependency(depends=["test_create_team"])
def test_add_user(config, headers):
    with allure.step("Add User 2 to team"):
        global team
        url = f"{config['base_url']}/teams/{team['id']}/members"

        payload = {
            'username': config['users']['teamuser']['username']
        }

        res = requests.put(url, json=payload, headers=headers)
        allure.attach(str(res.json()), name="Add team member Response", attachment_type=allure.attachment_type.JSON)
        assert res.status_code == 201
        assert res.json()['username'] == config['users']['teamuser']['username']


@allure.parent_suite("Sanity Test")
@allure.title('Share project')
@pytest.mark.order(3)
@pytest.mark.dependency(depends=["test_create_team"])
def test_share_project(config, headers):
    with allure.step("Get project info"):
        url = f"{config['base_url']}/projects"

        res = requests.put(url, json=config['projects'], headers=headers)
        allure.attach(str(res.json()), name="Get one project Response", attachment_type=allure.attachment_type.JSON)
        assert res.status_code == 201
        assert res.json()['title'] == config['projects']['title']
        assert res.json()['description'] == config['projects']['description']

        global project
        project = res.json()

    with allure.step("Share project with team"):
        global team
        payload = {
            'team_id': team['id'],
            'right': 1
        }

        url = f"{config['base_url']}/projects/{project['id']}/teams"

        res = requests.put(url ,json=payload, headers=headers)
        allure.attach(str(res.json()), name="Share project Response", attachment_type=allure.attachment_type.JSON)
        assert res.status_code == 201
        assert res.json()['team_id'] == team['id']
        assert res.json()['right'] == 1


@allure.parent_suite("Sanity Test")
@allure.title('Assign Task to user 2')
@pytest.mark.order(4)
@pytest.mark.dependency(depends=["test_add_user", "test_share_project"])
def test_assign_task(config, headers):
    with allure.step("Get user 2 info"):
        url = f"{config['base_url']}/users"
        params = {
            's': config['users']['teamuser']['username']
        }
        res = requests.get(url, params=params, headers=headers)
        allure.attach(str(res.json()), name="Get user Response", attachment_type=allure.attachment_type.JSON)
        assert res.status_code == 200
        assert res.json()[0]['username'] == config['users']['teamuser']['username']
        global user2_info
        user2_info = res.json()[0]

    with allure.step("Create task for sharing"):
        global project
        url = f"{config['base_url']}/projects/{project['id']}/tasks"
        res = requests.put(url, json=config['tasks'], headers=headers)
        allure.attach(str(res.json()), name="Create Task Response", attachment_type=allure.attachment_type.JSON)
        assert res.status_code == 201
        assert res.json()['title'] == config['tasks']['title']
        assert res.json()['description'] == config['tasks']['description']

        global task
        task = res.json()

    with allure.step("Assign user 2 to create task"):
        url = f"{config['base_url']}/tasks/{task['id']}/assignees"
        payload = {
            'user_id': user2_info['id']
        }
        res = requests.put(url, json=payload, headers=headers)
        allure.attach(str(res.json()), name="Assign task Response", attachment_type=allure.attachment_type.JSON)
        assert res.status_code == 201
        assert res.json()['user_id'] == user2_info['id']



@allure.parent_suite("Sanity Test")
@allure.title('Verify for user 2')
@pytest.mark.order(5)
@pytest.mark.dependency(depends=["test_assign_task"])
def test_verify(config):
    with allure.step("Login with user 2"):
        payload = {
            'username': config['users']['teamuser']['username'],
            'password': config['users']['teamuser']['password']
        }
        url = f"{config['base_url']}/login"
        res = requests.post(url, json=payload)
        allure.attach(str(res.json()), name="Login Response", attachment_type=allure.attachment_type.JSON)
        assert res.status_code == 200, "Login Failed"
        assert "token" in res.json(), "Token not found in response"


    with allure.step("Verify user 2 can see and is assigned to task"):
        global user2_header, task
        user2_header = {"Authorization": f"Bearer {res.json()['token']}"}

        url = f"{config['base_url']}/tasks/{task['id']}"
        res = requests.get(url, headers=user2_header)
        allure.attach(str(res.json()), name="Get Task Response", attachment_type=allure.attachment_type.JSON)
        assert res.status_code == 200
        assignees = res.json().get('assignees', [])
        with allure.step("Check assignee and creator of the task"):
            assert res.json()['created_by']['username'] == config['users']['test_user']['username']
            assert any(a['username'] == config['users']['teamuser']['username'] for a in assignees)


    
@allure.parent_suite("Sanity Test")
@allure.title('Remove user 2')
@pytest.mark.order(6)
@pytest.mark.dependency(depends=["test_verify"])
def test_remove_user2(config, headers):
    with allure.step("Remove user 2 from team"):
        global team, user2_info, user2_header
        url = f"{config['base_url']}/teams/{team['id']}/members/{user2_info['username']}"

        res = requests.delete(url, headers=headers)
        assert res.status_code == 200

        url = f"{config['base_url']}/tasks/{task['id']}"
        res = requests.get(url, headers=user2_header)
        allure.attach(str(res.json()), name="Remove user Response", attachment_type=allure.attachment_type.JSON)
        assert res.status_code == 403
        assert res.json()['message'] == "You don't have the right to see this"



@allure.parent_suite("Sanity Test")
@allure.title('Delete Team and Clean up')
@pytest.mark.order(7)
@pytest.mark.dependency(depends=["test_share_project"])
def test_delete_team_and_cleanup(config, headers):
    with allure.step("Delete team"):
        global team, project
        url = f"{config['base_url']}/teams/{team['id']}"
        res = requests.delete(url, headers=headers)
        allure.attach(str(res.json()), name="Delete Team Response", attachment_type=allure.attachment_type.JSON)
        assert res.status_code == 200
        assert res.json()['message'] == "Successfully deleted."

    with allure.step("Delete project"):
        url = f"{config['base_url']}/projects/{project['id']}"
        res = requests.delete(url, headers=headers)
        allure.attach(str(res.json()), name="Delete Project Response", attachment_type=allure.attachment_type.JSON)
        assert res.status_code == 200
        assert res.json()['message'] == "Successfully deleted."
