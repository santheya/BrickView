import streamlit as st
import pandas as pd
import mysql.connector
from pages import home,Dashboard,Analytics,crud,Sql_query,filter
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
st.markdown("""
<style>

/* Hide Streamlit default page navigation */

[data-testid="stSidebarNav"] {
    display: none;
}

</style>
""", unsafe_allow_html=True)
st.sidebar.title("🏠 BrickView")

page = st.sidebar.radio(
    "Navigation",
    (
        "🏠 Home",
        "📊 Dashboard",
        "📈 Analytics",
        "🛠 CRUD",
        "📝 SQL Queries",
        "🎛️ Filters Page"
    )
)

if page == "🏠 Home":
    home.show()
elif page == "📊 Dashboard":
    Dashboard.show()

elif page == "📈 Analytics":
    Analytics.show()

elif page == "🛠 CRUD":
    crud.show()

elif page == "📝 SQL Queries":
    Sql_query.show()
elif page == "🎛️ Filters Page":
    filter.show()



