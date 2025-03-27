import streamlit as st
import pandas as pd
import math
import pickle
import matplotlib.pyplot as plt

# Constants for cost estimation
PANEL_COST_PER_WATT = 40  # Approx Rs. per watt
BATTERY_COST_PER_KWH = 10000  # Rs. per kWh
INVERTER_COST_PER_KW = 12000  # Rs. per kW

MODEL_PATH = "energy_model.pkl"
SCALER_PATH = "scaler.pkl"

def load_model():
    with open(MODEL_PATH, "rb") as model_file:
        model = pickle.load(model_file)
    with open(SCALER_PATH, "rb") as scaler_file:
        scaler = pickle.load(scaler_file)
    return model, scaler

def predict_energy(data):
    model, scaler = load_model()
    scaled_data = scaler.transform(data)
    predictions = model.predict(scaled_data)
    return predictions

def prediction_page():
    st.title("🔮 Energy Prediction")
    
    option = st.radio("Choose Input Method:", ("Manual Entry", "Upload Excel File"))
    
    if option == "Manual Entry":
        col1, col2 = st.columns(2)
        with col1:
            temp = st.number_input("Temperature", value=25.0)
            humidity = st.number_input("Humidity", value=50.0)
        with col2:
            wind_speed = st.number_input("Wind Speed", value=5.0)
            solar_irradiance = st.number_input("Solar Irradiance", value=300.0)
        
        input_data = pd.DataFrame([[temp, humidity, wind_speed, solar_irradiance]],
                                  columns=["Temperature", "Humidity", "Wind Speed", "Solar Irradiance"])
        
        if st.button("Predict Energy"):
            prediction = predict_energy(input_data)[0]
            st.success(f"Predicted Energy: {prediction:.2f} kWh")
    
    elif option == "Upload Excel File":
        uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "csv"])
        if uploaded_file:
            df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith("xlsx") else pd.read_csv(uploaded_file)
            st.write("Preview:", df.head())
            predictions = predict_energy(df)
            df["Predicted Energy"] = predictions
            
            st.write("Predictions:", df)
            st.download_button("Download Predictions", df.to_csv(index=False), "predictions.csv", "text/csv")
            
            # Visualization
            fig, ax = plt.subplots()
            ax.plot(df.index, df["Predicted Energy"], label="Predicted Energy", color='orange')
            ax.set_xlabel("Day")
            ax.set_ylabel("Energy (kWh)")
            ax.set_title("Predicted Energy Generation for Next Month")
            ax.legend()
            st.pyplot(fig)

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to:", ["Solar System Estimator", "Energy Prediction"])
    
    if page == "Solar System Estimator":
        energy_estimator_page()
    elif page == "Energy Prediction":
        prediction_page()

def energy_estimator_page():
    st.title("Energy Meter & Solar System Estimator")

    # Appliance Selection Table
    st.header("⚡ Select Appliances & Usage Hours")
    data = {
        "Appliance": ["LED Bulb", "Ceiling Fan", "Refrigerator", "TV", "Washing Machine", "Microwave", "Laptop", "Iron"],
        "Watt": [10, 75, 150, 100, 500, 1200, 60, 1000],
        "Usage Hours": [0] * 8,
        "Selected": [False] * 8
    }
    df = pd.DataFrame(data)
    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="fixed",
        column_config={
            "Selected": st.column_config.CheckboxColumn("Include?", help="Select appliances to include in calculation"),
            "Usage Hours": st.column_config.NumberColumn("Hours/Day", min_value=0, max_value=24, step=1),
        }
    )
    total_energy = calculate_energy_consumption(edited_df)
    st.header("☀️ Solar System Requirement")
    selected_panel_watt = st.selectbox("Select panel wattage", [125, 180, 375, 440])
    panels_required, battery_capacity, inverter_capacity, total_cost, panel_cost = calculate_system_requirements(total_energy, selected_panel_watt)
    st.subheader("🔍 Estimated Solar Setup")
    st.write(f"**Total Energy Consumption:** {total_energy:.2f} Wh/day")
    st.write(f"**Panels Required to Meet Demand:** {panels_required} x {selected_panel_watt}W panels")
    st.write(f"**Battery Capacity Required:** {battery_capacity} kWh")
    st.write(f"**Inverter Capacity Required:** {inverter_capacity:.2f} W")
    st.write(f"**Estimated Total Cost:** Rs. {total_cost:,.2f}")
    st.header("🔧 Customize Your Setup")
    num_panels = st.number_input("Enter the number of solar panels you can afford", min_value=1, value=max(1, panels_required))
    panels_required, battery_capacity, inverter_capacity, total_cost, panel_cost = calculate_system_requirements(total_energy, selected_panel_watt, num_panels)
    solar_generated = selected_panel_watt * num_panels * 5
    grid_energy = max(0, total_energy - solar_generated)
    excess_solar = max(0, solar_generated - total_energy)
    bill_without_solar = (total_energy / 1000) * 8
    bill_with_solar = (grid_energy / 1000) * 8
    bill_credit = (excess_solar / 1000) * 5
    final_bill = max(0, bill_with_solar - bill_credit)
    st.subheader("🔍 Updated Energy & Bill Estimation")
    st.write(f"Solar Energy Generated: **{solar_generated:.2f} Wh**")
    st.write(f"Grid Energy Required: **{grid_energy:.2f} Wh**")
    st.write(f"Excess Solar Sent to Grid: **{excess_solar:.2f} Wh**")
    st.write(f"Estimated Bill Without Solar: **Rs. {bill_without_solar:.2f}**")
    st.write(f"Estimated Bill With Solar: **Rs. {bill_with_solar:.2f}**")
    st.write(f"Bill Credit for Exported Energy: **Rs. {bill_credit:.2f}**")
    st.success(f"Final Monthly Bill: **Rs. {final_bill:.2f}**")
    st.subheader("🔋 Final Solar System Recommendation")
    st.write(f"**Final Panel Setup:** {num_panels} x {selected_panel_watt}W panels")
    st.write(f"**Estimated Panel Cost:** Rs. {panel_cost:,.2f}")
    st.write(f"**Recommended Battery Capacity:** {battery_capacity} kWh")
    st.write(f"**Recommended Inverter Capacity:** {inverter_capacity:.2f} W")
    st.write(f"**Updated Total System Cost:** Rs. {total_cost:,.2f}")

if __name__ == "__main__":
    main()
