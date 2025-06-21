import tkinter as tk
from tkinter import ttk, messagebox

class VehiclesPage(tk.Frame):
    def __init__(self, parent, controller, role):
        super().__init__(parent, bg="#ECF0F1")
        self.controller = controller
        self.role = role  # "customer" or "admin"
        print("User role:", self.role)

        # Sample Data (Replace with Database later)
        self.vehicles = [
            {"ID": 1, "Customer": "Tharun", "Make": "Toyota", "Model": "Corolla", "Year": "2020", "VIN": "123ABC", "Plate": "XYZ-123"},
        ]

        # Header
        tk.Label(self, text="Vehicle Management", font=("Arial", 16, "bold"), bg="#ECF0F1").pack(pady=10)

        # Table
        self.tree = ttk.Treeview(self, columns=("ID", "Customer", "Make", "Model", "Year", "VIN", "Plate"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(pady=10, padx=20, fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_row_selected)  # ✅ Binds row click to populate form
        self.load_data()

        # Form
        form_frame = tk.Frame(self, bg="#ECF0F1")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Customer:").grid(row=0, column=0)
        self.customer_entry = tk.Entry(form_frame)
        self.customer_entry.grid(row=0, column=1, padx=10)

        tk.Label(form_frame, text="Make:").grid(row=0, column=2)
        self.make_entry = tk.Entry(form_frame)
        self.make_entry.grid(row=0, column=3, padx=10)

        tk.Label(form_frame, text="Model:").grid(row=1, column=0)
        self.model_entry = tk.Entry(form_frame)
        self.model_entry.grid(row=1, column=1, padx=10)

        tk.Label(form_frame, text="Year:").grid(row=1, column=2)
        self.year_entry = tk.Entry(form_frame)
        self.year_entry.grid(row=1, column=3, padx=10)

        tk.Label(form_frame, text="VIN:").grid(row=2, column=0)
        self.vin_entry = tk.Entry(form_frame)
        self.vin_entry.grid(row=2, column=1, padx=10)

        tk.Label(form_frame, text="Plate:").grid(row=2, column=2)
        self.plate_entry = tk.Entry(form_frame)
        self.plate_entry.grid(row=2, column=3, padx=10)

        # Buttons
        button_frame = tk.Frame(self, bg="#ECF0F1")
        button_frame.pack(pady=10)

        self.add_btn = tk.Button(button_frame, text="Add Vehicle", bg="#27AE60", fg="black", command=self.add_vehicle)
        self.add_btn.pack(side="left", padx=10)

        self.update_btn = tk.Button(button_frame, text="Update Vehicle", bg="#F39C12", fg="black", command=self.update_vehicle)
        self.update_btn.pack(side="left", padx=10)

        self.delete_btn = tk.Button(button_frame, text="Delete Vehicle", bg="#E74C3C", fg="black", command=self.delete_vehicle)
        self.delete_btn.pack(side="left", padx=10)
        controller.add_back_button(self)

        # Disable Delete if not allowed
        if self.role not in ["Admin", "Customer"]:
            self.delete_btn.config(state="disabled")

    def load_data(self):
        """ Load sample data into the table """
        for vehicle in self.vehicles:
            self.tree.insert("", "end", values=(vehicle["ID"], vehicle["Customer"], vehicle["Make"], vehicle["Model"], vehicle["Year"], vehicle["VIN"], vehicle["Plate"]))

    def add_vehicle(self):
        if self.role != "Customer":
            messagebox.showwarning("Permission Denied", "Only customers can add vehicles.")
            return

        new_id = self.vehicles[-1]["ID"] + 1 if self.vehicles else 1
        new_vehicle = {
            "ID": new_id,
            "Customer": self.customer_entry.get(),
            "Make": self.make_entry.get(),
            "Model": self.model_entry.get(),
            "Year": self.year_entry.get(),
            "VIN": self.vin_entry.get(),
            "Plate": self.plate_entry.get()
        }

        self.vehicles.append(new_vehicle)
        self.tree.insert("", "end", values=(new_vehicle["ID"], new_vehicle["Customer"], new_vehicle["Make"],
                                            new_vehicle["Model"], new_vehicle["Year"],
                                            new_vehicle["VIN"], new_vehicle["Plate"]))
        messagebox.showinfo("Success", "Vehicle added successfully!")
        self.clear_fields()

    def update_vehicle(self):
        if self.role != "Customer":
            messagebox.showwarning("Permission Denied", "Only customers can update vehicles.")
            return

        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a vehicle to update.")
            return

        vehicle_id = int(self.tree.item(selected_item[0])['values'][0])

        for idx, vehicle in enumerate(self.vehicles):
            if vehicle["ID"] == vehicle_id:
                self.vehicles[idx] = {
                    "ID": vehicle_id,
                    "Customer": self.customer_entry.get(),
                    "Make": self.make_entry.get(),
                    "Model": self.model_entry.get(),
                    "Year": self.year_entry.get(),
                    "VIN": self.vin_entry.get(),
                    "Plate": self.plate_entry.get()
                }
                self.tree.item(selected_item, values=(
                    vehicle_id, self.customer_entry.get(), self.make_entry.get(),
                    self.model_entry.get(), self.year_entry.get(),
                    self.vin_entry.get(), self.plate_entry.get()
                ))
                messagebox.showinfo("Success", "Vehicle updated successfully!")
                self.clear_fields()
                return

    def delete_vehicle(self):
        if self.role not in ["Admin", "Customer"]:
            messagebox.showwarning("Permission Denied", "Only admins or customers can delete vehicles.")
            return

        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a vehicle to delete.")
            return

        vehicle_id = int(self.tree.item(selected_item[0])['values'][0])

        for idx, vehicle in enumerate(self.vehicles):
            if vehicle["ID"] == vehicle_id:
                del self.vehicles[idx]
                break

        self.tree.delete(selected_item)
        messagebox.showinfo("Success", "Vehicle deleted successfully!")
        self.clear_fields()

    def clear_fields(self):
        self.customer_entry.delete(0, tk.END)
        self.make_entry.delete(0, tk.END)
        self.model_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.vin_entry.delete(0, tk.END)
        self.plate_entry.delete(0, tk.END)

    def on_row_selected(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0], "values")
            self.customer_entry.delete(0, tk.END)
            self.customer_entry.insert(0, values[1])

            self.make_entry.delete(0, tk.END)
            self.make_entry.insert(0, values[2])

            self.model_entry.delete(0, tk.END)
            self.model_entry.insert(0, values[3])

            self.year_entry.delete(0, tk.END)
            self.year_entry.insert(0, values[4])

            self.vin_entry.delete(0, tk.END)
            self.vin_entry.insert(0, values[5])

            self.plate_entry.delete(0, tk.END)
            self.plate_entry.insert(0, values[6])
