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

def create_category_table():
    connection, cursor = connect_database()
    if connection:
        try:
            cursor.execute('CREATE TABLE IF NOT EXISTS category_data(id INT PRIMARY KEY AUTO_INCREMENT, category_name VARCHAR(100) UNIQUE, description TEXT)')
            connection.commit()
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error creating category table: {e}')
        finally:
            connection.close()

create_category_table()

def clear_fields():
    global id_entry, category_name_entry, description_text
    id_entry.delete(0, END)
    category_name_entry.delete(0, END)
    description_text.delete('1.0', END)

def fetch_categories():
    connection, cursor = connect_database()
    if connection:
        try:
            cursor.execute('SELECT * FROM category_data')
            rows = cursor.fetchall()
            global category_tree_view
            category_tree_view.delete(*category_tree_view.get_children())
            for row in rows:
                category_tree_view.insert('', END, values=row)
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error fetching categories: {e}')
        finally:
            connection.close()

def populate_category_details(event):
    global category_tree_view, id_entry, category_name_entry, description_text
    selected_item = category_tree_view.focus()
    if selected_item:
        values = category_tree_view.item(selected_item)['values']
        id_entry.delete(0, END)
        id_entry.insert(0, values[0])
        category_name_entry.delete(0, END)
        category_name_entry.insert(0, values[1])
        description_text.delete('1.0', END)
        description_text.insert('1.0', values[2])

def add_category():
    global category_name_entry, description_text
    connection, cursor = connect_database()
    if connection:
        try:
            category_name = category_name_entry.get().strip()
            description = description_text.get('1.0', END).strip()

            if not category_name:
                messagebox.showerror('Error', 'Category Name is required.')
                return

            cursor.execute('INSERT INTO category_data (category_name, description) VALUES (%s, %s)',
                           (category_name, description))
            connection.commit()
            messagebox.showinfo('Success', 'Category added successfully!')
            clear_fields()
            fetch_categories()
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error adding category: {e}')
        finally:
            connection.close()

def delete_category():
    global category_tree_view
    connection, cursor = connect_database()
    if connection:
        try:
            selected_item = category_tree_view.focus()
            if not selected_item:
                messagebox.showerror('Error', 'Please select a category to delete.')
                return

            category_id = category_tree_view.item(selected_item)['values'][0]
            confirm = messagebox.askyesno('Confirm', f'Are you sure you want to delete category with ID: {category_id}?')
            if confirm:
                cursor.execute('DELETE FROM category_data WHERE id=%s', (category_id,))
                connection.commit()
                messagebox.showinfo('Success', 'Category deleted successfully!')
                clear_fields()
                fetch_categories()
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error deleting category: {e}')
        finally:
            connection.close()
def category_form(window, content_frame, draw_dashboard):
    global id_entry, category_name_entry, description_text, category_tree_view, category_image

    # Clear the content frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    category_frame = Frame(content_frame, bg='white')
    category_frame.place(x=0, y=0, width=1070, height=555)

    head_Label = Label(category_frame, text='Manage Category Details', font=('times new roman', 20, 'bold'), bg='#010c48', fg='white')
    head_Label.pack(fill=X)

    # Back Button
    back_btn = Button(category_frame, text="⬅", font=('times new roman', 15, 'bold'), command=lambda: draw_dashboard(content_frame))
    back_btn.place(x=10, y=10)

    # Top Right Frame for Input Fields
    input_frame = Frame(category_frame, bg='white')
    input_frame.place(x=500, y=50, width=550, height=150)

    id_lbl = Label(input_frame, text="Id", font=('times new roman', 12, 'bold'), bg='white')
    id_lbl.grid(row=0, column=0, padx=(10, 5), pady=5, sticky='w')
    id_entry = Entry(input_frame, font=('times new roman', 12), bg='lightYellow', width=10)
    id_entry.grid(row=0, column=1, padx=(5, 10), pady=5, sticky='ew')

    category_name_lbl = Label(input_frame, text="Category Name", font=('times new roman', 12, 'bold'), bg='white')
    category_name_lbl.grid(row=1, column=0, padx=(10, 5), pady=5, sticky='w')
    category_name_entry = Entry(input_frame, font=('times new roman', 12), bg='lightYellow', width=30)
    category_name_entry.grid(row=1, column=1, padx=(5, 10), pady=5, sticky='ew')

    description_lbl = Label(input_frame, text="Description", font=('times new roman', 12, 'bold'), bg='white')
    description_lbl.grid(row=2, column=0, padx=(10, 5), pady=5, sticky='nw')
    description_text = Text(input_frame, font=('times new roman', 12), bg='lightYellow', width=30, height=3)
    description_text.grid(row=2, column=1, padx=(5, 10), pady=5, sticky='ew')

    # BottomAvoid using the term "bottom" as it may be considered sensitive. Instead, consider using alternatives like "lower" or "below" when referring to the lower part of something. Left Frame for Image
    image_frame = Frame(category_frame, bg='white')
    image_frame.place(x=30, y=220, width=450, height=300)
    try:
        category_image = PhotoImage(file='new.png')
        category_image_label = Label(image_frame, image=category_image, bg='white')
        category_image_label.pack(fill=BOTH, expand=True)
    except FileNotFoundError:
        no_image_label = Label(image_frame, text='Category Image Not Found', font=('times new roman', 14), bg='white')
        no_image_label.pack(pady=50)

    # Bottom Right Frame for Buttons and Treeview
    bottom_right_frame = Frame(category_frame, bg='white')
    bottom_right_frame.place(x=500, y=220, width=550, height=300)

    button_frame = Frame(bottom_right_frame, bg='white')
    button_frame.pack(pady=10)

    add_btn = Button(button_frame, text='Add', font=('times new roman', 12, 'bold'), bg='#2196f3', fg='white', width=10,
                     cursor='hand2', command=add_category)
    add_btn.grid(row=0, column=0, padx=10)

    delete_btn = Button(button_frame, text='Delete', font=('times new roman', 12, 'bold'), bg='#f44336', fg='white',
                        width=10, cursor='hand2', command=delete_category)
    delete_btn.grid(row=0, column=1, padx=10)

    clear_btn = Button(button_frame, text='Clear', font=('times new roman', 12, 'bold'), bg='#ff9800', fg='white',
                       width=10, cursor='hand2', command=clear_fields)
    clear_btn.grid(row=0, column=2, padx=10)

    horizontal_scrollbar = Scrollbar(bottom_right_frame, orient=HORIZONTAL)
    vertical_scrollbar = Scrollbar(bottom_right_frame, orient=VERTICAL)
    category_tree_view = ttk.Treeview(bottom_right_frame, columns=('id', 'category_name', 'description'), show='headings',
                                     yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    vertical_scrollbar.pack(side=RIGHT, fill=Y, pady=(10, 0))
    horizontal_scrollbar.config(command=category_tree_view.xview)
    vertical_scrollbar.config(command=category_tree_view.yview)
    category_tree_view.pack(pady=(10, 0), fill=BOTH, expand=True)

    category_tree_view.heading('id', text='Id')
    category_tree_view.heading('category_name', text='Category Name')
    category_tree_view.heading('description', text='Description')

    category_tree_view.column('id', width=50)
    category_tree_view.column('category_name', width=200)
    category_tree_view.column('description', width=300)

    category_tree_view.bind("<ButtonRelease-1>", populate_category_details)
    fetch_categories() # Load initial data