import tkinter as tk
from tkinter import ttk, messagebox

class StaffPage(tk.Frame):
    def __init__(self, parent, controller, role):
        super().__init__(parent, bg="#ECF0F1")
        self.controller = controller
        self.role = role  # Default to 'customer'
        print("User role:", self.role)
        # Sample Data (Replace with Database later)
        self.staff_list = [
            {"ID": 1, "Name": "Sindhu", "Role": "Mechanic", "Phone": "123-456-7890", "Email": "mike@example.com", "Salary": "$3000"},
            # {"ID": 2, "Name": "Sarah Lee", "Role": "Manager", "Phone": "987-654-3210", "Email": "sarah@example.com", "Salary": "$4500"}
        ]

        # Header
        tk.Label(self, text="Workshop Staff Management", font=("Arial", 16, "bold"), bg="#ECF0F1").pack(pady=10)

        # Table
        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Role", "Phone", "Email", "Salary"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(pady=10, padx=20, fill="both", expand=True)
        self.load_data()

        # Form
        form_frame = tk.Frame(self, bg="#ECF0F1")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=10)

        tk.Label(form_frame, text="Role:").grid(row=0, column=2)
        self.role_entry = tk.Entry(form_frame)
        self.role_entry.grid(row=0, column=3, padx=10)

        tk.Label(form_frame, text="Phone:").grid(row=1, column=0)
        self.phone_entry = tk.Entry(form_frame)
        self.phone_entry.grid(row=1, column=1, padx=10)

        tk.Label(form_frame, text="Email:").grid(row=1, column=2)
        self.email_entry = tk.Entry(form_frame)
        self.email_entry.grid(row=1, column=3, padx=10)

        tk.Label(form_frame, text="Salary:").grid(row=2, column=0)
        self.salary_entry = tk.Entry(form_frame)
        self.salary_entry.grid(row=2, column=1, padx=10)

        # Buttons
        button_frame = tk.Frame(self, bg="#ECF0F1")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Staff", bg="#27AE60", fg="black", command=self.add_staff).pack(side="left", padx=10)
        tk.Button(button_frame, text="Update Staff", bg="#F39C12", fg="black", command=self.update_staff).pack(side="left", padx=10)
        tk.Button(button_frame, text="Delete Staff", bg="#E74C3C", fg="black", command=self.delete_staff).pack(side="left", padx=10)
        controller.add_back_button(self)
        
    def load_data(self):
        """ Load sample data into the table """
        for staff in self.staff_list:
            self.tree.insert("", "end", values=(staff["ID"], staff["Name"], staff["Role"], staff["Phone"], staff["Email"], staff["Salary"]))

    def add_staff(self):
        """ Add a new staff member """
        new_id = len(self.staff_list) + 1
        new_staff = {
            "ID": new_id,
            "Name": self.name_entry.get(),
            "Role": self.role_entry.get(),
            "Phone": self.phone_entry.get(),
            "Email": self.email_entry.get(),
            "Salary": self.salary_entry.get()
        }
        self.staff_list.append(new_staff)
        self.tree.insert("", "end", values=(new_id, new_staff["Name"], new_staff["Role"], new_staff["Phone"], new_staff["Email"], new_staff["Salary"]))
        messagebox.showinfo("Success", "Staff member added successfully!")
        self.clear_fields()

    def update_staff(self):
        """ Update selected staff member """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a staff member to update.")
            return

        item_index = self.tree.index(selected_item)
        updated_staff = {
            "ID": self.staff_list[item_index]["ID"],
            "Name": self.name_entry.get(),
            "Role": self.role_entry.get(),
            "Phone": self.phone_entry.get(),
            "Email": self.email_entry.get(),
            "Salary": self.salary_entry.get()
        }

        self.staff_list[item_index] = updated_staff
        self.tree.item(selected_item, values=(updated_staff["ID"], updated_staff["Name"], updated_staff["Role"], updated_staff["Phone"], updated_staff["Email"], updated_staff["Salary"]))
        messagebox.showinfo("Success", "Staff member updated successfully!")
        self.clear_fields()

    def delete_staff(self):
        """ Delete selected staff member """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a staff member to delete.")
            return

        item_index = self.tree.index(selected_item)
        del self.staff_list[item_index]
        self.tree.delete(selected_item)
        messagebox.showinfo("Success", "Staff member deleted successfully!")

    def clear_fields(self):
        """ Clear all input fields """
        self.name_entry.delete(0, tk.END)
        self.role_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.salary_entry.delete(0, tk.END)
