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

        # Start with no dish selected
        self.menu_combo.set("")

    def create_widgets(self):

        title = tk.Label(
            self.parent,
            text="Recipe / Ingredients",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=15)

        # MENU ITEM SELECTION

        menu_frame = tk.Frame(self.parent)
        menu_frame.pack(pady=5)

        tk.Label(
            menu_frame,
            text="Menu Item:",
            font=("Arial", 11, "bold")
        ).pack(side="left", padx=5)

        self.menu_combo = ttk.Combobox(
            menu_frame,
            width=35,
            state="readonly"
        )
        self.menu_combo.pack(side="left", padx=5)

        self.menu_combo.bind(
            "<<ComboboxSelected>>",
            self.load_recipe
        )

        # ADD INGREDIENT

        form = tk.Frame(self.parent)
        form.pack(pady=10)

        tk.Label(
            form,
            text="Inventory Item:"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.inventory_combo = ttk.Combobox(
            form,
            width=30,
            state="readonly"
        )
        self.inventory_combo.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        tk.Label(
            form,
            text="Quantity Used:"
        ).grid(row=0, column=2, padx=5, pady=5)

        self.quantity_entry = tk.Entry(
            form,
            width=15
        )
        self.quantity_entry.grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )

        tk.Button(
            form,
            text="Add Ingredient",
            width=15,
            command=self.add_ingredient
        ).grid(
            row=0,
            column=4,
            padx=5,
            pady=5
        )

        # DELETE BUTTON

        button_frame = tk.Frame(self.parent)
        button_frame.pack(pady=5)

        tk.Button(
            button_frame,
            text="Delete Ingredient",
            width=18,
            command=self.delete_ingredient
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Refresh",
            width=12,
            command=self.load_recipe
        ).pack(side="left", padx=5)

        # RECIPE TREE

        self.tree = ttk.Treeview(
            self.parent,
            columns=(
                "ID",
                "InventoryItem",
                "Unit",
                "QuantityUsed"
            ),
            show="headings"
        )

        self.tree.heading(
            "ID",
            text="ID"
        )

        self.tree.heading(
            "InventoryItem",
            text="Inventory Item"
        )

        self.tree.heading(
            "Unit",
            text="Unit"
        )

        self.tree.heading(
            "QuantityUsed",
            text="Quantity Used"
        )

        self.tree.column(
            "ID",
            width=60
        )

        self.tree.column(
            "InventoryItem",
            width=250
        )

        self.tree.column(
            "Unit",
            width=100
        )

        self.tree.column(
            "QuantityUsed",
            width=150
        )

        self.tree.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

    # LOAD MENU ITEMS

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
                values.append(
                    f"{row[0]} - {row[1]}"
                )

            self.menu_combo["values"] = values

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    # LOAD INVENTORY ITEMS

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
                values.append(
                    f"{row[0]} - {row[1]} ({row[2]})"
                )

            self.inventory_combo["values"] = values

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    # LOAD RECIPE FOR SELECTED MENU ITEM

    def load_recipe(self, event=None):

        for item in self.tree.get_children():
            self.tree.delete(item)

        menu_value = self.menu_combo.get()

        if not menu_value:
            return

        menu_id = int(
            menu_value.split(" - ")[0]
        )

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    mii.MenuItemIngredientID,
                    i.ItemName,
                    i.Unit,
                    mii.QuantityUsed
                FROM MenuItemIngredients mii
                INNER JOIN Inventory i
                    ON mii.InventoryID = i.InventoryID
                WHERE mii.menuItem_id = ?
                ORDER BY i.ItemName
            """, (menu_id,))

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
            messagebox.showerror(
                "Error",
                str(e)
            )

    # ADD INGREDIENT

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

        menu_id = int(
            menu_value.split(" - ")[0]
        )

        inventory_id = int(
            inventory_value.split(" - ")[0]
        )

        try:

            connection = get_connection()
            cursor = connection.cursor()

            # Check whether this ingredient is already used in this recipe

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
                    "This ingredient is already added to this dish."
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

            self.inventory_combo.set("")
            self.quantity_entry.delete(
                0,
                "end"
            )

            self.load_recipe()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

    # DELETE INGREDIENT

    def delete_ingredient(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select an ingredient."
            )

            return

        values = self.tree.item(
            selected[0],
            "values"
        )

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

            self.load_recipe()

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )