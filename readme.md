# Vikunja API Automation
This project contains automated test suites for the [Vikunja](https://vikunja.io) task management API, written using **Python**, `pytest`, `requests`, and `allure-pytest`.

It is designed to simulate real-world QA workflows like authentication, project/task management, team collaboration, and file attachments — with clear reporting and test control.
> **Note:** This project is intended as a demonstration of API automation practices and does not aim to provide complete test coverage of the Vikunja API.

---
## Project Goals
- Showcase professional QA automation skills
- Test core Vikunja workflows: auth, project/task management, team sharing
- Practice structuring scalable test suites  
- Generate and serve **Allure Reports**

---
## Folder Overview

- `FunctionalAutomation/Smoke/` – Smoke tests for basic health checks
- `FunctionalAutomation/Sanity/` – Feature-level tests for auth, projects, tasks, and teams
- `config.example.yaml` – Template config file with dummy test data
- `Reports/` – Output folder for Allure reports (auto-generated)
- `runtest.bat`, `run_tests.sh` – Local runners for Windows/Linux
---
## Getting Started
### Pre-requisites
Have a local instance of [Vikunja installed](https://vikunja.io/docs/installing).
 1.  ### Clone the repo and create config
```
git clone https://github.com/divyanshunagrale/vikunja-automation.git
cd vikunja-automation
cp config.example.yaml config.yaml
```
#### Configure `config.yaml`
`config.yaml` is not explicitly provided for security reasons. Instead a `config.example.yaml` file is provided for use. After copying the example file, make a few minimal changes:
- Register test users on your local Vikunja instance
- `test_user` is used for almost all test cases
- `teamuser` is only required for team-related test cases (only in `test_team.py` sanity test)
- Ensure the `base_url` points to your running Vikunja API (e.g. `http://localhost:3456/api/v1`)

2. ### Set up a Python environment
```
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
3. ### Run tests
With an Vikunja instance running, you can run tests
#### Manually:
```
# Smoke suite
pytest FunctionalAutomation/Smoke -m smoke --alluredir=Reports/allure-smoke

# Sanity suite
pytest FunctionalAutomation/Sanity -m sanity --alluredir=Reports/allure-sanity

# Serve report
allure serve Reports/aullre-smoke
allure serve Reports/allure-sanity
```
#### Using automated scripts:
```
source runtest.sh # For Linux
runtest.bat # For Windows
```
----------

## Highlights
-   `pytest-order`, `pytest-dependency` for deterministic test control
    
-   `@allure.step`, `@allure.attach` for detailed reporting
    
-   Fixtures for session and auth handling
    
-   File upload & team collaboration tests
    
-   `config.example.yaml` provided for safe reuse
----------

## Feedback & Contributions

This project is for educational and portfolio purposes only.  
Feel free to fork it, test it, or use it as a template!

----------

## Resources

-   [Vikunja API Docs](https://try.vikunja.io/api/v1/docs) (Public Instance, you can find your api docs under `/api/v1/docs` of your instance)
    
-   [Allure Reporting](https://docs.qameta.io/allure/)
    
-   [Pytest Docs](https://docs.pytest.org/en/stable/)