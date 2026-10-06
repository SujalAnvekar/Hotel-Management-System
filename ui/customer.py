import tkinter as tk
from tkinter import ttk, messagebox

from database.connection import get_connection


class CustomersPage:

    def __init__(self, parent):

        self.parent = parent

        # Main frame
        self.frame = tk.Frame(
            parent,
            bg="#F5F6FA"
        )

        self.frame.pack(
            fill="both",
            expand=True
        )

        # Create page
        self.create_widgets()

        # Load customers
        self.load_customers()

    # ==========================================
    # CREATE PAGE
    # ==========================================

    def create_widgets(self):

        # --------------------------------------
        # Title
        # --------------------------------------

        title_frame = tk.Frame(
            self.frame,
            bg="#F5F6FA"
        )

        title_frame.pack(
            fill="x",
            padx=30,
            pady=(25, 15)
        )

        tk.Label(
            title_frame,
            text="Customers",
            bg="#F5F6FA",
            fg="#172033",
            font=("Segoe UI", 24, "bold")
        ).pack(
            side="left"
        )

        # --------------------------------------
        # Search Area
        # --------------------------------------

        search_frame = tk.Frame(
            self.frame,
            bg="#F5F6FA"
        )

        search_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 15)
        )

        tk.Label(
            search_frame,
            text="Search:",
            bg="#F5F6FA",
            fg="#172033",
            font=("Segoe UI", 10)
        ).pack(
            side="left",
            padx=(0, 8)
        )

        self.search_entry = tk.Entry(
            search_frame,
            font=("Segoe UI", 10),
            width=35
        )

        self.search_entry.pack(
            side="left",
            ipady=6
        )

        # Search button
        tk.Button(
            search_frame,
            text="Search",
            bg="#4B74D9",
            fg="white",
            activebackground="#365DB5",
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10),
            cursor="hand2",
            command=self.search_customer
        ).pack(
            side="left",
            padx=8,
            ipadx=10,
            ipady=5
        )

        # Show All button
        tk.Button(
            search_frame,
            text="Show All",
            bg="#6B7280",
            fg="white",
            activebackground="#4B5563",
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10),
            cursor="hand2",
            command=self.load_customers
        ).pack(
            side="left",
            ipadx=10,
            ipady=5
        )

        # Add Customer button
        tk.Button(
            search_frame,
            text="+ Add Customer",
            bg="#E87524",
            fg="white",
            activebackground="#C95F17",
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=self.add_customer
        ).pack(
            side="right",
            ipadx=10,
            ipady=5
        )

        # --------------------------------------
        # Table Frame
        # --------------------------------------

        table_frame = tk.Frame(
            self.frame,
            bg="white"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 15)
        )

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical"
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # Treeview
        self.customer_table = ttk.Treeview(
            table_frame,
            columns=(
                "Customer_id",
                "full_name",
                "phone",
                "CreatedAt"
            ),
            show="headings",
            yscrollcommand=scrollbar.set
        )

        self.customer_table.pack(
            fill="both",
            expand=True
        )

        scrollbar.config(
            command=self.customer_table.yview
        )

        # Table headings
        self.customer_table.heading(
            "Customer_id",
            text="ID"
        )

        self.customer_table.heading(
            "full_name",
            text="Full Name"
        )

        self.customer_table.heading(
            "phone",
            text="phone"
        )

        self.customer_table.heading(
            "CreatedAt",
            text="Created At"
        )

        # Column widths
        self.customer_table.column(
            "Customer_id",
            width=70,
            anchor="center"
        )

        self.customer_table.column(
            "full_name",
            width=250
        )

        self.customer_table.column(
            "phone",
            width=180
        )

        self.customer_table.column(
            "CreatedAt",
            width=180
        )

        # --------------------------------------
        # Bottom Buttons
        # --------------------------------------

        button_frame = tk.Frame(
            self.frame,
            bg="#F5F6FA"
        )

        button_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 25)
        )

        # Edit button
        tk.Button(
            button_frame,
            text="Edit Customer",
            bg="#4B74D9",
            fg="white",
            activebackground="#365DB5",
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10),
            cursor="hand2",
            command=self.edit_customer
        ).pack(
            side="left",
            ipadx=12,
            ipady=6
        )

        # Delete button
        tk.Button(
            button_frame,
            text="Delete Customer",
            bg="#D84A4A",
            fg="white",
            activebackground="#B83232",
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10),
            cursor="hand2",
            command=self.delete_customer
        ).pack(
            side="left",
            padx=10,
            ipadx=12,
            ipady=6
        )

   
    # LOAD CUSTOMERS


    def load_customers(self):

        # Clear table
        for row in self.customer_table.get_children():

            self.customer_table.delete(row)

        try:

            connection = get_connection()

            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    Customer_id,
                    full_name,
                    phone,
                    CreatedAt
                FROM Customers
                ORDER BY Customer_id DESC
            """)

            rows = cursor.fetchall()

            for row in rows:

                self.customer_table.insert(
        "",
        "end",
        values=(
            row[0],
            row[1],
            row[2],
            row[3]
        )
    )

            cursor.close()
            connection.close()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    # SEARCH CUSTOMER

    def search_customer(self):

        search_text = self.search_entry.get().strip()

        if search_text == "":
            self.load_customers()
            return

        # Clear table
        for row in self.customer_table.get_children():

            self.customer_table.delete(row)

        try:

            connection = get_connection()

            cursor = connection.cursor()

            search_value = "%" + search_text + "%"

            cursor.execute("""
                SELECT
                    Customer_id,
                    full_name,
                    phone,
                    CreatedAt
                FROM Customers
                WHERE full_name LIKE ?
                   OR phone LIKE ?
                ORDER BY Customer_id DESC
            """, (
                search_value,
                search_value
            ))

            rows = cursor.fetchall()

            for row in rows:

                 self.customer_table.insert(
        "",
        "end",
        values=(
            row[0],
            row[1],
            row[2],
            row[3]
        )
    )

            cursor.close()
            connection.close()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    # ==========================================
    # ADD CUSTOMER
    # ==========================================

    def add_customer(self):

        # Create popup window
        add_window = tk.Toplevel(
            self.frame
        )

        add_window.title(
            "Add Customer"
        )

        add_window.geometry(
            "450x300"
        )

        add_window.resizable(
            False,
            False
        )

        add_window.transient(
            self.frame.winfo_toplevel()
        )

        # --------------------------------------
        # Title
        # --------------------------------------

        tk.Label(
            add_window,
            text="Add Customer",
            font=("Segoe UI", 18, "bold"),
            fg="#172033"
        ).pack(
            pady=(25, 20)
        )

        # --------------------------------------
        # Full Name
        # --------------------------------------

        tk.Label(
            add_window,
            text="Full Name",
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            padx=40
        )

        name_entry = tk.Entry(
            add_window,
            font=("Segoe UI", 10)
        )

        name_entry.pack(
            fill="x",
            padx=40,
            pady=(5, 15),
            ipady=6
        )

        # --------------------------------------
        # phone
        # --------------------------------------

        tk.Label(
            add_window,
            text="phone",
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            padx=40
        )

        phone_entry = tk.Entry(
            add_window,
            font=("Segoe UI", 10)
        )

        phone_entry.pack(
            fill="x",
            padx=40,
            pady=(5, 20),
            ipady=6
        )

        # --------------------------------------
        # Save Customer
        # --------------------------------------

        def save_customer():

            full_name = name_entry.get().strip()
            phone = phone_entry.get().strip()

            # Validation
            if full_name == "":
                messagebox.showwarning(
                    "Validation",
                    "Please enter customer name."
                )
                name_entry.focus()
                return

            if phone == "":
                messagebox.showwarning(
                    "Validation",
                    "Please enter phone number."
                )
                phone_entry.focus()
                return

            try:

                connection = get_connection()

                cursor = connection.cursor()

                cursor.execute("""
                    INSERT INTO Customers
                    (
                        full_name,
                        phone
                    )
                    VALUES (?, ?)
                """, (
                    full_name,
                    phone
                ))

                connection.commit()

                cursor.close()
                connection.close()

                messagebox.showinfo(
                    "Success",
                    "Customer added successfully."
                )

                add_window.destroy()

                # Refresh table
                self.load_customers()

            except Exception as e:

                messagebox.showerror(
                    "Database Error",
                    str(e)
                )

        # --------------------------------------
        # Buttons
        # --------------------------------------

        button_frame = tk.Frame(
            add_window
        )

        button_frame.pack()

        tk.Button(
            button_frame,
            text="Save",
            bg="#1F9D68",
            fg="white",
            activebackground="#167A50",
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=save_customer
        ).pack(
            side="left",
            ipadx=20,
            ipady=6
        )

        tk.Button(
            button_frame,
            text="Cancel",
            bg="#6B7280",
            fg="white",
            activebackground="#4B5563",
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10),
            cursor="hand2",
            command=add_window.destroy
        ).pack(
            side="left",
            padx=10,
            ipadx=15,
            ipady=6
        )

        name_entry.focus()

    # ==========================================
    # EDIT CUSTOMER
    # ==========================================

    def edit_customer(self):

        selected = self.customer_table.selection()

        if not selected:

            messagebox.showwarning(
                "Select Customer",
                "Please select a customer first."
            )

            return

        # Get selected row
        values = self.customer_table.item(
            selected[0],
            "values"
        )

        customer_id = values[0]
        old_name = values[1]
        old_phone = values[2]

        # --------------------------------------
        # Edit Window
        # --------------------------------------

        edit_window = tk.Toplevel(
            self.frame
        )

        edit_window.title(
            "Edit Customer"
        )

        edit_window.geometry(
            "450x300"
        )

        edit_window.resizable(
            False,
            False
        )

        # --------------------------------------
        # Title
        # --------------------------------------

        tk.Label(
            edit_window,
            text="Edit Customer",
            font=("Segoe UI", 18, "bold"),
            fg="#172033"
        ).pack(
            pady=(25, 20)
        )

        # --------------------------------------
        # Name
        # --------------------------------------

        tk.Label(
            edit_window,
            text="Full Name",
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            padx=40
        )

        name_entry = tk.Entry(
            edit_window,
            font=("Segoe UI", 10)
        )

        name_entry.pack(
            fill="x",
            padx=40,
            pady=(5, 15),
            ipady=6
        )

        name_entry.insert(
            0,
            old_name
        )

        # --------------------------------------
        # phone
        # --------------------------------------

        tk.Label(
            edit_window,
            text="phone",
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            padx=40
        )

        phone_entry = tk.Entry(
            edit_window,
            font=("Segoe UI", 10)
        )

        phone_entry.pack(
            fill="x",
            padx=40,
            pady=(5, 20),
            ipady=6
        )

        phone_entry.insert(
            0,
            old_phone
        )

        # --------------------------------------
        # Update Customer
        # --------------------------------------

        def update_customer():

            full_name = name_entry.get().strip()
            phone = phone_entry.get().strip()

            if full_name == "":
                messagebox.showwarning(
                    "Validation",
                    "Please enter customer name."
                )
                return

            if phone == "":
                messagebox.showwarning(
                    "Validation",
                    "Please enter phone number."
                )
                return

            try:

                connection = get_connection()

                cursor = connection.cursor()

                cursor.execute("""
                    UPDATE Customers
                    SET
                        full_name = ?,
                        phone = ?
                    WHERE customer_id = ?
                """, (
                    full_name,
                    phone,
                    customer_id
                ))

                connection.commit()

                cursor.close()
                connection.close()

                messagebox.showinfo(
                    "Success",
                    "Customer updated successfully."
                )

                edit_window.destroy()

                self.load_customers()

            except Exception as e:

                messagebox.showerror(
                    "Database Error",
                    str(e)
                )

        # --------------------------------------
        # Buttons
        # --------------------------------------

        button_frame = tk.Frame(
            edit_window
        )

        button_frame.pack()

        tk.Button(
            button_frame,
            text="Update",
            bg="#4B74D9",
            fg="white",
            activebackground="#365DB5",
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=update_customer
        ).pack(
            side="left",
            ipadx=20,
            ipady=6
        )

        tk.Button(
            button_frame,
            text="Cancel",
            bg="#6B7280",
            fg="white",
            activebackground="#4B5563",
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10),
            cursor="hand2",
            command=edit_window.destroy
        ).pack(
            side="left",
            padx=10,
            ipadx=15,
            ipady=6
        )

        name_entry.focus()

    # ==========================================
    # DELETE CUSTOMER
    # ==========================================

    def delete_customer(self):

        selected = self.customer_table.selection()

        if not selected:

            messagebox.showwarning(
                "Select Customer",
                "Please select a customer first."
            )

            return

        # Get selected customer
        values = self.customer_table.item(
            selected[0],
            "values"
        )

        customer_id = values[0]
        customer_name = values[1]

        # Confirm deletion
        result = messagebox.askyesno(
            "Delete Customer",
            "Are you sure you want to delete\n"
            + customer_name
            + "?"
        )

        if not result:
            return

        try:

            connection = get_connection()

            cursor = connection.cursor()

            cursor.execute("""
                DELETE FROM Customers
                WHERE customer_id = ?
            """, (
                customer_id,
            ))

            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Customer deleted successfully."
            )

            self.load_customers()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )