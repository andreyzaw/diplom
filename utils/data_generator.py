# utils/data_generator.py
from faker import Faker
import random
from datetime import datetime

fake = Faker()


class DataGenerator:

    @staticmethod
    def generate_valid_owner():
        """Генерирует валидное имя владельца (латиница)"""
        return f"{fake.first_name()} {fake.last_name()}".upper()

    @staticmethod
    def generate_cyrillic_owner():
        """Генерирует имя на кириллице"""
        return f"{fake.first_name()} {fake.last_name()}"

    @staticmethod
    def generate_long_owner(length=64):
        """Генерирует имя заданной длины"""
        return "A" * length

    @staticmethod
    def generate_single_letter_owner():
        """Одна буква"""
        return "A"

    @staticmethod
    def generate_cvc():
        """Генерирует валидный CVC"""
        return str(random.randint(1, 999)).zfill(3)

    @staticmethod
    def get_valid_card():
        """Валидная карта (APPROVED)"""
        return "4444 4444 4444 4441"

    @staticmethod
    def get_declined_card():
        """Отклоняемая карта (DECLINED)"""
        return "4444 4444 4444 4442"

    @staticmethod
    def get_invalid_card():
        """Невалидный номер карты"""
        return "1234 5678 9012 3456"

    @staticmethod
    def get_valid_month():
        """Валидный месяц"""
        return str(random.randint(1, 12)).zfill(2)

    @staticmethod
    def get_current_month():
        """Текущий месяц"""
        return datetime.now().strftime("%m")

    @staticmethod
    def get_past_month():
        """Прошлый месяц (если текущий январь, то декабрь)"""
        current_month = datetime.now().month
        past_month = current_month - 1 if current_month > 1 else 12
        return str(past_month).zfill(2)

    @staticmethod
    def get_invalid_month():
        """Невалидный месяц (13)"""
        return "13"

    @staticmethod
    def get_future_year():
        """Будущий год"""
        current_year = datetime.now().year % 100
        return str(random.randint(current_year + 1, current_year + 5)).zfill(2)

    @staticmethod
    def get_current_year():
        """Текущий год"""
        return datetime.now().strftime("%y")

    @staticmethod
    def get_year_plus_five():
        """Год +5 лет от текущего"""
        current_year = datetime.now().year
        return str((current_year + 5) % 100).zfill(2)

    @staticmethod
    def get_past_year():
        """Прошлый год"""
        current_year = datetime.now().year % 100
        return str(max(0, current_year - 1)).zfill(2)