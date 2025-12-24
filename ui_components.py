import streamlit as st

def inject_global_css():
    st.markdown(
        """
        <style>
        /* ===== App spacing ===== */
        .block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1200px; }

        /* ===== Reusable card ===== */
        .tg-card{
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 18px 18px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.22);
            backdrop-filter: blur(8px);
        }

        /* ===== Section header ===== */
        .tg-section{
            position: relative;
            overflow: hidden;
            border-radius: 22px;
            padding: 26px 26px;
            border: 1px solid rgba(255,255,255,0.10);
            background:
              radial-gradient(800px 200px at 10% 0%,
                rgba(255,77,75,0.20), rgba(0,0,0,0) 60%),
              rgba(255,255,255,0.02);
            box-shadow: 0 18px 45px rgba(0,0,0,0.35);
        }
        .tg-section h1{
            margin: 0;
            font-size: 42px;
            line-height: 1.1;
            font-weight: 800;
        }
        .tg-section p{
            margin: 10px 0 0 0;
            opacity: 0.85;
            font-size: 14px;
        }

        /* ===== Buttons ===== */
        .stButton > button{
            border-radius: 14px !important;
            padding: 0.7rem 1rem !important;
            border: 1px solid rgba(255,255,255,0.10) !important;
            background: rgba(255,255,255,0.04) !important;
        }
        .stButton > button:hover{
            transform: translateY(-1px);
        }

        /* ===== Inputs ===== */
        div[data-testid="stNumberInput"] input,
        div[data-testid="stTextInput"] input,
        div[data-testid="stTextArea"] textarea,
        div[data-testid="stSelectbox"] div[role="combobox"]{
            border-radius: 14px !important;
        }

        /* ===== Link cards grid (Official/Learn German) ===== */
        .card-grid{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 14px;
        }
        @media (max-width: 1100px){
            .card-grid{ grid-template-columns: repeat(2, minmax(0, 1fr)); }
        }
        @media (max-width: 650px){
            .card-grid{ grid-template-columns: repeat(1, minmax(0, 1fr)); }
        }

        a.card{
            display: block;
            text-decoration: none !important;
            color: inherit;
            padding: 16px 16px;
            border-radius: 16px;
            border: 2px solid rgba(255,255,255,0.10);
            background: rgba(255,255,255,0.03);
            box-shadow: 0 10px 28px rgba(0,0,0,0.22);
            transition: transform 0.15s ease, border-color 0.15s ease, background 0.15s ease;
        }
        a.card:hover{
            transform: translateY(-2px);
            background: rgba(255,255,255,0.045);
        }
        a.card h3{ margin: 0 0 6px 0; font-size: 18px; }
        a.card p{ margin: 0; opacity: 0.85; font-size: 13px; }

        /* Hover border colours */
        .card.red:hover { border-color: #ff4d4b; }
        .card.yellow:hover { border-color: #fadb14; }
        .card.green:hover { border-color: #52c41a; }
        .card.blue:hover { border-color: #1677ff; }
        .card.orange:hover { border-color: #fa8c16; }
        .card.purple:hover { border-color: #722ed1; }
        .card.teal:hover { border-color: #13c2c2; }
        .card.cyan:hover { border-color: #22b8cf; }
        .card.pink:hover { border-color: #eb2f96; }
        .card.magenta:hover { border-color: #c41d7f; }
        .card.lime:hover { border-color: #a0d911; }
        .card.gold:hover { border-color: #faad14; }
        .card.volcano:hover { border-color: #fa541c; }
        .card.geekblue:hover { border-color: #2f54eb; }
        .card.indigo:hover { border-color: #3f51b5; }
        .card.violet:hover { border-color: #8e44ad; }
        </style>
        """,
        unsafe_allow_html=True,
    )

def section_header(title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div class="tg-section">
          <h1>{title}</h1>
          <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def card_open():
    st.markdown('<div class="tg-card">', unsafe_allow_html=True)

def card_close():
    st.markdown("</div>", unsafe_allow_html=True)
