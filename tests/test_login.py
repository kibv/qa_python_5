from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class TestLogin:

    def perform_login(self, driver, email, password):
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@name='name']"))
            ).send_keys(email)

            driver.find_element(By.XPATH, "//input[@type='password']").send_keys(password)
            driver.find_element(By.XPATH, "//button[contains(text(), 'Войти')]").click()

            WebDriverWait(driver, 10).until(
                lambda d: "/" in d.current_url or "account" in d.current_url
            )
            return True
        except TimeoutException:
            return False

    def test_login_via_main_page_button(self, driver, registered_user):
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Войти в аккаунт')]"))
        ).click()

        assert self.perform_login(driver, registered_user["email"], registered_user["password"]), \
            "Не удалось войти через кнопку на главной странице"

    def test_login_via_personal_account_button(self, driver, registered_user):
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'account')]"))
        ).click()

        assert self.perform_login(driver, registered_user["email"], registered_user["password"]), \
            "Не удалось войти через кнопку 'Личный кабинет'"

    def test_login_via_registration_form(self, driver, registered_user):
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Войти в аккаунт')]"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Зарегистрироваться')]"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Войти')]"))
        ).click()

        assert self.perform_login(driver, registered_user["email"], registered_user["password"]), \
            "Не удалось войти через форму регистрации"

    def test_login_via_password_recovery_form(self, driver, registered_user):
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Войти в аккаунт')]"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Восстановить пароль')]"))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Войти')]"))
        ).click()

        assert self.perform_login(driver, registered_user["email"], registered_user["password"]), \
            "Не удалось войти через форму восстановления пароля"