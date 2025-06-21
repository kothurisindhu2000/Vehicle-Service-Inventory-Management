import tkinter as tk
from tkinter import ttk, messagebox
from db import fetch_all, execute_query

class OrdersPage(tk.Frame):
    def __init__(self, parent, controller, role):
        super().__init__(parent, bg="#ECF0F1")
        self.controller = controller
        self.role = role
        print("User role:", self.role)

        tk.Label(self, text="Modification Orders Management", font=("Arial", 16, "bold"), bg="#ECF0F1").pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("ID", "Customer ID", "Service Notes", "Cost", "Date", "Status"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(pady=10, padx=20, fill="both", expand=True)
        self.load_data()

        form_frame = tk.Frame(self, bg="#ECF0F1")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Customer ID:").grid(row=0, column=0)
        self.customer_entry = tk.Entry(form_frame)
        self.customer_entry.grid(row=0, column=1, padx=10)

        tk.Label(form_frame, text="Service Notes:").grid(row=0, column=2)
        self.notes_entry = tk.Entry(form_frame)
        self.notes_entry.grid(row=0, column=3, padx=10)

        tk.Label(form_frame, text="Total Cost:").grid(row=1, column=0)
        self.cost_entry = tk.Entry(form_frame)
        self.cost_entry.grid(row=1, column=1, padx=10)

        tk.Label(form_frame, text="Service Date (YYYY-MM-DD):").grid(row=1, column=2)
        self.date_entry = tk.Entry(form_frame)
        self.date_entry.grid(row=1, column=3, padx=10)

        tk.Label(form_frame, text="Status:").grid(row=2, column=0)
        self.status_entry = tk.Entry(form_frame)
        self.status_entry.grid(row=2, column=1, padx=10)

        tk.Label(form_frame, text="Mechanic ID:").grid(row=2, column=2)
        self.mechanic_entry = tk.Entry(form_frame)
        self.mechanic_entry.grid(row=2, column=3, padx=10)

        tk.Label(form_frame, text="Delivery Date (YYYY-MM-DD):").grid(row=3, column=0)
        self.delivery_entry = tk.Entry(form_frame)
        self.delivery_entry.grid(row=3, column=1, padx=10)

        button_frame = tk.Frame(self, bg="#ECF0F1")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Order", bg="#27AE60", fg="black", command=self.add_order).pack(side="left", padx=10)
        tk.Button(button_frame, text="Update Order", bg="#F39C12", fg="black", command=self.update_order).pack(side="left", padx=10)
        tk.Button(button_frame, text="Delete Order", bg="#E74C3C", fg="black", command=self.delete_order).pack(side="left", padx=10)

        controller.add_back_button(self)

    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        query = "SELECT Service_Request_ID AS ID, Customer_ID, Service_Notes, Total_Amount, Service_Date, Service_Status FROM SERVICE_REQUEST"
        results = fetch_all(query)
        for row in results:
            self.tree.insert("", "end", values=(row['ID'], row['Customer_ID'], row['Service_Notes'], row['Total_Amount'], row['Service_Date'], row['Service_Status']))

    def add_order(self):
        query = """
        INSERT INTO SERVICE_REQUEST (Customer_ID, Total_Amount, Service_Date, Service_Notes, Mechanic_ID, Service_Status, Delivery_Date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        data = (
            self.customer_entry.get(),
            self.cost_entry.get(),
            self.date_entry.get(),
            self.notes_entry.get(),
            self.mechanic_entry.get(),
            self.status_entry.get(),
            self.delivery_entry.get()
        )
        execute_query(query, data)
        messagebox.showinfo("Success", "Order added successfully!")
        self.load_data()
        self.clear_fields()

    def update_order(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an order to update.")
            return
        order_id = self.tree.item(selected[0], "values")[0]

        query = """
        UPDATE SERVICE_REQUEST
        SET Customer_ID=%s, Total_Amount=%s, Service_Date=%s, Service_Notes=%s, Mechanic_ID=%s, Service_Status=%s, Delivery_Date=%s
        WHERE Service_Request_ID=%s
        """
        data = (
            self.customer_entry.get(),
            self.cost_entry.get(),
            self.date_entry.get(),
            self.notes_entry.get(),
            self.mechanic_entry.get(),
            self.status_entry.get(),
            self.delivery_entry.get(),
            order_id
        )
        execute_query(query, data)
        messagebox.showinfo("Success", "Order updated successfully!")
        self.load_data()
        self.clear_fields()

    def delete_order(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an order to delete.")
            return
        order_id = self.tree.item(selected[0], "values")[0]
        query = "DELETE FROM SERVICE_REQUEST WHERE Service_Request_ID=%s"
        execute_query(query, (order_id,))
        messagebox.showinfo("Success", "Order deleted successfully!")
        self.load_data()

    def clear_fields(self):
        self.customer_entry.delete(0, tk.END)
        self.notes_entry.delete(0, tk.END)
        self.cost_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.status_entry.delete(0, tk.END)
        self.mechanic_entry.delete(0, tk.END)
        self.delivery_entry.delete(0, tk.END)
