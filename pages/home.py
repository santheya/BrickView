import streamlit as st

def show():
    st.title("🏠 BrickView Real Estate Analytics Dashboard")

    st.markdown("---")

    st.header("📌 Project Overview")

    st.write("""
    BrickView is a Real Estate Analytics Dashboard developed using
    Python, MySQL, Streamlit and Plotly.

    The project analyzes real estate listings, property details,
    buyers, agents and sales to generate meaningful business insights.
    """)

    st.markdown("---")
    st.header("🎯 Problem Statement")
    st.write("""
             Real estate companies generate huge amounts of property data.
             The objective of this project is to transform raw JSON data into meaningful business insights using SQL and interactive dashboards.""")
    st.header("🛠 Technologies Used")

    col1, col2 = st.columns(2)

    with col1:
        st.write("• Python")
        st.write("• Pandas")
        st.write("• Streamlit")

    with col2:
        st.write("• MySQL")
        st.write("• Plotly")
        st.write("• JSON")
    st.header("📂 Dataset")

    st.write("""
             The project consists of five datasets:
             • Listings
             • Property
             • Sales
             • Buyers
             • Agents""")
    st.header("🔄 Workflow")

    st.code("""
            JSON Files
                  ↓
            Data Cleaning (Pandas)
                  ↓
            CSV Files
                  ↓
            MySQL Database
                  ↓
            SQL Analysis
                  ↓
            Streamlit Dashboard""")
    st.header("📖 Dashboard Navigation")

    st.info("""
            🏠 Home

            📊 Dashboard

            📈 Analytics

            🛠 CRUD

            📝 SQL Queries

            ℹ About""")