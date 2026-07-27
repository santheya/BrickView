import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
conn = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    password = "Passw0rd",
    database='brickview')
if "result_df" not in st.session_state:
    st.session_state.result_df = None
def show():
    queries = { "Property & Pricing Analysis" :
            {"1.What is the average listing price by city?":"""Select City, avg(Price) as average_listing_price from brickview.Listings group by City order by average_listing_price""",
        "2.	What is the average price per square foot by property type?":"""Select Property_Type, avg(Price/Sqft) as average_price_per_sqft from brickview.Listings group by Property_Type order by average_price_per_sqft""",
        "3.	How does furnishing status impact property prices?":"""Select furnishing_status, avg(Price) from brickview.Property as A join brickview.Listings as B where A. listing_id = B. listing_id group by furnishing_status""",
        "4.	Do properties closer to metro stations command higher prices":"""SELECT CASE WHEN P.metro_distance_km <= 2 THEN '0-2' WHEN P.metro_distance_km <= 5 THEN '2-5' WHEN P.metro_distance_km <= 10 THEN '5-10' ELSE 'Above 10 km' END AS Metro_Distance, ROUND(AVG(L.Price), 2) AS Average_Price FROM brickview.Listings L JOIN brickview.Property P ON L.Listing_ID = P.Listing_ID GROUP BY Metro_Distance ORDER BY Metro_Distance desc """,
        "5.	Are rented properties priced differently from non-rented ones?":"""SELECT is_rented, ROUND(AVG(Price),2) AS Avg_Price FROM brickview.Listings L JOIN brickview.Property P ON L.Listing_ID=P.Listing_ID GROUP BY is_rented""",
        "6.	How do bedrooms and bathrooms affect pricing?":"""SELECT bedrooms,bathrooms,ROUND(AVG(Price),2) AS Avg_Price FROM brickview.Listings L JOIN brickview.Property P ON L.Listing_ID=P.Listing_ID GROUP BY bedrooms,bathrooms ORDER BY bedrooms,bathrooms""",
        "7.	Do properties with parking and power backup sell at higher prices?":"""Select parking_available, power_backup, avg(price) as average_price from brickview.Listings as A join brickview.Property as B where A.listing_id = B.listing_id group by parking_available, power_backup""",
        "8.	How does year built influence listing price?":"""select year_built, avg(price) as average_price from brickview.Listings as A join brickview.Property as B where A.listing_id = B.listing_id group by year_built order by year_built  asc""",
        "9.	Which cities have the highest average property prices?":"""select City, avg(Price) as average_price from brickview.Listings group by city order by average_price desc""",
        "10.How are properties distributed across price buckets?":"""SELECT CASE WHEN Price < 500000 THEN 'Under 500K' WHEN Price >= 500000 AND Price < 1000000 THEN '500K - 1M' WHEN Price >= 1000000 AND Price < 2000000 THEN '1M - 2M' ELSE 'Above 2M' END AS Price_Bucket,COUNT(*) AS Total_Properties FROM brickview.Listings GROUP BY Price_Bucket order by Price_Bucket asc"""},
    "Sales & Market Performance":{"11.What is the average days on market by city?":"""Select L.City , avg(S.Days_on_Market) as average_days_on_Market From brickview.Listings as L join brickview.Sales as S on L.listing_id = S.listing_id group by L.city order by average_days_on_Market""",
        "12.Which property types sell the fastest?":"""Select L.property_type , avg(S.Days_on_Market) as avg_days_on_Market From brickview.Listings as L join brickview.Sales as S on L.listing_id = S.listing_id group by L.property_type order by avg_days_on_Market""",
        "13.What percentage of properties are sold above listing price?":"""SELECT L.city , ROUND((SUM(CASE WHEN S.Sale_Price > L.Price THEN 1 ELSE 0 END) * 100.0) / COUNT(*), 2 ) AS Percentage_Sold_Above_Listing FROM brickview.Listings as L join brickview.Sales as S ON L.Listing_ID = S.Listing_ID group by L.city""",
        "14.What is the sale-to-list price ratio by city?":"""Select L.city, avg(S.sale_price/L.price) as Sale_to_listprice_ratio from brickview.Listings as L  join brickview.Sales as S on L.listing_id = S.listing_id  group by L.city """,
        "15.Which listings took more than 90 days to sell?":"""Select listing_id , Days_on_Market from brickview.sales where Days_on_Market > 90 order by Days_on_Market""",
        "16.How does metro distance affect time on market?":"""Select P.metro_distance_km , avg(S.Days_on_Market) as average_days_on_market from brickview.Property as P join brickview.Sales as S on P.listing_id = S.listing_id group by P.metro_distance_km order by P.metro_distance_km""",
        "17.What is the monthly sales trend?":"""Select  MONTH(Date_Sold) as Month, sum(Sale_price) as  total_sales_values from brickview.Sales group by MONTH(Date_Sold) order by Month""",
        "18.Which properties are currently unsold?":"""SELECT L.Listing_ID, L.City, L.Property_Type, L.Price FROM brickview.Listings AS L LEFT JOIN brickview.Sales AS S ON L.Listing_ID = S.Listing_ID WHERE S.Listing_ID IS NULL"""},
    "Agent Performance":{"19.Which agents have closed the most sales?":"""Select A.Agent_id, A.Name ,COUNT(S.Listing_id) as Sales_closed from brickview.Agents as A join brickview.listings as L on L.Agent_id =A.Agent_id join brickview.Sales as S on S.listing_id = L.listing_id group by A.Agent_id, A.Name order by Sales_closed desc""",
        "20.Who are the top agents by total sales revenue?":"""SELECT A.Agent_ID, A.Name, ROUND(SUM(S.Sale_Price), 2) AS Total_Sales_Revenue FROM brickview.Agents AS A JOIN brickview.Listings AS L ON A.Agent_ID = L.Agent_ID JOIN brickview.Sales AS S ON L.Listing_ID = S.Listing_ID GROUP BY A.Agent_ID, A.Name ORDER BY Total_Sales_Revenue DESC""",
        "21.Which agents close deals fastest?":"""select agent_id,name,avg_closing_days from brickview.Agents order by avg_closing_days asc""",
        "22.Does experience correlate with deals closed?":"""SELECT Agent_ID, Name, Experience_Years, Deals_Closed FROM brickview.Agents ORDER BY Experience_Years ASC""",
        "23.Do agents with higher ratings close deals faster?":"""SELECT Agent_ID, Name, Experience_Years, Deals_Closed FROM brickview.Agents ORDER BY Experience_Years ASC""",
        "24.What is the average commission earned by each agent?":"""select A.agent_id, A.Name, avg(S.sale_price*A.commission_rate/100 ) as average_commission_earned from brickview.agents as A join brickview.listings as L ON A.agent_id = L.agent_id join brickview.Sales as S on  L.listing_id= S.listing_id group by A.agent_id ,A.Name  order by average_commission_earned desc""",
        "25.Which agents currently have the most active listings?":"""SELECT A.Agent_ID, A.Name, COUNT(L.Listing_ID) AS Active_Listings FROM brickview.Agents AS A JOIN brickview.Listings AS L ON A.Agent_ID = L.Agent_ID LEFT JOIN brickview.Sales AS S ON L.Listing_ID = S.Listing_ID WHERE S.Listing_ID IS NULL GROUP BY A.Agent_ID, A.Name ORDER BY Active_Listings DESC"""},
    "Buyer & Financing Behavior" : {"26.What percentage of buyers are investors vs end users?":"""SELECT Buyer_Type, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM brickview.buyer), 2) AS Percentage FROM brickview.buyer GROUP BY Buyer_Type ORDER BY Percentage DESC""",
        "27.Which cities have the highest loan uptake rate?":"""SELECT L.City, ROUND( SUM(CASE WHEN B.Loan_Taken = 'True' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2 ) AS Loan_Uptake_Rate FROM brickview.Listings AS L JOIN brickview.Sales AS S ON L.Listing_ID = S.Listing_ID JOIN brickview.buyer AS B ON S.listing_id = B.Sale_ID GROUP BY L.City ORDER BY Loan_Uptake_Rate DESC""",
        "28.What is the average loan amount by buyer type?":"""Select  buyer_type, avg(loan_amount) as Average_loan_amount from brickview.buyer group by buyer_type order by Average_loan_amount""",
        "29.Which payment mode is most commonly used?":"""Select Payment_mode,Count(*) as total_payment_count from brickview.buyer group by payment_mode order by total_payment_count desc""",
        "30.Do loan-backed purchases take longer to close?":"""Select B.loan_taken, avg(S.Days_on_Market) as avg_days_taken from brickview.buyer as B join brickview.Sales as S on B.Sale_id = S.listing_id group by B.loan_taken"""}}
    category = st.selectbox("Select Category",list(queries.keys()),key="category")
    question = st.selectbox("Select Question",list(queries[category].keys()),key="question")
    sql = queries[category][question]
    st.code(sql, language="sql")
    if st.button("▶ Execute Query"):
        st.session_state["result_df"] = pd.read_sql(sql, conn)
        if "result_df" in st.session_state:
            st.dataframe(st.session_state["result_df"], use_container_width=True)
            st.download_button("📥 Download CSV",st.session_state["result_df"].to_csv(index=False),"query_result.csv","text/csv")
            st.success(f"✅ {len(st.session_state['result_df'])} records found.")



                          