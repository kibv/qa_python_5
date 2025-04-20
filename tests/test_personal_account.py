from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def test_go_to_personal_account(driver, registered_user):
    driver.get("https://stellarburgers.nomoreparties.site/login")

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[text()='Вход']"))
    )

    email_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='name']"))
    )
    email_input.send_keys(registered_user["email"])

    password_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='Пароль']"))
    )
    password_input.send_keys(registered_user["password"])

    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Войти']"))
    )
    driver.execute_script("arguments[0].click();", login_button)

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h1[text()='Соберите бургер']"))
    )
    account_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/account']"))
    )
    driver.execute_script("arguments[0].click();", account_button)

    try:
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, "//a[text()='Профиль']"))
        )
        assert "account" in driver.current_url
    except TimeoutException:
        driver.save_screenshot("personal_account_error.png")
        raise

def test_logout_from_personal_account(driver, registered_user):
    driver.get("https://stellarburgers.nomoreparties.site/login")

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[text()='Вход']"))
    )

    driver.find_element(By.XPATH, "//input[@name='name']").send_keys(registered_user["email"])
    driver.find_element(By.XPATH, "//input[@name='Пароль']").send_keys(registered_user["password"])

    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Войти']"))
    )
    driver.execute_script("arguments[0].click();", login_button)

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h1[text()='Соберите бургер']"))
    )

    account_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/account']"))
    )
    driver.execute_script("arguments[0].click();", account_button)

    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//a[text()='Профиль']"))
    )

    logout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='Выход']"))
    )
    driver.execute_script("arguments[0].click();", logout_button)

    WebDriverWait(driver, 10).until(
        EC.url_contains("/login")
    )

def test_navigate_from_account_to_constructor(driver, registered_user):
    driver.get("https://stellarburgers.nomoreparties.site/login")

    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[text()='Вход']"))
    )

    driver.find_element(By.XPATH, "//input[@name='name']").send_keys(registered_user["email"])
    driver.find_element(By.XPATH, "//input[@name='Пароль']").send_keys(registered_user["password"])

    login_button = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='Войти']"))
    )
    driver.execute_script("arguments[0].click();", login_button)

    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//h1[text()='Соберите бургер']"))
    )

    account_button = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/account']"))
    )
    driver.execute_script("arguments[0].click();", account_button)

    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//a[text()='Профиль']"))
    )

    constructor_button = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//p[text()='Конструктор']"))
    )
    driver.execute_script("arguments[0].click();", constructor_button)

    WebDriverWait(driver, 15).until(
        EC.url_to_be("https://stellarburgers.nomoreparties.site/")
    )

    account_button = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/account']"))
    )
    driver.execute_script("arguments[0].click();", account_button)

    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//a[text()='Профиль']"))
    )

    try:
        logo = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'AppHeader_header__logo')]//a"))
        )

        print(f"Current URL before logo click: {driver.current_url}")

        driver.execute_script("""
            try {
                arguments[0].click();
            } catch(e) {
                console.error('Logo click error:', e);
                throw e;
            }
        """, logo)

        WebDriverWait(driver, 20).until(
            lambda d: d.current_url in [
                "https://stellarburgers.nomoreparties.site/",
                "https://stellarburgers.nomoreparties.site"
            ]
        )

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h1[text()='Соберите бургер']"))
        )

        print(f"Current URL after logo click: {driver.current_url}")

    except Exception as e:
        driver.save_screenshot("logo_click_failure.png")
        print(f"Page source at failure:\n{driver.page_source[:2000]}")  # Логируем часть HTML для отладки
        raise