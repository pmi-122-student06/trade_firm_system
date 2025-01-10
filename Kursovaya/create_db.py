import sqlite3

def create_tables():
    conn = sqlite3.connect('trade_firm.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            characteristics TEXT,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            unit TEXT NOT NULL,
            arrival_date TEXT NOT NULL,
            store_name TEXT NOT NULL,
            discount REAL,
            vat REAL,
            image BLOB,
            FOREIGN KEY (store_name) REFERENCES stores(name)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS firms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            phone TEXT,
            address TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            phone TEXT,
            address TEXT
        )
    ''')

    # Таблица для связи товаров и фирм (многие ко многим)
    cursor.execute('''
         CREATE TABLE IF NOT EXISTS product_firm (
         product_id INTEGER NOT NULL,
         firm_id INTEGER NOT NULL,
         FOREIGN KEY (product_id) REFERENCES products(id),
         FOREIGN KEY (firm_id) REFERENCES firms(id),
         PRIMARY KEY (product_id, firm_id)
         )
         ''')

    conn.commit()
    conn.close()

def create_initial_data():
    conn = sqlite3.connect('trade_firm.db')
    cursor = conn.cursor()

    # Пример данных для фирм
    firms = [
        ("ООО Ромашка", "+79001234567", "ул. Цветочная, д.1"),
        ("ЗАО Василек", "+79109876543", "пер. Лесной, д. 2"),
    ]
    cursor.executemany("INSERT OR IGNORE INTO firms (name, phone, address) VALUES (?, ?, ?)", firms)

    # Пример данных для магазинов
    stores = [
        ("Магазин у дома", "+79201112233", "ул. Проспект, д.3"),
        ("Супермаркет Глобус", "+79304445566", "ул. Большая, д.4"),
    ]
    cursor.executemany("INSERT OR IGNORE INTO stores (name, phone, address) VALUES (?, ?, ?)", stores)


    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
    create_initial_data()
    print("База данных и таблицы созданы.")