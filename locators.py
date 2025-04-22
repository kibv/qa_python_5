from selenium.webdriver.common.by import By

class MainPageLocators:
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти в аккаунт']")
    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[text()='Конструктор']")
    PERSONAL_ACCOUNT_BUTTON = (By.XPATH, "//p[text()='Личный Кабинет']")
    REGISTER_LINK = (By.XPATH, "//a[text()='Зарегистрироваться']")
    CONSTRUCTOR_HEADER = (By.XPATH, "//h1[text()='Соберите бургер']")
    ACCOUNT_BUTTON = (By.XPATH, "//a[@href='/account']")
    LOGO = (By.XPATH, "//div[contains(@class, 'AppHeader_header__logo')]//a")

class LoginPageLocators:
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Войти')]")
    LOGIN_LINK = (By.XPATH, "//a[contains(text(), 'Войти')]")
    LOGIN_HEADER = (By.XPATH, "//h2[text()='Вход']")


class RegistrationPageLocators:
    NAME_FIELD = (By.XPATH, "//fieldset[1]//input")
    EMAIL_FIELD = (By.XPATH, "//fieldset[2]//input")
    PASSWORD_FIELD = (By.XPATH, "//input[@type='password']")
    REGISTER_BUTTON = (By.XPATH, "//button[text()='Зарегистрироваться']")
    PASSWORD_ERROR = (By.XPATH, "//p[contains(@class, 'input__error')]")

class PersonalAccountLocators:
    PROFILE_LINK = (By.XPATH, "//a[text()='Профиль']")
    LOGOUT_BUTTON = (By.XPATH, "//button[text()='Выход']")
    RECOVERY_LINK = (By.XPATH, "//a[contains(text(), 'Восстановить пароль')]")

class ConstructorPageLocators:
    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[text()='Конструктор']")
    BUNS_SECTION = (By.XPATH, "//span[text()='Булки']/..")
    SAUCES_SECTION = (By.XPATH, "//span[text()='Соусы']/..")
    FILLINGS_SECTION = (By.XPATH, "//span[text()='Начинки']/..")
    ACTIVE_SECTION = (By.CSS_SELECTOR, ".tab_tab_type_current")