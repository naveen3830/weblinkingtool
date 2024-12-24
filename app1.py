import streamlit as st

# Sample user credentials
USER_CREDENTIALS = {
    "user1": "password1",
    "user2": "password2",
}

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Login form
if not st.session_state.authenticated:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.authenticated = True
            st.success("Login successful!")
        else:
            st.error("Invalid username or password")

# After login
if st.session_state.authenticated:
    st.title("Welcome to the App!")
    if st.button("Logout"):
        st.session_state.authenticated = False
