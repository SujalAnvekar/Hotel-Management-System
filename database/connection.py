import pyodbc

server = "LAPTOP-12GALTT6\\SQLEXPRESS01"
database = "Hotel_Management"


def get_connection():
    try:
        connection = pyodbc.connect(
            "DRIVER={SQL Server};"
            f"SERVER={server};"
            f"DATABASE={database};"
            "Trusted_Connection=yes;"
        )

        print("Database connected successfully...")
        return connection

    except pyodbc.Error as e:
        print("Database connection error:", e)
        return None