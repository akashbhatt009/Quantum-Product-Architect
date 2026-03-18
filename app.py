import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# --- 1. SETTINGS & CUSTOM STYLES ---
st.set_page_config(page_title="Quantum Product Architect", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #58a6ff; color: white; border: none; }
    .stButton>button:hover { background-color: #1f6feb; border: none; }
    .metric-card { background-color: #161b22; border: 1px solid #30363d; padding: 20px; border_radius: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. AI STRATEGY ENGINE (Simulated Reasoning) ---
def generate_ai_backlog(product_name):
    """Simulates an AI generating features based on a product name."""
    generic_features = [
        "User Onboarding Flow", "Analytics Dashboard", "API Integration", 
        "Mobile App Version", "Subscription Tier", "AI Chatbot Support",
        "Social Sharing", "Data Encryption", "Cloud Sync", "Multi-language Support"
    ]
    selected = random.sample(generic_features, 5)
    
    new_data = []
    for i, feature in enumerate(selected):
        new_data.append({
            "Feature": f"{feature} for {product_name}",
            "Reach": random.randint(500, 5000),
            "Impact": random.choice([0.5, 1.0, 2.0, 3.0]),
            "Confidence": random.randint(50, 100),
            "Effort": random.randint(1, 6),
            "Start_Date": datetime.now().date() + timedelta(days=i*15)
        })
    return pd.DataFrame(new_data)

# --- 3. SIDEBAR & INPUT ---
with st.sidebar:
    st.title("⚙️ Strategy Settings")
    st.markdown("---")
    user_idea = st.text_input("Product Vision", placeholder="e.g. AI Coffee Roaster")
    generate_btn = st.button("Generate AI Strategy")
    st.markdown("---")
    st.write("Current Framework: **RICE Scoring**")
    st.write("Roadmap Horizon: **3 Months**")

# --- 4. DATA INITIALIZATION ---
if 'backlog' not in st.session_state or generate_btn:
    if generate_btn and user_idea:
        st.session_state.backlog = generate_ai_backlog(user_idea)
    elif 'backlog' not in st.session_state:
        # Default starter data
        st.session_state.backlog = pd.DataFrame([
            {"Feature": "Core MVP Dashboard", "Reach": 2000, "Impact": 3.0, "Confidence": 100, "Effort": 2, "Start_Date": datetime.now().date()},
            {"Feature": "Beta Testing Group", "Reach": 500, "Impact": 2.0, "Confidence": 80, "Effort": 1, "Start_Date": datetime.now().date() + timedelta(days=10)},
        ])

# --- 5. MAIN INTERFACE ---
st.title("⚡ Quantum Product Architect")
st.markdown("### Autonomous Product Discovery & Prioritization")

# Metrics row
cols = st.columns(4)
total_reach = st.session_state.backlog['Reach'].sum()
avg_effort = st.session_state.backlog['Effort'].mean()

cols[0].metric("Total Reach", f"{total_reach:,}")
cols[1].metric("Avg. Effort", f"{avg_effort:.1f} mo")
cols[2].metric("Strategy Phase", "Discovery")
cols[3].metric("Model Status", "Active")

st.markdown("---")

# Editable Data Table
st.subheader("📋 Dynamic Strategy Backlog")
edited_df = st.data_editor(
    st.session_state.backlog,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Confidence": st.column_config.NumberColumn("Confidence %", format="%d%%"),
        "Impact": st.column_config.SelectboxColumn("Impact Score", options=[0.5, 1.0, 2.0, 3.0])
    }
)

# RICE Calculation
edited_df['RICE_Score'] = (edited_df['Reach'] * edited_df['Impact'] * (edited_df['Confidence']/100)) / edited_df['Effort']
edited_df = edited_df.sort_values(by="RICE_Score", ascending=False)

# --- 6. VISUALIZATIONS ---
tab1, tab2 = st.tabs(["📊 Strategic Analysis", "📅 Delivery Roadmap"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        fig_rice = px.bar(edited_df, x="RICE_Score", y="Feature", orientation='h', 
                          title="RICE Priority Ranking", color="RICE_Score", template="plotly_dark")
        st.plotly_chart(fig_rice, use_container_width=True)
    with c2:
        fig_bubble = px.scatter(edited_df, x="Effort", y="Impact", size="Reach", color="RICE_Score",
                                hover_name="Feature", title="Impact vs. Effort Matrix", template="plotly_dark")
        st.plotly_chart(fig_bubble, use_container_width=True)

with tab2:
    # Build Roadmap data
    roadmap_list = []
    for _, row in edited_df.iterrows():
        end = row['Start_Date'] + timedelta(days=int(row['Effort'] * 30))
        roadmap_list.append(dict(Task=row['Feature'], Start=row['Start_Date'], Finish=end, Priority=row['RICE_Score']))
    
    df_roadmap = pd.DataFrame(roadmap_list)
    fig_gantt = px.timeline(df_roadmap, x_start="Start", x_end="Finish", y="Task", color="Priority",
                             title="Automated Release Timeline", template="plotly_dark")
    fig_gantt.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_gantt, use_container_width=True)

st.markdown("---")
st.caption("Quantum Product Architect | Framework-driven decision support for Product Owners.")
