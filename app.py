import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

# --- 1. SETTINGS & ELITE APPLE/GEMINI THEME ---
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
        border: 1px solid rgba(0, 102, 204, 0.1);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.05);
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

    /* Primary Button - Blue Gradient */
    .stButton>button {
        background: linear-gradient(135deg, #0066cc 0%, #004494 100%);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 12px 30px;
        font-weight: 600;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE BRAIN: STRATEGY ENGINE ---
def get_strategic_summary(product_name):
    summaries = [
        f"**Market Opportunity:** The {product_name} sector is shifting. Data suggests a 22% gap in Gen-Z tailored solutions.",
        f"**Risk Profile:** Moderate. The {product_name} roadmap focuses on low-CAPEX testing to validate market fit.",
        f"**Executive Summary:** This {product_name} strategy utilizes high-impact 'Viral Loops' to reduce customer acquisition costs."
    ]
    return random.choice(summaries)

def generate_elite_backlog(product_name):
    # Industry-specific feature intelligence
    p_lower = product_name.lower()
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

# --- 3. SIDEBAR: IDENTITY & CONTROL ---
if 'backlog' not in st.session_state:
    st.session_state.backlog = generate_elite_backlog("Venture Alpha")
    st.session_state.summary = "Awaiting Venture Input for Analysis..."
    st.session_state.count = 0

with st.sidebar:
    st.title("💎 Stratagem")
    
    # Professional Bio Card
    st.markdown("""
        <div style="background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; margin-bottom: 20px;">
            <p style="margin: 0; font-size: 0.85em; color: #5f6368; font-weight: 600; text-transform: uppercase;">Lead Architect</p>
            <p style="margin: 0; font-size: 1.1em; font-weight: 700; color: #1d1d1f;">[Your Name]</p>
            <p style="margin: 0; font-size: 0.8em; color: #5f6368;">AI Product Strategist</p>
        </div>
    """, unsafe_allow_html=True)

    scoring_method = st.radio("Framework Intelligence", ["RICE", "WSJF"], help="RICE = Consumer Growth | WSJF = Business Economics")
    product_goal = st.text_input("Venture Goal", placeholder="e.g. Lady shoes for genz")
    
    if st.button("Synthesize Strategy"):
        name = product_goal if product_goal else "Venture Alpha"
        st.session_state.backlog = generate_elite_backlog(name)
        st.session_state.summary = get_strategic_summary(name)
        st.session_state.count += 1
        st.rerun()
    
    st.markdown("---")
    st.markdown("""<p style='font-size: 0.75em; color: #8e8e93;'><b>Tech Stack:</b> Python 3.11, Streamlit, Plotly Analytics, RICE/WSJF Logic</p>""", unsafe_allow_html=True)

# --- 4. CALCULATIONS ---
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

# --- 5. UI MAIN OUTPUT ---
st.title("⚡ Quantum Stratagem")

# The Elite Summary Card
st.markdown(f"""
    <div class="elite-verdict">
        <span style="letter-spacing: 2px; color: #0066cc; font-weight: bold; text-transform: uppercase;">Executive Intelligence Summary</span>
        <p style="font-size: 1.25em; margin-top: 10px; line-height: 1.6;">{st.session_state.summary}</p>
    </div>
    """, unsafe_allow_html=True)

# KPIs
c1, c2, c3, c4 = st.columns(4)
c1.metric("Framework", scoring_method)
c2.metric("Backlog Depth", len(df))
c3.metric("Avg. Confidence", f"{int(df['Confidence'].mean())}%")
c4.metric("Strategy Fit", "Elite")

st.markdown("---")

# The Interactive Ledger (Wipes on re-synthesis due to key change)
st.subheader("📋 The Strategy Ledger")
edited_df = st.data_editor(df, use_container_width=True, key=f"editor_{st.session_state.count}")

# --- 6. INTELLIGENCE VISUALS ---
st.markdown(f"### 📈 {scoring_method} Priority Intelligence")
col_left, col_right = st.columns(2)

with col_left:
    fig_bar = px.bar(edited_df, x="Score", y="Feature", orientation='h', 
                      color="Score", color_continuous_scale=color_scale, template="plotly_white")
    fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    # Improved Bubble Chart - Priority Score dictates bubble size
    fig_scatter = px.scatter(edited_df, x=x_axis, y=y_axis, size="Score", color="Score",
                             color_continuous_scale=color_scale, template="plotly_white",
                             title=f"Bubble Size = {scoring_method} Priority Score")
    fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_scatter, use_container_width=True)
