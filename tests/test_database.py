# tests/test_database.py
import pytest
import allure
from utils.data_generator import DataGenerator as Data

@allure.feature("Проверка базы данных")
class TestDatabase:

    @allure.title("DB-01: Запись после успешной оплаты")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_payment_record_after_success(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        payment_page.submit_form()

        assert payment_page.is_success_visible()

        payment = db.get_last_payment()
        assert payment is not None, "Запись в payment_entity не создана"

        status = db.get_payment_status()
        assert status == "APPROVED", f"Статус платежа: {status}"

        amount = db.get_payment_amount()
        assert amount == 45000, f"Сумма оплаты {amount}, ожидалась 45000"

    @allure.title("DB-02: Запись после успешного кредита")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_credit_record_after_success(self, credit_page, db, clear_db):
        credit_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        credit_page.submit_form()

        assert credit_page.is_success_visible()

        credit = db.get_last_credit()
        assert credit is not None, "Запись в credit_request_entity не создана"

        status = db.get_credit_status()
        assert status == "APPROVED", f"Статус кредита: {status}"

    @allure.title("DB-03: Запись в order_entity для оплаты")
    @allure.severity(allure.severity_level.NORMAL)
    def test_order_entity_for_payment(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        payment_page.submit_form()

        order = db.get_last_order()
        assert order is not None, "Запись в order_entity не создана"

    @allure.title("DB-03: Запись в order_entity для кредита")
    @allure.severity(allure.severity_level.NORMAL)
    def test_order_entity_for_credit(self, credit_page, db, clear_db):
        credit_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        credit_page.submit_form()

        order = db.get_last_order()
        assert order is not None, "Запись в order_entity не создана"

    @allure.title("DB-04: Запись после отклонённой карты")
    @allure.severity(allure.severity_level.NORMAL)
    def test_declined_payment_record(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_declined_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        payment_page.submit_form()

        status = db.get_payment_status()
        assert status == "DECLINED", f"Ожидался DECLINED, получен {status}"

    @allure.title("DB-05: Отсутствие утечки данных - оплата не создаёт кредит")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_no_data_leak_payment_to_credit(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        payment_page.submit_form()

        credit = db.get_last_credit()
        assert credit is None, "При оплате не должно быть записи в credit_request_entity"

    @allure.title("DB-05: Отсутствие утечки данных - кредит не создаёт оплату")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_no_data_leak_credit_to_payment(self, credit_page, db, clear_db):
        credit_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        credit_page.submit_form()

        payment = db.get_last_payment()
        assert payment is None, "При кредите не должно быть записи в payment_entity"

