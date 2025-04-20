from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def test_go_to_personal_account(driver, registered_user):
    # Вход в систему
    driver.get("https://stellarburgers.nomoreparties.site/login")

    # Ожидаем появления формы входа
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[text()='Вход']"))
    )

    # Заполняем форму входа
    email_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='name']"))
    )
    email_input.send_keys(registered_user["email"])

    password_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='Пароль']"))
    )
    password_input.send_keys(registered_user["password"])

    # Ждем когда кнопка станет кликабельной
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Войти']"))
    )

    # Альтернативный способ клика через JavaScript
    driver.execute_script("arguments[0].click();", login_button)

    # Ожидаем загрузки главной страницы после входа
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h1[text()='Соберите бургер']"))
    )

    # Переход в личный кабинет через JavaScript
    account_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/account']"))
    )
    driver.execute_script("arguments[0].click();", account_button)

    # Проверка что мы в личном кабинете
    try:
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, "//a[text()='Профиль']"))
        )
        assert "account" in driver.current_url
    except TimeoutException:
        driver.save_screenshot("personal_account_error.png")
        raise

def test_logout_from_personal_account(driver, registered_user):
    # Вход в систему
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

    # Переход в личный кабинет
    account_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/account']"))
    )
    driver.execute_script("arguments[0].click();", account_button)

    # Ожидаем загрузки личного кабинета
    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//a[text()='Профиль']"))
    )

    # Выход из системы через JavaScript
    logout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='Выход']"))
    )
    driver.execute_script("arguments[0].click();", logout_button)

    # Проверка что перенаправило на страницу входа
    WebDriverWait(driver, 10).until(
        EC.url_contains("/login")
    )

def test_navigate_from_account_to_constructor(driver, registered_user):
    # Вход в систему
    driver.get("https://stellarburgers.nomoreparties.site/login")

    # Ожидаем форму входа
    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//h2[text()='Вход']"))
    )

    # Заполняем форму входа
    driver.find_element(By.XPATH, "//input[@name='name']").send_keys(registered_user["email"])
    driver.find_element(By.XPATH, "//input[@name='Пароль']").send_keys(registered_user["password"])

    # Кликаем кнопку входа через JavaScript
    login_button = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()='Войти']"))
    )
    driver.execute_script("arguments[0].click();", login_button)

    # Ожидаем главную страницу
    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, "//h1[text()='Соберите бургер']"))
    )

    # Переход в личный кабинет
    account_button = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/account']"))
    )
    driver.execute_script("arguments[0].click();", account_button)

    # Ожидаем загрузки личного кабинета
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//a[text()='Профиль']"))
    )

    # Переход в конструктор
    constructor_button = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//p[text()='Конструктор']"))
    )
    driver.execute_script("arguments[0].click();", constructor_button)

    # Проверка возврата на главную
    WebDriverWait(driver, 15).until(
        EC.url_to_be("https://stellarburgers.nomoreparties.site/")
    )

    # Снова переходим в личный кабинет
    account_button = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/account']"))
    )
    driver.execute_script("arguments[0].click();", account_button)

    # Ожидаем загрузки личного кабинета
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//a[text()='Профиль']"))
    )

    # Клик по логотипу с улучшенной обработкой
    try:
        # Альтернативный локатор для логотипа
        logo = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'AppHeader_header__logo')]//a"))
        )

        # Сохраняем текущий URL для отладки
        print(f"Current URL before logo click: {driver.current_url}")

        # Кликаем через JavaScript с обработкой возможных ошибок
        driver.execute_script("""
            try {
                arguments[0].click();
            } catch(e) {
                console.error('Logo click error:', e);
                throw e;
            }
        """, logo)

        # Проверяем URL с учетом возможного редиректа
        WebDriverWait(driver, 20).until(
            lambda d: d.current_url in [
                "https://stellarburgers.nomoreparties.site/",
                "https://stellarburgers.nomoreparties.site"
            ]
        )

        # Дополнительная проверка заголовка
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h1[text()='Соберите бургер']"))
        )

        print(f"Current URL after logo click: {driver.current_url}")

    except Exception as e:
        driver.save_screenshot("logo_click_failure.png")
        print(f"Page source at failure:\n{driver.page_source[:2000]}")  # Логируем часть HTML для отладки
        raise