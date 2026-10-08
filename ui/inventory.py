import tkinter as tk
from tkinter import ttk, messagebox

from database.connection import get_connection


class InventoryPage:

    def __init__(self, parent):

        self.parent = parent
        self.selected_inventory_id = None

        self.create_widgets()
        self.load_inventory()

    def create_widgets(self):

        title = tk.Label(
            self.parent,
            text="Inventory",
            font=("Arial", 20, "bold")
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=20
        )

        # Search
        search_frame = tk.Frame(self.parent)

        search_frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        tk.Label(
            search_frame,
            text="Search"
        ).pack(
            side="left",
            padx=5
        )

        self.search_entry = tk.Entry(
            search_frame,
            width=30
        )

        self.search_entry.pack(
            side="left",
            padx=5
        )

        tk.Button(
            search_frame,
            text="Search",
            command=self.search_inventory
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            search_frame,
            text="Show All",
            command=self.load_inventory
        ).pack(
            side="left",
            padx=5
        )

        # Form
        form_frame = tk.Frame(self.parent)

        form_frame.pack(
            fill="x",
            padx=20,
            pady=15
        )

        tk.Label(
            form_frame,
            text="Item Name"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.item_name_entry = tk.Entry(
            form_frame,
            width=25
        )

        self.item_name_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        tk.Label(
            form_frame,
            text="Unit"
        ).grid(
            row=0,
            column=2,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.unit_entry = tk.Entry(
            form_frame,
            width=15
        )

        self.unit_entry.grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )

        tk.Label(
            form_frame,
            text="Quantity"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.quantity_entry = tk.Entry(
            form_frame,
            width=25
        )

        self.quantity_entry.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        tk.Label(
            form_frame,
            text="Minimum Quantity"
        ).grid(
            row=1,
            column=2,
            padx=5,
            pady=5,
            sticky="w"
        )

        self.minimum_entry = tk.Entry(
            form_frame,
            width=15
        )

        self.minimum_entry.grid(
            row=1,
            column=3,
            padx=5,
            pady=5
        )

        # Buttons
        button_frame = tk.Frame(self.parent)

        button_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        tk.Button(
            button_frame,
            text="Add",
            width=12,
            command=self.add_inventory
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="Edit",
            width=12,
            command=self.edit_inventory
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="Delete",
            width=12,
            command=self.delete_inventory
        ).pack(
            side="left",
            padx=5
        )

        tk.Button(
            button_frame,
            text="Clear",
            width=12,
            command=self.clear_form
        ).pack(
            side="left",
            padx=5
        )

        # Treeview
        tree_frame = tk.Frame(self.parent)

        tree_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "InventoryID",
            "ItemName",
            "Unit",
            "Quantity",
            "MinimumQuantity",
            "Status",
            "CreatedAt"
        )

        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings"
        )

        self.tree.heading(
            "InventoryID",
            text="ID"
        )

        self.tree.heading(
            "ItemName",
            text="Item Name"
        )

        self.tree.heading(
            "Unit",
            text="Unit"
        )

        self.tree.heading(
            "Quantity",
            text="Quantity"
        )

        self.tree.heading(
            "MinimumQuantity",
            text="Minimum"
        )

        self.tree.heading(
            "Status",
            text="Status"
        )

        self.tree.heading(
            "CreatedAt",
            text="Created At"
        )

        self.tree.column(
            "InventoryID",
            width=60
        )

        self.tree.column(
            "ItemName",
            width=180
        )

        self.tree.column(
            "Unit",
            width=100
        )

        self.tree.column(
            "Quantity",
            width=100
        )

        self.tree.column(
            "MinimumQuantity",
            width=100
        )

        self.tree.column(
            "Status",
            width=100
        )

        self.tree.column(
            "CreatedAt",
            width=150
        )

        self.tree.pack(
            fill="both",
            expand=True
        )

        # Low stock row styling
        self.tree.tag_configure(
            "low_stock",
            foreground="#DC2626",
            background="#FEE2E2"
        )

        self.tree.tag_configure(
            "available",
            foreground="#166534",
            background="#F0FDF4"
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.select_inventory
        )

    def load_inventory(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    InventoryID,
                    ItemName,
                    Unit,
                    Quantity,
                    MinimumQuantity,
                    CreatedAt
                FROM Inventory
                ORDER BY InventoryID DESC
            """)

            rows = cursor.fetchall()

            connection.close()

            for row in rows:

                inventory_id = row[0]
                item_name = row[1]
                unit = row[2]
                quantity = float(row[3])
                minimum_quantity = float(row[4])
                created_at = row[5]

                if quantity <= minimum_quantity:
                    status = "Low Stock"
                    tag = "low_stock"
                else:
                    status = "Available"
                    tag = "available"

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        inventory_id,
                        item_name,
                        unit,
                        f"{quantity:.2f}",
                        f"{minimum_quantity:.2f}",
                        status,
                        created_at
                    ),
                    tags=(tag,)
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    def search_inventory(self):

        search_text = self.search_entry.get().strip()

        for item in self.tree.get_children():
            self.tree.delete(item)

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    InventoryID,
                    ItemName,
                    Unit,
                    Quantity,
                    MinimumQuantity,
                    CreatedAt
                FROM Inventory
                WHERE ItemName LIKE ?
                ORDER BY InventoryID DESC
            """, (
                "%" + search_text + "%",
            ))

            rows = cursor.fetchall()

            connection.close()

            for row in rows:

                quantity = float(row[3])
                minimum_quantity = float(row[4])

                if quantity <= minimum_quantity:
                    status = "Low Stock"
                    tag = "low_stock"
                else:
                    status = "Available"
                    tag = "available"

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        row[0],
                        row[1],
                        row[2],
                        f"{quantity:.2f}",
                        f"{minimum_quantity:.2f}",
                        status,
                        row[5]
                    ),
                    tags=(tag,)
                )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    def select_inventory(self, event=None):

        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(
            selected[0],
            "values"
        )

        self.selected_inventory_id = values[0]

        self.item_name_entry.delete(
            0,
            "end"
        )

        self.item_name_entry.insert(
            0,
            values[1]
        )

        self.unit_entry.delete(
            0,
            "end"
        )

        self.unit_entry.insert(
            0,
            values[2]
        )

        self.quantity_entry.delete(
            0,
            "end"
        )

        self.quantity_entry.insert(
            0,
            values[3]
        )

        self.minimum_entry.delete(
            0,
            "end"
        )

        self.minimum_entry.insert(
            0,
            values[4]
        )

    def add_inventory(self):

        item_name = self.item_name_entry.get().strip()
        unit = self.unit_entry.get().strip()

        try:

            quantity = float(
                self.quantity_entry.get()
            )

            minimum_quantity = float(
                self.minimum_entry.get()
            )

        except ValueError:

            messagebox.showwarning(
                "Warning",
                "Quantity and minimum quantity must be numbers."
            )

            return

        if item_name == "" or unit == "":

            messagebox.showwarning(
                "Warning",
                "Please fill all fields."
            )

            return

        if quantity < 0 or minimum_quantity < 0:

            messagebox.showwarning(
                "Warning",
                "Quantity cannot be negative."
            )

            return

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO Inventory
                (
                    ItemName,
                    Unit,
                    Quantity,
                    MinimumQuantity
                )
                VALUES (?, ?, ?, ?)
            """, (
                item_name,
                unit,
                quantity,
                minimum_quantity
            ))

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Inventory item added successfully."
            )

            self.clear_form()
            self.load_inventory()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    def edit_inventory(self):

        if self.selected_inventory_id is None:

            messagebox.showwarning(
                "Warning",
                "Please select an inventory item."
            )

            return

        item_name = self.item_name_entry.get().strip()
        unit = self.unit_entry.get().strip()

        try:

            quantity = float(
                self.quantity_entry.get()
            )

            minimum_quantity = float(
                self.minimum_entry.get()
            )

        except ValueError:

            messagebox.showwarning(
                "Warning",
                "Quantity and minimum quantity must be numbers."
            )

            return

        if item_name == "" or unit == "":

            messagebox.showwarning(
                "Warning",
                "Please fill all fields."
            )

            return

        if quantity < 0 or minimum_quantity < 0:

            messagebox.showwarning(
                "Warning",
                "Quantity cannot be negative."
            )

            return

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE Inventory
                SET
                    ItemName = ?,
                    Unit = ?,
                    Quantity = ?,
                    MinimumQuantity = ?
                WHERE InventoryID = ?
            """, (
                item_name,
                unit,
                quantity,
                minimum_quantity,
                self.selected_inventory_id
            ))

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Inventory item updated successfully."
            )

            self.clear_form()
            self.load_inventory()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    def delete_inventory(self):

        if self.selected_inventory_id is None:

            messagebox.showwarning(
                "Warning",
                "Please select an inventory item."
            )

            return

        confirm = messagebox.askyesno(
            "Confirm",
            "Are you sure you want to delete this inventory item?"
        )

        if not confirm:
            return

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                DELETE FROM Inventory
                WHERE InventoryID = ?
            """, (
                self.selected_inventory_id,
            ))

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Inventory item deleted successfully."
            )

            self.clear_form()
            self.load_inventory()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    def clear_form(self):

        self.selected_inventory_id = None

        self.item_name_entry.delete(
            0,
            "end"
        )

        self.unit_entry.delete(
            0,
            "end"
        )

        self.quantity_entry.delete(
            0,
            "end"
        )

        self.minimum_entry.delete(
            0,
            "end"
        )