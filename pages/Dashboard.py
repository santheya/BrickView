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
def get_query(query, column_name):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df.iloc[0][column_name]
def show():

    st.title("📊 Dashboard")
    conn = get_connection()
    total_listings = get_query(
    "SELECT COUNT(*) AS total FROM listings","total")
    total_sales = get_query(
    "SELECT COUNT(*) AS total FROM sales","total")
    total_buyers = get_query(
    "SELECT COUNT(*) AS total FROM Buyer","total")
    total_agents = get_query(
    "SELECT COUNT(*) AS total FROM Agents","total")
    total_revenue = get_query(
    "SELECT SUM(Sale_Price) AS revenue FROM Sales","revenue")
    average_price = get_query(
    "SELECT AVG(Price) AS avg_price FROM Listings","avg_price")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🏠 Total Listings", f"{total_listings:,}")
    with col2:
        st.metric("💰 Total Sales", f"{total_sales:,}")
    with col3:
        st.metric("👥 Total Buyer", f"{total_buyers:,}")
    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric("👨 Total Agents", f"{total_agents:,}")
    with col5:
        st.metric("💵 Total Revenue", f"${total_revenue:,.2f}")
    with col6:
        st.metric("⭐ Avg Property Price", f"${average_price:,.2f}")
    city_price_query = """SELECT City, AVG(Price) AS Average_Price FROM Listings GROUP BY City ORDER BY Average_Price DESC"""
    city_price_df = pd.read_sql(city_price_query, conn)    
    fig_city = px.bar(city_price_df,x="Average_Price",y="City",orientation="h",title="Average Property Price by City")
    fig_city.update_layout(xaxis_title="Average Price",yaxis_title="City",title_x=0.25)
    property_query = """SELECT Property_Type,COUNT(*) AS Total_Properties FROM Listings GROUP BY Property_Type ORDER BY Total_Properties DESC"""
    property_df = pd.read_sql(property_query, conn)
    fig_property = px.pie(property_df,names="Property_Type",values="Total_Properties",hole=0.5,title="Property Type Distribution")
    fig_property.update_layout(title_x=0.2,legend_title="Property Type")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏙 Average Property Price by City")
        st.plotly_chart(fig_city,use_container_width=True)
    with col2 :
        st.subheader("🏘 Property Type Distribution")
        st.plotly_chart(fig_property, use_container_width=True)
    monthly_sale_query = """Select  MONTHNAME(Date_Sold) as Month, sum(Sale_price) as  total_sales_values from brickview.Sales group by Month order by Month"""
    monthly_sale_df = pd.read_sql(monthly_sale_query, conn)
    fig_monthly_sale = px.line(monthly_sale_df,x="Month",y="total_sales_values",orientation="h",title="Monthly sale")
    fig_monthly_sale.update_layout(xaxis_title="Month",yaxis_title="Number of Sales",title_x=0.25)
    top_5agents_query = """SELECT A.Agent_ID, A.Name, ROUND(SUM(S.Sale_Price), 2) AS Total_Sales_Revenue FROM brickview.Agents AS A JOIN brickview.Listings AS L ON A.Agent_ID = L.Agent_ID JOIN brickview.Sales AS S ON L.Listing_ID = S.Listing_ID GROUP BY A.Agent_ID, A.Name ORDER BY Total_Sales_Revenue DESC limit 5"""
    top_5agents = pd.read_sql(top_5agents_query, conn)
    fig_top5agents = px.bar(top_5agents,x="Total_Sales_Revenue",y="Name",orientation="h",title="🏆 Top 5 Agents by Revenue")
    fig_top5agents.update_layout(xaxis_title="Total Revenue",yaxis_title="Agent Name",title_x=0.25)
    col1,col2 = st.columns(2)
    with col1:
        st.subheader("📈Monthly Sales Trend")
        st.plotly_chart(fig_monthly_sale, use_container_width=True)
    with col2:
        st.subheader("🏆 Top 5 Agents")
        st.plotly_chart(fig_top5agents, use_container_width=True)