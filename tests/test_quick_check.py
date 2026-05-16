# tests/test_quick_check.py
import pytest
import allure


@allure.feature("Быстрая проверка")
class TestQuickCheck:

    @allure.title("Проверка работы DataGenerator")
    def test_data_generator(self):
        from utils.data_generator import DataGenerator as Data

        # Проверяем все методы
        assert Data.get_valid_card() == "4444 4444 4444 4441"
        assert Data.get_declined_card() == "4444 4444 4444 4442"
        assert len(Data.generate_cvc()) == 3
        assert Data.get_current_year() is not None
        assert Data.get_year_plus_five() is not None
        assert Data.get_current_month() is not None
        assert len(Data.generate_long_owner(64)) == 64

        print("All DataGenerator methods work correctly!")

    @allure.title("Проверка подключения к БД")
    def test_db_connection(self, db):
        assert db is not None
        result = db.get_last_payment()
        # Просто проверяем, что подключение работает
        print(f"DB connection successful, last payment: {result}")