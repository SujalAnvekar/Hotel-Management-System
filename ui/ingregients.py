import tkinter as tk
from tkinter import ttk, messagebox

from database.connection import get_connection


class IngredientsPage:

    def __init__(self, parent):
        self.parent = parent

        self.menu_items = []
        self.inventory_items = []

        self.create_widgets()
        self.load_menu_items()
        self.load_inventory_items()
        self.load_ingredients()

    def create_widgets(self):

        title = tk.Label(
            self.parent,
            text="Recipe / Ingredients",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=15)

        form = tk.Frame(self.parent)
        form.pack(pady=10)

        tk.Label(
            form,
            text="Menu Item",
            font=("Arial", 11)
        ).grid(row=0, column=0, padx=5, pady=5)

        self.menu_combo = ttk.Combobox(
            form,
            width=30,
            state="readonly"
        )
        self.menu_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(
            form,
            text="Inventory Item",
            font=("Arial", 11)
        ).grid(row=1, column=0, padx=5, pady=5)

        self.inventory_combo = ttk.Combobox(
            form,
            width=30,
            state="readonly"
        )
        self.inventory_combo.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(
            form,
            text="Quantity Used",
            font=("Arial", 11)
        ).grid(row=2, column=0, padx=5, pady=5)

        self.quantity_entry = tk.Entry(
            form,
            width=33
        )
        self.quantity_entry.grid(row=2, column=1, padx=5, pady=5)

        button_frame = tk.Frame(self.parent)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Add",
            width=12,
            command=self.add_ingredient
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="Delete",
            width=12,
            command=self.delete_ingredient
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="Clear",
            width=12,
            command=self.clear_fields
        ).grid(row=0, column=2, padx=5)

        self.tree = ttk.Treeview(
            self.parent,
            columns=(
                "ID",
                "MenuItem",
                "InventoryItem",
                "QuantityUsed"
            ),
            show="headings"
        )

        self.tree.heading("ID", text="ID")
        self.tree.heading("MenuItem", text="Menu Item")
        self.tree.heading("InventoryItem", text="Inventory Item")
        self.tree.heading("QuantityUsed", text="Quantity Used")

        self.tree.column("ID", width=60)
        self.tree.column("MenuItem", width=220)
        self.tree.column("InventoryItem", width=220)
        self.tree.column("QuantityUsed", width=120)

        self.tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

    def load_menu_items(self):

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT menuItem_id, ItemName
                FROM MenuItems
                ORDER BY ItemName
            """)

            rows = cursor.fetchall()

            connection.close()

            self.menu_items = rows

            values = []

            for row in rows:
                values.append(f"{row[0]} - {row[1]}")

            self.menu_combo["values"] = values

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_inventory_items(self):

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT InventoryID, ItemName, Unit
                FROM Inventory
                ORDER BY ItemName
            """)

            rows = cursor.fetchall()

            connection.close()

            self.inventory_items = rows

            values = []

            for row in rows:
                values.append(f"{row[0]} - {row[1]} ({row[2]})")

            self.inventory_combo["values"] = values

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_ingredients(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    mii.MenuItemIngredientID,
                    mi.ItemName,
                    i.ItemName,
                    mii.QuantityUsed
                FROM MenuItemIngredients mii
                INNER JOIN MenuItems mi
                    ON mii.menuItem_id = mi.menuItem_id
                INNER JOIN Inventory i
                    ON mii.InventoryID = i.InventoryID
                ORDER BY mi.ItemName, i.ItemName
            """)

            rows = cursor.fetchall()

            connection.close()

            for row in rows:

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        row[0],
                        row[1],
                        row[2],
                        row[3]
                    )
                )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_ingredient(self):

        menu_value = self.menu_combo.get()
        inventory_value = self.inventory_combo.get()
        quantity = self.quantity_entry.get().strip()

        if not menu_value:
            messagebox.showwarning(
                "Warning",
                "Please select a menu item."
            )
            return

        if not inventory_value:
            messagebox.showwarning(
                "Warning",
                "Please select an inventory item."
            )
            return

        if not quantity:
            messagebox.showwarning(
                "Warning",
                "Please enter quantity used."
            )
            return

        try:
            quantity = float(quantity)

            if quantity <= 0:
                messagebox.showwarning(
                    "Warning",
                    "Quantity must be greater than 0."
                )
                return

        except ValueError:
            messagebox.showwarning(
                "Warning",
                "Please enter a valid quantity."
            )
            return

        try:

            menu_id = int(menu_value.split(" - ")[0])
            inventory_id = int(inventory_value.split(" - ")[0])

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT MenuItemIngredientID
                FROM MenuItemIngredients
                WHERE menuItem_id = ?
                  AND InventoryID = ?
            """, (
                menu_id,
                inventory_id
            ))

            existing = cursor.fetchone()

            if existing:
                connection.close()

                messagebox.showwarning(
                    "Warning",
                    "This ingredient is already added to this menu item."
                )
                return

            cursor.execute("""
                INSERT INTO MenuItemIngredients
                (
                    menuItem_id,
                    InventoryID,
                    QuantityUsed
                )
                VALUES (?, ?, ?)
            """, (
                menu_id,
                inventory_id,
                quantity
            ))

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Ingredient added successfully."
            )

            self.clear_fields()
            self.load_ingredients()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_ingredient(self):

        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Please select an ingredient."
            )
            return

        values = self.tree.item(selected[0], "values")

        ingredient_id = values[0]

        confirm = messagebox.askyesno(
            "Confirm",
            "Delete this ingredient?"
        )

        if not confirm:
            return

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                DELETE FROM MenuItemIngredients
                WHERE MenuItemIngredientID = ?
            """, (ingredient_id,))

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Ingredient deleted successfully."
            )

            self.load_ingredients()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_fields(self):

        self.menu_combo.set("")
        self.inventory_combo.set("")
        self.quantity_entry.delete(0, "end")