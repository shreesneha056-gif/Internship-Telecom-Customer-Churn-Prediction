CREATE DATABASE project2;

---Overview


SELECT * FROM CUSTOMER_DEMOGRAPHICS;
SELECT * FROM CUSTOMER_LOCATION;
SELECT * FROM CUSTOMER_SERVICES;
SELECT * FROM CUSTOMER_ACCOUNT_STATUS;
SELECT * FROM ZIPCODE_POPULATION;


---Count Rows

SELECT COUNT(*) AS total_count_demographics 
FROM CUSTOMER_DEMOGRAPHICS;

SELECT COUNT(*) AS total_count_location 
FROM CUSTOMER_LOCATION;

SELECT COUNT(*) AS total_count_services 
FROM CUSTOMER_SERVICES;

SELECT COUNT(*) AS total_count_account_status 
FROM CUSTOMER_ACCOUNT_STATUS;

SELECT COUNT(*) AS total_count_population 
FROM ZIPCODE_POPULATION;


---Primary Key Duplicate Check

SELECT CUSTOMER_ID, COUNT(*) AS Count_primary
FROM CUSTOMER_DEMOGRAPHICS
GROUP BY CUSTOMER_ID
HAVING COUNT(*) > 1;

SELECT CUSTOMER_ID, COUNT(*) AS Count_primary
FROM CUSTOMER_LOCATION
GROUP BY CUSTOMER_ID
HAVING COUNT(*) > 1;

SELECT CUSTOMER_ID, COUNT(*) AS Count_primary
FROM CUSTOMER_SERVICES
GROUP BY CUSTOMER_ID
HAVING COUNT(*) > 1;

SELECT CUSTOMER_ID, COUNT(*) AS Count_primary
FROM CUSTOMER_ACCOUNT_STATUS
GROUP BY CUSTOMER_ID
HAVING COUNT(*) > 1;

SELECT ZIP_CODE, COUNT(*) AS Count_primary
FROM ZIPCODE_POPULATION
GROUP BY ZIP_CODE
HAVING COUNT(*) > 1;


---Negative / Zero Value Check

SELECT * 
FROM CUSTOMER_DEMOGRAPHICS
WHERE AGE <= 0 OR NUMBER_OF_DEPENDENTS < 0;

SELECT * 
FROM CUSTOMER_ACCOUNT_STATUS
WHERE NUMBER_OF_REFERRALS < 0
   OR TENURE_IN_MONTHS <= 0
   OR MONTHLY_CHARGE <= 0----YES
   OR TOTAL_CHARGES < 0
   OR TOTAL_REFUNDS < 0
   OR TOTAL_EXTRA_DATA_CHARGES < 0
   OR TOTAL_LONG_DISTANCE_CHARGES < 0
   OR TOTAL_REVENUE < 0;

SELECT * 
FROM CUSTOMER_SERVICES
WHERE AVG_MONTHLY_LONG_DISTANCE_CHARGES < 0
   OR AVG_MONTHLY_GB_DOWNLOAD < 0;

SELECT * 
FROM ZIPCODE_POPULATION
WHERE POPULATION <= 0;


---NULL Value Check

DESCRIBE TABLE CUSTOMER_DEMOGRAPHICS;


SELECT
    SUM(IFF(CUSTOMER_ID IS NULL,1,0)) AS null_customer_id,
    SUM(IFF(Gender IS NULL,1,0)) AS null_gender,
    SUM(IFF(Age IS NULL,1,0)) AS null_age,
    SUM(IFF(Married IS NULL,1,0)) AS null_married,
    SUM(IFF(Number_of_Dependents IS NULL,1,0)) AS null_dependents
FROM customer_demographics;

DESCRIBE TABLE CUSTOMER_LOCATION;

SELECT
    SUM(IFF(Customer_ID IS NULL,1,0)) AS null_customer_id,
    SUM(IFF(City IS NULL,1,0)) AS null_city,
    SUM(IFF(Zip_Code IS NULL,1,0)) AS null_zip,
    SUM(IFF(Latitude IS NULL,1,0)) AS null_lat,
    SUM(IFF(Longitude IS NULL,1,0)) AS null_lon
FROM customer_location;

DESCRIBE TABLE customer_services;

SELECT
    SUM(IFF(Customer_ID IS NULL,1,0)) AS null_customer_id,
    SUM(IFF(Offer IS NULL,1,0)) AS null_offer,---YES
    SUM(IFF(Phone_Service IS NULL,1,0)) AS null_phone_service,
    SUM(IFF(Internet_Service IS NULL,1,0)) AS null_internet_service,
    SUM(IFF(Internet_Type IS NULL,1,0)) AS null_internet_type,---YES
    SUM(IFF(Avg_Monthly_GB_Download IS NULL,1,0)) AS null_avg_gb---YES
FROM customer_services;

DESCRIBE TABLE customer_account_status;

SELECT
    SUM(IFF(Customer_ID IS NULL,1,0)) AS null_customer_id,
    SUM(IFF(Contract IS NULL,1,0)) AS null_contract,
    SUM(IFF(Payment_Method IS NULL,1,0)) AS null_payment_method,
    SUM(IFF(Customer_Status IS NULL,1,0)) AS null_customer_status,
    SUM(IFF(Churn_Category IS NULL,1,0)) AS null_churn_category,---YES
    SUM(IFF(Churn_Reason IS NULL,1,0)) AS null_churn_reason---YES
FROM customer_account_status;

DESCRIBE TABLE zipcode_population;

SELECT
    SUM(IFF(Zip_Code IS NULL,1,0)) AS null_zip,
    SUM(IFF(Population IS NULL,1,0)) AS null_population
FROM zipcode_population;


---Primary Key Uniqueness Check 

SELECT COUNT(*) AS Total_Rows, COUNT(DISTINCT Customer_ID) AS Unique_Rows
FROM customer_demographics;

SELECT COUNT(*) AS Total_Rows, COUNT(DISTINCT Customer_ID) AS Unique_Rows
FROM customer_location;

SELECT COUNT(*) AS Total_Rows, COUNT(DISTINCT Customer_ID) AS Unique_Rows
FROM customer_services;

SELECT COUNT(*) AS Total_Rows, COUNT(DISTINCT Customer_ID) AS Unique_Rows
FROM customer_account_status;

SELECT COUNT(*) AS Total_Rows, COUNT(DISTINCT ZIP_CODE) AS Unique_Rows
FROM zipcode_population;


---Join Check and Orphan FK Check (chain pattern you built)

---customer_location -> customer_demographics
SELECT a.*
FROM customer_location AS a
LEFT JOIN customer_demographics AS b
ON a.Customer_ID = b.Customer_ID
WHERE b.Customer_ID IS NULL;

---customer_demographics -> customer_services
SELECT a.*
FROM customer_demographics AS a
LEFT JOIN customer_services AS b
ON a.Customer_ID = b.Customer_ID
WHERE b.Customer_ID IS NULL;

---customer_services -> customer_account_status
SELECT a.*
FROM customer_services AS a
LEFT JOIN customer_account_status AS b
ON a.Customer_ID = b.Customer_ID
WHERE b.Customer_ID IS NULL;

---customer_location -> zipcode_population
SELECT a.*
FROM customer_location AS a
LEFT JOIN zipcode_population AS b
ON a.zip_code = b.zip_code
WHERE b.zip_code IS NULL;

---Treating negative value

SELECT MONTHLY_CHARGE, COUNT(*) AS num_customers
FROM CUSTOMER_ACCOUNT_STATUS
WHERE MONTHLY_CHARGE < 0
GROUP BY MONTHLY_CHARGE
ORDER BY MONTHLY_CHARGE;


ALTER TABLE customer_account_status 
ADD Monthly_Discount_Amount FLOAT;

ALTER TABLE customer_account_status 
ADD Has_Discount INT;

UPDATE customer_account_status
SET Monthly_Discount_Amount = ABS(Monthly_Charge), Has_Discount = 1
WHERE Monthly_Charge < 0;

UPDATE customer_account_status
SET Monthly_Discount_Amount = 0, Has_Discount = 0
WHERE Monthly_Charge >= 0;

--- verifying updated table
SELECT Has_Discount, COUNT(*) AS customer_count, AVG(Monthly_Discount_Amount) AS avg_discount
FROM customer_account_status
GROUP BY Has_Discount;

SELECT COUNT(Monthly_charge) AS total_negative_count
FROM customer_account_status
WHERE monthly_charge<0;


---null check

-- Confirms Internet Type nulls only happen when there's no internet service
SELECT Internet_Service, COUNT(*) AS num_customers
FROM customer_services
WHERE Internet_Type IS NULL
GROUP BY Internet_Service;

-- Confirms Churn Category/Reason nulls only happen for non-churned customers
SELECT * FROM customer_account_status;

SELECT Customer_Status, COUNT(*) AS num_customers
FROM customer_account_status
WHERE Churn_Category IS NULL
GROUP BY Customer_Status;

SELECT * FROM customer_services;

---Table : customer_services
---Offer: null = customer wasn't on any promotional offer
SELECT * FROM customer_services;

ALTER TABLE customer_services 
ADD Offer_Clean VARCHAR(50);

UPDATE customer_services
SET Offer_Clean = IFF(Offer IS NULL, 'No Offer', Offer);

--- Internet Type: null = no internet service at all
ALTER TABLE customer_services 
ADD Internet_Type_Clean VARCHAR(50);

UPDATE customer_services
SET Internet_Type_Clean = IFF(Internet_Type IS NULL, 'No Internet Service', Internet_Type);

---Table : customer_account_status
-- Churn Category / Reason: null = customer never churned (Joined or Stayed)

SELECT * FROM customer_account_status;


ALTER TABLE customer_account_status 
ADD Churn_Category_Clean VARCHAR(50);

ALTER TABLE customer_account_status 
ADD Churn_Reason_Clean VARCHAR(100);

UPDATE customer_account_status
SET Churn_Category_Clean = IFF(Churn_Category IS NULL, 'Not Churned', Churn_Category),
    Churn_Reason_Clean   = IFF(Churn_Reason IS NULL, 'Not Churned', Churn_Reason);

-- Verify no more nulls remain in the Clean columns
SELECT
    SUM(IFF(Offer_Clean IS NULL,1,0)) AS null_offer_clean,
    SUM(IFF(Internet_Type_Clean IS NULL,1,0)) AS null_internet_clean
FROM customer_services;

SELECT
    SUM(IFF(Churn_Category_Clean IS NULL,1,0)) AS null_churn_cat_clean,
    SUM(IFF(Churn_Reason_Clean IS NULL,1,0)) AS null_churn_reason_clean
FROM customer_account_status;


--=============================================================================
---EDA
--- PROBLEM STATEMENT 1: Churn Driver & Retention Segmentation

--- Overall churn rate
SELECT * FROM customer_account_status;

SELECT Customer_Status, COUNT(*) AS num_customers, COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () AS pct_of_total
FROM customer_account_status
GROUP BY Customer_Status;

--- Churn rate by Contract type
SELECT * FROM customer_account_status;

SELECT Contract, COUNT(*) AS total_customers, SUM(IFF(Customer_Status = 'Churned', 1, 0)) AS churned,
    SUM(IFF(Customer_Status = 'Churned', 1, 0)) * 100.0 / COUNT(*) AS churn_rate_pct
FROM customer_account_status 
GROUP BY Contract
ORDER BY churn_rate_pct DESC;

--- Churn rate by Internet Type (services join)
SELECT * FROM customer_account_status;
SELECT * FROM customer_services;

SELECT b.Internet_Type_Clean, COUNT(*) AS total_customers, SUM(IFF(a.Customer_Status = 'Churned', 1, 0)) AS churned,
    SUM(IFF(a.Customer_Status = 'Churned', 1, 0)) * 100.0 / COUNT(*) AS churn_rate_pct
FROM customer_account_status AS a
JOIN customer_services AS b 
ON a.Customer_ID = b.Customer_ID
GROUP BY b.Internet_Type_Clean
ORDER BY churn_rate_pct DESC;

--- Churn rate by tenure band
SELECT * FROM customer_account_status;

SELECT IFF(tenure_in_months < 12, '0-12 months', 
        IFF(tenure_in_months < 24, '12-24 months', 
        IFF(tenure_in_months < 48, '24-48 months','48+ months'))) AS tenure_band,
    COUNT(*) AS total_customers, SUM(IFF(Customer_Status = 'Churned', 1, 0)) AS churned,
    SUM(IFF(Customer_Status = 'Churned', 1, 0)) * 100.0 / COUNT(*) AS churn_rate_pct
FROM customer_account_status
GROUP BY tenure_band
ORDER BY tenure_band ASC;

--- Avg Tenure
SELECT AVG(Tenure_in_Months) AS avg_tenure 
FROM customer_account_status;

--- Top churn reasons
SELECT * FROM customer_account_status;

SELECT Churn_Reason_Clean, COUNT(*) AS num_customers
FROM customer_account_status
WHERE Churn_Category_Clean != 'Not Churned'
GROUP BY Churn_Reason_Clean
ORDER BY num_customers DESC;

--=============================================================================
--- PROBLEM STATEMENT 2: Customer Lifetime Value & Referral Impact

--- Average Revenue, referral and tenure in months summary
SELECT * FROM customer_account_status;

SELECT AVG(Total_Revenue) AS avg_revenue, AVG(Number_of_Referrals) AS avg_referrals, AVG(Tenure_in_Months) AS avg_tenure
FROM customer_account_status;

--- Churn rate of average revenue by referral count band
SELECT IFF(number_of_referrals= 0, '0 referrals', IFF(number_of_referrals BETWEEN 1 AND 3 , '1-3 referrals','4+ referrals')) AS referral_band,
    COUNT(*) AS num_customers, SUM(IFF(Customer_Status = 'Churned', 1, 0)) AS churned,
    AVG(Total_Revenue) AS avg_revenue, 
    SUM(IFF(Customer_Status = 'Churned', 1, 0)) * 100.0 / COUNT(*) AS churn_rate_pct
FROM customer_account_status
GROUP BY referral_band
ORDER BY referral_band ASC;

--- Revenue by service bundle size (count of active services)
SELECT * FROM customer_account_status;
SELECT * FROM customer_services;

SELECT (IFF(b.Phone_Service='True',1,0) + IFF(b.multiple_lines='True',1,0)
     + IFF(b.internet_service='True',1,0) + IFF(b.online_security='True',1,0)
     + IFF(b.online_backup='True',1,0) + IFF(b.device_protection_plan='True',1,0)
     + IFF(b.premium_tech_support='True',1,0) + IFF(b.streaming_tv='True',1,0)
     + IFF(b.streaming_movies='True',1,0) + IFF(b.streaming_music='True',1,0)
     + IFF(b.unlimited_data='True',1,0)) AS num_services, COUNT(*) AS num_customers, AVG(a.total_revenue) AS avg_revenue, 
     SUM(IFF(a.Customer_Status = 'Churned', 1, 0)) * 100.0 / COUNT(*) AS churn_rate_pct
FROM customer_account_status AS a
JOIN customer_services AS b 
ON a.Customer_ID = b.Customer_ID
GROUP BY num_services
ORDER BY num_services;


--=============================================================================
--- PROBLEM STATEMENT 3: Geographic & Offer-Based Churn Patterns

--- Churn rate by Offer
SELECT * FROM customer_account_status;
SELECT * FROM customer_services;


SELECT b.Offer_Clean, COUNT(*) AS total_customers, SUM(IFF(a.Customer_Status = 'Churned', 1, 0)) * 100.0 / COUNT(*) AS churn_rate_pct
FROM customer_account_status AS a
JOIN customer_services AS b 
ON a.Customer_ID = b.Customer_ID
GROUP BY b.Offer_Clean
ORDER BY churn_rate_pct DESC;

--- Churn rate by City (top 15 by customer count)
SELECT * FROM customer_account_status;
SELECT * FROM customer_location;


SELECT TOP 15 b.City, COUNT(*) AS total_customers, SUM(IFF(a.Customer_Status = 'Churned', 1, 0)) * 100.0 / COUNT(*) AS churn_rate_pct
FROM customer_account_status AS a
JOIN customer_location AS b 
ON a.Customer_ID = b.Customer_ID
GROUP BY b.City
ORDER BY total_customers DESC;

--- Churn rate by zip code population density
SELECT * FROM customer_account_status;
SELECT * FROM customer_location;
SELECT * FROM zipcode_population;

SELECT IFF(c.Population <10000, 'Low density (<10K)', IFF(c.Population <50000, 'Medium density (10K-50K)', 'High density (50K+)')) AS               density_band, COUNT(*) AS total_customers, SUM(IFF(a.Customer_Status = 'Churned', 1, 0)) * 100.0 / COUNT(*) AS churn_rate_pct
FROM customer_account_status AS a
JOIN customer_location AS b 
ON a.Customer_ID = b.Customer_ID
JOIN zipcode_population AS c 
ON b.Zip_Code = c.Zip_Code
GROUP BY density_band;


---=============================================================
---Dashboard-1
-- Total Customers
SELECT COUNT(*) AS total_customers 
FROM customer_demographics;

--- Overall Churn Rate
SELECT SUM(IFF(Customer_Status='Churned',1,0)) * 100.0 / COUNT(*) AS churn_rate_pct
FROM customer_account_status;

--- Avg Tenure
SELECT AVG(Tenure_in_Months) AS avg_tenure 
FROM customer_account_status;

--- Churn Rate by Contract (chart data -- your strongest finding)
SELECT Contract, COUNT(*) AS total_customers, SUM(IFF(Customer_Status='Churned',1,0)) * 100.0 / COUNT(*) AS churn_rate_pct
FROM customer_account_status 
GROUP BY Contract;


---==========================================================================
---Dashboard-2
-- Total Revenue
SELECT SUM(Total_Revenue) AS total_revenue 
FROM customer_account_status;

--- Avg Revenue per Customer
SELECT AVG(Total_Revenue) AS avg_revenue 
FROM customer_account_status;

--- Churn by Referral Band (your standout insight)
SELECT IFF(number_of_referrals= 0, '0 referrals', IFF(number_of_referrals BETWEEN 1 AND 3 , '1-3 referrals','4+ referrals')) AS referral_band,
    COUNT(*) AS num_customers, SUM(IFF(Customer_Status = 'Churned', 1, 0)) AS churned,
    AVG(Total_Revenue) AS avg_revenue, 
    SUM(IFF(Customer_Status = 'Churned', 1, 0)) * 100.0 / COUNT(*) AS churn_rate_pct
FROM customer_account_status
GROUP BY referral_band
ORDER BY referral_band ASC;


---Connection to powerbi 
SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION();