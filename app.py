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

# Function to calculate solar energy generation
def calculate_solar_generation(panel_type, efficiency, hours_sunlight=5):
    panel_ratings = {"125W": 125, "180W": 180, "375W": 375, "440W": 440}
    return panel_ratings[panel_type] * efficiency / 100 * hours_sunlight  # in Wh

# Function to estimate solar panel, battery, and inverter requirements
def calculate_system_requirements(total_energy):
    panel_options = {"125W": 125, "180W": 180, "375W": 375, "440W": 440}
    
    # Determine number of panels needed for each type
    panel_recommendations = {
        panel: math.ceil(total_energy / (panel_watt * 5))  # 5 hours sunlight
        for panel, panel_watt in panel_options.items()
    }

    # Battery capacity (Assuming 50% discharge, needs 2x energy storage)
    battery_capacity = math.ceil((total_energy / 1000) * 2)  # in kWh

    # Inverter size (should handle peak power)
    peak_power = max(panel_options.values())  # in Watts
    inverter_capacity = peak_power * 1.2  # Adding buffer

    # Cost estimation (Assumed values)
    panel_costs = {"125W": 5000, "180W": 7000, "375W": 15000, "440W": 18000}  # Per panel cost
    battery_cost_per_kWh = 12000
    inverter_cost_per_kW = 25000

    cost_estimations = {
        panel: (panel_recommendations[panel] * panel_costs[panel]) +
               (battery_capacity * battery_cost_per_kWh) +
               (inverter_capacity / 1000 * inverter_cost_per_kW)
        for panel in panel_options.keys()
    }

    return panel_recommendations, battery_capacity, inverter_capacity, cost_estimations

# Streamlit App
def main():
    st.title("Energy Meter and Solar System Estimator")
    
    # Appliance Selection Table
    st.header("Select Home Electrical Appliances and Usage")

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

    # Solar Panel Selection
    st.header("Solar Panel Selection")
    panel_type = st.selectbox("Choose Solar Panel Type", ["125W", "180W", "375W", "440W"])
    efficiency = st.slider("Solar Panel Efficiency (%)", min_value=50, max_value=100, value=90)

    solar_generated = calculate_solar_generation(panel_type, efficiency)
    
    # Grid Interaction
    grid_energy = max(0, total_energy - solar_generated)
    excess_solar = max(0, solar_generated - total_energy)
    bill_without_solar = (total_energy / 1000) * 8  # Rs.8 per kWh
    bill_with_solar = (grid_energy / 1000) * 8
    bill_credit = (excess_solar / 1000) * 5
    final_bill = max(0, bill_with_solar - bill_credit)

    # System Requirement Calculation
    panel_recommendations, battery_capacity, inverter_capacity, cost_estimations = calculate_system_requirements(total_energy)

    # Display Energy Consumption
    st.subheader("Energy Consumption & Solar Impact")
    st.write(f"Total Daily Energy Consumption: **{total_energy:.2f} Wh**")
    st.write(f"Solar Energy Generated: **{solar_generated:.2f} Wh**")
    st.write(f"Grid Energy Required: **{grid_energy:.2f} Wh**")
    st.write(f"Excess Solar Sent to Grid: **{excess_solar:.2f} Wh**")
    st.write(f"Estimated Bill Without Solar: **Rs. {bill_without_solar:.2f}**")
    st.write(f"Estimated Bill With Solar: **Rs. {bill_with_solar:.2f}**")
    st.write(f"Bill Credit for Exported Energy: **Rs. {bill_credit:.2f}**")
    st.success(f"Final Monthly Bill: **Rs. {final_bill:.2f}**")

    # Display Solar Recommendations
    st.subheader("Solar Panel & System Recommendations")
    for panel, count in panel_recommendations.items():
        st.write(f"**{panel}**: {count} panels required (Estimated Cost: **Rs. {cost_estimations[panel]:,.2f}**)")

    st.write(f"**Recommended Battery Capacity:** {battery_capacity} kWh")
    st.write(f"**Recommended Inverter Capacity:** {inverter_capacity:.2f} W")

    # User selection for affordability
    st.header("Customize Your Solar Setup")
    max_panels = st.number_input(
        "How many solar panels can you afford?",
        min_value=1,
        max_value=max(1, panel_recommendations[panel_type]),  # Ensures min is 1
        value=max(1, panel_recommendations[panel_type])
    )

    # Recalculate based on user's selected number of panels
    user_solar_generated = max_panels * calculate_solar_generation(panel_type, efficiency)
    user_grid_energy = max(0, total_energy - user_solar_generated)
    user_bill_with_solar = (user_grid_energy / 1000) * 8
    user_bill_credit = (max(0, user_solar_generated - total_energy) / 1000) * 5
    user_final_bill = max(0, user_bill_with_solar - user_bill_credit)

    st.subheader("Final Cost & Impact with Selected Panels")
    st.write(f"Selected Solar Panels: **{max_panels} x {panel_type}**")
    st.write(f"Solar Energy Generated: **{user_solar_generated:.2f} Wh**")
    st.write(f"New Grid Energy Required: **{user_grid_energy:.2f} Wh**")
    st.write(f"New Estimated Monthly Bill: **Rs. {user_final_bill:.2f}**")
    st.success(f"Final Cost for {max_panels} panels: **Rs. {max_panels * cost_estimations[panel_type]:,.2f}**")

if __name__ == "__main__":
    main()
