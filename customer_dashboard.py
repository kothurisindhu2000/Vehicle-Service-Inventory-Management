import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from datetime import datetime, timedelta

class CustomerDashboard(tk.Tk):
    def __init__(self, customer_id):
        super().__init__()
        self.customer_id = customer_id
        self.title("Customer Dashboard")
        self.geometry("900x500")
        self.configure(bg="#F9F9F9")

        # Left panel
        left_frame = tk.Frame(self, width=200, bg="#DCE1E3")
        left_frame.pack(side="left", fill="both")

        tk.Label(left_frame, text="Dashboard", font=("Arial", 16, "bold"), bg="#DCE1E3").pack(pady=30)
        tk.Button(left_frame, text="Schedule a Service", width=20, command=self.schedule_service, bg="#3498DB").pack(pady=10)
        tk.Button(left_frame, text="View Previous Services", width=20, command=self.view_previous_services, bg="#2ECC71").pack(pady=10)
        tk.Button(left_frame, text="Current Service Status", width=20, command=self.check_current_status, bg="#F1C40F").pack(pady=10)
        tk.Button(left_frame, text="Log Out", width=20, command=self.logout, bg="#E74C3C", fg="white").pack(pady=10)

        # Right panel
        self.right_frame = tk.Frame(self, bg="#FFFFFF")
        self.right_frame.pack(side="right", fill="both", expand=True)

    def logout(self):
        """Cleanly exit the dashboard."""
        confirm = messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?")
        if confirm:
            self.destroy()
            from Login import LoginPage  # <- local import avoids circular dependency
            LoginPage().mainloop()

    def connect_db(self):
        return mysql.connector.connect(
            host='141.209.241.91',
            port=3306,
            user='sp2025bis698g6',
            password='warm',
            database='sp2025bis698g6s'
        )

    def clear_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def schedule_service(self):
        self.clear_right_frame()

        tk.Label(self.right_frame, text="Schedule a Service", font=("Arial", 16, "bold"), bg="#FFFFFF").pack(pady=10)

        tk.Label(self.right_frame, text="Select Services", font=("Arial", 12), bg="#FFFFFF").pack(pady=5)

        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT Service_ID, ServiceName, Service_Cost FROM SERVICES")
        self.services = cursor.fetchall()
        conn.close()

        self.service_map = {i: (sid, cost) for i, (sid, name, cost) in enumerate(self.services)}

        self.service_listbox = tk.Listbox(self.right_frame, selectmode="multiple", height=30, width=100, exportselection=0)
        for _, name, cost in self.services:
            self.service_listbox.insert("end", f"{name} - ${cost}")
        self.service_listbox.pack(padx=20, pady=5)

        tk.Label(self.right_frame, text="Optional Notes:", bg="#FFFFFF").pack(pady=(10, 0))
        self.notes_entry = tk.Text(self.right_frame, height=4, width=60)
        self.notes_entry.pack(pady=(0, 10))

        tk.Button(self.right_frame, text="Proceed", bg="#2ECC71", command=self.proceed_service).pack(pady=10)

    def proceed_service(self):
        selected_indices = self.service_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No Service Selected", "Please select at least one service.")
            return

        selected_services = [self.service_map[i] for i in selected_indices]
        total_amount = sum(cost for _, cost in selected_services)
        service_date = datetime.today().date()
        delivery_date = service_date + timedelta(days=3)
        notes = self.notes_entry.get("1.0", "end").strip()

        conn = self.connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO SERVICE_REQUEST (Customer_ID, Total_Amount, Service_Date, Service_Notes, Mechanic_ID, Service_Status, Delivery_Date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (self.customer_id, total_amount, service_date, notes, 1, "Pending", delivery_date))
        service_request_id = cursor.lastrowid

        for sid, cost in selected_services:
            cursor.execute("""
                INSERT INTO SERVICE_SELECTION (Service_ID, Customer_ID, Service_Cost)
                VALUES (%s, %s, %s)
            """, (sid, self.customer_id, cost))

        conn.commit()
        conn.close()

        messagebox.showinfo("Service Scheduled", f"Service scheduled!\nDelivery Date: {delivery_date}\nTotal: ${total_amount:.2f}")
        self.check_current_status()
          # Reset the form

    def view_previous_services(self):
        self.clear_right_frame()
        tk.Label(self.right_frame, text="Previous Services", font=("Arial", 16, "bold"), bg="#FFFFFF").pack(pady=10)

        container = tk.Frame(self.right_frame, bg="#FFFFFF")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("Service_Date", "Total_Amount", "Service_Notes", "Service_Status", "Delivery_Date", "Service_Request_ID")
        self.tree = ttk.Treeview(container, columns=columns, show="headings", height=15)

        for col in columns:
            self.tree.heading(col, text=col.replace("_", " "))
            self.tree.column(col, anchor="center", width=140)

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        try:
            conn = self.connect_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM SERVICE_REQUEST 
                WHERE Customer_ID = %s AND Service_Status = 'Completed'
                ORDER BY Service_Date DESC
            """, (self.customer_id,))
            services = cursor.fetchall()
            conn.close()

            if not services:
                self.tree.insert("", "end", values=("No records", "", "", "", "", ""))
            else:
                for svc in services:
                    self.tree.insert("", "end", values=(
                        svc['Service_Date'],
                        f"${svc['Total_Amount']:.2f}",
                        svc['Service_Notes'][:50] + ("..." if len(svc['Service_Notes']) > 50 else ""),
                        svc['Service_Status'],
                        svc['Delivery_Date'],
                        svc['Service_Request_ID']
                    ))

            tk.Button(self.right_frame, text="Give Feedback", bg="#27AE60", fg="white",
                    command=lambda: self.open_feedback_form(self.tree)).pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_feedback_form(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a service to give feedback on.")
            return

        item = tree.item(selected[0])
        values = item["values"]
        service_request_id = values[5]

        feedback_window = tk.Toplevel(self)
        feedback_window.title("Give Feedback")
        feedback_window.geometry("400x350")
        feedback_window.configure(bg="#F4F6F7")

        tk.Label(feedback_window, text="Rate your experience:", bg="#F4F6F7", font=("Arial", 12)).pack(pady=(10, 5))

        # Star rating UI
        star_frame = tk.Frame(feedback_window, bg="#F4F6F7")
        star_frame.pack()
        rating_var = tk.IntVar(value=0)
        stars = []

        def update_stars(selected_rating):
            rating_var.set(selected_rating)
            for i in range(5):
                stars[i].config(text="★" if i < selected_rating else "☆")

        for i in range(5):
            btn = tk.Button(star_frame, text="☆", font=("Arial", 20), bd=0, bg="#F4F6F7", command=lambda r=i+1: update_stars(r))
            btn.grid(row=0, column=i, padx=5)
            stars.append(btn)

        # Feedback box
        tk.Label(feedback_window, text="Feedback:", bg="#F4F6F7").pack(pady=(20, 5))
        feedback_text = tk.Text(feedback_window, height=5, width=40)
        feedback_text.pack()

        # Pre-fill if feedback exists
        try:
            conn = self.connect_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT Rating, Customer_feedback FROM FEEDBACK
                WHERE Customer_ID = %s AND Service_Request_ID = %s
            """, (self.customer_id, service_request_id))
            existing = cursor.fetchone()
            conn.close()

            if existing:
                update_stars(existing["Rating"])
                feedback_text.insert("1.0", existing["Customer_feedback"])

        except Exception as e:
            messagebox.showerror("Load Feedback Error", str(e))

        def submit_feedback():
            rating = rating_var.get()
            feedback = feedback_text.get("1.0", "end").strip()

            if rating == 0:
                messagebox.showerror("Error", "Please select a star rating.")
                return

            try:
                conn = self.connect_db()
                cursor = conn.cursor(dictionary=True)

                cursor.execute("""
                    SELECT Feedback_ID FROM FEEDBACK
                    WHERE Customer_ID = %s AND Service_Request_ID = %s
                """, (self.customer_id, service_request_id))
                existing = cursor.fetchone()

                if existing:
                    cursor.execute("""
                        UPDATE FEEDBACK
                        SET Customer_feedback = %s, Rating = %s
                        WHERE Feedback_ID = %s
                    """, (feedback, rating, existing["Feedback_ID"]))
                    messagebox.showinfo("Updated", "Your feedback has been updated.")
                else:
                    cursor.execute("""
                        INSERT INTO FEEDBACK (Service_Request_ID, Customer_feedback, Rating, Customer_ID)
                        VALUES (%s, %s, %s, %s)
                    """, (service_request_id, feedback, rating, self.customer_id))
                    messagebox.showinfo("Success", "Feedback submitted successfully!")

                conn.commit()
                conn.close()
                feedback_window.destroy()

            except Exception as e:
                messagebox.showerror("Database Error", str(e))


        tk.Button(feedback_window, text="Submit", command=submit_feedback, bg="#2ECC71", fg="white").pack(pady=15)



    


    def check_current_status(self):
        self.clear_right_frame()
        tk.Label(self.right_frame, text="Current Service Status", font=("Arial", 16, "bold"), bg="#FFFFFF").pack(pady=10)

        columns = ("Service Date", "Total Cost", "Notes", "Status", "Delivery Date")
        tree = ttk.Treeview(self.right_frame, columns=columns, show="headings", height=5)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=160, anchor="center")

        tree.pack(padx=10, pady=20, fill="x")

        try:
            conn = self.connect_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM SERVICE_REQUEST 
                WHERE Customer_ID = %s AND Service_Status IN ('Pending', 'In Progress')
                ORDER BY Service_Date DESC
            """, (self.customer_id,))
            services = cursor.fetchall()
            conn.close()

            if not services:
                tree.insert("", "end", values=("No records", "", "", "", ""))
            else:
                for svc in services:
                    tree.insert("", "end", values=(
                        svc['Service_Date'],
                        f"${svc['Total_Amount']:.2f}",
                        svc['Service_Notes'][:50] + ("..." if len(svc['Service_Notes']) > 50 else ""),
                        svc['Service_Status'],
                        svc['Delivery_Date']
                    ))

        except Exception as e:
            messagebox.showerror("Error", str(e))





    def check_current_status(self):
        self.clear_right_frame()    
        
        tk.Label(self.right_frame, text="Current Service Status", font=("Arial", 16, "bold"), bg="#FFFFFF").pack(pady=10)

        columns = ("Service Date", "Total Cost", "Notes", "Status","Delivery Date")
        tree = ttk.Treeview(self.right_frame, columns=columns, show="headings", height=5)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=200, anchor="center")
        tree.pack(padx=10, pady=20, fill="x")

        try:
            conn = self.connect_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM SERVICE_REQUEST 
                WHERE Customer_ID = %s AND Service_Status IN ('Pending' , 'In Progress')
                ORDER BY Service_Date DESC
            """, (self.customer_id,))
            services = cursor.fetchall()
            conn.close()

            if not services:
                tree.insert("", "end", values=("No records", "", "", "", ""))
            else:
                for svc in services:
                    tree.insert("", "end", values=(
                        svc['Service_Date'],
                        f"${svc['Total_Amount']:.2f}",
                        svc['Service_Notes'][:50] + ("..." if len(svc['Service_Notes']) > 50 else ""),
                        svc['Service_Status'],
                        svc['Delivery_Date']
                    ))

        except Exception as e:
            messagebox.showerror("Error", str(e))




# For testing only
if __name__ == "__main__":
    app = CustomerDashboard(customer_id=1)
    app.mainloop()
