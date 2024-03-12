import streamlit as st
import pandas as pd
import os
from users import user_page
from operators import operator_page

# Path to the user credentials Excel file
credentials_file = 'user_credentials.xlsx'

def check_file_exists(file_path):
    return os.path.exists(file_path)

def save_credentials(username, password, role):
    """Save the user credentials to an Excel file directly without hashing."""
    data = {
        'Username': [username],
        'Password': [password],  # Save password directly
        'Role': [role]
    }
    df = pd.DataFrame(data)
    if check_file_exists(credentials_file):
        with pd.ExcelWriter(credentials_file, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
            df.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)
    else:
        df.to_excel(credentials_file, index=False)

def validate_login(username, password):
    """Validate user login without hashing."""
    if check_file_exists(credentials_file):
        df = pd.read_excel(credentials_file)
        user_row = df.loc[df['Username'] == username]
        if not user_row.empty and user_row['Password'].values[0] == password:
            return True, user_row['Role'].values[0]
    return False, None

# Application starts here
st.title('Bus Ticket Reservation System')

tab1, tab2 = st.tabs(["Login", "Signup"])

with tab1:
    st.header("Login")
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")
    if st.button('Login'):
        valid, role = validate_login(login_username, login_password)
        if valid:
            st.success(f"Logged in successfully as {role}.")
            # Redirect based on role
            if role.lower() == 'operator':
                operator_page()
            elif role.lower() == 'user':
                user_page()
        else:
            st.error("Invalid username or password.")

with tab2:
    st.header("Signup")
    signup_username = st.text_input("Choose a Username", key="signup_username")
    signup_password = st.text_input("Choose a Password", type="password", key="signup_password")
    role = st.selectbox("Role", ["User", "Operator"], key="role")
    if st.button('Signup'):
        if not signup_username or not signup_password:
            st.error("Username and password cannot be empty.")
        else:
            save_credentials(signup_username, signup_password, role)
            st.success("Signup successful. You can now login.")
