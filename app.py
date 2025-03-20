import streamlit as st

def energy_calculation():
    st.header("Energy Consumption Calculator")
    power = st.number_input("Enter Power (Watts)", min_value=1.0, step=0.1)
    time = st.number_input("Enter Time (Hours)", min_value=0.1, step=0.1)
    if st.button("Calculate Energy"):
        energy = power * time
        st.success(f"Total Energy Consumed: {energy} Wh")

def solar_panel_sizing():
    st.header("Solar Panel Sizing")
    load = st.number_input("Enter Load Requirement (Watts)", min_value=1.0, step=1.0)
    battery_capacity = st.number_input("Enter Battery Capacity (Ah)", min_value=1.0, step=1.0)
    voltage = st.number_input("Enter System Voltage (V)", min_value=1.0, step=1.0)
    inverter_efficiency = st.slider("Inverter Efficiency (%)", min_value=50, max_value=100, value=90)
    if st.button("Calculate Panel Size"):
        required_energy = load * 24 / (inverter_efficiency / 100)
        panel_capacity = required_energy / voltage
        st.success(f"Required Solar Panel Capacity: {panel_capacity:.2f} W")

def hybrid_system_simulation():
    st.header("Hybrid System Simulation")
    system_type = st.selectbox("Select System Type", ["Grid-Tied", "Hybrid"])
    grid_availability = st.checkbox("Is Grid Available?")
    if st.button("Simulate"):
        if system_type == "Grid-Tied" and grid_availability:
            st.success("System will prioritize grid power and export excess energy.")
        elif system_type == "Hybrid":
            st.success("System will use battery backup and switch to grid when needed.")
        else:
            st.warning("Grid is unavailable, system will rely on battery backup.")

def main():
    st.title("Energy Meter and Solar Panel App")
    option = st.sidebar.selectbox("Choose a Function", ["Energy Calculation", "Solar Panel Sizing", "Hybrid System Simulation"])
    if option == "Energy Calculation":
        energy_calculation()
    elif option == "Solar Panel Sizing":
        solar_panel_sizing()
    elif option == "Hybrid System Simulation":
        hybrid_system_simulation()

if __name__ == "__main__":
    main()
