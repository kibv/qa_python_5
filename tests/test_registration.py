import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import generate_email, generate_name

class TestRegistration:
    def fill_registration_form(self, driver, name, email, password):
        name_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//fieldset[1]//input")))
        name_field.send_keys(name)

        email_field = driver.find_elements(By.XPATH, "//fieldset//input")[1]
        email_field.send_keys(email)

        password_field = driver.find_element(By.XPATH, "//input[@type='password']")
        password_field.send_keys(password)

    def test_successful_registration(self, driver):
        name = generate_name()
        email = generate_email()
        password = "validPassword123"

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Войти в аккаунт')]"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[text()='Зарегистрироваться']"))
        ).click()

        self.fill_registration_form(driver, name, email, password)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Зарегистрироваться']"))
        ).click()

        try:
            WebDriverWait(driver, 10).until(
                EC.url_contains("/login")
            )
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='name']"))
            )
            assert True
        except:
            driver.save_screenshot("registration_failed.png")
            pytest.fail("Не удалось зарегистрироваться или перейти на страницу входа")

    @pytest.mark.parametrize("invalid_password", ["12345", "qwert", "pass"])
    def test_invalid_password_registration(self, driver, invalid_password):
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Войти в аккаунт')]"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[text()='Зарегистрироваться']"))
        ).click()

        name = generate_name()
        email = generate_email()
        self.fill_registration_form(driver, name, email, invalid_password)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Зарегистрироваться']"))
        ).click()

        error = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//p[contains(@class, 'input__error')]"))
        )
        assert error.text == "Некорректный пароль", "Неверное сообщение об ошибке для некорректного пароля"