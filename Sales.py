from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql
from datetime import datetime

def connect_database():
    try:
        connection = pymysql.connect(host='localhost', user='root', password='anees123', database='inventory_system')
        cursor = connection.cursor()
        return connection, cursor
    except pymysql.Error as e:
        messagebox.showerror('Error', f'Database connection error: {e}')
        return None, None

def create_sales_table():
    connection, cursor = connect_database()
    if connection:
        try:
            cursor.execute('CREATE TABLE IF NOT EXISTS sales_data(id INT PRIMARY KEY AUTO_INCREMENT, product_name VARCHAR(100),'
                           'quantity_sold INT, total_price DECIMAL(10,2), sale_date DATE)')
            connection.commit()
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error creating sales table: {e}')
        finally:
            connection.close()

create_sales_table()

def fetch_products():
    connection, cursor = connect_database()
    if connection:
        try:
            cursor.execute('SELECT name, price, quantity FROM product_data')
            products = cursor.fetchall()
            return products
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error fetching products: {e}')
            return []
        finally:
            connection.close()
    return []

def clear_fields():
    global quantity_entry, total_price_entry, sale_date_entry, product_combo
    quantity_entry.delete(0, END)
    total_price_entry.delete(0, END)
    sale_date_entry.delete(0, END)
    sale_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
    product_combo.set('Select Product')

def fetch_sales():
    connection, cursor = connect_database()
    if connection:
        try:
            cursor.execute('SELECT * FROM sales_data')
            rows = cursor.fetchall()
            global sales_table
            sales_table.delete(*sales_table.get_children())
            for row in rows:
                sales_table.insert('', END, values=row)
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error fetching sales: {e}')
        finally:
            connection.close()

def populate_sale_details(event):
    global sales_table, quantity_entry, total_price_entry, sale_date_entry, product_combo
    selected_item = sales_table.focus()
    if selected_item:
        values = sales_table.item(selected_item)['values']
        product_combo.set(values[1])
        quantity_entry.delete(0, END)
        quantity_entry.insert(0, values[2])
        total_price_entry.delete(0, END)
        total_price_entry.insert(0, values[3])
        sale_date_entry.delete(0, END)
        sale_date_entry.insert(0, values[4])

def update_total_price(event=None):
    global product_combo, quantity_entry, total_price_entry, product_dict
    try:
        product_name = product_combo.get()
        quantity = int(quantity_entry.get()) if quantity_entry.get() else 0
        if product_name != 'Select Product' and quantity > 0:
            price = product_dict.get(product_name, {}).get('price', 0)
            total_price = price * quantity
            total_price_entry.delete(0, END)
            total_price_entry.insert(0, f"{total_price:.2f}")
        else:
            total_price_entry.delete(0, END)
            total_price_entry.insert(0, '0.00')
    except ValueError:
        total_price_entry.delete(0, END)
        total_price_entry.insert(0, '0.00')

def add_sale():
    global product_combo, quantity_entry, total_price_entry, sale_date_entry
    connection, cursor = connect_database()
    if connection:
        try:
            product_name = product_combo.get()
            quantity_sold = quantity_entry.get().strip()
            total_price = total_price_entry.get().strip()
            sale_date = sale_date_entry.get().strip()

            if not all([product_name, quantity_sold, total_price, sale_date]) or product_name == 'Select Product':
                messagebox.showerror('Error', 'All fields are required.')
                return

            try:
                quantity_sold = int(quantity_sold)
                total_price = float(total_price)
                sale_date = datetime.strptime(sale_date, '%Y-%m-%d').date()
            except ValueError:
                messagebox.showerror('Error', 'Quantity must be an integer, Total Price a number, and Sale Date in YYYY-MM-DD format.')
                return

            # Check product quantity
            product_info = product_dict.get(product_name, {})
            available_quantity = product_info.get('quantity', 0)
            if quantity_sold > available_quantity:
                messagebox.showerror('Error', f'Insufficient stock. Available quantity: {available_quantity}')
                return

            # Update product quantity
            cursor.execute('UPDATE product_data SET quantity = quantity - %s WHERE name = %s', (quantity_sold, product_name))
            connection.commit()

            # Insert sale record
            cursor.execute('INSERT INTO sales_data (product_name, quantity_sold, total_price, sale_date) VALUES (%s, %s, %s, %s)',
                           (product_name, quantity_sold, total_price, sale_date))
            connection.commit()
            messagebox.showinfo('Success', 'Sale recorded successfully!')
            clear_fields()
            fetch_sales()
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error adding sale: {e}')
        finally:
            connection.close()

def update_sale():
    global sales_table, product_combo, quantity_entry, total_price_entry, sale_date_entry
    connection, cursor = connect_database()
    if connection:
        try:
            selected_item = sales_table.focus()
            if not selected_item:
                messagebox.showerror('Error', 'Please select a sale to update.')
                return

            sale_id = sales_table.item(selected_item)['values'][0]
            old_product_name = sales_table.item(selected_item)['values'][1]
            old_quantity_sold = sales_table.item(selected_item)['values'][2]

            product_name = product_combo.get()
            quantity_sold = quantity_entry.get().strip()
            total_price = total_price_entry.get().strip()
            sale_date = sale_date_entry.get().strip()

            if not all([product_name, quantity_sold, total_price, sale_date]) or product_name == 'Select Product':
                messagebox.showerror('Error', 'All fields are required for update.')
                return

            try:
                quantity_sold = int(quantity_sold)
                total_price = float(total_price)
                sale_date = datetime.strptime(sale_date, '%Y-%m-%d').date()
            except ValueError:
                messagebox.showerror('Error', 'Quantity must be an integer, Total Price a number, and Sale Date in YYYY-MM-DD format.')
                return

            # Check product quantity
            product_info = product_dict.get(product_name, {})
            available_quantity = product_info.get('quantity', 0)
            if old_product_name == product_name:
                quantity_difference = quantity_sold - old_quantity_sold
            else:
                quantity_difference = quantity_sold
                # Restore old product's quantity
                cursor.execute('UPDATE product_data SET quantity = quantity + %s WHERE name = %s', (old_quantity_sold, old_product_name))
                connection.commit()

            if quantity_difference > available_quantity:
                messagebox.showerror('Error', f'Insufficient stock. Available quantity: {available_quantity}')
                return

            # Update product quantity
            cursor.execute('UPDATE product_data SET quantity = quantity - %s WHERE name = %s', (quantity_difference, product_name))
            connection.commit()

            # Update sale record
            cursor.execute('UPDATE sales_data SET product_name=%s, quantity_sold=%s, total_price=%s, sale_date=%s WHERE id=%s',
                           (product_name, quantity_sold, total_price, sale_date, sale_id))
            connection.commit()
            messagebox.showinfo('Success', 'Sale updated successfully!')
            clear_fields()
            fetch_sales()
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error updating sale: {e}')
        finally:
            connection.close()

def delete_sale():
    global sales_table
    connection, cursor = connect_database()
    if connection:
        try:
            selected_item = sales_table.focus()
            if not selected_item:
                messagebox.showerror('Error', 'Please select a sale to delete.')
                return

            sale_id = sales_table.item(selected_item)['values'][0]
            product_name = sales_table.item(selected_item)['values'][1]
            quantity_sold = sales_table.item(selected_item)['values'][2]

            confirm = messagebox.askyesno('Confirm', f'Are you sure you want to delete sale with ID: {sale_id}?')
            if confirm:
                # Restore product quantity
                cursor.execute('UPDATE product_data SET quantity = quantity + %s WHERE name = %s', (quantity_sold, product_name))
                connection.commit()

                # Delete sale record
                cursor.execute('DELETE FROM sales_data WHERE id=%s', (sale_id,))
                connection.commit()
                messagebox.showinfo('Success', 'Sale deleted successfully!')
                clear_fields()
                fetch_sales()
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error deleting sale: {e}')
        finally:
            connection.close()

def search_sale():
    global search_by_combo, search_entry, sales_table
    connection, cursor = connect_database()
    if connection:
        try:
            search_by = search_by_combo.get().lower()
            search_text = search_entry.get().lower()

            if search_by == 'select' or not search_text:
                messagebox.showerror('Error', 'Please select a search criteria and enter a value.')
                return

            if search_by == 'sale id':
                cursor.execute('SELECT * FROM sales_data WHERE id=%s', (search_text,))
            elif search_by == 'product':
                cursor.execute('SELECT * FROM sales_data WHERE LOWER(product_name) LIKE %s', ('%' + search_text + '%',))
            elif search_by == 'sale date':
                cursor.execute('SELECT * FROM sales_data WHERE sale_date=%s', (search_text,))
            else:
                messagebox.showerror('Error', 'Invalid search criteria.')
                return

            rows = cursor.fetchall()
            sales_table.delete(*sales_table.get_children())
            for row in rows:
                sales_table.insert('', END, values=row)
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error searching sales: {e}')
        finally:
            connection.close()

def show_all_sales():
    fetch_sales()

def sales_form(window, content_frame, draw_dashboard):
    global quantity_entry, total_price_entry, sale_date_entry, product_combo, sales_table, search_by_combo, search_entry, product_dict

    # Clear the content frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Fetch product data for dropdown and price calculation
    products = fetch_products()
    product_dict = {product[0]: {'price': product[1], 'quantity': product[2]} for product in products}
    product_names = ['Select Product'] + [product[0] for product in products]

    # --- Sales Form Frame ---
    sales_frame = Frame(content_frame, bg='white')
    sales_frame.place(x=0, y=0, width=1070, height=555)

    # Title for Sales Form
    sales_title = Label(sales_frame, text="Manage Sales Details", font=('times new roman', 20, 'bold'), bg='#010c48', fg='white')
    sales_title.pack(fill=X)

    # Back Button
    back_btn = Button(sales_frame, text="⬅", font=('times new roman', 15, 'bold'), command=draw_dashboard)
    back_btn.place(x=10, y=10)

    # --- Left Side: Input Form ---
    input_frame = Frame(sales_frame, bg='white')
    input_frame.place(x=10, y=50, width=400, height=450)

    # Product
    product_label = Label(input_frame, text="Product", font=('times new roman', 15), bg='white')
    product_label.pack(anchor='w', pady=5)
    product_combo = ttk.Combobox(input_frame, values=product_names, state='readonly', font=('times new roman', 12))
    product_combo.set("Select Product")
    product_combo.pack(fill=X)
    product_combo.bind("<<ComboboxSelected>>", update_total_price)

    # Quantity Sold
    quantity_label = Label(input_frame, text="Quantity Sold", font=('times new roman', 15), bg='white')
    quantity_label.pack(anchor='w', pady=5)
    quantity_entry = Entry(input_frame, font=('times new roman', 12), bg='lightyellow')
    quantity_entry.pack(fill=X)
    quantity_entry.bind("<KeyRelease>", update_total_price)

    # Total Price
    total_price_label = Label(input_frame, text="Total Price", font=('times new roman', 15), bg='white')
    total_price_label.pack(anchor='w', pady=5)
    total_price_entry = Entry(input_frame, font=('times new roman', 12), bg='lightyellow', state='readonly')
    total_price_entry.pack(fill=X)
    total_price_entry.insert(0, '0.00')

    # Sale Date
    sale_date_label = Label(input_frame, text="Sale Date (YYYY-MM-DD)", font=('times new roman', 15), bg='white')
    sale_date_label.pack(anchor='w', pady=5)
    sale_date_entry = Entry(input_frame, font=('times new roman', 12), bg='lightyellow')
    sale_date_entry.pack(fill=X)
    sale_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))

    # Buttons
    button_frame = Frame(input_frame, bg='white')
    button_frame.pack(fill=X, pady=20)

    add_btn = Button(button_frame, text="Add", font=('times new roman', 15, 'bold'), bg='#2196f3', fg='white', width=8, command=add_sale)
    add_btn.pack(side=LEFT, padx=5)

    update_btn = Button(button_frame, text="Update", font=('times new roman', 15, 'bold'), bg='#4caf50', fg='white', width=8, command=update_sale)
    update_btn.pack(side=LEFT, padx=5)

    delete_btn = Button(button_frame, text="Delete", font=('times new roman', 15, 'bold'), bg='#f44336', fg='white', width=8, command=delete_sale)
    delete_btn.pack(side=LEFT, padx=5)

    clear_btn = Button(button_frame, text="Clear", font=('times new roman', 15, 'bold'), bg='#ff9800', fg='white', width=8, command=clear_fields)
    clear_btn.pack(side=LEFT, padx=5)

    # --- Right Side: Search and Table ---
    search_frame = Frame(sales_frame, bg='white')
    search_frame.place(x=420, y=50, width=640, height=450)

    # Search Section
    search_label = Label(search_frame, text="Search Sales", font=('times new roman', 15, 'bold'), bg='white')
    search_label.pack(anchor='w')

    search_subframe = Frame(search_frame, bg='white')
    search_subframe.pack(fill=X, pady=5)

    search_by_label = Label(search_subframe, text="Search By", font=('times new roman', 12), bg='white')
    search_by_label.pack(side=LEFT)

    search_by_combo = ttk.Combobox(search_subframe, values=["Sale ID", "Product", "Sale Date"], state='readonly', font=('times new roman', 12), width=15)
    search_by_combo.set("Select")
    search_by_combo.pack(side=LEFT, padx=5)

    search_entry = Entry(search_subframe, font=('times new roman', 12), bg='lightyellow')
    search_entry.pack(side=LEFT, fill=X, expand=True, padx=5)

    search_btn = Button(search_subframe, text="Search", font=('times new roman', 12, 'bold'), bg='#0f4d7d', fg='white', command=search_sale)
    search_btn.pack(side=LEFT, padx=5)

    show_all_btn = Button(search_subframe, text="Show All", font=('times new roman', 12, 'bold'), bg='#0f4d7d', fg='white', command=show_all_sales)
    show_all_btn.pack(side=LEFT, padx=5)

    # Table
    table_frame = Frame(search_frame, bg='white')
    table_frame.pack(fill=BOTH, expand=True, pady=10)

    scrollbar_x = Scrollbar(table_frame, orient=HORIZONTAL)
    scrollbar_y = Scrollbar(table_frame, orient=VERTICAL)

    sales_table = ttk.Treeview(table_frame, columns=('Sale ID', 'Product', 'Quantity Sold', 'Total Price', 'Sale Date'), xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)

    scrollbar_x.pack(side=BOTTOM, fill=X)
    scrollbar_y.pack(side=RIGHT, fill=Y)

    scrollbar_x.config(command=sales_table.xview)
    scrollbar_y.config(command=sales_table.yview)

    sales_table.heading('Sale ID', text='Sale ID')
    sales_table.heading('Product', text='Product')
    sales_table.heading('Quantity Sold', text='Qty Sold')
    sales_table.heading('Total Price', text='Total Price')
    sales_table.heading('Sale Date', text='Sale Date')

    sales_table['show'] = 'headings'

    sales_table.column('Sale ID', width=80)
    sales_table.column('Product', width=150)
    sales_table.column('Quantity Sold', width=100)
    sales_table.column('Total Price', width=100)
    sales_table.column('Sale Date', width=100)

    sales_table.pack(fill=BOTH, expand=True)

    sales_table.bind("<ButtonRelease-1>", populate_sale_details)
    fetch_sales()