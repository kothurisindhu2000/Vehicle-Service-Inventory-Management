import tkinter as tk
from tkinter import ttk, messagebox

class FeedbackPage(tk.Frame):
    def __init__(self, parent, controller, role):
        super().__init__(parent, bg="#ECF0F1")
        self.controller = controller
        self.role = role  # This is the role (mechanic, customer, admin)

        self.feedback_list = [
            {
                "ID": 1,
                "Customer": "Tharun",
                "Order ID": 101,
                "Rating": 5,
                "Comments": "Excellent service!",
                "Date": "2025-03-22",
                "Mechanic Reply": ""
            }
        ]

        tk.Label(self, text="Customer Feedback & Reviews", font=("Arial", 16, "bold"), bg="#ECF0F1").pack(pady=10)

        # Table with Mechanic Reply
        self.tree = ttk.Treeview(self, columns=("ID", "Customer", "Order ID", "Rating", "Comments", "Date", "Mechanic Reply"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(pady=10, padx=20, fill="both", expand=True)
        self.load_data()
        self.tree.bind("<<TreeviewSelect>>", self.on_feedback_select)

        # Form
        form_frame = tk.Frame(self, bg="#ECF0F1")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Customer:").grid(row=0, column=0)
        self.customer_entry = tk.Entry(form_frame)
        self.customer_entry.grid(row=0, column=1, padx=10)

        tk.Label(form_frame, text="Order ID:").grid(row=0, column=2)
        self.order_id_entry = tk.Entry(form_frame)
        self.order_id_entry.grid(row=0, column=3, padx=10)

        tk.Label(form_frame, text="Rating (1-5):").grid(row=1, column=0)
        self.rating_entry = tk.Entry(form_frame)
        self.rating_entry.grid(row=1, column=1, padx=10)

        tk.Label(form_frame, text="Comments:").grid(row=1, column=2)
        self.comments_entry = tk.Entry(form_frame)
        self.comments_entry.grid(row=1, column=3, padx=10)

        tk.Label(form_frame, text="Date:").grid(row=2, column=0)
        self.date_entry = tk.Entry(form_frame)
        self.date_entry.grid(row=2, column=1, padx=10)

        tk.Label(form_frame, text="Mechanic Reply:").grid(row=2, column=2)
        self.mechanic_reply_entry = tk.Entry(form_frame)
        self.mechanic_reply_entry.grid(row=2, column=3, padx=10)

        # Buttons
        button_frame = tk.Frame(self, bg="#ECF0F1")
        button_frame.pack(pady=10)

        if self.role == "Customer":
            tk.Button(button_frame, text="Add Feedback", bg="#27AE60", fg="black", command=self.add_feedback).pack(side="left", padx=10)
            # tk.Button(button_frame, text="Reply to Feedback", bg="#F39C12", fg="black", state=tk.DISABLED).pack(side="left", padx=10)
            # tk.Button(button_frame, text="Remove Feedback", bg="#E74C3C", fg="black", state=tk.DISABLED).pack(side="left", padx=10)

        elif self.role == "Mechanic":
            # tk.Button(button_frame, text="Add Feedback", bg="#27AE60", fg="black", state=tk.DISABLED).pack(side="left", padx=10)
            tk.Button(button_frame, text="Reply to Feedback", bg="#F39C12", fg="black", command=self.update_feedback).pack(side="left", padx=10)
            tk.Button(button_frame, text="Remove Feedback", bg="#E74C3C", fg="black", state=tk.DISABLED).pack(side="left", padx=10)

        elif self.role == "Admin":
            # tk.Button(button_frame, text="Add Feedback", bg="#27AE60", fg="black", command=self.add_feedback).pack(side="left", padx=10)
            # tk.Button(button_frame, text="Reply to Feedback", bg="#F39C12", fg="black", command=self.update_feedback).pack(side="left", padx=10)
            tk.Button(button_frame, text="Remove Feedback", bg="#E74C3C", fg="black", command=self.delete_feedback).pack(side="left", padx=10)
        
        controller.add_back_button(self)
    def load_data(self):
        for fb in self.feedback_list:
            self.tree.insert("", "end", values=(fb["ID"], fb["Customer"], fb["Order ID"], fb["Rating"], fb["Comments"], fb["Date"], fb["Mechanic Reply"]))

    def on_feedback_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        self.customer_entry.delete(0, tk.END)
        self.customer_entry.insert(0, values[1])

        self.order_id_entry.delete(0, tk.END)
        self.order_id_entry.insert(0, values[2])

        self.rating_entry.delete(0, tk.END)
        self.rating_entry.insert(0, values[3])

        self.comments_entry.delete(0, tk.END)
        self.comments_entry.insert(0, values[4])

        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, values[5])

        self.mechanic_reply_entry.delete(0, tk.END)
        self.mechanic_reply_entry.insert(0, values[6])

    def add_feedback(self):
        new_id = len(self.feedback_list) + 1
        new_fb = {
            "ID": new_id,
            "Customer": self.customer_entry.get(),
            "Order ID": self.order_id_entry.get(),
            "Rating": int(self.rating_entry.get()),
            "Comments": self.comments_entry.get(),
            "Date": self.date_entry.get(),
            "Mechanic Reply": self.mechanic_reply_entry.get()
        }
        self.feedback_list.append(new_fb)
        self.tree.insert("", "end", values=(new_id, new_fb["Customer"], new_fb["Order ID"], new_fb["Rating"], new_fb["Comments"], new_fb["Date"], new_fb["Mechanic Reply"]))
        messagebox.showinfo("Success", "Feedback added successfully!")
        self.clear_fields()

    def update_feedback(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a feedback to reply to.")
            return
        rating_value = self.rating_entry.get()
        if not rating_value.isdigit() or not (1 <= int(rating_value) <= 5):
            messagebox.showerror("Error", "Please enter a valid rating between 1 and 5.")
            return

        selected_item = self.tree.item(selected)
        selected_id = selected_item['values'][0]

        updated = {
            "ID": selected_id,
            "Customer": self.customer_entry.get(),
            "Order ID": self.order_id_entry.get(),
            "Rating": int(self.rating_entry.get()),
            "Comments": self.comments_entry.get(),
            "Date": self.date_entry.get(),
            "Mechanic Reply": self.mechanic_reply_entry.get()
        }

        for fb in self.feedback_list:
            if fb["ID"] == selected_id:
                fb.update(updated)

        self.tree.item(selected, values=(updated["ID"], updated["Customer"], updated["Order ID"], updated["Rating"], updated["Comments"], updated["Date"], updated["Mechanic Reply"]))
        messagebox.showinfo("Success", "Feedback updated with mechanic reply!")
        self.clear_fields()

    def delete_feedback(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a feedback to delete.")
            return

        selected_item = self.tree.item(selected)
        selected_id = selected_item['values'][0]

        self.feedback_list = [fb for fb in self.feedback_list if fb["ID"] != selected_id]
        self.tree.delete(selected)
        messagebox.showinfo("Success", "Feedback deleted successfully!")

    def clear_fields(self):
        self.customer_entry.delete(0, tk.END)
        self.order_id_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)
        self.comments_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.mechanic_reply_entry.delete(0, tk.END)
