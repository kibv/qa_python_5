import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

class TestConstructor:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        driver.get("https://stellarburgers.nomoreparties.site/")
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//h1[text()='Соберите бургер']"))
        )
        yield

    def switch_to_section(self, driver, section_name):
        """Переключается на указанный раздел и возвращает его активность"""
        section_tab = driver.find_element(By.XPATH, f"//span[text()='{section_name}']/..")
        ActionChains(driver).move_to_element(section_tab).click().perform()
        time.sleep(3)
        section_classes = section_tab.get_attribute("class")
        return "tab_tab_type_current" in section_classes

    def test_buns_section(self, driver):
        # Сначала переключаемся на Соусы
        self.switch_to_section(driver, "Соусы")

        # Затем переключаемся на Булки и проверяем активность
        is_active = self.switch_to_section(driver, "Булки")
        assert is_active, "Раздел 'Булки' не стал активным после переключения"

    def test_sauces_section(self, driver):
        # Переключаемся на Соусы и проверяем активность
        is_active = self.switch_to_section(driver, "Соусы")
        assert is_active, "Раздел 'Соусы' не стал активным после переключения"

    def test_fillings_section(self, driver):
        # Переключаемся на Начинки и проверяем активность
        is_active = self.switch_to_section(driver, "Начинки")
        assert is_active, "Раздел 'Начинки' не стал активным после переключения"