import streamlit as st
import pandas as pd

def calculate_energy_consumption(selected_appliances):
    total_energy = 0
    for _, row in selected_appliances.iterrows():
        total_energy += row["Wattage"] * row["Usage Hours"]
    return total_energy

def calculate_solar_generation(panel_type, efficiency, hours_sunlight=5):
    panel_ratings = {"125W": 125, "180W": 180, "375W": 375, "440W": 440}
    if panel_type not in panel_ratings:
        return 0
    return panel_ratings[panel_type] * efficiency / 100 * hours_sunlight

def main():
    st.title("Energy Meter and Solar Panel Optimization")

    # Define appliances with default wattage & hours
    appliance_data = [
        ["LED Bulb", 10, 4],
        ["Ceiling Fan", 75, 6],
        ["Refrigerator", 150, 24],
        ["TV", 100, 5],
        ["Washing Machine", 500, 2],
        ["Microwave", 1200, 1],
        ["Air Conditioner", 1500, 8],
    ]

    # Convert to DataFrame with Serial Number
    df = pd.DataFrame(appliance_data, columns=["Appliance", "Wattage", "Usage Hours"])
    df.insert(0, "S.No", range(1, len(df) + 1))  # Add serial number column
    
    # Create a dictionary to store selections
    selected_rows = []
    
    # Display Table with Checkboxes
    st.subheader("Select Appliances and Adjust Wattage & Hours")
    for i in range(len(df)):
        col1, col2, col3, col4, col5 = st.columns([0.5, 2, 2, 2, 1])
        with col1:
            st.write(df.loc[i, "S.No"])
        with col2:
            st.write(df.loc[i, "Appliance"])
        with col3:
            wattage = st.number_input(f"Wattage for {df.loc[i, 'Appliance']}", value=df.loc[i, "Wattage"], key=f"watt_{i}")
        with col4:
            usage_hours = st.number_input(f"Usage Hours for {df.loc[i, 'Appliance']}", value=df.loc[i, "Usage Hours"], key=f"hours_{i}")
        with col5:
            selected = st.checkbox("", key=f"select_{i}")
        
        if selected:
            selected_rows.append({"Appliance": df.loc[i, "Appliance"], "Wattage": wattage, "Usage Hours": usage_hours})
    
    selected_appliances = pd.DataFrame(selected_rows)

    if not selected_appliances.empty:
        total_energy = calculate_energy_consumption(selected_appliances)  # Daily consumption in Wh

        # Solar Panel Selection
        st.header("Solar Panel Selection")
        panel_type = st.selectbox("Choose Solar Panel Type", ["125W", "180W", "375W", "440W"])
        efficiency = st.slider("Solar Panel Efficiency (%)", min_value=50, max_value=100, value=90)
        solar_generated = calculate_solar_generation(panel_type, efficiency)

        # Grid Interaction & Bill Calculation
        st.header("Grid Interaction and Bill Calculation")
        grid_energy = max(0, total_energy - solar_generated)  # Energy required from grid
        excess_solar = max(0, solar_generated - total_energy)  # Extra energy sent to grid
        bill_without_solar = (total_energy / 1000) * 8  # Rs.8 per kWh
        bill_with_solar = (grid_energy / 1000) * 8  # After solar contribution
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
