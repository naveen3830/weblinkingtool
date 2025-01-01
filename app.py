import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import concurrent.futures
import time
import logging
from urllib3.exceptions import InsecureRequestWarning
import re
from streamlit_option_menu import option_menu
from demo import Home
from link import link
import hashlib
from config import AUTHORIZED_USERS  


st.set_page_config(page_title="Internal Linking Opportunities", layout="wide")

st.markdown(
        """
        <style>
        /* Main container adjustments */
        .main {
            background-color: #222f3b;
            color: #d2d2d6;
        }

        /* Title and headings styling */
        h1, h2, h3 {
            color: #1cb3e0;
            font-family: 'sans-serif';
        }

        /* Button adjustments */
        .stButton>button {
            background-color: #1cb3e0;
            color: #ffffff;
            border-radius: 8px;
            padding: 10px 20px;
            border: none;
            transition: 0.3s ease-in-out;
        }
        .stButton>button:hover {
            background-color: #148bb5;
        }

        /* Table styling */
        .stDataFrame {
            background-color: #344758;
            color: #d2d2d6;
            border: none;
        }

        /* Sidebar tweaks */
        .sidebar .sidebar-content {
            background-color: #344758;
        }
        .sidebar .sidebar-content h1 {
            color: #1cb3e0;
        }

        /* Download button styling */
        .stDownloadButton>button {
            background-color: #1cb3e0;
            color: #ffffff;
            border-radius: 8px;
            padding: 8px 16px;
            transition: 0.3s ease-in-out;
        }
        .stDownloadButton>button:hover {
            background-color: #148bb5;
        }

        /* Input field styling */
        input, textarea {
            background-color: #344758;
            color: #d2d2d6;
            border: 1px solid #1cb3e0;
            border-radius: 4px;
            padding: 8px;
        }

        /* Spinner styling */
        .stSpinner {
            color: #1cb3e0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def creds_entered():
    """Verify credentials when entered."""
    username = st.session_state["user"].strip()
    password = st.session_state["passwd"].strip()
    hashed_password = hash_password(password)
    
    if username in AUTHORIZED_USERS and AUTHORIZED_USERS[username] == hashed_password:
        st.session_state["authenticated"] = True
        st.session_state["username"] = username
    else:
        st.session_state["authenticated"] = False
        if not password:
            st.warning("Please enter password.")
        elif not username:
            st.warning("Please enter username.")
        else:
            st.error("Invalid Username/Password :face_with_raised_eyebrow:")

def authenticate_user():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
        st.session_state["username"] = None
    
    if not st.session_state["authenticated"]:
        st.markdown("""
            <style>
            .stApp {
                background-color: #f3f4f6;
            }
            div[data-testid="stVerticalBlock"] {
                padding: 2rem;
                max-width: 28rem;
                margin: 0 auto;
            }
            .stTextInput > div > div {
                background-color: #ffffff;
                color: #1f2937;
                border: 1px solid #d1d5db;
                border-radius: 0.375rem;
            }
            .stTextInput > label {
                color: #374151;
                font-weight: 500;
            }
            .stButton > button {
                background-color: #2563eb;
                color: white;
                width: 100%;
            }
            .stButton > button:hover {
                background-color: #1d4ed8;
            }
            </style>
        """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown('<div style="text-align: center; margin-bottom: 2rem;"><h1 style="color: #1f2937;">Welcome Back</h1><p style="color: #4b5563;">Please sign in to continue</p></div>', unsafe_allow_html=True)
            st.text_input(label="Username:", value="", key="user", on_change=creds_entered)
            st.text_input(label="Password:", value="", key="passwd", type="password", on_change=creds_entered)
        return False
    
    return True

def logout():
    """Handle user logout."""
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.session_state["user"] = ""
    st.session_state["passwd"] = ""

def main():
    if authenticate_user():
        # Show logout button in sidebar
        with st.sidebar:
            st.markdown("<h2 style='text-align: center;'>Menu</h2>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='text-align: center;'>Welcome, {st.session_state['username']}!</h4>", 
                    unsafe_allow_html=True)
            
            selected = option_menu(
                'Main Menu',
                ['URL Extractor', 'Keyword Analysis'],
                icons=['house', 'list-check'],
                default_index=0,
                menu_icon="cast"
            )
            
            if st.button("Logout"):
                logout()
                st.rerun()

        if selected == "URL Extractor":
            link()
        elif selected == "Keyword Analysis":
            Home()

if __name__ == "__main__":
    main()