-- Retail sales analysis | MySQL 8
-- First import retail_sales_dataset.csv into a table called retail_sales,
-- then select that table's database in MySQL Workbench. See README.md.
-- This script is read-only; it does not create or drop a database.

-- Dataset size, distinct orders, and customers
SELECT COUNT(*) AS records,
       COUNT(DISTINCT Order_ID) AS orders,
       COUNT(DISTINCT Customer_ID) AS customers
FROM retail_sales;

-- Revenue, profit, profit margin, and average order value
SELECT ROUND(SUM(Sales_Revenue_INR), 2) AS revenue_inr,
       ROUND(SUM(Profit_INR), 2) AS profit_inr,
       ROUND(100 * SUM(Profit_INR) / NULLIF(SUM(Sales_Revenue_INR), 0), 2) AS profit_margin_pct,
       ROUND(SUM(Sales_Revenue_INR) / NULLIF(COUNT(DISTINCT Order_ID), 0), 2) AS average_order_value_inr
FROM retail_sales;

-- Sales by region
SELECT Region,
       COUNT(DISTINCT Order_ID) AS orders,
       ROUND(SUM(Sales_Revenue_INR), 2) AS revenue_inr,
       ROUND(SUM(Profit_INR), 2) AS profit_inr
FROM retail_sales
GROUP BY Region
ORDER BY revenue_inr DESC;

-- Top ten products by revenue
SELECT Product_Name, SUM(Quantity) AS units_sold,
       ROUND(SUM(Sales_Revenue_INR), 2) AS revenue_inr
FROM retail_sales
GROUP BY Product_Name
ORDER BY revenue_inr DESC
LIMIT 10;

-- Revenue, profit and weighted profit margin by product category
SELECT Product_Category,
       ROUND(SUM(Sales_Revenue_INR), 2) AS revenue_inr,
       ROUND(SUM(Profit_INR), 2) AS profit_inr,
       ROUND(100 * SUM(Profit_INR) / NULLIF(SUM(Sales_Revenue_INR), 0), 2) AS profit_margin_pct
FROM retail_sales
GROUP BY Product_Category
ORDER BY revenue_inr DESC;

-- Monthly revenue. Order_Date must be a DATE or an ISO yyyy-mm-dd string.
SELECT SUBSTR(Order_Date, 1, 7) AS sales_month,
       COUNT(DISTINCT Order_ID) AS orders,
       ROUND(SUM(Sales_Revenue_INR), 2) AS revenue_inr
FROM retail_sales
GROUP BY SUBSTR(Order_Date, 1, 7)
ORDER BY sales_month;

-- Repeat customers in the available period
SELECT Customer_ID, COUNT(DISTINCT Order_ID) AS orders,
       ROUND(SUM(Sales_Revenue_INR), 2) AS revenue_inr
FROM retail_sales
GROUP BY Customer_ID
HAVING COUNT(DISTINCT Order_ID) > 1
ORDER BY orders DESC, revenue_inr DESC;

-- Sales channel comparison
SELECT Sales_Channel, COUNT(DISTINCT Order_ID) AS orders,
       ROUND(SUM(Sales_Revenue_INR), 2) AS revenue_inr,
       ROUND(SUM(Profit_INR), 2) AS profit_inr
FROM retail_sales
GROUP BY Sales_Channel
ORDER BY revenue_inr DESC;
