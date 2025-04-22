import pytest
import random
import string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from urls import BASE_URL
from locators import MainPageLocators

def generate_email():
    letters = string.ascii_lowercase
    username = ''.join(random.choice(letters) for _ in range(8))
    cohort = "20"
    random_digits = ''.join(random.choice(string.digits) for _ in range(3))
    return f"{username}_{cohort}_{random_digits}@yandex.ru"

def generate_password():
    return str(random.randint(100000, 900000))

def generate_name():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(8))

@pytest.fixture
def get_credentials():
    email = generate_email()
    password = generate_password()
    return email, password

@pytest.fixture
def registered_user():
    return {
        "email": "test_user_09_123@example.com",
        "password": "password123"
    }

@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(BASE_URL)
    yield driver
    driver.quit()

@pytest.fixture(autouse=True, scope="function")  # Меняем class -> function
def auto_load_main_page(driver):
    driver.get(BASE_URL)
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(MainPageLocators.CONSTRUCTOR_HEADER)
    )
    yield