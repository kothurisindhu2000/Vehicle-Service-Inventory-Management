import tkinter as tk
from tkinter import ttk, messagebox

class PartsPage(tk.Frame):
    def __init__(self, parent, controller, role):
        super().__init__(parent, bg="#ECF0F1")
        self.controller = controller
        self.role = role  # Default to 'customer'
        print("User role:", self.role)
        # Sample Data (Replace with Database later)
        self.parts_list = [
            {"ID": 1, "Name": "Turbocharger", "Description": "Increases engine power", "Stock": 10, "Price": "$500", "Supplier": "SpeedParts Inc."},
            {"ID": 2, "Name": "Alloy Wheels", "Description": "Lightweight and stylish wheels", "Stock": 15, "Price": "$250", "Supplier": "WheelTech Ltd."}
        ]

        # Header
        tk.Label(self, text="Parts Inventory Management", font=("Arial", 16, "bold"), bg="#ECF0F1").pack(pady=10)

        # Table
        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Description", "Stock", "Price", "Supplier"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(pady=10, padx=20, fill="both", expand=True)
        self.load_data()

        # Form
        form_frame = tk.Frame(self, bg="#ECF0F1")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Part Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=10)

        tk.Label(form_frame, text="Description:").grid(row=0, column=2)
        self.description_entry = tk.Entry(form_frame)
        self.description_entry.grid(row=0, column=3, padx=10)

        tk.Label(form_frame, text="Stock Quantity:").grid(row=1, column=0)
        self.stock_entry = tk.Entry(form_frame)
        self.stock_entry.grid(row=1, column=1, padx=10)

        tk.Label(form_frame, text="Price:").grid(row=1, column=2)
        self.price_entry = tk.Entry(form_frame)
        self.price_entry.grid(row=1, column=3, padx=10)

        tk.Label(form_frame, text="Supplier:").grid(row=2, column=0)
        self.supplier_entry = tk.Entry(form_frame)
        self.supplier_entry.grid(row=2, column=1, padx=10)

        # Buttons
        button_frame = tk.Frame(self, bg="#ECF0F1")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Part", bg="#27AE60", fg="black", command=self.add_part).pack(side="left", padx=10)
        tk.Button(button_frame, text="Update Part", bg="#F39C12", fg="black", command=self.update_part).pack(side="left", padx=10)
        tk.Button(button_frame, text="Delete Part", bg="#E74C3C", fg="black", command=self.delete_part).pack(side="left", padx=10)
        controller.add_back_button(self)
        
    def load_data(self):
        """ Load sample data into the table """
        for part in self.parts_list:
            self.tree.insert("", "end", values=(part["ID"], part["Name"], part["Description"], part["Stock"], part["Price"], part["Supplier"]))

    def add_part(self):
        """ Add a new part to the inventory """
        new_id = len(self.parts_list) + 1
        new_part = {
            "ID": new_id,
            "Name": self.name_entry.get(),
            "Description": self.description_entry.get(),
            "Stock": self.stock_entry.get(),
            "Price": self.price_entry.get(),
            "Supplier": self.supplier_entry.get()
        }
        self.parts_list.append(new_part)
        self.tree.insert("", "end", values=(new_id, new_part["Name"], new_part["Description"], new_part["Stock"], new_part["Price"], new_part["Supplier"]))
        messagebox.showinfo("Success", "Part added successfully!")
        self.clear_fields()

    def update_part(self):
        """ Update selected part details """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a part to update.")
            return

        item_index = self.tree.index(selected_item)
        updated_part = {
            "ID": self.parts_list[item_index]["ID"],
            "Name": self.name_entry.get(),
            "Description": self.description_entry.get(),
            "Stock": self.stock_entry.get(),
            "Price": self.price_entry.get(),
            "Supplier": self.supplier_entry.get()
        }

        self.parts_list[item_index] = updated_part
        self.tree.item(selected_item, values=(updated_part["ID"], updated_part["Name"], updated_part["Description"], updated_part["Stock"], updated_part["Price"], updated_part["Supplier"]))
        messagebox.showinfo("Success", "Part updated successfully!")
        self.clear_fields()

    def delete_part(self):
        """ Delete selected part from inventory """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a part to delete.")
            return

        item_index = self.tree.index(selected_item)
        del self.parts_list[item_index]
        self.tree.delete(selected_item)
        messagebox.showinfo("Success", "Part deleted successfully!")

    def clear_fields(self):
        """ Clear all input fields """
        self.name_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.stock_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.supplier_entry.delete(0, tk.END)
