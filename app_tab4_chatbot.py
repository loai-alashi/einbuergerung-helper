import streamlit as st
from openai import OpenAI

# NEW Gemini SDK
from google import genai


# ------------------------------------------------------------
# Keys / Clients
# ------------------------------------------------------------
def _get_keys():
    openai_key = st.secrets.get("OPENAI_API_KEY")
    google_key = st.secrets.get("GOOGLE_API_KEY")
    return openai_key, google_key


def _get_openai_client():
    api_key = st.secrets.get("OPENAI_API_KEY", "")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def _get_gemini_client():
    api_key = st.secrets.get("GOOGLE_API_KEY", "")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)


# ------------------------------------------------------------
# Prompts
# ------------------------------------------------------------
SYSTEM_PROMPT_FAST = """
You are 'Einbürgerung Helper' for German naturalisation (Einbürgerung).

Mode: FAST (no browsing).
- Answer ONLY Einbürgerung questions.
- Be short and clear.
- Say clearly you are NOT checking websites right now and info may be outdated.
- You may recommend official sites, but do NOT claim you just verified anything.
"""

SYSTEM_PROMPT_BROWSE = """
You are 'Einbürgerung Helper' for German naturalisation (Einbürgerung).

Mode: OFFICIAL SOURCES (browsing).
- Answer ONLY Einbürgerung questions.
- Use web search results from allowed official domains when needed.
- Mention the site you used (example: “According to bamf.de…”).
- Be short and clear. No legal advice.
"""

ALLOWED_DOMAINS = [
    "bamf.de",
    "bmi.bund.de",
    "bva.bund.de",
    "service.berlin.de",
    "bundesregierung.de",
]


# ------------------------------------------------------------
# Chat logic
# ------------------------------------------------------------
def _answer_with_openai(user_q: str, use_search: bool) -> str:
    system_prompt = SYSTEM_PROMPT_BROWSE if use_search else SYSTEM_PROMPT_FAST

    client = _get_openai_client()
    if client is None:
        return "OpenAI is not configured (missing OPENAI_API_KEY)."

    if use_search:
        r = client.responses.create(
            model="gpt-5",
            tools=[{"type": "web_search", "filters": {"allowed_domains": ALLOWED_DOMAINS}}],
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_q},
            ],
        )
        return r.output_text

    c = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_q},
        ],
    )
    return c.choices[0].message.content


def _answer_with_gemini(user_q: str) -> str:
    client = _get_gemini_client()
    if client is None:
        return "Gemini is not configured (missing GOOGLE_API_KEY)."

    prompt = f"{SYSTEM_PROMPT_FAST}\n\nUser question:\n{user_q}"

    # Try a couple model names commonly supported by the new SDK
    model_names = ["gemini-2.0-flash", "gemini-1.5-flash"]

    last_error = None
    for name in model_names:
        try:
            resp = client.models.generate_content(
                model=name,
                contents=prompt,
            )
            return resp.text
        except Exception as e:
            last_error = e

    return f"Gemini failed. Last error: {last_error}"


def answer_question(user_q: str, provider: str, use_search: bool) -> str:
    if provider == "OpenAI":
        return _answer_with_openai(user_q, use_search=use_search)

    # provider == Gemini
    if use_search:
        return "Official sources mode is OpenAI-only right now. Switch provider to OpenAI for that."

    return _answer_with_gemini(user_q)


# ------------------------------------------------------------
# Streamlit UI
# ------------------------------------------------------------
def render_tab4():
    st.title("Chatbot")

    openai_key, google_key = _get_keys()

    provider_options = []
    if openai_key:
        provider_options.append("OpenAI")
    if google_key:
        provider_options.append("Gemini")

    if not provider_options:
        st.warning("Chatbot is disabled because API keys are missing in .streamlit/secrets.toml")
        return

    provider = st.selectbox("Provider", provider_options)
    use_official = st.toggle("Official sources (OpenAI only)", value=False)

    if "chat" not in st.session_state:
        st.session_state.chat = []

    for m in st.session_state.chat:
        st.chat_message(m["role"]).write(m["content"])

    prompt = st.chat_input("Ask about Einbürgerung…")
    if prompt:
        st.session_state.chat.append({"role": "user", "content": prompt})
        reply = answer_question(prompt, provider=provider, use_search=use_official)
        st.session_state.chat.append({"role": "assistant", "content": reply})
        st.rerun()


if __name__ == "__main__":
    render_tab4()
