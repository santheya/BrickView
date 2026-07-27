import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px
def get_connection():
    conn = mysql.connector.connect(
        host = "127.0.0.1",
        user = "root",
        password = "Passw0rd",
        database='brickview',
    )
    return conn

st.set_page_config(
    page_title="BrickView Real Estate Dashboard",
    page_icon="🏠",
    layout="wide"
)
def load_data(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df
def plot_bar(df, x, y, title):
    fig = px.bar(df, x=x, y=y, title=title)
    st.plotly_chart(fig, use_container_width=True)
def plot_box(df, x, y, title):
    fig = px.box(df, x=x, y=y, title=title)
    st.plotly_chart(fig, use_container_width=True)
def show():
    st.title("📈 Analytics")
    analysis_option = st.selectbox(
    "Select Analysis",
    (
        "Listing Analysis",
        "Sales Analysis",
        "Buyer Analysis",
        "Agent Analysis",
        "Property Analysis"
    ) 
    )
    if analysis_option == "Listing Analysis":
        st.subheader("🏠 Listing Analysis")
        st.markdown("Analyze listing prices, property types, furnishing status, metro accessibility, and price distribution.")
        col1,col2=st.columns(2)
        with col1:
            avg_listingprice_query="""SELECT City,AVG(Price) AS Average_Price FROM brickview.listings GROUP BY City ORDER BY Average_Price DESC """
            city_price_df = load_data(avg_listingprice_query)
            plot_bar(city_price_df,"City","Average_Price","Average Listing Price by City")
        with col2:
            avg_price_per_sqft_query = """SELECT Property_Type,AVG(Price / Sqft) AS Avg_Price_Per_Sqft FROM listings GROUP BY Property_Type ORDER BY Avg_Price_Per_Sqft DESC"""
            price_per_sqft_df = load_data(avg_price_per_sqft_query)
            plot_bar(price_per_sqft_df,"Property_Type","Avg_Price_Per_Sqft","Average price per sqft by Property type")
        col3,col4 =st.columns(2)
        with col3:
            furniture_query="""SELECT P.Furnishing_Status,L.Price FROM Property P JOIN listings L ON P.Listing_ID = L.Listing_ID"""
            furniture_df=load_data(furniture_query)
            plot_box(furniture_df,"Furnishing_Status","Price","Property price by furnishing status")
        with col4:
            metrodistance_query="""SELECT Metro_Distance_KM,Price FROM Property P JOIN Listings L ON P.Listing_ID = L.Listing_ID"""
            metrodistance_df=load_data(metrodistance_query)
            plot_bar(metrodistance_df,"Metro_Distance_KM","Price","Metro distance vs Property price")
        price_bucket_query="""SELECT CASE
        WHEN Price < 100000 THEN 'Below 100K'
        WHEN Price BETWEEN 100000 AND 300000 THEN '100K-300K'
        WHEN Price BETWEEN 300001 AND 500000 THEN '300K-500K'
        ELSE 'Above 500K' END AS Price_Bucket, COUNT(*) AS Total_Properties FROM listings GROUP BY Price_Bucket"""
        price_bucket_df=load_data(price_bucket_query)
        plot_box(price_bucket_df,"Price_Bucket","Total_Properties","Property Distribution by Price Bucket")
    elif analysis_option == "Sales Analysis":
        st.subheader("💰 Sales Analysis")
        col1,col2=st.columns(2)
        with col1:
            fast_Selling_property_query="""Select L.property_type , avg(S.Days_on_Market) as avg_days_on_Market From   brickview.Listings as L join brickview.Sales as S on L.listing_id = S.listing_id group by L.property_type order by avg_days_on_Market """
            fast_selling_df=load_data(fast_Selling_property_query)
            plot_bar(fast_selling_df,"property_type","avg_days_on_Market","fastest selling property type")
        with col2:
            sale_to_list_query="""Select L.city, avg(S.sale_price/L.price) as Sale_to_listprice_ratio from brickview.Listings as L  join brickview.Sales as S on L.listing_id = S.listing_id  group by L.city"""
            sale_ratio_df=load_data(sale_to_list_query)
            plot_box(sale_ratio_df,"city","Sale_to_listprice_ratio","sale-to-list price ratio by city")
        col3,col4=st.columns(2)
        with col3:
            salestrend_query = """Select  MONTHNAME(Date_Sold) as Month, sum(Sale_price) as  total_sales_values from brickview.Sales group by MONTHNAME(Date_Sold) order by Month"""
            salestrend_df=load_data(salestrend_query)
            plot_bar(salestrend_df,"Month","total_sales_values","Monthly Sales Trend")
        with col4:
            unsoldproperty_query="""SELECT L.Listing_ID, L.City, L.Property_Type, L.Price FROM brickview.Listings AS L LEFT JOIN brickview.Sales AS S ON L.Listing_ID = S.Listing_ID WHERE S.Listing_ID IS NULL"""
            unsold_df=load_data(unsoldproperty_query)
            plot_box(unsold_df,"City","Property_Type","Unsold Properties")
        average_daysonmarket="""Select L.City , avg(S.Days_on_Market) as average_days_on_Market From brickview.Listings as L join brickview.Sales as S on L.listing_id = S.listing_id group by L.city order by average_days_on_Market """
        days_onmarket_df=load_data(average_daysonmarket)
        plot_bar(days_onmarket_df,"City","average_days_on_Market","Property average days on Market")
    elif analysis_option == "Buyer Analysis":
        st.subheader("👥 Buyer Analysis")
        col1,col2=st.columns(2)
        with col1:
            investor_enduser_query="""SELECT Buyer_Type, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM brickview.buyer), 2) AS Percentage FROM brickview.buyer GROUP BY Buyer_Type ORDER BY Percentage DESC"""
            inv_enduser_df=load_data(investor_enduser_query)
            plot_bar(inv_enduser_df,"Buyer_Type","Percentage","Investor vs Endusers percentage")
        with col2:
            loanuptake_query="""SELECT L.City, ROUND( SUM(CASE WHEN B.Loan_Taken = 'True' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2 ) AS Loan_Uptake_Rate FROM brickview.Listings AS L JOIN brickview.Sales AS S ON L.Listing_ID = S.Listing_ID JOIN brickview.buyer AS B ON S.listing_id = B.Sale_ID GROUP BY L.City ORDER BY Loan_Uptake_Rate DESC"""
            loanuptake_df=load_data(loanuptake_query)
            plot_bar(loanuptake_df,"City","Loan_Uptake_Rate","loan uptake rate by city")
        col3,col4=st.columns(2)
        with col3:
            Avg_loanquery="""Select  buyer_type, avg(loan_amount) as Average_loan_amount from brickview.buyer group by buyer_type order by Average_loan_amount"""
            avg_loan_df=load_data(Avg_loanquery)
            plot_box(avg_loan_df,"buyer_type","Average_loan_amount","Average loan amount by Buyer type")
        with col4:
            payment_mode_query="""Select Payment_mode,Count(*) as total_payment_count from brickview.buyer group by payment_mode order by total_payment_count desc """
            payment_mode_df=load_data(payment_mode_query)
            plot_bar(payment_mode_df,"Payment_mode","total_payment_count","commonly used payment mode")
        loanbacked_query="""Select B.loan_taken, avg(S.Days_on_Market) as avg_days_taken from brickview.buyer as B join brickview.Sales as S on B.Sale_id = S.listing_id group by B.loan_taken"""
        loanbacked_df=load_data(loanbacked_query)
        plot_box(loanbacked_df,"loan_taken","avg_days_taken","Time for loan backed purchses to close")
    elif analysis_option == "Agent Analysis":
        st.subheader("🧑‍💼 Agent Analysis")
        col1,col2=st.columns(2)
        with col1:
            mostsales_query="""Select A.Agent_id, A.Name ,COUNT(S.Listing_id) as Sales_closed from brickview.Agents as A join brickview.listings as L on L.Agent_id =A.Agent_id join brickview.Sales as S on S.listing_id = L.listing_id group by A.Agent_id, A.Name order by Sales_closed desc"""
            mostsales_df=load_data(mostsales_query)
            plot_bar(mostsales_df,"Agent_id","Sales_closed","Agents with most sales")
        with col2:
            topagent_query="""SELECT A.Agent_ID, A.Name, ROUND(SUM(S.Sale_Price), 2) AS Total_Sales_Revenue FROM brickview.Agents AS A JOIN brickview.Listings AS L ON A.Agent_ID = L.Agent_ID JOIN brickview.Sales AS S ON L.Listing_ID = S.Listing_ID GROUP BY A.Agent_ID, A.Name ORDER BY Total_Sales_Revenue DESC"""
            topagent_df=load_data(topagent_query)
            plot_bar(topagent_df,"Agent_ID","Total_Sales_Revenue","Top Agents by Sale revenue")
        col3,col4=st.columns(2)
        with col3:
            fastclose_quer="""select agent_id,name,avg_closing_days from brickview.Agents order by avg_closing_days asc"""
            fastclose_df=load_data(fastclose_quer)
            plot_bar(fastclose_df,"agent_id","avg_closing_days","agents with fastest deals close")
        with col4:
            commission_query="""select A.agent_id, A.Name, avg(S.sale_price*A.commission_rate/100 ) as average_commission_earned from brickview.agents as A join brickview.listings as L ON A.agent_id = L.agent_id join brickview.Sales as S on  L.listing_id= S.listing_id group by A.agent_id ,A.Name  order by average_commission_earned desc"""
            commission_df=load_data(commission_query)
            plot_bar(commission_df,"agent_id","average_commission_earned","Average commission earned")
    elif analysis_option == "Property Analysis":
        st.subheader("🏡 Property Analysis")
        col1,col2=st.columns(2)
        with col1:
            rentedprice_query="""SELECT is_rented, ROUND(AVG(Price),2) AS Avg_Price FROM brickview.listings L JOIN brickview.Property P ON L.Listing_ID=P.Listing_ID GROUP BY is_rented"""
            rentedprice_df=load_data(rentedprice_query)
            plot_box(rentedprice_df,"is_rented","Avg_Price","Price of Rented vs Non-rented")
        with col2:
            year_query="""select year_built, avg(price) as average_price from brickview.Listings as A join brickview.Property as B where A.listing_id = B.listing_id group by year_built order by year_built  asc"""
            year_df=load_data(year_query)
            plot_box(year_df,"year_built","average_price","Year build influence prices")
        col3,col4=st.columns(2)
        bedroom_query="""SELECT   bedrooms, bathrooms,  ROUND(AVG(Price),2) AS Avg_Price FROM brickview.listings L JOIN brickview.Property P ON L.Listing_ID=P.Listing_ID  GROUP BY bedrooms,bathrooms ORDER BY bedrooms,bathrooms"""
        bedroom_df=load_data(bedroom_query)
        with col3:
            plot_box(bedroom_df,"bedrooms","Avg_Price","Prices based on bedrooms")
        with col4:
            plot_bar(bedroom_df,"bathrooms","Avg_Price","Prices based on bathrooms")
        parking_query="""Select parking_available, power_backup, avg(price) as average_price from brickview.listings as A join brickview.Property as B where A.listing_id = B.listing_id group by parking_available, power_backup"""
        parking_df=load_data(parking_query)
        col5,col6=st.columns(2)
        with col5:
            plot_bar(parking_df,"parking_available","average_price","parkings affects property price")
        with col6:
            plot_bar(parking_df,"power_backup","average_price","Power backup affects property price")

