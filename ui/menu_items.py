import tkinter as tk
from tkinter import ttk, messagebox

from database.connection import get_connection


class MenuItemsPage:

    def __init__(self, parent):

        self.parent = parent

        self.frame = tk.Frame(parent,bg="#F5F6FA")
        self.frame.pack(fill="both",expand=True)
        self.create_widgets()
        self.load_menu_items()

    # ==========================================
    # CREATE PAGE
    # ==========================================

    def create_widgets(self):

        # Title
        title_frame = tk.Frame(self.frame,bg="#F5F6FA")
        title_frame.pack(fill="x",padx=30,pady=(25, 15))

        tk.Label(title_frame,text="Menu Items",bg="#F5F6FA",fg="#172033",font=("Segoe UI", 24, "bold")).pack(side="left")

        # ======================================
        # Search Area
        # ======================================

        search_frame = tk.Frame(self.frame,bg="#F5F6FA")
        search_frame.pack(fill="x",padx=30,pady=(0, 15))
        tk.Label(search_frame,text="Search:",bg="#F5F6FA",fg="#172033",font=("Segoe UI", 10)).pack(side="left",padx=(0, 8))
        self.search_entry = tk.Entry(search_frame,font=("Segoe UI", 10),width=30)
        self.search_entry.pack(side="left",ipady=6)

        # Search button
        tk.Button(search_frame,text="Search",bg="#4B74D9",fg="white",activebackground="#365DB5",activeforeground="white",relief="flat",
        bd=0,font=("Segoe UI", 10),cursor="hand2",command=self.search_menu_item).pack(side="left",padx=8,ipadx=10,ipady=5)

        # Show All button
        tk.Button(search_frame,text="Show All",bg="#6B7280",fg="white",activebackground="#4B5563",activeforeground="white",relief="flat",
        bd=0,font=("Segoe UI", 10),cursor="hand2",command=self.load_menu_items).pack(side="left",ipadx=10,ipady=5)

        # Add Menu Item
        tk.Button(search_frame,text="+ Add Menu Item",bg="#E87524",fg="white",activebackground="#C95F17",activeforeground="white",
        relief="flat",bd=0,font=("Segoe UI", 10, "bold"),cursor="hand2",command=self.add_menu_item).pack(
        side="right",ipadx=10,ipady=5)

        # ======================================
        # Table
        # ======================================

        table_frame = tk.Frame(self.frame,bg="white")
        table_frame.pack(fill="both",expand=True,padx=30,pady=(0, 15))
        scrollbar = ttk.Scrollbar(table_frame,orient="vertical")
        scrollbar.pack(side="right",fill="y")
        self.menu_table = ttk.Treeview(table_frame,columns=(
                "menuItem_id",
                "category_name",
                "ItemName",
                "Price",
                "CreatedAt"
            ),
            show="headings",
            yscrollcommand=scrollbar.set
        )

        self.menu_table.pack(fill="both",expand=True)
        scrollbar.config(command=self.menu_table.yview)

        # Headings
        self.menu_table.heading("menuItem_id",text="ID")
        self.menu_table.heading("category_name",text="Category")
        self.menu_table.heading("ItemName",text="Item Name")
        self.menu_table.heading("Price",text="Price")
        self.menu_table.heading("CreatedAt",text="Created At")

        # Column widths
        self.menu_table.column("menuItem_id",width=60,anchor="center")
        self.menu_table.column("category_name",width=180)
        self.menu_table.column("ItemName",width=250)
        self.menu_table.column("Price",width=120,anchor="center")
        self.menu_table.column( "CreatedAt", width=180)

        # Bottom Buttons

        button_frame = tk.Frame(self.frame,bg="#F5F6FA")
        button_frame.pack(fill="x",padx=30,pady=(0, 25))

        # Edit
        tk.Button(button_frame,
            text="Edit Menu Item",
            bg="#4B74D9",
            fg="white",
            activebackground="#365DB5",
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10),
            cursor="hand2",
            command=self.edit_menu_item
        ).pack(
            side="left",
            ipadx=12,
            ipady=6
        )

        # Delete
        tk.Button(
            button_frame,
            text="Delete Menu Item",
            bg="#D84A4A",
            fg="white",
            activebackground="#B83232",
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10),
            cursor="hand2",
            command=self.delete_menu_item
        ).pack(
            side="left",
            padx=10,
            ipadx=12,
            ipady=6
        )

    # ==========================================
    # LOAD MENU ITEMS
    # ==========================================

    def load_menu_items(self):
        for row in self.menu_table.get_children():
            self.menu_table.delete(row)
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("""
                SELECT
                    M.menuItem_id,
                    C.category_name,
                    M.ItemName,
                    M.Price,
                    M.CreatedAt
                FROM MenuItems M
                INNER JOIN Categories C
                    ON M.category_id = C.category_id
                ORDER BY M.menuItem_id DESC
            """)

            rows = cursor.fetchall()
            for row in rows:
                self.menu_table.insert(
                    "",
                    "end",
                    values=(
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                        row[4]
                    )
                )

            cursor.close()
            connection.close()

        except Exception as e:

            messagebox.showerror("Database Error",str(e))

    # SEARCH MENU ITEM

    def search_menu_item(self):
        search_text = self.search_entry.get().strip()
        if search_text == "":
            self.load_menu_items()
            return

        for row in self.menu_table.get_children():
            self.menu_table.delete(row)

        try:
            connection = get_connection()
            cursor = connection.cursor()
            search_value = "%" + search_text + "%"
            cursor.execute("""
                SELECT
                    M.menuItem_id,
                    C.category_name,
                    M.ItemName,
                    M.Price,
                    M.CreatedAt
                FROM MenuItems M
                INNER JOIN Categories C
                    ON M.category_id = C.category_id
                WHERE M.ItemName LIKE ?
                   OR C.category_name LIKE ?
                ORDER BY M.menuItem_id DESC
            """, (search_value,search_value))

            rows = cursor.fetchall()
            for row in rows:
                self.menu_table.insert(
                    "",
                    "end",
                    values=(
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                        row[4]
                    )
                )

            cursor.close()
            connection.close()

        except Exception as e:

            messagebox.showerror("Database Error",str(e))

    # GET CATEGORIES
    def get_categories(self):
        categories = []
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("""
                SELECT category_id, category_name
                FROM Categories
                ORDER BY category_name
            """)
            rows = cursor.fetchall()
            for row in rows:
                categories.append((row[0], row[1]))

            cursor.close()
            connection.close()

        except Exception as e:

            messagebox.showerror("Database Error",str(e))

        return categories

    # ADD MENU ITEM
    def add_menu_item(self):
        categories = self.get_categories()
        if len(categories) == 0:
            messagebox.showwarning("No Categories","Please add a category first.")

            return

        add_window = tk.Toplevel(self.frame)
        add_window.title("Add Menu Item")
        add_window.geometry("450x400")
        add_window.resizable(False,False)
        add_window.transient(self.frame.winfo_toplevel())

        # Title
        tk.Label(add_window,text="Add Menu Item",font=("Segoe UI", 18, "bold"),fg="#172033").pack(pady=(25, 20))

        # Category
        tk.Label(add_window,text="Category",font=("Segoe UI", 10)).pack(anchor="w",padx=40)

        category_values = []

        for category in categories:
            category_values.append(category[1])

        category_combo = ttk.Combobox(add_window,values=category_values,state="readonly",font=("Segoe UI", 10))
        category_combo.pack(fill="x",padx=40,pady=(5, 15),ipady=5)
        category_combo.current(0)

        # Item Name
        tk.Label(add_window,text="Item Name",font=("Segoe UI", 10)).pack(anchor="w",padx=40)

        item_entry = tk.Entry(add_window,font=("Segoe UI", 10))
        item_entry.pack(fill="x",padx=40,pady=(5, 15),ipady=6)

        # Price
        tk.Label(add_window,text="Price",font=("Segoe UI", 10)).pack(anchor="w",padx=40)
        price_entry = tk.Entry(add_window,font=("Segoe UI", 10))
        price_entry.pack( fill="x",padx=40, pady=(5, 20),ipady=6)

        # SAVE
        def save_menu_item():
            category_name = category_combo.get().strip()
            item_name = item_entry.get().strip()
            price = price_entry.get().strip()

            if category_name == "":
                messagebox.showwarning("Validation", "Please select a category.")
                return

            if item_name == "":
                messagebox.showwarning("Validation", "Please enter item name.")
                item_entry.focus()
                return

            if price == "":
                messagebox.showwarning("Validation","Please enter price.")
                price_entry.focus()
                return

            try:
                price_value = float(price)
                if price_value < 0:
                    messagebox.showwarning("Validation","Price cannot be negative.")
                    return

            except ValueError:

                messagebox.showwarning("Validation","Please enter a valid price.")
                price_entry.focus()

                return

            # Find category_id
            category_id = None

            for category in categories:
                if category[1] == category_name:
                    category_id = category[0]
                    break

            try:
                connection = get_connection()
                cursor = connection.cursor()
                cursor.execute("""
                    INSERT INTO MenuItems
                    (
                        category_id,
                        ItemName,
                        Price
                    )
                    VALUES (?, ?, ?)
                """, (
                    category_id,
                    item_name,
                    price_value
                ))
                connection.commit()
                cursor.close()
                connection.close()
                messagebox.showinfo("Success", "Menu item added successfully.")
                add_window.destroy()
                self.load_menu_items()

            except Exception as e:

                messagebox.showerror( "Database Error",str(e))

        # Buttons
        button_frame = tk.Frame(add_window)
        button_frame.pack()
        tk.Button(button_frame,text="Save", bg="#1F9D68",fg="white",activebackground="#167A50",activeforeground="white",
        relief="flat",bd=0,font=("Segoe UI", 10, "bold"),cursor="hand2",command=save_menu_item).pack(
        side="left",ipadx=20,ipady=6)

        tk.Button(button_frame,text="Cancel",bg="#6B7280",fg="white",activebackground="#4B5563",activeforeground="white",
        relief="flat",bd=0,font=("Segoe UI", 10),cursor="hand2",command=add_window.destroy).pack(
        side="left", padx=10,ipadx=15,ipady=6)

        item_entry.focus()

    # EDIT MENU ITEM
    def edit_menu_item(self):
        selected = self.menu_table.selection()
        if not selected:
            messagebox.showwarning("Select Menu Item","Please select a menu item first.")

            return

        values = self.menu_table.item(selected[0],"values")
        menu_item_id = values[0]
        old_category = values[1]
        old_item_name = values[2]
        old_price = values[3]

        categories = self.get_categories()

        edit_window = tk.Toplevel(self.frame)
        edit_window.title("Edit Menu Item")
        edit_window.geometry("450x400")
        edit_window.resizable(False,False)

        # Title
        tk.Label(edit_window,text="Edit Menu Item", font=("Segoe UI", 18, "bold"),fg="#172033").pack(pady=(25, 20))

        # Category
        tk.Label(edit_window, text="Category",font=("Segoe UI", 10) ).pack(anchor="w",padx=40)

        category_values = []

        for category in categories:
            category_values.append(category[1])

        category_combo = ttk.Combobox(edit_window,values=category_values, state="readonly",font=("Segoe UI", 10))
        category_combo.pack(fill="x",padx=40, pady=(5, 15),ipady=5)

        if old_category in category_values:

            category_combo.set(
                old_category
            )

        # Item Name
        tk.Label(edit_window,text="Item Name",font=("Segoe UI", 10)).pack(anchor="w",padx=40)

        item_entry = tk.Entry(edit_window,font=("Segoe UI", 10))

        item_entry.pack(fill="x",padx=40,pady=(5, 15),ipady=6)

        item_entry.insert(0,old_item_name)

        # Price
        tk.Label(
            edit_window,text="Price",font=("Segoe UI", 10)).pack(anchor="w",padx=40)

        price_entry = tk.Entry(edit_window,font=("Segoe UI", 10))

        price_entry.pack(fill="x", padx=40,pady=(5, 20), ipady=6)

        price_entry.insert(0,old_price)

        # UPDATE
       
        def update_menu_item():

            category_name = category_combo.get().strip()
            item_name = item_entry.get().strip()
            price = price_entry.get().strip()

            if category_name == "":
                messagebox.showwarning("Validation","Please select a category.")
                return

            if item_name == "":
                messagebox.showwarning("Validation","Please enter item name.")
                return

            if price == "":
                messagebox.showwarning("Validation","Please enter price.")
                return

            try:
                price_value = float(price)
                if price_value < 0:
                    messagebox.showwarning("Validation","Price cannot be negative.")

                    return

            except ValueError:
                messagebox.showwarning("Validation","Please enter a valid price.")

                return

            # Find category_id
            category_id = None

            for category in categories:
                if category[1] == category_name:
                    category_id = category[0]
                    break

            try:
                connection = get_connection()
                cursor = connection.cursor()

                cursor.execute("""
                    UPDATE MenuItems
                    SET
                        category_id = ?,
                        ItemName = ?,
                        Price = ?
                    WHERE menuItem_id = ?
                """, (category_id,item_name, price_value,menu_item_id))

                connection.commit()
                cursor.close()
                connection.close()
                messagebox.showinfo("Success","Menu item updated successfully.")
                edit_window.destroy()
                self.load_menu_items()

            except Exception as e:

                messagebox.showerror("Database Error",str(e))

        # Buttons
        button_frame = tk.Frame(edit_window)
        button_frame.pack()
        tk.Button(
            button_frame,text="Update",bg="#4B74D9",fg="white",activebackground="#365DB5",activeforeground="white",
            relief="flat", bd=0,font=("Segoe UI", 10, "bold"),cursor="hand2",command=update_menu_item).pack(
            side="left",
            ipadx=20,
            ipady=6
        )

        tk.Button(button_frame,text="Cancel",bg="#6B7280",fg="white",activebackground="#4B5563", activeforeground="white",
            relief="flat",bd=0,font=("Segoe UI", 10),cursor="hand2",command=edit_window.destroy).pack(
            side="left",
            padx=10,
            ipadx=15,
            ipady=6
        )

        item_entry.focus()

    # ==========================================
    # DELETE MENU ITEM
    # ==========================================

    def delete_menu_item(self):

        selected = self.menu_table.selection()

        if not selected:

            messagebox.showwarning("Select Menu Item", "Please select a menu item first.")

            return

        values = self.menu_table.item(selected[0],"values")

        menu_item_id = values[0]
        item_name = values[2]
        result = messagebox.askyesno( "Delete Menu Item","Are you sure you want to delete\n"+ item_name + "?")

        if not result:
            return

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                DELETE FROM MenuItems
                WHERE menuItem_id = ?
            """, (
                menu_item_id,
            ))

            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo("Success", "Menu item deleted successfully.")

            self.load_menu_items()

        except Exception as e:
            messagebox.showerror("Database Error",str(e)
            )