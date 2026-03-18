import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

# --- 1. SETTINGS & ELITE GEMINI THEME ---
st.set_page_config(page_title="Quantum Stratagem", layout="wide")

st.markdown("""
    <style>
    /* Ultra-Clean White Theme */
    .stApp { background-color: #ffffff; color: #1d1d1f; }
    
    /* Elegant Sidebar */
    section[data-testid="stSidebar"] { 
        background-color: #f5f5f7; 
        border-right: 1px solid #d2d2d7; 
    }
    
    /* Glassmorphism Verdict Box */
    .elite-verdict {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 102, 204, 0.2);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        border-left: 8px solid #0066cc;
        margin-bottom: 30px;
    }

    /* Metric Styling */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border-bottom: 3px solid #0066cc;
        padding: 20px;
        border-radius: 12px;
    }

    /* Primary Button */
    .stButton>button {
        background: linear-gradient(135deg, #0066cc 0%, #004494 100%);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 12px 30px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ELITE LOGIC: ANALYTICS ENGINE ---
def get_strategic_summary(product_name):
    summaries = [
        f"**Market Opportunity:** The {product_name} sector is currently undergoing a digital shift. By prioritizing high-reach features, we can capture 15% more market share in Q3.",
        f"**Risk Profile:** High. However, the {product_name} roadmap minimizes capital expenditure by front-loading high-confidence features.",
        f"**Executive Summary:** This {product_name} strategy balances aggressive Gen Z acquisition with robust risk mitigation frameworks."
    ]
    return random.choice(summaries)

def generate_elite_backlog(product_name):
    # Expanded list for a robust roadmap
    features = ["Gen Z Portal", "AI Stylist Engine", "Viral Loop Integration", 
                "Sustainability Ledger", "Global Logistics API", "Premium Membership", "Influencer Dashboard"]
    data = []
    for i, f in enumerate(features):
        data.append({
            "Feature": f"{f} - {product_name}",
            "Reach": random.randint(2000, 9000),
            "Impact": random.choice([1, 2, 3]),
            "Confidence": random.randint(60, 100),
            "Effort": random.randint(1, 5),
            "Business_Value": random.randint(5, 10),
            "Time_Criticality": random.randint(4, 9),
            "Risk_Reduction": random.randint(3, 8),
            "Start_Date": datetime.now().date() + timedelta(days=i*14)
        })
    return pd.DataFrame(data)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("💎 Stratagem")
    st.markdown("---")
    scoring_method = st.radio("Framework", ["RICE", "WSJF"])
    product_goal = st.text_input("Venture Goal", placeholder="e.g. Lady shoes for genz")
    trigger = st.button("Synthesize Strategy")

# --- 4. DATA PROCESSING ---
if 'backlog' not in st.session_state or trigger:
    name = product_goal if product_goal else "Venture Alpha"
    st.session_state.backlog = generate_elite_backlog(name)
    st.session_state.summary = get_strategic_summary(name)

df = st.session_state.backlog

# --- 5. CALCULATIONS ---
if scoring_method == "RICE":
    df['Score'] = (df['Reach'] * df['Impact'] * (df['Confidence']/100)) / df['Effort']
    chart_title = "Impact vs. Reach (RICE Growth)"
    color_scale = "Blues"
else:
    df['Score'] = (df['Business_Value'] + df['Time_Criticality'] + df['Risk_Reduction']) / df['Effort']
    chart_title = "Economic Priority (WSJF Economics)"
    color_scale = "Reds"

df = df.sort_values(by="Score", ascending=False)

# --- 6. ELITE UI OUTPUT ---
st.title("⚡ Quantum Stratagem")

# The Elite Verdict Box
st.markdown(f"""
    <div class="elite-verdict">
        <span style="text-transform: uppercase; letter-spacing: 2px; color: #0066cc; font-weight: bold;">Executive Intelligence Summary</span>
        <p style="font-size: 1.25em; margin-top: 10px; line-height: 1.6;">{st.session_state.summary}</p>
    </div>
    """, unsafe_allow_html=True)

# Key Performance Indicators
c1, c2, c3, c4 = st.columns(4)
c1.metric("Framework", scoring_method)
c2.metric("Backlog Depth", len(df))
c3.metric("Avg. Confidence", f"{int(df['Confidence'].mean())}%")
c4.metric("Strategy Fit", "Elite")

st.markdown("---")

# Data Interaction
st.subheader("📋 The Strategy Ledger")
edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")

# --- 7. INTELLIGENCE VISUALS ---
st.markdown(f"### 📈 {chart_title}")
col_left, col_right = st.columns(2)

with col_left:
    # Bar Chart shows the Final Score
    fig_bar = px.bar(edited_df, x="Score", y="Feature", orientation='h', 
                      color="Score", color_continuous_scale=color_scale, template="plotly_white")
    fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    # Scatter plot changes based on the framework
    if scoring_method == "RICE":
        fig_scatter = px.scatter(edited_df, x="Reach", y="Impact", size="Score", color="Score",
                                 color_continuous_scale="Blues", template="plotly_white", title="Reach vs Impact")
    else:
        fig_scatter = px.scatter(edited_df, x="Time_Criticality", y="Business_Value", size="Score", color="Score",
                                 color_continuous_scale="Reds", template="plotly_white", title="Criticality vs Value")
    
    fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_scatter, use_container_width=True)
