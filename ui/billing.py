import tkinter as tk
from tkinter import ttk, messagebox

from database.connection import get_connection


class BillingPage:

    def __init__(self, parent):

        self.parent = parent

        self.selected_order_id = None
        self.order_list = []

        self.create_widgets()
        self.load_orders()

    # --------------------------------------------------
    # CREATE WIDGETS
    # --------------------------------------------------

    def create_widgets(self):

        title_label = tk.Label(
            self.parent,
            text="Billing",
            font=("Arial", 20, "bold")
        )

        title_label.pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        # ----------------------------------------------
        # ORDER SECTION
        # ----------------------------------------------

        order_frame = tk.Frame(
            self.parent,
            bd=1,
            relief="solid"
        )

        order_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        tk.Label(
            order_frame,
            text="Served Order:",
            font=("Arial", 11)
        ).pack(
            side="left",
            padx=10,
            pady=10
        )

        self.order_combo = ttk.Combobox(
            order_frame,
            state="readonly",
            width=40
        )

        self.order_combo.pack(
            side="left",
            padx=10,
            pady=10
        )

        self.order_combo.bind(
            "<<ComboboxSelected>>",
            self.load_order_details
        )

        refresh_button = tk.Button(
            order_frame,
            text="Refresh",
            command=self.load_orders
        )

        refresh_button.pack(
            side="left",
            padx=10
        )

        # ----------------------------------------------
        # ORDER ITEMS
        # ----------------------------------------------

        items_frame = tk.Frame(
            self.parent
        )

        items_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        tk.Label(
            items_frame,
            text="Order Items",
            font=("Arial", 14, "bold")
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        columns = (
            "ItemName",
            "Price",
            "Quantity",
            "Amount"
        )

        self.items_tree = ttk.Treeview(
            items_frame,
            columns=columns,
            show="headings"
        )

        self.items_tree.heading(
            "ItemName",
            text="Item Name"
        )

        self.items_tree.heading(
            "Price",
            text="Price"
        )

        self.items_tree.heading(
            "Quantity",
            text="Quantity"
        )

        self.items_tree.heading(
            "Amount",
            text="Amount"
        )

        self.items_tree.column(
            "ItemName",
            width=250
        )

        self.items_tree.column(
            "Price",
            width=100
        )

        self.items_tree.column(
            "Quantity",
            width=100
        )

        self.items_tree.column(
            "Amount",
            width=120
        )

        self.items_tree.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------------------
        # BILLING SECTION
        # ----------------------------------------------

        billing_frame = tk.Frame(
            self.parent,
            bd=1,
            relief="solid"
        )

        billing_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        # Subtotal

        tk.Label(
            billing_frame,
            text="Subtotal:",
            font=("Arial", 11)
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=8,
            sticky="w"
        )

        self.subtotal_label = tk.Label(
            billing_frame,
            text="0.00",
            font=("Arial", 11, "bold")
        )

        self.subtotal_label.grid(
            row=0,
            column=1,
            padx=10,
            pady=8,
            sticky="w"
        )

        # Tax Percentage

        tk.Label(
            billing_frame,
            text="Tax (%):",
            font=("Arial", 11)
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=8,
            sticky="w"
        )

        self.tax_entry = tk.Entry(
            billing_frame,
            width=15
        )

        self.tax_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=8,
            sticky="w"
        )

        self.tax_entry.insert(
            0,
            "0"
        )

        # Discount Amount

        tk.Label(
            billing_frame,
            text="Discount Amount:",
            font=("Arial", 11)
        ).grid(
            row=2,
            column=0,
            padx=10,
            pady=8,
            sticky="w"
        )

        self.discount_entry = tk.Entry(
            billing_frame,
            width=15
        )

        self.discount_entry.grid(
            row=2,
            column=1,
            padx=10,
            pady=8,
            sticky="w"
        )

        self.discount_entry.insert(
            0,
            "0"
        )

        # Tax Amount

        tk.Label(
            billing_frame,
            text="Tax Amount:",
            font=("Arial", 11)
        ).grid(
            row=3,
            column=0,
            padx=10,
            pady=8,
            sticky="w"
        )

        self.tax_amount_label = tk.Label(
            billing_frame,
            text="0.00",
            font=("Arial", 11, "bold")
        )

        self.tax_amount_label.grid(
            row=3,
            column=1,
            padx=10,
            pady=8,
            sticky="w"
        )

        # Discount Amount Display

        tk.Label(
            billing_frame,
            text="Discount Amount:",
            font=("Arial", 11)
        ).grid(
            row=4,
            column=0,
            padx=10,
            pady=8,
            sticky="w"
        )

        self.discount_amount_label = tk.Label(
            billing_frame,
            text="0.00",
            font=("Arial", 11, "bold")
        )

        self.discount_amount_label.grid(
            row=4,
            column=1,
            padx=10,
            pady=8,
            sticky="w"
        )

        # Total

        tk.Label(
            billing_frame,
            text="Total:",
            font=("Arial", 13, "bold")
        ).grid(
            row=5,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.total_label = tk.Label(
            billing_frame,
            text="0.00",
            font=("Arial", 13, "bold")
        )

        self.total_label.grid(
            row=5,
            column=1,
            padx=10,
            pady=10,
            sticky="w"
        )

        # ----------------------------------------------
        # BUTTONS
        # ----------------------------------------------

        button_frame = tk.Frame(
            billing_frame
        )

        button_frame.grid(
            row=6,
            column=0,
            columnspan=2,
            pady=15
        )

        calculate_button = tk.Button(
            button_frame,
            text="Calculate Total",
            width=18,
            command=self.calculate_total
        )

        calculate_button.pack(
            side="left",
            padx=10
        )

        create_bill_button = tk.Button(
            button_frame,
            text="Create Bill",
            width=18,
            command=self.create_bill
        )

        create_bill_button.pack(
            side="left",
            padx=10
        )

    # --------------------------------------------------
    # LOAD SERVED ORDERS
    # --------------------------------------------------

    def load_orders(self):

        self.order_combo["values"] = []

        self.order_list = []

        self.selected_order_id = None

        # Keep dropdown empty by default
        self.order_combo.set("")

        # Clear order items
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
# Reset
        self.subtotal_label.config(text="0.00")
        self.tax_amount_label.config(text="0.00")
        self.discount_amount_label.config(text="0.00")
        self.total_label.config(text="0.00")

        # Clear tax and discount input fields
        self.tax_entry.delete(0, "end")
        self.tax_entry.insert(0, "0")

        self.discount_entry.delete(0, "end")
        self.discount_entry.insert(0, "0")

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    o.OrderID,
                    c.full_name,
                    o.OrderDate,
                    o.TotalAmount
                FROM Orders o
                INNER JOIN Customers c
                    ON o.customer_id = c.customer_id
                WHERE o.Status = 'Served'
                ORDER BY o.OrderID DESC
            """)

            rows = cursor.fetchall()

            connection.close()

            display_list = []

            for row in rows:

                order_id = row[0]
                customer_name = row[1]
                total_amount = row[3]

                display_text = (
                    f"Order #{order_id} - "
                    f"{customer_name} - "
                    f"₹{float(total_amount):.2f}"
                )

                display_list.append(
                    display_text
                )

                self.order_list.append(
                    order_id
                )

            self.order_combo["values"] = display_list

            # Do NOT automatically select first order

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # --------------------------------------------------
    # LOAD ORDER DETAILS
    # --------------------------------------------------

    def load_order_details(self, event=None):

        selected = self.order_combo.current()

        if selected < 0:
            return

        self.selected_order_id = self.order_list[selected]

        for item in self.items_tree.get_children():
            self.items_tree.delete(item)

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    m.ItemName,
                    oi.Price,
                    oi.Quantity,
                    oi.Amount
                FROM OrderItems oi
                INNER JOIN MenuItems m
                    ON oi.MenuItem_id = m.MenuItem_id
                WHERE oi.OrderID = ?
            """, (
                self.selected_order_id,
            ))

            rows = cursor.fetchall()

            connection.close()

            subtotal = 0

            for row in rows:

                item_name = row[0]
                price = float(row[1])
                quantity = row[2]
                amount = float(row[3])

                subtotal += amount

                self.items_tree.insert(
                    "",
                    "end",
                    values=(
                        item_name,
                        f"{price:.2f}",
                        quantity,
                        f"{amount:.2f}"
                    )
                )

            self.subtotal_label.config(
                text=f"{subtotal:.2f}"
            )

            self.calculate_total()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # --------------------------------------------------
    # CALCULATE TOTAL
    # --------------------------------------------------

    def calculate_total(self):

        try:

            subtotal = float(
                self.subtotal_label.cget("text")
            )

            tax_percent = float(
                self.tax_entry.get()
            )

            discount_amount = float(
                self.discount_entry.get()
            )

            if tax_percent < 0:

                messagebox.showwarning(
                    "Warning",
                    "Tax percentage cannot be negative."
                )

                return

            if discount_amount < 0:

                messagebox.showwarning(
                    "Warning",
                    "Discount cannot be negative."
                )

                return

            if discount_amount > subtotal:

                messagebox.showwarning(
                    "Warning",
                    "Discount cannot be greater than subtotal."
                )

                return

            # Tax is percentage
            tax_amount = (
                subtotal * tax_percent / 100
            )

            # Discount is fixed amount
            total = (
                subtotal
                + tax_amount
                - discount_amount
            )

            self.tax_amount_label.config(
                text=f"{tax_amount:.2f}"
            )

            self.discount_amount_label.config(
                text=f"{discount_amount:.2f}"
            )

            self.total_label.config(
                text=f"{total:.2f}"
            )

        except ValueError:

            messagebox.showwarning(
                "Warning",
                "Tax percentage and discount must be numbers."
            )

    # --------------------------------------------------
    # CREATE BILL
    # --------------------------------------------------

    def create_bill(self):

    # Check whether an order is selected
        if self.selected_order_id is None:

            messagebox.showwarning(
                "Warning",
                "Please select an order."
            )

            return

        # Get billing values
        try:

            subtotal = float(
                self.subtotal_label.cget("text")
            )

            tax_percent = float(
                self.tax_entry.get()
            )

            discount_amount = float(
                self.discount_entry.get()
            )

            # Tax cannot be negative
            if tax_percent < 0:

                messagebox.showwarning(
                    "Warning",
                    "Tax percentage cannot be negative."
                )

                return

            # Discount cannot be negative
            if discount_amount < 0:

                messagebox.showwarning(
                    "Warning",
                    "Discount cannot be negative."
                )

                return

            # Discount cannot be greater than subtotal
            if discount_amount > subtotal:

                messagebox.showwarning(
                    "Warning",
                    "Discount cannot be greater than subtotal."
                )

                return

            # Calculate tax amount
            # Tax is percentage
            tax_amount = subtotal * tax_percent / 100

            # Calculate final total
            total = (
                subtotal
                + tax_amount
                - discount_amount
            )

        except ValueError:

            messagebox.showwarning(
                "Warning",
                "Please enter valid tax percentage and discount amount."
            )

            return

        # Save bill into database
        try:

            connection = get_connection()
            cursor = connection.cursor()

            # Check whether bill already exists
            cursor.execute("""
                SELECT BillID
                FROM Bills
                WHERE OrderID = ?
            """, (
                self.selected_order_id,
            ))

            existing_bill = cursor.fetchone()

            if existing_bill:

                connection.close()

                messagebox.showwarning(
                    "Warning",
                    "A bill already exists for this order."
                )

                return

            # Create bill
            cursor.execute("""
                INSERT INTO Bills
                (
                    OrderID,
                    SubTotal,
                    TaxAmount,
                    DiscountAmount,
                    TotalAmount
                )
                OUTPUT INSERTED.BillID
                VALUES (?, ?, ?, ?, ?)
            """, (
                self.selected_order_id,
                subtotal,
                tax_amount,
                discount_amount,
                total
            ))

            # Get newly created BillID
            bill_id = cursor.fetchone()[0]

            # Save changes
            connection.commit()

            # Close connection
            connection.close()

            # Show success message
            messagebox.showinfo(
                "Success",
                f"Bill #{bill_id} created successfully."
            )

            # Refresh served orders
            # The billed order will disappear
            self.load_orders()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )