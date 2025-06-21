# RegisterPage.py

import tkinter as tk
from tkinter import messagebox
import mysql.connector
import re

def get_db_connection():
    return mysql.connector.connect(
       host = '141.209.241.91',
    port = 3306,
    user = 'sp2025bis698g6',
    password = 'warm',
    database = 'sp2025bis698g6s'
    )

class RegisterPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Register")
        self.geometry("450x400")
        self.configure(bg="#ECF0F1")

        self.fields = {
            "Name": None,
            "Email": None,
            "Phone Number": None,
            "Address": None,
            "Password": None
        }

        row = 0
        for label in self.fields:
            tk.Label(self, text=f"{label}:", bg="#ECF0F1").grid(row=row, column=0, sticky="e", padx=10, pady=5)
            entry = tk.Entry(self, show="*" if label == "Password" else "")
            entry.grid(row=row, column=1, padx=10)
            self.fields[label] = entry
            row += 1

        tk.Button(self, text="Register", bg="#2ECC71", command=self.register_user).grid(columnspan=2, row=row, pady=10)
        tk.Button(self, text="Back to Login", command=self.back_to_login, bg="#95A5A6").grid(columnspan=2, row=row+1, pady=5)

        self.mainloop()

    def register_user(self):
        data = {label: entry.get().strip() for label, entry in self.fields.items()}

        if not all(data.values()):
            messagebox.showerror("Missing Fields", "All fields must be filled out.")
            return

        if not re.match(r"^[6-9]\d{9}$", data["Phone Number"]):
            messagebox.showerror("Invalid Phone", "Phone must be 10 digits starting with 6-9.")
            return

        if not re.match(r"[^@]+@gmail\.com$", data["Email"]):
            messagebox.showerror("Invalid Email", "Email must be a valid Gmail address.")
            return

        if len(data["Password"]) < 8:
            messagebox.showerror("Weak Password", "Password must be at least 8 characters.")
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT 1 FROM CUSTOMER WHERE Email = %s", (data["Email"],))
            if cursor.fetchone():
                messagebox.showerror("Registration Error", "Email already registered.")
                return

            cursor.execute("SELECT COALESCE(MAX(Customer_ID), 0) + 1 FROM CUSTOMER")
            customer_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO CUSTOMER (Customer_ID, Name, Email, Phone_number, Address, Password)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                customer_id,
                data["Name"],
                data["Email"],
                data["Phone Number"],
                data["Address"],
                data["Password"]
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Registration successful!")
            self.back_to_login()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def back_to_login(self):
        self.destroy()
        from Login import LoginPage  # <- local import avoids circular dependency
        LoginPage().mainloop()
