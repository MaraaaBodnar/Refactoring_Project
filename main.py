from abc import ABC, abstractmethod
from typing import List
import sqlite3


# Абстрактний інтерфейс для оповіщення
class OrderNotifier(ABC):
    @abstractmethod
    def notify(self, order: "Order") -> None:
        pass


# Клас для представлення страви
class Strava:
    def __init__(self, name: str, price: float):
        if not name:
            raise ValueError("Назва страви повинна бути непорожньою.")
        if price <= 0:
            raise ValueError("Ціна повинна бути більше 0.")
        self.name = name
        self.price = price
        self.description = ""
        self.category = ""

    def set_description(self, description: str):
        self.description = description

    def set_category(self, category: str):
        self.category = category

    def get_price(self):
        return self.price

    def __str__(self):
        return f"{self.name} - {self.price} грн"


# Клас для представлення меню
class Menu:
    def __init__(self):
        self.items: List[Strava] = []
        self.counter = 0

    def add_strava(self, strava: Strava) -> None:
        self.items.append(strava)
        self.counter += 1

    def remove_strava(self, strava: Strava):
        if strava in self.items:
            self.items.remove(strava)
            self.counter -= 1

    def get_menu_items(self):
        return [str(strava) for strava in self.items]


# Клас клієнта
class Client:
    def __init__(self, name: str):
        self.name = name
        self.orders = []

    def place_order(self, order: "Order", database: "Database", kitchen_notifier: "KitchenNotifier") -> None:
        database.add_order(order)
        kitchen_notifier.notify(order)
        self.orders.append(order)

    def get_orders(self):
        return self.orders


# Замовлення
class Order:
    def __init__(self, client: "Client", items: List["Strava"]):
        if client is None:
            raise TypeError("Клієнт не може бути None")
        self.client = client
        self.items = items
        self.options = []
        self.status = "Очікується"

    def add_option(self, option: str) -> None:
        self.options.append(option)

    def set_status(self, status: str):
        self.status = status

    def get_status(self):
        return self.status

    def __str__(self):
        item_list = ', '.join(f"{strava.name} ({strava.price} грн)" for strava in self.items)
        return f"Замовлення для {self.client.name}: {item_list}"


# Factory для створення замовлень
class OrderFactory:
    @staticmethod
    def create_order(order_type: str, client, items):
        if order_type == "normal":
            return Order(client, items)
        elif order_type == "special":
            order = Order(client, items)
            order.add_option("special")
            return order
        else:
            raise ValueError("Unknown order type")


# Повідомлення для кухні
class KitchenNotifier:
    def __init__(self):
        self.subscribers = []
        self.logs = []

    def subscribe(self, observer):
        self.subscribers.append(observer)
        self.logs.append(f"Subscribed: {observer}")

    def unsubscribe(self, observer):
        self.subscribers.remove(observer)
        self.logs.append(f"Unsubscribed: {observer}")

    def notify(self, order):
        for subscriber in self.subscribers:
            subscriber.update(order)
        self.logs.append(f"Order Notified: {order}")


# Кухня, яка отримує замовлення
class Kitchen:
    def update(self, order):
        print(f"Нове замовлення на кухні: {order}")
        order.set_status("Готується")


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.conn = sqlite3.connect("../orders.db")
            cls._instance.cursor = cls._instance.conn.cursor()
            cls._instance.create_table()
        return cls._instance

    def create_table(self):
        """Створює таблицю, якщо вона ще не існує."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client TEXT,
                items TEXT
            )
        """)
        self.conn.commit()

    def add_order(self, order):
        """Додає замовлення в базу даних."""
        items_str = ", ".join([f"{item.name} ({item.price} грн)" for item in order.items])
        self.cursor.execute("INSERT INTO orders (client, items) VALUES (?, ?)", (order.client.name, items_str))
        self.conn.commit()

    def get_orders(self):
        """Отримує всі замовлення з бази."""
        self.cursor.execute("SELECT client, items FROM orders")
        return self.cursor.fetchall()