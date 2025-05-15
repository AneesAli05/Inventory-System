from tkinter import *
from Employees import emp_form
from Suppliers import supplier_form
from Category import category_form
from Sales import sales_form
from Product import product_form  # Import product_form function

def draw_dashboard():
    # Code to display dashboard layout
    print("Dashboard is displayed")
    # Or any other code that draws the dashboard screen.

def open_product_form(content_frame):
    product_form(window, content_frame, draw_dashboard)  # Open product form when needed

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
titleLabel.place(x=0, y=0, relwidth=1)

logout_btn = Button(window, text='Logout',
                      font=('times new roman', 20, 'bold'), fg='#010C48')
logout_btn.place(x=1100, y=10)

subtitleLabel = Label(window,
                      text='Welcome Admin\t\t Date: 10-05-2025\t\t Time: 01:00:00 PM',
                      font=('times new roman', 15), bg='#4d636d', fg='white')
subtitleLabel.place(x=0, y=70, relwidth=1)

# --- Left Menu Frame ---
left_frame = Frame(window)
left_frame.place(x=0, y=102, width=200, height=555)

logoImage = PhotoImage(file='checklist.png')
image_label = Label(left_frame, image=logoImage)
image_label.pack(fill=X)

menuLabel = Label(left_frame, text='Menu', font=('times new roman', 20),
                  bg='#009688')
menuLabel.pack(fill=X)

employeeIcon = PhotoImage(file='man.png')
employee_btn = Button(left_frame, image=employeeIcon, compound=LEFT,
                       text='Employees', font=('times new roman', 20, 'bold'),
                       anchor='w', padx=10, command=lambda: emp_form(window))
employee_btn.pack(fill=X)

supplierIcon = PhotoImage(file='wholesale.png')
supplier_btn = Button(left_frame, image=supplierIcon, compound=LEFT,
                       text='Suppliers', font=('times new roman', 20, 'bold'),
                       anchor='w', padx=10, command=lambda: supplier_form(window))
supplier_btn.pack(fill=X)

categoryIcon = PhotoImage(file='categorization.png')
category_btn = Button(left_frame, image=categoryIcon, compound=LEFT,
                       text='Categories', font=('times new roman', 20, 'bold'),
                       anchor='w', padx=10, command=lambda: category_form(window))
category_btn.pack(fill=X)

productIcon = PhotoImage(file='new-product.png')
product_btn = Button(left_frame, image=productIcon, compound=LEFT,
                      text='Products', font=('times new roman', 20, 'bold'),
                      anchor='w', padx=10,command=lambda :product_form(window))
product_btn.pack(fill=X)

salesIcon = PhotoImage(file='sales-agent.png')
sales_btn = Button(left_frame, image=salesIcon, compound=LEFT,
                    text='Sales', font=('times new roman', 20, 'bold'),
                    anchor='w', padx=10,command=lambda :sales_form(window))
sales_btn.pack(fill=X)

exitIcon = PhotoImage(file='exit.png')
exit_btn = Button(left_frame, image=exitIcon, compound=LEFT, text='Exit',
                   font=('times new roman', 20, 'bold'), anchor='w', padx=10,
                   command=window.quit)  # This will close the application
exit_btn.pack(fill=X)

# --- Dashboard Summary Frames ---
emp_frame = Frame(window, bg='#2c3e50', bd=3, relief=RIDGE)
emp_frame.place(x=400, y=125, height=170, width=280)
emp_frame_icon = PhotoImage(file='team.png')
total_emp_icon_lbl = Label(emp_frame, image=emp_frame_icon, bg='#2c3e50')
total_emp_icon_lbl.pack(pady=10)

total_emp_lbl = Label(emp_frame, text='Total Employees', bg='#2c3e50',
                      fg='white', font=('times new roman', 15, 'bold'))
total_emp_lbl.pack()

total_emp_count_lbl = Label(emp_frame, text='0', bg='#2c3e50', fg='white',
                            font=('times new roman', 15, 'bold'))
total_emp_count_lbl.pack()

supplier_frame = Frame(window, bg='#8e44ad', bd=3, relief=RIDGE)
supplier_frame.place(x=800, y=125, height=170, width=280)
sup_frame_icon = PhotoImage(file='truck.png')
total_sup_icon_lbl = Label(supplier_frame, image=sup_frame_icon, bg='#8e44ad')
total_sup_icon_lbl.pack(pady=10)

total_sup_lbl = Label(supplier_frame, text='Total Suppliers', bg='#8e44ad',
                      fg='white', font=('times new roman', 15, 'bold'))
total_sup_lbl.pack()

total_sup_count_lbl = Label(supplier_frame, text='0', bg='#8e44ad', fg='white',
                            font=('times new roman', 15, 'bold'))
total_sup_count_lbl.pack()

category_frame = Frame(window, bg='#27ae60', bd=3, relief=RIDGE)
category_frame.place(x=400, y=310, height=170, width=280)
cat_frame_icon = PhotoImage(file='classification.png')
total_cat_icon_lbl = Label(category_frame, image=cat_frame_icon,
                            bg='#27ae60')
total_cat_icon_lbl.pack(pady=10)

total_cat_lbl = Label(category_frame, text='Total Categories', bg='#27ae60',
                      fg='white', font=('times new roman', 15, 'bold'))
total_cat_lbl.pack()

total_cat_count_lbl = Label(category_frame, text='0', bg='#27ae60', fg='white',
                            font=('times new roman', 15, 'bold'))
total_cat_count_lbl.pack()

product_frame = Frame(window, bg='#98be53', bd=3, relief=RIDGE)
product_frame.place(x=800, y=310, height=170, width=280)
prod_frame_icon = PhotoImage(file='best-product.png')
total_prod_icon_lbl = Label(product_frame, image=prod_frame_icon,
                            bg='#98be53')
total_prod_icon_lbl.pack(pady=10)

total_prod_lbl = Label(product_frame, text='Total Products', bg='#98be53',
                      fg='white', font=('times new roman', 15, 'bold'))
total_prod_lbl.pack()

total_prod_count_lbl = Label(product_frame, text='0', bg='#99be53', fg='white',
                            font=('times new roman', 15, 'bold'))
total_prod_count_lbl.pack()

Sales_frame = Frame(window, bg='#e74c3c', bd=3, relief=RIDGE)
Sales_frame.place(x=600, y=495, height=170, width=280)
sale_frame_icon = PhotoImage(file='sales-manager.png')
total_sale_icon_lbl = Label(Sales_frame, image=sale_frame_icon,
                           bg='#e74c3c')
total_sale_icon_lbl.pack(pady=10)

total_sale_lbl = Label(Sales_frame, text='Total Sales', bg='#e74c3c',
                     fg='white', font=('times new roman', 15, 'bold'))
total_sale_lbl.pack()

total_sale_count_lbl = Label(Sales_frame, text='0', bg='#e74c3c', fg='white',
                           font=('times new roman', 15, 'bold'))
total_sale_count_lbl.pack()

window.mainloop()
