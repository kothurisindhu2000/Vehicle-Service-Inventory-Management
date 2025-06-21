import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from RegisterPage import RegisterPage
from main import MainApp
from Admindashboard import AdminDashboard
from customer_dashboard import CustomerDashboard
from Mechanic_dashboard import MechanicDashboard
import os

ADMIN_CREDENTIALS = {"admin": "admin123"}

def get_db_connection():
    return mysql.connector.connect(
        host='141.209.241.91',
        port=3306,
        user='sp2025bis698g6',
        password='warm',
        database='sp2025bis698g6s'
    )

def get_user_role(username, password):
    if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
        return "Admin", None

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT Mechanic_ID FROM MECHANIC WHERE Mechanic_User_Name = %s AND Mechanic_Password = %s", (username, password))
    mech = cursor.fetchone()
    if mech:
        return "Mechanic", mech["Mechanic_ID"]

    cursor.execute("SELECT Customer_ID FROM CUSTOMER WHERE Email = %s AND Password = %s", (username, password))
    cust = cursor.fetchone()
    if cust:
        return "Customer", cust["Customer_ID"]

    conn.close()
    return None, None

class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("1000x800")
        self.configure(bg="#ECF0F1")

        # Logo Section
        try:
            current_directory = os.path.dirname(os.path.abspath(__file__))
            logo_path = os.path.join(current_directory, "logo.png")
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((350, 350), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_image)
            tk.Label(self, image=self.logo, bg="#ECF0F1").pack(pady=(30, 10))
        except Exception as e:
            print(f"Logo load failed: {e}")

        # Login Form
        tk.Label(self, text="Login", font=("Arial", 22, "bold"), bg="#ECF0F1").pack(pady=10)
        tk.Label(self, text="Email or Username", bg="#ECF0F1", font=("Arial", 12)).pack()
        self.username_entry = tk.Entry(self, font=("Arial", 12), width=30)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Password", bg="#ECF0F1", font=("Arial", 12)).pack()
        self.password_entry = tk.Entry(self, show="*", font=("Arial", 12), width=30)
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Login", bg="#3498DB", fg="white", font=("Arial", 12, "bold"), width=15,
                  command=self.login).pack(pady=15)
        tk.Button(self, text="Register", bg="#2ECC71", fg="white", font=("Arial", 11), command=self.open_register_page).pack()

    def open_register_page(self):
        self.destroy()
        RegisterPage()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role, user_id = get_user_role(username, password)

        if role == "Customer":
            messagebox.showinfo("Login Successful", f"Welcome, {username} ({role})")
            self.destroy() 
            CustomerDashboard(customer_id=user_id).mainloop()

        elif role == "Mechanic":
            messagebox.showinfo("Login Successful", f"Welcome, {username} ({role})")
            self.destroy()
            root = tk.Tk()
            root.title("Mechanic Dashboard")
            MechanicDashboard(root, controller=SimpleController(root), role=role, mechanic_id=user_id)
            root.mainloop()

        elif role == "Admin":
            messagebox.showinfo("Login Successful", f"Welcome, {username} (Admin)")
            self.destroy()
            root = tk.Tk()
            AdminDashboard(root)
            root.mainloop()

        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

class SimpleController:
    def __init__(self, parent):
        self.parent = parent

    def add_back_button(self, dashboard):
        tk.Button(self.parent, text="Back", command=self.go_back).pack(pady=5)

    def go_back(self):
        self.parent.destroy()
        LoginPage().mainloop()

if __name__ == "__main__":
    LoginPage().mainloop()
