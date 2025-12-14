import streamlit as st
from tensorflow.keras.models import load_model
import pickle
import pandas as pd

# ============================================================
# CACHED LOADERS (short & clean)
# ============================================================

@st.cache_resource
def load_ann_model():
    return load_model("models/eligibility_ann.keras")


@st.cache_resource
def load_feature_columns():
    # This should now only contain correct names,
    # including "language_level_encoded"
    with open("models/eligibility_feature_columns.pkl", "rb") as f:
        feature_columns = pickle.load(f)
    return feature_columns


@st.cache_resource
def load_preprocessors():
    with open("models/eligibility_scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    with open("models/eligibility_label_encoder.pkl", "rb") as f:
        label_encoder = pickle.load(f)
    with open("models/eligibility_onehot_encoder.pkl", "rb") as f:
        onehot_encoder = pickle.load(f)
    return scaler, label_encoder, onehot_encoder


# ============================================================
# MAIN TAB FUNCTION (used by app_main.py)
# ============================================================

def render_tab1():

 # --- Disclaimer box ---.


    st.markdown("""
    <style>
    .notice-box{border-left:6px solid #f5c542;padding:14px 16px;border-radius:10px;
    background:rgba(245,197,66,.18);color:inherit;}
    .notice-box b{font-size:1.05rem}
    .notice-box .small{opacity:.85}
    </style>
    <div class="notice-box">
    <b>⚠️ Important notice</b><div class="small">
    EN: This tool is not official advice.<br>
    DE: Dieses Tool ist keine offizielle Beratung.<br>
    RU: Этот инструмент не является официальной консультацией.<br>
    AR: هذه الأداة ليست نصيحة رسمية.<br><br>
    Results may be inaccurate or outdated. Always check official sources.
    </div></div>
    """, unsafe_allow_html=True)


    st.markdown("---")



    # ---- Load model + preprocessors (cached) ----
    model = load_ann_model()
    feature_columns = load_feature_columns()
    scaler, label_encoder, onehot_encoder = load_preprocessors()

    #with st.expander("Model details (technical)", expanded=False):
     #   st.success("✅ ANN model + preprocessors loaded.")
      #  st.write(f"Model expects **{len(feature_columns)}** input features.")
      #  st.write("First few feature names:")
      #  st.write(feature_columns[:5])
   # st.markdown("---")


    
    # ---- Useful official resources ----
   # with st.expander("Official information & helpful websites"):
   #     st.markdown(
    #        """
   # - [BAMF – Bundesamt für Migration und Flüchtlinge](https://www.bamf.de)
   # - [BMI – Bundesministerium des Innern](https://www.bmi.bund.de)
   # - [BVA – Bundesverwaltungsamt](https://www.bva.bund.de)
   # - [Einbürgerung.de – Information portal](https://www.einbuergerung.de)
   # - [Publikationen der Bundesregierung](https://www.publikationen-bundesregierung.de)
   # - [Integrationsbeauftragte der Bundesregierung](https://www.integrationsbeauftragte.de)
   # - [Handbook Germany](https://handbookgermany.de)
   # - [Deutschland.de](https://www.deutschland.de)
   # - [Tatsachen über Deutschland](https://www.tatsachen-ueber-deutschland.de)
   # - [Service-Portal (example: Berlin)](https://service.berlin.de)
     #       """
      #  )

    # ---- Learn German (recommended websites) ----
    #with st.expander("Learn German – Top websites"):
      #  st.markdown(
         #   """
   # - [DW – Deutsche Welle](https://www.dw.com)
   # - [Goethe Institut](https://www.goethe.de)
    #- [VHS Lernportal](https://www.vhs-lernportal.de)
    #- [Deutschland.de – German learning section](https://www.deutschland.de)
    #- [DW Learn German](https://learngerman.dw.com)
    #- [Deutsch-to-go](https://www.deutsch-to-go.de)
    #- [DeutschAkademie](https://www.deutschakademie.de)
   # - [Deutsch.info](https://deutsch.info)
    #- [Busuu](https://www.busuu.com)
   # - [Babbel](https://www.babbel.com)
     #       """
       # )

    # =======================================================
    # USER INPUT FORM
    # =======================================================

    st.subheader("Test the ANN with your own details")

    # --- Basic numeric inputs ---
    col1, col2 = st.columns(2)
    with col1:
        years_in_germany = st.number_input(
            "Years in Germany", min_value=0, max_value=60, value=5, step=1
        )
    with col2:
        age = st.number_input(
            "Age", min_value=18, max_value=100, value=32, step=1
        )

    monthly_income_eur = st.number_input(
        "Monthly income (EUR)", min_value=0, max_value=10000, value=1800, step=50
    )

    months_tax_paid_last_12 = st.number_input(
        "Months of tax paid in the last 12 months",
        min_value=0, max_value=12, value=12, step=1
    )

    # --- Language level (raw, will be label-encoded) ---
    language_level = st.selectbox(
        "Language level", ["A1", "A2", "B1", "B2", "C1", "C2"], index=2  # default B1
    )

    # --- Yes/No features as checkboxes -> 0/1 ---
    col3, col4 = st.columns(2)
    with col3:
        has_integration_course = int(
            st.checkbox("Completed integration course?", value=True)
        )
        passed_naturalisation_test = int(
            st.checkbox("Passed naturalisation test?", value=True)
        )
        has_permanent_residence = int(
            st.checkbox("Has permanent residence?", value=False)
        )
        currently_paying_taxes = int(
            st.checkbox("Currently paying taxes?", value=True)
        )

    with col4:
        has_criminal_record = int(
            st.checkbox("Has criminal record?", value=False)
        )
        financial_independent = int(
            st.checkbox("Financially independent?", value=True)
        )
        married_to_german = int(
            st.checkbox("Married to German citizen?", value=False)
        )
        children_in_germany = int(
            st.checkbox("Children living in Germany?", value=False)
        )

    # --- Categorical options from OneHotEncoder ---
    nat_categories, permit_categories = onehot_encoder.categories_

    nationality = st.selectbox(
        "Nationality",
        nat_categories,
        index=list(nat_categories).index("syria") if "syria" in nat_categories else 0,
    )

    resident_permit_type = st.selectbox(
        "Resident permit type",
        permit_categories,
        index=list(permit_categories).index("permanent_residence")
        if "permanent_residence" in permit_categories
        else 0,
    )

    # =======================================================
    # BUILD DATAFRAME FOR THIS PERSON
    # =======================================================

    example_person = {
        "years_in_germany": years_in_germany,
        "age": age,
        "monthly_income_eur": monthly_income_eur,
        "has_integration_course": has_integration_course,
        "passed_naturalisation_test": passed_naturalisation_test,
        "has_criminal_record": has_criminal_record,
        "has_permanent_residence": has_permanent_residence,
        "financial_independent": financial_independent,
        "married_to_german": married_to_german,
        "children_in_germany": children_in_germany,
        "months_tax_paid_last_12": months_tax_paid_last_12,
        "currently_paying_taxes": currently_paying_taxes,
        "language_level": language_level,
        "nationality": nationality,
        "resident_permit_type": resident_permit_type,
    }

    raw_df = pd.DataFrame([example_person])

    # 1) Encode language_level -> language_level_encoded
    raw_df["language_level_encoded"] = label_encoder.transform(
        raw_df["language_level"]
    )

    # 2) One-hot encode nationality + resident_permit_type
    ohe_array = onehot_encoder.transform(
        raw_df[["nationality", "resident_permit_type"]]
    )
    ohe_cols = onehot_encoder.get_feature_names_out(
        ["nationality", "resident_permit_type"]
    )
    ohe_df = pd.DataFrame(ohe_array, columns=ohe_cols)

    # 3) Combine and drop original categorical columns
    full_df = pd.concat([raw_df, ohe_df], axis=1)
    full_df = full_df.drop(
        columns=["nationality", "resident_permit_type", "language_level"]
    )

    # 4) Reorder columns to match training order
    missing_cols = set(feature_columns) - set(full_df.columns)
    if missing_cols:
        st.error(f"Missing columns in input: {missing_cols}")
        st.write("Current columns:", list(full_df.columns))
        st.write("Expected:", feature_columns)
        st.stop()

    X_input = full_df[feature_columns].copy()

    # 5) Scale + predict
    X_scaled = scaler.transform(X_input)
    prob = float(model.predict(X_scaled)[0][0])
    eligible_pred = prob >= 0.5

    st.markdown(f"**Predicted probability of being eligible:** {prob:.2%}")

    if eligible_pred:
        st.success("✅ The model predicts: **Eligible** (demo prediction).")
    else:
        st.error("❌ The model predicts: **Not yet eligible** (demo prediction).")


# Allow running this file alone if you want
if __name__ == "__main__":
    render_tab1()
