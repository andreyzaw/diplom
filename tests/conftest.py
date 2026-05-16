import pytest
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from utils.db_helper import DatabaseHelper

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
   # options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)

    app_url = os.getenv('APP_URL', 'http://localhost:8080')
    driver.get(app_url)

    yield driver
    driver.quit()

    import time
    time.sleep(2)