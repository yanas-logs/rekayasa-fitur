import streamlit as st
import json
import os

def load_apps_dataset():
    path = os.path.join('data', 'apps.json')
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"WhatsApp": "com.whatsapp"}

def apply_custom_css():
    st.markdown("""
        <style>
        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main {
            cursor: default !important;
            user-select: none;
        }
        input, textarea, [data-baseweb="input"] {
            cursor: text !important;
            user-select: text !important;
        }
        button, [role="combobox"], [data-testid="stMarkdownContainer"] a {
            cursor: pointer !important;
        }
        </style>
        """, unsafe_allow_html=True)