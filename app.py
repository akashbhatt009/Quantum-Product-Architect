import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

# --- 1. CONFIG & THEME ---
st.set_page_config(page_title="Quantum Product Architect", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #161b22; border-radius: 10px; padding: 15px; border: 1px solid #30363d; }
    h1, h2, h3 { color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BRAIN: SCORING LOGIC ---
def calculate_scores(df, method):
    if method == "RICE":
        # RICE = (Reach * Impact * Confidence) / Effort
        return (df['Reach'] * df['Impact'] * (df['Confidence']/100)) / df['Effort']
    else:
        # WSJF = (Business Value + Time Criticality + Risk Reduction) / Effort (Job Size)
        return (df['Business_Value'] + df['Time_Criticality'] + df['Risk_Reduction']) / df['Effort']

# --- 3. SIDEBAR & CONTROLS ---
with st.sidebar:
    st.title("⚙️ Strategy Control")
    scoring_method = st.radio("Prioritization Framework", ["RICE", "WSJF"], help="RICE is for growth; WSJF is for Business Economics.")
    st.markdown("---")
    user_idea = st.text_input("New Product Goal", placeholder="e.g. Fintech App for Gen Z")
    generate_btn = st.button("AI Discovery")

# --- 4. DATA INITIALIZATION ---
if 'backlog' not in st.session_state or generate_btn:
    # Creating a dynamic starting point
    base_name = user_idea if user_idea else "Core Project"
    st.session_state.backlog = pd.DataFrame([
        {"Feature": f"Alpha Release - {base_name}", "Reach": 2000, "Impact": 3.0, "Confidence": 100, "Effort": 3, 
         "Business_Value": 8, "Time_Criticality": 9, "Risk_Reduction": 5, "Start_Date": datetime.now().date()},
        {"Feature": "API Integration Layer", "Reach": 500, "Impact": 2.0, "Confidence": 80, "Effort": 2, 
         "Business_Value": 5, "Time_Criticality": 3, "Risk_Reduction": 7, "Start_Date": datetime.now().date() + timedelta(days=15)},
    ])

# --- 5. INTERFACE ---
st.title("⚡ Quantum Product Architect")
st.caption(f"Currently active framework: **{scoring_method}**")

# Metrics
m1, m2, m3 = st.columns(3)
m1.metric("Method", scoring_method)
m2.metric("Total Tasks", len(st.session_state.backlog))
m3.metric("Status", "Strategy Optimized")

# Data Editor
st.subheader("📋 Interactive Strategy Ledger")
edited_df = st.data_editor(st.session_state.backlog, use_container_width=True, num_rows="dynamic")

# Calculate & Sort
edited_df['Score'] = calculate_scores(edited_df, scoring_method)
edited_df = edited_df.sort_values(by="Score", ascending=False)

# --- 6. VISUALS ---
tab1, tab2 = st.tabs(["📊 Priority Analysis", "📅 Release Roadmap"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        fig_bar = px.bar(edited_df, x="Score", y="Feature", orientation='h', color="Score", 
                          title=f"{scoring_method} Ranking", template="plotly_dark")
        st.plotly_chart(fig_bar, use_container_width=True)
    with c2:
        # Business Analyst Matrix
        x_axis = "Effort"
        y_axis = "Impact" if scoring_method == "RICE" else "Business_Value"
        fig_scatter = px.scatter(edited_df, x=x_axis, y=y_axis, size="Score", color="Score",
                                 hover_name="Feature", title="Priority Matrix", template="plotly_dark")
        st.plotly_chart(fig_scatter, use_container_width=True)

with tab2:
    roadmap_data = []
    for _, row in edited_df.iterrows():
        end = row['Start_Date'] + timedelta(days=int(row['Effort'] * 30))
        roadmap_data.append(dict(Task=row['Feature'], Start=row['Start_Date'], Finish=end, Score=row['Score']))
    
    df_roadmap = pd.DataFrame(roadmap_data)
    fig_gantt = px.timeline(df_roadmap, x_start="Start", x_end="Finish", y="Task", color="Score",
                             title="Gantt Release Schedule", template="plotly_dark")
    fig_gantt.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_gantt, use_container_width=True)
