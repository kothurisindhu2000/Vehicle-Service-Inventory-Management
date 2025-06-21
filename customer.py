import tkinter as tk
from tkinter import ttk, messagebox

class CustomersPage(tk.Frame):
    def __init__(self, parent, controller, role):
        super().__init__(parent)
        self.controller = controller
        self.role = role  # Default to 'customer'
        print("User role:", self.role)

        self.customers = [
            {"customer_id": 1, "name": "Tharun", "contact": "8976574325", "email": "tharun@gmail.com", "address": "123 Street, NY"},
        ]
        self.appointments = []  # Store appointments
       

        tk.Label(self, text="Customer Management", font=("Arial", 16, "bold")).pack(pady=10)

        table_frame = tk.Frame(self)
        table_frame.pack(pady=10)

        self.tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Contact", "Email", "Address"), show="headings")
        for col in ("ID", "Name", "Contact", "Email", "Address"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.bind("<<TreeviewSelect>>", self.select_customer)
        self.tree.pack()
        self.selected_customer = None
        self.selected_appointment = None
        # self.tree.bind("<<TreeviewSelect>>", self.on_row_selected)


        self.load_customers()

        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Contact:").grid(row=1, column=0, padx=5, pady=5)
        self.contact_entry = tk.Entry(form_frame, width=30)
        self.contact_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        self.email_entry = tk.Entry(form_frame, width=30)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Address:").grid(row=3, column=0, padx=5, pady=5)
        self.address_entry = tk.Entry(form_frame, width=30)
        self.address_entry.grid(row=3, column=1, padx=5, pady=5)

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        self.add_btn = tk.Button(button_frame, text="Add Customer", command=self.add_customer, bg="green", width=15)
        self.add_btn.grid(row=0, column=0, padx=5)

        self.update_btn = tk.Button(button_frame, text="Update Customer", command=self.update_customer, bg="blue", width=15)
        self.update_btn.grid(row=0, column=1, padx=5)

        self.delete_btn = tk.Button(button_frame, text="Delete Customer", command=self.delete_customer, bg="red", width=15)
        self.delete_btn.grid(row=0, column=2, padx=5)

        # Service Management
        service_frame = tk.LabelFrame(self, text="Service Management", font=("Arial", 12, "bold"), padx=10, pady=10)
        service_frame.pack(pady=20, fill="x", padx=20)

        if self.role == "Customer":
            tk.Button(service_frame, text="Book Appointment", command=self.book_appointment, bg="#1ABC9C", width=20).grid(row=0, column=0, padx=10, pady=5)
            controller.add_back_button(self)
        if self.role == "Admin":
            tk.Button(service_frame, text="Check Appointment Status", command=self.check_status, bg="#9B59B6", width=20).grid(row=0, column=0, padx=10, pady=5)
            controller.add_back_button(self)
        # controller.add_back_button(self)

        self.apply_role_restrictions()
        

    def apply_role_restrictions(self):
        if self.role == "Admin":
            self.add_btn.config(state="disabled")
            self.update_btn.config(state="disabled")
            # self.delete_btn.config(state="enable")
        elif self.role == "Customer":
            pass  # Customers can access customer operations

    def go_back(self):
        self.controller.show_frame("DashboardPage")

    def load_customers(self):
        self.tree.delete(*self.tree.get_children())
        for c in self.customers:
            self.tree.insert("", "end", values=(c["customer_id"], c["name"], c["contact"], c["email"], c["address"]))

    def select_customer(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            values = item["values"]
            self.selected_customer = values[0]

            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, values[1])
            self.contact_entry.delete(0, tk.END)
            self.contact_entry.insert(0, values[2])
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, values[3])
            self.address_entry.delete(0, tk.END)
            self.address_entry.insert(0, values[4])

    def add_customer(self):
        name = self.name_entry.get()
        contact = self.contact_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        if not all([name, contact, email, address]):
            messagebox.showerror("Error", "All fields are required!")
            return

        new_id = max([c["customer_id"] for c in self.customers], default=0) + 1
        self.customers.append({
            "customer_id": new_id,
            "name": name,
            "contact": contact,
            "email": email,
            "address": address
        })
        self.load_customers()
        self.clear_form()
        messagebox.showinfo("Success", "Customer added!")

    def update_customer(self):
        if self.selected_customer is None:
            messagebox.showerror("Error", "Select a customer to update.")
            return

        for c in self.customers:
            if c["customer_id"] == self.selected_customer:
                c["name"] = self.name_entry.get()
                c["contact"] = self.contact_entry.get()
                c["email"] = self.email_entry.get()
                c["address"] = self.address_entry.get()
                break

        self.load_customers()
        self.clear_form()
        messagebox.showinfo("Updated", "Customer updated!")

    def delete_customer(self):
        if self.selected_customer is None:
            messagebox.showerror("Error", "Select a customer to delete.")
            return

        self.customers = [c for c in self.customers if c["customer_id"] != self.selected_customer]
        self.load_customers()
        self.clear_form()
        messagebox.showinfo("Deleted", "Customer deleted.")

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.selected_customer = None

    def book_appointment(self):
        def confirm():
            vehicle = vehicle_entry.get()
            date = date_entry.get()
            service = service_type.get()
            if not vehicle or not date or not service:
                messagebox.showwarning("Incomplete", "Fill all fields.")
                return
            self.appointments.append({"vehicle": vehicle, "date": date, "service": service})
            messagebox.showinfo("Booked", f"Appointment booked for {vehicle}")
            popup.destroy()

        popup = tk.Toplevel(self)
        popup.title("Book Appointment")
        popup.geometry("300x200")

        tk.Label(popup, text="Vehicle:").pack()
        vehicle_entry = tk.Entry(popup)
        vehicle_entry.pack()

        tk.Label(popup, text="Date (YYYY-MM-DD):").pack()
        date_entry = tk.Entry(popup)
        date_entry.pack()

        tk.Label(popup, text="Service Type:").pack()
        service_type = ttk.Combobox(popup, values=["Oil Change", "Tire Rotation", "Battery Check"])
        service_type.pack()

        tk.Button(popup, text="Confirm", command=confirm, bg="green").pack(pady=10)

    def check_status(self):
        def show():
            result = "\n".join(
                [f"{i+1}. {a['vehicle']} on {a['date']} - {a['service']}" for i, a in enumerate(self.appointments)]
            )
            if not result:
                result = "No appointments found."
            messagebox.showinfo("Appointments", result)
            popup.destroy()

        popup = tk.Toplevel(self)
        popup.title("Check Appointment Status")
        popup.geometry("300x200")

        tk.Label(popup, text="Appointments:").pack()
        tk.Button(popup, text="Show All", command=show, bg="blue", fg="black").pack(pady=10)

    def delete_appointment(self):
        def delete_selected():
            idx = int(entry.get()) - 1
            if 0 <= idx < len(self.appointments):
                del self.appointments[idx]
                messagebox.showinfo("Deleted", "Appointment removed.")
            else:
                messagebox.showwarning("Invalid", "Invalid number.")
            popup.destroy()

        if not self.appointments:
            messagebox.showinfo("No Appointments", "Nothing to delete.")
            return

        popup = tk.Toplevel(self)
        popup.title("Delete Appointment")
        popup.geometry("300x200")

        for i, a in enumerate(self.appointments):
            tk.Label(popup, text=f"{i+1}. {a['vehicle']} - {a['date']} - {a['service']}").pack()

        tk.Label(popup, text="Enter number to delete:").pack()
        entry = tk.Entry(popup)
        entry.pack()
        tk.Button(popup, text="Delete", command=delete_selected, bg="red").pack(pady=10)
