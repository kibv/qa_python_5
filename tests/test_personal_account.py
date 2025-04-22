from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from locators import LoginPageLocators, MainPageLocators, PersonalAccountLocators
from urls import LOGIN_URL, PROFILE_URL, BASE_URL

def test_go_to_personal_account(driver, registered_user):
    # Используем константу URL
    driver.get(LOGIN_URL)

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(LoginPageLocators.LOGIN_HEADER)
    )

    email_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(LoginPageLocators.EMAIL_INPUT)
    )
    email_input.send_keys(registered_user["email"])

    password_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(LoginPageLocators.PASSWORD_INPUT)
    )
    password_input.send_keys(registered_user["password"])

    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(LoginPageLocators.LOGIN_BUTTON)
    )
    driver.execute_script("arguments[0].click();", login_button)

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(MainPageLocators.CONSTRUCTOR_HEADER)
    )
    account_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(MainPageLocators.ACCOUNT_BUTTON)
    )
    driver.execute_script("arguments[0].click();", account_button)

    try:
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located(PersonalAccountLocators.PROFILE_LINK)
        )
        assert PROFILE_URL in driver.current_url
    except TimeoutException:
        driver.save_screenshot("personal_account_error.png")
        raise

def test_logout_from_personal_account(driver, registered_user):
    driver.get(LOGIN_URL)

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(LoginPageLocators.LOGIN_HEADER)
    )

    # Заполнение формы
    driver.find_element(*LoginPageLocators.EMAIL_INPUT).send_keys(registered_user["email"])
    driver.find_element(*LoginPageLocators.PASSWORD_INPUT).send_keys(registered_user["password"])

    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(LoginPageLocators.LOGIN_BUTTON)
    )
    driver.execute_script("arguments[0].click();", login_button)

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(MainPageLocators.CONSTRUCTOR_HEADER)
    )
    account_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(MainPageLocators.ACCOUNT_BUTTON)
    )
    driver.execute_script("arguments[0].click();", account_button)

    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(PersonalAccountLocators.PROFILE_LINK)
    )
    logout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(PersonalAccountLocators.LOGOUT_BUTTON)
    )
    driver.execute_script("arguments[0].click();", logout_button)

    WebDriverWait(driver, 10).until(
        EC.url_contains("/login")
    )

def test_navigate_from_account_to_constructor(driver, registered_user):
    driver.get(LOGIN_URL)

    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(LoginPageLocators.LOGIN_HEADER)
    )

    driver.find_element(*LoginPageLocators.EMAIL_INPUT).send_keys(registered_user["email"])
    driver.find_element(*LoginPageLocators.PASSWORD_INPUT).send_keys(registered_user["password"])

    login_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable(LoginPageLocators.LOGIN_BUTTON)
    )
    login_button.click()

    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(MainPageLocators.CONSTRUCTOR_HEADER)
    )

    account_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable(MainPageLocators.ACCOUNT_BUTTON)
    )
    account_button.click()

    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(PersonalAccountLocators.PROFILE_LINK)
    )

    constructor_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable(MainPageLocators.CONSTRUCTOR_BUTTON)
    )
    constructor_button.click()

    WebDriverWait(driver, 15).until(
        lambda d: BASE_URL in d.current_url
    )

    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(MainPageLocators.CONSTRUCTOR_HEADER)
    )