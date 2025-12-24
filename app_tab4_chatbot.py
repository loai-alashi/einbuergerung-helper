# app_tab4_chatbot.py  (replace ONLY your render_tab4() with this one)

import streamlit as st
from ui_components import section_header, card_open, card_close

def _get_keys():
    openai_key = st.secrets.get("OPENAI_API_KEY")
    google_key = st.secrets.get("GOOGLE_API_KEY")
    return openai_key, google_key

from openai import OpenAI
import google.generativeai as genai


def _get_openai_client():
    api_key = st.secrets.get("OPENAI_API_KEY", "")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def _get_gemini_model():
    api_key = st.secrets.get("GOOGLE_API_KEY", "")
    if not api_key:
        return None

    genai.configure(api_key=api_key)

    # Try a few common model names (depends on the project/key availability)
    for name in ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro"]:
        try:
            return genai.GenerativeModel(name)
        except Exception:
            continue

    return None

def answer_question(user_q: str, provider: str, use_search: bool = False) -> str:
    system_prompt = (
        "You are an assistant for German naturalisation (Einbürgerung). "
        "This is not legal advice."
    )

    # OpenAI
    if provider == "OpenAI":
        client = _get_openai_client()
        if not client:
            return "OpenAI is not configured."

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_q},
            ],
        )
        return response.choices[0].message.content

    # Gemini
    model = _get_gemini_model()
    if not model:
        return "Gemini is not available."

    resp = model.generate_content(
        f"{system_prompt}\n\nUser question:\n{user_q}"
    )
    return resp.text


def render_tab4():
    section_header(
        "Chatbot",
        "Ask questions about German naturalisation (Einbürgerung). Not legal advice."
    )

    # --- Keys / available providers ---
    openai_key, google_key = _get_keys()

    provider_options = []
    if openai_key:
        provider_options.append("OpenAI")
    if google_key:
        provider_options.append("Gemini")

    if not provider_options:
        st.warning("Chatbot is disabled because API keys are missing in .streamlit/secrets.toml")
        return

    # --- Local UI-only CSS (groups elements into one 'panel') ---
    st.markdown("""
    <style>
      .chat-panel {
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 14px 14px 10px 14px;
        background: rgba(255,255,255,0.02);
        box-shadow: 0 14px 40px rgba(0,0,0,0.30);
        margin-bottom: 14px;
      }
      .chat-panel .hint {
        opacity: 0.75;
        font-size: 0.92rem;
        padding-top: 6px;
      }
      .chat-divider {
        height: 1px;
        background: rgba(255,255,255,0.08);
        margin: 12px 0 10px 0;
      }
    </style>
    """, unsafe_allow_html=True)

    # --- One grouped "panel" for settings + chat ---
    st.markdown('<div class="chat-panel">', unsafe_allow_html=True)

    # Settings row (NOT sidebar)
    c1, c2, c3 = st.columns([2.2, 2.2, 5.6])
    with c1:
        provider = st.selectbox(
            "Provider",
            provider_options,
            key="chat_provider",
            label_visibility="visible",
        )

    with c2:
        use_official = st.toggle(
            "Official sources",
            value=False,
            key="chat_official",
            help="Only applies to OpenAI (restricted to official domains).",
        )

    with c3:
        if provider != "OpenAI":
            st.markdown('<div class="hint">Gemini: fast mode (no official browsing).</div>', unsafe_allow_html=True)
        else:
            msg = "ON: Official sources mode (OpenAI web_search restricted)." if use_official else "OFF: Fast mode. No web browsing, information may be outdated."
            st.markdown(f'<div class="hint">{msg}</div>', unsafe_allow_html=True)

    st.markdown('<div class="chat-divider"></div>', unsafe_allow_html=True)

    # Chat memory
    if "chat" not in st.session_state:
        st.session_state.chat = []

    # Chat history inside a nice card
    card_open()
    for m in st.session_state.chat:
        st.chat_message(m["role"]).write(m["content"])
    card_close()

    # Input stays inside the same panel
    prompt = st.chat_input("Ask about Einbürgerung…")
    st.markdown("</div>", unsafe_allow_html=True)

    if prompt:
        st.session_state.chat.append({"role": "user", "content": prompt})
        reply = answer_question(prompt, provider=provider, use_search=(use_official and provider == "OpenAI"))
        st.session_state.chat.append({"role": "assistant", "content": reply})
        st.rerun()
