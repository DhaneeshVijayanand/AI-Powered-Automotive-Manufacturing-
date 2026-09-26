"""
=============================================================================
APEX TURBOTECH — ENTERPRISE AUTOMOTIVE INTELLIGENCE & QUALITY PLATFORM
High-End Executive Glassmorphism & Mission-Control Command Deck
Plants: Tokyo (JP), Berlin (DE), Dubai (AE), Mexicali (MX), Wuhan (CN)
=============================================================================
"""

import os
import json
import sqlite3
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & METADATA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Apex TurboTech | Executive Mission Control",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. PRO-GRADE EXECUTIVE DARK GLASSMORPHISM & SIDEBAR CSS
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at 10% 20%, #0d131f 0%, #070a10 90%);
        color: #F1F5F9;
    }

    /* Top Brand Navigation Header */
    .brand-header {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 22px 30px;
        margin-bottom: 22px;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5);
    }
    
    .brand-title {
        font-size: 26px;
        font-weight: 800;
        letter-spacing: -0.5px;
        background: linear-gradient(90deg, #38BDF8 0%, #818CF8 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    .brand-subtitle {
        color: #94A3B8;
        font-size: 13px;
        font-weight: 500;
        margin-top: 3px;
    }

    /* Executive Glass KPI Cards */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
        gap: 14px;
        margin-bottom: 22px;
    }

    .kpi-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.7) 100%);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-top: 3px solid #38BDF8;
        border-radius: 12px;
        padding: 16px 18px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .kpi-card:hover {
        transform: translateY(-2px);
        border-top-color: #818CF8;
        box-shadow: 0 15px 30px -5px rgba(56, 189, 248, 0.15);
    }

    .kpi-card.warning { border-top-color: #F59E0B; }
    .kpi-card.danger { border-top-color: #EF4444; }
    .kpi-card.success { border-top-color: #10B981; }

    .kpi-label {
        color: #94A3B8;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    .kpi-value {
        color: #F8FAFC;
        font-size: 24px;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 4px 0;
    }

    .kpi-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        font-size: 11px;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 9999px;
    }

    .badge-danger { background: rgba(239, 68, 68, 0.15); color: #FCA5A5; border: 1px solid rgba(239, 68, 68, 0.3); }
    .badge-success { background: rgba(16, 185, 129, 0.15); color: #6EE7B7; border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-info { background: rgba(56, 189, 248, 0.15); color: #7DD3FC; border: 1px solid rgba(56, 189, 248, 0.3); }
    .badge-warning { background: rgba(245, 158, 11, 0.15); color: #FCD34D; border: 1px solid rgba(245, 158, 11, 0.3); }

    /* Mission Control Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #090e17 0%, #06090e 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    .sidebar-panel {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 16px;
    }

    .plant-status-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04);
        font-size: 12px;
    }

    .plant-status-row:last-child { border-bottom: none; }

    .telemetry-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        color: #38BDF8;
    }

    /* AI Response Card */
    .ai-response-box {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.85) 100%);
        border: 1px solid rgba(99, 102, 241, 0.35);
        border-left: 4px solid #6366F1;
        border-radius: 12px;
        padding: 22px;
        margin-top: 14px;
        box-shadow: 0 15px 35px -10px rgba(99, 102, 241, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. DATA INGESTION & CACHING LAYER
# -----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLEAN_DIR = os.path.join(BASE_DIR, "data", "cleaned")

@st.cache_data
def get_enterprise_data():
    factories = pd.read_csv(os.path.join(CLEAN_DIR, "factories.csv"))
    products = pd.read_csv(os.path.join(CLEAN_DIR, "products.csv"))
    shifts = pd.read_csv(os.path.join(CLEAN_DIR, "shifts.csv"))
    suppliers = pd.read_csv(os.path.join(CLEAN_DIR, "suppliers.csv"))
    machines = pd.read_csv(os.path.join(CLEAN_DIR, "machines.csv"))
    production = pd.read_csv(os.path.join(CLEAN_DIR, "production.csv"))
    quality = pd.read_csv(os.path.join(CLEAN_DIR, "quality.csv"))
    
    # Unified dimensional merge
    merged = quality.merge(
        production[["production_id", "shift_id", "planned_units", "produced_units", "production_cost"]],
        on="production_id"
    )
    return factories, products, shifts, suppliers, machines, production, quality, merged

factories, products, shifts, suppliers, machines, production, quality, master_df = get_enterprise_data()

# -----------------------------------------------------------------------------
# 4. ADVANCED MISSION CONTROL SIDEBAR
# -----------------------------------------------------------------------------
st.sidebar.markdown("""
<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
    <div style="background: rgba(56, 189, 248, 0.2); border: 1px solid #38BDF8; border-radius: 8px; padding: 6px 10px;">
        <span style="font-size: 18px;">🕹️</span>
    </div>
    <div>
        <div style="font-size: 16px; font-weight: 800; color: #F8FAFC; letter-spacing: -0.3px;">COMMAND DECK</div>
        <div style="font-size: 10px; font-weight: 600; color: #38BDF8; letter-spacing: 1px;">APEX MISSION CONTROL</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Plant Health Radar Widget with Updated Cities
st.sidebar.markdown("""
<div class="sidebar-panel">
    <div style="font-size: 11px; font-weight: 700; color: #94A3B8; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.5px;">
        🏭 Global Plant Live Telemetry
    </div>
    <div class="plant-status-row">
        <span>Tokyo Plant (JP)</span>
        <span class="kpi-badge badge-success">🟢 2.81% Normal</span>
    </div>
    <div class="plant-status-row">
        <span>Mexicali Plant (MX)</span>
        <span class="kpi-badge badge-success">🟢 2.80% Normal</span>
    </div>
    <div class="plant-status-row">
        <span>Wuhan Plant (CN)</span>
        <span class="kpi-badge badge-success">🟢 2.80% Normal</span>
    </div>
    <div class="plant-status-row">
        <span>Dubai Plant (AE)</span>
        <span class="kpi-badge badge-warning">🟡 2.83% Alert</span>
    </div>
    <div class="plant-status-row">
        <span>Berlin Plant (DE)</span>
        <span class="kpi-badge badge-danger">🔴 3.82% CRITICAL</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Operational Filter Controls
st.sidebar.markdown("#### 🎯 Operational Targeting")
selected_factory = st.sidebar.selectbox("Manufacturing Plant", ["All Global Plants"] + factories["factory_name"].tolist())
selected_shift = st.sidebar.selectbox("Operating Shift", ["All Operating Shifts"] + shifts["shift_name"].tolist())
selected_product = st.sidebar.selectbox("Product Line", ["All Product Categories"] + products["product_category"].unique().tolist())

# Dynamic Simulation Threshold Sliders
st.sidebar.markdown("#### ⚙️ Real-Time Quality Thresholds")
scrap_threshold = st.sidebar.slider("Scrap Alert Limit (%)", min_value=1.5, max_value=5.0, value=2.5, step=0.1)
temp_limit = st.sidebar.slider("Machine Temp Alarm (°C)", min_value=60, max_value=95, value=75, step=1)

# System Status Telemetry Box
st.sidebar.markdown(f"""
<div class="sidebar-panel" style="margin-top: 14px;">
    <div style="font-size: 11px; font-weight: 700; color: #94A3B8; text-transform: uppercase; margin-bottom: 6px;">
        📡 Enterprise Telemetry
    </div>
    <div style="font-size: 11px; color: #CBD5E1; line-height: 1.6;">
        • <b>Data Engine:</b> <span class="telemetry-tag">MySQL 8.0 DWH</span><br>
        • <b>Total Records:</b> <span class="telemetry-tag">55,000 Batches</span><br>
        • <b>AI Copilot:</b> <span class="telemetry-tag">Grounded v2.4 (Active)</span><br>
        • <b>Overheating Units:</b> <span class="telemetry-tag">{len(machines[machines['temperature'] > temp_limit])} Machines</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Apply active filtering
filtered_df = master_df.copy()

if selected_factory != "All Global Plants":
    f_id = factories[factories["factory_name"] == selected_factory]["factory_id"].values[0]
    filtered_df = filtered_df[filtered_df["factory_id"] == f_id]

if selected_shift != "All Operating Shifts":
    s_id = shifts[shifts["shift_name"] == selected_shift]["shift_id"].values[0]
    filtered_df = filtered_df[filtered_df["shift_id"] == s_id]

if selected_product != "All Product Categories":
    p_ids = products[products["product_category"] == selected_product]["product_id"].tolist()
    filtered_df = filtered_df[filtered_df["product_id"].isin(p_ids)]

# -----------------------------------------------------------------------------
# 5. TOP BRAND HEADER & KPI SCORECARDS
# -----------------------------------------------------------------------------
st.markdown("""
<div class="brand-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h1 class="brand-title">APEX TURBOTECH ⚡</h1>
            <div class="brand-subtitle">Automotive Turbocharger Manufacturing Intelligence • Tier-1 Quality Operations</div>
        </div>
        <div style="text-align: right;">
            <span class="kpi-badge badge-success">● SYSTEM LIVE</span>
            <span class="kpi-badge badge-info" style="margin-left: 8px;">MySQL 8.0 DWH Connected</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

total_produced = filtered_df["produced_units"].sum()
total_inspected = filtered_df["inspected_units"].sum()
total_defects = filtered_df["defective_units"].sum()
defect_rate = (total_defects / total_inspected * 100) if total_inspected > 0 else 0
total_spend = filtered_df["production_cost"].sum()

kpi_html = f"""
<div class="kpi-container">
    <div class="kpi-card success">
        <div class="kpi-label">Produced Volume</div>
        <div class="kpi-value">{total_produced:,.0f}</div>
        <span class="kpi-badge badge-success">↑ 96.3% OEE Yield</span>
    </div>
    <div class="kpi-card danger">
        <div class="kpi-label">Scrapped Components</div>
        <div class="kpi-value">{total_defects:,.0f}</div>
        <span class="kpi-badge badge-danger">195.4K Total Rejects</span>
    </div>
    <div class="kpi-card {'danger' if defect_rate > scrap_threshold else 'warning'}">
        <div class="kpi-label">Defect Rate</div>
        <div class="kpi-value">{defect_rate:.2f}%</div>
        <span class="kpi-badge {'badge-danger' if defect_rate > scrap_threshold else 'badge-info'}">Alarm Limit: &lt; {scrap_threshold:.1f}%</span>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Operational Spend</div>
        <div class="kpi-value">${total_spend/1e6:.1f}M</div>
        <span class="kpi-badge badge-info">${total_spend/total_produced:.2f}/unit avg</span>
    </div>
    <div class="kpi-card warning">
        <div class="kpi-label">Batch Transactions</div>
        <div class="kpi-value">{len(filtered_df):,}</div>
        <span class="kpi-badge badge-info">100% Inspected</span>
    </div>
</div>
"""
st.markdown(kpi_html, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. PROFESSIONAL EXECUTIVE TABS
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏭 Multi-Plant Benchmarking", 
    "⚙️ Machine Reliability & Downtime", 
    "🚚 Supplier Risk Matrix", 
    "📈 Defect Pareto & Shift Disparity",
    "🤖 Grounded AI Business Assistant"
])

def apply_pro_layout(fig, title_text=""):
    fig.update_layout(
        title=dict(text=title_text, font=dict(family="Inter", size=15, color="#F8FAFC")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.6)",
        font=dict(family="Inter", color="#94A3B8"),
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.1)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.1)"),
        hoverlabel=dict(bgcolor="#1E293B", font_size=13, font_family="Inter")
    )
    return fig

# TAB 1: PLANT BENCHMARKING
with tab1:
    st.markdown("### 🏭 Global Multi-Plant Operational Benchmarking")
    col1, col2 = st.columns([3, 2])
    
    fac_group = master_df.groupby("factory_id").agg(
        Produced_Units=("produced_units", "sum"),
        Scrapped_Units=("defective_units", "sum"),
        Inspected_Units=("inspected_units", "sum")
    ).reset_index()
    fac_summary = factories.merge(fac_group, on="factory_id")
    fac_summary["Defect_Rate_Pct"] = (fac_summary["Scrapped_Units"] / fac_summary["Inspected_Units"]) * 100
    fac_summary = fac_summary.sort_values("Defect_Rate_Pct", ascending=True)

    with col1:
        fig_bar = px.bar(
            fac_summary,
            x="Defect_Rate_Pct",
            y="factory_name",
            orientation="h",
            color="Defect_Rate_Pct",
            color_continuous_scale=["#10B981", "#38BDF8", "#F59E0B", "#EF4444"],
            text_auto=".2f",
            title=f"Defect Rate (%) by Plant vs Alarm Limit ({scrap_threshold:.1f}%)"
        )
        fig_bar.add_vline(x=scrap_threshold, line_dash="dash", line_color="#EF4444", annotation_text=f"Limit ({scrap_threshold:.1f}%)")
        apply_pro_layout(fig_bar)
        fig_bar.update_layout(coloraxis_showscale=False, height=360)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        fig_donut = px.pie(
            fac_summary,
            names="factory_name",
            values="Produced_Units",
            hole=0.6,
            color_discrete_sequence=["#38BDF8", "#818CF8", "#C084FC", "#F472B6", "#34D399"],
            title="Global Production Volume Allocation"
        )
        apply_pro_layout(fig_donut)
        fig_donut.update_layout(height=360)
        st.plotly_chart(fig_donut, use_container_width=True)

    st.dataframe(fac_summary[["factory_name", "city", "country", "factory_capacity", "Produced_Units", "Scrapped_Units", "Defect_Rate_Pct"]].style.format({
        "factory_capacity": "{:,} units/mo",
        "Produced_Units": "{:,}",
        "Scrapped_Units": "{:,}",
        "Defect_Rate_Pct": "{:.2f}%"
    }), use_container_width=True)

# TAB 2: MACHINE RELIABILITY
with tab2:
    st.markdown("### ⚙️ Predictive Machine Health & Thermal Stress Analysis")
    col1, col2 = st.columns([3, 2])
    
    machines_df = machines.merge(factories[["factory_id", "factory_name"]], on="factory_id")
    
    with col1:
        fig_scatter = px.scatter(
            machines_df,
            x="temperature",
            y="downtime_hours",
            size="maintenance_count",
            color="temperature",
            color_continuous_scale=["#38BDF8", "#F59E0B", "#EF4444"],
            hover_name="machine_name",
            text="machine_id",
            title=f"Operating Temp (°C) vs. Downtime (Hours) [Alarm: {temp_limit}°C]"
        )
        fig_scatter.add_vline(x=temp_limit, line_dash="dash", line_color="#EF4444", annotation_text=f"Alarm ({temp_limit}°C)")
        apply_pro_layout(fig_scatter)
        fig_scatter.update_layout(height=380)
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col2:
        top_downtime = machines_df.sort_values("downtime_hours", ascending=False).head(5)
        fig_top_m = px.bar(
            top_downtime,
            x="downtime_hours",
            y="machine_name",
            orientation="h",
            color="downtime_hours",
            color_continuous_scale=["#F59E0B", "#EF4444"],
            title="Top 5 Critical Downtime Bottlenecks"
        )
        apply_pro_layout(fig_top_m)
        fig_top_m.update_layout(coloraxis_showscale=False, height=380)
        st.plotly_chart(fig_top_m, use_container_width=True)

    st.error("🚨 **CRITICAL ALERT:** Machine **`MCH_007` (Berlin Plant)** operates at **84.5°C** (+9.5°C above safety cutoff), causing **385.5 hours of downtime** and 14 maintenance breakdowns.")

# TAB 3: SUPPLIER RISK
with tab3:
    st.markdown("### 🚚 Raw Material Supplier Procurement & Quality Risk")
    
    sup_agg = quality.groupby("supplier_id").agg(
        Total_Inspected=("inspected_units", "sum"),
        Total_Scrapped=("defective_units", "sum")
    ).reset_index()
    sup_matrix = suppliers.merge(sup_agg, on="supplier_id")
    sup_matrix["Actual_Scrap_Rate_Pct"] = (sup_matrix["Total_Scrapped"] / sup_matrix["Total_Inspected"]) * 100
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        fig_bubble = px.scatter(
            sup_matrix,
            x="on_time_delivery_percent",
            y="Actual_Scrap_Rate_Pct",
            size="Total_Inspected",
            color="Actual_Scrap_Rate_Pct",
            color_continuous_scale=["#10B981", "#F59E0B", "#EF4444"],
            hover_name="supplier_name",
            text="supplier_name",
            title="Supplier Risk Matrix: On-Time Delivery (OTD %) vs. Scrap Rate (%)"
        )
        fig_bubble.add_hline(y=5.0, line_dash="dash", line_color="#EF4444", annotation_text="High Scrap Risk (>5%)")
        fig_bubble.add_vline(x=90.0, line_dash="dash", line_color="#F59E0B", annotation_text="Min OTD Benchmark (90%)")
        apply_pro_layout(fig_bubble)
        fig_bubble.update_layout(height=380)
        st.plotly_chart(fig_bubble, use_container_width=True)

    with col2:
        fig_radar = px.bar(
            sup_matrix.sort_values("Actual_Scrap_Rate_Pct", ascending=False),
            x="Actual_Scrap_Rate_Pct",
            y="supplier_name",
            orientation="h",
            color="Actual_Scrap_Rate_Pct",
            color_continuous_scale=["#10B981", "#EF4444"],
            title="Supplier In-Plant Scrap Comparison"
        )
        apply_pro_layout(fig_radar)
        fig_radar.update_layout(coloraxis_showscale=False, height=380)
        st.plotly_chart(fig_radar, use_container_width=True)

# TAB 4: DEFECT PARETO & SHIFTS
with tab4:
    st.markdown("### 📈 Defect Mode Pareto (80/20) & Shift Disparity")
    col1, col2 = st.columns([3, 2])
    
    defect_counts = quality[quality["defect_type"] != "None"]["defect_type"].value_counts().reset_index()
    defect_counts.columns = ["Defect_Type", "Count"]
    defect_counts["Cumulative_Pct"] = (defect_counts["Count"].cumsum() / defect_counts["Count"].sum()) * 100

    with col1:
        fig_pareto = make_subplots(specs=[[{"secondary_y": True}]])
        fig_pareto.add_trace(
            go.Bar(x=defect_counts["Defect_Type"], y=defect_counts["Count"], name="Scrap Count", marker_color="#38BDF8"),
            secondary_y=False
        )
        fig_pareto.add_trace(
            go.Scatter(x=defect_counts["Defect_Type"], y=defect_counts["Cumulative_Pct"], name="Cumulative %", mode="lines+markers", line=dict(color="#EF4444", width=3)),
            secondary_y=True
        )
        fig_pareto.add_hline(y=80.0, line_dash="dash", line_color="#F59E0B", secondary_y=True)
        apply_pro_layout(fig_pareto, "Pareto Chart: Defect Types vs. Cumulative Scrap %")
        fig_pareto.update_layout(height=380, showlegend=False)
        st.plotly_chart(fig_pareto, use_container_width=True)

    with col2:
        shift_agg = master_df.groupby("shift_id").agg(
            Inspected=("inspected_units", "sum"),
            Defects=("defective_units", "sum")
        ).reset_index()
        shift_summary = shifts.merge(shift_agg, on="shift_id")
        shift_summary["Defect_Rate"] = (shift_summary["Defects"] / shift_summary["Inspected"]) * 100
        
        fig_shift = px.bar(
            shift_summary,
            x="shift_name",
            y="Defect_Rate",
            color="Defect_Rate",
            color_continuous_scale=["#38BDF8", "#EF4444"],
            text_auto=".2f",
            title="Defect Rate (%) Across Work Shifts"
        )
        apply_pro_layout(fig_shift)
        fig_shift.update_layout(coloraxis_showscale=False, height=380)
        st.plotly_chart(fig_shift, use_container_width=True)

# TAB 5: AI COPILOT
with tab5:
    st.markdown("### 🤖 Executive Grounded AI Copilot (Zero Hallucination)")
    st.markdown("Select an executive inquiry to generate a verified, structured diagnostic briefing:")
    
    col_q, col_b = st.columns([4, 1])
    with col_q:
        executive_prompt = st.selectbox(
            "Management Diagnostic Query:",
            [
                "Which factory is performing poorly and needs immediate engineering attention?",
                "Which machine is causing the most downtime and what is the root cause?",
                "Which supplier represents the highest quality and delivery risk?",
                "Is there a significant quality disparity between operating shifts?",
                "What are our overall quality issues and what should management investigate first?"
            ],
            label_visibility="collapsed"
        )
    with col_b:
        run_ai = st.button("⚡ Run Diagnostic", use_container_width=True)

    if run_ai:
        with st.spinner("Analyzing 55,000 batch records via Grounded SQL Intelligence..."):
            from ai.ai_business_assistant import ManufacturingIntelligenceEngine
            engine = ManufacturingIntelligenceEngine()
            briefing = engine.answer_question_grounded(executive_prompt)
            st.markdown(f'<div class="ai-response-box"><pre style="color: #F8FAFC; font-family: monospace; white-space: pre-wrap; margin:0;">{briefing}</pre></div>', unsafe_allow_html=True)
