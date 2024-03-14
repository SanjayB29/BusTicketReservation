import streamlit as st
from auth import auth_page
from users import user_page
from operators import operator_page

# Initialize session state variables if they don't exist
if 'is_logged_in' not in st.session_state:
    st.session_state['is_logged_in'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = ''

def main():
    if not st.session_state['is_logged_in']:
        # User is not logged in, show the authentication page
        auth_page()
    else:
        # User is logged in, redirect based on role
        if st.session_state['user_role'].lower() == 'user':
            user_page()
        elif st.session_state['user_role'].lower() == 'operator':
            operator_page()
        else:
            st.error("Unknown user role. Please login again.")
            st.session_state['is_logged_in'] = False  # Reset login state to force re-authentication

if __name__ == "__main__":
    main()
