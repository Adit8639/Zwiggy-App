import streamlit as st
import pandas as pd
import plotly.express as px

# 1. PAGE CONFIGURATION & STRICT CSS THEMING
st.set_page_config(page_title="Zwiggy Green-Route AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #000000; font-family: 'Helvetica Neue', sans-serif; }
    h1, h2, h3, p, span, div { color: #000000 !important; }
    .stMetric > div > div > div { color: #000000 !important; font-weight: 900 !important; }
    div[data-testid="stMetricValue"] { font-size: 3rem !important; }
    div[data-testid="stVerticalBlock"] > div[style*="border"] {
        border: 2px solid #000000 !important; background-color: #FAFAFA !important; border-radius: 8px; padding: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. HEADER
st.title("🟢 Zwiggy Green-Route AI Radar")
st.markdown("**CTO Live Governor Simulation:** Testing platform stability under Multi-Cart load.")

# 3. SIDEBAR (INPUTS)
with st.sidebar:
    st.header("⚙️ Live Environment Variables")
    traffic_level = st.slider("Traffic Congestion (1=Low, 10=Gridlock)", min_value=1, max_value=10, value=5)
    sync_variance = st.slider("Kitchen Prep Variance (minutes)", min_value=0, max_value=45, value=15)
    active_riders = st.slider("Active Riders in Zone", min_value=10, max_value=200, value=100)

# 4. RECTIFIED CTO GOVERNOR LOGIC (The Engine)
# System Stress incorporates all 3 variables
base_stress = (traffic_level * 6) + (sync_variance * 1.5) - (active_riders * 0.15)
system_stress = max(0, min(100, base_stress))

# Dynamic ETA Math for ALL variables
rider_efficiency = active_riders * 0.05  # More riders = slightly faster delivery
base_time = 20

# Calculate exact ETAs dynamically
single_order_eta = int(base_time + (traffic_level * 1.5) - rider_efficiency)
unrestricted_eta = int(single_order_eta + sync_variance) # Takes the full penalty of out-of-sync kitchens
green_route_eta = int(single_order_eta + (sync_variance * 0.2)) # AI optimizes the route, drastically reducing the penalty

# Governor Threshold Logic
if system_stress > 80:
    route_status = "🚨 DISABLED (Red Zone)"
    status_color = "red"
    display_eta = "N/A (System Protected)"
    delta = "Overloaded"
else:
    route_status = "✅ ACTIVE (Green Route)"
    status_color = "green"
    display_eta = f"{green_route_eta} mins"
    delta = f"-{unrestricted_eta - green_route_eta} mins vs Unrestricted"

# 5. MAIN DASHBOARD (OUTPUTS)
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.metric(label="System Stress Score", value=f"{int(system_stress)}%", delta="Threshold: 80%")

with col2:
    with st.container(border=True):
        st.markdown(f"<h3 style='text-align: center; color: {status_color} !important;'>Multi-Cart Status</h3>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center; color: {status_color} !important;'>{route_status}</h2>", unsafe_allow_html=True)

with col3:
    with st.container(border=True):
        st.metric(label="Green-Route ETA", value=display_eta, delta=delta, delta_color="inverse")

st.write("---")

# 6. VISUALIZATION: Dynamic Chart
st.subheader("📊 Delivery Time Comparison (Simulated)")

# The chart now perfectly reflects all 3 slider inputs
data = pd.DataFrame({
    "Order Type": ["Single Order", "Unrestricted Multi-Cart", "Zwiggy Green-Route"],
    "Estimated Time (Mins)": [
        max(10, single_order_eta), 
        max(10, unrestricted_eta), 
        max(10, green_route_eta) if system_stress <= 80 else 0 
    ]
})

if system_stress <= 80:
    fig = px.bar(data, x="Order Type", y="Estimated Time (Mins)", text="Estimated Time (Mins)",
                 color="Order Type", color_discrete_sequence=["#B0BEC5", "#FF5252", "#4CAF50"])
    fig.update_traces(texttemplate='%{text} mins', textposition='outside')
    fig.update_layout(paper_bgcolor='white', plot_bgcolor='white', font=dict(color='black', size=14),
                      yaxis=dict(range=[0, max(data["Estimated Time (Mins)"]) + 15]))
    
    with st.container(border=True):
        st.plotly_chart(fig, use_container_width=True)
else:
    with st.container(border=True):
        st.error("📉 CHART UNAVAILABLE: The CTO Governor has disabled Multi-Cart in this zone to prevent SLA collapse. Add riders or reduce variance to lower stress below 80%.")