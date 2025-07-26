import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import re

CSV_FILE = "contacts.csv"

# ----- Utilities -----
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_phone(phone):
    return re.match(r"^[0-9]{10}$", phone)

def load_contacts():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Phone", "Email"])
    with open(CSV_FILE, "r") as f:
        reader = csv.reader(f)
        next(reader, None)
        return list(reader)

def save_contact(name, phone, email):
    with open(CSV_FILE, "a", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([name, phone, email])

def overwrite_contacts(contacts):
    with open(CSV_FILE, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Phone", "Email"])
        writer.writerows(contacts)

# ----- GUI -----
class ContactBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📒 Contact Book")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        self.selected_item = None

        self.build_ui()
        self.load_table()

    def build_ui(self):
        # Input Frame
        input_frame = tk.LabelFrame(self.root, text="Manage Contact", padx=10, pady=10)
        input_frame.place(x=20, y=20, width=660, height=110)

        tk.Label(input_frame, text="Name:").grid(row=0, column=0)
        tk.Label(input_frame, text="Phone:").grid(row=0, column=2)
        tk.Label(input_frame, text="Email:").grid(row=0, column=4)

        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()

        self.name_entry = tk.Entry(input_frame, textvariable=self.name_var, width=20)
        self.phone_entry = tk.Entry(input_frame, textvariable=self.phone_var, width=20)
        self.email_entry = tk.Entry(input_frame, textvariable=self.email_var, width=30)

        self.name_entry.grid(row=1, column=0, padx=5)
        self.phone_entry.grid(row=1, column=2, padx=5)
        self.email_entry.grid(row=1, column=4, padx=5)

        tk.Button(input_frame, text="Add", bg="#4caf50", fg="white", command=self.add_or_update_contact).grid(row=1, column=5, padx=10)
        tk.Button(input_frame, text="Clear", command=self.clear_fields).grid(row=1, column=6, padx=5)

        # Table Frame
        table_frame = tk.Frame(self.root)
        table_frame.place(x=20, y=140, width=660, height=280)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        style.configure("Treeview", rowheight=25)

        self.contact_table = ttk.Treeview(table_frame, columns=("Name", "Phone", "Email"), show="headings")
        self.contact_table.heading("Name", text="Name")
        self.contact_table.heading("Phone", text="Phone")
        self.contact_table.heading("Email", text="Email")

        self.contact_table.column("Name", width=180)
        self.contact_table.column("Phone", width=150)
        self.contact_table.column("Email", width=280)

        self.contact_table.pack(fill="both", expand=True)
        self.contact_table.bind("<Double-1>", self.load_selected_contact)

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.place(x=20, y=430, width=660)

        tk.Button(btn_frame, text="Delete", bg="#f44336", fg="white", command=self.delete_contact).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Refresh", bg="#2196f3", fg="white", command=self.load_table).pack(side="left", padx=10)

    def load_table(self):
        for row in self.contact_table.get_children():
            self.contact_table.delete(row)
        contacts = load_contacts()
        for contact in contacts:
            self.contact_table.insert('', 'end', values=contact)

    def add_or_update_contact(self):
        name = self.name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()

        if not name or not phone or not email:
            messagebox.showwarning("Missing Info", "All fields are required.")
            return
        if not is_valid_email(email):
            messagebox.showwarning("Invalid Email", "Enter a valid email address.")
            return
        if not is_valid_phone(phone):
            messagebox.showwarning("Invalid Phone", "Phone number must be 10 digits.")
            return

        contacts = load_contacts()
        if self.selected_item:
            # Update contact
            old_data = self.contact_table.item(self.selected_item)["values"]
            for i, contact in enumerate(contacts):
                if contact == old_data:
                    contacts[i] = [name, phone, email]
                    break
            overwrite_contacts(contacts)
            messagebox.showinfo("Updated", "Contact updated successfully.")
            self.selected_item = None
        else:
            if [name, phone, email] in contacts:
                messagebox.showwarning("Duplicate", "This contact already exists.")
                return
            save_contact(name, phone, email)
            messagebox.showinfo("Success", "Contact added successfully.")

        self.clear_fields()
        self.load_table()

    def load_selected_contact(self, event):
        selected = self.contact_table.selection()
        if selected:
            self.selected_item = selected[0]
            values = self.contact_table.item(self.selected_item)["values"]
            self.name_var.set(values[0])
            self.phone_var.set(values[1])
            self.email_var.set(values[2])

    def delete_contact(self):
        selected = self.contact_table.selection()
        if not selected:
            messagebox.showinfo("Info", "Select a contact to delete.")
            return

        result = messagebox.askyesno("Confirm", "Are you sure you want to delete this contact?")
        if not result:
            return

        contact_data = self.contact_table.item(selected)["values"]
        all_contacts = load_contacts()
        if contact_data in all_contacts:
            all_contacts.remove(contact_data)
            overwrite_contacts(all_contacts)
            messagebox.showinfo("Deleted", "Contact deleted successfully.")
            self.load_table()

    def clear_fields(self):
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.selected_item = None


# Run App
if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBookApp(root)
    root.mainloop()
