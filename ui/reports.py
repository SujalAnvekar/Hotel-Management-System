import tkinter as tk
from tkinter import ttk, messagebox

from database.connection import get_connection


class ReportsPage:

    def __init__(self, parent):

        self.parent = parent

        self.create_widgets()
        self.load_sales_report()

    def create_widgets(self):

        title = tk.Label(
            self.parent,
            text="Reports",
            font=("Arial", 20, "bold")
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=20
        )

        # Report buttons
        button_frame = tk.Frame(
            self.parent
        )

        button_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        tk.Button(
            button_frame,
            text="Sales Report",
            width=15,
            command=self.load_sales_report
        ).pack(
            side="left",
            padx=5
        )

        # Summary
        summary_frame = tk.Frame(
            self.parent
        )

        summary_frame.pack(
            fill="x",
            padx=20,
            pady=15
        )

        self.total_bills_label = tk.Label(
            summary_frame,
            text="Total Bills: 0",
            font=("Arial", 12, "bold")
        )

        self.total_bills_label.pack(
            side="left",
            padx=20
        )

        self.total_sales_label = tk.Label(
            summary_frame,
            text="Total Sales: ₹0.00",
            font=("Arial", 12, "bold")
        )

        self.total_sales_label.pack(
            side="left",
            padx=20
        )

        # Sales table
        table_frame = tk.Frame(
            self.parent
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "BillID",
            "OrderID",
            "BillDate",
            "SubTotal",
            "TaxAmount",
            "DiscountAmount",
            "TotalAmount"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.tree.heading(
            "BillID",
            text="Bill ID"
        )

        self.tree.heading(
            "OrderID",
            text="Order ID"
        )

        self.tree.heading(
            "BillDate",
            text="Bill Date"
        )

        self.tree.heading(
            "SubTotal",
            text="Subtotal"
        )

        self.tree.heading(
            "TaxAmount",
            text="Tax"
        )

        self.tree.heading(
            "DiscountAmount",
            text="Discount"
        )

        self.tree.heading(
            "TotalAmount",
            text="Total"
        )

        self.tree.column(
            "BillID",
            width=70
        )

        self.tree.column(
            "OrderID",
            width=80
        )

        self.tree.column(
            "BillDate",
            width=150
        )

        self.tree.column(
            "SubTotal",
            width=100
        )

        self.tree.column(
            "TaxAmount",
            width=100
        )

        self.tree.column(
            "DiscountAmount",
            width=100
        )

        self.tree.column(
            "TotalAmount",
            width=120
        )

        self.tree.pack(
            fill="both",
            expand=True
        )

    def load_sales_report(self):

        # Clear old records
        for item in self.tree.get_children():

            self.tree.delete(item)

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    BillID,
                    OrderID,
                    BillDate,
                    SubTotal,
                    TaxAmount,
                    DiscountAmount,
                    TotalAmount
                FROM Bills
                ORDER BY BillID DESC
            """)

            rows = cursor.fetchall()

            connection.close()

            total_bills = 0
            total_sales = 0

            for row in rows:

                bill_id = row[0]
                order_id = row[1]
                bill_date = row[2]
                subtotal = float(row[3])
                tax_amount = float(row[4])
                discount_amount = float(row[5])
                total_amount = float(row[6])

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        bill_id,
                        order_id,
                        bill_date,
                        f"₹{subtotal:.2f}",
                        f"₹{tax_amount:.2f}",
                        f"₹{discount_amount:.2f}",
                        f"₹{total_amount:.2f}"
                    )
                )

                total_bills += 1
                total_sales += total_amount

            self.total_bills_label.config(
                text=f"Total Bills: {total_bills}"
            )

            self.total_sales_label.config(
                text=f"Total Sales: ₹{total_sales:.2f}"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )