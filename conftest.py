# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytest
import random
import string

def generate_email():
    letters = string.ascii_lowercase
    username = ''.join(random.choice(letters) for _ in range(8))
    cohort = "20"  # Номер когорты
    random_digits = ''.join(random.choice(string.digits) for _ in range(3))
    return f"{username}_{cohort}_{random_digits}@yandex.ru"

def generate_password():
    return str(random.randint(100000, 900000))

def generate_name():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(8))

@pytest.fixture
def get_credentials():
    cohort_number = 20
    email = generate_email(cohort_number)
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
    driver.get("https://stellarburgers.nomoreparties.site/")
    yield driver
    driver.quit()

