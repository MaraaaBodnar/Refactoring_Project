from abc import ABC, abstractmethod
import sqlite3

class A(ABC):
    @abstractmethod
    def a(self, o):
        pass

class B:
    def __init__(self, x, y):
        if not x:
            raise ValueError("e")
        if y <= 0:
            raise ValueError("e")
        self.x = x  # назва страви
        self.y = y  # ціна
        self.z = ""  # не використовується
        self.c = ""  # не використовується

    def s1(self, d):
        self.z = d

    def s2(self, c):
        self.c = c

    def p(self):
        return self.y

    def __str__(self):
        return f"{self.x} - {self.y} грн"

class C:
    def __init__(self):
        self.i = []  # список страв
        self.j = 0   # кількість

    def f1(self, q):  # додати страву
        self.i.append(q)
        self.j += 1

    def f2(self, q):  # прибрати страву
        if q in self.i:
            self.i.remove(q)
            self.j -= 1

    def f3(self):  # повернути список у форматі рядків
        return [str(r) for r in self.i]

    def __str__(self):
        return "\n".join(str(item) for item in self.i)  # Виводить список страв


class D:
    def __init__(self, n):
        self.n = n  # ім'я клієнта
        self.o = []  # замовлення

    @property
    def name(self):
        return self.n

    def g(self, o, d, k):
        d.k(o)  # зберегти в БД
        k.b(o)  # повідомити кухню
        self.o.append(o)

    def h(self):
        return self.o

class E:
    def __init__(self, x, y):
        if x is None:
            raise TypeError("None")
        self.a = x  # клієнт
        self.b = y  # страви
        self.c = []  # мітки (наприклад, special)
        self.d = "Очікується"  # статус

    @property
    def client(self):
        return self.a

    @property
    def items(self):
        return self.b

    def ao(self, op):
        self.c.append(op)

    def s(self, s):
        self.d = s  # Оновлюємо статус

    def g(self):
        return self.d

    def get_status(self):
        return self.d

    @property
    def special(self):
        return "special" in self.c

    def __str__(self):
        return f"Замовлення для {self.a.n}: {', '.join(f'{i.x} ({i.y} грн)' for i in self.b)}"


class F:
    @staticmethod
    def f(t, c, i):
        if t == "normal":
            return E(c, i)
        elif t == "special":
            z = E(c, i)
            z.ao("special")
            return z
        else:
            raise ValueError("???")

    build_order = f

class G:
    def __init__(self):
        self.s = []
        self.l = []

    def a(self, o):
        self.s.append(o)
        self.l.append(f"Subscribed: {o}")

    def u(self, o):
        self.s.remove(o)
        self.l.append(f"Unsubscribed: {o}")

    def b(self, o):
        for s in self.s:
            s.up(o)
        self.l.append(f"Order Notified: {o}")

class H:
    def up(self, o):
        o.s("Готується")  # зміна статусу на "Готується"
        print(f"Нове замовлення на кухні: {o}")

class I:
    _i = None

    def __new__(cls):
        if cls._i is None:
            cls._i = super(I, cls).__new__(cls)
            cls._i.a = sqlite3.connect(":memory:")
            cls._i.b = cls._i.a.cursor()
            cls._i.t()
        return cls._i

    def t(self):
        self.b.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client TEXT,
            items TEXT
        )""")
        self.a.commit()

    def k(self, o):
        z = ", ".join([f"{m.x} ({m.y} грн)" for m in o.b])
        self.b.execute("INSERT INTO orders (client, items) VALUES (?, ?)", (o.a.n, z))
        self.a.commit()

    def j(self):
        self.b.execute("SELECT client, items FROM orders")
        return self.b.fetchall()
