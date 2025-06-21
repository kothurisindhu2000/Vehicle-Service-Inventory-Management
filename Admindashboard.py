import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='141.209.241.91',
        port=3306,
        user='sp2025bis698g6',
        password='warm',
        database='sp2025bis698g6s'
    )

class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x650")
        self.root.title("Admin Dashboard")
        self.root.configure(bg="#ECF0F1")

        tk.Label(root, text="Admin Dashboard", font=("Arial", 18, "bold"), bg="#2C3E50", fg="white").pack(fill=tk.X)

        button_frame = tk.Frame(root, bg="#34495E", width=200)
        button_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.content_frame = tk.Frame(root, bg="#FDFEFE")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Navigation Buttons
        tk.Button(button_frame, text="Dashboard Overview", bg="#1ABC9C", fg="white", width=25,
                  command=self.show_metrics).pack(pady=10)
        tk.Button(button_frame, text="All Services", bg="#3498DB", fg="white", width=25,
                  command=self.show_all_services).pack(pady=5)
        tk.Button(button_frame, text="Unassigned Services", bg="#9B59B6", fg="white", width=25,
                  command=self.show_unassigned_services).pack(pady=5)
        tk.Button(button_frame, text="Completed Services", bg="#E67E22", fg="white", width=25,
                  command=self.show_completed_services).pack(pady=5)
        tk.Button(button_frame, text="All Parts Details", bg="#E67E00", fg="white", width=25,
                  command=self.show_parts_details).pack(pady=5)
        tk.Button(button_frame, text="All Suppliers", bg="#5D6D7E", fg="white", width=25,
                  command=self.show_suppliers).pack(pady=5)
        tk.Button(button_frame, text="Add New Service", bg="#F39C12", fg="white", width=25,
          command=self.show_add_service_form).pack(pady=5)
        tk.Button(button_frame, text="Add New Mechanic", bg="#8E44AD", fg="white", width=25,
          command=self.show_add_mechanic_form).pack(pady=5)
        tk.Button(button_frame, text="Logout", bg="#E74C3C", fg="white", width=25,
          command=self.logout).pack(pady=30)


        self.show_metrics()

    def logout(self):
        self.root.destroy()
        from Login import LoginPage
        LoginPage().mainloop()


    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_metrics(self):
        self.clear_content()

        tk.Label(self.content_frame, text="Dashboard Overview", font=("Arial", 18, "bold"), bg="#FDFEFE", fg="#2C3E50").pack(pady=10)

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM CUSTOMER")
        customers = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM MECHANIC")
        mechanics = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM SERVICE_REQUEST WHERE Service_Status = 'In Progress'")
        in_progress = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM SERVICE_REQUEST WHERE Service_Status = 'Pending'")
        pending = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM SERVICE_REQUEST WHERE Service_Status = 'Completed'")
        completed = cursor.fetchone()[0]

        conn.close()

        stats = [
            ("👥 Customers", customers, "#3498DB"),
            ("🔧 Mechanics", mechanics, "#9B59B6"),
            ("🚗 In Progress Services", in_progress, "#E67E22"),
            ("🕒 Pending Services", pending, "#F1C40F"),
            ("✅ Completed Services", completed, "#2ECC71")
        ]

        cards_frame = tk.Frame(self.content_frame, bg="#FDFEFE")
        cards_frame.pack(pady=10)

        for idx, (label, value, color) in enumerate(stats):
            box = tk.Frame(cards_frame, bg=color, width=180, height=100, bd=2, relief=tk.RIDGE)
            box.grid(row=0, column=idx, padx=10, pady=10)
            box.grid_propagate(False)

            tk.Label(box, text=label, font=("Arial", 10, "bold"), bg=color, fg="white", wraplength=150, justify="center").pack(pady=5)
            tk.Label(box, text=str(value), font=("Arial", 16, "bold"), bg=color, fg="white").pack()


    def show_all_services(self):
        self.clear_content()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Service_ID, ServiceName, Service_Cost FROM SERVICES")
        data = cursor.fetchall()
        conn.close()
        self.display_table(["ID", "Service Name", "Cost"], data)

    def show_unassigned_services(self):
        self.clear_content()

        # Add a frame that will use grid layout, and pack it inside the content_frame
        grid_frame = tk.Frame(self.content_frame, bg="#FDFEFE")
        grid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(grid_frame, text="Services Assigned to MechUser0 (Unassigned Services)", font=("Arial", 16, "bold"),
                bg="#FDFEFE").grid(row=0, column=0, columnspan=6, pady=10)

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Services where Mechanic_ID = 1 (MechUser0)
        cursor.execute("""
            SELECT sr.Service_Request_ID, sr.Customer_ID, sr.Service_Date, sr.Service_Status
            FROM SERVICE_REQUEST sr
            WHERE sr.Mechanic_ID = 1
            AND sr.Service_Status IN ('Pending', 'In Progress')
        """)
        rows = cursor.fetchall()

        if not rows:
            tk.Label(grid_frame, text="No unassigned services.", bg="#FDFEFE", font=("Arial", 12)).grid(row=1, column=0, columnspan=6)
            return

        # Get list of mechanics (excluding MechUser0)
        cursor.execute("SELECT Name FROM MECHANIC WHERE Mechanic_ID != 1")
        mechanic_names = [r["Name"] for r in cursor.fetchall()]
        conn.close()

        headers = ["Request ID", "Customer ID", "Service Date", "Status", "Assign Mechanic", "Action"]
        for col, header in enumerate(headers):
            tk.Label(grid_frame, text=header, font=("Arial", 10, "bold"), bg="#D6EAF8", width=20).grid(row=2, column=col, pady=5)

        for row_idx, row in enumerate(rows, start=3):
            req_id = row["Service_Request_ID"]

            tk.Label(grid_frame, text=req_id, bg="#FDFEFE").grid(row=row_idx, column=0)
            tk.Label(grid_frame, text=row["Customer_ID"], bg="#FDFEFE").grid(row=row_idx, column=1)
            tk.Label(grid_frame, text=row["Service_Date"], bg="#FDFEFE").grid(row=row_idx, column=2)
            tk.Label(grid_frame, text=row["Service_Status"], bg="#FDFEFE").grid(row=row_idx, column=3)

            # Create unique StringVar per dropdown
            mech_var = tk.StringVar()
            dropdown = ttk.Combobox(grid_frame, textvariable=mech_var, values=mechanic_names, width=20, state="readonly")
            dropdown.grid(row=row_idx, column=4)

            # Fix closure issue by using mech_var here
            def make_assigner(req_id=req_id, name_var=mech_var):
                def assign():
                    selected_name = name_var.get()
                    if not selected_name:
                        messagebox.showerror("Missing", "Please select a mechanic.")
                        return
                    conn2 = get_db_connection()
                    cur2 = conn2.cursor()
                    cur2.execute("SELECT Mechanic_ID FROM MECHANIC WHERE Name = %s", (selected_name,))
                    result = cur2.fetchone()
                    if result:
                        new_id = result[0]
                        cur2.execute("UPDATE SERVICE_REQUEST SET Mechanic_ID = %s WHERE Service_Request_ID = %s", (new_id, req_id))
                        conn2.commit()
                        cur2.close()
                        conn2.close()
                        messagebox.showinfo("Success", f"Assigned '{selected_name}' (ID {new_id}) to Service {req_id}")
                        self.clear_content()
                        self.show_unassigned_services()
                    else:
                        messagebox.showerror("Error", "Mechanic not found.")
                        conn2.close()

                return assign

            tk.Button(grid_frame, text="Assign", bg="#28B463", fg="white", command=make_assigner()).grid(row=row_idx, column=5, padx=5)


        conn.close()

    def show_completed_services(self):
        self.clear_content()

        grid_frame = tk.Frame(self.content_frame, bg="#FDFEFE")
        grid_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(grid_frame, text="Completed Services", font=("Arial", 16, "bold"), bg="#FDFEFE").grid(row=0, column=0, columnspan=8, pady=10)

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT sr.Service_Request_ID, sr.Service_Date, sr.Delivery_Date, sr.Mechanic_ID, sr.Service_Status,
                c.Name AS Customer_Name, m.Name AS Mechanic_Name
            FROM SERVICE_REQUEST sr
            JOIN CUSTOMER c ON sr.Customer_ID = c.Customer_ID
            JOIN MECHANIC m ON sr.Mechanic_ID = m.Mechanic_ID
            WHERE sr.Service_Status = 'Completed' AND (sr.Payment_Status IS NULL OR sr.Payment_Status != 'Paid')
        """)
        services = cursor.fetchall()
        conn.close()

        headers = ["Request ID", "Customer", "Mechanic", "Mech ID", "Service Date", "Delivery Date", "Payment Status", "Action"]
        for col, h in enumerate(headers):
            tk.Label(grid_frame, text=h, font=("Arial", 10, "bold"), bg="#D6EAF8", width=18).grid(row=1, column=col)

        for row_idx, s in enumerate(services, start=2):
            tk.Label(grid_frame, text=s["Service_Request_ID"]).grid(row=row_idx, column=0)
            tk.Label(grid_frame, text=s["Customer_Name"]).grid(row=row_idx, column=1)
            tk.Label(grid_frame, text=s["Mechanic_Name"]).grid(row=row_idx, column=2)
            tk.Label(grid_frame, text=s["Mechanic_ID"]).grid(row=row_idx, column=3)
            tk.Label(grid_frame, text=s["Service_Date"]).grid(row=row_idx, column=4)
            tk.Label(grid_frame, text=s["Delivery_Date"]).grid(row=row_idx, column=5)

            status_var = tk.StringVar(value="Unpaid")  # default
            dropdown = ttk.Combobox(grid_frame, textvariable=status_var, values=["Unpaid", "Paid"], width=12, state="readonly")
            dropdown.grid(row=row_idx, column=6)

            def make_updater(req_id=s["Service_Request_ID"], status_var=status_var):
                def update():
                    new_status = status_var.get()
                    try:
                        conn2 = get_db_connection()
                        cur2 = conn2.cursor()
                        cur2.execute("UPDATE SERVICE_REQUEST SET Payment_Status = %s WHERE Service_Request_ID = %s", (new_status, req_id))
                        conn2.commit()
                        conn2.close()
                        messagebox.showinfo("Updated", f"Marked Service {req_id} as {new_status}")
                        self.show_completed_services()
                    except Exception as e:
                        messagebox.showerror("Error", str(e))
                return update

            tk.Button(grid_frame, text="Update", bg="#27AE60", fg="white", command=make_updater()).grid(row=row_idx, column=7)


    def show_parts_details(self):
        self.clear_content()
        conn = get_db_connection()
        cursor = conn.cursor()

        tk.Label(self.content_frame, text="All Tools", font=("Arial", 14, "bold"), bg="#FDFEFE").pack(pady=5)
        cursor.execute("SELECT Part_ID, Part_name, Total_quantity FROM PARTS")
        parts = cursor.fetchall()
        self.display_table(["Part ID", "Part Name", "Total Qty"], parts)

        tk.Label(self.content_frame, text="Tools Used Per Service", font=("Arial", 14, "bold"), bg="#FDFEFE").pack(pady=10)
        cursor.execute("""
            SELECT p.Part_name, pu.Quantity_used, pu.Service_ID
            FROM PARTS_USED pu
            JOIN PARTS p ON pu.Part_ID = p.Part_ID
        """)
        usage = cursor.fetchall()
        conn.close()
        self.display_table(["Part Name", "Qty Used", "Service ID"], usage)

    def show_suppliers(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Suppliers List", font=("Arial", 16, "bold"), bg="#FDFEFE").pack(pady=10)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Supplier_ID, Name, Contact_Number, Address FROM SUPPLIER")
        data = cursor.fetchall()
        conn.close()
        self.display_table(["Supplier ID", "Name", "Contact", "Address"], data)

    def display_table(self, columns, data):
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=180)
        for row in data:
            tree.insert('', tk.END, values=row)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def show_add_service_form(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Add New Service", font=("Arial", 16, "bold"), bg="#FDFEFE").pack(pady=10)

        name_var = tk.StringVar()
        cost_var = tk.StringVar()

        tk.Label(self.content_frame, text="Service Name:").pack(pady=5)
        tk.Entry(self.content_frame, textvariable=name_var, width=30).pack()

        tk.Label(self.content_frame, text="Service Cost:").pack(pady=5)
        tk.Entry(self.content_frame, textvariable=cost_var, width=30).pack()

        def save_service():
            name = name_var.get().strip()
            try:
                cost = float(cost_var.get())
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO SERVICES (ServiceName, Service_Cost) VALUES (%s, %s)", (name, cost))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", f"Service '{name}' added.")
                self.show_all_services()
            except ValueError:
                messagebox.showerror("Invalid", "Service cost must be a number.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.content_frame, text="Add Service", bg="#27AE60", fg="white", command=save_service).pack(pady=10)

    def show_add_mechanic_form(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Add New Mechanic", font=("Arial", 16, "bold"), bg="#FDFEFE").pack(pady=10)

        name_var = tk.StringVar()
        username_var = tk.StringVar()
        password_var = tk.StringVar()

        tk.Label(self.content_frame, text="Name:").pack(pady=5)
        tk.Entry(self.content_frame, textvariable=name_var, width=30).pack()

        tk.Label(self.content_frame, text="Username:").pack(pady=5)
        tk.Entry(self.content_frame, textvariable=username_var, width=30).pack()

        tk.Label(self.content_frame, text="Password:").pack(pady=5)
        tk.Entry(self.content_frame, textvariable=password_var, width=30, show="*").pack()

        def save_mechanic():
            name = name_var.get().strip()
            user = username_var.get().strip()
            pwd = password_var.get().strip()

            if not all([name, user, pwd]):
                messagebox.showerror("Invalid", "All fields are required.")
                return

            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO MECHANIC (Name, Mechanic_User_Name, Mechanic_Password) VALUES (%s, %s, %s)",
                            (name, user, pwd))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", f"Mechanic '{name}' added.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.content_frame, text="Add Mechanic", bg="#27AE60", fg="white", command=save_mechanic).pack(pady=10)



if __name__ == "__main__":
    root = tk.Tk()
    AdminDashboard(root)  # Replace with actual mechanic ID
    root.mainloop()
