import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import db_operations
from datetime import datetime
import base64
from PIL import Image, ImageTk
import io


def add_product():
    def save_product():
        name = name_entry.get()
        category = category_entry.get()
        characteristics = characteristics_entry.get("1.0", "end-1c")  # Получаем многострочный текст
        price = price_entry.get()
        quantity = quantity_entry.get()
        unit = unit_entry.get()
        arrival_date = datetime.now().strftime('%Y-%m-%d')
        store_name = store_entry.get()
        discount = discount_entry.get()
        vat = vat_entry.get()
        db_operations.insert_product(name, category, characteristics, price, quantity, unit, arrival_date, store_name,
                                     discount, vat, None)
        messagebox.showinfo("Успех", "Товар добавлен")
        add_window.destroy()

    add_window = tk.Toplevel(root)
    add_window.title("Добавить товар")

    tk.Label(add_window, text="Название товара:").grid(row=0, column=0, sticky="w")
    name_entry = tk.Entry(add_window)
    name_entry.grid(row=0, column=1, sticky="e")

    tk.Label(add_window, text="Категория:").grid(row=1, column=0, sticky="w")
    category_entry = tk.Entry(add_window)
    category_entry.grid(row=1, column=1, sticky="e")

    tk.Label(add_window, text="Характеристики:").grid(row=2, column=0, sticky="w")
    characteristics_entry = tk.Text(add_window, height=3)  # Используем Text виджет для многострочного ввода
    characteristics_entry.grid(row=2, column=1, sticky="e")

    tk.Label(add_window, text="Цена:").grid(row=3, column=0, sticky="w")
    price_entry = tk.Entry(add_window)
    price_entry.grid(row=3, column=1, sticky="e")

    tk.Label(add_window, text="Количество:").grid(row=4, column=0, sticky="w")
    quantity_entry = tk.Entry(add_window)
    quantity_entry.grid(row=4, column=1, sticky="e")

    tk.Label(add_window, text="Единица измерения:").grid(row=5, column=0, sticky="w")
    unit_entry = tk.Entry(add_window)
    unit_entry.grid(row=5, column=1, sticky="e")

    tk.Label(add_window, text="Название магазина:").grid(row=6, column=0, sticky="w")
    store_entry = tk.Entry(add_window)
    store_entry.grid(row=6, column=1, sticky="e")

    tk.Label(add_window, text="Скидка:").grid(row=7, column=0, sticky="w")
    discount_entry = tk.Entry(add_window)
    discount_entry.grid(row=7, column=1, sticky="e")

    tk.Label(add_window, text="НДС:").grid(row=8, column=0, sticky="w")
    vat_entry = tk.Entry(add_window)
    vat_entry.grid(row=8, column=1, sticky="e")

    tk.Button(add_window, text="Сохранить", command=save_product).grid(row=9, column=0, columnspan=2, pady=10)


def add_product_firm():
    def save_product_firm():
        product_name = product_name_entry.get()
        firm_name = firm_name_entry.get()
        message = db_operations.insert_product_firm(product_name, firm_name)
        messagebox.showinfo("Результат", message)
        add_firm_window.destroy()

    add_firm_window = tk.Toplevel(root)
    add_firm_window.title("Связать товар с фирмой")

    tk.Label(add_firm_window, text="Название товара:").grid(row=0, column=0, sticky="w")
    product_name_entry = tk.Entry(add_firm_window)
    product_name_entry.grid(row=0, column=1, sticky="e")

    tk.Label(add_firm_window, text="Название фирмы:").grid(row=1, column=0, sticky="w")
    firm_name_entry = tk.Entry(add_firm_window)
    firm_name_entry.grid(row=1, column=1, sticky="e")

    tk.Button(add_firm_window, text="Сохранить", command=save_product_firm).grid(row=2, column=0, columnspan=2, pady=10)


def show_all_products():
    products = db_operations.get_all_products()
    if products:
        show_window = tk.Toplevel(root)
        show_window.title("Все товары")
        display_products_in_treeview(show_window, products)
    else:
        messagebox.showinfo("Информация", "Нет товаров.")


def show_all_firms():
    firms = db_operations.get_all_firms()
    if firms:
        show_window = tk.Toplevel(root)
        show_window.title("Все фирмы")

        tree = ttk.Treeview(show_window, columns=("ID", "Название"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Название", text="Название")
        tree.grid(row=0, column=0)

        for firm in firms:
            tree.insert("", "end", values=(firm[0], firm[1]))
    else:
        messagebox.showinfo("Информация", "Нет фирм.")


def show_all_stores():
    stores = db_operations.get_all_stores()
    if stores:
        show_window = tk.Toplevel(root)
        show_window.title("Все магазины")

        tree = ttk.Treeview(show_window, columns=("ID", "Название"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Название", text="Название")
        tree.grid(row=0, column=0)

        for store in stores:
            tree.insert("", "end", values=(store[0], store[1]))

    else:
        messagebox.showinfo("Информация", "Нет магазинов.")


def show_delivery_report():
    def display_report():
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        report = db_operations.get_delivery_report(start_date, end_date)
        if report:
            show_window = tk.Toplevel(report_window)
            show_window.title("Отчет о поставках за период")
            tree = ttk.Treeview(show_window,
                                columns=("Товар", "Категория", "Количество", "Цена", "Магазин", "Дата", "Фирма"),
                                show="headings")
            tree.heading("Товар", text="Товар")
            tree.heading("Категория", text="Категория")
            tree.heading("Количество", text="Количество")
            tree.heading("Цена", text="Цена")
            tree.heading("Магазин", text="Магазин")
            tree.heading("Дата", text="Дата")
            tree.heading("Фирма", text="Фирма")
            tree.grid(row=0, column=0)

            for record in report:
                tree.insert("", "end",
                            values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6]))

        else:
            messagebox.showinfo("Информация", "Нет данных о поставках за этот период.")

    report_window = tk.Toplevel(root)
    report_window.title("Отчет по поставкам за период")

    tk.Label(report_window, text="Начальная дата (YYYY-MM-DD):").grid(row=0, column=0, sticky="w")
    start_date_entry = tk.Entry(report_window)
    start_date_entry.grid(row=0, column=1, sticky="e")

    tk.Label(report_window, text="Конечная дата (YYYY-MM-DD):").grid(row=1, column=0, sticky="w")
    end_date_entry = tk.Entry(report_window)
    end_date_entry.grid(row=1, column=1, sticky="e")

    tk.Button(report_window, text="Показать отчет", command=display_report).grid(row=2, column=0, columnspan=2, pady=10)


def show_delivery_report_by_store():
    def display_report_store():
        store_name = store_name_entry.get()
        report = db_operations.get_delivery_report_by_store(store_name)
        if report:
            show_window = tk.Toplevel(report_store_window)
            show_window.title(f"Отчет о поставках для магазина {store_name}")
            tree = ttk.Treeview(show_window, columns=("Товар", "Категория", "Количество", "Цена", "Дата", "Фирма"),
                                show="headings")
            tree.heading("Товар", text="Товар")
            tree.heading("Категория", text="Категория")
            tree.heading("Количество", text="Количество")
            tree.heading("Цена", text="Цена")
            tree.heading("Дата", text="Дата")
            tree.heading("Фирма", text="Фирма")
            tree.grid(row=0, column=0)

            for record in report:
                tree.insert("", "end", values=(record[0], record[1], record[2], record[3], record[4], record[5]))
        else:
            messagebox.showinfo("Информация", f"Нет данных о поставках для магазина {store_name}.")

    report_store_window = tk.Toplevel(root)
    report_store_window.title("Отчет по поставкам для магазина")

    tk.Label(report_store_window, text="Название магазина:").grid(row=0, column=0, sticky="w")
    store_name_entry = tk.Entry(report_store_window)
    store_name_entry.grid(row=0, column=1, sticky="e")

    tk.Button(report_store_window, text="Показать отчет", command=display_report_store).grid(row=1, column=0,
                                                                                             columnspan=2, pady=10)


def show_delivery_report_by_firm():
    def display_report_firm():
        firm_name = firm_name_entry.get()
        report = db_operations.get_delivery_report_by_firm(firm_name)
        if report:
            show_window = tk.Toplevel(report_firm_window)
            show_window.title(f"Отчет о поставках для фирмы {firm_name}")
            tree = ttk.Treeview(show_window, columns=("Товар", "Категория", "Количество", "Цена", "Дата", "Магазин"),
                                show="headings")
            tree.heading("Товар", text="Товар")
            tree.heading("Категория", text="Категория")
            tree.heading("Количество", text="Количество")
            tree.heading("Цена", text="Цена")
            tree.heading("Дата", text="Дата")
            tree.heading("Магазин", text="Магазин")
            tree.grid(row=0, column=0)

            for record in report:
                tree.insert("", "end", values=(record[0], record[1], record[2], record[3], record[4], record[5]))
        else:
            messagebox.showinfo("Информация", f"Нет данных о поставках для фирмы {firm_name}.")

    report_firm_window = tk.Toplevel(root)
    report_firm_window.title("Отчет по поставкам для фирмы")

    tk.Label(report_firm_window, text="Название фирмы:").grid(row=0, column=0, sticky="w")
    firm_name_entry = tk.Entry(report_firm_window)
    firm_name_entry.grid(row=0, column=1, sticky="e")

    tk.Button(report_firm_window, text="Показать отчет", command=display_report_firm).grid(row=1, column=0,
                                                                                           columnspan=2, pady=10)


def load_product_image():
    def upload_image():
        product_name = product_name_entry.get()
        file_path = filedialog.askopenfilename()
        if file_path:
            message = db_operations.load_image_to_db(product_name, file_path)
            messagebox.showinfo("Результат", message)
            image_window.destroy()

    image_window = tk.Toplevel(root)
    image_window.title("Загрузить изображение")

    tk.Label(image_window, text="Название товара:").grid(row=0, column=0, sticky="w")
    product_name_entry = tk.Entry(image_window)
    product_name_entry.grid(row=0, column=1, sticky="e")

    tk.Button(image_window, text="Выбрать файл", command=upload_image).grid(row=1, column=0, columnspan=2, pady=10)


def view_product_image():
    def display_image():
        product_name = product_name_entry.get()
        image_data = db_operations.get_image_from_db(product_name)
        if image_data:
            try:
                image = Image.open(io.BytesIO(image_data))
                image = image.resize((300, 300), Image.LANCZOS)  # меняем размер
                photo = ImageTk.PhotoImage(image)
                image_label.config(image=photo)
                image_label.image = photo
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось отобразить изображение: {e}")
        else:
            messagebox.showinfo("Информация", "Изображение не найдено")

    view_image_window = tk.Toplevel(root)
    view_image_window.title("Посмотреть изображение")

    tk.Label(view_image_window, text="Название товара:").grid(row=0, column=0, sticky="w")
    product_name_entry = tk.Entry(view_image_window)
    product_name_entry.grid(row=0, column=1, sticky="e")

    tk.Button(view_image_window, text="Посмотреть изображение", command=display_image).grid(row=1, column=0,
                                                                                            columnspan=2, pady=10)
    image_label = tk.Label(view_image_window)
    image_label.grid(row=2, column=0, columnspan=2, pady=10)


def show_products_by_category():
    def show_products():
        category = category_entry.get()
        products = db_operations.get_products_by_category(category)
        if products:
            show_window = tk.Toplevel(category_window)
            show_window.title(f"Товары категории {category}")
            display_products_in_treeview(show_window, products)
        else:
            messagebox.showinfo("Информация", "Нет товаров этой категории")

    category_window = tk.Toplevel(root)
    category_window.title("Товары по категории")

    tk.Label(category_window, text="Название категории:").grid(row=0, column=0, sticky="w")
    category_entry = tk.Entry(category_window)
    category_entry.grid(row=0, column=1, sticky="e")

    tk.Button(category_window, text="Показать товары", command=show_products).grid(row=1, column=0, columnspan=2,
                                                                                   pady=10)


def filter_products_by_name():
    def show_filtered_products():
        name = name_entry.get()
        products = db_operations.get_products_by_name(name)
        if products:
            show_window = tk.Toplevel(filter_window)
            show_window.title(f"Товары, содержащие в названии '{name}'")
            display_products_in_treeview(show_window, products)
        else:
            messagebox.showinfo("Информация", "Нет товаров, удовлетворяющих условию")

    filter_window = tk.Toplevel(root)
    filter_window.title("Фильтрация товаров по названию")

    tk.Label(filter_window, text="Название товара:").grid(row=0, column=0, sticky="w")
    name_entry = tk.Entry(filter_window)
    name_entry.grid(row=0, column=1, sticky="e")
    tk.Button(filter_window, text="Показать", command=show_filtered_products).grid(row=1, column=0, columnspan=2,
                                                                                   pady=10)


def move_product_to_store():
    def transfer_product():
        product_name = product_name_entry.get()
        new_store_name = store_name_entry.get()
        message = db_operations.move_product(product_name, new_store_name)
        messagebox.showinfo("Результат", message)
        move_window.destroy()

    move_window = tk.Toplevel(root)
    move_window.title("Переместить товар")

    tk.Label(move_window, text="Название товара:").grid(row=0, column=0, sticky="w")
    product_name_entry = tk.Entry(move_window)
    product_name_entry.grid(row=0, column=1, sticky="e")

    tk.Label(move_window, text="Новый магазин:").grid(row=1, column=0, sticky="w")
    store_name_entry = tk.Entry(move_window)
    store_name_entry.grid(row=1, column=1, sticky="e")

    tk.Button(move_window, text="Переместить", command=transfer_product).grid(row=2, column=0, columnspan=2, pady=10)


def display_products_in_treeview(parent, products):
    tree = ttk.Treeview(parent, columns=("ID", "Название", "Категория", "Цена", "Количество"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Название", text="Название")
    tree.heading("Категория", text="Категория")
    tree.heading("Цена", text="Цена")
    tree.heading("Количество", text="Количество")
    tree.grid(row=0, column=0)

    for product in products:
        tree.insert('', 'end', values=(product[0], product[1], product[2], product[4], product[5]))


root = tk.Tk()
root.title("Торговая фирма-посредник")
root.geometry("800x800")

main_menu = tk.Menu(root)
root.config(menu=main_menu)

products_menu = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="Товары", menu=products_menu)
products_menu.add_command(label="Добавить товар", command=add_product)
products_menu.add_command(label="Связать товар с фирмой", command=add_product_firm)
products_menu.add_command(label="Показать все товары", command=show_all_products)
products_menu.add_command(label="Фильтрация по названию", command=filter_products_by_name)
products_menu.add_command(label="Переместить товар", command=move_product_to_store)
products_menu.add_command(label="Загрузить изображение товара", command=load_product_image)
products_menu.add_command(label="Посмотреть изображение товара", command=view_product_image)
products_menu.add_command(label="Показать товары заданной категории", command=show_products_by_category)

firms_menu = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="Фирмы", menu=firms_menu)
firms_menu.add_command(label="Показать все фирмы", command=show_all_firms)

stores_menu = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="Магазины", menu=stores_menu)
stores_menu.add_command(label="Показать все магазины", command=show_all_stores)

report_menu = tk.Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="Отчеты", menu=report_menu)
report_menu.add_command(label="Отчет по поставкам за период", command=show_delivery_report)
report_menu.add_command(label="Отчет по поставкам для заданного магазина", command=show_delivery_report_by_store)
report_menu.add_command(label="Отчет по поставкам для заданной фирмы", command=show_delivery_report_by_firm)

root.mainloop()