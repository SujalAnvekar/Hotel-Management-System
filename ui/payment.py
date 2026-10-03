import tkinter as tk
from tkinter import ttk, messagebox

from database.connection import get_connection


class PaymentPage:

    def __init__(self, parent):

        self.parent = parent

        self.bill_list = []
        self.selected_bill_id = None

        self.create_widgets()
        self.load_bills()

    def create_widgets(self):

        title = tk.Label(
            self.parent,
            text="Payments",
            font=("Arial", 20, "bold")
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=20
        )

        # Bill selection
        bill_frame = tk.Frame(self.parent)

        bill_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        tk.Label(
            bill_frame,
            text="Select Bill"
        ).pack(
            side="left",
            padx=5
        )

        self.bill_combo = ttk.Combobox(
            bill_frame,
            state="readonly",
            width=40
        )

        self.bill_combo.pack(
            side="left",
            padx=10
        )

        self.bill_combo.bind(
            "<<ComboboxSelected>>",
            self.load_bill
        )

        # Amount
        tk.Label(
            self.parent,
            text="Amount"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        self.amount_entry = tk.Entry(
            self.parent,
            width=30
        )

        self.amount_entry.pack(
            anchor="w",
            padx=20
        )

        # Payment Method
        tk.Label(
            self.parent,
            text="Payment Method"
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 5)
        )

        self.method_combo = ttk.Combobox(
            self.parent,
            values=[
                "Cash",
                "Card",
                "UPI"
            ],
            state="readonly",
            width=27
        )

        self.method_combo.pack(
            anchor="w",
            padx=20
        )

        # Buttons
        button_frame = tk.Frame(self.parent)

        button_frame.pack(
            anchor="w",
            padx=20,
            pady=20
        )

        tk.Button(
            button_frame,
            text="Refresh",
            width=12,
            command=self.load_bills
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="Make Payment",
            width=15,
            command=self.make_payment
        ).pack(
            side="left",
            padx=5
        )

    def load_bills(self):

        self.bill_combo["values"] = []

        self.bill_list = []
        self.selected_bill_id = None

        self.bill_combo.set("")

        self.amount_entry.delete(
            0,
            "end"
        )

        self.method_combo.set("")

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    b.BillID,
                    o.OrderID,
                    c.full_name,
                    b.TotalAmount
                FROM Bills b
                INNER JOIN Orders o
                    ON b.OrderID = o.OrderID
                INNER JOIN Customers c
                    ON o.customer_id = c.customer_id
                LEFT JOIN Payments p
                    ON b.BillID = p.BillID
                WHERE p.PaymentID IS NULL
                ORDER BY b.BillID DESC
            """)

            rows = cursor.fetchall()

            connection.close()

            display_list = []

            for row in rows:

                bill_id = row[0]
                order_id = row[1]
                customer_name = row[2]
                total_amount = float(row[3])

                display_text = (
                    f"Bill #{bill_id} - "
                    f"Order #{order_id} - "
                    f"{customer_name} - "
                    f"₹{total_amount:.2f}"
                )

                display_list.append(display_text)

                self.bill_list.append(
                    {
                        "bill_id": bill_id,
                        "amount": total_amount
                    }
                )

            self.bill_combo["values"] = display_list

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    def load_bill(self, event=None):

        selected = self.bill_combo.current()

        if selected < 0:
            return

        self.selected_bill_id = self.bill_list[selected]["bill_id"]

        amount = self.bill_list[selected]["amount"]

        self.amount_entry.delete(
            0,
            "end"
        )

        self.amount_entry.insert(
            0,
            f"{amount:.2f}"
        )

    def make_payment(self):

        if self.selected_bill_id is None:

            messagebox.showwarning(
                "Warning",
                "Please select a bill."
            )

            return

        payment_method = self.method_combo.get().strip()

        if payment_method == "":

            messagebox.showwarning(
                "Warning",
                "Please select payment method."
            )

            return

        try:

            amount = float(
                self.amount_entry.get()
            )

            if amount <= 0:

                messagebox.showwarning(
                    "Warning",
                    "Amount must be greater than 0."
                )

                return

        except ValueError:

            messagebox.showwarning(
                "Warning",
                "Please enter a valid amount."
            )

            return

        try:

            connection = get_connection()
            cursor = connection.cursor()

            # Get bill amount
            cursor.execute("""
                SELECT TotalAmount
                FROM Bills
                WHERE BillID = ?
            """, (
                self.selected_bill_id,
            ))

            bill = cursor.fetchone()

            if bill is None:

                connection.close()

                messagebox.showerror(
                    "Error",
                    "Bill not found."
                )

                return

            bill_amount = float(
                bill[0]
            )

            # Check payment amount
            if amount != bill_amount:

                connection.close()

                messagebox.showwarning(
                    "Warning",
                    f"Payment amount must be ₹{bill_amount:.2f}."
                )

                return

            # Create payment
            cursor.execute("""
                INSERT INTO Payments
                (
                    BillID,
                    PaymentMethod,
                    Amount
                )
                VALUES (?, ?, ?)
            """, (
                self.selected_bill_id,
                payment_method,
                amount
            ))

            # Mark order as Completed
            cursor.execute("""
                UPDATE Orders
                SET Status = 'Completed'
                WHERE OrderID = (
                    SELECT OrderID
                    FROM Bills
                    WHERE BillID = ?
                )
            """, (
                self.selected_bill_id,
            ))

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Payment completed successfully."
            )

            self.load_bills()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )