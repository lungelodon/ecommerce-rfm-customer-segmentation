```sql
-- SQL Script for E-commerce RFM Customer Segmentation

-- 1. Select all data from the sales transactions table
SELECT * FROM sales_transactions;

-- 2. Calculate Recency for each customer (conceptual, requires current date)
-- In a real database, you'd use a function like DATEDIFF or similar.
SELECT
    CustomerID,
    MAX(InvoiceDate) AS LastPurchaseDate,
    -- DATEDIFF(CURRENT_DATE(), MAX(InvoiceDate)) AS Recency
    'Recency calculation conceptual' AS Recency
FROM
    sales_transactions
GROUP BY
    CustomerID;

-- 3. Calculate Frequency for each customer
SELECT
    CustomerID,
    COUNT(DISTINCT InvoiceNo) AS Frequency
FROM
    sales_transactions
GROUP BY
    CustomerID;

-- 4. Calculate Monetary value for each customer
SELECT
    CustomerID,
    SUM(Quantity * UnitPrice) AS Monetary
FROM
    sales_transactions
GROUP BY
    CustomerID;

-- 5. Combine RFM scores (conceptual join, actual RFM segmentation done in Python)
-- This query illustrates how you might conceptually join RFM components.
SELECT
    c.CustomerID,
    'RecencyScore' AS RecencyScore,
    f.Frequency,
    m.Monetary
FROM
    (SELECT CustomerID, MAX(InvoiceDate) AS LastPurchaseDate FROM sales_transactions GROUP BY CustomerID) c
JOIN
    (SELECT CustomerID, COUNT(DISTINCT InvoiceNo) AS Frequency FROM sales_transactions GROUP BY CustomerID) f ON c.CustomerID = f.CustomerID
JOIN
    (SELECT CustomerID, SUM(Quantity * UnitPrice) AS Monetary FROM sales_transactions GROUP BY CustomerID) m ON c.CustomerID = m.CustomerID;
```

