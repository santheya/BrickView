import streamlit as st
import pandas as pd
import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Passw0rd",
        database="brickview")
    return conn

def show():
    st.title("📝 CRUD Operations")
    if st.session_state.get("update_success", False):
        st.success("✅ Updated Successfully")
        st.session_state["update_success"] = False
    conn = get_connection()
    if conn is None:
        st.error("Database connection failed")
        return
    cursor = conn.cursor()
    tables = ["listings", "property", "sales", "buyer", "agents"]
    table_name = st.selectbox("Select Table", tables)
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    result = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(result, columns=column_names)
    if table_name == "listings":
        edited_df = st.data_editor(df,disabled=["listing_id"],use_container_width=True,key="editor")
    elif table_name == "property":
        edited_df = st.data_editor(df,disabled=["attribute_id", "listing_id"],use_container_width=True,key="editor")
    elif table_name == "buyer":
        edited_df = st.data_editor(df,disabled=["buyer_id"],use_container_width=True,key="editor")
    elif table_name == "agents":
        edited_df = st.data_editor(df,disabled=["Agent_ID"],use_container_width=True,key="editor")
    elif table_name == "sales":
        edited_df = st.data_editor(df,disabled=["listing_ID"],use_container_width=True,key="editor")
    col1, col2, col3 = st.columns(3)
    if "show_add_form" not in st.session_state:
        st.session_state.show_add_form = False
    if "show_delete" not in st.session_state:
        st.session_state.show_delete = False
    with col1:
        if st.button("➕ Add Record", use_container_width=True):
            st.session_state.show_add_form = True
    with col2:
        save_btn = st.button("💾 Save Changes", use_container_width=True)
    with col3:
        if st.button("❌ Delete Selected", use_container_width=True):
            st.session_state.show_delete = True
    primary_keys = {"listings": "listing_id","property": "attribute_id","buyer": "buyer_id","sales": "Listing_ID","agents": "Agent_ID"}
    if save_btn:
        pk = primary_keys[table_name]
        if edited_df.equals(df):
            st.info("No changes detected.")
            return
        for index, row in edited_df.iterrows():
            original_row = df.iloc[index]
            updates = []
            values = []
            for col in edited_df.columns:
                if col == pk:
                    continue
                if str(row[col]) != str(original_row[col]):
                    updates.append(f"{col}=%s")
                    values.append(row[col])
            if len(updates) == 0:
                continue
            values.append(row[pk])
            sql = f"""UPDATE {table_name} SET {', '.join(updates)} WHERE {pk}=%s"""
            cursor.execute(sql, tuple(values))
        conn.commit()
        st.session_state["update_success"] = True
        st.rerun()
    if st.session_state.show_add_form:
        if table_name == "listings":
            with st.form("add_listing"):
                city = st.text_input("City")
                property_type = st.text_input("Property Type")
                price = st.number_input("Price", min_value=0.0)
                sqft = st.number_input("Sqft", min_value=0.0)
                date_listed = st.date_input("Date Listed")
                agent_id = st.text_input("Agent ID")
                latitude = st.number_input("Latitude", format="%.6f")
                longitude = st.number_input("Longitude", format="%.6f")
                insert_btn = st.form_submit_button("Insert Record")
            if insert_btn:
                cursor.execute("""SELECT MAX(CAST(SUBSTRING(listing_id,2) AS UNSIGNED))FROM listings""")
                last = cursor.fetchone()[0]
                new_id = f"L{last+1:05d}"
                sql = """INSERT INTO listings (listing_id,City,Property_Type,Price,Sqft,Date_Listed,Agent_ID,Latitude,Longitude) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                values = (new_id,city,property_type,price,sqft,date_listed,agent_id,latitude,longitude)
                cursor.execute(sql, values)
                conn.commit()
                st.success("✅ Record Inserted Successfully")
                st.session_state.show_add_form = False
        if table_name == "property":
            with st.form("add_property"):
                listing_id = st.text_input("Listing ID")
                bedrooms = st.number_input("Bedrooms", min_value=0)
                bathrooms = st.number_input("Bathrooms", min_value=0)
                floor_number = st.number_input("Floor Number", min_value=0)
                total_floors = st.number_input("Total Floors", min_value=0)
                year_built = st.number_input("Year Built", min_value=1900)
                is_rented = st.selectbox("Is Rented", ["Yes", "No"])
                tenant_count = st.number_input("Tenant Count", min_value=0)
                furnishing_status = st.selectbox("Furnishing Status",["Furnished", "Semi-Furnished", "Unfurnished"])
                metro_distance_km = st.number_input("Metro Distance (km)")
                parking_available = st.selectbox("Parking Available", ["Yes", "No"])
                power_backup = st.selectbox("Power Backup", ["Yes", "No"])
                insert_btn = st.form_submit_button("Insert Record")
            if insert_btn:
                cursor.execute("""SELECT MAX(attribute_id) FROM property""")
                last = cursor.fetchone()[0]
                new_id = last+1
                sql = """INSERT INTO property(attribute_id,listing_id,bedrooms,bathrooms,floor_number,total_floors,year_built,is_rented,tenant_count,furnishing_status,metro_distance_km,parking_available,power_backup) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                values = (new_id,listing_id,bedrooms,bathrooms,floor_number,total_floors,year_built,is_rented,tenant_count,furnishing_status,metro_distance_km,parking_available,power_backup)
                cursor.execute(sql, values)
                conn.commit()
                st.success("Record Inserted Successfully in Property Table")
        if table_name == "buyer":
            with st.form("add_buyer"):
                sale_id = st.text_input("Sale ID")
                buyer_type = st.text_input("Buyer Type")
                payment_mode = st.text_input("Payment Mode")
                loan_taken = st.selectbox("Loan Taken", ["Yes", "No"])
                loan_provider = st.text_input("Loan Provider")
                loan_amount = st.number_input("Loan Amount")
                insert_btn = st.form_submit_button("Insert Record")
            if insert_btn:
                cursor.execute("""SELECT MAX(buyer_id) FROM buyer""")
                last = cursor.fetchone()[0]
                new_id = last +1
                sql = """INSERT INTO buyer VALUES (%s,%s,%s,%s,%s,%s,%s)"""
                values = (new_id,sale_id,buyer_type,payment_mode,loan_taken,loan_provider,loan_amount)
                cursor.execute(sql, values)
                conn.commit()
                st.success("Buyer Added Successfully")
        if table_name == "agents":
            with st.form("add_agent"):
                name = st.text_input("Name")
                phone = st.text_input("Phone")
                email = st.text_input("Email")
                commission_rate = st.number_input("Commission Rate")
                deals_closed = st.number_input("Deals Closed")
                rating = st.number_input("Rating")
                experience_years = st.number_input("Experience")
                avg_closing_days = st.number_input("Average Closing Days")
                insert_btn = st.form_submit_button("Insert Record")
            if insert_btn:
                cursor.execute("""SELECT MAX(CAST(SUBSTRING(Agent_ID,2) AS UNSIGNED))FROM agents""")
                last = cursor.fetchone()[0]
                new_id = f"A{last+1:05d}"
                sql = """INSERT INTO agents VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                values = (new_id,name,phone,email,commission_rate,deals_closed,rating,experience_years,avg_closing_days)
                cursor.execute(sql, values)
                conn.commit()
                st.success("Agent Added Successfully")
        if table_name == "sales":
            with st.form("add_sales"):
                listing_id = st.text_input("Listing ID")
                sale_price = st.number_input("Sale Price")
                date_sold = st.date_input("Date Sold")
                days_on_market = st.number_input("Days on Market")
                insert_btn = st.form_submit_button("Insert Record")
            if insert_btn:
                sql = """INSERT INTO sales VALUES (%s,%s,%s,%s)""" 
                values = (listing_id,sale_price,date_sold,days_on_market)
                cursor.execute(sql, values)
                conn.commit()
                st.success("Sale Added Successfully")
    if st.session_state.show_delete:
        pk = primary_keys[table_name]
        st.subheader("🗑 Delete Record")
        delete_id = st.selectbox(f"Select {pk}",df[pk].tolist(),key="delete_id")
        if st.button("Confirm Delete"):
            try:
                sql = f"DELETE FROM {table_name} WHERE {pk}=%s"
                cursor.execute(sql, (delete_id,))
                conn.commit()
                if cursor.rowcount > 0:
                    st.success("✅ Record Deleted Successfully")
                else:
                    st.warning("⚠ Record not found")
            except Exception as e:
                st.error(e)
                    