USE HotelManagement;
GO


/* =========================================================
   1. USERS
   ========================================================= */

CREATE TABLE Users
(
    UserID INT IDENTITY(1,1) PRIMARY KEY,
    Username NVARCHAR(50) NOT NULL UNIQUE,
    Password NVARCHAR(100) NOT NULL,
    FullName NVARCHAR(100) NOT NULL,
    IsActive BIT NOT NULL DEFAULT 1,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
    LastLogin DATETIME2 NULL
);
GO


/* =========================================================
   2. CUSTOMERS
   ========================================================= */

CREATE TABLE Customers
(
    customer_id INT IDENTITY(1,1) PRIMARY KEY,
    full_name NVARCHAR(100) NOT NULL,
    phone NVARCHAR(20) NOT NULL,
    createdAt DATETIME2 NOT NULL DEFAULT GETDATE()
);
GO


/* =========================================================
   3. CATEGORIES
   ========================================================= */

CREATE TABLE Categories
(
    category_id INT IDENTITY(1,1) PRIMARY KEY,
    category_name NVARCHAR(100) NOT NULL,
    createdAt DATETIME2 NOT NULL DEFAULT GETDATE()
);
GO


/* =========================================================
   4. MENU ITEMS
   ========================================================= */

CREATE TABLE MenuItems
(
    menuItem_id INT IDENTITY(1,1) PRIMARY KEY,
    category_id INT NOT NULL,
    itemName NVARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    createdAt DATETIME2 NOT NULL DEFAULT GETDATE(),

    FOREIGN KEY (category_id)
        REFERENCES Categories(category_id)
);
GO


/* =========================================================
   5. ORDERS
   ========================================================= */

CREATE TABLE Orders
(
    OrderID INT IDENTITY(1,1) PRIMARY KEY,
    customer_id INT NOT NULL,
    OrderDate DATETIME2 NOT NULL DEFAULT GETDATE(),
    Status NVARCHAR(30) NOT NULL DEFAULT 'Pending',
    TotalAmount DECIMAL(10,2) NOT NULL DEFAULT 0,

    FOREIGN KEY (customer_id)
        REFERENCES Customers(customer_id)
);
GO


/* =========================================================
   6. ORDER ITEMS
   ========================================================= */

CREATE TABLE OrderItems
(
    OrderItemID INT IDENTITY(1,1) PRIMARY KEY,
    OrderID INT NOT NULL,
    menuItem_id INT NOT NULL,
    Quantity INT NOT NULL,
    Price DECIMAL(10,2) NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,

    FOREIGN KEY (OrderID)
        REFERENCES Orders(OrderID),

    FOREIGN KEY (menuItem_id)
        REFERENCES MenuItems(menuItem_id)
);
GO


/* =========================================================
   7. KITCHEN HISTORY
   ========================================================= */

CREATE TABLE KitchenHistory
(
    KitchenHistoryID INT IDENTITY(1,1) PRIMARY KEY,
    OrderID INT NOT NULL,
    Status NVARCHAR(30) NOT NULL,
    UpdatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),

    FOREIGN KEY (OrderID)
        REFERENCES Orders(OrderID)
);
GO


/* =========================================================
   8. BILLS
   ========================================================= */

CREATE TABLE Bills
(
    BillID INT IDENTITY(1,1) PRIMARY KEY,
    OrderID INT NOT NULL,
    BillDate DATETIME2 NOT NULL DEFAULT GETDATE(),
    SubTotal DECIMAL(10,2) NOT NULL,
    TaxAmount DECIMAL(10,2) NOT NULL DEFAULT 0,
    DiscountAmount DECIMAL(10,2) NOT NULL DEFAULT 0,
    TotalAmount DECIMAL(10,2) NOT NULL,

    FOREIGN KEY (OrderID)
        REFERENCES Orders(OrderID)
);
GO


/* =========================================================
   9. PAYMENTS
   ========================================================= */

CREATE TABLE Payments
(
    PaymentID INT IDENTITY(1,1) PRIMARY KEY,
    BillID INT NOT NULL,
    PaymentDate DATETIME2 NOT NULL DEFAULT GETDATE(),
    PaymentMethod NVARCHAR(30) NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,

    FOREIGN KEY (BillID)
        REFERENCES Bills(BillID)
);
GO


/* =========================================================
   10. INVENTORY
   ========================================================= */

CREATE TABLE Inventory
(
    InventoryID INT IDENTITY(1,1) PRIMARY KEY,
    ItemName NVARCHAR(100) NOT NULL,
    Unit NVARCHAR(30) NOT NULL,
    Quantity DECIMAL(10,2) NOT NULL DEFAULT 0,
    MinimumQuantity DECIMAL(10,2) NOT NULL DEFAULT 0,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE()
);
GO


/* =========================================================
   11. MENU ITEM INGREDIENTS / RECIPES
   ========================================================= */

CREATE TABLE MenuItemIngredients
(
    MenuItemIngredientID INT IDENTITY(1,1) PRIMARY KEY,
    menuItem_id INT NOT NULL,
    InventoryID INT NOT NULL,
    QuantityUsed DECIMAL(10,3) NOT NULL,

    FOREIGN KEY (menuItem_id)
        REFERENCES MenuItems(menuItem_id),

    FOREIGN KEY (InventoryID)
        REFERENCES Inventory(InventoryID)
);
GO