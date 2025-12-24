# app_main.py
import streamlit as st

from app_tab1_eligibility import render_tab1
from app_tab4_chatbot import render_tab4
from app_tab5_official_info import render_tab5
from app_tab6_learn_german import render_tab6
from app_tab7_technical import render_tab7
from app_tab8_quiz import render_tab8

from ui_components import inject_global_css


st.set_page_config(
    page_title="Einbürgerung Helper",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()

st.markdown("""
<div style="max-width: 1200px; margin: 0 auto;">
  <h1 style="margin-bottom: 0.2rem;">DE Einbürgerung Helper</h1>
  <p style="margin-top: 0; opacity: 0.85;">
    Prepare for German naturalisation (Einbürgerung)
    <br/>
    Learn • Practice • Check eligibility • Test your knowledge
  </p>
  <div style="
      margin: 0.8rem 0 1.2rem 0;
      padding: 0.65rem 0.9rem;
      border-left: 4px solid #ffcf5c;
      background: rgba(255, 207, 92, 0.08);
      border-radius: 12px;
  ">
    ⚠️ <i>This app is for learning and guidance only.</i><br/>
    <i>It is not legal advice. Always check official sources.</i>
  </div>
</div>
""", unsafe_allow_html=True)


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
