import streamlit as st
import pandas as pd
import math

# Function to calculate total energy consumption
def calculate_energy_consumption(appliances):
    total_energy = 0
    for _, row in appliances.iterrows():
        if row["Selected"]:
            total_energy += row["Watt"] * row["Usage Hours"]
    return total_energy  # in Wh (Watt-hours)

# Function to estimate system requirements based on panel wattage
def calculate_system_requirements(total_energy, panel_watt, num_panels):
    solar_generated = panel_watt * num_panels * 5  # Assuming 5 hours of sunlight

    # Battery capacity (Assuming 50% discharge, needs 2x energy storage)
    battery_capacity = math.ceil((total_energy / 1000) * 2)  # in kWh

    # Inverter capacity should match peak power demand
    inverter_capacity = max(panel_watt, total_energy / 5) * 1.2  # Adding buffer

    return solar_generated, battery_capacity, inverter_capacity

# Streamlit App
def main():
    st.title("🔋 Energy Meter & Solar System Estimator")

    # Appliance Selection Table
    st.header("⚡ Select Appliances & Usage Hours")

    data = {
        "Appliance": ["LED Bulb", "Ceiling Fan", "Refrigerator", "TV", "Washing Machine", "Microwave", "Laptop", "Iron"],
        "Watt": [10, 75, 150, 100, 500, 1200, 60, 1000],
        "Usage Hours": [0] * 8,  # Default values
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

    # User Input for Custom Solar Panel Configuration
    st.header("☀️ Customize Your Solar Setup")
    
    num_panels = st.number_input("Enter the number of solar panels you can afford", min_value=1, value=1)
    panel_watt = st.number_input("Enter the wattage of your selected panels", min_value=50, value=125)

    # Calculate System Requirements
    solar_generated, battery_capacity, inverter_capacity = calculate_system_requirements(total_energy, panel_watt, num_panels)

    # Smart Meter Readings
    grid_energy = max(0, total_energy - solar_generated)
    excess_solar = max(0, solar_generated - total_energy)
    bill_without_solar = (total_energy / 1000) * 8  # Rs.8 per kWh
    bill_with_solar = (grid_energy / 1000) * 8
    bill_credit = (excess_solar / 1000) * 5
    final_bill = max(0, bill_with_solar - bill_credit)

    # Display Results
    st.subheader("🔍 Energy Consumption & Solar Impact")
    st.write(f"Total Daily Energy Consumption: **{total_energy:.2f} Wh**")
    st.write(f"Solar Energy Generated: **{solar_generated:.2f} Wh**")
    st.write(f"Grid Energy Required: **{grid_energy:.2f} Wh**")
    st.write(f"Excess Solar Sent to Grid: **{excess_solar:.2f} Wh**")
    st.write(f"Estimated Bill Without Solar: **Rs. {bill_without_solar:.2f}**")
    st.write(f"Estimated Bill With Solar: **Rs. {bill_with_solar:.2f}**")
    st.write(f"Bill Credit for Exported Energy: **Rs. {bill_credit:.2f}**")
    st.success(f"Final Monthly Bill: **Rs. {final_bill:.2f}**")

    # Solar System Recommendations
    st.subheader("🔋 Solar System Requirements")
    st.write(f"**Solar Panel Setup:** {num_panels} x {panel_watt}W panels")
    st.write(f"**Battery Capacity Required:** {battery_capacity} kWh")
    st.write(f"**Inverter Capacity Required:** {inverter_capacity:.2f} W")

if __name__ == "__main__":
    main()
