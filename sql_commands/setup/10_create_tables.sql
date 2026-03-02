CREATE TABLE Categories (
    CategoryID INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    CategoryName VARCHAR(15) NOT NULL,
    Description TEXT
);

CREATE INDEX IDX_Categories_CategoryName ON Categories (CategoryName);

CREATE TABLE Customers (
    CustomerID VARCHAR(5) PRIMARY KEY,
    CompanyName VARCHAR(40) NOT NULL,
    ContactName VARCHAR(30),
    ContactTitle VARCHAR(30),
    Address VARCHAR(60),
    City VARCHAR(15),
    Region VARCHAR(15),
    PostalCode VARCHAR(10),
    Country VARCHAR(15),
    Phone VARCHAR(24),
    Fax VARCHAR(24)
);

CREATE INDEX IDX_Customers_City ON Customers (City);

CREATE INDEX IDX_Customers_CompanyName ON Customers (CompanyName);

CREATE INDEX IDX_Customers_PostalCode ON Customers (PostalCode);

CREATE INDEX IDX_Customers_Region ON Customers (Region);

CREATE TABLE Employees (
    EmployeeID INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    LastName VARCHAR(20) NOT NULL,
    FirstName VARCHAR(10) NOT NULL,
    Title VARCHAR(30),
    TitleOfCourtesy VARCHAR(25),
    BirthDate DATE,
    HireDate DATE,
    Address VARCHAR(60),
    City VARCHAR(15),
    Region VARCHAR(15),
    PostalCode VARCHAR(10),
    Country VARCHAR(15)
);

CREATE INDEX IDX_Employees_LastName ON Employees (LastName);

CREATE INDEX IDX_Employees_PostalCode ON Employees (PostalCode);

CREATE TABLE EmployeeTerritories (
    EmployeeID INTEGER NOT NULL,
    TerritoryID VARCHAR(20) NOT NULL,
    CONSTRAINT PK_EmployeeTerritories PRIMARY KEY (EmployeeID, TerritoryID)
);

CREATE TABLE OrderDetails (
    OrderID INTEGER NOT NULL,
    ProductID INTEGER NOT NULL,
    UnitPrice DECIMAL(10,4) NOT NULL DEFAULT 0,
    Quantity SMALLINT NOT NULL DEFAULT 1,
    Discount double precision NOT NULL DEFAULT 0,
    CONSTRAINT PK_OrderDetails PRIMARY KEY (OrderID, ProductID)
);

CREATE TABLE Orders (
    OrderID INTEGER NOT NULL,
    CustomerID VARCHAR(5),
    EmployeeID INTEGER,
    OrderDate DATE,
    RequiredDate DATE,
    ShippedDate DATE,
    ShipVia INTEGER,
    Freight DECIMAL(10,4) DEFAULT 0,
    ShipName VARCHAR(40),
    ShipAddress VARCHAR(60),
    ShipCity VARCHAR(15),
    ShipRegion VARCHAR(15),
    ShipPostalCode VARCHAR(10),
    ShipCountry VARCHAR(15)
);

CREATE INDEX IDX_Orders_OrderDate ON Orders (OrderDate);

CREATE INDEX IDX_Orders_ShippedDate ON Orders (ShippedDate);

CREATE INDEX IDX_Orders_ShipPostalCode ON Orders (ShipPostalCode);

CREATE TABLE Products (
    ProductID INTEGER PRIMARY KEY,
    ProductName VARCHAR(40) NOT NULL,
    SupplierID INTEGER,
    CategoryID INTEGER,
    QuantityPerUnit VARCHAR(20),
    UnitPrice DECIMAL(10,4) DEFAULT 0,
    UnitsInStock SMALLINT DEFAULT 0,
    UnitsOnOrder SMALLINT DEFAULT 0,
    ReorderLevel SMALLINT DEFAULT 0,
    Discontinued BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX IDX_Products_ProductName ON Products (ProductName);

CREATE TABLE Region (
    RegionID INTEGER NOT NULL,
    RegionDescription VARCHAR(50) NOT NULL,
    CONSTRAINT PK_Region PRIMARY KEY (RegionID)
);

CREATE TABLE Shippers (
    ShipperID INTEGER PRIMARY KEY,
    CompanyName VARCHAR(40) NOT NULL,
    Phone VARCHAR(24)
);

CREATE TABLE Suppliers (
    SupplierID INTEGER PRIMARY KEY,
    CompanyName VARCHAR(40) NOT NULL,
    ContactName VARCHAR(30),
    ContactTitle VARCHAR(30),
    Address VARCHAR(60),
    City VARCHAR(15),
    Region VARCHAR(15),
    PostalCode VARCHAR(10),
    Country VARCHAR(15),
    Phone VARCHAR(24),
    Fax VARCHAR(24),
    HomePage TEXT
);

CREATE INDEX IDX_Suppliers_CompanyName ON Suppliers (CompanyName);

CREATE INDEX IDX_Suppliers_PostalCode ON Suppliers (PostalCode);

CREATE TABLE Territories (
    TerritoryID VARCHAR(20) NOT NULL,
    TerritoryDescription VARCHAR(50) NOT NULL,
    RegionID INTEGER NOT NULL,
    CONSTRAINT PK_Territories PRIMARY KEY (TerritoryID)
);

ALTER TABLE Orders ADD CONSTRAINT PK_Orders
    PRIMARY KEY (OrderID);

ALTER TABLE Orders
    ALTER COLUMN OrderId
        ADD GENERATED ALWAYS AS IDENTITY;

ALTER TABLE Products
    ALTER COLUMN ProductID
        ADD GENERATED ALWAYS AS IDENTITY;

ALTER TABLE Shippers
    ALTER COLUMN ShipperID
        ADD GENERATED ALWAYS AS IDENTITY;

ALTER TABLE Suppliers
    ALTER COLUMN SupplierID
        ADD GENERATED ALWAYS AS IDENTITY;

ALTER TABLE EmployeeTerritories ADD CONSTRAINT FK_EmployeeTerritories_Employees
    FOREIGN KEY (EmployeeID) REFERENCES Employees (EmployeeID);

ALTER TABLE EmployeeTerritories ADD CONSTRAINT FK_EmployeeTerritories_Territories
    FOREIGN KEY (TerritoryID) REFERENCES Territories (TerritoryID);

ALTER TABLE OrderDetails ADD CONSTRAINT FK_Order_Details_Orders
    FOREIGN KEY (OrderID) REFERENCES Orders (OrderID);

ALTER TABLE OrderDetails ADD CONSTRAINT FK_Order_Details_Products
    FOREIGN KEY (ProductID) REFERENCES Products (ProductID);

ALTER TABLE Orders ADD CONSTRAINT FK_Orders_Customers
    FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID);

ALTER TABLE Orders ADD CONSTRAINT FK_Orders_Employees
    FOREIGN KEY (EmployeeID) REFERENCES Employees (EmployeeID);

ALTER TABLE Orders ADD CONSTRAINT FK_Orders_Shippers
    FOREIGN KEY (ShipVia) REFERENCES Shippers (ShipperID);

ALTER TABLE Products ADD CONSTRAINT FK_Products_Categories
    FOREIGN KEY (CategoryID) REFERENCES Categories (CategoryID);

ALTER TABLE Products ADD CONSTRAINT FK_Products_Suppliers
    FOREIGN KEY (SupplierID) REFERENCES Suppliers (SupplierID);

ALTER TABLE Territories ADD CONSTRAINT FK_Territories_Region
    FOREIGN KEY (RegionID) REFERENCES Region (RegionID);
