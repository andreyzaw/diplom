# tests/test_payment.py
import pytest
import allure
from pages.payment_page import PaymentPage
from utils.data_generator import DataGenerator as Data


@allure.feature("Оплата по дебетовой карте")
class TestPayment:

    # ==================== ПОЗИТИВНЫЕ СЦЕНАРИИ ====================

    @allure.title("POS-01: Успешная оплата тура валидной картой")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_successful_payment(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        payment_page.submit_form()

        assert payment_page.is_success_visible(), "Уведомление об успехе не появилось"

        status = db.get_payment_status()
        assert status == "APPROVED", f"Ожидался APPROVED, получен {status}"

    @allure.title("POS-03: Владелец - минимальная длина (1 символ)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_owner_min_length(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            "A",
            Data.generate_cvc()
        )
        payment_page.submit_form()
        assert payment_page.is_success_visible(), "Оплата с владельцем из 1 символа не прошла"

    @allure.title("POS-04: Владелец - максимальная длина (64 символа)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_owner_max_length(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            Data.generate_long_owner(64),
            Data.generate_cvc()
        )
        payment_page.submit_form()
        assert payment_page.is_success_visible(), "Оплата с владельцем из 64 символов не прошла"

    @allure.title("POS-05: Владелец - двойная фамилия через дефис")
    @allure.severity(allure.severity_level.NORMAL)
    def test_owner_double_surname(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            "PETROV-IVANOV",
            Data.generate_cvc()
        )
        payment_page.submit_form()
        assert payment_page.is_success_visible(), "Оплата с двойной фамилией не прошла"

    @allure.title("POS-06: Месяц - минимальное значение (01)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_month_min_value(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            "01",
            Data.get_future_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        payment_page.submit_form()
        assert payment_page.is_success_visible(), "Оплата с месяцем 01 не прошла"

    @allure.title("POS-07: Месяц - максимальное значение (12)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_month_max_value(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            "12",
            Data.get_future_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        payment_page.submit_form()
        assert payment_page.is_success_visible(), "Оплата с месяцем 12 не прошла"

    @allure.title("POS-08: Год - текущий")
    @allure.severity(allure.severity_level.NORMAL)
    def test_year_current(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_current_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        payment_page.submit_form()
        assert payment_page.is_success_visible(), "Оплата с текущим годом не прошла"

    @allure.title("POS-09: Год - +5 лет от текущего")
    @allure.severity(allure.severity_level.NORMAL)
    def test_year_plus_five(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_year_plus_five(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        payment_page.submit_form()
        assert payment_page.is_success_visible(), "Оплата с годом +5 лет не прошла"

    @allure.title("POS-10: CVC - ведущие нули (001)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cvc_leading_zeros(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            Data.generate_valid_owner(),
            "001"
        )
        payment_page.submit_form()
        assert payment_page.is_success_visible(), "Оплата с CVC 001 не прошла"

    @allure.title("POS-11: CVC - максимальное значение (999)")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cvc_max_value(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            Data.generate_valid_owner(),
            "999"
        )
        payment_page.submit_form()
        assert payment_page.is_success_visible(), "Оплата с CVC 999 не прошла"

    # ==================== НЕГАТИВНЫЕ СЦЕНАРИИ ====================

    @allure.title("NEG-01: Оплата отклоняемой картой")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_declined_payment(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_declined_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        payment_page.submit_form()

        assert payment_page.is_error_visible(), "Уведомление об ошибке не появилось"

        status = db.get_payment_status()
        assert status == "DECLINED", f"Ожидался DECLINED, получен {status}"

    @allure.title("NEG-02: Номер карты - 16 нулей")
    @allure.severity(allure.severity_level.NORMAL)
    def test_card_number_all_zeros(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            "0000 0000 0000 0000",
            Data.get_valid_month(),
            Data.get_future_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        payment_page.submit_form()

        errors = payment_page.get_validation_errors()
        assert len(errors) > 0, "Ожидалась ошибка валидации номера карты"

    @allure.title("NEG-03: Номер карты - 15 цифр")
    @allure.severity(allure.severity_level.NORMAL)
    def test_card_number_15_digits(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            "4444 4444 4444 444",
            Data.get_valid_month(),
            Data.get_future_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        payment_page.submit_form()

        errors = payment_page.get_validation_errors()
        assert len(errors) > 0, "Ожидалась ошибка валидации номера карты"

    @allure.title("NEG-04: Номер карты - 17 цифр")
    @allure.severity(allure.severity_level.NORMAL)
    def test_card_number_17_digits(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            "4444 4444 4444 44444",
            Data.get_valid_month(),
            Data.get_future_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        payment_page.submit_form()

        errors = payment_page.get_validation_errors()
        assert len(errors) > 0, "Ожидалась ошибка валидации номера карты"

    @allure.title("NEG-05: Номер карты - содержит буквы")
    @allure.severity(allure.severity_level.NORMAL)
    def test_card_number_with_letters(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            "4444 4444 4444 ABCD",
            Data.get_valid_month(),
            Data.get_future_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        payment_page.submit_form()

        errors = payment_page.get_validation_errors()
        assert len(errors) > 0, "Ожидалась ошибка валидации номера карты"

    @allure.title("NEG-06: Месяц - значение 00")
    @allure.severity(allure.severity_level.NORMAL)
    def test_month_zero(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            "00",
            Data.get_future_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        payment_page.submit_form()

        errors = payment_page.get_validation_errors()
        assert any("месяц" in str(e).lower() for e in errors), "Ожидалась ошибка 'Неверный месяц'"

    @allure.title("NEG-07: Месяц - значение 13")
    @allure.severity(allure.severity_level.NORMAL)
    def test_month_thirteen(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            "13",
            Data.get_future_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        payment_page.submit_form()

        errors = payment_page.get_validation_errors()
        assert any("месяц" in str(e).lower() for e in errors), "Ожидалась ошибка 'Неверный месяц'"

    @allure.title("NEG-08: Месяц - пустое поле")
    @allure.severity(allure.severity_level.NORMAL)
    def test_month_empty(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            "",
            Data.get_future_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        payment_page.submit_form()

        errors = payment_page.get_validation_errors()
        assert len(errors) > 0, "Ожидалась ошибка валидации"

    @allure.title("NEG-09: Год - прошлый")
    @allure.severity(allure.severity_level.NORMAL)
    def test_year_past(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_past_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        payment_page.submit_form()

        errors = payment_page.get_validation_errors()
        assert any("истек" in str(e).lower() or "срок" in str(e).lower() for e in errors), \
            "Ожидалась ошибка 'Истёк срок'"

    @allure.title("NEG-10: Год - значение 00")
    @allure.severity(allure.severity_level.NORMAL)
    def test_year_zero(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            "00",
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        payment_page.submit_form()

        errors = payment_page.get_validation_errors()
        assert any("истек" in str(e).lower() or "срок" in str(e).lower() for e in errors), \
            "Ожидалась ошибка 'Истёк срок'"

    @allure.title("NEG-11: Год - пустое поле")
    @allure.severity(allure.severity_level.NORMAL)
    def test_year_empty(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            "",
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        payment_page.submit_form()

        errors = payment_page.get_validation_errors()
        assert len(errors) > 0, "Ожидалась ошибка валидации"

    @allure.title("NEG-12: Владелец - кириллица")
    @allure.severity(allure.severity_level.NORMAL)
    def test_owner_cyrillic(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            "ИВАН ПЕТРОВ",
            Data.generate_cvc()
        )
        payment_page.submit_form()

        errors = payment_page.get_validation_errors()
        assert len(errors) > 0, "Ожидалась ошибка 'Неверный формат'"

    @allure.title("NEG-13: Владелец - цифры")
    @allure.severity(allure.severity_level.NORMAL)
    def test_owner_digits(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            "1234 5678",
            Data.generate_cvc()
        )
        payment_page.submit_form()

        errors = payment_page.get_validation_errors()
        assert len(errors) > 0, "Ожидалась ошибка 'Неверный формат'"

    @allure.title("NEG-14: Владелец - спецсимволы")
    @allure.severity(allure.severity_level.NORMAL)
    def test_owner_special_chars(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            "IVAN@#$",
            Data.generate_cvc()
        )
        payment_page.submit_form()

        errors = payment_page.get_validation_errors()
        assert len(errors) > 0, "Ожидалась ошибка 'Неверный формат'"

    @allure.title("NEG-15: Владелец - только пробел")
    @allure.severity(allure.severity_level.NORMAL)
    def test_owner_only_space(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            "   ",
            Data.generate_cvc()
        )
        payment_page.submit_form()

        errors = payment_page.get_validation_errors()
        assert len(errors) > 0, "Ожидалась ошибка 'Неверный формат'"

    @allure.title("NEG-16: Владелец - пустое поле")
    @allure.severity(allure.severity_level.NORMAL)
    def test_owner_empty(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            "",
            Data.generate_cvc()
        )
        payment_page.submit_form()

        errors = payment_page.get_validation_errors()
        assert len(errors) > 0, "Ожидалась ошибка 'Поле обязательно'"

    @allure.title("NEG-17: CVC - 1 цифра")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cvc_one_digit(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            Data.generate_valid_owner(),
            "1"
        )
        payment_page.submit_form()

        errors = payment_page.get_validation_errors()
        assert len(errors) > 0, "Ожидалась ошибка формата CVC"

    @allure.title("NEG-18: CVC - 2 цифры")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cvc_two_digits(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            Data.generate_valid_owner(),
            "12"
        )
        payment_page.submit_form()

        errors = payment_page.get_validation_errors()
        assert len(errors) > 0, "Ожидалась ошибка формата CVC"

    @allure.title("NEG-19: CVC - 000")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cvc_zeros(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            Data.generate_valid_owner(),
            "000"
        )
        payment_page.submit_form()

        errors = payment_page.get_validation_errors()
        assert any("cvc" in str(e).lower() for e in errors), "Ожидалась ошибка 'Неверный CVC'"

    @allure.title("NEG-20: CVC - пустое поле")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cvc_empty(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_valid_month(),
            Data.get_future_year(),
            Data.generate_valid_owner(),
            ""
        )
        payment_page.submit_form()

        errors = payment_page.get_validation_errors()
        assert len(errors) > 0, "Ожидалась ошибка 'Поле обязательно'"

    @allure.title("NEG-21: Истекший срок - год прошлый, месяц текущий")
    @allure.severity(allure.severity_level.NORMAL)
    def test_expired_card_past_year_current_month(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_current_month(),
            Data.get_past_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        payment_page.submit_form()

        errors = payment_page.get_validation_errors()
        assert any("истек" in str(e).lower() or "срок" in str(e).lower() for e in errors), \
            "Ожидалась ошибка 'Истёк срок'"

    @allure.title("NEG-22: Истекший срок - год текущий, месяц прошлый")
    @allure.severity(allure.severity_level.NORMAL)
    def test_expired_card_current_year_past_month(self, payment_page, db, clear_db):
        payment_page.fill_card_data(
            Data.get_valid_card(),
            Data.get_past_month(),
            Data.get_current_year(),
            Data.generate_valid_owner(),
            Data.generate_cvc()
        )
        payment_page.submit_form()

        errors = payment_page.get_validation_errors()
        assert any("истек" in str(e).lower() or "срок" in str(e).lower() for e in errors), \
            "Ожидалась ошибка 'Истёк срок'"