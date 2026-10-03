import tkinter as tk
from tkinter import ttk, messagebox

from database.connection import get_connection


class BillingPage:

    def __init__(self, parent):

        self.parent = parent
        self.selected_order_id = None

        self.create_widgets()
        self.load_orders()

    def create_widgets(self):

        title = tk.Label(
            self.parent,
            text="Billing",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=15)

        # Orders section
        order_frame = tk.Frame(self.parent)
        order_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(
            order_frame,
            text="Served Order:"
        ).pack(side="left", padx=5)

        self.order_combo = ttk.Combobox(
            order_frame,
            state="readonly",
            width=35
        )
        self.order_combo.pack(side="left", padx=5)

        tk.Button(
            order_frame,
            text="Load Order",
            command=self.load_order_details
        ).pack(side="left", padx=10)

        # Items table
        table_frame = tk.Frame(self.parent)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "ItemName",
            "Price",
            "Quantity",
            "Amount"
        )

        self.item_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.item_table.heading(
            "ItemName",
            text="Item Name"
        )

        self.item_table.heading(
            "Price",
            text="Price"
        )

        self.item_table.heading(
            "Quantity",
            text="Quantity"
        )

        self.item_table.heading(
            "Amount",
            text="Amount"
        )

        self.item_table.column(
            "ItemName",
            width=250
        )

        self.item_table.column(
            "Price",
            width=100
        )

        self.item_table.column(
            "Quantity",
            width=100
        )

        self.item_table.column(
            "Amount",
            width=120
        )

        self.item_table.pack(
            fill="both",
            expand=True
        )

        # Bill section
        bill_frame = tk.Frame(self.parent)
        bill_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        tk.Label(
            bill_frame,
            text="Subtotal:"
        ).grid(row=0, column=0, sticky="e", padx=5, pady=5)

        self.subtotal_label = tk.Label(
            bill_frame,
            text="0.00"
        )
        self.subtotal_label.grid(
            row=0,
            column=1,
            sticky="w",
            padx=5
        )

        tk.Label(
            bill_frame,
            text="Tax:"
        ).grid(row=1, column=0, sticky="e", padx=5, pady=5)

        self.tax_entry = tk.Entry(
            bill_frame,
            width=15
        )
        self.tax_entry.grid(
            row=1,
            column=1,
            sticky="w",
            padx=5
        )
        self.tax_entry.insert(0, "0")

        tk.Label(
            bill_frame,
            text="Discount:"
        ).grid(row=2, column=0, sticky="e", padx=5, pady=5)

        self.discount_entry = tk.Entry(
            bill_frame,
            width=15
        )
        self.discount_entry.grid(
            row=2,
            column=1,
            sticky="w",
            padx=5
        )
        self.discount_entry.insert(0, "0")

        tk.Label(
            bill_frame,
            text="Total:",
            font=("Arial", 14, "bold")
        ).grid(
            row=3,
            column=0,
            sticky="e",
            padx=5,
            pady=8
        )

        self.total_label = tk.Label(
            bill_frame,
            text="0.00",
            font=("Arial", 14, "bold")
        )
        self.total_label.grid(
            row=3,
            column=1,
            sticky="w",
            padx=5
        )

        tk.Button(
            bill_frame,
            text="Calculate",
            command=self.calculate_total
        ).grid(
            row=4,
            column=0,
            padx=5,
            pady=10
        )

        tk.Button(
            bill_frame,
            text="Create Bill",
            command=self.create_bill
        ).grid(
            row=4,
            column=1,
            padx=5,
            pady=10,
            sticky="w"
        )

    def load_orders(self):

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    o.OrderID,
                    c.full_name,
                    o.TotalAmount
                FROM Orders o
                INNER JOIN Customers c
                    ON o.customer_id = c.customer_id
                WHERE o.Status = 'Served'
                ORDER BY o.OrderDate
            """)

            rows = cursor.fetchall()

            connection.close()

            self.order_list = rows

            order_names = []

            for row in rows:

                order_names.append(
                    f"Order #{row[0]} - {row[1]}"
                )

            self.order_combo["values"] = order_names

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    def load_order_details(self):

        order_index = self.order_combo.current()

        if order_index == -1:

            messagebox.showwarning(
                "Warning",
                "Please select an order."
            )

            return

        order = self.order_list[order_index]

        self.selected_order_id = order[0]

        for item in self.item_table.get_children():
            self.item_table.delete(item)

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
                    ON oi.menuItem_id = m.menuItem_id
                WHERE oi.OrderID = ?
            """, (
                self.selected_order_id,
            ))

            rows = cursor.fetchall()

            connection.close()

            subtotal = 0

            for row in rows:

                subtotal += float(row[3])

                self.item_table.insert(
                    "",
                    "end",
                    values=(
                        row[0],
                        f"{float(row[1]):.2f}",
                        row[2],
                        f"{float(row[3]):.2f}"
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

    def calculate_total(self):

        try:

            subtotal = float(
                self.subtotal_label.cget("text")
            )

            tax = float(
                self.tax_entry.get()
            )

            discount = float(
                self.discount_entry.get()
            )

            total = subtotal + tax - discount

            if total < 0:
                total = 0

            self.total_label.config(
                text=f"{total:.2f}"
            )

        except ValueError:

            messagebox.showwarning(
                "Warning",
                "Tax and discount must be numbers."
            )

    def create_bill(self):

        if self.selected_order_id is None:

            messagebox.showwarning(
                "Warning",
                "Please select an order."
            )

            return

        try:

            subtotal = float(
                self.subtotal_label.cget("text")
            )

            tax = float(
                self.tax_entry.get()
            )

            discount = float(
                self.discount_entry.get()
            )

            total = subtotal + tax - discount

            if total < 0:
                total = 0

        except ValueError:

            messagebox.showwarning(
                "Warning",
                "Please enter valid tax and discount."
            )

            return

        try:

            connection = get_connection()
            cursor = connection.cursor()

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
                tax,
                discount,
                total
            ))

            bill_id = cursor.fetchone()[0]

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Success",
                f"Bill #{bill_id} created successfully."
            )

            self.load_orders()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )