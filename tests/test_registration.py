import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import generate_email, generate_password, generate_name
import time

class TestRegistration:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        driver.get("https://stellarburgers.nomoreparties.site/")
        yield

    def fill_registration_form(self, driver, name, email, password):
        """Заполняет форму регистрации"""
        # Ожидаем и заполняем поле имени
        name_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//fieldset[1]//input")))
        name_field.send_keys(name)

        # Заполняем поле email (второй input в форме)
        email_field = driver.find_elements(By.XPATH, "//fieldset//input")[1]
        email_field.send_keys(email)

        # Заполняем поле пароля (input с type='password')
        password_field = driver.find_element(By.XPATH, "//input[@type='password']")
        password_field.send_keys(password)

    def test_successful_registration(self, driver):
        # Генерируем уникальные данные
        name = generate_name()
        email = generate_email()
        password = "validPassword123"

        # Переходим на страницу регистрации
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Войти в аккаунт')]"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[text()='Зарегистрироваться']"))
        ).click()

        # Заполняем форму
        self.fill_registration_form(driver, name, email, password)

        # Кликаем кнопку регистрации
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Зарегистрироваться']"))
        ).click()

        # Ждем перехода на страницу входа (проверяем URL или наличие поля входа)
        try:
            WebDriverWait(driver, 10).until(
                EC.url_contains("/login")
            )
            # Проверяем наличие поля ввода email на странице входа
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='name']"))
            )
            assert True
        except:
            # Делаем скриншот для отладки
            driver.save_screenshot("registration_failed.png")
            pytest.fail("Не удалось зарегистрироваться или перейти на страницу входа")

    @pytest.mark.parametrize("invalid_password", ["12345", "qwert", "pass"])
    def test_invalid_password_registration(self, driver, invalid_password):
        # Переходим на страницу регистрации
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Войти в аккаунт')]"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[text()='Зарегистрироваться']"))
        ).click()

        # Заполняем форму
        name = generate_name()
        email = generate_email()
        self.fill_registration_form(driver, name, email, invalid_password)

        # Кликаем кнопку регистрации
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Зарегистрироваться']"))
        ).click()

        # Проверяем сообщение об ошибке
        error = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//p[contains(@class, 'input__error')]"))
        )
        assert error.text == "Некорректный пароль", "Неверное сообщение об ошибке для некорректного пароля"