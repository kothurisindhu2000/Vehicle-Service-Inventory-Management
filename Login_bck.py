import tkinter as tk
from tkinter import messagebox
import re
from main import MainApp  # Ensure this exists

# Sample user database (in-memory)
USERS = {
    "Vineeth": {"password": "admin123", "role": "Admin"},
    "Sindhu": {"password": "mech123", "role": "Mechanic"},
    "Tharun": {"password": "cust123", "role": "Customer"}
}

class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Workshop Login")
        self.geometry("350x300")
        self.configure(bg="#ECF0F1")

        tk.Label(self, text="Login", font=("Arial", 18, "bold"), bg="#ECF0F1").pack(pady=10)

        tk.Label(self, text="Username:", bg="#ECF0F1").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password:", bg="#ECF0F1").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Login", bg="#3498DB", command=self.login).pack(pady=10)
        tk.Button(self, text="Forgot Password?", command=self.open_forgot_password, bg="#95A5A6").pack()
        tk.Button(self, text="Register", bg="#2ECC71", command=self.open_register).pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = USERS.get(username)
        if user and user["password"] == password:
            messagebox.showinfo("Login Successful", f"Welcome, {username} ({user['role']})")
            self.destroy()
            MainApp(user["role"]).mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def open_register(self):
        RegisterPage(self)

    def open_forgot_password(self):
        ForgotPasswordPage(self)


class RegisterPage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Register")
        self.geometry("400x400")
        self.configure(bg="#ECF0F1")

        fields = ["Name", "Contact", "Phone Number", "Email", "Username", "Password", "Address"]
        self.entries = {}

        for i, field in enumerate(fields):
            tk.Label(self, text=field + ":", bg="#ECF0F1").grid(row=i, column=0, sticky="e", pady=5, padx=10)
            entry = tk.Entry(self)
            entry.grid(row=i, column=1, padx=10)
            self.entries[field] = entry

        tk.Button(self, text="Register", bg="#2ECC71", command=self.register_user).grid(row=len(fields), columnspan=2, pady=10)

    def register_user(self):
        data = {field: self.entries[field].get() for field in self.entries}

        if not data["Contact"].isdigit() or len(data["Contact"]) != 10:
            messagebox.showerror("Invalid Contact", "Contact must be 10 digits.")
            return

        if not data["Email"].endswith("@gmail.com"):
            messagebox.showerror("Invalid Email", "Email must end with @gmail.com.")
            return

        if data["Username"] in USERS:
            messagebox.showerror("Registration Error", "Username already exists.")
            return

        USERS[data["Username"]] = {"password": data["Password"], "role": "Customer"}
        messagebox.showinfo("Success", "Registered successfully! You can now login.")
        self.destroy()


class ForgotPasswordPage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Forgot Password")
        self.geometry("300x200")
        self.configure(bg="#ECF0F1")

        tk.Label(self, text="Enter your username:", bg="#ECF0F1").pack(pady=10)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Button(self, text="Get Password", bg="#F1C40F", command=self.recover_password).pack(pady=10)

    def recover_password(self):
        username = self.username_entry.get()
        if username in USERS:
            password = USERS[username]["password"]
            messagebox.showinfo("Password Recovery", f"Password for {username} is: {password}")
            self.destroy()
        else:
            messagebox.showerror("Error", "Username not found.")

if __name__ == "__main__":
    LoginPage().mainloop()
