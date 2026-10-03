import tkinter as tk
from tkinter import ttk

from database.connection import get_connection

from ui.customer import CustomersPage
from ui.category import CategoriesPage
from ui.menu_items import MenuItemsPage
from ui.orders import OrdersPage
from ui.kitchen import KitchenPage
from ui.billing import BillingPage
from ui.payment import PaymentPage
from ui.inventory import InventoryPage
from ui.reports import ReportsPage
from ui.ingregients import IngredientsPage


class DashboardWindow:

    def __init__(self, root, user):

        self.root = root
        self.user = user

        # Window settings
        self.root.title("Hotel Management System")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)

        # Create dashboard
        self.create_dashboard()

    # -----------------------------------
    # Create Dashboard
    # -----------------------------------

    def create_dashboard(self):

        main_frame = tk.Frame(
            self.root,
            bg="#F5F6FA"
        )

        main_frame.pack(
            fill="both",
            expand=True
        )

        # -----------------------------------
        # Sidebar
        # -----------------------------------

        sidebar = tk.Frame(
            main_frame,
            bg="#172033",
            width=220
        )

        sidebar.pack(
            side="left",
            fill="y"
        )

        sidebar.pack_propagate(False)

        # Logo
        tk.Label(
            sidebar,
            text="HOTEL\nMANAGEMENT",
            bg="#172033",
            fg="white",
            font=("Segoe UI", 18, "bold"),
            justify="left"
        ).pack(
            anchor="w",
            padx=25,
            pady=(30, 50)
        )

        # Menu items
        menu_items = [
            "Dashboard",
            "Customers",
            "Categories",
            "Menu",
            "Orders",
            "Kitchen",
            "Billing",
            "Payment",
            "Inventory",
            "Ingredients",
            "Reports"
        ]

        # Create sidebar buttons
        for item in menu_items:

            if item == "Dashboard":

                button = tk.Button(
                    sidebar,
                    text=item,
                    font=("Segoe UI", 11, "bold"),
                    bg="#24314A",
                    fg="white",
                    activebackground="#2F405F",
                    activeforeground="white",
                    relief="flat",
                    bd=0,
                    anchor="w",
                    padx=25,
                    cursor="hand2",
                    command=self.show_dashboard
                )

            elif item == "Customers":

                button = tk.Button(
                    sidebar,
                    text=item,
                    font=("Segoe UI", 11),
                    bg="#2c3e50",
                    fg="white",
                    activebackground="#24314A",
                    activeforeground="white",
                    relief="flat",
                    bd=0,
                    anchor="w",
                    padx=25,
                    cursor="hand2",
                    command=self.open_customers
                )

            elif item == "Categories":

                button = tk.Button(
                    sidebar,
                    text=item,
                    font=("Segoe UI", 11),
                    bg="#2c3e50",
                    fg="white",
                    activebackground="#24314A",
                    activeforeground="white",
                    relief="flat",
                    bd=0,
                    anchor="w",
                    padx=25,
                    cursor="hand2",
                    command=self.open_categories
                )

            elif item == "Menu":

                button = tk.Button(
                    sidebar,
                    text=item,
                    font=("Segoe UI", 11),
                    bg="#2c3e50",
                    fg="white",
                    activebackground="#24314A",
                    activeforeground="white",
                    relief="flat",
                    bd=0,
                    anchor="w",
                    padx=25,
                    cursor="hand2",
                    command=self.open_menu_items
                )

            elif item == "Orders":

                button = tk.Button(
                    sidebar,
                    text=item,
                    font=("Segoe UI", 11),
                    bg="#2c3e50",
                    fg="white",
                    activebackground="#24314A",
                    activeforeground="white",
                    relief="flat",
                    bd=0,
                    anchor="w",
                    padx=25,
                    cursor="hand2",
                    command=self.open_orders
                )

            elif item == "Kitchen":

                button = tk.Button(
                    sidebar,
                    text=item,
                    font=("Segoe UI", 11),
                    bg="#2c3e50",
                    fg="white",
                    activebackground="#24314A",
                    activeforeground="white",
                    relief="flat",
                    bd=0,
                    anchor="w",
                    padx=25,
                    cursor="hand2",
                    command=self.open_kitchen
                )

            elif item == "Billing":

                button = tk.Button(
                    sidebar,
                    text=item,
                    font=("Segoe UI", 11),
                    bg="#2c3e50",
                    fg="white",
                    activebackground="#24314A",
                    activeforeground="white",
                    relief="flat",
                    bd=0,
                    anchor="w",
                    padx=25,
                    cursor="hand2",
                    command=self.open_billing
                )

            elif item == "Payment":

                button = tk.Button(
                    sidebar,
                    text=item,
                    font=("Segoe UI", 11),
                    bg="#2c3e50",
                    fg="white",
                    activebackground="#24314A",
                    activeforeground="white",
                    relief="flat",
                    bd=0,
                    anchor="w",
                    padx=25,
                    cursor="hand2",
                    command=self.open_payment
                )

            elif item == "Inventory":

                button = tk.Button(
                    sidebar,
                    text=item,
                    font=("Segoe UI", 11),
                    bg="#2c3e50",
                    fg="white",
                    activebackground="#24314A",
                    activeforeground="white",
                    relief="flat",
                    bd=0,
                    anchor="w",
                    padx=25,
                    cursor="hand2",
                    command=self.open_inventory
                )

            elif item == "Ingredients":

                button = tk.Button(
                    sidebar,
                    text=item,
                    font=("Segoe UI", 11),
                    bg="#2c3e50",
                    fg="white",
                    activebackground="#24314A",
                    activeforeground="white",
                    relief="flat",
                    bd=0,
                    anchor="w",
                    padx=25,
                    cursor="hand2",
                    command=self.open_ingredients
                )

            elif item == "Reports":

                button = tk.Button(
                    sidebar,
                    text=item,
                    font=("Segoe UI", 11),
                    bg="#2c3e50",
                    fg="white",
                    activebackground="#24314A",
                    activeforeground="white",
                    relief="flat",
                    bd=0,
                    anchor="w",
                    padx=25,
                    cursor="hand2",
                    command=self.open_reports
                )

            button.pack(
                fill="x",
                pady=2
            )

        # -----------------------------------
        # Content Area
        # -----------------------------------

        self.content = tk.Frame(
            main_frame,
            bg="#F5F6FA"
        )

        self.content.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Show dashboard
        self.show_dashboard()

    # -----------------------------------
    # Dashboard Page
    # -----------------------------------

    def show_dashboard(self):

        # Remove old content
        for widget in self.content.winfo_children():
            widget.destroy()

        # -----------------------------------
        # Header
        # -----------------------------------

        header = tk.Frame(
            self.content,
            bg="#F5F6FA"
        )

        header.pack(
            fill="x",
            padx=35,
            pady=(25, 15)
        )

        tk.Label(
            header,
            text="Dashboard",
            bg="#F5F6FA",
            fg="#172033",
            font=("Segoe UI", 24, "bold")
        ).pack(
            side="left"
        )

        tk.Label(
            header,
            text="Welcome, " + self.user.FullName,
            bg="#F5F6FA",
            fg="#6B7280",
            font=("Segoe UI", 10)
        ).pack(
            side="right"
        )

        # -----------------------------------
        # Get Dashboard Data
        # -----------------------------------

        data = self.get_dashboard_data()

        # -----------------------------------
        # Statistics Cards
        # -----------------------------------

        stats_frame = tk.Frame(
            self.content,
            bg="#F5F6FA"
        )

        stats_frame.pack(
            fill="x",
            padx=35
        )

        self.create_card(
            stats_frame,
            "Today's Orders",
            str(data["today_orders"]),
            0
        )

        self.create_card(
            stats_frame,
            "Today's Sales",
            "₹" + f'{data["today_sales"]:.2f}',
            1
        )

        self.create_card(
            stats_frame,
            "Pending Orders",
            str(data["pending_orders"]),
            2
        )

        self.create_card(
            stats_frame,
            "Low Stock Items",
            str(data["low_stock"]),
            3
        )

        # -----------------------------------
        # Second Row Cards
        # -----------------------------------

        second_stats = tk.Frame(
            self.content,
            bg="#F5F6FA"
        )

        second_stats.pack(
            fill="x",
            padx=35,
            pady=(15, 0)
        )

        self.create_card(
            second_stats,
            "Total Customers",
            str(data["total_customers"]),
            0
        )

        self.create_card(
            second_stats,
            "Total Menu Items",
            str(data["total_menu_items"]),
            1
        )

        self.create_card(
            second_stats,
            "Total Bills",
            str(data["total_bills"]),
            2
        )

        self.create_card(
            second_stats,
            "Total Payments",
            "₹" + f'{data["total_payments"]:.2f}',
            3
        )

        # -----------------------------------
        # Recent Orders Section
        # -----------------------------------

        recent_frame = tk.Frame(
            self.content,
            bg="white"
        )

        recent_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=20
        )

        tk.Label(
            recent_frame,
            text="Recent Orders",
            bg="white",
            fg="#172033",
            font=("Segoe UI", 16, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(15, 10)
        )

        # Treeview container
        tree_frame = tk.Frame(
            recent_frame,
            bg="white"
        )

        tree_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 15)
        )

        columns = (
            "OrderID",
            "Customer",
            "OrderDate",
            "Status",
            "TotalAmount"
        )

        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            height=7
        )

        tree.heading(
            "OrderID",
            text="Order ID"
        )

        tree.heading(
            "Customer",
            text="Customer"
        )

        tree.heading(
            "OrderDate",
            text="Order Date"
        )

        tree.heading(
            "Status",
            text="Status"
        )

        tree.heading(
            "TotalAmount",
            text="Amount"
        )

        tree.column(
            "OrderID",
            width=80,
            anchor="center"
        )

        tree.column(
            "Customer",
            width=200
        )

        tree.column(
            "OrderDate",
            width=180
        )

        tree.column(
            "Status",
            width=120,
            anchor="center"
        )

        tree.column(
            "TotalAmount",
            width=120,
            anchor="e"
        )

        scrollbar = ttk.Scrollbar(
            tree_frame,
            orient="vertical",
            command=tree.yview
        )

        tree.configure(
            yscrollcommand=scrollbar.set
        )

        tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # Load recent orders
        for row in data["recent_orders"]:

            tree.insert(
                "",
                "end",
                values=(
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    f"₹{float(row[4]):.2f}"
                )
            )

    # -----------------------------------
    # Get Dashboard Data
    # -----------------------------------

    def get_dashboard_data(self):

        data = {
            "today_orders": 0,
            "today_sales": 0,
            "pending_orders": 0,
            "low_stock": 0,
            "total_customers": 0,
            "total_menu_items": 0,
            "total_bills": 0,
            "total_payments": 0,
            "recent_orders": []
        }

        connection = None

        try:

            connection = get_connection()
            cursor = connection.cursor()

            # Today's Orders
            cursor.execute("""
                SELECT COUNT(*)
                FROM Orders
                WHERE CAST(OrderDate AS DATE) = CAST(GETDATE() AS DATE)
            """)

            data["today_orders"] = cursor.fetchone()[0]

            # Today's Sales
            cursor.execute("""
                SELECT ISNULL(SUM(TotalAmount), 0)
                FROM Bills
                WHERE CAST(BillDate AS DATE) = CAST(GETDATE() AS DATE)
            """)

            data["today_sales"] = float(
                cursor.fetchone()[0] or 0
            )

            # Pending Orders
            cursor.execute("""
                SELECT COUNT(*)
                FROM Orders
                WHERE Status = 'Pending'
            """)

            data["pending_orders"] = cursor.fetchone()[0]

            # Low Stock Items
            cursor.execute("""
                SELECT COUNT(*)
                FROM Inventory
                WHERE Quantity <= MinimumQuantity
            """)

            data["low_stock"] = cursor.fetchone()[0]

            # Total Customers
            cursor.execute("""
                SELECT COUNT(*)
                FROM Customers
            """)

            data["total_customers"] = cursor.fetchone()[0]

            # Total Menu Items
            cursor.execute("""
                SELECT COUNT(*)
                FROM MenuItems
            """)

            data["total_menu_items"] = cursor.fetchone()[0]

            # Total Bills
            cursor.execute("""
                SELECT COUNT(*)
                FROM Bills
            """)

            data["total_bills"] = cursor.fetchone()[0]

            # Total Payments
            cursor.execute("""
                SELECT ISNULL(SUM(Amount), 0)
                FROM Payments
            """)

            data["total_payments"] = float(
                cursor.fetchone()[0] or 0
            )

            # Recent Orders
            cursor.execute("""
                SELECT TOP 10
                    o.OrderID,
                    c.full_name,
                    o.OrderDate,
                    o.Status,
                    o.TotalAmount
                FROM Orders o
                INNER JOIN Customers c
                    ON o.customer_id = c.customer_id
                ORDER BY o.OrderID DESC
            """)

            data["recent_orders"] = cursor.fetchall()

            connection.close()

        except Exception as e:

            if connection:
                connection.close()

            print("Dashboard Error:", e)

        return data

    # -----------------------------------
    # Create Dashboard Card
    # -----------------------------------

    def create_card(
        self,
        parent,
        title,
        value,
        column
    ):

        card = tk.Frame(
            parent,
            bg="white",
            height=105
        )

        card.grid(
            row=0,
            column=column,
            padx=6,
            sticky="nsew"
        )

        parent.grid_columnconfigure(
            column,
            weight=1
        )

        tk.Label(
            card,
            text=title,
            bg="white",
            fg="#6B7280",
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 3)
        )

        tk.Label(
            card,
            text=value,
            bg="white",
            fg="#172033",
            font=("Segoe UI", 20, "bold")
        ).pack(
            anchor="w",
            padx=18
        )

    # -----------------------------------
    # Open Customers
    # -----------------------------------

    def open_customers(self):

        for widget in self.content.winfo_children():
            widget.destroy()

        CustomersPage(self.content)

    # -----------------------------------
    # Open Categories
    # -----------------------------------

    def open_categories(self):

        for widget in self.content.winfo_children():
            widget.destroy()

        CategoriesPage(self.content)

    # -----------------------------------
    # Open Menu Items
    # -----------------------------------

    def open_menu_items(self):

        for widget in self.content.winfo_children():
            widget.destroy()

        MenuItemsPage(self.content)

    # -----------------------------------
    # Open Orders
    # -----------------------------------

    def open_orders(self):

        for widget in self.content.winfo_children():
            widget.destroy()

        OrdersPage(self.content)

    # -----------------------------------
    # Open Kitchen
    # -----------------------------------

    def open_kitchen(self):

        for widget in self.content.winfo_children():
            widget.destroy()

        KitchenPage(self.content)

    # -----------------------------------
    # Open Billing
    # -----------------------------------

    def open_billing(self):

        for widget in self.content.winfo_children():
            widget.destroy()

        BillingPage(self.content)

    # -----------------------------------
    # Open Payment
    # -----------------------------------

    def open_payment(self):

        for widget in self.content.winfo_children():
            widget.destroy()

        PaymentPage(self.content)

    # -----------------------------------
    # Open Inventory
    # -----------------------------------

    def open_inventory(self):

        for widget in self.content.winfo_children():
            widget.destroy()

        InventoryPage(self.content)

    # -----------------------------------
    # Open Ingredients
    # -----------------------------------

    def open_ingredients(self):

        for widget in self.content.winfo_children():
            widget.destroy()

        IngredientsPage(self.content)

    # -----------------------------------
    # Open Reports
    # -----------------------------------

    def open_reports(self):

        for widget in self.content.winfo_children():
            widget.destroy()

        ReportsPage(self.content)
