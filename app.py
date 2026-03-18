import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

# --- 1. SETTINGS & ELITE GEMINI THEME ---
st.set_page_config(page_title="Quantum Stratagem", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1d1d1f; }
    section[data-testid="stSidebar"] { background-color: #f5f5f7; border-right: 1px solid #d2d2d7; }
    .elite-verdict {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 102, 204, 0.1);
        padding: 30px; border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.05);
        border-left: 8px solid #0066cc; margin-bottom: 30px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #0066cc 0%, #004494 100%);
        color: white; border-radius: 12px; border: none; padding: 12px 30px; font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE BRAIN: AI VERDICT & FEATURE GENERATOR ---
def get_strategic_summary(product_name):
    summaries = [
        f"**Market Opportunity:** The {product_name} sector is shifting. Data suggests a 22% gap in Gen-Z tailored solutions.",
        f"**Risk Profile:** Moderate. The {product_name} roadmap focuses on low-CAPEX testing to validate market fit.",
        f"**Executive Summary:** This {product_name} strategy utilizes high-impact 'Viral Loops' to reduce customer acquisition costs."
    ]
    return random.choice(summaries)

def generate_elite_backlog(product_name):
    # Industry-specific feature logic
    if "shoe" in product_name.lower():
        features = ["AR Try-on Mirror", "Drop Shipping API", "Limited Edition Raffle", "Eco-Sole Tracker", "Influencer Box", "3D Foot Scan", "Resale Marketplace"]
    elif "coffee" in product_name.lower():
        features = ["Mobile Order Ahead", "Subscription Beans", "Roast Profile AI", "Loyalty Wallet", "Local Roaster Map", "Smart Cup Integration", "Barista Training Hub"]
    else:
        features = ["MVP Core Dashboard", "User Analytics", "Payment Gateway", "Mobile Optimization", "Cloud Sync", "Security Patch", "Beta Feedback Loop"]
    
    data = []
    for i, f in enumerate(features):
        data.append({
            "Feature": f"{f} ({product_name})",
            "Reach": random.randint(2000, 9500),
            "Impact": random.choice([1.0, 2.0, 3.0]),
            "Confidence": random.randint(70, 100),
            "Effort": random.randint(1, 5),
            "Business_Value": random.randint(5, 10),
            "Time_Criticality": random.randint(4, 10),
            "Risk_Reduction": random.randint(3, 8),
            "Start_Date": datetime.now().date() + timedelta(days=i*14)
        })
    return pd.DataFrame(data)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("💎 Stratagem")
    scoring_method = st.radio("Framework", ["RICE", "WSJF"])
    product_goal = st.text_input("Venture Goal", placeholder="e.g. Lady shoes for genz")
    if st.button("Synthesize Strategy"):
        name = product_goal if product_goal else "Venture Alpha"
        # FORCE REFRESH: This clears the old data and ledger
        st.session_state.backlog = generate_elite_backlog(name)
        st.session_state.summary = get_strategic_summary(name)
        st.session_state.count = random.randint(1, 10000) # Unique key for table
        st.rerun()

# Initialize session state if empty
if 'backlog' not in st.session_state:
    st.session_state.backlog = generate_elite_backlog("Initial Project")
    st.session_state.summary = "Awaiting Venture Input for Analysis..."
    st.session_state.count = 0

df = st.session_state.backlog.copy()

# --- 4. CALCULATIONS ---
if scoring_method == "RICE":
    df['Score'] = (df['Reach'] * df['Impact'] * (df['Confidence']/100)) / df['Effort']
    color_scale = "Blues"
    y_axis = "Impact"
    x_axis = "Reach"
else:
    df['Score'] = (df['Business_Value'] + df['Time_Criticality'] + df['Risk_Reduction']) / df['Effort']
    color_scale = "Reds"
    y_axis = "Business_Value"
    x_axis = "Time_Criticality"

df = df.sort_values(by="Score", ascending=False)

# --- 5. UI OUTPUT ---
st.title("⚡ Quantum Stratagem")

st.markdown(f"""<div class="elite-verdict">
    <span style="letter-spacing: 2px; color: #0066cc; font-weight: bold;">EXECUTIVE INTELLIGENCE SUMMARY</span>
    <p style="font-size: 1.2em; margin-top: 10px;">{st.session_state.summary}</p>
    </div>""", unsafe_allow_html=True)

st.subheader("📋 The Strategy Ledger")
# The 'key' ensures the table refreshes when you click the button
edited_df = st.data_editor(df, use_container_width=True, key=f"editor_{st.session_state.count}")

st.markdown("---")

# --- 6. IMPROVED BUBBLE CHART ---
st.markdown(f"### 📈 {scoring_method} Priority Intelligence")
col_l, col_r = st.columns(2)

with col_l:
    fig_bar = px.bar(edited_df, x="Score", y="Feature", orientation='h', color="Score", color_continuous_scale=color_scale, template="plotly_white")
    st.plotly_chart(fig_bar, use_container_width=True)

with col_r:
    # Scatter plot with size=Score to make them pop!
    fig_scatter = px.scatter(edited_df, x=x_axis, y=y_axis, size="Score", color="Score",
                             color_continuous_scale=color_scale, template="plotly_white",
                             title=f"{x_axis} vs {y_axis} (Bubble size = Priority Score)")
    st.plotly_chart(fig_scatter, use_container_width=True)
