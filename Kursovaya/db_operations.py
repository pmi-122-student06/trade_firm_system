import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Вставка данных о товаре
def insert_product(name, category, characteristics, price, quantity, unit, arrival_date, store_name, discount, vat,
                   image):
    try:
        if not name:
            messagebox.showinfo("Ошибка", "Название товара не может быть пустым")
        if not category:
            messagebox.showinfo("ошибка", "Категория товара не может быть пустой.")
        if not price:
            messagebox.showinfo("Ошибка","Цена товара не может быть пустой.")
        if not quantity:
            messagebox.showinfo("Ошибка","Количество товара не может быть пустым.")
        if not unit:
            messagebox.showinfo("Ошибка","Единица измерения товара не может быть пустой.")
        if not arrival_date:
            messagebox.showinfo("Ошибка","Дата поступления товара не может быть пустой.")
        if not store_name:
            messagebox.showinfo("Ошибка","Название магазина не может быть пустым.")

        conn = sqlite3.connect('trade_firm.db')
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO products (name, category, characteristics, price, quantity, unit, arrival_date, store_name, discount, vat, image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, category, characteristics, price, quantity, unit, arrival_date, store_name, discount, vat, image)
        )
        conn.commit()
        conn.close()
        return "Товар успешно добавлен"
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
            conn.close()
        return f"Ошибка при добавлении товара: {e}"

# Добавление товара и фирмы в таблицу связей
def insert_product_firm(product_name, firm_name):
    try:
        conn = sqlite3.connect('trade_firm.db')
        cursor = conn.cursor()

        # Получаем id товара по его имени
        cursor.execute("SELECT id FROM products WHERE name = ?", (product_name,))
        product_result = cursor.fetchone()
        if not product_result:
            conn.close()
            return "Товар не найден"
        product_id = product_result[0]

        # Получаем id фирмы по ее имени
        cursor.execute("SELECT id FROM firms WHERE name = ?", (firm_name,))
        firm_result = cursor.fetchone()
        if not firm_result:
            conn.close()
            return "Фирма не найдена"
        firm_id = firm_result[0]

        cursor.execute(
            '''
            INSERT OR IGNORE INTO product_firm (product_id, firm_id)
            VALUES (?, ?)
            ''', (product_id, firm_id)
        )
        conn.commit()
        conn.close()
        return "Связь между товаром и фирмой добавлена"
    except sqlite3.Error as e:
        if conn:
             conn.rollback()
             conn.close()
        return f"Ошибка при связывании товара и фирмы: {e}"

# Функция для получения списка всех товаров
def get_all_products():
    try:
        conn = sqlite3.connect('trade_firm.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()
        conn.close()
        return products
    except sqlite3.Error as e:
        if conn:
             conn.close()
        return f"Ошибка при получении списка товаров: {e}"


# Получение всех фирм
def get_all_firms():
    try:
        conn = sqlite3.connect('trade_firm.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM firms')
        firms = cursor.fetchall()
        conn.close()
        return firms
    except sqlite3.Error as e:
         if conn:
             conn.close()
         return f"Ошибка при получении списка фирм: {e}"


# Получение всех магазинов
def get_all_stores():
    try:
        conn = sqlite3.connect('trade_firm.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM stores')
        stores = cursor.fetchall()
        conn.close()
        return stores
    except sqlite3.Error as e:
        if conn:
             conn.close()
        return f"Ошибка при получении списка магазинов: {e}"


# Функция для формирования отчета об объеме поставок за период
def get_delivery_report(start_date, end_date):
    try:
        conn = sqlite3.connect('trade_firm.db')
        cursor = conn.cursor()

        cursor.execute(
            '''
            SELECT 
                p.name, p.category, p.quantity, p.price,
                p.store_name, p.arrival_date, f.name
            FROM products AS p
            JOIN product_firm AS pf ON pf.product_id = p.id
            JOIN firms AS f ON f.id = pf.firm_id
            WHERE p.arrival_date BETWEEN ? AND ?
            ''',
            (start_date, end_date)
        )
        report = cursor.fetchall()
        conn.close()
        return report
    except sqlite3.Error as e:
         if conn:
            conn.close()
         return f"Ошибка при формировании отчета о поставках за период: {e}"


# Функция для формирования отчета о поставках для заданного магазина
def get_delivery_report_by_store(store_name):
    try:
        conn = sqlite3.connect('trade_firm.db')
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT 
                p.name, p.category, p.quantity, p.price,
                p.arrival_date, f.name
            FROM products AS p
            JOIN product_firm AS pf ON pf.product_id = p.id
            JOIN firms AS f ON f.id = pf.firm_id
            WHERE p.store_name = ?
            ''',
            (store_name,)
        )
        report = cursor.fetchall()
        conn.close()
        return report
    except sqlite3.Error as e:
        if conn:
            conn.close()
        return f"Ошибка при формировании отчета о поставках для магазина: {e}"


#  Отчет по поставкам для заданной фирмы
def get_delivery_report_by_firm(firm_name):
    try:
        conn = sqlite3.connect('trade_firm.db')
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT 
                p.name, p.category, p.quantity, p.price,
                 p.arrival_date, s.name
            FROM products AS p
            JOIN product_firm AS pf ON pf.product_id = p.id
            JOIN firms AS f ON f.id = pf.firm_id
            JOIN stores AS s ON s.name = p.store_name
            WHERE f.name = ?
            ''',
            (firm_name,)
        )
        report = cursor.fetchall()
        conn.close()
        return report
    except sqlite3.Error as e:
        if conn:
            conn.close()
        return f"Ошибка при формировании отчета о поставках для фирмы: {e}"


# Загрузка изображения в базу
def load_image_to_db(product_name, image_path):
    try:
        conn = sqlite3.connect('trade_firm.db')
        cursor = conn.cursor()

        with open(image_path, 'rb') as file:
            image_data = file.read()

        cursor.execute(
            "UPDATE products SET image = ? WHERE name = ?", (image_data, product_name)
        )
        conn.commit()
        conn.close()
        return "Изображение успешно загружено"
    except (sqlite3.Error, FileNotFoundError) as e:
        if conn:
            conn.rollback()
            conn.close()
        return f"Ошибка при загрузке изображения: {e}"

# Получение изображения из базы
def get_image_from_db(product_name):
    try:
        conn = sqlite3.connect('trade_firm.db')
        cursor = conn.cursor()
        cursor.execute("SELECT image FROM products WHERE name = ?", (product_name,))
        image_data = cursor.fetchone()
        conn.close()

        if image_data and image_data[0]:
            return image_data[0]
        return None
    except sqlite3.Error as e:
          if conn:
            conn.close()
          return f"Ошибка при получении изображения: {e}"


# Фильтрация товаров по категории
def get_products_by_category(category):
    try:
        conn = sqlite3.connect('trade_firm.db')
        cursor = conn.cursor()

        cursor.execute("CALL GetProductsByCategory(?)", (category,))

        products = cursor.fetchall()
        conn.close()
        return products
    except sqlite3.Error as e:
         if conn:
             conn.close()
         return f"Ошибка при фильтрации товаров по категории: {e}"


# Фильтрация товаров по имени
def get_products_by_name(name):
    try:
        conn = sqlite3.connect('trade_firm.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + name + '%',))
        products = cursor.fetchall()
        conn.close()
        return products
    except sqlite3.Error as e:
        if conn:
            conn.close()
        return f"Ошибка при фильтрации товаров по имени: {e}"

# Триггер для обновления даты поступления товара
def create_update_arrival_date_trigger():
    try:
        conn = sqlite3.connect('trade_firm.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS update_product_arrival_date
            AFTER UPDATE ON products
            BEGIN
                UPDATE products
                SET arrival_date = datetime('now')
                WHERE id = NEW.id
                AND NEW.quantity != OLD.quantity;
            END;
        ''')
        conn.commit()
        conn.close()
        return "Триггер для обновления даты поступления товара успешно создан"
    except sqlite3.Error as e:
        if conn:
            conn.close()
        return f"Ошибка при создании триггера для обновления даты поступления товара: {e}"


# Хранимая процедура для получения товаров по категории
def create_get_products_by_category_proc():
    try:
        conn = sqlite3.connect('trade_firm.db')
        cursor = conn.cursor()

        cursor.execute('''
        CREATE PROCEDURE IF NOT EXISTS GetProductsByCategory (category_name TEXT)
          BEGIN
             SELECT * FROM products WHERE category = category_name;
          END;
      ''')
        conn.commit()
        conn.close()
        return "Хранимая процедура для получения товаров по категории успешно создана"
    except sqlite3.Error as e:
         if conn:
             conn.close()
         return f"Ошибка при создании хранимой процедуры для получения товаров по категории: {e}"


# Функция для перемещения товара
def move_product(product_name, new_store_name):
    try:
        conn = sqlite3.connect('trade_firm.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE products SET store_name = ? WHERE name = ?", (new_store_name, product_name))
        conn.commit()
        conn.close()
        return "Товар успешно перемещен"
    except sqlite3.Error as e:
        if conn:
           conn.rollback()
           conn.close()
        return f"Ошибка перемещения товара {e}"



if __name__ == '__main__':
    message1 = create_update_arrival_date_trigger()
    message2 = create_get_products_by_category_proc()
    print(message1)
    print(message2)