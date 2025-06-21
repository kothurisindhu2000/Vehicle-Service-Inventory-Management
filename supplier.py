import tkinter as tk
from tkinter import ttk, messagebox

class SuppliersPage(tk.Frame):
    def __init__(self, parent, controller, role):
        super().__init__(parent, bg="#ECF0F1")
        self.controller = controller   
        self.role = role
        print("User role:", self.role) 

        self.suppliers = [
            {"ID": 1, "Name": "SpeedParts Inc.", "Phone": "123-456-7890", "Email": "contact@speedparts.com", "Address": "New York"},
            {"ID": 2, "Name": "WheelTech Ltd.", "Phone": "987-654-3210", "Email": "sales@wheeltech.com", "Address": "California"}
        ]

        tk.Label(self, text="Suppliers Management", font=("Arial", 16, "bold"), bg="#ECF0F1").pack(pady=10)

        # Table
        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Phone", "Email", "Address"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(pady=10, padx=20, fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)  # Binding the select event
        self.load_data()

        # Form
        form_frame = tk.Frame(self, bg="#ECF0F1")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=10)

        tk.Label(form_frame, text="Phone:").grid(row=0, column=2)
        self.phone_entry = tk.Entry(form_frame)
        self.phone_entry.grid(row=0, column=3, padx=10)

        tk.Label(form_frame, text="Email:").grid(row=1, column=0)
        self.email_entry = tk.Entry(form_frame)
        self.email_entry.grid(row=1, column=1, padx=10)

        tk.Label(form_frame, text="Address:").grid(row=1, column=2)
        self.address_entry = tk.Entry(form_frame)
        self.address_entry.grid(row=1, column=3, padx=10)

        # Buttons
        button_frame = tk.Frame(self, bg="#ECF0F1")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Supplier", bg="#27AE60", fg="black", command=self.add_supplier).pack(side="left", padx=10)
        tk.Button(button_frame, text="Update Supplier", bg="#F39C12", fg="black", command=self.update_supplier).pack(side="left", padx=10)
        tk.Button(button_frame, text="Delete Supplier", bg="#E74C3C", fg="black", command=self.delete_supplier).pack(side="left", padx=10)
        
        controller.add_back_button(self)

    def load_data(self):
        for sup in self.suppliers:
            self.tree.insert("", "end", values=(sup["ID"], sup["Name"], sup["Phone"], sup["Email"], sup["Address"]))

    def add_supplier(self):
        new_id = len(self.suppliers) + 1
        new_sup = {
            "ID": new_id,
            "Name": self.name_entry.get(),
            "Phone": self.phone_entry.get(),
            "Email": self.email_entry.get(),
            "Address": self.address_entry.get()
        }
        self.suppliers.append(new_sup)
        self.tree.insert("", "end", values=(new_id, new_sup["Name"], new_sup["Phone"], new_sup["Email"], new_sup["Address"]))
        messagebox.showinfo("Success", "Supplier added successfully!")
        self.clear_fields()

    def update_supplier(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a supplier to update.")
            return

        idx = self.tree.index(selected)
        updated = {
            "ID": self.suppliers[idx]["ID"],
            "Name": self.name_entry.get(),
            "Phone": self.phone_entry.get(),
            "Email": self.email_entry.get(),
            "Address": self.address_entry.get()
        }
        self.suppliers[idx] = updated
        self.tree.item(selected, values=(updated["ID"], updated["Name"], updated["Phone"], updated["Email"], updated["Address"]))
        messagebox.showinfo("Success", "Supplier updated successfully!")
        self.clear_fields()

    def delete_supplier(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a supplier to delete.")
            return

        idx = self.tree.index(selected)
        del self.suppliers[idx]
        self.tree.delete(selected)
        messagebox.showinfo("Success", "Supplier deleted successfully!")
        self.clear_fields()

    def on_row_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected)
        values = item["values"]
        # Populate entry fields
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[1])
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, values[2])
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, values[3])
        self.address_entry.delete(0, tk.END)
        self.address_entry.insert(0, values[4])

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
