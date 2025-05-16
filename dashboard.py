from tkinter import *
from Employees import emp_form
from Suppliers import supplier_form
from Category import category_form
from Sales import sales_form
from Product import product_form
from datetime import datetime
import time
import pymysql

# Database connection function
def connect_database():
    try:
        connection = pymysql.connect(host='localhost', user='root', password='anees123', database='inventory_system')
        cursor = connection.cursor()
        return connection, cursor
    except pymysql.Error as e:
        print(f"Database connection error: {e}")
        return None, None

def draw_dashboard(content_frame):
    # Clear the content frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Fetch counts from the database
    connection, cursor = connect_database()
    emp_count = sup_count = cat_count = prod_count = sale_count = 0

    if connection:
        try:
            # Fetch Employees count
            cursor.execute('SELECT COUNT(*) FROM employee_data')
            emp_count = cursor.fetchone()[0]

            # Fetch Suppliers count
            cursor.execute('SELECT COUNT(*) FROM supplier_data')
            sup_count = cursor.fetchone()[0]

            # Fetch Categories count
            cursor.execute('SELECT COUNT(*) FROM category_data')
            cat_count = cursor.fetchone()[0]

            # Fetch Products count
            cursor.execute('SELECT COUNT(*) FROM product_data')
            prod_count = cursor.fetchone()[0]

            # Fetch Sales count
            cursor.execute('SELECT COUNT(*) FROM sales_data')
            sale_count = cursor.fetchone()[0]

        except pymysql.Error as e:
            print(f"Error fetching counts: {e}")
        finally:
            connection.close()

    # Dashboard layout
    print("Dashboard is displayed")

    # Store PhotoImage objects to prevent garbage collection
    emp_frame_icon = PhotoImage(file='team.png')
    sup_frame_icon = PhotoImage(file='truck.png')
    cat_frame_icon = PhotoImage(file='classification.png')
    prod_frame_icon = PhotoImage(file='best-product.png')
    sale_frame_icon = PhotoImage(file='sales-manager.png')

    # --- Dashboard Summary Frames ---
    # Employees Frame (x=400, y=125 on window -> x=200, y=23 in content_frame)
    emp_frame = Frame(content_frame, bg='#2c3e50', bd=3, relief=RIDGE)
    emp_frame.place(x=200, y=23, height=170, width=280)
    total_emp_icon_lbl = Label(emp_frame, image=emp_frame_icon, bg='#2c3e50')
    total_emp_icon_lbl.image = emp_frame_icon  # Keep a reference
    total_emp_icon_lbl.place(relx=0.5, rely=0.3, anchor=CENTER)  # Center the icon

    # Subframe to center text labels
    emp_text_frame = Frame(emp_frame, bg='#2c3e50')
    emp_text_frame.place(relx=0.5, rely=0.7, anchor=CENTER)
    total_emp_lbl = Label(emp_text_frame, text='Total Employees', bg='#2c3e50',
                          fg='white', font=('times new roman', 15, 'bold'))
    total_emp_lbl.pack()
    total_emp_count_lbl = Label(emp_text_frame, text=str(emp_count), bg='#2c3e50', fg='white',
                                font=('times new roman', 15, 'bold'))
    total_emp_count_lbl.pack()

    # Suppliers Frame (x=800, y=125 on window -> x=600, y=23 in content_frame)
    supplier_frame = Frame(content_frame, bg='#8e44ad', bd=3, relief=RIDGE)
    supplier_frame.place(x=600, y=23, height=170, width=280)
    total_sup_icon_lbl = Label(supplier_frame, image=sup_frame_icon, bg='#8e44ad')
    total_sup_icon_lbl.image = sup_frame_icon  # Keep a reference
    total_sup_icon_lbl.place(relx=0.5, rely=0.3, anchor=CENTER)  # Center the icon

    # Subframe to center text labels
    sup_text_frame = Frame(supplier_frame, bg='#8e44ad')
    sup_text_frame.place(relx=0.5, rely=0.7, anchor=CENTER)
    total_sup_lbl = Label(sup_text_frame, text='Total Suppliers', bg='#8e44ad',
                          fg='white', font=('times new roman', 15, 'bold'))
    total_sup_lbl.pack()
    total_sup_count_lbl = Label(sup_text_frame, text=str(sup_count), bg='#8e44ad', fg='white',
                                font=('times new roman', 15, 'bold'))
    total_sup_count_lbl.pack()

    # Categories Frame (x=400, y=310 on window -> x=200, y=208 in content_frame)
    category_frame = Frame(content_frame, bg='#27ae60', bd=3, relief=RIDGE)
    category_frame.place(x=200, y=208, height=170, width=280)
    total_cat_icon_lbl = Label(category_frame, image=cat_frame_icon,
                               bg='#27ae60')
    total_cat_icon_lbl.image = cat_frame_icon  # Keep a reference
    total_cat_icon_lbl.place(relx=0.5, rely=0.3, anchor=CENTER)  # Center the icon

    # Subframe to center text labels
    cat_text_frame = Frame(category_frame, bg='#27ae60')
    cat_text_frame.place(relx=0.5, rely=0.7, anchor=CENTER)
    total_cat_lbl = Label(cat_text_frame, text='Total Categories', bg='#27ae60',
                          fg='white', font=('times new roman', 15, 'bold'))
    total_cat_lbl.pack()
    total_cat_count_lbl = Label(cat_text_frame, text=str(cat_count), bg='#27ae60', fg='white',
                                font=('times new roman', 15, 'bold'))
    total_cat_count_lbl.pack()

    # Products Frame (x=800, y=310 on window -> x=600, y=208 in content_frame)
    product_frame = Frame(content_frame, bg='#98be53', bd=3, relief=RIDGE)
    product_frame.place(x=600, y=208, height=170, width=280)
    total_prod_icon_lbl = Label(product_frame, image=prod_frame_icon,
                                bg='#98be53')
    total_prod_icon_lbl.image = prod_frame_icon  # Keep a reference
    total_prod_icon_lbl.place(relx=0.5, rely=0.3, anchor=CENTER)  # Center the icon

    # Subframe to center text labels
    prod_text_frame = Frame(product_frame, bg='#98be53')
    prod_text_frame.place(relx=0.5, rely=0.7, anchor=CENTER)
    total_prod_lbl = Label(prod_text_frame, text='Total Products', bg='#98be53',
                           fg='white', font=('times new roman', 15, 'bold'))
    total_prod_lbl.pack()
    total_prod_count_lbl = Label(prod_text_frame, text=str(prod_count), bg='#98be53', fg='white',
                                 font=('times new roman', 15, 'bold'))
    total_prod_count_lbl.pack()

    # Sales Frame (x=600, y=495 on window -> x=400, y=393 in content_frame)
    sales_frame = Frame(content_frame, bg='#e74c3c', bd=3, relief=RIDGE)
    sales_frame.place(x=400, y=393, height=170, width=280)
    total_sale_icon_lbl = Label(sales_frame, image=sale_frame_icon,
                                bg='#e74c3c')
    total_sale_icon_lbl.image = sale_frame_icon  # Keep a reference
    total_sale_icon_lbl.place(relx=0.5, rely=0.3, anchor=CENTER)  # Center the icon

    # Subframe to center text labels
    sale_text_frame = Frame(sales_frame, bg='#e74c3c')
    sale_text_frame.place(relx=0.5, rely=0.7, anchor=CENTER)
    total_sale_lbl = Label(sale_text_frame, text='Total Sales', bg='#e74c3c',
                           fg='white', font=('times new roman', 15, 'bold'))
    total_sale_lbl.pack()
    total_sale_count_lbl = Label(sale_text_frame, text=str(sale_count), bg='#e74c3c', fg='white',
                                 font=('times new roman', 15, 'bold'))
    total_sale_count_lbl.pack()

window = Tk()
window.title("Dashboard")
window.geometry('1270x668+0+0')
window.resizable(0, 0)
window.config(bg='white')

# --- Title Section ---
bgImage = PhotoImage(file='inventory.png')
titleLabel = Label(window, image=bgImage, compound=LEFT,
                   text='  Inventory Management System',
                   font=('times new roman', 40, 'bold'), bg='#010c48',
                   fg='white', anchor='w', padx='20px')
titleLabel.image = bgImage  # Keep a reference
titleLabel.place(x=0, y=0, relwidth=1)

logout_btn = Button(window, text='Logout',
                    font=('times new roman', 20, 'bold'), fg='#010C48',
                    command=window.destroy)
logout_btn.place(x=1100, y=10)

subtitleLabel = Label(window,
                      text=f'Welcome Admin\t\t Date: {datetime.now().strftime("%d-%m-%Y")}\t\t Time: {time.strftime("%I:%M:%S %p")}',
                      font=('times new roman', 15), bg='#4d636d', fg='white')
subtitleLabel.place(x=0, y=70, relwidth=1)

# --- Left Menu Frame ---
left_frame = Frame(window)
left_frame.place(x=0, y=102, width=200, height=555)

logoImage = PhotoImage(file='checklist.png')
image_label = Label(left_frame, image=logoImage)
image_label.image = logoImage  # Keep a reference
image_label.pack(fill=X)

menuLabel = Label(left_frame, text='Menu', font=('times new roman', 20),
                  bg='#009688')
menuLabel.pack(fill=X)

employeeIcon = PhotoImage(file='man.png')
employee_btn = Button(left_frame, image=employeeIcon, compound=LEFT,
                      text='Employees', font=('times new roman', 20, 'bold'),
                      anchor='w', padx=10, command=lambda: emp_form(window,content_frame,draw_dashboard))
employee_btn.image = employeeIcon  # Keep a reference
employee_btn.pack(fill=X)

supplierIcon = PhotoImage(file='wholesale.png')
supplier_btn = Button(left_frame, image=supplierIcon, compound=LEFT,
                      text='Suppliers', font=('times new roman', 20, 'bold'),
                      anchor='w', padx=10, command=lambda: supplier_form(window,content_frame,draw_dashboard))
supplier_btn.image = supplierIcon  # Keep a reference
supplier_btn.pack(fill=X)

categoryIcon = PhotoImage(file='categorization.png')
category_btn = Button(left_frame, image=categoryIcon, compound=LEFT,
                      text='Categories', font=('times new roman', 20, 'bold'),
                      anchor='w', padx=10, command=lambda: category_form(window,content_frame,draw_dashboard))
category_btn.image = categoryIcon  # Keep a reference
category_btn.pack(fill=X)

productIcon = PhotoImage(file='new-product.png')
product_btn = Button(left_frame, image=productIcon, compound=LEFT,
                     text='Products', font=('times new roman', 20, 'bold'),
                     anchor='w', padx=10, command=lambda: product_form(window, content_frame, draw_dashboard))
product_btn.image = productIcon  # Keep a reference
product_btn.pack(fill=X)

salesIcon = PhotoImage(file='sales-agent.png')
sales_btn = Button(left_frame, image=salesIcon, compound=LEFT,
                   text='Sales', font=('times new roman', 20, 'bold'),
                   anchor='w', padx=10, command=lambda: sales_form(window, content_frame, draw_dashboard))
sales_btn.image = salesIcon  # Keep a reference
sales_btn.pack(fill=X)

exitIcon = PhotoImage(file='exit.png')
exit_btn = Button(left_frame, image=exitIcon, compound=LEFT, text='Exit',
                  font=('times new roman', 20, 'bold'), anchor='w', padx=10,
                  command=window.quit)
exit_btn.image = exitIcon  # Keep a reference
exit_btn.pack(fill=X)

# --- Content Frame ---
content_frame = Frame(window, bg='white')
content_frame.place(x=200, y=102, width=1070, height=555)

# Initial dashboard draw
draw_dashboard(content_frame)

window.mainloop()