import tkinter as tk

class InventoryDashboard:
    def __init__(self, parent, controller, role):
        self.parent = parent
        self.controller = controller
        self.role = role  # Default to 'customer'
        print("User role:", self.role)
        
        tk.Label(parent, text="Parts Inventory", font=("Arial", 16, "bold")).pack(pady=10)
        

        self.parts = [
            {"part_id": 1, "name": "Turbocharger", "stock": 10, "supplier": "ABC Motors"},
            {"part_id": 2, "name": "Alloy Wheels", "stock": 5, "supplier": "XYZ Auto"}
        ]

        self.list_parts()

    def list_parts(self):
        for part in self.parts:
            tk.Label(self.parent, text=f"{part['part_id']}. {part['name']} - {part['stock']} in stock ({part['supplier']})", font=("Arial", 12)).pack()
