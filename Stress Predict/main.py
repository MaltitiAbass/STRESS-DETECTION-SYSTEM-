import streamlit as st
import pandas as pd
from Tabs import home, data, predict, visualise
from web_functions import (
    load_data, authenticate_user, register_user,
    get_all_users, reset_user_password, send_message,
    get_messages, verify_phone_number, authenticate_admin, reply_to_message,
    store_report, get_all_reports
)

# Configure the app
st.set_page_config(
    page_title='Acquah StressPredict',
    page_icon=':exclamation:',
    layout='wide',
    initial_sidebar_state='auto'
)

# Function to add CSS from a file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Use the local_css function to add your CSS file
local_css("style.css")

# Add JavaScript to handle button disabling
st.markdown("""
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            var buttons = document.querySelectorAll("button");
            buttons.forEach(function(button) {
                button.addEventListener("click", function() {
                    button.disabled = true;
                    setTimeout(function() {
                        button.disabled = false;
                    }, 500);
                });
            });
        });
    </script>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state.page = 'Login'
if 'forgot_username' not in st.session_state:
    st.session_state.forgot_username = ''
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# Load the data once to be used across different tabs
df, X, y = load_data()
st.session_state['df'] = df
st.session_state['X'] = X
st.session_state['y'] = y

# Display login or registration page if not logged in
if 'username' not in st.session_state:
    if st.session_state.page == 'Login':
        st.title("Acquah StressPredict Login")
        st.write("Welcome to Acquah StressPredict, your stress detection application.")
        with st.form(key='login_form'):
            username = st.text_input("Username", key='login_username')
            password = st.text_input("Password", type="password", key='login_password')
            submit_button = st.form_submit_button("Login")
            if submit_button:
                if authenticate_user(username, password):
                    st.session_state.username = username
                    st.session_state.page = 'Home'
                else:
                    st.error("Invalid username or password")
        if st.button("Forgot Password?", key='forgot_password_button'):
            st.session_state.page = 'Forgot Password'
        if st.button("Don't have an account? Register", key='register_button'):
            st.session_state.page = 'Register'
        if st.button("Admin Login", key='admin_login_button'):
            st.session_state.page = 'Admin Login'

    elif st.session_state.page == 'Admin Login':
        st.title("Acquah StressPredict Admin Login")
        st.write("Admin Login for Acquah StressPredict.")
        with st.form(key='admin_login_form'):
            username = st.text_input("Username", key='admin_username')
            password = st.text_input("Password", type="password", key='admin_password')
            submit_button = st.form_submit_button("Login")
            if submit_button:
                if authenticate_admin(username, password):
                    st.session_state.username = username
                    st.session_state.is_admin = True
                    st.session_state.page = 'Admin Dashboard'
                else:
                    st.error("Invalid admin credentials")
        if st.button("Back to Login", key='admin_back_to_login_button'):
            st.session_state.page = 'Login'

    elif st.session_state.page == 'Register':
        st.title("Acquah StressPredict Registration")
        st.write("Create a new account for Acquah StressPredict.")
        with st.form(key='register_form'):
            first_name = st.text_input("First Name", key='reg_first_name')
            last_name = st.text_input("Last Name", key='reg_last_name')
            email = st.text_input("Email", key='reg_email')
            phone_number = st.text_input("Phone Number", key='reg_phone_number')
            password = st.text_input("Password", type="password", key='reg_password')
            repeat_password = st.text_input("Repeat Password", type="password", key='reg_repeat_password')
            submit_button = st.form_submit_button("Register")
            if submit_button:
                if (password == repeat_password and
                    first_name and last_name and email and phone_number and password):
                    if register_user(first_name, last_name, email, phone_number, f"{first_name} {last_name}", password):
                        st.success(f"Registration successful, {first_name}! Please log in.")
                        st.session_state.page = 'Login'
                    else:
                        st.error("Registration failed, please try again.")
                elif password != repeat_password:
                    st.error("Passwords do not match")
                else:
                    st.error("Please fill out all fields")
        if st.button("Back to Login", key='register_back_to_login_button'):
            st.session_state.page = 'Login'

    elif st.session_state.page == 'Forgot Password':
        st.title("Acquah StressPredict Forgot Password")
        st.write("Reset your password for Acquah StressPredict.")
        with st.form(key='forgot_password_form'):
            st.text_input("Username", key='forgot_username_input')
            st.text_input("Phone Number", key='forgot_phone_number')
            submit_button = st.form_submit_button("Verify")
            if submit_button:
                if verify_phone_number(st.session_state.forgot_username_input, st.session_state.forgot_phone_number):
                    st.session_state.forgot_username = st.session_state.forgot_username_input
                    st.session_state.page = 'Reset Password'
                else:
                    st.error("Username and phone number do not match.")
        if st.button("Back to Login", key='forgot_back_to_login_button'):
            st.session_state.page = 'Login'

    elif st.session_state.page == 'Reset Password':
        st.title("Acquah StressPredict Reset Password")
        st.write("Enter a new password for your Acquah StressPredict account.")
        with st.form(key='reset_password_form'):
            new_password = st.text_input("New Password", type="password", key='reset_password')
            repeat_new_password = st.text_input("Repeat New Password", type="password", key='reset_repeat_password')
            submit_button = st.form_submit_button("Reset Password")
            if submit_button:
                if new_password == repeat_new_password:
                    reset_user_password(st.session_state.forgot_username, new_password)
                    st.success("Password reset successful. Please log in.")
                    st.session_state.page = 'Login'
                else:
                    st.error("Passwords do not match")
        if st.button("Back to Login", key='reset_back_to_login_button'):
            st.session_state.page = 'Login'
            

else:
    # Check if the logged-in user is an admin
    is_admin = st.session_state.get('is_admin', False)

    # Display the sidebar without the WhatsApp icon
    st.sidebar.title(f"Welcome, {st.session_state.username}!")
    if st.sidebar.button("Logout", key='logout_button_1'):
        st.session_state.clear()
        st.session_state.page = 'Login'

    if is_admin:
        # Admin dashboard
        st.sidebar.title("Admin Dashboard")
        page = st.sidebar.selectbox("Select a page", ["Home", "View Users", "Reports"], key='admin_selectbox')

        if page == "Home":
            home.app(df, X, y)
        elif page == "View Users":
            st.title("View Users")
            users = get_all_users()
            df_users = pd.DataFrame(users)
            st.table(df_users)
            with st.form(key='reset_password_admin_form'):
                username_to_reset = st.text_input("Enter username to reset password", key='reset_username')
                new_password = st.text_input("Enter new password", type='password', key='new_password')
                submit_button = st.form_submit_button("Reset Password")
                if submit_button:
                    if username_to_reset and new_password:
                        reset_user_password(username_to_reset, new_password)
                        st.success("Password reset successfully")
                    else:
                        st.error("Please enter both username and new password")
        elif page == "Reports":
            st.title("Reports")
            # Fetch and display reports
            reports = get_all_reports()
            for report in reports:
                st.write(f"**Title:** {report['title']}")
                st.write(f"**Description:** {report['description']}")
                st.write("---")
            if not reports:
                st.write("No reports found.")

    else:
        # Regular user interface
        page = st.sidebar.selectbox("Select a page", ["Home", "Predict", "Visualise", "Report Issue"], key='user_selectbox')

        if page == "Home":
            home.app(df, X, y)
        elif page == "Predict":
            predict.app(df, X, y)
        elif page == "Visualise":
            visualise.app(df, X, y)
        elif page == "Report Issue":
            st.title("Report an Issue")
            st.write(
                "If you need immediate assistance, please [click here to chat with us on WhatsApp](https://wa.me/233549916659)."
            )
            st.markdown("""
                <div style="background-color: #25D366; color: white; padding: 10px; border-radius: 5px;">
                    <a href="https://wa.me/233549916659" target="_blank" style="color: white; text-decoration: none;">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp" style="width:20px; height:20px; vertical-align:middle; margin-right:5px;"> Chat with us on WhatsApp
                    </a>
                </div>
            """, unsafe_allow_html=True)

            with st.form(key='report_issue_form'):
                title = st.text_input("Issue Title", key='report_title')
                description = st.text_area("Issue Description", key='report_description')
                submit_button = st.form_submit_button("Submit")
                if submit_button:
                    if title and description:
                        store_report(title, description)
                        st.success("Report submitted successfully")
                    else:
                        st.error("Please fill out both fields")
