import streamlit as st

# Function to calculate total energy consumption
def calculate_energy_consumption(appliances):
    total_energy = sum(watt * hours for watt, hours in appliances)
    return total_energy

# Function to calculate solar energy generation
def calculate_solar_generation(panel_type, efficiency, hours_sunlight=5):
    panel_ratings = {"125W": 125, "180W": 180, "375W": 375, "440W": 440}
    return panel_ratings[panel_type] * (efficiency / 100) * hours_sunlight if panel_type in panel_ratings else 0

# Streamlit app
def main():
    st.title("Energy Meter and Solar Panel Optimization")
    
    # Appliance selection
    st.header("Select Home Electrical Appliances")
    appliance_options = {
        "LED Bulb": 10, 
        "Ceiling Fan": 75, 
        "Refrigerator": 150, 
        "TV": 100,
        "Air Conditioner": 2000,
        "Washing Machine": 500
    }
    
    selected_appliances = st.multiselect("Choose appliances", list(appliance_options.keys()))

    appliances = []
    for appliance in selected_appliances:
        watt = st.number_input(f"Enter wattage for {appliance}", min_value=1, value=appliance_options[appliance])
        hours = st.number_input(f"Usage hours per day for {appliance}", min_value=0, step=1)
        appliances.append((watt, hours))

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
