from selenium.webdriver.common.action_chains import ActionChains
import time
from locators import ConstructorPageLocators

class TestConstructor:
    def switch_to_section(self, driver, locator):
        section_tab = driver.find_element(*locator)
        ActionChains(driver).move_to_element(section_tab).click().perform()
        time.sleep(3)
        section_classes = section_tab.get_attribute("class")
        return "tab_tab_type_current" in section_classes

    def test_buns_section(self, driver):
        self.switch_to_section(driver, ConstructorPageLocators.SAUCES_SECTION)

        is_active = self.switch_to_section(driver, ConstructorPageLocators.BUNS_SECTION)
        assert is_active, "Раздел 'Булки' не стал активным после переключения"

    def test_sauces_section(self, driver):
        is_active = self.switch_to_section(driver, ConstructorPageLocators.SAUCES_SECTION)
        assert is_active, "Раздел 'Соусы' не стал активным после переключения"

    def test_fillings_section(self, driver):
        is_active = self.switch_to_section(driver, ConstructorPageLocators.FILLINGS_SECTION)
        assert is_active, "Раздел 'Начинки' не стал активным после переключения"
