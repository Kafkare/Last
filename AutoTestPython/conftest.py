import pytest, yaml, requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import WebDriverException
import logging

with open("./testdata.yaml") as f:
    testdata = yaml.safe_load(f)
    browser_name = testdata["browser"]

@pytest.fixture(scope="session")
def browser():
    if browser_name == "chrome":
        try:
            service = ChromeService(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            driver = webdriver.Chrome(service=service, options=options)
        except WebDriverException as e:
            logging.error(f"Ошибка при инициализации Chrome WebDriver: {e}")
            raise
    elif browser_name == "firefox":
        try:
            service = FirefoxService(GeckoDriverManager().install())
            options = webdriver.FirefoxOptions()
            driver = webdriver.Firefox(service=service, options=options)
        except WebDriverException as e:
            logging.error(f"Ошибка при инициализации Firefox WebDriver: {e}")
            raise
    else:
        raise ValueError(f"Неизвестный браузер: {browser_name}")

    yield driver
    driver.quit()

@pytest.fixture
def login():
    try:
        res = requests.post(
            testdata["base_url"] + "gateway/login",
            data={"username": testdata["username"], "password": testdata["password"]},
            timeout=10
        )
        res.raise_for_status()
        return res.json()["token"]
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Ошибка авторизации: {str(e)}")

@pytest.fixture
def testtext1():
    return "Test Post Title3"

@pytest.fixture
def post_data():
    return {
        "title": testdata["post_title"],
        "description": testdata["post_description"],
        "content": testdata["post_content"]
    }

@pytest.fixture
def created_post(login, post_data):
    try:
        header = {"X-Auth-Token": login}
        res = requests.post(
            testdata["base_url"] + "api/posts",
            headers=header,
            data=post_data,
            timeout=10
        )
        res.raise_for_status()
        assert res.status_code == 200
        return post_data
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Ошибка создания тестового поста: {str(e)}")

