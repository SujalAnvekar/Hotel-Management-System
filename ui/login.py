import tkinter as tk
from tkinter import ttk, messagebox
from ui.dashboard import DashboardWindow
from database.connection import get_connection


class LoginWindow:
    def __init__(self, root):
        self.root = root

        self.root.title("Hotel Management System - Login")
        self.root.geometry("500x500+500+200")
        self.root.resizable(False, False)

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()

        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 24, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            font=("Segoe UI", 11)
        )

        style.configure(
            "TButton",
            font=("Segoe UI", 11, "bold"),
            padding=10
        )

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=40)
        main_frame.pack(fill="both", expand=True)

        # Title
        ttk.Label(
            main_frame,
            text="Hotel Management",
            style="Title.TLabel"
        ).pack(pady=(40, 5))

        ttk.Label(
            main_frame,
            text="Admin Login",
            style="Subtitle.TLabel"
        ).pack(pady=(0, 35))

        # Username
        ttk.Label(
            main_frame,
            text="Username"
        ).pack(anchor="w")

        self.username_entry = ttk.Entry(
            main_frame,
            font=("Segoe UI", 12)
        )
        self.username_entry.pack(
            fill="x",
            pady=(5, 20)
        )

        # Password
        ttk.Label(
            main_frame,
            text="Password"
        ).pack(anchor="w")

        self.password_entry = ttk.Entry(
            main_frame,
            show="*",
            font=("Segoe UI", 12)
        )
        self.password_entry.pack(
            fill="x",
            pady=(5, 30)
        )

        # Login button
        ttk.Button(
            main_frame,
            text="LOGIN",
            command=self.login
        ).pack(fill="x")

        # Enter key
        self.root.bind("<Return>", lambda event: self.login())

        self.username_entry.focus()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning(
                "Login",
                "Please enter username and password."
            )
            return

        connection = None

        try:
            connection = get_connection()

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT UserID, Username, FullName
                FROM Users
                WHERE Username = ?
                  AND Password = ?
                  AND IsActive = 1
                """,
                (username, password)
            )

            user = cursor.fetchone()

            if user:
                cursor.execute(
                    """
                    UPDATE Users
                    SET LastLogin = GETDATE()
                    WHERE UserID = ?
                    """,
                    (user.UserID,)
                )

                connection.commit()

                messagebox.showinfo(
                    "Login Successful",
                    f"Welcome, {user.FullName}!"
                )

                self.root.destroy()

                # Dashboard will be connected here next.

                dashboard_root=tk.Tk()

                DashboardWindow(
                    dashboard_root,user
                )

                dashboard_root.mainloop()


            else:
                messagebox.showerror(
                    "Login Failed",
                    "Invalid Credentials."
                )

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:
            if connection:
                connection.close()