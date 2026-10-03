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

        connection = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            # -----------------------------------------
            # GET BILL DETAILS
            # -----------------------------------------

            cursor.execute("""
                SELECT
                    b.TotalAmount,
                    b.OrderID
                FROM Bills b
                WHERE b.BillID = ?
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

            bill_amount = float(bill[0])
            order_id = bill[1]

            # -----------------------------------------
            # CHECK PAYMENT AMOUNT
            # -----------------------------------------

            if amount != bill_amount:

                connection.close()

                messagebox.showwarning(
                    "Warning",
                    f"Payment amount must be ₹{bill_amount:.2f}."
                )

                return

            # -----------------------------------------
            # CHECK WHETHER RECIPE EXISTS
            # FOR EVERY ORDER ITEM
            # -----------------------------------------

            cursor.execute("""
                SELECT
                    mi.ItemName
                FROM OrderItems oi
                INNER JOIN MenuItems mi
                    ON oi.menuItem_id = mi.menuItem_id
                LEFT JOIN MenuItemIngredients mii
                    ON oi.menuItem_id = mii.menuItem_id
                WHERE oi.OrderID = ?
                GROUP BY
                    mi.menuItem_id,
                    mi.ItemName
                HAVING COUNT(mii.MenuItemIngredientID) = 0
            """, (
                order_id,
            ))

            missing_recipe = cursor.fetchone()

            if missing_recipe:

                connection.close()

                messagebox.showwarning(
                    "Recipe Missing",
                    f"No ingredients have been added for "
                    f"{missing_recipe[0]}."
                )

                return

            # -----------------------------------------
            # CALCULATE REQUIRED INVENTORY
            # -----------------------------------------

            cursor.execute("""
                SELECT
                    i.InventoryID,
                    i.ItemName,
                    i.Unit,
                    i.Quantity,
                    i.MinimumQuantity,
                    SUM(
                        oi.Quantity * mii.QuantityUsed
                    ) AS RequiredQuantity
                FROM OrderItems oi

                INNER JOIN MenuItemIngredients mii
                    ON oi.menuItem_id = mii.menuItem_id

                INNER JOIN Inventory i
                    ON mii.InventoryID = i.InventoryID

                WHERE oi.OrderID = ?

                GROUP BY
                    i.InventoryID,
                    i.ItemName,
                    i.Unit,
                    i.Quantity,
                    i.MinimumQuantity
            """, (
                order_id,
            ))

            inventory_rows = cursor.fetchall()

            # -----------------------------------------
            # CHECK STOCK
            # -----------------------------------------

            for row in inventory_rows:

                inventory_id = row[0]
                item_name = row[1]
                unit = row[2]
                current_quantity = float(row[3])
                minimum_quantity = float(row[4])
                required_quantity = float(row[5])

                if current_quantity < required_quantity:

                    connection.close()

                    messagebox.showwarning(
                        "Insufficient Stock",
                        f"Not enough {item_name}.\n\n"
                        f"Available: {current_quantity:.3f} {unit}\n"
                        f"Required: {required_quantity:.3f} {unit}"
                    )

                    return

            # -----------------------------------------
            # DEDUCT INVENTORY
            # -----------------------------------------

            low_stock_items = []

            for row in inventory_rows:

                inventory_id = row[0]
                item_name = row[1]
                unit = row[2]
                current_quantity = float(row[3])
                minimum_quantity = float(row[4])
                required_quantity = float(row[5])

                new_quantity = (
                    current_quantity - required_quantity
                )

                cursor.execute("""
                    UPDATE Inventory
                    SET Quantity = ?
                    WHERE InventoryID = ?
                """, (
                    new_quantity,
                    inventory_id
                ))

                # Check low stock after deduction

                if new_quantity <= minimum_quantity:

                    low_stock_items.append(
                        f"{item_name}: "
                        f"{new_quantity:.3f} {unit}"
                    )

            # -----------------------------------------
            # CREATE PAYMENT
            # -----------------------------------------

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

            # -----------------------------------------
            # MARK ORDER COMPLETED
            # -----------------------------------------

            cursor.execute("""
                UPDATE Orders
                SET Status = 'Completed'
                WHERE OrderID = ?
            """, (
                order_id,
            ))

            # -----------------------------------------
            # SAVE EVERYTHING
            # -----------------------------------------

            connection.commit()
            connection.close()

            # -----------------------------------------
            # SUCCESS MESSAGE
            # -----------------------------------------

            message = "Payment completed successfully."

            if low_stock_items:

                message += "\n\nLow Stock Items:\n"

                for item in low_stock_items:
                    message += f"\n• {item}"

            messagebox.showinfo(
                "Success",
                message
            )

            self.load_bills()

        except Exception as e:

            if connection is not None:

                connection.rollback()
                connection.close()

            messagebox.showerror(
                "Error",
                str(e)
            )