# app_tab4_chatbot.py
# -------------------
# Chat tab (OpenAI + Gemini) with:
# 1) Clean single-row settings (Provider + Official sources + Status text + Reset)
# 2) No sidebar, no expander (so no “pill”)
# 3) Robust Gemini model fallback (fixes the 404 model-not-found problem)
# 4) Safe session-state init (no NameErrors)

import streamlit as st
from openai import OpenAI
from google import genai

try:
    from ui_components import section_header, card_open, card_close
except ImportError as e:
    st.error(f"Failed to import UI components: {e}")
    # Fallback definitions
    def section_header(title: str, subtitle: str = ""):
        st.markdown(f"### {title}")
        if subtitle:
            st.caption(subtitle)
    def card_open():
        return
    def card_close():
        return


# =========================
# 1) KEYS / CLIENTS
# =========================
def _get_keys():
    """Read API keys from Streamlit Secrets."""
    openai_key = st.secrets.get("OPENAI_API_KEY")
    google_key = st.secrets.get("GOOGLE_API_KEY")
    return openai_key, google_key


def _get_openai_client():
    """Create OpenAI client if key exists."""
    key = st.secrets.get("OPENAI_API_KEY")
    if not key:
        return None
    return OpenAI(api_key=key)


def _get_gemini_client():
    """Create Gemini client if key exists."""
    key = st.secrets.get("GOOGLE_API_KEY")
    if not key:
        return None
    return genai.Client(api_key=key)


# =========================
# 2) MODEL HELPERS (GEMINI)
# =========================
def _pick_gemini_model(client: genai.Client) -> str:
    """
    Gemini model names change across accounts/regions.
    We try common candidates first, then fall back to listing models.
    Returns a model id string usable by client.models.generate_content(...).
    """
    # Try the most common “flash” models first (fast + cheap).
    candidates = [
        "gemini-2.0-flash",
        "gemini-2.0-flash-lite",
        "gemini-1.5-flash",
        "gemini-1.5-flash-8b",
        "gemini-1.5-pro",
    ]

    # If list() works, we can pick something that exists in your project.
    try:
        available = []
        for m in client.models.list():
            name = getattr(m, "name", "") or ""
            # name sometimes looks like "models/gemini-2.0-flash"
            short = name.replace("models/", "")
            available.append(short)

        # Prefer flash if present
        for c in candidates:
            if c in available:
                return c

        # Otherwise pick any gemini model found
        for a in available:
            if a.startswith("gemini-"):
                return a
    except Exception:
        # If listing models is blocked, we just try candidates by execution below.
        pass

    # Default fallback (we will still catch errors when calling)
    return "gemini-2.0-flash"


# =========================
# 3) ANSWER FUNCTION
# =========================
def answer_question(user_q: str, provider: str) -> str:
    """
    Sends the user question to the selected provider and returns text.
    """
    system_prompt = (
        "You are an assistant for German naturalisation (Einbürgerung). "
        "This is not legal advice. Keep answers clear, practical, and short."
    )

    # ----- OpenAI -----
    if provider == "OpenAI":
        client = _get_openai_client()
        if not client:
            return "OpenAI is not configured (missing OPENAI_API_KEY)."

        try:
            r = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_q},
                ],
            )
            return (r.choices[0].message.content or "").strip()
        except Exception as e:
            return f"OpenAI error: {e}"

    # ----- Gemini -----
    g = _get_gemini_client()
    if not g:
        return "Gemini is not configured (missing GOOGLE_API_KEY)."

    # Pick a model that exists for YOUR account to avoid 404.
    model_id = _pick_gemini_model(g)

    # Try selected model first; if it fails, try common fallbacks.
    fallbacks = [model_id, "gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]
    tried = set()

    for mid in fallbacks:
        if mid in tried:
            continue
        tried.add(mid)
        try:
            r = g.models.generate_content(
                model=mid,
                contents=f"{system_prompt}\n\nUser question:\n{user_q}",
            )
            return (getattr(r, "text", "") or "").strip()
        except Exception as e:
            last_err = e

    return f"Gemini error: {last_err}"


# =========================
# 4) UI (TAB RENDER)
# =========================
def render_tab4():
    # ---- Page section header (top banner) ----
    section_header(
        "Chatbot",
        "Ask questions about German naturalisation (Einbürgerung). Not legal advice.",
    )

    # ---- Determine available providers based on keys ----
    openai_key, google_key = _get_keys()
    provider_options = []
    if openai_key:
        provider_options.append("OpenAI")
    if google_key:
        provider_options.append("Gemini")

    if not provider_options:
        st.warning("Chatbot is disabled because API keys are missing in Streamlit Secrets.")
        return

    # ---- Session state init (prevents NameErrors) ----
    if "chat" not in st.session_state:
        st.session_state.chat = []
    
    # Clean out any empty messages that might have been created
    st.session_state.chat = [m for m in st.session_state.chat if m.get("content") and str(m.get("content", "")).strip()]

    # Settings panel with background (separate from chat container)
    st.markdown('<div class="chat-settings">', unsafe_allow_html=True)
    
    # Settings row (everything on ONE line)
    c1, c2, c3, c4 = st.columns([2.2, 2.2, 4.5, 1.1])

    with c1:
        provider = st.selectbox(
            "Provider",
            provider_options,
            key="chat_provider",
            label_visibility="visible",
        )

    # Toggle behaves differently depending on provider
    with c2:
        if provider == "OpenAI":
            use_official = st.toggle(
                "Official sources",
                value=st.session_state.get("chat_official", False),
                key="chat_official",
                help="Planned: will restrict answers to official sources when enabled.",
            )
        else:
            # Disabled for Gemini (so the UI explains reality clearly)
            use_official = st.toggle(
                "Official sources",
                value=False,
                key="chat_official_disabled",
                disabled=True,
                help="Not available for Gemini.",
            )

    # Status text (the explanation you wanted, depending on provider + toggle)
    with c3:
        st.markdown("<br>", unsafe_allow_html=True)  # Vertical alignment
        if provider != "OpenAI":
            st.caption("💨 **Gemini:** Fast mode (no official browsing)")
        else:
            if use_official:
                st.caption("✅ **ON:** Official sources mode (OpenAI only)")
            else:
                st.caption("⚡ **OFF:** Fast mode. No web browsing, information may be outdated.")

    with c4:
        st.markdown("<br>", unsafe_allow_html=True)  # Vertical alignment
        if st.button("Reset", use_container_width=True, type="secondary"):
            st.session_state.chat = []
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close settings panel

    # Chat messages area - only show container if there are messages
    messages_to_show = [m for m in st.session_state.chat if m.get("content") and str(m.get("content", "")).strip()]
    
    if messages_to_show:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for m in messages_to_show:
            st.chat_message(m["role"]).write(m["content"])
        st.markdown('</div>', unsafe_allow_html=True)  # Close main container

    # Chat input (Streamlit renders this at the bottom; that’s normal)
    prompt = st.chat_input("Ask about Einbürgerung…")
    if prompt:
        st.session_state.chat.append({"role": "user", "content": prompt})
        reply = answer_question(prompt, provider=provider)
        st.session_state.chat.append({"role": "assistant", "content": reply})
        st.rerun()
