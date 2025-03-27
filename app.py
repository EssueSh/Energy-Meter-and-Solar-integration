import streamlit as st
import pandas as pd
import math
import pickle
import matplotlib.pyplot as plt

# Constants for cost estimation
PANEL_COST_PER_WATT = 40  # Rs. per watt
BATTERY_COST_PER_KWH = 10000  # Rs. per kWh
INVERTER_COST_PER_KW = 12000  # Rs. per kW

MODEL_PATH = "energy_model.pkl"
SCALER_PATH = "scaler.pkl"

@st.cache_resource
def load_model():
    try:
        with open(MODEL_PATH, "rb") as model_file:
            model = pickle.load(model_file)
        with open(SCALER_PATH, "rb") as scaler_file:
            scaler = pickle.load(scaler_file)
        st.write("✅ Model and scaler loaded successfully.")
        return model, scaler
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        return None, None


def predict_energy(data):
    model, scaler = load_model()
    if model is None or scaler is None:
        st.error("Model loading failed. Predictions cannot be made.")
        return None
    scaled_data = scaler.transform(data)
    return model.predict(scaled_data)

def prediction_page():
    st.title("🔮 Energy Prediction")
    
    option = st.radio("Choose Input Method:", ("Manual Entry", "Upload File"))

    if option == "Manual Entry":
        temp = st.number_input("Temperature (°C)", value=25.0)
        humidity = st.number_input("Humidity (%)", value=50.0)
        wind_speed = st.number_input("Wind Speed (m/s)", value=5.0)
        solar_irradiance = st.number_input("Solar Irradiance (W/m²)", value=300.0)

        input_data = pd.DataFrame([[temp, humidity, wind_speed, solar_irradiance]],
                                  columns=["Temperature", "Humidity", "Wind Speed", "Solar Irradiance"])

        if st.button("Predict Energy"):
            prediction = predict_energy(input_data)
            if prediction is not None:
                st.success(f"Predicted Energy: {prediction[0]:.2f} kWh")

    elif option == "Upload File":
        uploaded_file = st.file_uploader("Upload CSV or Excel File", type=["csv", "xlsx"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
            st.write("Preview:", df.head())
            predictions = predict_energy(df)
            if predictions is not None:
                df["Predicted Energy"] = predictions
                st.write("Predictions:", df)
                st.download_button("Download Predictions", df.to_csv(index=False), "predictions.csv", "text/csv")

def main_page():
    st.title("Energy Meter & Solar System Estimator")
    
    # Appliance Selection
    st.header("⚡ Select Appliances & Usage Hours")
    data = {
        "Appliance": ["LED Bulb", "Ceiling Fan", "Refrigerator", "TV", "Washing Machine", "Microwave", "Laptop", "Iron"],
        "Watt": [10, 75, 150, 100, 500, 1200, 60, 1000],
        "Usage Hours": [0] * 8,
        "Selected": [False] * 8
    }
    df = pd.DataFrame(data)

    edited_df = st.data_editor(df, use_container_width=True,
                               num_rows="fixed",
                               column_config={
                                   "Selected": st.column_config.CheckboxColumn("Include?", help="Select appliances"),
                                   "Usage Hours": st.column_config.NumberColumn("Hours/Day", min_value=0, max_value=24, step=1),
                               })

    total_energy = sum(row["Watt"] * row["Usage Hours"] for _, row in edited_df.iterrows() if row["Selected"])
    
    st.header("☀️ Solar System Requirement")
    selected_panel_watt = st.selectbox("Select panel wattage", [125, 180, 375, 440])
    panels_required = math.ceil(total_energy / (selected_panel_watt * 5))
    
    battery_capacity = math.ceil((total_energy / 1000) * 2)
    inverter_capacity = max(selected_panel_watt, total_energy / 5) * 1.2
    total_cost = panels_required * selected_panel_watt * PANEL_COST_PER_WATT + battery_capacity * BATTERY_COST_PER_KWH + (inverter_capacity / 1000) * INVERTER_COST_PER_KW
    
    st.subheader("🔍 Estimated Solar Setup")
    st.write(f"Total Energy Consumption: **{total_energy:.2f} Wh/day**")
    st.write(f"Panels Required: **{panels_required} x {selected_panel_watt}W**")
    st.write(f"Battery Capacity Required: **{battery_capacity} kWh**")
    st.write(f"Inverter Capacity Required: **{inverter_capacity:.2f} W**")
    st.write(f"Estimated Total Cost: **Rs. {total_cost:,.2f}**")

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Energy Prediction"])
    
    if page == "Home":
        main_page()
    elif page == "Energy Prediction":
        prediction_page()

if __name__ == "__main__":
    main()
