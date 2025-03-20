import streamlit as st
import pandas as pd
import math

# Constants for cost estimation
PANEL_COST_PER_WATT = 40  # Approx Rs. per watt
BATTERY_COST_PER_KWH = 10000  # Rs. per kWh
INVERTER_COST_PER_KW = 12000  # Rs. per kW

# Function to calculate total energy consumption
def calculate_energy_consumption(appliances):
    total_energy = 0
    for _, row in appliances.iterrows():
        if row["Selected"]:
            total_energy += row["Watt"] * row["Usage Hours"]
    return total_energy  # in Wh (Watt-hours)

# Function to estimate system requirements
def calculate_system_requirements(total_energy, panel_watt, num_panels=None):
    required_panels = math.ceil(total_energy / (panel_watt * 5))  # 5 sun hours

    if num_panels is None:
        num_panels = required_panels  # Default to fully meeting the demand

    # Battery capacity (Assuming 50% discharge, needs 2x energy storage)
    battery_capacity = math.ceil((total_energy / 1000) * 2)  # in kWh

    # Inverter capacity should match peak power demand
    inverter_capacity = max(panel_watt, total_energy / 5) * 1.2  # Adding buffer

    # Cost Estimation
    panel_cost = num_panels * panel_watt * PANEL_COST_PER_WATT
    battery_cost = battery_capacity * BATTERY_COST_PER_KWH
    inverter_cost = (inverter_capacity / 1000) * INVERTER_COST_PER_KW
    total_cost = panel_cost + battery_cost + inverter_cost

    return required_panels, battery_capacity, inverter_capacity, total_cost, panel_cost

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

    # Step 1: Auto-Calculate Required Panels, Battery & Inverter
    st.header("☀️ Solar System Requirement")
    selected_panel_watt = st.selectbox("Select panel wattage", [125, 180, 375, 440])

    panels_required, battery_capacity, inverter_capacity, total_cost, panel_cost = calculate_system_requirements(total_energy, selected_panel_watt)

    # Display Required Setup
    st.subheader("🔍 Estimated Solar Setup")
    st.write(f"**Total Energy Consumption:** {total_energy:.2f} Wh/day")
    st.write(f"**Panels Required to Meet Demand:** {panels_required} x {selected_panel_watt}W panels")
    st.write(f"**Battery Capacity Required:** {battery_capacity} kWh")
    st.write(f"**Inverter Capacity Required:** {inverter_capacity:.2f} W")
    st.write(f"**Estimated Total Cost:** Rs. {total_cost:,.2f}")

    # Step 2: User Enters Custom Panels
    st.header("🔧 Customize Your Setup")

    num_panels = st.number_input("Enter the number of solar panels you can afford", min_value=1, value=panels_required)

    # Recalculate based on User's Budget
    panels_required, battery_capacity, inverter_capacity, total_cost, panel_cost = calculate_system_requirements(total_energy, selected_panel_watt, num_panels)

    solar_generated = selected_panel_watt * num_panels * 5  # Assuming 5 hours of sunlight
    grid_energy = max(0, total_energy - solar_generated)
    excess_solar = max(0, solar_generated - total_energy)

    # Smart Meter and Bill Calculation
    bill_without_solar = (total_energy / 1000) * 8  # Rs.8 per kWh
    bill_with_solar = (grid_energy / 1000) * 8
    bill_credit = (excess_solar / 1000) * 5
    final_bill = max(0, bill_with_solar - bill_credit)

    # Display Results
    st.subheader("🔍 Updated Energy & Bill Estimation")
    st.write(f"Solar Energy Generated: **{solar_generated:.2f} Wh**")
    st.write(f"Grid Energy Required: **{grid_energy:.2f} Wh**")
    st.write(f"Excess Solar Sent to Grid: **{excess_solar:.2f} Wh**")
    st.write(f"Estimated Bill Without Solar: **Rs. {bill_without_solar:.2f}**")
    st.write(f"Estimated Bill With Solar: **Rs. {bill_with_solar:.2f}**")
    st.write(f"Bill Credit for Exported Energy: **Rs. {bill_credit:.2f}**")
    st.success(f"Final Monthly Bill: **Rs. {final_bill:.2f}**")

    # Custom System Output
    st.subheader("🔋 Final Solar System Recommendation")
    st.write(f"**Final Panel Setup:** {num_panels} x {selected_panel_watt}W panels")
    st.write(f"**Estimated Panel Cost:** Rs. {panel_cost:,.2f}")
    st.write(f"**Recommended Battery Capacity:** {battery_capacity} kWh")
    st.write(f"**Recommended Inverter Capacity:** {inverter_capacity:.2f} W")
    st.write(f"**Updated Total System Cost:** Rs. {total_cost:,.2f}")

if __name__ == "__main__":
    main()
