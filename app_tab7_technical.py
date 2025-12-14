import streamlit as st
import pickle

def render_tab7():
    st.title("Model details (technical info)")

    with open("models/eligibility_feature_columns.pkl", "rb") as f:
        cols = pickle.load(f)

    st.write(f"Model input features: **{len(cols)}**")
    st.write("First 10 feature names:")
    st.write(cols[:10])

    st.info("""
    - Model type: Artificial Neural Network (ANN)
    - Training data: Synthetic (demo purposes)
    - Output: Probability of eligibility
    - Threshold: 0.5
    - This model does NOT make legal decisions
    """)

