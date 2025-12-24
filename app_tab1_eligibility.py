import streamlit as st
from tensorflow.keras.models import load_model
import pickle
import pandas as pd
from ui_components import section_header, card_open, card_close

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
    section_header(
        "Eligibility Check",
        "Test whether you may qualify for German naturalisation."
    )

    # ---- Load model + preprocessors (cached) ----
    model = load_ann_model()
    feature_columns = load_feature_columns()
    scaler, label_encoder, onehot_encoder = load_preprocessors()

    nat_categories, permit_categories = onehot_encoder.categories_

    card_open()

    with st.form("elig_form", clear_on_submit=False):
        st.subheader("Your details")

        # --- Row 1: key numbers (compact) ---
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            years_in_germany = st.number_input("Years", min_value=0, max_value=60, value=5, step=1)
        with c2:
            age = st.number_input("Age", min_value=18, max_value=100, value=32, step=1)
        with c3:
            monthly_income_eur = st.number_input("Income (€)", min_value=0, max_value=10000, value=1800, step=50)
        with c4:
            months_tax_paid_last_12 = st.number_input("Tax months", min_value=0, max_value=12, value=12, step=1)

        # --- Row 2: language + permit/nationality (still compact) ---
        c5, c6, c7 = st.columns([1.2, 1.6, 1.6])
        with c5:
            language_level = st.selectbox("Language", ["A1", "A2", "B1", "B2", "C1", "C2"], index=2)
        with c6:
            nationality = st.selectbox(
                "Nationality",
                nat_categories,
                index=list(nat_categories).index("syria") if "syria" in nat_categories else 0,
            )
        with c7:
            resident_permit_type = st.selectbox(
                "Permit",
                permit_categories,
                index=list(permit_categories).index("permanent_residence")
                if "permanent_residence" in permit_categories
                else 0,
            )

        # --- Advanced toggles hidden (shorter page) ---
        with st.expander("More details (optional)", expanded=False):
            a1, a2 = st.columns(2)

            with a1:
                has_integration_course = int(st.checkbox("Integration course completed", value=True))
                passed_naturalisation_test = int(st.checkbox("Naturalisation test passed", value=True))
                currently_paying_taxes = int(st.checkbox("Currently paying taxes", value=True))
                financial_independent = int(st.checkbox("Financially independent", value=True))

            with a2:
                has_permanent_residence = int(st.checkbox("Permanent residence", value=False))
                has_criminal_record = int(st.checkbox("Criminal record", value=False))
                married_to_german = int(st.checkbox("Married to German citizen", value=False))
                children_in_germany = int(st.checkbox("Children in Germany", value=False))

        st.markdown("")
        submit = st.form_submit_button("Predict eligibility", use_container_width=True)

    card_close()

    if not submit:
        st.info("Fill in your details and click **Predict eligibility**.")
        return

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
    raw_df["language_level_encoded"] = label_encoder.transform(raw_df["language_level"])

    # 2) One-hot encode nationality + resident_permit_type
    ohe_array = onehot_encoder.transform(raw_df[["nationality", "resident_permit_type"]])
    ohe_cols = onehot_encoder.get_feature_names_out(["nationality", "resident_permit_type"])
    ohe_df = pd.DataFrame(ohe_array, columns=ohe_cols)

    # 3) Combine and drop original categorical columns
    full_df = pd.concat([raw_df, ohe_df], axis=1)
    full_df = full_df.drop(columns=["nationality", "resident_permit_type", "language_level"])

    # 4) Reorder columns to match training order
    missing_cols = set(feature_columns) - set(full_df.columns)
    if missing_cols:
        st.error(f"Missing columns in input: {missing_cols}")
        st.stop()

    X_input = full_df[feature_columns].copy()

    # 5) Scale + predict
    X_scaled = scaler.transform(X_input)
    prob = float(model.predict(X_scaled)[0][0])
    eligible_pred = prob >= 0.5

    card_open()
    st.markdown(f"### Result")
    st.markdown(f"**Predicted probability:** {prob:.2%}")

    if eligible_pred:
        st.success("✅ The model predicts: **Eligible** (demo prediction).")
    else:
        st.error("❌ The model predicts: **Not yet eligible** (demo prediction).")

    st.caption("This is a demo ML prediction, not legal advice.")
    card_close()
