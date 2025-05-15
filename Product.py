from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql

from Inventory_Management_System.Category import fetch_categories, clear_fields
from Inventory_Management_System.Suppliers import fetch_suppliers


#
# def connect_database():
#     try:
#         connection = pymysql.connect(host='localhost', user='root', password='anees123', database='inventory_system')
#         cursor = connection.cursor()
#         return connection, cursor
#     except pymysql.Error as e:
#         messagebox.showerror('Error', f'Database connection error: {e}')
#         return None, None
#
# def create_product_table():
#     connection, cursor = connect_database()
#     if connection:
#         try:
#             cursor.execute('CREATE TABLE IF NOT EXISTS product_data(id INT PRIMARY KEY AUTO_INCREMENT, category VARCHAR(100),'
#                            'supplier VARCHAR(100), name VARCHAR(100), price DECIMAL(10,2), quantity INT, status VARCHAR(50))')
#             connection.commit()
#         except pymysql.Error as e:
#             messagebox.showerror('Error', f'Error creating product table: {e}')
#         finally:
#             connection.close()
#
# create_product_table()
#
# def fetch_categories():
#     connection, cursor = connect_database()
#     if connection:
#         try:
#             cursor.execute('SELECT category_name FROM category_data')
#             categories = [row[0] for row in cursor.fetchall()]
#             return categories
#         except pymysql.Error as e:
#             messagebox.showerror('Error', f'Error fetching categories: {e}')
#             return []
#         finally:
#             connection.close()
#     return []
#
# def fetch_suppliers():
#     connection, cursor = connect_database()
#     if connection:
#         try:
#             cursor.execute('SELECT supplier_name FROM supplier_data')
#             suppliers = [row[0] for row in cursor.fetchall()]
#             return suppliers
#         except pymysql.Error as e:
#             messagebox.showerror('Error', f'Error fetching suppliers: {e}')
#             return []
#         finally:
#             connection.close()
#     return []
#
# def clear_fields():
#     global name_entry, price_entry, quantity_entry, category_combo, supplier_combo, status_combo
#     name_entry.delete(0, END)
#     price_entry.delete(0, END)
#     quantity_entry.delete(0, END)
#     category_combo.set('Select')
#     supplier_combo.set('Select')
#     status_combo.set('Select Status')
#
# def fetch_products():
#     connection, cursor = connect_database()
#     if connection:
#         try:
#             cursor.execute('SELECT * FROM product_data')
#             rows = cursor.fetchall()
#             global product_table
#             product_table.delete(*product_table.get_children())
#             for row in rows:
#                 product_table.insert('', END, values=row)
#         except pymysql.Error as e:
#             messagebox.showerror('Error', f'Error fetching products: {e}')
#         finally:
#             connection.close()
#
# def populate_product_details(event):
#     global product_table, name_entry, price_entry, quantity_entry, category_combo, supplier_combo, status_combo
#     selected_item = product_table.focus()
#     if selected_item:
#         values = product_table.item(selected_item)['values']
#         name_entry.delete(0, END)
#         name_entry.insert(0, values[3])
#         price_entry.delete(0, END)
#         price_entry.insert(0, values[4])
#         quantity_entry.delete(0, END)
#         quantity_entry.insert(0, values[5])
#         category_combo.set(values[1])
#         supplier_combo.set(values[2])
#         status_combo.set(values[6])
#
# def add_product():
#     global name_entry, price_entry, quantity_entry, category_combo, supplier_combo, status_combo
#     connection, cursor = connect_database()
#     if connection:
#         try:
#             category = category_combo.get()
#             supplier = supplier_combo.get()
#             name = name_entry.get().strip()
#             price = price_entry.get().strip()
#             quantity = quantity_entry.get().strip()
#             status = status_combo.get()
#
#             if not all([category, supplier, name, price, quantity, status]) or category == 'Select' or supplier == 'Select' or status == 'Select Status':
#                 messagebox.showerror('Error', 'All fields are required.')
#                 return
#
#             try:
#                 price = float(price)
#                 quantity = int(quantity)
#             except ValueError:
#                 messagebox.showerror('Error', 'Price must be a number and Quantity must be an integer.')
#                 return
#
#             cursor.execute('INSERT INTO product_data (category, supplier, name, price, quantity, status) VALUES (%s, %s, %s, %s, %s, %s)',
#                            (category, supplier, name, price, quantity, status))
#             connection.commit()
#             messagebox.showinfo('Success', 'Product added successfully!')
#             clear_fields()
#             fetch_products()
#         except pymysql.Error as e:
#             messagebox.showerror('Error', f'Error adding product: {e}')
#         finally:
#             connection.close()
#
# def update_product():
#     global product_table, name_entry, price_entry, quantity_entry, category_combo, supplier_combo, status_combo
#     connection, cursor = connect_database()
#     if connection:
#         try:
#             selected_item = product_table.focus()
#             if not selected_item:
#                 messagebox.showerror('Error', 'Please select a product to update.')
#                 return
#
#             product_id = product_table.item(selected_item)['values'][0]
#             category = category_combo.get()
#             supplier = supplier_combo.get()
#             name = name_entry.get().strip()
#             price = price_entry.get().strip()
#             quantity = quantity_entry.get().strip()
#             status = status_combo.get()
#
#             if not all([category, supplier, name, price, quantity, status]) or category == 'Select' or supplier == 'Select' or status == 'Select Status':
#                 messagebox.showerror('Error', 'All fields are required for update.')
#                 return
#
#             try:
#                 price = float(price)
#                 quantity = int(quantity)
#             except ValueError:
#                 messagebox.showerror('Error', 'Price must be a number and Quantity must be an integer.')
#                 return
#
#             cursor.execute('UPDATE product_data SET category=%s, supplier=%s, name=%s, price=%s, quantity=%s, status=%s WHERE id=%s',
#                            (category, supplier, name, price, quantity, status, product_id))
#             connection.commit()
#             messagebox.showinfo('Success', 'Product updated successfully!')
#             clear_fields()
#             fetch_products()
#         except pymysql.Error as e:
#             messagebox.showerror('Error', f'Error updating product: {e}')
#         finally:
#             connection.close()
#
# def delete_product():
#     global product_table
#     connection, cursor = connect_database()
#     if connection:
#         try:
#             selected_item = product_table.focus()
#             if not selected_item:
#                 messagebox.showerror('Error', 'Please select a product to delete.')
#                 return
#
#             product_id = product_table.item(selected_item)['values'][0]
#             confirm = messagebox.askyesno('Confirm', f'Are you sure you want to delete product with ID: {product_id}?')
#             if confirm:
#                 cursor.execute('DELETE FROM product_data WHERE id=%s', (product_id,))
#                 connection.commit()
#                 messagebox.showinfo('Success', 'Product deleted successfully!')
#                 clear_fields()
#                 fetch_products()
#         except pymysql.Error as e:
#             messagebox.showerror('Error', f'Error deleting product: {e}')
#         finally:
#             connection.close()
#
# def search_product():
#     global search_by_combo, search_entry, product_table
#     connection, cursor = connect_database()
#     if connection:
#         try:
#             search_by = search_by_combo.get().lower()
#             search_text = search_entry.get().lower()
#
#             if search_by == 'select' or not search_text:
#                 messagebox.showerror('Error', 'Please select a search criteria and enter a value.')
#                 return
#
#             if search_by == 'id':
#                 cursor.execute('SELECT * FROM product_data WHERE id=%s', (search_text,))
#             elif search_by == 'category':
#                 cursor.execute('SELECT * FROM product_data WHERE LOWER(category) LIKE %s', ('%' + search_text + '%',))
#             elif search_by == 'supplier':
#                 cursor.execute('SELECT * FROM product_data WHERE LOWER(supplier) LIKE %s', ('%' + search_text + '%',))
#             elif search_by == 'name':
#                 cursor.execute('SELECT * FROM product_data WHERE LOWER(name) LIKE %s', ('%' + search_text + '%',))
#             elif search_by == 'price':
#                 cursor.execute('SELECT * FROM product_data WHERE price=%s', (search_text,))
#             elif search_by == 'quantity':
#                 cursor.execute('SELECT * FROM product_data WHERE quantity=%s', (search_text,))
#             elif search_by == 'status':
#                 cursor.execute('SELECT * FROM product_data WHERE LOWER(status) LIKE %s', ('%' + search_text + '%',))
#             else:
#                 messagebox.showerror('Error', 'Invalid search criteria.')
#                 return
#
#             rows = cursor.fetchall()
#             product_table.delete(*product_table.get_children())
#             for row in rows:
#                 product_table.insert('', END, values=row)
#         except pymysql.Error as e:
#             messagebox.showerror('Error', f'Error searching products: {e}')
#         finally:
#             connection.close()
#
# def show_all_products():
#     fetch_products()
#
# def product_form(window):
#     global name_entry, price_entry, quantity_entry, category_combo, supplier_combo, status_combo, product_table, search_by_combo, search_entry
#
#     # Create a frame for the product form
#     product_frame = Frame(window, bg='white')
#     product_frame.place(x=0, y=0, width=1070, height=555)
#
#     # Title for Product Form
#     product_title = Label(product_frame, text="Manage Product Details", font=('times new roman', 20, 'bold'), bg='#010c48', fg='white')
#     product_title.pack(fill=X)
#
#     # Back Button
#     back_btn = Button(product_frame, text="⬅", font=('times new roman', 15, 'bold'), command=lambda: window.destroy())  # Close window on back button
#     back_btn.place(x=10, y=10)
#
#     # --- Left Side: Input Form ---
#     input_frame = Frame(product_frame, bg='white')
#     input_frame.place(x=10, y=50, width=400, height=450)
#
#     # Category
#     category_label = Label(input_frame, text="Category", font=('times new roman', 15), bg='white')
#     category_label.pack(anchor='w', pady=5)
#     categories = fetch_categories()
#     if not categories:
#         categories = ["Select"]
#     category_combo = ttk.Combobox(input_frame, values=categories, state='readonly', font=('times new roman', 12))
#     category_combo.set("Select")
#     category_combo.pack(fill=X)
#
#     # Supplier
#     supplier_label = Label(input_frame, text="Supplier", font=('times new roman', 15), bg='white')
#     supplier_label.pack(anchor='w', pady=5)
#     suppliers = fetch_suppliers()
#     if not suppliers:
#         suppliers = ["Select"]
#     supplier_combo = ttk.Combobox(input_frame, values=suppliers, state='readonly', font=('times new roman', 12))
#     supplier_combo.set("Select")
#     supplier_combo.pack(fill=X)
#
#     # Name
#     name_label = Label(input_frame, text="Name", font=('times new roman', 15), bg='white')
#     name_label.pack(anchor='w', pady=5)
#     name_entry = Entry(input_frame, font=('times new roman', 12), bg='lightyellow')
#     name_entry.pack(fill=X)
#
#     # Price
#     price_label = Label(input_frame, text="Price", font=('times new roman', 15), bg='white')
#     price_label.pack(anchor='w', pady=5)
#     price_entry = Entry(input_frame, font=('times new roman', 12), bg='lightyellow')
#     price_entry.pack(fill=X)
#
#     # Quantity
#     quantity_label = Label(input_frame, text="Quantity", font=('times new roman', 15), bg='white')
#     quantity_label.pack(anchor='w', pady=5)
#     quantity_entry = Entry(input_frame, font=('times new roman', 12), bg='lightyellow')
#     quantity_entry.pack(fill=X)
#
#     # Status
#     status_label = Label(input_frame, text="Status", font=('times new roman', 15), bg='white')
#     status_label.pack(anchor='w', pady=5)
#     status_combo = ttk.Combobox(input_frame, values=["Available", "Out of Stock"], state='readonly', font=('times new roman', 12))
#     status_combo.set("Select Status")
#     status_combo.pack(fill=X)
#
#     # Buttons
#     button_frame = Frame(input_frame, bg='white')
#     button_frame.pack(fill=X, pady=20)
#
#     add_btn = Button(button_frame, text="Add", font=('times new roman', 15, 'bold'), bg='#2196f3', fg='white', width=8, command=add_product)
#     add_btn.pack(side=LEFT, padx=5)
#
#     update_btn = Button(button_frame, text="Update", font=('times new roman', 15, 'bold'), bg='#4caf50', fg='white', width=8, command=update_product)
#     update_btn.pack(side=LEFT, padx=5)
#
#     delete_btn = Button(button_frame, text="Delete", font=('times new roman', 15, 'bold'), bg='#f44336', fg='white', width=8, command=delete_product)
#     delete_btn.pack(side=LEFT, padx=5)
#
#     clear_btn = Button(button_frame, text="Clear", font=('times new roman', 15, 'bold'), bg='#ff9800', fg='white', width=8, command=clear_fields)
#     clear_btn.pack(side=LEFT, padx=5)
#
#     # --- Right Side: Search and Table ---
#     search_frame = Frame(product_frame, bg='white')
#     search_frame.place(x=420, y=50, width=640, height=450)
#
#     # Search Section
#     search_label = Label(search_frame, text="Search Product", font=('times new roman', 15, 'bold'), bg='white')
#     search_label.pack(anchor='w')
#
#     search_subframe = Frame(search_frame, bg='white')
#     search_subframe.pack(fill=X, pady=5)
#
#     search_by_label = Label(search_subframe, text="Search By", font=('times new roman', 12), bg='white')
#     search_by_label.pack(side=LEFT)
#
#     search_by_combo = ttk.Combobox(search_subframe, values=["Id", "Category", "Supplier", "Name", "Price", "Quantity", "Status"], state='readonly', font=('times new roman', 12), width=15)
#     search_by_combo.set("Select")
#     search_by_combo.pack(side=LEFT, padx=5)
#
#     search_entry = Entry(search_subframe, font=('times new roman', 12), bg='lightyellow')
#     search_entry.pack(side=LEFT, fill=X, expand=True, padx=5)
#
#     search_btn = Button(search_subframe, text="Search", font=('times new roman', 12, 'bold'), bg='#0f4d7d', fg='white', command=search_product)
#     search_btn.pack(side=LEFT, padx=5)
#
#     show_all_btn = Button(search_subframe, text="Show All", font=('times new roman', 12, 'bold'), bg='#0f4d7d', fg='white', command=show_all_products)
#     show_all_btn.pack(side=LEFT, padx=5)
#
#     # Table
#     table_frame = Frame(search_frame, bg='white')
#     table_frame.pack(fill=BOTH, expand=True, pady=10)
#
#     scrollbar_x = Scrollbar(table_frame, orient=HORIZONTAL)
#     scrollbar_y = Scrollbar(table_frame, orient=VERTICAL)
#
#     product_table = ttk.Treeview(table_frame, columns=('Id', 'Category', 'Supplier', 'Name', 'Price', 'Quantity', 'Status'), xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
#
#     scrollbar_x.pack(side=BOTTOM, fill=X)
#     scrollbar_y.pack(side=RIGHT, fill=Y)
#
#     scrollbar_x.config(command=product_table.xview)
#     scrollbar_y.config(command=product_table.yview)
#
#     product_table.heading('Id', text='Id')
#     product_table.heading('Category', text='Category')
#     product_table.heading('Supplier', text='Supplier')
#     product_table.heading('Name', text='Name')
#     product_table.heading('Price', text='Price')
#     product_table.heading('Quantity', text='Quantity')
#     product_table.heading('Status', text='Status')
#
#     product_table['show'] = 'headings'
#
#     product_table.column('Id', width=50)
#     product_table.column('Category', width=100)
#     product_table.column('Supplier', width=100)
#     product_table.column('Name', width=100)
#     product_table.column('Price', width=80)
#     product_table.column('Quantity', width=80)
#     product_table.column('Status', width=100)
#
#     product_table.pack(fill=BOTH, expand=True)
#
#     product_table.bind("<ButtonRelease-1>", populate_product_details)
#     fetch_products()


def product_form(window, add_product=None, update_product=None, delete_product=None, search_product=None,
                 show_all_products=None, populate_product_details=None):
    global name_entry, price_entry, quantity_entry, category_combo, supplier_combo, status_combo, product_table, search_by_combo, search_entry

    # Create a frame for the product form
    product_frame = Frame(window, bg='white')
    product_frame.place(x=0, y=0, width=1070, height=555)

    # Title for Product Form
    product_title = Label(product_frame, text="Inventory Management System", font=('times new roman', 20, 'bold'),
                          bg='#010c48', fg='white')
    product_title.pack(fill=X)

    # Welcome and Date/Time
    info_frame = Frame(product_frame, bg='#010c48')
    info_frame.pack(fill=X)

    welcome_label = Label(info_frame, text="Welcome Admin", font=('times new roman', 12), bg='#010c48', fg='white')
    welcome_label.pack(side=LEFT, padx=10)

    date_label = Label(info_frame, text="Date: 10-05-2025", font=('times new roman', 12), bg='#010c48', fg='white')
    date_label.pack(side=LEFT, padx=10)

    time_label = Label(info_frame, text="Time: 01:00:00 PM", font=('times new roman', 12), bg='#010c48', fg='white')
    time_label.pack(side=LEFT, padx=10)

    # Menu Bar
    menu_frame = Frame(product_frame, bg='#010c48')
    menu_frame.pack(fill=X)

    menu_items = ["Employees", "Suppliers", "Categories", "Products", "Sales", "Exit"]
    for item in menu_items:
        btn = Button(menu_frame, text=item, font=('times new roman', 12), bg='#010c48', fg='white', bd=0)
        btn.pack(side=LEFT, padx=5)

    # Main Content Frame
    main_frame = Frame(product_frame, bg='white')
    main_frame.pack(fill=BOTH, expand=True)

    # Left Panel - Product Form
    left_frame = Frame(main_frame, bg='white', bd=2, relief=GROOVE)
    left_frame.pack(side=LEFT, fill=Y, padx=10, pady=10)

    form_title = Label(left_frame, text="Product Information", font=('times new roman', 16, 'bold'), bg='white')
    form_title.pack(fill=X, pady=5)

    # Category
    category_frame = Frame(left_frame, bg='white')
    category_frame.pack(fill=X, padx=5, pady=5)
    Label(category_frame, text="Category:", font=('times new roman', 12), bg='white').pack(side=LEFT)
    categories = fetch_categories()
    if not categories:
        categories = ["Select"]
    category_combo = ttk.Combobox(category_frame, values=categories, state='readonly', font=('times new roman', 12),
                                  width=20)
    category_combo.set("Select")
    category_combo.pack(side=RIGHT)

    # Supplier
    supplier_frame = Frame(left_frame, bg='white')
    supplier_frame.pack(fill=X, padx=5, pady=5)
    Label(supplier_frame, text="Supplier:", font=('times new roman', 12), bg='white').pack(side=LEFT)
    suppliers = fetch_suppliers()
    if not suppliers:
        suppliers = ["Select"]
    supplier_combo = ttk.Combobox(supplier_frame, values=suppliers, state='readonly', font=('times new roman', 12),
                                  width=20)
    supplier_combo.set("Select")
    supplier_combo.pack(side=RIGHT)

    # Name
    name_frame = Frame(left_frame, bg='white')
    name_frame.pack(fill=X, padx=5, pady=5)
    Label(name_frame, text="Name:", font=('times new roman', 12), bg='white').pack(side=LEFT)
    name_entry = Entry(name_frame, font=('times new roman', 12), bg='lightyellow')
    name_entry.pack(side=RIGHT)

    # Price
    price_frame = Frame(left_frame, bg='white')
    price_frame.pack(fill=X, padx=5, pady=5)
    Label(price_frame, text="Price:", font=('times new roman', 12), bg='white').pack(side=LEFT)
    price_entry = Entry(price_frame, font=('times new roman', 12), bg='lightyellow')
    price_entry.pack(side=RIGHT)

    # Quantity
    quantity_frame = Frame(left_frame, bg='white')
    quantity_frame.pack(fill=X, padx=5, pady=5)
    Label(quantity_frame, text="Quantity:", font=('times new roman', 12), bg='white').pack(side=LEFT)
    quantity_entry = Entry(quantity_frame, font=('times new roman', 12), bg='lightyellow')
    quantity_entry.pack(side=RIGHT)

    # Status
    status_frame = Frame(left_frame, bg='white')
    status_frame.pack(fill=X, padx=5, pady=5)
    Label(status_frame, text="Status:", font=('times new roman', 12), bg='white').pack(side=LEFT)
    status_combo = ttk.Combobox(status_frame, values=["Available", "Out of Stock"], state='readonly',
                                font=('times new roman', 12), width=20)
    status_combo.set("Select Status")
    status_combo.pack(side=RIGHT)

    # Action Buttons
    button_frame = Frame(left_frame, bg='white')
    button_frame.pack(fill=X, pady=10)

    add_btn = Button(button_frame, text="Add", font=('times new roman', 12, 'bold'), bg='#2196f3', fg='white', width=8,
                     command=add_product)
    add_btn.pack(side=LEFT, padx=5)

    update_btn = Button(button_frame, text="Update", font=('times new roman', 12, 'bold'), bg='#4caf50', fg='white',
                        width=8, command=update_product)
    update_btn.pack(side=LEFT, padx=5)

    delete_btn = Button(button_frame, text="Delete", font=('times new roman', 12, 'bold'), bg='#f44336', fg='white',
                        width=8, command=delete_product)
    delete_btn.pack(side=LEFT, padx=5)

    clear_btn = Button(button_frame, text="Clear", font=('times new roman', 12, 'bold'), bg='#ff9800', fg='white',
                       width=8, command=clear_fields)
    clear_btn.pack(side=LEFT, padx=5)

    # Right Panel - Search and Table
    right_frame = Frame(main_frame, bg='white', bd=2, relief=GROOVE)
    right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

    # Search Section
    search_title = Label(right_frame, text="Search Product", font=('times new roman', 16, 'bold'), bg='white')
    search_title.pack(fill=X, pady=5)

    search_frame = Frame(right_frame, bg='white')
    search_frame.pack(fill=X, padx=5, pady=5)

    Label(search_frame, text="Search By:", font=('times new roman', 12), bg='white').pack(side=LEFT)
    search_by_combo = ttk.Combobox(search_frame,
                                   values=["Id", "Category", "Supplier", "Name", "Price", "Quantity", "Status"],
                                   state='readonly', font=('times new roman', 12), width=15)
    search_by_combo.set("Select")
    search_by_combo.pack(side=LEFT, padx=5)

    search_entry = Entry(search_frame, font=('times new roman', 12), bg='lightyellow')
    search_entry.pack(side=LEFT, fill=X, expand=True, padx=5)

    search_btn = Button(search_frame, text="Search", font=('times new roman', 12, 'bold'), bg='#0f4d7d', fg='white',
                        command=search_product)
    search_btn.pack(side=LEFT, padx=5)

    show_all_btn = Button(search_frame, text="Show All", font=('times new roman', 12, 'bold'), bg='#0f4d7d', fg='white',
                          command=show_all_products)
    show_all_btn.pack(side=LEFT, padx=5)

    # Filter Section
    filter_frame = Frame(right_frame, bg='white')
    filter_frame.pack(fill=X, padx=5, pady=5)

    Label(filter_frame, text="Filter by Status:", font=('times new roman', 12), bg='white').pack(side=LEFT)
    filter_combo = ttk.Combobox(filter_frame, values=["All", "Available", "Out of Stock"],
                                state='readonly', font=('times new roman', 12), width=15)
    filter_combo.set("All")
    filter_combo.pack(side=LEFT, padx=5)

    # Product Table
    table_frame = Frame(right_frame, bg='white')
    table_frame.pack(fill=BOTH, expand=True, pady=10)

    scrollbar_x = Scrollbar(table_frame, orient=HORIZONTAL)
    scrollbar_y = Scrollbar(table_frame, orient=VERTICAL)

    product_table = ttk.Treeview(table_frame,
                                 columns=('Id', 'Category', 'Supplier', 'Name', 'Price', 'Quantity', 'Status'),
                                 xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

    scrollbar_x.pack(side=BOTTOM, fill=X)
    scrollbar_y.pack(side=RIGHT, fill=Y)

    scrollbar_x.config(command=product_table.xview)
    scrollbar_y.config(command=product_table.yview)

    # Configure columns
    product_table.heading('Id', text='Id')
    product_table.heading('Category', text='Category')
    product_table.heading('Supplier', text='Supplier')
    product_table.heading('Name', text='Name')
    product_table.heading('Price', text='Price')
    product_table.heading('Quantity', text='Quantity')
    product_table.heading('Status', text='Status')

    product_table['show'] = 'headings'

    product_table.column('Id', width=50, anchor=CENTER)
    product_table.column('Category', width=100, anchor=CENTER)
    product_table.column('Supplier', width=100, anchor=CENTER)
    product_table.column('Name', width=150, anchor=CENTER)
    product_table.column('Price', width=80, anchor=CENTER)
    product_table.column('Quantity', width=80, anchor=CENTER)
    product_table.column('Status', width=100, anchor=CENTER)

    product_table.pack(fill=BOTH, expand=True)

    product_table.bind("<ButtonRelease-1>", populate_product_details)
    fetch_products()