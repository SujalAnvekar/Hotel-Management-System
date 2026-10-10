### Hotel Management System

A desktop-based Hotel Management System developed using **Python, Tkinter, and Microsoft SQL Server** to streamline food service operations, including customer management, menu management, order processing, kitchen operations, billing, payments, and inventory tracking.

The system automates ingredient stock deduction after successful payment based on predefined recipes and highlights low-stock items to support efficient inventory management.

---
## 📌 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Application Workflow](#-application-workflow)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Database Design](#-database-design)
- [Installation and Setup](#-installation-and-setup)
- [How to Run](#-how-to-run)
- [Inventory Automation](#-inventory-automation)
- [Future Enhancements](#-future-enhancements)
- [Author](#-author)

---

## 📖 Overview
The Hotel Management System provides a centralized desktop application for managing customer orders and related hotel operations.

It connects order processing, kitchen status tracking, billing, payment recording, and inventory management into a single workflow.

The application uses **Tkinter** to provide a graphical user interface and **Microsoft SQL Server** to store application data.

### Project Objectives
- Simplify daily hotel food service operations.
- Maintain organized customer, menu, and order records.
- Track order preparation and serving status.
- Generate bills with tax and discount calculations.
- Automate ingredient stock deduction after successful payment.
- Monitor inventory levels and identify low-stock items.

## ✨ Key Features

### 🔐 Admin Login
- Admin login system.
- Database-based credential validation.
- Last login tracking.

### 👥 Customer Management
- Add new customers.
- View and search customer records.
- Update customer information.
- Delete customer records.

### 🍽️ Category and Menu Management
- Create and manage menu categories.
- Add menu items with prices.
- Assign menu items to categories.
- Search, update, and delete records.

### 🧾 Order Management
- Select customers and menu items.
- Add multiple items to an order.
- Specify item quantities.
- Calculate item amounts and order totals.
- Save orders and order details in the database.

### 👨‍🍳 Kitchen Management
- View active orders.
- Track order preparation status.
- Update order status through the kitchen workflow.

### 💰 Billing Management
- Generate bills for served orders.
- Calculate subtotal, tax, discount, and final amount.
- Prevent duplicate bills for the same order.

### 💳 Payment Management
- Record payments using Cash, Card, or UPI.
- Associate payments with bills.
- Mark orders as completed after successful payment.

### 📦 Inventory Management
- Add, edit, delete, and search inventory items.
- Track current and minimum stock quantities.
- Highlight low-stock items in red.
- Monitor ingredient availability.

### 🧪 Ingredients and Recipes
- Associate ingredients with menu items.
- Define ingredient quantities required for each menu item.
- Calculate ingredient consumption based on order quantities.
- Support automatic inventory deduction after successful payment.

### 📊 Reports and Dashboard
- Provide a central dashboard for application navigation.
- Support business monitoring through reports.

## 🔄 Application Workflow

The following flow represents the main operational process of the system.

```text
                    ┌──────────────────┐
                    │    Admin Login   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Dashboard     │
                    └────────┬─────────┘
                             │
                             ▼
              ┌────────────────────────────┐
              │ Manage Customers, Categories│
              │         and Menu Items      │
              └──────────────┬─────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Create Order   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │      Pending     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │    Preparing     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │       Ready      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │      Served      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Generate Bill  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Record Payment  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Payment Success  │
                    └────────┬─────────┘
                             │
                             ▼
              ┌────────────────────────────┐
              │ Mark Order as Completed    │
              │ Deduct Recipe Ingredients  │
              │ Update Inventory           │
              └──────────────┬─────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Reports / Review │
                    └──────────────────┘
