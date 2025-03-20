import streamlit as st
import pandas as pd

# Function to calculate total energy consumption
def calculate_energy_consumption(appliances):
    total_energy = sum(appliance["Wattage"] * appliance["Hours"] for appliance in appliances if appliance["Hours"] > 0)
    return total_energy

# Function to calculate solar energy generation
def calculate_solar_generation(panel_type, efficiency, hours_sunlight=5):
    panel_ratings = {"125W": 125, "180W": 180, "375W": 375, "440W": 440}
    return panel_ratings[panel_type] * (efficiency / 100) * hours_sunlight if panel_type in panel_ratings else 0

# Streamlit app
def main():
    st.title("Energy Meter and Solar Panel Optimization")

    # Appliance Selection
    st.header("Select Home Electrical Appliances")
    
    # Default appliance data
    appliance_data = [
        {"Appliance": "LED Bulb", "Wattage": 10, "Hours": 0},
        {"Appliance": "Ceiling Fan", "Wattage": 75, "Hours": 0},
        {"Appliance": "Refrigerator", "Wattage": 150, "Hours": 0},
        {"Appliance": "TV", "Wattage": 100, "Hours": 0},
        {"Appliance": "Air Conditioner", "Wattage": 2000, "Hours": 0},
        {"Appliance": "Washing Machine", "Wattage": 500, "Hours": 0}
    ]

    # Create an editable table for selecting appliances
    df = pd.DataFrame(appliance_data)
    edited_df = st.experimental_data_editor(df, use_container_width=True, num_rows="fixed")

    # Convert edited DataFrame to list of dictionaries
    appliances = edited_df.to_dict("records")

    # Calculate total energy
    total_energy = calculate_energy_consumption(appliances)  # Daily consumption in Wh

    # Solar Panel Selection
    st.header("Solar Panel Selection")
    panel_type = st.selectbox("Choose Solar Panel Type", ["125W", "180W", "375W", "440W"])
    efficiency = st.slider("Solar Panel Efficiency (%)", min_value=50, max_value=100, value=90)
    solar_generated = calculate_solar_generation(panel_type, efficiency)

    # Grid Interaction
    st.header("Grid Interaction and Bill Calculation")
    grid_energy = max(0, total_energy - solar_generated)  # If solar can't meet demand, grid supplies
    excess_solar = max(0, solar_generated - total_energy)  # Extra energy sent to grid
    bill_without_solar = (total_energy / 1000) * 8  # Rs.8 per kWh
    bill_with_solar = (grid_energy / 1000) * 8  # After considering solar contribution
    bill_credit = (excess_solar / 1000) * 5  # Rs.5 per kWh for exported energy
    final_bill = max(0, bill_with_solar - bill_credit)

    # Display Results
    st.subheader("Energy Consumption & Savings")
    st.write(f"Daily Energy Consumption: {total_energy:.2f} Wh")
    st.write(f"Solar Energy Generated: {solar_generated:.2f} Wh")
    st.write(f"Grid Energy Required: {grid_energy:.2f} Wh")
    st.write(f"Excess Solar Sent to Grid: {excess_solar:.2f} Wh")
    st.write(f"Bill Without Solar: Rs. {bill_without_solar:.2f}")
    st.write(f"Bill With Solar: Rs. {bill_with_solar:.2f}")
    st.write(f"Bill Credit for Exported Energy: Rs. {bill_credit:.2f}")
    st.success(f"Final Monthly Bill: Rs. {final_bill:.2f}")

if __name__ == "__main__":
    main()
