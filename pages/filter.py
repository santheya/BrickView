import streamlit as st
import pandas as pd
import mysql.connector

st.set_page_config(page_title="Filters", layout="wide")
def get_connection():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Passw0rd",
        database="brickview")
    return conn

def show ():
    st.subheader("🏙️ Filter by City")
    conn = get_connection()
    listings = pd.read_sql("SELECT * FROM listings", conn)
    cities = sorted(listings["City"].dropna().unique())
    selected_city = st.multiselect("Select City",cities)
    if selected_city:
        city_df = listings[listings["City"].isin(selected_city)]
        st.dataframe(city_df, use_container_width=True)
    st.divider()
# ---------------- PROPERTY TYPE ---------------- #
    st.subheader("🏠 Filter by Property Type")
    property_types = sorted(listings["Property_Type"].dropna().unique())
    selected_property = st.selectbox("Select Property Type",["Select Propery type"] + property_types)
    if selected_property != "Select Propery type":
        property_df = listings[listings["Property_Type"] == selected_property]
        st.dataframe(property_df, use_container_width=True)
    st.divider()
# ---------------- PRICE FILTER ---------------- #
    st.subheader("💰 Filter by Price")
    min_price = int(listings["Price"].min())
    max_price = int(listings["Price"].max())
    price = st.slider("Price Range",min_price,max_price,(min_price, max_price))
    price_df = listings[(listings["Price"] >= price[0]) & (listings["Price"] <= price[1])]
    st.dataframe(price_df, use_container_width=True)
    st.divider()
# ---------------- AGENT FILTER ---------------- #
    st.subheader("👤 Filter by Agent")
    agents = pd.read_sql("SELECT * FROM agents", conn)
    agent_names = sorted(agents["Name"].dropna().unique())
    selected_agent = st.selectbox("Select Agent",["Select the agent"] + agent_names)
    if selected_agent != "Select the agent":
        agent_df = agents[agents["Name"] == selected_agent]
        st.dataframe(agent_df, use_container_width=True)
    st.divider()
# ---------------- SALE DATE FILTER ---------------- #
    st.subheader("📅 Filter by Sale Date")
    sales = pd.read_sql("SELECT * FROM sales", conn)
    sales["Date_Sold"] = pd.to_datetime(sales["Date_Sold"])
    date_range = st.date_input("Select Date Range",
    (
        sales["Date_Sold"].min(),
        sales["Date_Sold"].max()
    ))

    if len(date_range) == 2:
        sale_df = sales[
        (sales["Date_Sold"] >= pd.to_datetime(date_range[0])) &
        (sales["Date_Sold"] <= pd.to_datetime(date_range[1]))]
    st.dataframe(sale_df, use_container_width=True)
    conn.close()