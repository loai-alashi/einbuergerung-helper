import streamlit as st
from ui_components import section_header



def render_tab5():
    section_header(
    "Official Information",
    "Official sources for Einbürgerung. Always confirm details with the authorities."
)

    st.markdown("""
    <div class="card-grid">

      <a class="card blue" href="https://www.bamf.de" target="_blank">
        <h3>BAMF</h3>
        <p>Federal Office for Migration and Refugees</p>
      </a>

      <a class="card yellow" href="https://www.bmi.bund.de" target="_blank">
        <h3>BMI</h3>
        <p>Federal Ministry of the Interior</p>
      </a>

      <a class="card green" href="https://service.berlin.de" target="_blank">
        <h3>Service Berlin</h3>
        <p>Appointments & official services (Berlin)</p>
      </a>

      <a class="card orange" href="https://www.bundesregierung.de" target="_blank">
        <h3>Bundesregierung</h3>
        <p>Federal government information</p>
      </a>

      <a class="card purple" href="https://www.bva.bund.de" target="_blank">
        <h3>BVA</h3>
        <p>Federal Office of Administration</p>
      </a>

      <a class="card blue" href="https://www.gesetze-im-internet.de" target="_blank">
        <h3>Gesetze im Internet</h3>
        <p>Official German law portal</p>
      </a>

      <a class="card green" href="https://www.bundesrat.de" target="_blank">
        <h3>Bundesrat</h3>
        <p>Federal Council information</p>
      </a>

      <a class="card orange" href="https://www.bundestag.de" target="_blank">
        <h3>Bundestag</h3>
        <p>German parliament information</p>
      </a>

      <a class="card yellow" href="https://www.deutschland.de" target="_blank">
        <h3>Deutschland.de</h3>
        <p>Germany portal (facts & life in Germany)</p>
      </a>

      <a class="card purple" href="https://verwaltung.bund.de" target="_blank">
        <h3>Verwaltungportal</h3>
        <p>Administrative services portal</p>
      </a>

    </div>
    """, unsafe_allow_html=True)