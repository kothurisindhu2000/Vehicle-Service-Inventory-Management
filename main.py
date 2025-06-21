import tkinter as tk
from customer import CustomersPage
from vehicles import VehiclesPage
from staff import StaffPage
from parts import PartsPage
from invoices import InvoicesPage
from feedback import FeedbackPage
from supplier import SuppliersPage
from inventory import InventoryDashboard  
from work_management import WorkManagementPage
from payments import PaymentsPage
from customer_dashboard_copy import CustomerDashboard

class MainApp(tk.Tk):
    def __init__(self, role):
        super().__init__()
        self.title(f"{role} Dashboard")
        self.geometry("1000x600")
        self.role = role

        self.content_frame = tk.Frame(self, bg="#ECF0F1")
        self.content_frame.pack(expand=True, fill="both")

        # Top label for role info
        tk.Label(self.content_frame, text=f"Welcome, {self.role}!", 
                 font=("Arial", 18, "bold"), bg="#ECF0F1", fg="#2C3E50").pack(pady=20)

        self.button_frame = tk.Frame(self.content_frame, bg="#ECF0F1")
        self.button_frame.pack()

        self.build_dashboard()

    def build_dashboard(self):
        self.button_frame = tk.Frame(self.content_frame, bg="#ECF0F1")
        self.button_frame.pack()
        def add_button(label, command, row, col):
            button = tk.Button(
                self.button_frame,
                text=label,
                command=command,
                bg="#3498DB",
                fg="black",
                font=("Arial", 12, "bold"),
                width=12,
                height=6,  # Makes it square-ish
                relief="raised",
                bd=3
            )
            button.grid(row=row, column=col, padx=20, pady=20)

        buttons = []

        if self.role == "Admin":
            buttons = [
                ("Customers", lambda: self.show(CustomersPage, role=self.role)),
                ("Vehicles", lambda: self.show(VehiclesPage, role=self.role)),
                ("Staff", lambda: self.show(StaffPage, role=self.role)),
                ("Parts", lambda: self.show(PartsPage, role=self.role)),
                ("Invoices", lambda: self.show(InvoicesPage, role=self.role)),
                ("Feedback", lambda: self.show(FeedbackPage, role=self.role)),
                ("Suppliers", lambda: self.show(SuppliersPage, role=self.role)),
                ("Payments", lambda: self.show(PaymentsPage, role=self.role)),
                # ("Inventory", lambda: self.show_inventory()),  
                ("Work Management", lambda: self.show(WorkManagementPage, role=self.role)),
            ]

        elif self.role == "Mechanic":
            buttons = [
                ("Feedback", lambda: self.show(FeedbackPage, role=self.role)),
                ("Inventory", lambda: self.show_inventory()),
                ("Work Management", lambda: self.show(WorkManagementPage, role=self.role)),
                ("Payments", lambda: self.show(PaymentsPage, role=self.role)),
                ("Invoices", lambda: self.show(InvoicesPage, role=self.role)),
                ("Parts", lambda: self.show(PartsPage, role=self.role)),
                ("Suppliers", lambda: self.show(SuppliersPage, role=self.role)),
            ]

        elif self.role == "Customer":
            buttons = [
                # ("Customers", lambda: self.show(CustomersPage, role=self.role)),
                ("Give Feedback", lambda: self.show(FeedbackPage, role=self.role)),
                ("Payments", lambda: self.show(PaymentsPage, role=self.role)),
                ("My Vehicles", lambda: self.show(VehiclesPage, role=self.role)),

            ]

        # Add buttons in grid (4 per row)
        for index, (label, cmd) in enumerate(buttons):
            row = index // 4
            col = index % 4
            add_button(label, cmd, row, col)

        # Logout button placed separately at the bottom
        tk.Button(self.content_frame, text="Logout", command=self.logout,
                  bg="#E74C3C", fg="black", font=("Arial", 12, "bold"),
                  width=15, height=2).pack(pady=30)

    

    def show(self, page_class, **kwargs):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        page = page_class(self.content_frame, controller=self, **kwargs)
        page.pack(fill="both", expand=True)
            

    def show_inventory(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        InventoryDashboard(self.content_frame, self)

    def logout(self):
        self.destroy()  # Close the current dashboard window
        from Login import LoginPage  # Import inside the function to avoid circular import
        LoginPage().mainloop()  # Reopen the login screen
    
    def add_back_button(self, parent):
        back_btn = tk.Button(parent, text="Back to Dashboard", command=self.show_dashboard,
                            bg="#95A5A6", fg="black", font=("Arial", 10, "bold"),
                            width=20)
        back_btn.pack(pady=10)
    
    def show_dashboard(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.build_dashboard()
    # main.py



    def MainApp(role):
        if role == "Customer":
            return CustomerDashboard(customer_id=role)
    
        elif role == "Mechanic":
        # return MechanicDashboard()
            pass
        elif role == "Admin":
        # return AdminDashboard()
            pass


if __name__ == "__main__":
    from Login import LoginPage
    LoginPage().mainloop()
