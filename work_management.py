# work_management.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# Mock parts list (replace this with DB fetch later)
AVAILABLE_PARTS = ["Brake Pads", "Oil Filter", "Air Filter", "Spark Plug", "Battery", "Headlight"]

class WorkManagementPage(tk.Frame):
    def __init__(self, parent, controller, role):
        super().__init__(parent, bg="#ECF0F1")
        self.controller = controller
        self.role = role  # Default to 'customer'
        print("User role:", self.role)

        tk.Label(self, text="Assigned Work", font=("Arial", 16, "bold"), bg="#ECF0F1", fg="#2C3E50").pack(pady=20)

        columns = ("JobID", "Vehicle", "Description", "Status")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(expand=True, fill="both", padx=20, pady=10)

        self.sample_jobs = [
            (101, "Toyota Corolla", "Oil Change", "Pending"),
            (102, "Honda Civic", "Brake Inspection", "In Progress"),
            (103, "Ford F-150", "Engine Diagnosis", "Completed")
        ]

        for job in self.sample_jobs:
            self.tree.insert("", "end", values=job)

        btn_frame = tk.Frame(self, bg="#ECF0F1")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Order Part", command=self.order_part, bg="#2ECC71", fg="black", width=15).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Edit Status", command=self.edit_status, bg="#F1C40F", fg="black", width=15).pack(side=tk.LEFT, padx=10)
        controller.add_back_button(self)
    def get_selected_job(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a job.")
            return None
        return self.tree.item(selected[0])

    def order_part(self):
        job = self.get_selected_job()
        if not job:
            return

        job_id = job["values"][0]

        # Create popup window
        popup = tk.Toplevel(self)
        popup.title("Order Part")
        popup.geometry("300x150")
        popup.resizable(False, False)

        tk.Label(popup, text=f"Order part for Job #{job_id}", font=("Arial", 12)).pack(pady=10)

        selected_part = tk.StringVar(value=AVAILABLE_PARTS[0])

        part_dropdown = ttk.Combobox(popup, textvariable=selected_part, values=AVAILABLE_PARTS, state="readonly")
        part_dropdown.pack(pady=10)

        def confirm_order():
            part = selected_part.get()
            messagebox.showinfo("Part Ordered", f"Ordered '{part}' for Job #{job_id}")
            popup.destroy()

        tk.Button(popup, text="Confirm", command=confirm_order, bg="#2980B9", fg="black").pack(pady=5)

    def edit_status(self):
        job = self.get_selected_job()
        if job:
            current_status = job["values"][3]
            status_options = ["Pending", "In Progress", "Completed"]

            new_status = simpledialog.askstring("Edit Status", f"Current status: {current_status}\nEnter new status:")
            if new_status and new_status in status_options:
                selected = self.tree.selection()[0]
                self.tree.set(selected, column="Status", value=new_status)
                messagebox.showinfo("Status Updated", f"Job status updated to '{new_status}'")
            else:
                messagebox.showerror("Invalid Status", "Please enter a valid status: Pending, In Progress, or Completed.")