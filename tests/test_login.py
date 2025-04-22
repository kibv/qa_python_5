from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from locators import LoginPageLocators, MainPageLocators, PersonalAccountLocators

class TestLogin:

    def perform_login(self, driver, email, password):
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(LoginPageLocators.EMAIL_INPUT)
            ).send_keys(email)

            driver.find_element(*LoginPageLocators.PASSWORD_INPUT).send_keys(password)
            driver.find_element(*LoginPageLocators.LOGIN_BUTTON).click()

            WebDriverWait(driver, 10).until(
                lambda d: "/" in d.current_url or "account" in d.current_url
            )
            return True
        except TimeoutException:
            return False

    def test_login_via_main_page_button(self, driver, registered_user):
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(MainPageLocators.LOGIN_BUTTON)
        ).click()

        assert self.perform_login(driver, registered_user["email"], registered_user["password"]), \
            "Не удалось войти через кнопку на главной странице"

    def test_login_via_personal_account_button(self, driver, registered_user):
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(MainPageLocators.PERSONAL_ACCOUNT_BUTTON)
        ).click()

        assert self.perform_login(driver, registered_user["email"], registered_user["password"]), \
            "Не удалось войти через кнопку 'Личный кабинет'"

    def test_login_via_registration_form(self, driver, registered_user):
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(MainPageLocators.LOGIN_BUTTON)
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(MainPageLocators.REGISTER_LINK)
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(LoginPageLocators.LOGIN_LINK)
        ).click()

        assert self.perform_login(driver, registered_user["email"], registered_user["password"]), \
            "Не удалось войти через форму регистрации"

    def test_login_via_password_recovery_form(self, driver, registered_user):
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(MainPageLocators.LOGIN_BUTTON)
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(PersonalAccountLocators.RECOVERY_LINK)
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(LoginPageLocators.LOGIN_LINK)
        ).click()

        assert self.perform_login(driver, registered_user["email"], registered_user["password"]), \
            "Не удалось войти через форму восстановления пароля"