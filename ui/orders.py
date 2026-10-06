import tkinter as tk
from tkinter import ttk, messagebox

from database.connection import get_connection


class OrdersPage:

    def __init__(self, parent):

        self.parent = parent
        self.customer_list = []
        self.menu_list = []
        self.current_items = []
        self.create_widgets()
        self.load_customers()
        self.load_menu_items()

    def create_widgets(self):
        title = tk.Label(self.parent,text="Orders",font=("Arial", 22, "bold"))
        title.pack(pady=15)

        # Customer section
        customer_frame = tk.Frame(self.parent)
        customer_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(customer_frame,text="Customer:").pack(side="left", padx=5)

        self.customer_combo = ttk.Combobox(customer_frame,state="readonly",width=30)
        self.customer_combo.pack(side="left", padx=5)

        # Menu item section
        item_frame = tk.Frame(self.parent)
        item_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(item_frame,text="Menu Item:").pack(side="left", padx=5)

        self.menu_combo = ttk.Combobox(item_frame,state="readonly",width=30)
        self.menu_combo.pack(side="left", padx=5)

        tk.Label(item_frame,text="Quantity:").pack(side="left", padx=5)

        self.quantity_entry = tk.Entry(item_frame,width=10)
        self.quantity_entry.pack(side="left", padx=5)

        add_button = tk.Button(item_frame,text="Add Item",command=self.add_item)
        add_button.pack(side="left", padx=10)

        # Order items table
        table_frame = tk.Frame(self.parent)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = (
            "menuItem_id",
            "itemName",
            "Price",
            "Quantity",
            "Amount"
        )

        self.order_table = ttk.Treeview(table_frame,columns=columns,show="headings")
        self.order_table.heading("menuItem_id",text="ID")
        self.order_table.heading("itemName",text="Item Name")
        self.order_table.heading("Price",text="Price")
        self.order_table.heading("Quantity",text="Quantity")
        self.order_table.heading("Amount",text="Amount")
        
        self.order_table.column("menuItem_id",width=60)
        self.order_table.column("itemName",width=250)
        self.order_table.column("Price",width=100)
        self.order_table.column("Quantity",width=100)
        self.order_table.column("Amount",width=120)
        self.order_table.pack(fill="both",expand=True)

        # Bottom section
        bottom_frame = tk.Frame(self.parent)
        bottom_frame.pack(fill="x", padx=20, pady=10)
        self.total_label = tk.Label(bottom_frame,text="Total: 0.00",font=("Arial", 16, "bold"))
        self.total_label.pack(side="left")
        save_button = tk.Button(bottom_frame,text="Save Order",command=self.save_order)
        save_button.pack(side="right", padx=5)
        clear_button = tk.Button(bottom_frame,text="Clear",command=self.clear_order)
        clear_button.pack(side="right", padx=5)

    def load_customers(self):

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT customer_id, full_name
                FROM Customers
                ORDER BY full_name
            """)

            rows = cursor.fetchall()

            connection.close()

            self.customer_list = rows

            customer_names = []

            for row in rows:
                customer_names.append(
                    row[1]
                )

            self.customer_combo["values"] = customer_names

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    def load_menu_items(self):

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT menuItem_id, itemName, Price
                FROM MenuItems
                ORDER BY itemName
            """)

            rows = cursor.fetchall()

            connection.close()

            self.menu_list = rows

            menu_names = []

            for row in rows:
                menu_names.append(
                    row[1]
                )

            self.menu_combo["values"] = menu_names

        except Exception as e:

            messagebox.showerror("Error",str(e))

    def add_item(self):
        menu_index = self.menu_combo.current()
        if menu_index == -1:

            messagebox.showwarning("Warning","Please select a menu item.")

            return

        quantity_text = self.quantity_entry.get().strip()

        if quantity_text == "":
            messagebox.showwarning("Warning","Please enter quantity.")

            return

        try:

            quantity = int(quantity_text)

        except ValueError:

            messagebox.showwarning("Warning", "Quantity must be a number.")

            return

        if quantity <= 0:

            messagebox.showwarning("Warning","Quantity must be greater than 0.")

            return

        menu_row = self.menu_list[menu_index]

        menu_item_id = menu_row[0]
        item_name = menu_row[1]
        price = float(menu_row[2])

        amount = price * quantity

        self.current_items.append({
            "menuItem_id": menu_item_id,
            "itemName": item_name,
            "Price": price,
            "Quantity": quantity,
            "Amount": amount
        })

        self.order_table.insert("","end",
            values=(menu_item_id,item_name,f"{price:.2f}",quantity,f"{amount:.2f}"))

        self.update_total()

        self.quantity_entry.delete(0,tk.END)

    def update_total(self):

        total = 0

        for item in self.current_items:

            total += item["Amount"]

        self.total_label.config(text=f"Total: {total:.2f}")

    def clear_order(self):

        self.current_items.clear()

        for item in self.order_table.get_children():

            self.order_table.delete(item)

        self.customer_combo.set("")
        self.menu_combo.set("")
        self.quantity_entry.delete(0,tk.END)

        self.update_total()

    def save_order(self):

        customer_index = self.customer_combo.current()

        if customer_index == -1:

            messagebox.showwarning("Warning","Please select a customer.")

            return

        if len(self.current_items) == 0:

            messagebox.showwarning("Warning","Please add at least one item.")

            return

        customer_id = self.customer_list[customer_index][0]

        total = 0

        for item in self.current_items:

            total += item["Amount"]

        try:

            connection = get_connection()
            cursor = connection.cursor()

            # Insert order
            cursor.execute("""
                INSERT INTO Orders
                (
                    customer_id,
                    Status,
                    TotalAmount
                )
                OUTPUT INSERTED.OrderID
                VALUES (?, ?, ?)
            """, (
                customer_id,
                "Pending",
                total
            ))

            order_id = cursor.fetchone()[0]

            # Insert order items
            for item in self.current_items:

                cursor.execute("""
                    INSERT INTO OrderItems
                    (
                        OrderID,
                        menuItem_id,
                        Quantity,
                        Price,
                        Amount
                    )
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    order_id,
                    item["menuItem_id"],
                    item["Quantity"],
                    item["Price"],
                    item["Amount"]
                ))

            connection.commit()
            connection.close()

            messagebox.showinfo("Success",f"Order #{order_id} saved successfully.")

            self.clear_order()

        except Exception as e:

            messagebox.showerror("Error",str(e))