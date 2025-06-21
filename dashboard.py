import tkinter as tk
from customer import CustomersPage
from orders import OrdersPage
from inventory import InventoryDashboard
from invoices import InvoicesPage
from feedback import FeedbackPage

class MainDashboard:
    def __init__(self, parent, role, controller):
        self.parent = parent
        self.controller = controller
        self.role = role
        
        tk.Label(parent, text=f"{role.capitalize()} Dashboard", font=("Arial", 18, "bold")).pack(pady=10)

        options = []
        
        if role == "Admin":
            options = [
                ("Manage Customers", lambda: controller.load_module(CustomersPage)),
                ("Manage Orders", lambda: controller.load_module(OrdersPage)),
                ("Manage Inventory", lambda: controller.load_module(InventoryDashboard)),
                ("Manage Invoices", lambda: controller.load_module(InvoicesPage)),
                ("View Feedback", lambda: controller.load_module(FeedbackPage)),
            ]
        elif role == "Mechanic":
            options = [
                ("View Assigned Work", lambda: controller.load_module(OrdersPage)),
                ("Update Work Status", lambda: controller.load_module(OrdersPage)),
            ]
        elif role == "Customer":
            options = [
                ("View My Orders", lambda: controller.load_module(OrdersPage)),
                ("Give Feedback", lambda: controller.load_module(FeedbackPage)),
            ]

        for text, command in options:
            tk.Button(parent, text=text, command=command, font=("Arial", 12), width=30, height=2).pack(pady=5)
