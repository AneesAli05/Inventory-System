from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql

def connect_database():
    try:
        connection = pymysql.connect(host='localhost', user='root', password='anees123', database='inventory_system')
        cursor = connection.cursor()
        return connection, cursor
    except pymysql.Error as e:
        messagebox.showerror('Error', f'Database connection error: {e}')
        return None, None

def create_supplier_table():
    connection, cursor = connect_database()
    if connection:
        try:
            cursor.execute('CREATE TABLE IF NOT EXISTS supplier_data(invoice_no INT PRIMARY KEY, supplier_name VARCHAR(100),'
                           'contact VARCHAR(30), description VARCHAR(255))')
            connection.commit()
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error creating supplier table: {e}')
        finally:
            connection.close()

create_supplier_table()

def clear_fields():
    global invoice_no_entry, supplier_name_entry, contact_entry, description_entry
    invoice_no_entry.delete(0, END)
    supplier_name_entry.delete(0, END)
    contact_entry.delete(0, END)
    description_entry.delete(0, END)

def fetch_suppliers():
    connection, cursor = connect_database()
    if connection:
        try:
            cursor.execute('SELECT * FROM supplier_data')
            rows = cursor.fetchall()
            global supplier_tree_view
            supplier_tree_view.delete(*supplier_tree_view.get_children())
            for row in rows:
                supplier_tree_view.insert('', END, values=row)
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error fetching suppliers: {e}')
        finally:
            connection.close()

def populate_supplier_details(event):
    global supplier_tree_view, invoice_no_entry, supplier_name_entry, contact_entry, description_entry
    selected_item = supplier_tree_view.focus()
    if selected_item:
        values = supplier_tree_view.item(selected_item)['values']
        invoice_no_entry.delete(0, END)
        invoice_no_entry.insert(0, values[0])
        supplier_name_entry.delete(0, END)
        supplier_name_entry.insert(0, values[1])
        contact_entry.delete(0, END)
        contact_entry.insert(0, values[2])
        description_entry.delete(0, END)
        description_entry.insert(0, values[3])

def save_supplier():
    global invoice_no_entry, supplier_name_entry, contact_entry, description_entry
    connection, cursor = connect_database()
    if connection:
        try:
            invoice_no = invoice_no_entry.get()
            supplier_name = supplier_name_entry.get()
            contact = contact_entry.get()
            description = description_entry.get()

            if not all([invoice_no, supplier_name, contact, description]):
                messagebox.showerror('Error', 'All fields are required.')
                return

            cursor.execute('INSERT INTO supplier_data VALUES (%s, %s, %s, %s)',
                           (invoice_no, supplier_name, contact, description))
            connection.commit()
            messagebox.showinfo('Success', 'Supplier data added successfully!')
            clear_fields()
            fetch_suppliers()
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error adding supplier: {e}')
        finally:
            connection.close()

def update_supplier():
    global supplier_tree_view, invoice_no_entry, supplier_name_entry, contact_entry, description_entry
    connection, cursor = connect_database()
    if connection:
        try:
            selected_item = supplier_tree_view.focus()
            if not selected_item:
                messagebox.showerror('Error', 'Please select a supplier to update.')
                return

            invoice_no = invoice_no_entry.get()
            supplier_name = supplier_name_entry.get()
            contact = contact_entry.get()
            description = description_entry.get()

            if not all([invoice_no, supplier_name, contact, description]):
                messagebox.showerror('Error', 'All fields are required for update.')
                return

            cursor.execute('UPDATE supplier_data SET supplier_name=%s, contact=%s, description=%s WHERE invoice_no=%s',
                           (supplier_name, contact, description, invoice_no))
            connection.commit()
            messagebox.showinfo('Success', 'Supplier data updated successfully!')
            clear_fields()
            fetch_suppliers()
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error updating supplier: {e}')
        finally:
            connection.close()

def delete_supplier():
    global supplier_tree_view
    connection, cursor = connect_database()
    if connection:
        try:
            selected_item = supplier_tree_view.focus()
            if not selected_item:
                messagebox.showerror('Error', 'Please select a supplier to delete.')
                return

            invoice = supplier_tree_view.item(selected_item)['values'][0]
            confirm = messagebox.askyesno('Confirm', f'Are you sure you want to delete supplier with Invoice No: {invoice}?')
            if confirm:
                cursor.execute('DELETE FROM supplier_data WHERE invoice_no=%s', (invoice,))
                connection.commit()
                messagebox.showinfo('Success', 'Supplier data deleted successfully!')
                clear_fields()
                fetch_suppliers()
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error deleting supplier: {e}')
        finally:
            connection.close()

def search_supplier():
    global search_combo, search_entry, supplier_tree_view
    connection, cursor = connect_database()
    if connection:
        try:
            search_by = search_combo.get().lower()
            search_text = search_entry.get().lower()

            if search_by == 'search by' or not search_text:
                messagebox.showerror('Error', 'Please select a search criteria and enter a value.')
                return

            if search_by == 'invoice no.':
                cursor.execute('SELECT * FROM supplier_data WHERE invoice_no=%s', (search_text,))
            elif search_by == 'name':
                cursor.execute('SELECT * FROM supplier_data WHERE LOWER(supplier_name) LIKE %s', ('%' + search_text + '%',))
            elif search_by == 'contact':
                cursor.execute('SELECT * FROM supplier_data WHERE contact LIKE %s', ('%' + search_text + '%',))
            elif search_by == 'description':
                cursor.execute('SELECT * FROM supplier_data WHERE LOWER(description) LIKE %s', ('%' + search_text + '%',))
            else:
                messagebox.showerror('Error', 'Invalid search criteria.')
                return

            rows = cursor.fetchall()
            supplier_tree_view.delete(*supplier_tree_view.get_children())
            for row in rows:
                supplier_tree_view.insert('', END, values=row)
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error searching suppliers: {e}')
        finally:
            connection.close()

def show_all_suppliers():
    fetch_suppliers()
def supplier_form(window, content_frame, draw_dashboard):
    global invoice_no_entry, supplier_name_entry, contact_entry, description_entry, supplier_tree_view, search_combo, search_entry

    # Clear the content frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    supplier_frame = Frame(content_frame, bg='white')
    supplier_frame.place(x=0, y=0, width=1070, height=555)

    head_Label = Label(supplier_frame, text='Manage Supplier Details', font=('times new roman', 20, 'bold'), bg='#010c48', fg='white')
    head_Label.pack(fill=X)

    # Back Button
    back_btn = Button(supplier_frame, text="⬅", font=('times new roman', 15, 'bold'), command=lambda: draw_dashboard(content_frame))
    back_btn.place(x=10, y=10)

    top_frame = Frame(supplier_frame, bg='white')
    top_frame.place(x=0, y=50, relwidth=1, height=235)

    search_frame = Frame(top_frame, bg='white')
    search_frame.pack()
    search_combo = ttk.Combobox(search_frame, values=('Invoice No.', 'Name', 'Contact', 'Description'), font=('times new roman', 12), state='readonly', width=15)
    search_combo.set('Search by')
    search_combo.grid(row=0, column=0, padx=20)

    search_entry = Entry(search_frame, font=('times new roman', 12), bg='lightyellow', width=20)
    search_entry.grid(row=0, column=1)

    search_btn = Button(search_frame, text='Search', font=('times new roman', 12), width=10, cursor='hand2', fg='white', bg='#0f4d7d', command=search_supplier)
    search_btn.grid(row=0, column=2, padx=20)
    show_btn = Button(search_frame, text='Show All', font=('times new roman', 12), width=10, cursor='hand2', fg='white', bg='#0f4d7d', command=show_all_suppliers)
    show_btn.grid(row=0, column=3)

    horizontal_scrollbar = Scrollbar(top_frame, orient=HORIZONTAL)
    vertical_scrollbar = Scrollbar(top_frame, orient=VERTICAL)
    supplier_tree_view = ttk.Treeview(top_frame, columns=('invoice_no', 'supplier_name', 'contact', 'description'), show='headings',
                                    yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    vertical_scrollbar.pack(side=RIGHT, fill=Y, pady=(10, 0))
    horizontal_scrollbar.config(command=supplier_tree_view.xview)
    vertical_scrollbar.config(command=supplier_tree_view.yview)
    supplier_tree_view.pack(pady=(10, 0))

    supplier_tree_view.heading('invoice_no', text='Invoice No.')
    supplier_tree_view.heading('supplier_name', text='Name')
    supplier_tree_view.heading('contact', text='Contact')
    supplier_tree_view.heading('description', text='Description')

    supplier_tree_view.column('invoice_no', width=100)
    supplier_tree_view.column('supplier_name', width=200)
    supplier_tree_view.column('contact', width=150)
    supplier_tree_view.column('description', width=300)

    supplier_tree_view.bind("<ButtonRelease-1>", populate_supplier_details)
    fetch_suppliers()  # Load initial data

    detail_frame = Frame(supplier_frame, bg='white')
    detail_frame.place(x=10, y=300, relwidth=1, height=200)

    # Configure column weights for detail_frame
    detail_frame.columnconfigure(1, weight=1)
    detail_frame.columnconfigure(3, weight=1)

    # Labels and Entry fields for Supplier Details
    invoice_no_lbl = Label(detail_frame, text="Invoice No.", font=('times new roman', 12, 'bold'), bg='white')
    invoice_no_lbl.grid(row=0, column=0, padx=(10, 5), pady=5, sticky='w')
    invoice_no_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow', width=20)
    invoice_no_entry.grid(row=0, column=1, padx=(5, 10), pady=5, sticky='ew')

    supplier_name_lbl = Label(detail_frame, text="Supplier Name", font=('times new roman', 12, 'bold'), bg='white')
    supplier_name_lbl.grid(row=0, column=2, padx=(10, 5), pady=5, sticky='w')
    supplier_name_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow', width=30)
    supplier_name_entry.grid(row=0, column=3, padx=(5, 10), pady=5, sticky='ew')

    contact_lbl = Label(detail_frame, text="Contact", font=('times new roman', 12, 'bold'), bg='white')
    contact_lbl.grid(row=1, column=0, padx=(10, 5), pady=5, sticky='w')
    contact_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow', width=20)
    contact_entry.grid(row=1, column=1, padx=(5, 10), pady=5, sticky='ew')

    description_lbl = Label(detail_frame, text="Description", font=('times new roman', 12, 'bold'), bg='white')
    description_lbl.grid(row=1, column=2, padx=(10, 5), pady=5, sticky='w')
    description_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow', width=30)
    description_entry.grid(row=1, column=3, padx=(5, 10), pady=5, sticky='ew')

    # Buttons for Save, Update, Delete, and Clear
    button_frame = Frame(detail_frame, bg='white')
    button_frame.grid(row=2, columnspan=4, pady=15)

    save_btn = Button(button_frame, text='Save', font=('times new roman', 12, 'bold'), bg='#2196f3', fg='white', width=10,
                      cursor='hand2', command=save_supplier)
    save_btn.grid(row=0, column=0, padx=10)

    update_btn = Button(button_frame, text='Update', font=('times new roman', 12, 'bold'), bg='#4caf50', fg='white',
                        width=10, cursor='hand2', command=update_supplier)
    update_btn.grid(row=0, column=1, padx=10)

    delete_btn = Button(button_frame, text='Delete', font=('times new roman', 12, 'bold'), bg='#f44336', fg='white',
                        width=10, cursor='hand2', command=delete_supplier)
    delete_btn.grid(row=0, column=2, padx=10)

    clear_btn = Button(button_frame, text='Clear', font=('times new roman', 12, 'bold'), bg='#ff9800', fg='white',
                       width=10, cursor='hand2', command=clear_fields)
    clear_btn.grid(row=0, column=3, padx=10)