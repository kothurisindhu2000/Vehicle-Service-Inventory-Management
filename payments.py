import tkinter as tk
from tkinter import messagebox, ttk

class PaymentsPage(tk.Frame):
    def __init__(self, parent, controller, role):
        super().__init__(parent)
        self.controller = controller
        self.role = role  # Default to 'customer'
        print("User role:", self.role)

        role = controller.role

        tk.Label(self, text="Payments", font=("Arial", 16, "bold")).pack(pady=10)

        if role == "Customer":
            self.make_payment_section()

        self.view_summary_section()

        controller.add_back_button(self)

    def make_payment_section(self):
        frame = tk.LabelFrame(self, text="Make Payment", padx=10, pady=10)
        frame.pack(pady=10, padx=10, fill="x")

        tk.Label(frame, text="Order ID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.order_id_entry = tk.Entry(frame)
        self.order_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.amount_entry = tk.Entry(frame)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Payment Mode:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.mode_cb = ttk.Combobox(frame, values=["Cash", "Credit Card", "Debit Card", "Net Banking"])
        self.mode_cb.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(frame, text="Pay Now", command=self.make_payment, bg="green", fg="black").grid(row=3, columnspan=2, pady=10)
        

    def view_summary_section(self):
        frame = tk.LabelFrame(self, text="Payment Summary", padx=10, pady=10)
        frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.tree = ttk.Treeview(frame, columns=("Order ID", "Amount", "Mode", "Status"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

        self.load_payment_summary()

    def make_payment(self):
        order_id = self.order_id_entry.get()
        amount = self.amount_entry.get()
        mode = self.mode_cb.get()

        if not order_id or not amount or not mode:
            messagebox.showerror("Missing Data", "Please fill all fields.")
            return

        # Here we simulate a payment
        messagebox.showinfo("Success", f"Payment of ₹{amount} for Order ID {order_id} was successful!")

        # Add to summary (in real app, save to DB)
        self.tree.insert("", "end", values=(order_id, amount, mode, "Paid"))
        self.clear_form()

    def clear_form(self):
        self.order_id_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.mode_cb.set("")

    def load_payment_summary(self):
        # Simulated records
        data = [
            ("Order123", "1200", "Cash", "Paid"),
            ("Order456", "800", "Credit Card", "Paid"),
        ]
        for row in data:
            self.tree.insert("", "end", values=row)
