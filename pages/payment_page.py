# pages/payment_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time


class PaymentPage(BasePage):
    # Локаторы
    PAYMENT_TAB = (By.XPATH, "//button[contains(., 'Купить')]")
    CREDIT_TAB = (By.XPATH, "//button[contains(., 'Купить в кредит')]")

    # Локаторы полей ввода
    CARD_NUMBER = (By.CSS_SELECTOR, "input[placeholder='0000 0000 0000 0000']")
    MONTH = (By.CSS_SELECTOR, "input[placeholder='08']")
    YEAR = (By.CSS_SELECTOR, "input[placeholder='22']")
    OWNER = (By.XPATH, "//div[contains(@class, 'input')][.//input[@class='input__control']][not(./input/@placeholder)]//input")
    CVC = (By.CSS_SELECTOR, "input[placeholder='999']")

    # Кнопка продолжения
    CONTINUE_BUTTON = (By.XPATH, "//button[normalize-space()='Продолжить']")

    # Нотификации
    SUCCESS_NOTIFICATION = (By.CSS_SELECTOR, ".notification_status_ok")
    SUCCESS_NOTIFICATION_ALT = (By.XPATH, "//div[contains(@class, 'notification') and contains(@class, 'status_ok')]")
    SUCCESS_TEXT = (By.XPATH, "//div[contains(@class, 'notification')]//div[contains(text(), 'Успешно')]")

    ERROR_NOTIFICATION = (By.CSS_SELECTOR, ".notification_status_error")
    ERROR_NOTIFICATION_ALT = (By.XPATH, "//div[contains(@class, 'notification') and contains(@class, 'status_error')]")

    # Валидационные сообщения
    INVALID_FORMAT = (By.CSS_SELECTOR, ".input__sub")

    # Локаторы для ошибок под конкретными полями
    CARD_NUMBER_ERROR = (By.XPATH, "//input[@placeholder='0000 0000 0000 0000']/following-sibling::span[@class='input__sub']")
    MONTH_ERROR = (By.XPATH, "//input[@placeholder='08']/following-sibling::span[@class='input__sub']")
    YEAR_ERROR = (By.XPATH, "//input[@placeholder='22']/following-sibling::span[@class='input__sub']")
    CVC_ERROR = (By.XPATH, "//input[@placeholder='999']/following-sibling::span[@class='input__sub']")

    def select_payment_tab(self):
        """Выбор вкладки 'Купить'"""
        try:
            self.click(self.PAYMENT_TAB)
            time.sleep(0.5)
            self.wait_for_form_ready()
        except:
            pass

    def select_credit_tab(self):
        """Выбор вкладки 'Купить в кредит'"""
        try:
            self.click(self.CREDIT_TAB)
            time.sleep(0.5)
            self.wait_for_form_ready()
        except:
            pass

    def fill_card_data(self, card_number, month, year, owner, cvc):
        """Заполнение формы данными карты"""
        self.input_text(self.CARD_NUMBER, card_number)
        time.sleep(0.2)
        self.input_text(self.MONTH, month)
        time.sleep(0.2)
        self.input_text(self.YEAR, year)
        time.sleep(0.2)
        self.input_text_by_index(3, owner)
        time.sleep(0.2)
        self.input_text(self.CVC, cvc)
        time.sleep(0.3)

    def input_text_by_index(self, index, text):
        """Ввод текста в поле по его индексу"""
        wait = WebDriverWait(self.driver, 10)
        inputs = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input.input__control"))
        )
        if len(inputs) > index:
            inputs[index].clear()
            inputs[index].send_keys(text)
        else:
            raise Exception(f"Input index {index} not found. Total inputs: {len(inputs)}")

    def submit_form(self):
        """Отправка формы"""
        time.sleep(0.5)

        # Поиск через JS по тексту
        try:
            button = self.driver.execute_script(
                "return Array.from(document.querySelectorAll('button')).find(btn => btn.textContent.includes('Продолжить'))"
            )
            if button:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                time.sleep(0.3)
                self.driver.execute_script("arguments[0].click();", button)
                time.sleep(2)
                return
        except Exception as e:
            print(f"JS click failed: {e}")

        # Альтернативные локаторы
        wait = WebDriverWait(self.driver, 10)
        locators = [
            (By.XPATH, "//button[normalize-space()='Продолжить']"),
            (By.XPATH, "//button[contains(text(), 'Продолжить')]"),
            (By.XPATH, "//button[contains(., 'Продолжить')]"),
        ]

        for locator in locators:
            try:
                button = wait.until(EC.element_to_be_clickable(locator))
                self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                time.sleep(0.3)
                button.click()
                time.sleep(2)
                return
            except:
                continue

        raise Exception("Could not find or click 'Продолжить' button")

    def is_success_visible(self):
        """Проверка видимости уведомления об успехе"""
        try:
            wait = WebDriverWait(self.driver, 15)
            success_locators = [
                self.SUCCESS_NOTIFICATION,
                self.SUCCESS_NOTIFICATION_ALT,
                self.SUCCESS_TEXT,
                (By.XPATH, "//div[contains(@class, 'notification')][contains(text(), 'Успешно')]"),
                (By.XPATH, "//div[contains(., 'Успешно') and contains(@class, 'notification')]")
            ]

            for locator in success_locators:
                try:
                    if wait.until(EC.visibility_of_element_located(locator)):
                        return True
                except:
                    continue
            return False
        except:
            return False

    def is_error_visible(self):
        """Проверка видимости уведомления об ошибке"""
        try:
            wait = WebDriverWait(self.driver, 10)
            error_locators = [
                self.ERROR_NOTIFICATION,
                self.ERROR_NOTIFICATION_ALT,
                (By.XPATH, "//div[contains(@class, 'notification')][contains(text(), 'Ошибка')]")
            ]

            for locator in error_locators:
                try:
                    if wait.until(EC.visibility_of_element_located(locator)):
                        return True
                except:
                    continue
            return False
        except:
            return False

    def get_validation_errors(self):
        """Получение текстов всех ошибок валидации"""
        try:
            # Ждем появления ошибок
            time.sleep(1)
            errors = self.driver.find_elements(*self.INVALID_FORMAT)
            error_texts = [error.text for error in errors if error.text]

            # Также проверяем специфичные ошибки полей
            card_error = self.driver.find_elements(*self.CARD_NUMBER_ERROR)
            month_error = self.driver.find_elements(*self.MONTH_ERROR)
            year_error = self.driver.find_elements(*self.YEAR_ERROR)
            cvc_error = self.driver.find_elements(*self.CVC_ERROR)

            for error in card_error + month_error + year_error + cvc_error:
                if error.text:
                    error_texts.append(error.text)

            return error_texts
        except:
            return []

    def wait_for_form_ready(self):
        """Ожидание появления всех полей формы"""
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located(self.CARD_NUMBER))
            wait.until(EC.presence_of_element_located(self.MONTH))
            wait.until(EC.presence_of_element_located(self.YEAR))
            wait.until(EC.presence_of_element_located(self.CVC))
        except:
            pass

    def take_screenshot(self, name="screenshot"):
        """Делает скриншот для отладки"""
        try:
            self.driver.save_screenshot(f"{name}.png")
            print(f"Screenshot saved: {name}.png")
        except Exception as e:
            print(f"Failed to take screenshot: {e}")

    def clear_form(self):
        """Очистка формы"""
        fields = [self.CARD_NUMBER, self.MONTH, self.YEAR, self.OWNER, self.CVC]
        for field in fields:
            try:
                element = self.find_element(field)
                element.clear()
            except:
                pass