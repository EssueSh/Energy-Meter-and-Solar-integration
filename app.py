import streamlit as st
import pandas as pd

def calculate_energy_consumption(selected_appliances):
    total_energy = 0
    for _, row in selected_appliances.iterrows():
        total_energy += row["Wattage"] * row["Usage Hours"]
    return total_energy  # Total energy in Wh per day

def calculate_solar_requirements(total_energy, panel_type, efficiency, battery_backup):
    panel_ratings = {"125W": 125, "180W": 180, "375W": 375, "440W": 440}
    panel_wattage = panel_ratings[panel_type]
    solar_generated = panel_wattage * efficiency / 100 * 5  # Assuming 5 hours of sunlight

    panels_required = total_energy / solar_generated  
    battery_capacity = total_energy / 12  # 12V system (Wh to Ah)
    inverter_capacity = total_energy / 1000  # kW inverter required

    return panels_required, battery_capacity, inverter_capacity

def estimate_cost(panels_required, panel_type):
    panel_cost = {"125W": 5000, "180W": 7000, "375W": 15000, "440W": 18000}
    battery_cost_per_Ah = 150  
    inverter_cost_per_kW = 20000  

    panel_total_cost = panels_required * panel_cost[panel_type]
    battery_capacity = panels_required * 100  # Assuming each panel supports 100Ah battery
    battery_total_cost = battery_capacity * battery_cost_per_Ah
    inverter_total_cost = (battery_capacity / 100) * inverter_cost_per_kW

    return panel_total_cost, battery_total_cost, inverter_total_cost

def main():
    st.title("Solar Panel System Calculator")

    appliance_data = [
        ["LED Bulb", 10, 4],
        ["Ceiling Fan", 75, 6],
        ["Refrigerator", 150, 24],
        ["TV", 100, 5],
        ["Washing Machine", 500, 2],
        ["Microwave", 1200, 1],
        ["Air Conditioner", 1500, 8],
    ]

    df = pd.DataFrame(appliance_data, columns=["Appliance", "Wattage", "Usage Hours"])
    df.insert(0, "S.No", range(1, len(df) + 1))
    
    selected_rows = []

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
        total_energy = calculate_energy_consumption(selected_appliances)

        st.header("Solar Panel Selection")
        panel_type = st.selectbox("Choose Solar Panel Type", ["125W", "180W", "375W", "440W"])
        efficiency = st.slider("Solar Panel Efficiency (%)", min_value=50, max_value=100, value=90)
        battery_backup = st.slider("Battery Backup Required (hours)", min_value=0, max_value=24, value=5)

        panels_required, battery_capacity, inverter_capacity = calculate_solar_requirements(total_energy, panel_type, efficiency, battery_backup)
        panel_total_cost, battery_total_cost, inverter_total_cost = estimate_cost(panels_required, panel_type)

        total_system_cost = panel_total_cost + battery_total_cost + inverter_total_cost

        st.subheader("System Requirements and Estimated Cost")
        st.write(f"🔋 **Total Energy Consumption**: {total_energy:.2f} Wh per day")
        st.write(f"🔆 **Solar Panels Required**: {panels_required:.2f} ({panel_type})")
        st.write(f"🔋 **Battery Capacity Needed**: {battery_capacity:.2f} Ah (12V System)")
        st.write(f"⚡ **Inverter Capacity Required**: {inverter_capacity:.2f} kW")

        st.subheader("Cost Estimation")
        st.write(f"🛠️ **Solar Panel Cost**: Rs. {panel_total_cost:.2f}")
        st.write(f"🔋 **Battery Cost**: Rs. {battery_total_cost:.2f}")
        st.write(f"⚡ **Inverter Cost**: Rs. {inverter_total_cost:.2f}")
        st.success(f"💰 **Total Estimated Cost**: Rs. {total_system_cost:.2f}")

        st.header("Customize Your System")
        max_panels = st.number_input("How many solar panels can you afford?", min_value=1, max_value=int(panels_required), value=int(panels_required))
        
        adjusted_panels_required = min(max_panels, panels_required)
        adjusted_solar_generated = adjusted_panels_required * (panel_total_cost / panels_required)
        adjusted_grid_energy = max(0, total_energy - adjusted_solar_generated)
        adjusted_bill = (adjusted_grid_energy / 1000) * 8  # Rs.8 per kWh

        st.subheader("Updated System Based on Your Budget")
        st.write(f"🔆 **Selected Solar Panels**: {adjusted_panels_required}")
        st.write(f"⚡ **Updated Energy from Solar**: {adjusted_solar_generated:.2f} Wh")
        st.write(f"💡 **Updated Grid Energy Required**: {adjusted_grid_energy:.2f} Wh")
        st.success(f"💰 **New Estimated Monthly Bill**: Rs. {adjusted_bill:.2f}")

if __name__ == "__main__":
    main()
