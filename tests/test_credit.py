# tests/test_credit.py
import pytest
import allure
from utils.data_generator import DataGenerator as Data


@allure.feature("Покупка в кредит")
class TestCredit:

    # ==================== ПОЗИТИВНЫЕ СЦЕНАРИИ ====================

    @allure.title("POS-02: Успешное оформление кредита")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_credit(self, credit_page, db, clear_db):
        credit_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        credit_page.submit_form()

        assert credit_page.is_success_visible(), "Уведомление об успехе не появилось"

        status = db.get_credit_status()
        assert status == "APPROVED", f"Ожидался APPROVED, получен {status}"

    @allure.title("Кредит - владелец минимальной длины")
    @allure.severity(allure.severity_level.NORMAL)
    def test_credit_owner_min_length(self, credit_page, db, clear_db):
        credit_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            "A",
            Data.generate_cvc()
        )
        credit_page.submit_form()
        assert credit_page.is_success_visible()

    @allure.title("Кредит - месяц 01")
    @allure.severity(allure.severity_level.NORMAL)
    def test_credit_month_min(self, credit_page, db, clear_db):
        credit_page.fill_card_data(
            Data.get_valid_card(),
            "01",
            Data.get_future_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        credit_page.submit_form()
        assert credit_page.is_success_visible()

    @allure.title("Кредит - месяц 12")
    @allure.severity(allure.severity_level.NORMAL)
    def test_credit_month_max(self, credit_page, db, clear_db):
        credit_page.fill_card_data(
            Data.get_valid_card(),
            "12",
            Data.get_future_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        credit_page.submit_form()
        assert credit_page.is_success_visible()

    @allure.title("Кредит - CVC с ведущими нулями")
    @allure.severity(allure.severity_level.NORMAL)
    def test_credit_cvc_leading_zeros(self, credit_page, db, clear_db):
        credit_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            Data.generate_valid_owner(),
            "001"
        )
        credit_page.submit_form()
        assert credit_page.is_success_visible()

    # ==================== НЕГАТИВНЫЕ СЦЕНАРИИ ====================

    @allure.title("NEG-01: Отказ в кредите при использовании отклоняемой карты")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_declined_credit(self, credit_page, db, clear_db):
        credit_page.fill_card_data(
            Data.get_declined_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        credit_page.submit_form()

        assert credit_page.is_error_visible(), "Уведомление об ошибке не появилось"

        status = db.get_credit_status()
        assert status == "DECLINED", f"Ожидался DECLINED, получен {status}"

    @allure.title("Кредит - невалидный месяц 00")
    @allure.severity(allure.severity_level.NORMAL)
    def test_credit_month_zero(self, credit_page, db, clear_db):
        credit_page.fill_card_data(
            Data.get_valid_card(),
            "00",
            Data.get_future_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        credit_page.submit_form()

        errors = credit_page.get_validation_errors()
        assert len(errors) > 0, "Ожидалась ошибка валидации месяца"

    @allure.title("Кредит - невалидный месяц 13")
    @allure.severity(allure.severity_level.NORMAL)
    def test_credit_month_thirteen(self, credit_page, db, clear_db):
        credit_page.fill_card_data(
            Data.get_valid_card(),
            "13",
            Data.get_future_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        credit_page.submit_form()

        errors = credit_page.get_validation_errors()
        assert len(errors) > 0, "Ожидалась ошибка валидации месяца"

    @allure.title("Кредит - год прошлый")
    @allure.severity(allure.severity_level.NORMAL)
    def test_credit_year_past(self, credit_page, db, clear_db):
        credit_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_past_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        credit_page.submit_form()

        errors = credit_page.get_validation_errors()
        assert any("истек" in str(e).lower() or "срок" in str(e).lower() for e in errors)

    @allure.title("Кредит - владелец кириллицей")
    @allure.severity(allure.severity_level.NORMAL)
    def test_credit_owner_cyrillic(self, credit_page, db, clear_db):
        credit_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            "ИВАН ПЕТРОВ",
            Data.generate_cvc()
        )
        credit_page.submit_form()

        errors = credit_page.get_validation_errors()
        assert len(errors) > 0, "Ожидалась ошибка формата владельца"

    @allure.title("Кредит - CVC 000")
    @allure.severity(allure.severity_level.NORMAL)
    def test_credit_cvc_zeros(self, credit_page, db, clear_db):
        credit_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            Data.generate_valid_owner(),
            "000"
        )
        credit_page.submit_form()

        errors = credit_page.get_validation_errors()
        assert len(errors) > 0, "Ожидалась ошибка CVC"