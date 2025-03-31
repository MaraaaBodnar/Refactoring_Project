import unittest
from main import Strava, Menu, Client, Order, KitchenNotifier, Database


class TestSystem(unittest.TestCase):

    def test_create_strava(self):
        strava = Strava("Піца", 120.0)
        self.assertEqual(strava.name, "Піца")
        self.assertEqual(strava.price, 120.0)

    def test_create_menu(self):
        menu = Menu()
        self.assertEqual(len(menu.items), 0)

    def test_add_strava_to_menu(self):
        menu = Menu()
        strava = Strava("Бургер", 80.0)
        menu.add_strava(strava)
        self.assertIn(strava, menu.items)

    def test_create_client(self):
        client = Client("Марія")
        self.assertEqual(client.name, "Марія")

    def test_create_order(self):
        client = Client("Олексій")
        items = [Strava("Суші", 200.0)]
        order = Order(client, items)
        self.assertEqual(order.client, client)
        self.assertEqual(order.items, items)

    def test_order_with_multiple_items(self):
        client = Client("Іван")
        items = [Strava("Салат", 50.0), Strava("Сік", 30.0)]
        order = Order(client, items)
        self.assertEqual(len(order.items), 2)

    def test_client_places_order(self):
        client = Client("Наталя")
        order = Order(client, [Strava("Кава", 40.0)])
        database = Database()  # Ініціалізуємо тестову базу даних
        notifier = KitchenNotifier()  # Ініціалізуємо тестовий KitchenNotifier
        client.place_order(order, database, notifier)  # Передаємо всі аргументи

    def test_order_notifier_interface(self):
        notifier = KitchenNotifier()
        order = Order(Client("Петро"), [Strava("Торт", 150.0)])
        notifier.notify(order)  # Метод має існувати

    def test_order_str_representation(self):
        client = Client("Олена")
        items = [Strava("Морозиво", 60.0)]
        order = Order(client, items)
        self.assertIn("Олена", str(order))
        self.assertIn("Морозиво", str(order))

    def test_kitchen_notifier_notify(self):
        notifier = KitchenNotifier()
        order = Order(Client("Андрій"), [Strava("Пельмені", 90.0)])
        self.assertIsNone(notifier.notify(order))  # Метод не повинен повертати значення

    def test_add_strava_with_missing_name(self):
        """Тест на додавання страви без назви."""
        with self.assertRaises(ValueError):
            strava = Strava("", 100.0)  # Назва повинна бути непорожньою

    def test_add_strava_with_missing_price(self):
        """Тест на додавання страви без ціни."""
        with self.assertRaises(ValueError):
            strava = Strava("Котлета", -50.0)  # Ціна повинна бути більшою за 0

    def test_empty_menu(self):
        """Тест для порожнього меню."""
        menu = Menu()
        self.assertEqual(len(menu.items), 0)

    def test_create_order_with_empty_menu(self):
        """Тест для замовлення, коли меню порожнє."""
        client = Client("Марія")
        menu = Menu()
        items = []  # Порожній список страв
        order = Order(client, items)
        self.assertEqual(order.items, [])

    def test_order_with_no_client(self):
        """Тест для замовлення без клієнта."""
        items = [Strava("Салат", 50.0)]
        with self.assertRaises(TypeError):  # Очікуємо помилку, бо клієнт не заданий
            order = Order(None, items)

    def test_notify_kitchen_with_no_items(self):
        """Тест для оповіщення кухні, коли замовлення не містить страв."""
        client = Client("Іван")
        items = []  # Порожнє замовлення
        order = Order(client, items)
        notifier = KitchenNotifier()
        self.assertIsNone(notifier.notify(order))  # Повідомлення не повинно мати вмісту

    def test_add_multiple_stravy(self):
        """Тест для додавання кількох страв у меню."""
        menu = Menu()
        strava1 = Strava("Бургер", 80.0)
        strava2 = Strava("Піца", 120.0)
        menu.add_strava(strava1)
        menu.add_strava(strava2)
        self.assertEqual(len(menu.items), 2)  # Перевіряємо, чи додано дві страви

    def test_create_order_with_multiple_items(self):
        """Тест для замовлення з кількома стравами."""
        client = Client("Наталя")
        items = [Strava("Кава", 40.0), Strava("Торт", 100.0)]
        order = Order(client, items)
        self.assertEqual(len(order.items), 2)
        self.assertEqual(order.items[0].name, "Кава")
        self.assertEqual(order.items[1].name, "Торт")

    def test_notify_kitchen_with_valid_order(self):
        """Тест для оповіщення кухні про замовлення зі стравами."""
        client = Client("Олена")
        items = [Strava("Морозиво", 60.0)]
        order = Order(client, items)
        notifier = KitchenNotifier()
        self.assertIsNone(notifier.notify(order))  # Перевіряємо, чи відбулося оповіщення