from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql
from tkcalendar import Calendar

def connect_database():
    try:
        connection = pymysql.connect(host='localhost', user='root', password='anees123', database='inventory_system')
        cursor = connection.cursor()
        return connection, cursor
    except pymysql.Error as e:
        messagebox.showerror('Error', f'Database connection error: {e}')
        return None, None

def create_tables():
    connection, cursor = connect_database()
    if connection:
        try:
            cursor.execute('CREATE TABLE IF NOT EXISTS employee_data(empID INT PRIMARY KEY,name VARCHAR(100),'
                           'email VARCHAR(100),gender VARCHAR(50),dob VARCHAR(30),contact VARCHAR(30),employment_type VARCHAR(50),'
                           'education VARCHAR(50),work_shift VARCHAR(50),address VARCHAR(100),doj VARCHAR(30),salary VARCHAR(50), usertype VARCHAR(50),'
                           'password VARCHAR(50))')
            connection.commit()
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error creating table: {e}')
        finally:
            connection.close()

create_tables()

def clear_fields():
    global empid_entry, name_entry, email_entry, gender_combo, dob_entry, contact_entry, \
           employment_combo, education_entry, workshift_combo, address_entry, doj_entry, salary_entry, \
           usertype_combo, password_entry
    empid_entry.delete(0, END)
    name_entry.delete(0, END)
    email_entry.delete(0, END)
    gender_combo.set('Select Gender')
    dob_entry.delete(0, END)
    contact_entry.delete(0, END)
    employment_combo.set('Select Type')
    education_entry.delete(0, END)
    workshift_combo.set('Select Shift')
    address_entry.delete(0, END)
    doj_entry.delete(0, END)
    salary_entry.delete(0, END)
    usertype_combo.set('Select Type')
    password_entry.delete(0, END)

def fetch_employees():
    connection, cursor = connect_database()
    if connection:
        try:
            cursor.execute('SELECT * FROM employee_data')
            rows = cursor.fetchall()
            global employee_tree_view
            employee_tree_view.delete(*employee_tree_view.get_children())
            for row in rows:
                employee_tree_view.insert('', END, values=row)
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error fetching employees: {e}')
        finally:
            connection.close()

def populate_employee_details(event):
    global employee_tree_view, empid_entry, name_entry, email_entry, gender_combo, dob_entry, contact_entry, \
           employment_combo, education_entry, workshift_combo, address_entry, doj_entry, salary_entry, \
           usertype_combo, password_entry
    selected_item = employee_tree_view.focus()
    if selected_item:
        values = employee_tree_view.item(selected_item)['values']
        empid_entry.delete(0, END)
        empid_entry.insert(0, values[0])
        name_entry.delete(0, END)
        name_entry.insert(0, values[1])
        email_entry.delete(0, END)
        email_entry.insert(0, values[2])
        gender_combo.set(values[3])
        dob_entry.delete(0, END)
        dob_entry.insert(0, values[4])
        contact_entry.delete(0, END)
        contact_entry.insert(0, values[5])
        employment_combo.set(values[6])
        education_entry.delete(0, END)
        education_entry.insert(0, values[7])
        workshift_combo.set(values[8])
        address_entry.delete(0, END)
        address_entry.insert(0, values[9])
        doj_entry.delete(0, END)
        doj_entry.insert(0, values[10])
        salary_entry.delete(0, END)
        salary_entry.insert(0, values[11])
        usertype_combo.set(values[12])
        password_entry.delete(0, END) # Consider if you want to populate the password field

def save_employee():
    global empid_entry, name_entry, email_entry, gender_combo, dob_entry, contact_entry, \
           employment_combo, education_entry, workshift_combo, address_entry, doj_entry, salary_entry, \
           usertype_combo, password_entry
    connection, cursor = connect_database()
    if connection:
        try:
            empid = empid_entry.get()
            name = name_entry.get()
            email = email_entry.get()
            gender = gender_combo.get()
            dob = dob_entry.get()
            contact = contact_entry.get()
            employment_type = employment_combo.get()
            education = education_entry.get()
            work_shift = workshift_combo.get()
            address = address_entry.get()
            doj = doj_entry.get()
            salary = salary_entry.get()
            usertype = usertype_combo.get()
            password = password_entry.get()

            if not all([empid, name, email, gender, dob, contact, employment_type, education, work_shift, address, doj, salary, usertype, password]):
                messagebox.showerror('Error', 'All fields are required.')
                return

            cursor.execute('INSERT INTO employee_data VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                           (empid, name, email, gender, dob, contact, employment_type, education, work_shift, address, doj, salary, usertype, password))
            connection.commit()
            messagebox.showinfo('Success', 'Employee data added successfully!')
            clear_fields()
            fetch_employees()
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error adding employee: {e}')
        finally:
            connection.close()

def update_employee():
    global employee_tree_view, empid_entry, name_entry, email_entry, gender_combo, dob_entry, contact_entry, \
           employment_combo, education_entry, workshift_combo, address_entry, doj_entry, salary_entry, \
           usertype_combo, password_entry
    connection, cursor = connect_database()
    if connection:
        try:
            selected_item = employee_tree_view.focus()
            if not selected_item:
                messagebox.showerror('Error', 'Please select an employee to update.')
                return

            empid = empid_entry.get()
            name = name_entry.get()
            email = email_entry.get()
            gender = gender_combo.get()
            dob = dob_entry.get()
            contact = contact_entry.get()
            employment_type = employment_combo.get()
            education = education_entry.get()
            work_shift = workshift_combo.get()
            address = address_entry.get()
            doj = doj_entry.get()
            salary = salary_entry.get()
            usertype = usertype_combo.get()
            password = password_entry.get()

            if not all([empid, name, email, gender, dob, contact, employment_type, education, work_shift, address, doj, salary, usertype]):
                messagebox.showerror('Error', 'All fields except password are required for update.')
                return

            cursor.execute('UPDATE employee_data SET name=%s, email=%s, gender=%s, dob=%s, contact=%s, employment_type=%s, '
                           'education=%s, work_shift=%s, address=%s, doj=%s, salary=%s, usertype=%s, password=%s WHERE empID=%s',
                           (name, email, gender, dob, contact, employment_type, education, work_shift, address, doj, salary, usertype, password, empid))
            connection.commit()
            messagebox.showinfo('Success', 'Employee data updated successfully!')
            clear_fields()
            fetch_employees()
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error updating employee: {e}')
        finally:
            connection.close()

def delete_employee():
    global employee_tree_view
    connection, cursor = connect_database()
    if connection:
        try:
            selected_item = employee_tree_view.focus()
            if not selected_item:
                messagebox.showerror('Error', 'Please select an employee to delete.')
                return

            employee_id = employee_tree_view.item(selected_item)['values'][0]
            confirm = messagebox.askyesno('Confirm', f'Are you sure you want to delete employee with ID: {employee_id}?')
            if confirm:
                cursor.execute('DELETE FROM employee_data WHERE empID=%s', (employee_id,))
                connection.commit()
                messagebox.showinfo('Success', 'Employee data deleted successfully!')
                clear_fields()
                fetch_employees()
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error deleting employee: {e}')
        finally:
            connection.close()

def search_employee():
    global search_combo, search_entry, employee_tree_view
    connection, cursor = connect_database()
    if connection:
        try:
            search_by = search_combo.get().lower()
            search_text = search_entry.get().lower()

            if search_by == 'search by' or not search_text:
                messagebox.showerror('Error', 'Please select a search criteria and enter a value.')
                return

            if search_by == 'id':
                cursor.execute('SELECT * FROM employee_data WHERE empID=%s', (search_text,))
            elif search_by == 'name':
                cursor.execute('SELECT * FROM employee_data WHERE LOWER(name) LIKE %s', ('%' + search_text + '%',))
            elif search_by == 'email':
                cursor.execute('SELECT * FROM employee_data WHERE LOWER(email) LIKE %s', ('%' + search_text + '%',))
            else:
                messagebox.showerror('Error', 'Invalid search criteria.')
                return

            rows = cursor.fetchall()
            employee_tree_view.delete(*employee_tree_view.get_children())
            for row in rows:
                employee_tree_view.insert('', END, values=row)
        except pymysql.Error as e:
            messagebox.showerror('Error', f'Error searching employees: {e}')
        finally:
            connection.close()

def show_all_employees():
    fetch_employees()

def emp_form(window):
    global backIcon, empid_entry, name_entry, email_entry, gender_combo, dob_entry, contact_entry, \
           employment_combo, education_entry, workshift_combo, address_entry, doj_entry, salary_entry, \
           usertype_combo, password_entry, employee_tree_view, search_combo, search_entry, dob_cal, doj_cal_

    emp_frame = Frame(window, width=1070, height=567, bg='white')
    emp_frame.place(x=200, y=100)
    head_Label = Label(emp_frame, text='Manage Employee Details', font=('times new roman', 16, 'bold'), bg='#0f4d7d', fg='white')
    head_Label.place(x=0, y=0, relwidth=1)
    backIcon = PhotoImage(file='return.png')
    back_btn = Button(emp_frame, image=backIcon, bd=0, cursor='hand2', bg='white', command=lambda: emp_frame.place_forget())
    back_btn.place(x=10, y=30)

    top_frame = Frame(emp_frame, bg='white')
    top_frame.place(x=0, y=60, relwidth=1, height=235)

    search_frame = Frame(top_frame, bg='white')
    search_frame.pack()
    search_combo = ttk.Combobox(search_frame, values=('Id', 'Name', 'Email'), font=('times new roman', 12), state='readonly', width=15)
    search_combo.set('Search by')
    search_combo.grid(row=0, column=0, padx=20)

    search_entry = Entry(search_frame, font=('times new roman', 12), bg='lightyellow', width=20)
    search_entry.grid(row=0, column=1)

    search_btn = Button(search_frame, text='Search', font=('times new roman', 12), width=10, cursor='hand2', fg='white', bg='#0f4d7d', command=search_employee)
    search_btn.grid(row=0, column=2, padx=20)
    show_btn = Button(search_frame, text='Show All', font=('times new roman', 12), width=10, cursor='hand2', fg='white', bg='#0f4d7d', command=show_all_employees)
    show_btn.grid(row=0, column=3)

    horizontal_scrollbar = Scrollbar(top_frame, orient=HORIZONTAL)
    vertical_scrollbar = Scrollbar(top_frame, orient=VERTICAL)
    employee_tree_view = ttk.Treeview(top_frame, columns=('empID', 'name', 'email', 'gender', 'dob', 'contacts', 'employment_type',
                                                       'education', 'work_shift', 'address', 'doj', 'salary', 'usertype'), show='headings',
                                    yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    vertical_scrollbar.pack(side=RIGHT, fill=Y, pady=(10, 0))
    horizontal_scrollbar.config(command=employee_tree_view.xview)
    vertical_scrollbar.config(command=employee_tree_view.yview)
    employee_tree_view.pack(pady=(10, 0))

    employee_tree_view.heading('empID', text='EmpID')
    employee_tree_view.heading('name', text='Name')
    employee_tree_view.heading('email', text='Email')
    employee_tree_view.heading('gender', text='Gender')
    employee_tree_view.heading('dob', text='Date of Birth')
    employee_tree_view.heading('contacts', text='Contacts')
    employee_tree_view.heading('employment_type', text='Employment Type')
    employee_tree_view.heading('education', text='Education')
    employee_tree_view.heading('work_shift', text='Work Shift')
    employee_tree_view.heading('address', text='Address')
    employee_tree_view.heading('doj', text='Date of Joining')
    employee_tree_view.heading('salary', text='Salary')
    employee_tree_view.heading('usertype', text='User Type')

    employee_tree_view.column('empID', width=60)
    employee_tree_view.column('name', width=140)
    employee_tree_view.column('email', width=180)
    employee_tree_view.column('gender', width=80)
    employee_tree_view.column('dob', width=100)
    employee_tree_view.column('contacts', width=100)
    employee_tree_view.column('employment_type', width=120)
    employee_tree_view.column('education', width=120)
    employee_tree_view.column('work_shift', width=100)
    employee_tree_view.column('address', width=200)
    employee_tree_view.column('doj', width=100)
    employee_tree_view.column('salary', width=140)
    employee_tree_view.column('usertype', width=120)

    employee_tree_view.bind("<ButtonRelease-1>", populate_employee_details)
    fetch_employees()  # Load initial data

    detail_frame = Frame(emp_frame, bg='white')
    detail_frame.place(x=10, y=300, relwidth=1, height=250)

    # Configure
    # Configure column weights for detail_frame
    detail_frame.columnconfigure(1, weight=1)
    detail_frame.columnconfigure(3, weight=1)

    # Function to open the calendar for Date of Birth
    def open_dob_calendar():
        top = Toplevel(window)
        dob_cal = Calendar(top, selectmode='day', date_pattern='DD/MM/YYYY')
        dob_cal.pack(padx=10, pady=10)

        def set_dob():
            dob_entry.delete(0, END)
            dob_entry.insert(0, dob_cal.get_date())
            top.destroy()

        select_date_btn = Button(top, text='Select Date', command=set_dob)
        select_date_btn.pack(pady=5)

    # Function to open the calendar for Date of Joining
    def open_doj_calendar():
        top = Toplevel(window)
        doj_cal_ = Calendar(top, selectmode='day', date_pattern='DD/MM/YYYY')
        doj_cal_.pack(padx=10, pady=10)

        def set_doj():
            doj_entry.delete(0, END)
            doj_entry.insert(0, doj_cal_.get_date())
            top.destroy()

        select_date_btn = Button(top, text='Select Date', command=set_doj)
        select_date_btn.pack(pady=5)

    # Labels and Entry fields for Employee Details - Adjusted padding and sticky, and reduced widths
    empid_lbl = Label(detail_frame, text="EmpId", font=('times new roman', 12, 'bold'), bg='white')
    empid_lbl.grid(row=0, column=0, padx=(3, 1), pady=2, sticky='w')
    empid_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow', width=8)  # Reduced width
    empid_entry.grid(row=0, column=1, padx=(1, 3), pady=2, sticky='ew')

    name_lbl = Label(detail_frame, text="Name", font=('times new roman', 12, 'bold'), bg='white')
    name_lbl.grid(row=0, column=2, padx=(3, 1), pady=2, sticky='w')
    name_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow', width=10)  # Reduced width
    name_entry.grid(row=0, column=3, padx=(1, 3), pady=2, sticky='ew')

    email_lbl = Label(detail_frame, text="Email", font=('times new roman', 12, 'bold'), bg='white')
    email_lbl.grid(row=1, column=0, padx=(3, 1), pady=2, sticky='w')
    email_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow', width=12)  # Reduced width
    email_entry.grid(row=1, column=1, padx=(1, 3), pady=2, sticky='ew')

    gender_lbl = Label(detail_frame, text="Gender", font=('times new roman', 12, 'bold'), bg='white')
    gender_lbl.grid(row=1, column=2, padx=(3, 1), pady=2, sticky='w')
    gender_combo = ttk.Combobox(detail_frame, values=('Male', 'Female', 'Other'), font=('times new roman', 12),
                                state='readonly', width=8)
    gender_combo.grid(row=1, column=3, padx=(1, 3), pady=2, sticky='ew')
    gender_combo.set('Select Gender')

    dob_lbl = Label(detail_frame, text="Date of Birth", font=('times new roman', 12, 'bold'), bg='white')
    dob_lbl.grid(row=2, column=0, padx=(3, 1), pady=2, sticky='w')
    dob_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow', width=8)  # Reduced width
    dob_entry.grid(row=2, column=1, padx=(1, 3), pady=2, sticky='ew')
    dob_entry.insert(0, 'DD/MM/YYYY')
    dob_calendar_btn = Button(detail_frame, text='...', font=('times new roman', 10, 'bold'), width=2,
                              command=open_dob_calendar)
    dob_calendar_btn.grid(row=2, column=2, padx=(1, 1), pady=2, sticky='w')

    contact_lbl = Label(detail_frame, text="Contact", font=('times new roman', 12, 'bold'), bg='white')
    contact_lbl.grid(row=2, column=3, padx=(3, 1), pady=2, sticky='w')
    contact_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow', width=8)  # Reduced width
    contact_entry.grid(row=2, column=4, padx=(1, 3), pady=2, sticky='ew')  # Adjusted column

    employment_lbl = Label(detail_frame, text="Employment Type", font=('times new roman', 12, 'bold'), bg='white')
    employment_lbl.grid(row=3, column=0, padx=(3, 1), pady=2, sticky='w')
    employment_combo = ttk.Combobox(detail_frame, values=('Full-Time', 'Part-Time', 'Contract'),
                                    font=('times new roman', 12), state='readonly', width=10)  # Reduced width
    employment_combo.grid(row=3, column=1, padx=(1, 3), pady=2, sticky='ew')
    employment_combo.set('Select Type')

    education_lbl = Label(detail_frame, text="Education", font=('times new roman', 12, 'bold'), bg='white')
    education_lbl.grid(row=3, column=2, padx=(3, 1), pady=2, sticky='w')
    education_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow', width=10)  # Reduced width
    education_entry.grid(row=3, column=3, padx=(1, 3), pady=2, sticky='ew')
    education_entry.insert(0, 'Select Education')

    workshift_lbl = Label(detail_frame, text="Work Shift", font=('times new roman', 12, 'bold'), bg='white')
    workshift_lbl.grid(row=4, column=0, padx=(3, 1), pady=2, sticky='w')
    workshift_combo = ttk.Combobox(detail_frame, values=('Morning', 'Evening', 'Night'), font=('times new roman', 12),
                                   state='readonly', width=6)  # Reduced width
    workshift_combo.grid(row=4, column=1, padx=(1, 3), pady=2, sticky='ew')
    workshift_combo.set('Select Shift')

    address_lbl = Label(detail_frame, text="Address", font=('times new roman', 12, 'bold'), bg='white')
    address_lbl.grid(row=4, column=2, padx=(3, 1), pady=2, sticky='w')
    address_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow', width=15)  # Reduced width
    address_entry.grid(row=4, column=3, padx=(1, 3), pady=2, sticky='ew')

    doj_lbl = Label(detail_frame, text="Date of Joining", font=('times new roman', 12, 'bold'), bg='white')
    doj_lbl.grid(row=5, column=0, padx=(3, 1), pady=2, sticky='w')
    doj_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow', width=8)  # Reduced width
    doj_entry.grid(row=5, column=1, padx=(1, 3), pady=2, sticky='ew')
    doj_entry.insert(0, 'DD/MM/YYYY')
    doj_calendar_btn = Button(detail_frame, text='...', font=('times new roman', 10, 'bold'), width=2,
                              command=open_doj_calendar)
    doj_calendar_btn.grid(row=5, column=2, padx=(1, 1), pady=2, sticky='w')

    salary_lbl = Label(detail_frame, text="Salary", font=('times new roman', 12, 'bold'), bg='white')
    salary_lbl.grid(row=5, column=3, padx=(3, 1), pady=2, sticky='w')
    salary_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow', width=10)  # Reduced width
    salary_entry.grid(row=5, column=4, padx=(1, 3), pady=2, sticky='ew')  # Adjusted column

    usertype_lbl = Label(detail_frame, text="User Type", font=('times new roman', 12, 'bold'), bg='white')
    usertype_lbl.grid(row=6, column=0, padx=(3, 1), pady=2, sticky='w')
    usertype_combo = ttk.Combobox(detail_frame, values=('Admin', 'Employee'), font=('times new roman', 12),
                                  state='readonly', width=6)  # Reduced width
    usertype_combo.grid(row=6, column=1, padx=(1, 3), pady=2, sticky='ew')
    usertype_combo.set('Select Type')

    password_lbl = Label(detail_frame, text="Password", font=('times new roman', 12, 'bold'), bg='white')
    password_lbl.grid(row=6, column=2, padx=(3, 1), pady=2, sticky='w')
    password_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow', show='*',
                           width=10)  # Reduced width
    password_entry.grid(row=6, column=3, padx=(1, 3), pady=2, sticky='ew')

    # Buttons for Add, Update, Delete, and Clear
    button_frame = Frame(detail_frame, bg='white')
    button_frame.grid(row=7, columnspan=5, pady=8)  # Adjusted columnspan

    add_btn = Button(button_frame, text='Add', font=('times new roman', 12, 'bold'), bg='#2196f3', fg='white', width=10,
                     cursor='hand2', command=save_employee)
    add_btn.grid(row=0, column=0, padx=3)

    update_btn = Button(button_frame, text='Update', font=('times new roman', 12, 'bold'), bg='#4caf50', fg='white',
                        width=10, cursor='hand2', command=update_employee)
    update_btn.grid(row=0, column=1, padx=3)

    delete_btn = Button(button_frame, text='Delete', font=('times new roman', 12, 'bold'), bg='#f44336', fg='white',
                        width=10, cursor='hand2', command=delete_employee)
    delete_btn.grid(row=0, column=2, padx=3)

    clear_btn = Button(button_frame, text='Clear', font=('times new roman', 12, 'bold'), bg='#ff9800', fg='white',
                       width=10, cursor='hand2', command=clear_fields)
    clear_btn.grid(row=0, column=3, padx=3)