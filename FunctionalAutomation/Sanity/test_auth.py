import requests
import allure
import pytest

pytestmark = pytest.mark.sanity


@allure.parent_suite("Sanity Test")
@allure.title('Incorrect Credentials')
def test_incorrect_auth(config):
    with allure.step("Login with Incorrect Credentials"):
        payload = {
            'username': config['users']['test_user']['username'],
            'password': 'wrongpass'
        }
        url = f"{config['base_url']}/login"

        res = requests.post(url, json=payload)
        allure.attach(str(res.json()), name="Login Response", attachment_type=allure.attachment_type.JSON)
        assert res.status_code == 412
        assert res.json()["message"] == "Wrong username or password."


@allure.parent_suite("Sanity Test")
@allure.title('Missing Field')
@pytest.mark.parametrize("payload", [
    {"username": "onlyusername"},
    {"password": "onlypassword"},
    {}
])
def test_missing_field(config, payload):
    with allure.step("Login with Missing Field"):

        url = f"{config['base_url']}/login"

        res = requests.post(url, json=payload)
        allure.attach(str(res.json()), name="Login Response", attachment_type=allure.attachment_type.JSON)
        assert res.status_code == 400
        assert res.json()["message"] == "Please specify a username and a password."



@allure.parent_suite("Sanity Test")
@allure.title('Incorrect Field')
def test_incorrect_field(config):
    with allure.step("Login with Incorrect Field"):
        payload = {
            'usernaem': config['users']['test_user']['username'],
            'password': config['users']['test_user']['password']
        }
        url = f"{config['base_url']}/login"

        res = requests.post(url, json=payload)
        allure.attach(str(res.json()), name="Login Response", attachment_type=allure.attachment_type.JSON)
        assert res.status_code == 400
        assert res.json()["message"] == "Please specify a username and a password."



@allure.parent_suite("Sanity Test")
@allure.title('Correct Credentials')
def test_correct_auth(config):
    with allure.step("Login with Correct Credentials"):
        payload = {
            'username': config['users']['test_user']['username'],
            'password': config['users']['test_user']['password']
        }
        url = f"{config['base_url']}/login"

        res = requests.post(url, json=payload)
        allure.attach(str(res.json()), name="Login Response", attachment_type=allure.attachment_type.JSON)
        assert res.status_code == 200
        assert 'token' in res.json()

    