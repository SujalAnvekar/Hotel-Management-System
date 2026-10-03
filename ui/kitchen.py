import tkinter as tk
from tkinter import ttk, messagebox

from database.connection import get_connection


class KitchenPage:

    def __init__(self, parent):

        self.parent = parent

        self.create_widgets()
        self.load_orders()

    def create_widgets(self):

        title = tk.Label(
            self.parent,
            text="Kitchen",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=15)

        button_frame = tk.Frame(self.parent)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Refresh",
            command=self.load_orders
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Start Preparing",
            command=self.start_preparing
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Mark Ready",
            command=self.mark_ready
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Mark Served",
            command=self.mark_served
        ).pack(side="left", padx=5)

        table_frame = tk.Frame(self.parent)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "OrderID",
            "Customer",
            "OrderDate",
            "Status",
            "Total"
        )

        self.order_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.order_table.heading(
            "OrderID",
            text="Order ID"
        )

        self.order_table.heading(
            "Customer",
            text="Customer"
        )

        self.order_table.heading(
            "OrderDate",
            text="Order Date"
        )

        self.order_table.heading(
            "Status",
            text="Status"
        )

        self.order_table.heading(
            "Total",
            text="Total"
        )

        self.order_table.column(
            "OrderID",
            width=80
        )

        self.order_table.column(
            "Customer",
            width=200
        )

        self.order_table.column(
            "OrderDate",
            width=180
        )

        self.order_table.column(
            "Status",
            width=120
        )

        self.order_table.column(
            "Total",
            width=120
        )

        self.order_table.pack(
            fill="both",
            expand=True
        )

    def load_orders(self):

        for item in self.order_table.get_children():
            self.order_table.delete(item)

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    o.OrderID,
                    c.full_name,
                    o.OrderDate,
                    o.Status,
                    o.TotalAmount
                FROM Orders o
                INNER JOIN Customers c
                    ON o.customer_id = c.customer_id
                WHERE o.Status IN
                    ('Pending', 'Preparing', 'Ready')
                ORDER BY o.OrderDate
            """)

            rows = cursor.fetchall()

            connection.close()

            for row in rows:

                self.order_table.insert(
                    "",
                    "end",
                    values=(
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                        f"{float(row[4]):.2f}"
                    )
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    def get_selected_order(self):

        selected = self.order_table.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select an order."
            )

            return None

        values = self.order_table.item(
            selected[0],
            "values"
        )

        return values

    def update_status(self, new_status):

        order = self.get_selected_order()

        if order is None:
            return

        order_id = order[0]

        try:

            connection = get_connection()
            cursor = connection.cursor()

            # Update order status
            cursor.execute("""
                UPDATE Orders
                SET Status = ?
                WHERE OrderID = ?
            """, (
                new_status,
                order_id
            ))

            # Store status history
            cursor.execute("""
                INSERT INTO KitchenHistory
                (
                    OrderID,
                    Status
                )
                VALUES (?, ?)
            """, (
                order_id,
                new_status
            ))

            connection.commit()
            connection.close()

            self.load_orders()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

            order = self.get_selected_order()

            if order is None:
                return

            order_id = order[0]

        try:

                connection = get_connection()
                cursor = connection.cursor()

                cursor.execute("""
                    UPDATE Orders
                    SET Status = ?
                    WHERE OrderID = ?
                """, (
                    new_status,
                    order_id
                ))

                connection.commit()
                connection.close()

                self.load_orders()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    def start_preparing(self):

        self.update_status("Preparing")

    def mark_ready(self):

        self.update_status("Ready")

    def mark_served(self):

        self.update_status("Served")