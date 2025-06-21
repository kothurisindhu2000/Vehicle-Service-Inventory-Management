import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector
from datetime import datetime

def get_db_connection():
    return mysql.connector.connect(
        host='141.209.241.91',
        port=3306,
        user='sp2025bis698g6',
        password='warm',
        database='sp2025bis698g6s'
    )

class MechanicDashboard:
    def __init__(self, root, controller=None, role=None, mechanic_id=None):
        self.root = root
        self.controller = controller
        self.role = role
        self.mechanic_id = mechanic_id

        self.root.geometry("1000x600")
        self.root.title("Mechanic Dashboard")

        tk.Label(root, text="Mechanic Dashboard", font=("Arial", 18, "bold")).pack(pady=10)

        button_frame = tk.Frame(root)
        button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        self.content_frame = tk.Frame(root, bg="#F4F6F7")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Button(button_frame, text="Services Assigned to Me",bg="#3498DB", fg="white", width=25, command=self.show_assigned_services).pack(pady=5)
        tk.Button(button_frame, text="All Services",bg="#9B59B6", fg="white", width=25, command=self.show_all_services).pack(pady=5)
        tk.Button(button_frame, text="Previous Services",bg="#E67E22", fg="white", width=25, command=self.show_completed_services).pack(pady=5)
        tk.Button(button_frame, text="All Tools Details",bg="#E67E00", fg="white", width=25, command=self.show_tools_details).pack(pady=5)
        tk.Button(button_frame, text="Logout", bg="Blue", fg="white", width=25, command=self.logout).pack(pady=5)


    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def display_table(self, columns, data):
        tree = ttk.Treeview(self.content_frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        for row in data:
            tree.insert('', tk.END, values=row)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def show_all_services(self):
        self.clear_content()
        tk.Label(self.content_frame, text="All Services List", font=("Arial", 16, "bold"), bg="#FDFEFE").pack(pady=10)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Service_Request_ID, Service_Date, Mechanic_ID, Service_Status, Delivery_Date, Total_Amount
            FROM SERVICE_REQUEST
            WHERE Mechanic_ID = %s
        """, (self.mechanic_id,))
        rows = cursor.fetchall()
        conn.close()

        self.display_table(
            ["Service ID", "Service Date", "Mechanic ID", "Status", "Delivery Date", "Total Amount"],
            rows
        )

    def logout(self):
        from Login import LoginPage
        self.root.destroy()
        LoginPage().mainloop()

    def show_assigned_services(self):
        self.clear_content()
        #tk.Label(self.content_frame, text="Assigned Services to Me", font=("Arial", 16, "bold"), bg="#FDFEFE").grid(row=0, column=0, columnspan=7, pady=10)
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT Service_Request_ID, Service_Date, Service_Status, Delivery_Date
            FROM SERVICE_REQUEST
            WHERE Mechanic_ID = %s AND Service_Status IN ('Pending', 'In Progress')
        """, (self.mechanic_id,))
        services = cursor.fetchall()
        #print(f"Fetched {len(services)} assigned services for mechanic {self.mechanic_id}")
        cursor.close()
        conn.close()

        if not services:
            tk.Label(self.content_frame, text="No assigned services to update.").pack()
            return

        headers = ["Request ID", "Service Date", "Current Status", "New Status", "Current Delivery Date", "New Delivery Date", "Action"]
        for col_idx, header in enumerate(headers):
            tk.Label(self.content_frame, text=header, font=("Arial", 10, "bold")).grid(row=0, column=col_idx, padx=5, pady=5)

        status_options = ["Pending", "In Progress", "Completed"]

        for row_idx, service in enumerate(services, start=1):
            req_id = service["Service_Request_ID"]
            #tk.Label(self.content_frame, text=req_id).grid(row=row_idx, column=0,bg="#D6EAF8")
            tk.Label(self.content_frame, text=req_id, bg="#D6EAF8").grid(row=row_idx, column=0)
            tk.Label(self.content_frame, text=service["Service_Date"]).grid(row=row_idx, column=1)
            tk.Label(self.content_frame, text=service["Service_Status"]).grid(row=row_idx, column=2)

            # New status dropdown
            new_status_var = tk.StringVar(value=service["Service_Status"])
            status_menu = ttk.Combobox(self.content_frame, textvariable=new_status_var, values=status_options, state="readonly", width=15)
            status_menu.grid(row=row_idx, column=3)

            # Current delivery date
            tk.Label(self.content_frame, text=str(service["Delivery_Date"])).grid(row=row_idx, column=4)

            # New delivery date picker
            date_picker = DateEntry(self.content_frame, width=12, background='darkblue', foreground='white',
                                    borderwidth=2, date_pattern='yyyy-mm-dd')
            date_picker.set_date(service["Delivery_Date"])
            date_picker.grid(row=row_idx, column=5)

            # Update button
            def make_updater(req_id=req_id, status_var=new_status_var, date_widget=date_picker):
                def update():
                    new_status = status_var.get()
                    new_date = date_widget.get_date().strftime("%Y-%m-%d")

                    try:
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute("""
                            UPDATE SERVICE_REQUEST
                            SET Service_Status = %s, Delivery_Date = %s
                            WHERE Service_Request_ID = %s
                        """, (new_status, new_date, req_id))
                        conn.commit()
                        cursor.close()
                        conn.close()
                        messagebox.showinfo("Success", f"Service {req_id} updated.")
                        self.show_assigned_services()
                    except Exception as e:
                        messagebox.showerror("Update Error", str(e))

                return update

            #tk.Button(self.content_frame, text="Update", command=make_updater()).grid(row=row_idx, column=6, padx=5)
            tk.Button(self.content_frame, text="Update", command=make_updater(),bg="#27AE60",fg="white",activebackground="#2ECC71",activeforeground="white").grid(row=row_idx, column=6, padx=5, pady=2)

    def show_completed_services(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Feedback for Completed Services", font=("Arial", 16, "bold"), bg="#FDFEFE").pack(pady=10)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sr.Service_Request_ID, sr.Service_Date, f.Rating, f.Customer_feedback
            FROM SERVICE_REQUEST sr
            LEFT JOIN FEEDBACK f ON sr.Service_Request_ID = f.Service_Request_ID
            WHERE sr.Mechanic_ID = %s AND sr.Service_Status = 'Completed'
        """, (self.mechanic_id,))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            tk.Label(self.content_frame, text="No completed services found.", font=("Arial", 12), bg="#FDFEFE").pack(pady=20)
            return

        self.display_table(["Request ID", "Date", "Rating", "Feedback"], rows)

    def show_tools_details(self):
        self.clear_content()

        heading = tk.Label(self.content_frame, text="All Tools & Usage Details", font=("Arial", 16, "bold"), bg="#FDFEFE", fg="#2C3E50")
        heading.pack(pady=10)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Top Table: All Tools from PARTS
        cursor.execute("""
            SELECT Part_ID, Part_name, Total_quantity FROM PARTS
        """)
        parts = cursor.fetchall()

        top_label = tk.Label(self.content_frame, text="🧰 All Tools Inventory", font=("Arial", 12, "bold"), fg="#1F618D", bg="#FDFEFE")
        top_label.pack(pady=(10, 0))
        top_table = ttk.Treeview(self.content_frame, columns=["Part ID", "Part Name", "Total Quantity"], show="headings", height=8)
        for col in ["Part ID", "Part Name", "Total Quantity"]:
            top_table.heading(col, text=col)
            top_table.column(col, width=150)
        for row in parts:
            top_table.insert("", tk.END, values=row)
        top_table.pack(pady=5, fill=tk.X)

        # Bottom Table: Tools used per service
        cursor.execute("""
            SELECT p.Part_name, pu.Quantity_used, pu.Service_ID
            FROM PARTS_USED pu
            JOIN PARTS p ON pu.Part_ID = p.Part_ID
        """)
        parts_used = cursor.fetchall()
        conn.close()

        bottom_label = tk.Label(self.content_frame, text="🔧 Tools Used Per Service", font=("Arial", 12, "bold"), fg="#AF601A", bg="#FDFEFE")
        bottom_label.pack(pady=(20, 0))
        bottom_table = ttk.Treeview(self.content_frame, columns=["Part Name", "Quantity Used", "Service ID"], show="headings", height=10)
        for col in ["Part Name", "Quantity Used", "Service ID"]:
            bottom_table.heading(col, text=col)
            bottom_table.column(col, width=160)
        for row in parts_used:
            bottom_table.insert("", tk.END, values=row)
        bottom_table.pack(pady=5, fill=tk.X)
    
    
# Example of launching the dashboard directly
if __name__ == "__main__":
    root = tk.Tk()
    MechanicDashboard(root, mechanic_id=27)  # Replace with actual mechanic ID
    root.mainloop()
