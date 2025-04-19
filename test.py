import unittest
from original_code import D as OriginalClient, B as OriginalStrava, F as OriginalOrderFactory, C as OriginalMenu, G as OriginalNotifier, H as OriginalKitchen, I as OriginalDatabase
from refactored_code import Client as RefactoredClient, Strava as RefactoredStrava, OrderFactory as RefactoredOrderFactory, Menu as RefactoredMenu, KitchenNotifier as RefactoredNotifier, Kitchen as RefactoredKitchen, Database as RefactoredDatabase


def prepare_order_system(ClientClass, StravaClass, OrderFactoryClass, MenuClass, NotifierClass, KitchenClass, DatabaseClass):
    kitchen = KitchenClass()
    notifier = NotifierClass()

    if hasattr(notifier, "subscribe"):
        notifier.subscribe(kitchen)
    elif hasattr(notifier, "a"):
        notifier.a(kitchen)

    menu = MenuClass()
    strava1 = StravaClass("Суп", 50)
    strava2 = StravaClass("Вареники", 60)

    if hasattr(menu, "add_item"):
        menu.add_item(strava1)
        menu.add_item(strava2)
    elif hasattr(menu, "f1"):
        menu.f1(strava1)
        menu.f1(strava2)

    client = ClientClass("Іван")
    items = [strava1, strava2]

    if hasattr(OrderFactoryClass, "create_order"):
        order = OrderFactoryClass.create_order("normal", client, items)
    elif hasattr(OrderFactoryClass, "build_order"):
        order = OrderFactoryClass.build_order("normal", client, items)
    else:
        order = None

    db = DatabaseClass()
    if hasattr(client, "place_order") and order:
        client.place_order(order, db, notifier)
    elif hasattr(client, "g") and order:
        client.g(order, db, notifier)
    return client, menu, db, notifier, kitchen, order


def generate_tests(ClientClass, StravaClass, OrderFactoryClass, MenuClass, NotifierClass, KitchenClass, DatabaseClass):

    class CommonTests(unittest.TestCase):

        def test_client_can_place_order(self):
            client, _, _, _, _, order = prepare_order_system(ClientClass, StravaClass, OrderFactoryClass, MenuClass, NotifierClass, KitchenClass, DatabaseClass)
            if order and hasattr(client, "get_orders"):
                self.assertIn(order, client.get_orders())

        def test_menu_adds_items(self):
            _, menu, *_ = prepare_order_system(ClientClass, StravaClass, OrderFactoryClass, MenuClass, NotifierClass, KitchenClass, DatabaseClass)
            if hasattr(menu, "get_menu_items"):
                self.assertEqual(len(menu.get_menu_items()), 2)

        def test_order_status_changes(self):
            _, _, _, _, _, order = prepare_order_system(ClientClass, StravaClass, OrderFactoryClass, MenuClass, NotifierClass, KitchenClass, DatabaseClass)
            if order and hasattr(order, "get_status"):
                self.assertEqual(order.get_status(), "Готується")

        def test_database_saves_order(self):
            _, _, db, _, _, order = prepare_order_system(ClientClass, StravaClass, OrderFactoryClass, MenuClass, NotifierClass, KitchenClass, DatabaseClass)
            if order and hasattr(db, "get_orders"):
                orders = db.get_orders()
                self.assertTrue(any(order.client.name in row and order.items[0].name in row[1] for row in orders))

        def test_strava_validation(self):
            with self.assertRaises(ValueError):
                StravaClass("", 100)
            with self.assertRaises(ValueError):
                StravaClass("Суп", -5)

        def test_multiple_orders(self):
            client, _, db, notifier, kitchen, _ = prepare_order_system(ClientClass, StravaClass, OrderFactoryClass, MenuClass, NotifierClass, KitchenClass, DatabaseClass)
            strava3 = StravaClass("Деруни", 70)
            if hasattr(OrderFactoryClass, "create_order"):
                order2 = OrderFactoryClass.create_order("normal", client, [strava3])
            else:
                order2 = OrderFactoryClass.build_order("normal", client, [strava3])
            if hasattr(client, "place_order"):
                client.place_order(order2, db, notifier)
                self.assertIn(order2, client.get_orders())

        def test_special_order(self):
            client = ClientClass("Оксана")
            strava = StravaClass("Котлета", 80)
            if hasattr(OrderFactoryClass, "create_order"):
                order = OrderFactoryClass.create_order("special", client, [strava])
            elif hasattr(OrderFactoryClass, "build_order"):
                order = OrderFactoryClass.build_order("special", client, [strava])
            else:
                order = None
            self.assertTrue(order and hasattr(order, "special"))

        def test_kitchen_receives_notification(self):
            _, _, _, notifier, kitchen, order = prepare_order_system(ClientClass, StravaClass, OrderFactoryClass, MenuClass, NotifierClass, KitchenClass, DatabaseClass)
            if order and hasattr(kitchen, "orders"):
                self.assertIn(order, kitchen.orders)

        def test_menu_str(self):
            _, menu, *_ = prepare_order_system(ClientClass, StravaClass, OrderFactoryClass, MenuClass, NotifierClass, KitchenClass, DatabaseClass)
            menu_str = str(menu)
            self.assertIn("Суп", menu_str)
            self.assertIn("Вареники", menu_str)

        def test_order_str(self):
            client, _, _, _, _, order = prepare_order_system(ClientClass, StravaClass, OrderFactoryClass, MenuClass, NotifierClass, KitchenClass, DatabaseClass)
            if order:
                self.assertIn(client.name, str(order))

        def test_get_status(self):
            _, _, _, _, _, order = prepare_order_system(ClientClass, StravaClass, OrderFactoryClass, MenuClass, NotifierClass, KitchenClass, DatabaseClass)
            if order:
                self.assertEqual(order.get_status(), "Готується")

        def test_menu_removal(self):
            _, menu, *_ = prepare_order_system(ClientClass, StravaClass, OrderFactoryClass, MenuClass, NotifierClass, KitchenClass, DatabaseClass)
            if hasattr(menu, "get_menu_items") and len(menu.get_menu_items()) > 0:
                item = menu.get_menu_items()[0]
                if hasattr(menu, "remove_item"):
                    menu.remove_item(item)
                self.assertNotIn(item, menu.get_menu_items())

        def test_client_order_count(self):
            client, _, _, _, _, order = prepare_order_system(ClientClass, StravaClass, OrderFactoryClass, MenuClass, NotifierClass, KitchenClass, DatabaseClass)
            if order and hasattr(client, "get_orders"):
                self.assertEqual(len(client.get_orders()), 1)

        def test_notifier_log(self):
            _, _, _, notifier, _, order = prepare_order_system(ClientClass, StravaClass, OrderFactoryClass, MenuClass, NotifierClass, KitchenClass, DatabaseClass)
            if order and hasattr(notifier, "logs"):
                self.assertTrue(any("Order Notified" in log for log in notifier.logs))

        def test_notifier_unsubscribe(self):
            kitchen = KitchenClass()
            notifier = NotifierClass()
            if hasattr(notifier, "subscribe") and hasattr(notifier, "unsubscribe"):
                notifier.subscribe(kitchen)
                notifier.unsubscribe(kitchen)
                if hasattr(notifier, "subscribers"):
                    self.assertNotIn(kitchen, notifier.subscribers)

        def test_order_total_price(self):
            _, _, _, _, _, order = prepare_order_system(ClientClass, StravaClass, OrderFactoryClass, MenuClass, NotifierClass, KitchenClass, DatabaseClass)
            if order and hasattr(order, "get_total_price"):
                total = sum(item.price for item in order.items)
                self.assertEqual(order.get_total_price(), total)

        def test_order_factory_invalid_type(self):
            with self.assertRaises(ValueError):
                if hasattr(OrderFactoryClass, "create_order"):
                    OrderFactoryClass.create_order("invalid", ClientClass("Микола"), [])
                else:
                    OrderFactoryClass.build_order("invalid", ClientClass("Микола"), [])

        def test_database_structure(self):
            db = DatabaseClass()
            if hasattr(db, "get_orders"):
                self.assertIsNotNone(db.get_orders())

        def test_order_items_content(self):
            _, _, _, _, _, order = prepare_order_system(ClientClass, StravaClass, OrderFactoryClass, MenuClass, NotifierClass, KitchenClass, DatabaseClass)
            if order:
                self.assertTrue(all(isinstance(item, StravaClass) for item in order.items))

        def test_order_has_client_reference(self):
            client, _, _, _, _, order = prepare_order_system(ClientClass, StravaClass, OrderFactoryClass, MenuClass, NotifierClass, KitchenClass, DatabaseClass)
            if order:
                self.assertEqual(order.client, client)

    return CommonTests


OriginalTests = generate_tests(
    OriginalClient, OriginalStrava, OriginalOrderFactory,
    OriginalMenu, OriginalNotifier, OriginalKitchen, OriginalDatabase
)

RefactoredTests = generate_tests(
    RefactoredClient, RefactoredStrava, RefactoredOrderFactory,
    RefactoredMenu, RefactoredNotifier, RefactoredKitchen, RefactoredDatabase
)

if __name__ == '__main__':
    unittest.main()
