# ui_components.py
import streamlit as st


def inject_global_css():
    st.markdown(
        """
        <style>
          /* --- Global spacing (less “floating”) --- */
          .block-container { padding-top: 2rem; padding-bottom: 2.5rem; max-width: 1100px; }
          [data-testid="stHorizontalBlock"] { gap: 0.9rem; }

          /* --- Header card --- */
          .tg-header {
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 22px;
            padding: 26px 26px 18px 26px;
            background: radial-gradient(900px 280px at 15% 10%, rgba(255,77,75,0.18), rgba(0,0,0,0) 60%),
                        rgba(255,255,255,0.02);
            box-shadow: 0 18px 60px rgba(0,0,0,0.35);
            margin-bottom: 18px;
          }
          .tg-header h1 {
            margin: 0;
            font-size: 2.2rem;
            letter-spacing: 0.2px;
          }
          .tg-header p {
            margin: 10px 0 0 0;
            opacity: 0.85;
            font-size: 1.02rem;
          }

          /* --- Link cards (Official info + Learn German) --- */
          .card-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
          @media (max-width: 1100px) { .card-grid { grid-template-columns: repeat(2, 1fr);} }
          @media (max-width: 650px)  { .card-grid { grid-template-columns: 1fr;} }

          a.card {
            display:block;
            padding: 14px 16px;
            border-radius: 16px;
            text-decoration:none;
            border: 2px solid rgba(255,255,255,0.08);
            background: rgba(255,255,255,0.02);
            box-shadow: 0 14px 35px rgba(0,0,0,0.30);
            transition: all .18s ease;
          }
          a.card:hover {
            transform: translateY(-2px);
            border-color: rgba(255,255,255,0.25);
          }
          a.card h3 { margin: 0; font-size: 1.02rem; }
          a.card p  { margin: 6px 0 0 0; opacity: 0.8; font-size: 0.95rem; }

          /* Hover accent colours */
          .card.red:hover    { border-color: #ff4d4b; box-shadow: 0 14px 45px rgba(255,77,75,0.15); }
          .card.yellow:hover { border-color: #fadb14; box-shadow: 0 14px 45px rgba(250,219,20,0.12); }
          .card.green:hover  { border-color: #52c41a; box-shadow: 0 14px 45px rgba(82,196,26,0.12); }
          .card.blue:hover   { border-color: #1677ff; box-shadow: 0 14px 45px rgba(22,119,255,0.12); }
          .card.orange:hover { border-color: #fa8c16; box-shadow: 0 14px 45px rgba(250,140,22,0.12); }
          .card.purple:hover { border-color: #722ed1; box-shadow: 0 14px 45px rgba(114,46,209,0.12); }
          .card.cyan:hover   { border-color: #13c2c2; box-shadow: 0 14px 45px rgba(19,194,194,0.12); }
          .card.magenta:hover{ border-color: #eb2f96; box-shadow: 0 14px 45px rgba(235,47,150,0.12); }
          .card.lime:hover   { border-color: #a0d911; box-shadow: 0 14px 45px rgba(160,217,17,0.12); }
          .card.geekblue:hover{border-color:#2f54eb; box-shadow: 0 14px 45px rgba(47,84,235,0.12); }
          .card.gold:hover   { border-color: #faad14; box-shadow: 0 14px 45px rgba(250,173,20,0.12); }
          .card.volcano:hover{ border-color: #fa541c; box-shadow: 0 14px 45px rgba(250,84,28,0.12); }

          /* --- Chat container card --- */
          .chat-container {
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 20px;
            padding: 24px;
            padding-bottom: 24px;
            background: rgba(255,255,255,0.02);
            box-shadow: 0 14px 40px rgba(0,0,0,0.30);
            margin-bottom: 20px;
          }
          
          /* Remove extra padding when chat area is empty */
          .chat-container:has(> .chat-settings:only-child) {
            padding-bottom: 24px;
          }

          /* --- Settings panel within chat --- */
          .chat-settings {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 14px;
            padding: 18px 20px;
            margin-bottom: 20px;
          }

          /* --- Hide empty chat message containers (pills) --- */
          [data-testid="stChatMessage"]:empty,
          [data-testid="stChatMessage"]:has(> div:empty),
          div[data-testid="stChatMessage"]:not(:has(*)) {
            display: none !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            visibility: hidden !important;
          }
          
          /* Hide empty chat message content areas */
          [data-testid="stChatMessageContent"]:empty,
          [data-testid="stChatMessageContent"]:not(:has(*)) {
            display: none !important;
            height: 0 !important;
          }
          
          /* Hide any empty rounded containers that look like pills */
          .chat-container > div:empty,
          .chat-container > [class*="stChat"]:empty,
          .chat-container > [data-testid]:empty {
            display: none !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
          }
          
          /* Hide Streamlit's empty chat message placeholders */
          div[data-testid="stChatMessage"]:not(:has([data-testid="stChatMessageContent"] *)) {
            display: none !important;
          }
          
          /* More aggressive: hide any div that looks like an empty chat container */
          .chat-container div[class*="message"]:empty,
          .chat-container div[class*="Message"]:empty {
            display: none !important;
          }

        </style>
        """,
        unsafe_allow_html=True,
    )


def section_header(title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div class="tg-header">
          <h1>{title}</h1>
          <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# IMPORTANT:
# These used to print HTML "wrappers", which created the empty rounded pills.
# Keep them for compatibility, but make them NO-OP.
def card_open():
    return


def card_close():
    return
