import tkinter as tk
from tkinter import ttk, messagebox

class InvoicesPage(tk.Frame):
    def __init__(self, parent, controller, role):
        super().__init__(parent, bg="#ECF0F1")
        self.controller = controller
        self.role = role  # 'admin' or 'customer'
        print("User role:", self.role)

        # Sample Data (Replace with Database later)
        self.invoice_list = [
            {"ID": 1, "Order ID": 101, "Customer": "Tharun", "Total": "$1200", "Status": "Paid", "Method": "Credit Card", "Date": "2025-03-20"},
        ]

        # Header
        tk.Label(self, text="Invoices Management", font=("Arial", 16, "bold"), bg="#ECF0F1").pack(pady=10)

        # Table
        self.tree = ttk.Treeview(self, columns=("ID", "Order ID", "Customer", "Total", "Status", "Method", "Date"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(pady=10, padx=20, fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)
        self.load_data()

        # Form
        form_frame = tk.Frame(self, bg="#ECF0F1")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Order ID:").grid(row=0, column=0)
        self.order_id_entry = tk.Entry(form_frame)
        self.order_id_entry.grid(row=0, column=1, padx=10)

        tk.Label(form_frame, text="Customer:").grid(row=0, column=2)
        self.customer_entry = tk.Entry(form_frame)
        self.customer_entry.grid(row=0, column=3, padx=10)

        tk.Label(form_frame, text="Total Amount:").grid(row=1, column=0)
        self.total_entry = tk.Entry(form_frame)
        self.total_entry.grid(row=1, column=1, padx=10)

        tk.Label(form_frame, text="Status:").grid(row=1, column=2)
        self.status_entry = tk.Entry(form_frame)
        self.status_entry.grid(row=1, column=3, padx=10)

        tk.Label(form_frame, text="Payment Method:").grid(row=2, column=0)
        self.method_entry = tk.Entry(form_frame)
        self.method_entry.grid(row=2, column=1, padx=10)

        tk.Label(form_frame, text="Invoice Date:").grid(row=2, column=2)
        self.date_entry = tk.Entry(form_frame)
        self.date_entry.grid(row=2, column=3, padx=10)

        # Buttons
        button_frame = tk.Frame(self, bg="#ECF0F1")
        button_frame.pack(pady=10)


        if self.role.lower() == "admin":
            tk.Button(button_frame, text="Update Invoice", bg="#F39C12", fg="black", command=self.update_invoice).pack(side="left", padx=10)
            tk.Button(button_frame, text="Delete Invoice", bg="#E74C3C", fg="black", command=self.delete_invoice).pack(side="left", padx=10)
            controller.add_back_button(self)
    def load_data(self):
        """ Load sample data into the table """
        for invoice in self.invoice_list:
            self.tree.insert("", "end", values=(invoice["ID"], invoice["Order ID"], invoice["Customer"], invoice["Total"], invoice["Status"], invoice["Method"], invoice["Date"]))

    def on_row_select(self, event):
        """ Populate fields when a row is selected """
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.order_id_entry.delete(0, tk.END)
            self.order_id_entry.insert(0, values[1])
            self.customer_entry.delete(0, tk.END)
            self.customer_entry.insert(0, values[2])
            self.total_entry.delete(0, tk.END)
            self.total_entry.insert(0, values[3])
            self.status_entry.delete(0, tk.END)
            self.status_entry.insert(0, values[4])
            self.method_entry.delete(0, tk.END)
            self.method_entry.insert(0, values[5])
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, values[6])

    def add_invoice(self):
        """ Add a new invoice """
        new_id = len(self.invoice_list) + 1
        new_invoice = {
            "ID": new_id,
            "Order ID": self.order_id_entry.get(),
            "Customer": self.customer_entry.get(),
            "Total": self.total_entry.get(),
            "Status": self.status_entry.get(),
            "Method": self.method_entry.get(),
            "Date": self.date_entry.get()
        }
        self.invoice_list.append(new_invoice)
        self.tree.insert("", "end", values=(new_id, new_invoice["Order ID"], new_invoice["Customer"], new_invoice["Total"], new_invoice["Status"], new_invoice["Method"], new_invoice["Date"]))
        messagebox.showinfo("Success", "Invoice added successfully!")
        self.clear_fields()

    def update_invoice(self):
        """ Update selected invoice (Admins Only) """
        if self.role.lower() != "admin":
            messagebox.showerror("Permission Denied", "Only admins can update invoices.")
            return

        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an invoice to update.")
            return

        item_index = self.tree.index(selected_item)
        updated_invoice = {
            "ID": self.invoice_list[item_index]["ID"],
            "Order ID": self.order_id_entry.get(),
            "Customer": self.customer_entry.get(),
            "Total": self.total_entry.get(),
            "Status": self.status_entry.get(),
            "Method": self.method_entry.get(),
            "Date": self.date_entry.get()
        }

        self.invoice_list[item_index] = updated_invoice
        self.tree.item(selected_item, values=(
            updated_invoice["ID"], updated_invoice["Order ID"], updated_invoice["Customer"],
            updated_invoice["Total"], updated_invoice["Status"], updated_invoice["Method"], updated_invoice["Date"]))
        messagebox.showinfo("Success", "Invoice updated successfully!")
        self.clear_fields()

    def delete_invoice(self):
        """ Delete selected invoice (Admins Only) """
        if self.role.lower() != "admin":
            messagebox.showerror("Permission Denied", "Only admins can delete invoices.")
            return

        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an invoice to delete.")
            return

        item_index = self.tree.index(selected_item)
        del self.invoice_list[item_index]
        self.tree.delete(selected_item)
        messagebox.showinfo("Success", "Invoice deleted successfully!")

    def clear_fields(self):
        """ Clear all input fields """
        self.order_id_entry.delete(0, tk.END)
        self.customer_entry.delete(0, tk.END)
        self.total_entry.delete(0, tk.END)
        self.status_entry.delete(0, tk.END)
        self.method_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
