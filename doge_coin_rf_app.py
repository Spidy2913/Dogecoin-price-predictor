import streamlit as st
import numpy as np
import joblib
import base64

# Page configuration
st.set_page_config(page_title="Dogecoin Price Predictor", layout="wide")
st.title("🚀 Dogecoin Price Predictor")

# Add background image from local file
def set_background(image_path):
    with open(image_path, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
        background-color: rgba(0, 0, 0, 0.3);  /* semi-transparent overlay */
        background-blend-mode: darken;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Set background
set_background(r"C:\Users\niran\OneDrive\Documents\ML project - Random forest method\Designer.jpeg")

# Define features and model path
feature_names = ["open", "high", "low", "volume"]
model_path = "dogecoin_model.pkl"

# Use same column layout for consistency
left_col, _ = st.columns([1, 1])  # 50% width for left pane

# Load model inside left column
with left_col:
    try:
        model = joblib.load(model_path)
        st.success("✅ Pretrained model loaded successfully!")
    except Exception as e:
        st.error(f"❌ Could not load model: {e}")
        st.stop()

# Prediction function
def predict_and_display(values):
    try:
        input_array = np.array(values).reshape(1, -1)
        prediction = model.predict(input_array)[0]
        st.success(f"💰 Predicted Close Price: **{prediction:.4f}**")
    except Exception as err:
        st.error(f"❌ Prediction failed: {err}")

# Input UI in left column
with left_col:
    st.subheader("📥 Enter Feature Values")

    user_input = {}
    for feature in feature_names:
        user_input[feature] = st.number_input(
            f"{feature.capitalize()}:", 
            value=0.0, 
            format="%.6f"
        )

    # Checkbox and button
    auto_predict = st.checkbox("🔁 Auto-predict when values change", value=False)

    # Extract values and predict
    input_values = [user_input[feature] for feature in feature_names]
    if auto_predict:
        predict_and_display(input_values)
    elif st.button("📊 Predict Close Price"):
        predict_and_display(input_values)
