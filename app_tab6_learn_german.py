import streamlit as st
from ui_components import section_header



def render_tab6():
    section_header(
    "Learn German",
    "Trusted platforms to improve your German for daily life and Einbürgerung."
)

    st.markdown("""
    <div class="card-grid">

      <a class="card blue" href="https://www.dw.com" target="_blank">
        <h3>Deutsche Welle (DW)</h3>
        <p>News, videos & easy German explanations</p>
      </a>

      <a class="card yellow" href="https://learngerman.dw.com" target="_blank">
        <h3>DW Learn German</h3>
        <p>Structured German courses (A1–B2)</p>
      </a>

      <a class="card green" href="https://www.goethe.de" target="_blank">
        <h3>Goethe-Institut</h3>
        <p>Official German courses & exams</p>
      </a>

      <a class="card orange" href="https://www.vhs-lernportal.de" target="_blank">
        <h3>VHS Lernportal</h3>
        <p>Free German learning by Volkshochschule</p>
      </a>

      <a class="card purple" href="https://www.deutschland.de" target="_blank">
        <h3>Deutschland.de</h3>
        <p>Language & life in Germany</p>
      </a>

      <a class="card blue" href="https://www.deutsch-to-go.de" target="_blank">
        <h3>Deutsch-to-go</h3>
        <p>Listening exercises with transcripts</p>
      </a>

      <a class="card green" href="https://www.deutschakademie.de" target="_blank">
        <h3>DeutschAkademie</h3>
        <p>Free grammar & vocabulary exercises</p>
      </a>

      <a class="card yellow" href="https://deutsch.info" target="_blank">
        <h3>Deutsch.info</h3>
        <p>Beginner to advanced German learning</p>
      </a>

      <a class="card orange" href="https://www.busuu.com" target="_blank">
        <h3>Busuu</h3>
        <p>Language learning app (freemium)</p>
      </a>

      <a class="card purple" href="https://www.babbel.com" target="_blank">
        <h3>Babbel</h3>
        <p>Structured paid German courses</p>
      </a>

    </div>
    """, unsafe_allow_html=True)