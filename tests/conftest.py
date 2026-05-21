import pytest
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.db_helper import DatabaseHelper
from pages.payment_page import PaymentPage

load_dotenv()


@pytest.fixture(scope="session")
def db():
    """Фикстура для подключения к базе данных"""
    helper = DatabaseHelper()
    yield helper
    helper.close()


@pytest.fixture(scope="function")
def clear_db(db):
    """Фикстура для очистки таблиц перед каждым тестом"""
    db.clear_tables()
    yield
    db.clear_tables()


@pytest.fixture(scope="function")
def driver():
    # Selenium Manager will auto-download the appropriate driver
    options = Options()
    options.add_argument("--headless")  # run without UI
    options.add_argument("--no-sandbox")  # required in many CI environments
    options.add_argument("--disable-dev-shm-usage")  # overcome limited /dev/shm size on Linux
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)

    app_url = os.getenv('APP_URL', 'http://localhost:8080')
    driver.get(app_url)

    # Дожидаемся загрузки страницы вместо time.sleep
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(("tag name", "body"))
    )

    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def payment_page(driver):
    """Фикстура для страницы оплаты"""
    page = PaymentPage(driver)
    page.select_payment_tab()
    return page


@pytest.fixture(scope="function")
def credit_page(driver):
    """Фикстура для страницы кредита"""
    page = PaymentPage(driver)
    page.select_credit_tab()
    return page


@pytest.fixture(scope="function", params=["payment", "credit"])
def payment_or_credit_page(request, driver):
    """Параметризованная фикстура для обеих вкладок"""
    page = PaymentPage(driver)
    if request.param == "payment":
        page.select_payment_tab()
    else:
        page.select_credit_tab()
    return page