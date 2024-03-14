import streamlit as st
import pandas as pd
import os

# Path to the user credentials Excel file
credentials_file = 'user_credentials.xlsx'

def check_file_exists(file_path):
    """Check if a file exists."""
    return os.path.exists(file_path)

def save_credentials(username, password, role):
    """Save user credentials to an Excel file."""
    data = {
        'Username': [username],
        'Password': [password],  # For demonstration purposes; consider hashing in production
        'Role': [role]
    }
    df = pd.DataFrame(data)
    if check_file_exists(credentials_file):
        with pd.ExcelWriter(credentials_file, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
            df.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)
    else:
        df.to_excel(credentials_file, index=False)

def validate_login(username, password):
    """Validate user login credentials."""
    if check_file_exists(credentials_file):
        df = pd.read_excel(credentials_file)
        user_row = df.loc[df['Username'] == username]
        if not user_row.empty and user_row['Password'].values[0] == password:
            return True, user_row['Role'].values[0]
    return False, None

def show_login_page():
    """Display the login page."""
    st.header("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button('Login'):
        valid, role = validate_login(username, password)
        if valid:
            st.success(f"Logged in successfully as {role}.")
            st.session_state['is_logged_in'] = True
            st.session_state['user_role'] = role
        else:
            st.error("Invalid username or password.")

def show_signup_page():
    """Display the signup page."""
    st.header("Signup")
    username = st.text_input("Choose a Username", key="signup_username")
    password = st.text_input("Choose a Password", type="password", key="signup_password")
    role = st.selectbox("Role", ["User", "Operator"], key="role")
    if st.button('Signup'):
        save_credentials(username, password, role)
        st.success("Signup successful. You can now login.")
        st.session_state['signup_page'] = False  # Assuming you use this to toggle between login/signup

def auth_page():
    """Main function to display the authentication page."""
    st.title('Authentication')

    if 'signup_page' not in st.session_state:
        st.session_state['signup_page'] = False

    if st.session_state['signup_page']:
        show_signup_page()
    else:
        show_login_page()
        if st.button('Go to Signup'):
            st.session_state['signup_page'] = True

if __name__ == "__main__":
    auth_page()
