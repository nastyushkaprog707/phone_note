import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import sys

class Employee(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_employee()
        self.db = db
        self.view_records()

    def init_employee(self):
        toolbar = tk.Frame(bg="#d7d8e0", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.add_png = tk.PhotoImage(file="./images/add.png")
        button_add_employee = tk.Button(toolbar, bg="#d7d8e0", bd=0, image=self.add_png, command=self.add_employee)
        button_add_employee.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(
            self, columns=("ID", "name", "telephone", "email", "salary"), height=45, show="headings"
        )

        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("name", width=300, anchor=tk.CENTER)
        self.tree.column("telephone", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)
        self.tree.column("salary", width=200, anchor=tk.CENTER)

        self.tree.heading("ID", text="ID")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("telephone", text="Телефон")
        self.tree.heading("email", text="E-mail")
        self.tree.heading("salary", text="Зарплата")

        self.tree.pack(side=tk.LEFT)

        self.update_png = tk.PhotoImage(file="./images/update.png")
        button_update_employee = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.update_png,
            command=self.update_employee,
        )
        button_update_employee.pack(side=tk.LEFT)

        self.delete_png = tk.PhotoImage(file="./images/delete.png")
        button_delete_employee = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.delete_png,
            command=self.delete_employee,
        )
        button_delete_employee.pack(side=tk.LEFT)

        self.search_png = tk.PhotoImage(file="./images/search.png")
        button_search = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.search_png,
            command=self.search_employee,
        )
        button_search.pack(side=tk.LEFT)

        self.refresh_png = tk.PhotoImage(file="./images/refresh.png")
        button_refresh = tk.Button(
            toolbar,
            bg="#d7d8e0",
            bd=0,
            image=self.refresh_png,
            command=self.refresh_employee,
        )
        button_refresh.pack(side=tk.LEFT)

    def add_employee(self):
        AddEmployee()

    def records(self, name, telephone, email, salary):
        self.db.insert_data(name, telephone, email, salary)
        self.view_records()

    def view_records(self):
        self.db.cursor.execute("SELECT * FROM db")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()]

    def update_employee(self):
        UpdateEmployee()

    def update_records(self, name, telephone, email, salary):
        self.db.cursor.execute(
            """UPDATE db SET name=?, telephone=?, email=?, salary=? WHERE id=?""",
            (name, telephone, email, salary, self.tree.set(self.tree.selection()[0], "#1")),
        )
        self.db.conn.commit()
        self.view_records()

    def delete_employee(self):
        for selection_items in self.tree.selection():
            self.db.cursor.execute(
                "DELETE FROM db WHERE id=?", (self.tree.set(selection_items, "#1"))
            )
        self.db.conn.commit()
        self.view_records()

    def search_employee(self):
        SearchEmployee()

    def refresh_employee(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)

    def search_records(self, name):
        name = "%" + name + "%"
        self.db.cursor.execute("SELECT * FROM db WHERE name LIKE ?", (name,))

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row) for row in self.db.cursor.fetchall()]


class AddEmployee(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_add_employee()
        self.view = app

    def init_add_employee(self):
        self.title("Создание сотрудника")
        self.geometry("400x220")
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text="ФИО сотрудника:")
        label_name.place(x=50, y=50)
        label_telephone = tk.Label(self, text="Номер телефона:")
        label_telephone.place(x=50, y=80)
        label_email = tk.Label(self, text="Почтовый ящик:")
        label_email.place(x=50, y=110)
        label_salary = tk.Label(self, text="Средняя зарплата:")
        label_salary.place(x=50, y=140)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_telephone = ttk.Entry(self)
        self.entry_telephone.place(x=200, y=80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140)

        self.button_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        self.button_cancel.place(x=220, y=170)

        self.button_ok = ttk.Button(self, text="Добавить")
        self.button_ok.place(x=300, y=170)

        self.button_ok.bind(
            "<Button-1>",
            lambda event: self.view.records(
                self.entry_name.get(), self.entry_telephone.get(), self.entry_email.get(), self.entry_salary.get(),
            ),
        )


class UpdateEmployee(AddEmployee):
    def __init__(self):
        super().__init__()
        self.init_update_employee()
        self.view = app
        self.db = db
        self.default_data()

    def init_update_employee(self):
        self.title("Редактирование сотрудника")
        button_edit = ttk.Button(self, text="Редактировать")
        button_edit.place(x=205, y=170)
        button_edit.bind(
            "<Button-1>",
            lambda event: self.view.update_records(
                self.entry_name.get(), self.entry_telephone.get(), self.entry_email.get(), self.entry_salary.get(),
            ),
        )
        button_edit.bind("<Button-1>", lambda event: self.destroy(), add="+")
        self.button_ok.destroy()

    def default_data(self):
        self.db.cursor.execute(
            "SELECT * FROM db WHERE id=?",
            self.view.tree.set(self.view.tree.selection()[0], "#1"),
        )
        row = self.db.cursor.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_telephone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])


class SearchEmployee(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search_employee()
        self.view = app

    def init_search_employee(self):
        self.title("Поиск сотрудника")
        self.geometry("300x100")
        self.resizable(False, False)

        label_search = tk.Label(self, text="Имя:")
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=100, y=20, width=150)

        button_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        button_cancel.place(x=185, y=50)

        search_button = ttk.Button(self, text="Найти")
        search_button.place(x=105, y=50)
        search_button.bind(
            "<Button-1>",
            lambda event: self.view.search_records(self.entry_search.get()),
        )
        search_button.bind("<Button-1>", lambda event: self.destroy(), add="+")


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("db.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS db (
                id INTEGER PRIMARY KEY,
                name TEXT,
                telephone TEXT,
                email TEXT,
                salary INTEGER
            )"""
        )
        self.conn.commit()

    def insert_data(self, name, telephone, email, salary):
        self.cursor.execute(
            """INSERT INTO db(name, telephone, email, salary) VALUES(?, ?, ?, ?)""", (name, telephone, email, salary)
        )
        self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = Database()
    app = Employee(root)
    app.pack()
    root.title("Список сотрудников компании")
    root.geometry("800x600")
    root.resizable(False, False)
    root.mainloop()