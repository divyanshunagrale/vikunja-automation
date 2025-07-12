import pytest, requests
from FunctionalAutomation.utils.load_config import load_config

@pytest.fixture(scope="session")
def config():
    return load_config()

@pytest.fixture(scope="session")
def auth_token(config):
    payload = {
        'username': config['users']['test_user']['username'],
        'password': config['users']['test_user']['password']
    }
    url = f"{config['base_url']}/login"

    res = requests.post(url, json=payload)
    assert res.status_code == 200, "Login Failed"

    return res.json()['token']


@pytest.fixture(scope="session")
def headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}