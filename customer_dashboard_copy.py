# customer_dashboard.py

import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
            host = '141.209.241.91',
        port = 3306,
        user = 'sp2025bis698g6',
        password = 'warm',
        database = 'sp2025bis698g6s'
    )

# customer_dashboard.py

class CustomerDashboard(tk.Tk):
    def __init__(self, customer_id):
        super().__init__()
        self.customer_id = customer_id
        self.title("Customer Dashboard")
        self.geometry("600x500")
        self.configure(bg="#F9F9F9")

        tk.Label(self, text="Customer Dashboard", font=("Arial", 16, "bold"), bg="#F9F9F9").pack(pady=10)

        tk.Button(self, text="Schedule a Service", width=30, command=self.schedule_service, bg="#3498DB").pack(pady=10)
        tk.Button(self, text="View Previous Services", width=30, command=self.view_previous_services, bg="#2ECC71").pack(pady=10)
        tk.Button(self, text="Check Current Service Status", width=30, command=self.check_current_status, bg="#F1C40F").pack(pady=10)

        self.text_area = tk.Text(self, height=15, width=70, wrap="word")
        self.text_area.pack(pady=20)

    def get_customer_id(self):
        return self.customer_id


    def schedule_service(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT Service_ID, ServiceName, Service_Cost FROM sp2025bis698g6s.SERVICES")
            services = cursor.fetchall()

            if not services:
                messagebox.showinfo("No Services", "No services available to schedule.")
                return

            win = tk.Toplevel(self)
            win.title("Select a Service")
            win.geometry("400x200")

            tk.Label(win, text="Select Service:").pack(pady=5)
            selected_service = tk.StringVar()
            service_names = [f"{sid} - {name} (${cost})" for sid, name, cost in services]
            dropdown = ttk.Combobox(win, values=service_names, textvariable=selected_service)
            dropdown.pack()

            def confirm_schedule():
                index = dropdown.current()
                if index < 0:
                    messagebox.showerror("Selection Error", "Please select a valid service.")
                    return

                service_id, _, cost = services[index]
                customer_id = self.get_customer_id()

                cursor.execute("SELECT COALESCE(MAX(Service_Selection_ID), 0) + 1 FROM SERVICE_SELECTION")
                selection_id = cursor.fetchone()[0]

                cursor.execute("""
                    INSERT INTO SERVICE_SELECTION (Service_Selection_ID, Service_ID, Customer_ID, Service_Cost)
                    VALUES (%s, %s, %s, %s)
                """, (selection_id, service_id, customer_id, cost))

                conn.commit()
                conn.close()
                win.destroy()
                messagebox.showinfo("Success", "Service scheduled successfully!")

            tk.Button(win, text="Confirm", command=confirm_schedule).pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def view_previous_services(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            customer_id = self.get_customer_id()
            cursor.execute("""
                SELECT * FROM SERVICE_REQUEST 
                WHERE Customer_ID = %s AND Service_Status = 'Completed'
                ORDER BY Service_Date DESC
            """, (customer_id,))
            services = cursor.fetchall()
            conn.close()

            self.text_area.delete(1.0, tk.END)
            if not services:
                self.text_area.insert(tk.END, "No previous services found.\n")
            else:
                for svc in services:
                    self.text_area.insert(tk.END, f"Date: {svc['Service_Date']}\n")
                    self.text_area.insert(tk.END, f"Total: ${svc['Total_Amount']:.2f}\n")
                    self.text_area.insert(tk.END, f"Notes: {svc['Service_Notes']}\n")
                    self.text_area.insert(tk.END, f"Status: {svc['Service_Status']}\n")
                    self.text_area.insert(tk.END, "-"*40 + "\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def check_current_status(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            customer_id = self.get_customer_id()
            cursor.execute("""
                SELECT * FROM SERVICE_REQUEST 
                WHERE Customer_ID = %s AND Service_Status IN ('Pending', 'In Progress')
                ORDER BY Service_Date DESC
                LIMIT 1
            """, (customer_id,))
            svc = cursor.fetchone()
            conn.close()

            self.text_area.delete(1.0, tk.END)
            if not svc:
                self.text_area.insert(tk.END, "No current service in progress.\n")
            else:
                self.text_area.insert(tk.END, f"Service Date: {svc['Service_Date']}\n")
                self.text_area.insert(tk.END, f"Status: {svc['Service_Status']}\n")
                self.text_area.insert(tk.END, f"Expected Delivery: {svc['Delivery_Date']}\n")
                self.text_area.insert(tk.END, f"Notes: {svc['Service_Notes']}\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_customer_id(self):
        # 🔐 Replace with actual login session management if needed
        return 1  # Currently using Customer_ID = 1 for demonstration

