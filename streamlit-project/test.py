import streamlit as st
import requests

API_URL = "http://localhost:8000"  # Change if your FastAPI runs elsewhere

st.title("Customer Portal")

# Registration
st.header("Register New Customer")
with st.form("register_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Register")
    if submitted:
        resp = requests.post(
            f"{API_URL}/customer",
            json={"name": name, "email": email, "password": password}
        )
        if resp.status_code == 200:
            st.success("Registration successful!")
        else:
            st.error(resp.json())

# List Customers
if st.button("List All Customers"):
    resp = requests.get(f"{API_URL}/customers")
    if resp.status_code == 200:
        customers = resp.json()
        st.write(customers)
    else:
        st.error("Failed to fetch customers.")

# Get Customer by ID (with password)
st.header("Get Customer by ID")
customer_id = st.number_input("Customer ID", min_value=1, step=1)
password_lookup = st.text_input("Password for Lookup", type="password")
if st.button("Get Customer"):
    resp = requests.get(
        f"{API_URL}/customer/{customer_id}",
        params={"password": password_lookup}
    )
    if resp.status_code == 200:
        st.write(resp.json())
    else:
        st.error(resp.json())