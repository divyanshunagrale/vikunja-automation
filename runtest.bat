@echo off
cls
echo =============================
echo  VIKUNJA AUTOMATION TEST RUN
echo =============================
echo.
echo Select test suite to run:
echo 1. Smoke
echo 2. Sanity
set /p choice=Enter choice [1/2]:

if "%choice%"=="1" (
    echo Running SMOKE tests...
    pytest -m smoke --alluredir=Reports\allure-smoke
    echo.
    echo Serving Allure Report...
    allure serve Reports\allure-smoke
) else if "%choice%"=="2" (
    echo Running SANITY tests...
    pytest -m sanity --alluredir=Reports\allure-sanity
    echo.
    echo Serving Allure Report...
    allure serve Reports\allure-sanity
) else (
    echo Invalid choice. Please run the script again and enter 1 or 2.
)
pause