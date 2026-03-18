import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

# --- 1. SETTINGS & GEMINI-STYLE UI ---
st.set_page_config(page_title="Quantum Product Architect", layout="wide")

st.markdown("""
    <style>
    /* Gemini/Apple White Theme */
    .stApp { background-color: #f8f9fa; color: #1f1f1f; }
    
    /* Soft White Cards */
    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    
    /* Clean Sidebar */
    section[data-testid="stSidebar"] { background-color: white; border-right: 1px solid #e0e0e0; }
    
    /* Strategic Verdict Box */
    .verdict-box {
        background-color: #e8f0fe;
        border-left: 5px solid #1a73e8;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 25px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Custom Button */
    .stButton>button {
        background-color: #1a73e8;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 24px;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE BRAIN: AI VERDICT & FEATURE GENERATOR ---
def get_strategic_verdict(product_name):
    # Simulated AI analysis for the "Summary"
    analysis = [
        f"The market for **{product_name}** shows high 'Blue Ocean' potential. Focus on Gen Z aesthetic and sustainability.",
        f"**{product_name}** is a high-competition niche. Success depends on the 'Risk Reduction' features and rapid time-to-market.",
        f"Innovative approach. The RICE scores suggest the 'API Integration' should be deprioritized in favor of 'User Experience'."
    ]
    return random.choice(analysis)

def generate_full_backlog(product_name):
    # 7 Features to make the roadmap look professional
    features = [
        "Core MVP Design", "Social Integration", "AI Search Engine", 
        "Beta Group Launch", "Sustainability Tracker", "Influencer Portal", "Secure Payment Gateway"
    ]
    new_data = []
    for i, feature in enumerate(features):
        new_data.append({
            "Feature": f"{feature} - {product_name}",
            "Reach": random.randint(1000, 8000),
            "Impact": random.choice([1.0, 2.0, 3.0]),
            "Confidence": random.randint(70, 100),
            "Effort": random.randint(1, 5),
            "Business_Value": random.randint(4, 10),
            "Time_Criticality": random.randint(3, 9),
            "Risk_Reduction": random.randint(2, 8),
            "Start_Date": datetime.now().date() + timedelta(days=i*14)
        })
    return pd.DataFrame(new_data)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.image("https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d47353039331e16b92ad.svg", width=40)
    st.title("Architect")
    st.markdown("---")
    scoring_method = st.radio("Framework", ["RICE", "WSJF"])
    product_idea = st.text_input("Product Goal", placeholder="e.g. Lady shoes for genz")
    trigger = st.button("Generate Strategy")

# --- 4. DATA LOGIC ---
if 'backlog' not in st.session_state or trigger:
    name = product_idea if product_idea else "New Project"
    st.session_state.backlog = generate_full_backlog(name)
    st.session_state.verdict = get_strategic_verdict(name)

# --- 5. THE UI OUTPUT ---
st.title("✨ Quantum Product Architect")

# Strategic Verdict (The Summary Box)
st.markdown(f"""
    <div class="verdict-box">
        <h4 style="margin-top:0; color:#1a73e8;">Strategic AI Verdict</h4>
        <p style="font-size:1.1em;">{st.session_state.verdict}</p>
    </div>
    """, unsafe_allow_html=True)

# Metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("Method", scoring_method)
m2.metric("Total Features", len(st.session_state.backlog))
m3.metric("Project Health", "Optimal")
m4.metric("Market Fit", "88%")

st.markdown("---")

# Data Table
st.subheader("📋 Executive Backlog")
edited_df = st.data_editor(st.session_state.backlog, use_container_width=True, num_rows="dynamic")

# Math
if scoring_method == "RICE":
    edited_df['Score'] = (edited_df['Reach'] * edited_df['Impact'] * (edited_df['Confidence']/100)) / edited_df['Effort']
else:
    edited_df['Score'] = (edited_df['Business_Value'] + edited_df['Time_Criticality'] + edited_df['Risk_Reduction']) / edited_df['Effort']

edited_df = edited_df.sort_values(by="Score", ascending=False)

# --- 6. CHARTS ---
st.markdown("### 📊 Market & Delivery Intelligence")
c1, c2 = st.columns(2)

with c1:
    fig_bar = px.bar(edited_df, x="Score", y="Feature", orientation='h', 
                      color="Score", color_continuous_scale="Blues", template="plotly_white")
    fig_bar.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    # Gantt Roadmap
    roadmap_list = []
    for _, row in edited_df.iterrows():
        end = row['Start_Date'] + timedelta(days=int(row['Effort'] * 25))
        roadmap_list.append(dict(Task=row['Feature'], Start=row['Start_Date'], Finish=end, Score=row['Score']))
    
    df_roadmap = pd.DataFrame(roadmap_list)
    fig_gantt = px.timeline(df_roadmap, x_start="Start", x_end="Finish", y="Task", color="Score",
                             color_continuous_scale="Blues", template="plotly_white")
    fig_gantt.update_yaxes(autorange="reversed")
    fig_gantt.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_gantt, use_container_width=True)
