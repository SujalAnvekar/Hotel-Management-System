import tkinter as tk
from tkinter import ttk

from ui.customer import CustomersPage
from ui.category import CategoriesPage
from ui.menu_items import MenuItemsPage
from ui.orders import OrdersPage
from ui.kitchen import KitchenPage


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

        # Main frame
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
            "Inventory",
            "Suppliers",
            "Expenses",
            "Reports",
            "Settings"
        ]

        # Create buttons
        for item in menu_items:

            if item == "Customers":

                button = tk.Button(
                    sidebar,
                    text=item,
                    bg="#172033",
                    fg="white",
                    activebackground="#24314A",
                    activeforeground="white",
                    relief="flat",
                    bd=0,
                    anchor="w",
                    padx=25,
                    font=("Segoe UI", 10),
                    cursor="hand2",
                    command=self.open_customers
                )
            elif item == 'Categories':
                 button = tk.Button(
            sidebar,
            text=item,
            bg="#172033",
            fg="white",
            activebackground="#24314A",
            activeforeground="white",
            relief="flat",
            bd=0,
            anchor="w",
            padx=25,
            font=("Segoe UI", 10),
            cursor="hand2",
            command=self.open_categories
        )
            elif item == "Menu":

                button = tk.Button(
                    sidebar,
                    text=item,
                    bg="#172033",
                    fg="white",
                    activebackground="#24314A",
                    activeforeground="white",
                    relief="flat",
                    bd=0,
                    anchor="w",
                    padx=25,
                    font=("Segoe UI", 10),
                    cursor="hand2",
                    command=self.open_menu_items
                )
            elif item == "Orders":

                    button = tk.Button(
                        sidebar,
                        text=item,
                        font=("Arial", 12),
                        bg="#2c3e50",
                        fg="white",
                        relief="flat",
                        anchor="w",
                        command=self.open_orders
                    )
            elif item == "Kitchen":

                button = tk.Button(
                    sidebar,
                    text=item,
                    font=("Arial", 12),
                    bg="#2c3e50",
                    fg="white",
                    relief="flat",
                    anchor="w",
                    command=self.open_kitchen
                )
            else:

                button = tk.Button(
                    sidebar,
                    text=item,
                    bg="#172033",
                    fg="white",
                    activebackground="#24314A",
                    activeforeground="white",
                    relief="flat",
                    bd=0,
                    anchor="w",
                    padx=25,
                    font=("Segoe UI", 10),
                    cursor="hand2"
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

        # Header
        header = tk.Frame(
            self.content,
            bg="#F5F6FA"
        )

        header.pack(
            fill="x",
            padx=35,
            pady=(30, 20)
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
        # Statistics
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
            "0",
            0
        )

        self.create_card(
            stats_frame,
            "Today's Sales",
            "₹0",
            1
        )

        self.create_card(
            stats_frame,
            "Pending Orders",
            "0",
            2
        )

        self.create_card(
            stats_frame,
            "Low Stock Items",
            "0",
            3
        )

        # -----------------------------------
        # Welcome Box
        # -----------------------------------

        welcome = tk.Frame(
            self.content,
            bg="white"
        )

        welcome.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=30
        )

        tk.Label(
            welcome,
            text="Hotel Management Dashboard",
            bg="white",
            fg="#172033",
            font=("Segoe UI", 18, "bold")
        ).pack(
            anchor="w",
            padx=25,
            pady=(25, 10)
        )

        tk.Label(
            welcome,
            text="Use the menu on the left to manage customers, "
                 "orders, kitchen, billing, inventory and reports.",
            bg="white",
            fg="#6B7280",
            font=("Segoe UI", 11),
            wraplength=700,
            justify="left"
        ).pack(
            anchor="w",
            padx=25
        )

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
            height=120
        )

        card.grid(
            row=0,
            column=column,
            padx=7,
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
            padx=20,
            pady=(20, 5)
        )

        tk.Label(
            card,
            text=value,
            bg="white",
            fg="#172033",
            font=("Segoe UI", 22, "bold")
        ).pack(
            anchor="w",
            padx=20
        )

    # -----------------------------------
    # Open Customers
    # -----------------------------------

    def open_customers(self):

        # Remove dashboard content
        for widget in self.content.winfo_children():

            widget.destroy()

        # Open Customers page
        CustomersPage(self.content)

    def open_categories(self):

        for widget in self.content.winfo_children():
            widget.destroy()

        CategoriesPage(self.content)

    def open_menu_items(self):

        for widget in self.content.winfo_children():
            widget.destroy()

        MenuItemsPage(self.content)

    def open_orders(self):

        for widget in self.content.winfo_children():
            widget.destroy()

        OrdersPage(self.content)

    def open_kitchen(self):

        for widget in self.content.winfo_children():
            widget.destroy()

        KitchenPage(self.content)