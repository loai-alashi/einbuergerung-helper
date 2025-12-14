import os
import streamlit as st
from openai import OpenAI

from google import genai
from google.genai import types
from google.genai.errors import ClientError


# ------------------------------------------------------------
# Clients
# ------------------------------------------------------------
client_openai = OpenAI()
client_gemini = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

# ------------------------------------------------------------
# Persona / system prompts
# ------------------------------------------------------------
SYSTEM_PROMPT = """
You are 'Einbürgerung Helper' — a cautious assistant for German naturalisation (Einbürgerung).

Scope:
- Answer ONLY questions related to Einbürgerung in Germany
  (requirements, process, documents, language, tests, residence, timelines).
- If the question is not about Einbürgerung, refuse briefly and ask the user to rephrase.

Safety:
- You are NOT a lawyer. No legal advice. No guarantees.
- If unsure, say so and recommend contacting the local Ausländerbehörde.

Sources:
- Prefer official German sources and direct the user to them:
  bamf.de, bmi.bund.de, bva.bund.de, service.berlin.de, bundesregierung.de
- If asked about “latest changes”, say you cannot verify live updates and point to official sites.

Style:
- Simple, short, step-by-step answers.
- Ask 1–2 clarifying questions if needed.
"""

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
- Cite/mention the site you used (example: “According to bamf.de…”).
- Be short and clear. No legal advice.
"""

ALLOWED_DOMAINS = [
    "bamf.de",
    "bmi.bund.de",
    "bva.bund.de",
    "service.berlin.de",
    "bundesregierung.de",
]

OFFICIAL_SITE_QUERY = (
    "site:bamf.de OR site:bmi.bund.de OR site:bva.bund.de OR "
    "site:service.berlin.de OR site:bundesregierung.de"
)

# ------------------------------------------------------------
# Chat logic (ONE function, provider + optional search)
# ------------------------------------------------------------
def answer_question(user_q: str, provider: str, use_search: bool = False) -> str:
    system_prompt = SYSTEM_PROMPT_BROWSE if use_search else SYSTEM_PROMPT_FAST

    # --- OpenAI ---
    if provider == "OpenAI":
        if use_search:
            r = client_openai.responses.create(
                model="gpt-5",
                tools=[{"type": "web_search", "filters": {"allowed_domains": ALLOWED_DOMAINS}}],
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_q},
                ],
                timeout=20,
            )
            return r.output_text

        c = client_openai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_q},
            ],
        )
        return c.choices[0].message.content

    # --- Gemini ---
    query = user_q
    tools = None
    if use_search:
        query = OFFICIAL_SITE_QUERY + "\n\n" + user_q
        tools = [types.Tool(google_search=types.GoogleSearch())]

    resp = client_gemini.models.generate_content(
        model="gemini-2.0-flash",
        contents=query,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=tools,
        ),
    )
    return resp.text


# ------------------------------------------------------------
# Streamlit UI
# ------------------------------------------------------------
def render_tab4():
    st.write(
        "Ask general questions about German naturalisation (Einbürgerung). "
        "This chatbot gives simplified explanations, not legal advice."
    )

    provider = st.selectbox("Provider", ["OpenAI", "Gemini"], index=0)
    use_official = st.toggle("Use official sources", value=False)

    st.caption("Mode: Official sources (slower)." if use_official else "Mode: Fast (no browsing).")
    st.markdown("---")

    # Chat memory
    if "chat" not in st.session_state:
        st.session_state.chat = []

    # Show history
    for m in st.session_state.chat:
        st.chat_message(m["role"]).write(m["content"])

    # Input
    prompt = st.chat_input("Ask about Einbürgerung…")

    if prompt:
        st.session_state.chat.append({"role": "user", "content": prompt})
        reply = answer_question(prompt, provider=provider, use_search=use_official)
        st.session_state.chat.append({"role": "assistant", "content": reply})
        st.rerun()


if __name__ == "__main__":
    render_tab4()
