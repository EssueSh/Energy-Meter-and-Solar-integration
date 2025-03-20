import streamlit as st

def calculate_energy_consumption(appliances):
    total_energy = 0
    for appliance, usage in appliances.items():
        total_energy += appliance * usage
    return total_energy

def calculate_solar_generation(panel_type, efficiency, hours_sunlight=5):
    panel_ratings = {"125W": 125, "180W": 180, "375W": 375, "440W": 440}
    if panel_type not in panel_ratings:
        return 0
    return panel_ratings[panel_type] * efficiency / 100 * hours_sunlight

def main():
    st.title("Energy Meter and Solar Panel Optimization")
    
    # Appliance Selection
    st.header("Select Home Electrical Appliances")
    appliances = {
        "LED Bulb (10W)": st.number_input("Number of LED Bulbs", min_value=0, step=1) * 10,
        "Ceiling Fan (75W)": st.number_input("Number of Ceiling Fans", min_value=0, step=1) * 75,
        "Refrigerator (150W)": st.number_input("Number of Refrigerators", min_value=0, step=1) * 150,
        "TV (100W)": st.number_input("Number of TVs", min_value=0, step=1) * 100,
    }
    
    appliance_usage = {}
    for key in appliances.keys():
        appliance_usage[appliances[key]] = st.number_input(f"Usage hours for {key}", min_value=0, step=1)
    
    total_energy = calculate_energy_consumption(appliance_usage)  # Daily consumption in Wh
    
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
