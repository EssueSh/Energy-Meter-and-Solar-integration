import streamlit as st

# Appliance power ratings (in Watts)
appliance_power = {
    "Fan": 75,
    "Air Conditioner": 1500,
    "Refrigerator": 200,
    "LED Bulb": 10,
    "Washing Machine": 500,
    "Television": 100,
    "Iron": 1000,
    "Microwave Oven": 1200
}

def calculate_energy_consumption(appliance, hours_per_day):
    power = appliance_power[appliance]
    daily_energy = power * hours_per_day  # in Wh
    monthly_energy = (daily_energy * 30) / 1000  # Convert to kWh (Units)
    return monthly_energy

def calculate_solar_savings(monthly_energy, panel_capacity, panel_efficiency, electricity_rate=8):
    solar_generation = (panel_capacity * panel_efficiency / 100) * 30  # Monthly solar energy (kWh)
    grid_energy_needed = max(0, monthly_energy - solar_generation)
    monthly_bill = grid_energy_needed * electricity_rate
    return solar_generation, monthly_bill

# Streamlit UI
st.title("Energy Meter and Solar Panel Savings Calculator")

# Step 1: Select Appliance
st.header("1. Select Home Appliance")
appliance = st.selectbox("Choose an Appliance", list(appliance_power.keys()))
usage_hours = st.number_input("Daily Usage (Hours)", min_value=0.5, step=0.5)

if st.button("Calculate Monthly Energy Consumption"):
    monthly_energy = calculate_energy_consumption(appliance, usage_hours)
    st.success(f"Estimated Monthly Energy Consumption: {monthly_energy:.2f} kWh (Units)")
    
    # Step 2: Enter Solar Panel Details
    st.header("2. Solar Panel Specifications")
    panel_capacity = st.number_input("Solar Panel Capacity (Watts)", min_value=100, step=50)
    panel_efficiency = st.slider("Solar Panel Efficiency (%)", min_value=50, max_value=100, value=90)
    
    if st.button("Calculate Savings"):
        solar_generation, monthly_bill = calculate_solar_savings(monthly_energy, panel_capacity, panel_efficiency)
        st.success(f"Solar Energy Generated: {solar_generation:.2f} kWh per month")
        st.success(f"Estimated Monthly Electricity Bill: ₹{monthly_bill:.2f}")
        
        # Final Recommendation
        if monthly_bill == 0:
            st.balloons()
            st.success("Your solar system fully covers your energy needs! No electricity bill!")
        elif solar_generation > monthly_energy / 2:
            st.info("Great! Your solar panels significantly reduce your bill.")
        else:
            st.warning("Consider increasing solar capacity to save more!")
