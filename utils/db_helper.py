import pymysql
import os
from dotenv import load_dotenv

load_dotenv()


class DatabaseHelper:
    def __init__(self):
        self.connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3307)),  # Используем порт 3307
            user=os.getenv('DB_USER', 'app_user'),
            password=os.getenv('DB_PASSWORD', 'app_pass'),
            database=os.getenv('DB_NAME', 'app_db'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def get_last_payment(self):
        """Получение последней записи из payment_entity"""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM payment_entity ORDER BY id DESC LIMIT 1")
            return cursor.fetchone()

    def get_last_credit(self):
        """Получение последней записи из credit_request_entity"""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM credit_request_entity ORDER BY id DESC LIMIT 1")
            return cursor.fetchone()

    def get_last_order(self):
        """Получение последней записи из order_entity"""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM order_entity ORDER BY id DESC LIMIT 1")
            return cursor.fetchone()

    def get_payment_status(self):
        """Получение статуса последнего платежа"""
        payment = self.get_last_payment()
        return payment['status'] if payment else None

    def get_credit_status(self):
        """Получение статуса последнего кредита"""
        credit = self.get_last_credit()
        return credit['status'] if credit else None

    def get_payment_amount(self):
        """Получение суммы последнего платежа"""
        payment = self.get_last_payment()
        return payment['amount'] if payment else None

    def clear_tables(self):
        """Очистка таблиц перед тестом"""
        with self.connection.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            cursor.execute("TRUNCATE TABLE payment_entity")
            cursor.execute("TRUNCATE TABLE credit_request_entity")
            cursor.execute("TRUNCATE TABLE order_entity")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            self.connection.commit()

    def close(self):
        """Закрытие соединения с БД"""
        self.connection.close()