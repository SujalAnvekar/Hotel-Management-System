import tkinter as tk
from tkinter import ttk, messagebox

from database.connection import get_connection


class CategoriesPage:

    def __init__(self, parent):

        self.parent = parent

        self.frame = tk.Frame(parent, bg="#F5F6FA")
        self.frame.pack(fill="both",expand=True)
        self.create_widgets()
        self.load_categories()

    # CREATE PAGE

    def create_widgets(self):

        # Title
        title_frame = tk.Frame(self.frame,bg="#F5F6FA")
        title_frame.pack(fill="x",padx=30,pady=(25, 15))
        tk.Label(title_frame,text="Categories",bg="#F5F6FA",fg="#172033",font=("Segoe UI", 24, "bold")).pack(side="left")

        # Search Area
        search_frame = tk.Frame(self.frame,bg="#F5F6FA")
        search_frame.pack(fill="x",padx=30,pady=(0, 15))
        tk.Label(search_frame,text="Search:",bg="#F5F6FA",fg="#172033",font=("Segoe UI", 10)).pack(side="left",padx=(0, 8))
        self.search_entry = tk.Entry(search_frame,font=("Segoe UI", 10),width=35)
        self.search_entry.pack(side="left",ipady=6)

        # Search
        tk.Button(search_frame,text="Search",bg="#4B74D9",fg="white",activebackground="#365DB5",activeforeground="white",
        relief="flat",bd=0,font=("Segoe UI", 10),cursor="hand2",command=self.search_category).pack(side="left",padx=8,ipadx=10,ipady=5)

        # Show All
        tk.Button(search_frame,text="Show All",bg="#6B7280",fg="white",activebackground="#4B5563",activeforeground="white",
        relief="flat",bd=0,font=("Segoe UI", 10),cursor="hand2",command=self.load_categories).pack(side="left",ipadx=10,ipady=5)

        # Add Category
        tk.Button(search_frame,text="+ Add Category",bg="#E87524",fg="white",activebackground="#C95F17",activeforeground="white",
        relief="flat",bd=0,font=("Segoe UI", 10, "bold"),cursor="hand2",command=self.add_category).pack(side="right",ipadx=10,ipady=5)

        # Table

        table_frame = tk.Frame(self.frame,bg="white")
        table_frame.pack(fill="both",expand=True,padx=30,pady=(0, 15))
        scrollbar = ttk.Scrollbar(table_frame,orient="vertical")
        scrollbar.pack(side="right",fill="y")
        self.category_table = ttk.Treeview(table_frame,
            columns=(
                "category_id",
                "category_name",
                "CreatedAt"
            ),
            show="headings",
            yscrollcommand=scrollbar.set
        )

        self.category_table.pack(fill="both",expand=True)
        scrollbar.config(command=self.category_table.yview)

        # Headings
        self.category_table.heading("category_id",text="ID")
        self.category_table.heading("category_name",text="Category Name")
        self.category_table.heading( "CreatedAt", text="Created At")

        # Column widths
        self.category_table.column("category_id",width=80,anchor="center")
        self.category_table.column("category_name",width=300)
        self.category_table.column( "CreatedAt", width=200)

        # Bottom Buttons

        button_frame = tk.Frame(self.frame, bg="#F5F6FA")
        button_frame.pack(fill="x",padx=30,pady=(0, 25))

        # Edit
        tk.Button(button_frame,text="Edit Category",bg="#4B74D9",fg="white",activebackground="#365DB5",activeforeground="white",
        relief="flat",bd=0,font=("Segoe UI", 10),cursor="hand2",command=self.edit_category).pack(side="left",ipadx=12,ipady=6)

        # Delete
        tk.Button(button_frame,text="Delete Category",bg="#D84A4A",fg="white",activebackground="#B83232",activeforeground="white",
        relief="flat",bd=0,font=("Segoe UI", 10),cursor="hand2",command=self.delete_category).pack(side="left",padx=10,ipadx=12,ipady=6)

    # LOAD CATEGORIES

    def load_categories(self):

        # Clear table
        for row in self.category_table.get_children():

            self.category_table.delete(row)

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    category_id,
                    category_name,
                    CreatedAt
                FROM Categories
                ORDER BY category_id DESC
            """)

            rows = cursor.fetchall()

            for row in rows:

                self.category_table.insert("","end",
                    values=(
                        row[0],
                        row[1],
                        row[2]
                    )
                )

            cursor.close()
            connection.close()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    # SEARCH CATEGORY

    def search_category(self):

        search_text = self.search_entry.get().strip()

        if search_text == "":
            self.load_categories()
            return

        # Clear table
        for row in self.category_table.get_children():
            self.category_table.delete(row)

        try:

            connection = get_connection()
            cursor = connection.cursor()

            search_value = "%" + search_text + "%"

            cursor.execute("""
                SELECT
                    category_id,
                    category_name,
                    CreatedAt
                FROM Categories
                WHERE category_name LIKE ?
                ORDER BY category_id DESC
            """, (search_value,))

            rows = cursor.fetchall()

            for row in rows:
                self.category_table.insert("","end",
                    values=(
                        row[0],
                        row[1],
                        row[2]
                    )
                )

            cursor.close()
            connection.close()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

    # ADD CATEGORY

    def add_category(self):

        add_window = tk.Toplevel(self.frame)
        add_window.title("Add Category")
        add_window.geometry("450x250")
        add_window.resizable(False,False)
        add_window.transient(self.frame.winfo_toplevel())

        # Title
        tk.Label(add_window,text="Add Category",font=("Segoe UI", 18, "bold"),fg="#172033").pack(pady=(25, 20))

        # Category Name
        tk.Label(add_window,text="Category Name",font=("Segoe UI", 10)).pack(anchor="w",padx=40)
        category_entry = tk.Entry(add_window,font=("Segoe UI", 10))
        category_entry.pack(fill="x",padx=40,pady=(5, 20),ipady=6)

        # Save function
        def save_category():

            category_name = category_entry.get().strip()

            if category_name == "":
                messagebox.showwarning(
                    "Validation",
                    "Please enter category name.")

                category_entry.focus()

                return

            try:

                connection = get_connection()
                cursor = connection.cursor()

                cursor.execute("""
                    INSERT INTO Categories
                    (
                        category_name
                    )
                    VALUES (?)
                """, (category_name,))

                connection.commit()

                cursor.close()
                connection.close()

                messagebox.showinfo(
                    "Success",
                    "Category added successfully."
                )

                add_window.destroy()

                self.load_categories()

            except Exception as e:

                messagebox.showerror(
                    "Database Error",
                    str(e)
                )

        # Buttons
        button_frame = tk.Frame(add_window)
        button_frame.pack()

        tk.Button(button_frame,text="Save",bg="#1F9D68",fg="white",activebackground="#167A50",activeforeground="white",
        relief="flat",bd=0,font=("Segoe UI", 10, "bold"),cursor="hand2",command=save_category).pack(side="left",ipadx=20,ipady=6)

        tk.Button(button_frame,text="Cancel",bg="#6B7280",fg="white",activebackground="#4B5563",activeforeground="white",
        relief="flat",bd=0,font=("Segoe UI", 10),cursor="hand2",command=add_window.destroy).pack(side="left",padx=10,ipadx=15,ipady=6)

        category_entry.focus()

    # EDIT CATEGORY

    def edit_category(self):

        selected = self.category_table.selection()

        if not selected:

            messagebox.showwarning(
                "Select Category",
                "Please select a category first."
            )

            return

        values = self.category_table.item(selected[0],"values")
        category_id = values[0]
        old_name = values[1]

        # Edit window
        edit_window = tk.Toplevel(self.frame)
        edit_window.title("Edit Category")
        edit_window.geometry("450x250")
        edit_window.resizable(False,False)

        # Title
        tk.Label(edit_window,text="Edit Category",font=("Segoe UI", 18, "bold"),fg="#172033").pack(pady=(25, 20))

        # Name
        tk.Label(edit_window,text="Category Name",font=("Segoe UI", 10)).pack(anchor="w",padx=40)

        category_entry = tk.Entry(edit_window,font=("Segoe UI", 10))
        category_entry.pack(fill="x",padx=40,pady=(5, 20),ipady=6)
        category_entry.insert(0,old_name)

        # Update
        def update_category():

            category_name = category_entry.get().strip()

            if category_name == "":

                messagebox.showwarning(
                    "Validation",
                    "Please enter category name."
                )

                return

            try:

                connection = get_connection()
                cursor = connection.cursor()

                cursor.execute("""
                    UPDATE Categories
                    SET category_name = ?
                    WHERE category_id = ?
                """, (category_name,category_id))

                connection.commit()

                cursor.close()
                connection.close()

                messagebox.showinfo(
                    "Success",
                    "Category updated successfully."
                )

                edit_window.destroy()

                self.load_categories()

            except Exception as e:

                messagebox.showerror(
                    "Database Error",
                    str(e)
                )

        # Buttons
        button_frame = tk.Frame(edit_window)
        button_frame.pack()
        tk.Button(button_frame,text="Update",bg="#4B74D9",fg="white",activebackground="#365DB5",activeforeground="white",
        relief="flat",bd=0,font=("Segoe UI", 10, "bold"),cursor="hand2",command=update_category).pack(side="left",ipadx=20,ipady=6)

        tk.Button(button_frame,text="Cancel",bg="#6B7280",fg="white",activebackground="#4B5563",activeforeground="white",
        relief="flat",bd=0,font=("Segoe UI", 10),cursor="hand2",command=edit_window.destroy).pack(side="left",padx=10,ipadx=15,ipady=6)

        category_entry.focus()

    # DELETE CATEGORY

    def delete_category(self):

        selected = self.category_table.selection()

        if not selected:

            messagebox.showwarning(
                "Select Category",
                "Please select a category first."
            )

            return

        values = self.category_table.item(
            selected[0],
            "values"
        )

        category_id = values[0]
        category_name = values[1]

        # Confirmation
        result = messagebox.askyesno(
            "Delete Category",
            "Are you sure you want to delete\n"
            + category_name
            + "?"
        )

        if not result:
            return

        try:

            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                DELETE FROM Categories
                WHERE category_id = ?
            """, (category_id,))

            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Category deleted successfully."
            )

            self.load_categories()

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )