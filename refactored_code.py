# refactored_code.py

from abc import ABC, abstractmethod
from typing import List
import sqlite3


# Constants
ORDER_TYPE_NORMAL = "normal"
ORDER_TYPE_SPECIAL = "special"


class OrderNotifier(ABC):
    """Абстрактний інтерфейс для класів-оповіщувачів про нові замовлення."""
    @abstractmethod
    def notify(self, order: "Order") -> None:
        """Надсилає сповіщення про нове замовлення."""
        pass


class Strava:
    """Клас, що представляє страву у меню."""
    def __init__(self, name: str, price: float, description: str = "", category: str = ""):
        if not name:
            raise ValueError("Назва страви повинна бути непорожньою.")
        if price <= 0:
            raise ValueError("Ціна повинна бути більше 0.")
        self._name = name
        self._price = price
        self._description = description
        self._category = category

    @property
    def name(self):
        """Повертає назву страви."""
        return self._name

    @property
    def price(self):
        """Повертає ціну страви."""
        return self._price

    def set_description(self, description: str):
        """Встановлює опис страви."""
        self._description = description

    def set_category(self, category: str):
        """Встановлює категорію страви."""
        self._category = category

    def __str__(self):
        return f"{self._name} - {self._price} грн"


class Menu:
    """Клас для представлення меню, що містить список страв."""
    def __init__(self):
        self._items: List[Strava] = []

    def add_item(self, item: Strava) -> None:
        """Додає страву до меню."""
        self._items.append(item)

    def remove_item(self, item: Strava) -> None:
        """Видаляє страву з меню."""
        if item in self._items:
            self._items.remove(item)

    def get_menu_items(self):
        return self._items  # повертаємо список об'єктів, не рядків

    def __str__(self):
        return ", ".join([str(item.name) for item in self._items])


class Client:
    """Клас, що представляє клієнта, який може створювати замовлення."""
    def __init__(self, name: str):
        self._name = name
        self._orders: List[Order] = []

    @property
    def name(self):
        """Повертає ім'я клієнта."""
        return self._name

    def place_order(self, order: "Order", db: "Database", notifier: OrderNotifier) -> None:
        """Розміщує замовлення: зберігає його та повідомляє кухню."""
        db.save_order(order)
        notifier.notify(order)
        self._orders.append(order)

    def get_orders(self):
        """Повертає список усіх замовлень клієнта."""
        return self._orders


class Order:
    """Клас, що представляє замовлення клієнта."""
    def __init__(self, client: Client, items: List[Strava]):
        if client is None:
            raise TypeError("Клієнт не може бути None")
        self._client = client
        self._items = items
        self._options = []
        self._status = "Очікується"

    @property
    def client(self):
        """Повертає клієнта, що зробив замовлення."""
        return self._client

    @property
    def items(self):
        """Повертає список страв у замовленні."""
        return self._items

    def add_option(self, option: str):
        """Додає опцію до замовлення (наприклад, "special")."""
        self._options.append(option)

    def set_status(self, status: str):
        """Встановлює статус замовлення."""
        self._status = status

    def get_status(self):
        """Повертає поточний статус замовлення."""
        return self._status

    def __str__(self):
        item_list = ', '.join(f"{item.name} ({item.price} грн)" for item in self._items)
        return f"Замовлення для {self._client.name}: {item_list}"


class NormalOrder(Order):
    """Звичайне замовлення без додаткових опцій."""
    pass


class SpecialOrder(Order):
    """Особливе замовлення з опцією 'special'."""
    def __init__(self, client: Client, items: List[Strava]):
        super().__init__(client, items)
        self.add_option("special")

    @property
    def special(self):
        return "special" in self._options


class OrderFactory:
    """Фабрика для створення різних типів замовлень."""
    @staticmethod
    def create_order(order_type: str, client: Client, items: List[Strava]) -> Order:
        """Створює замовлення відповідно до зазначеного типу."""
        if order_type == ORDER_TYPE_NORMAL:
            return NormalOrder(client, items)
        elif order_type == ORDER_TYPE_SPECIAL:
            return SpecialOrder(client, items)
        else:
            raise ValueError("Невідомий тип замовлення")


class Kitchen:
    """Кухня, яка реагує на нові замовлення."""
    def update(self, order: Order):
        """Оновлює стан замовлення при надходженні на кухню."""
        print(f"Нове замовлення на кухні: {order}")
        order.set_status("Готується")


class KitchenNotifier(OrderNotifier):
    """Клас-оповіщувач, який інформує кухню про нові замовлення."""
    def __init__(self):
        self._subscribers = []
        self._logs = []

    def subscribe(self, observer: Kitchen):
        """Додає кухню до списку підписників."""
        self._subscribers.append(observer)
        self._log(f"Subscribed: {observer}")

    def unsubscribe(self, observer: Kitchen):
        """Видаляє кухню зі списку підписників."""
        self._subscribers.remove(observer)
        self._log(f"Unsubscribed: {observer}")

    def notify(self, order: Order):
        """Надсилає повідомлення всім підписникам про нове замовлення."""
        for subscriber in self._subscribers:
            subscriber.update(order)
        self._log(f"Order Notified: {order}")

    def _log(self, message: str):
        """Логує повідомлення."""
        self._logs.append(message)


class Database:
    """Singleton-клас для збереження замовлень у базу даних SQLite."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._init_connection()
        return cls._instance

    def _init_connection(self):
        """Ініціалізує підключення до бази даних."""
        self._conn = sqlite3.connect("../orders.db")
        self._cursor = self._conn.cursor()
        self._create_table()

    def _create_table(self):
        """Створює таблицю замовлень, якщо вона ще не існує."""
        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client TEXT,
                items TEXT
            )
        """)
        self._conn.commit()

    def save_order(self, order: Order):
        """Зберігає замовлення у базі даних."""
        items_str = ", ".join(f"{item.name} ({item.price} грн)" for item in order.items)
        self._cursor.execute("INSERT INTO orders (client, items) VALUES (?, ?)", (order.client.name, items_str))
        self._conn.commit()

    def get_all_orders(self):
        """Повертає всі збережені замовлення."""
        self._cursor.execute("SELECT client, items FROM orders")
        return self._cursor.fetchall()
