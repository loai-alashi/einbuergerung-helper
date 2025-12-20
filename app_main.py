# app_main.py
import streamlit as st

from app_tab1_eligibility import render_tab1
from app_tab4_chatbot import render_tab4
from app_tab5_official_info import render_tab5
from app_tab6_learn_german import render_tab6
from app_tab7_technical import render_tab7
from app_tab8_quiz import render_tab8

st.set_page_config(page_title="Einbürgerung Helper", layout="wide")
st.title("Einbürgerung – Demo App")


tabs = st.tabs([
    "Eligibility",
    "Chatbot",
    "Official info",
    "Learn German",
    "Quiz",
    "Technical info",
])

with tabs[0]:
    render_tab1()

with tabs[1]:
    render_tab4()

with tabs[2]:
    render_tab5()

with tabs[3]:
    render_tab6()

with tabs[4]:
    render_tab8()

with tabs[5]:
    render_tab7()

