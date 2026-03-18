import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

# --- 1. SETTINGS & ELITE GEMINI THEME ---
st.set_page_config(page_title="Quantum Stratagem", layout="wide")

st.markdown("""
    <style>
    /* Clean White Aesthetic */
    .stApp { background-color: #ffffff; color: #1d1d1f; }
    
    /* Soft Sidebar */
    section[data-testid="stSidebar"] { 
        background-color: #f5f5f7; 
        border-right: 1px solid #d2d2d7; 
    }
    
    /* Elite Verdict Card */
    .elite-verdict {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 102, 204, 0.1);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.05);
        border-left: 8px solid #1a73e8;
        margin-bottom: 30px;
    }

    /* Metric Styling */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border-bottom: 3px solid #1a73e8;
        padding: 20px;
        border-radius: 12px;
    }

    /* Blue Action Button */
    .stButton>button {
        background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 100%);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 12px 30px;
        font-weight: 600;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC: STRATEGY & FEATURE SYNTHESIS ---
def get_strategic_summary(product_name):
    summaries = [
        f"**Market Opportunity:** The {product_name} sector is currently experiencing a digital-first shift. Strategic focus on Gen-Z engagement is advised.",
        f"**Risk Profile:** Low to Moderate. This {product_name} roadmap prioritizes 'Risk Reduction' features to protect capital expenditure.",
        f"**Executive Summary:** Data indicates that {product_name} requires a focus on high-reach 'Viral Loops' to lower customer acquisition costs."
    ]
    return random.choice(summaries)

def generate_elite_backlog(product_name):
    p_lower = product_name.lower()
    # Industry-specific logic
    if "shoe" in p_lower:
        features = ["AR Try-on Mirror", "Drop Shipping API", "Limited Edition Raffle", "Eco-Sole Tracker", "Influencer Box", "3D Foot Scan", "Resale Marketplace"]
    elif "coffee" in p_lower:
        features = ["Mobile Order Ahead", "Subscription Beans", "Roast Profile AI", "Loyalty Wallet", "Local Roaster Map", "Smart Cup Integration", "Barista Training Hub"]
    elif "chair" in p_lower or "corporate" in p_lower:
        features = ["Ergonomic Sensor API", "B2B Bulk Portal", "Lumber Support AI", "Sustainability Cert", "Office Layout Tool", "Bulk Logistics Sync", "Warranty Dashboard"]
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

# --- 3. SESSION STATE ---
if 'backlog' not in st.session_state:
    st.session_state.backlog = generate_elite_backlog("Initial Venture")
    st.session_state.summary = "Submit a Product Goal to begin Strategic Synthesis."
    st.session_state.count = 0

# --- 4. SIDEBAR: THE AKASH BRAND ---
with st.sidebar:
    st.title("💎 Stratagem")
    
    st.markdown("""
        <div style="background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; margin-bottom: 20px;">
            <p style="margin: 0; font-size: 0.85em; color: #5f6368; font-weight: 600; text-transform: uppercase;">Lead Architect</p>
            <p style="margin: 0; font-size: 1.25em; font-weight: 700; color: #1d1d1f;">Akash</p>
            <p style="margin: 0; font-size: 0.85em; color: #1a73e8; font-weight: 500;">AI Product Strategist</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="font-size: 0.85em; color: #3c4043; line-height: 1.5; margin-bottom: 20px;">
        <b>About Stratagem:</b><br>
        A decision-intelligence engine designed to transform product ideas into data-backed roadmaps using RICE and WSJF frameworks.
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    scoring_method = st.radio("Framework Intelligence", ["RICE", "WSJF"], help="RICE = Consumer Growth | WSJF = Economic Priority")
    product_goal = st.text_input("Venture Goal", placeholder="e.g. Lady shoes for genz")
    
    if st.button("Synthesize Strategy"):
        name = product_goal if product_goal else "Venture Alpha"
        st.session_state.backlog = generate_elite_backlog(name)
        st.session_state.summary = get_strategic_summary(name)
        st.session_state.count += 1
        st.rerun()

# --- 5. CALCULATIONS ---
df = st.session_state.backlog.copy()

if scoring_method == "RICE":
    df['Score'] = (df['Reach'] * df['Impact'] * (df['Confidence']/100)) / df['Effort']
    color_scale = "Blues"
    y_axis, x_axis = "Impact", "Reach"
else:
    df['Score'] = (df['Business_Value'] + df['Time_Criticality'] + df['Risk_Reduction']) / df['Effort']
    color_scale = "Reds"
    y_axis, x_axis = "Business_Value", "Time_Criticality"

df = df.sort_values(by="Score", ascending=False)

# --- 6. MAIN DISPLAY ---
st.title("⚡ Quantum Stratagem")

st.markdown(f"""
    <div class="elite-verdict">
        <span style="letter-spacing: 2px; color: #1a73e8; font-weight: bold; text-transform: uppercase; font-size: 0.8em;">Executive Intelligence Summary</span>
        <p style="font-size: 1.25em; margin-top: 10px; line-height: 1.5;">{st.session_state.summary}</p>
    </div>
    """, unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Framework", scoring_method)
c2.metric("Backlog Items", len(df))
c3.metric("System Health", "Optimal")
c4.metric("Strategy Fit", "Elite")

st.markdown("---")

st.subheader("📋 The Strategy Ledger")
# Key refresh logic to wipe the table when clicking 'Synthesize'
edited_df = st.data_editor(df, use_container_width=True, key=f"ledger_{st.session_state.count}")

st.markdown("---")

# --- 7. CHARTS ---
st.markdown(f"### 📈 {scoring_method} Analysis")
left, right = st.columns(2)

with left:
    fig_bar = px.bar(edited_df, x="Score", y="Feature", orientation='h', 
                      color="Score", color_continuous_scale=color_scale, template="plotly_white")
    st.plotly_chart(fig_bar, use_container_width=True)

with right:
    fig_scatter = px.scatter(edited_df, x=x_axis, y=y_axis, size="Score", color="Score",
                             color_continuous_scale=color_scale, template="plotly_white",
                             title=f"Bubble Size = {scoring_method} Priority Score")
    st.plotly_chart(fig_scatter, use_container_width=True)
