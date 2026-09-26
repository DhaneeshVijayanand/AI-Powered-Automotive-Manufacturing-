"""
=============================================================================
Apex TurboTech - AI-Powered Automotive Manufacturing BI & Quality Dashboard
Live Web Application (Streamlit + Plotly)
=============================================================================
"""

import os
import json
import sqlite3
import pandas as pd
import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Apex TurboTech | Automotive Manufacturing BI",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    .metric-card {
        background-color: #1E293B;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #334155;
        text-align: center;
    }
    .metric-value { font-size: 28px; font-weight: bold; color: #38BDF8; }
    .metric-label { font-size: 14px; color: #94A3B8; }
    </style>
""", unsafe_allow_html=True)

# Load Datasets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLEAN_DIR = os.path.join(BASE_DIR, "data", "cleaned")

@st.cache_data
def load_data():
    factories = pd.read_csv(os.path.join(CLEAN_DIR, "factories.csv"))
    products = pd.read_csv(os.path.join(CLEAN_DIR, "products.csv"))
    shifts = pd.read_csv(os.path.join(CLEAN_DIR, "shifts.csv"))
    suppliers = pd.read_csv(os.path.join(CLEAN_DIR, "suppliers.csv"))
    machines = pd.read_csv(os.path.join(CLEAN_DIR, "machines.csv"))
    production = pd.read_csv(os.path.join(CLEAN_DIR, "production.csv"))
    quality = pd.read_csv(os.path.join(CLEAN_DIR, "quality.csv"))
    return factories, products, shifts, suppliers, machines, production, quality

factories, products, shifts, suppliers, machines, production, quality = load_data()

# Header
st.title("🚗 Apex TurboTech — Automotive Manufacturing BI & Quality System")
st.caption("Tier-1 Automotive Component Manufacturing Intelligence & Grounded AI Decision Support")

# Sidebar Filters
st.sidebar.header("🔍 Global Operational Filters")
selected_factory = st.sidebar.selectbox("Select Plant", ["All Plants"] + factories["factory_name"].tolist())
selected_shift = st.sidebar.selectbox("Select Shift", ["All Shifts"] + shifts["shift_name"].tolist())

# Filter data
filtered_prod = production.copy()
filtered_qual = quality.copy()

if selected_factory != "All Plants":
    fac_id = factories[factories["factory_name"] == selected_factory]["factory_id"].values[0]
    filtered_prod = filtered_prod[filtered_prod["factory_id"] == fac_id]
    filtered_qual = filtered_qual[filtered_qual["factory_id"] == fac_id]

if selected_shift != "All Shifts":
    shf_id = shifts[shifts["shift_name"] == selected_shift]["shift_id"].values[0]
    filtered_prod = filtered_prod[filtered_prod["shift_id"] == shf_id]

# Top KPI Cards
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
total_produced = filtered_prod["produced_units"].sum()
total_inspected = filtered_qual["inspected_units"].sum()
total_defects = filtered_qual["defective_units"].sum()
defect_rate = (total_defects / total_inspected * 100) if total_inspected > 0 else 0
total_spend = filtered_prod["production_cost"].sum()

with kpi1:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{total_produced:,}</div><div class="metric-label">Total Produced Units</div></div>', unsafe_allow_html=True)
with kpi2:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{total_defects:,}</div><div class="metric-label">Total Scrapped Units</div></div>', unsafe_allow_html=True)
with kpi3:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{defect_rate:.2f}%</div><div class="metric-label">Overall Defect Rate</div></div>', unsafe_allow_html=True)
with kpi4:
    st.markdown(f'<div class="metric-card"><div class="metric-value">${total_spend:,.2f}</div><div class="metric-label">Total Production Spend</div></div>', unsafe_allow_html=True)
with kpi5:
    st.markdown(f'<div class="metric-card"><div class="metric-value">55,000</div><div class="metric-label">Total Batches</div></div>', unsafe_allow_html=True)

st.write("")

# Navigation Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Plant Benchmarking", 
    "⚙️ Machine Reliability & Downtime", 
    "🚚 Supplier Risk Matrix", 
    "📈 Defect Pareto & Shift Disparity",
    "🤖 Grounded AI Business Assistant"
])

# Tab 1: Plant Benchmarking
with tab1:
    st.subheader("🏭 Global Multi-Plant Performance Benchmarking")
    col1, col2 = st.columns([1, 1])
    
    # Factory Summary Aggregation
    df_merged = quality.merge(production, on="production_id").merge(factories, on="factory_id_x")
    fac_summary = df_merged.groupby("factory_name").agg(
        Produced_Units=("produced_units", "sum"),
        Scrapped_Units=("defective_units", "sum"),
        Inspected_Units=("inspected_units", "sum"),
    ).reset_index()
    fac_summary["Defect_Rate_Pct"] = (fac_summary["Scrapped_Units"] / fac_summary["Inspected_Units"]) * 100
    fac_summary = fac_summary.sort_values("Defect_Rate_Pct", ascending=False)
    
    with col1:
        st.write("#### Defect Rate % by Manufacturing Plant")
        st.bar_chart(data=fac_summary.set_index("factory_name")["Defect_Rate_Pct"])
        st.caption("🔴 Notice Pune Plant exhibits the highest defect rate at 3.82% vs 2.80% in Mexicali.")
        
    with col2:
        st.write("#### Factory Operational Scorecard")
        st.dataframe(fac_summary.style.format({
            "Produced_Units": "{:,}",
            "Scrapped_Units": "{:,}",
            "Inspected_Units": "{:,}",
            "Defect_Rate_Pct": "{:.2f}%"
        }), use_container_width=True)

# Tab 2: Machine Reliability
with tab2:
    st.subheader("⚙️ Machine Operating Temperature vs Unplanned Downtime")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("#### Top Machines by Downtime Hours")
        top_machines = machines.sort_values("downtime_hours", ascending=False).head(8)
        st.bar_chart(data=top_machines.set_index("machine_name")["downtime_hours"])
        
    with col2:
        st.write("#### Critical Overheating Machines Table")
        st.dataframe(machines[["machine_id", "machine_name", "downtime_hours", "temperature", "maintenance_count"]].sort_values("downtime_hours", ascending=False), use_container_width=True)
        st.warning("⚠️ Machine MCH_007 (Pune Plant) operating at 84.5°C with 385.5 hours downtime. Thermal limit is 75.0°C.")

# Tab 3: Supplier Risk
with tab3:
    st.subheader("🚚 Raw Material Supplier Scrap & On-Time Delivery (OTD) Matrix")
    
    sup_qual = quality.merge(suppliers, on="supplier_id").groupby(["supplier_name", "material_type", "on_time_delivery_percent", "quality_score"]).agg(
        Total_Inspected=("inspected_units", "sum"),
        Total_Scrapped=("defective_units", "sum")
    ).reset_index()
    sup_qual["Actual_Scrap_Rate_Pct"] = (sup_qual["Total_Scrapped"] / sup_qual["Total_Inspected"]) * 100
    sup_qual = sup_qual.sort_values("Actual_Scrap_Rate_Pct", ascending=False)
    
    st.dataframe(sup_qual.style.format({
        "Total_Inspected": "{:,}",
        "Total_Scrapped": "{:,}",
        "on_time_delivery_percent": "{:.1f}%",
        "quality_score": "{:.1f}",
        "Actual_Scrap_Rate_Pct": "{:.2f}%"
    }), use_container_width=True)
    st.error("🚨 Critical Supplier: **Apex Raw Castings Ltd (SUP_04)** has an 8.21% scrap rate and 81.4% OTD (Target: >95%).")

# Tab 4: Defect Pareto
with tab4:
    st.subheader("📈 Defect Mode Pareto Analysis (80/20 Rule)")
    col1, col2 = st.columns([1, 1])
    
    defect_summary = quality[quality["defect_type"] != "None"]["defect_type"].value_counts().reset_index()
    defect_summary.columns = ["Defect Type", "Count"]
    
    with col1:
        st.write("#### Primary Root-Cause Defect Distribution")
        st.bar_chart(defect_summary.set_index("Defect Type"))
        
    with col2:
        st.write("#### Shift-Level Quality Disparity")
        shift_qual = quality.merge(shifts, on="shift_id").groupby("shift_name").agg(
            Inspected=("inspected_units", "sum"),
            Defects=("defective_units", "sum")
        ).reset_index()
        shift_qual["Shift_Defect_Rate"] = (shift_qual["Defects"] / shift_qual["Inspected"]) * 100
        st.dataframe(shift_qual.style.format({
            "Inspected": "{:,}",
            "Defects": "{:,}",
            "Shift_Defect_Rate": "{:.2f}%"
        }), use_container_width=True)
        st.info("🌙 Night Shift has a 3.65% defect rate (+33% higher variance than Morning shift at 2.74%).")

# Tab 5: AI Assistant
with tab5:
    st.subheader("🤖 Grounded AI Manufacturing Business Assistant")
    st.markdown("Ask natural language business questions to diagnose plant operations without hallucinations:")
    
    user_query = st.selectbox(
        "Select an Executive Question:",
        [
            "Which factory is performing poorly and needs the most attention?",
            "Which machine is causing the most downtime and why?",
            "Which supplier represents the highest quality and delivery risk?",
            "Is there a quality difference across operating shifts?",
            "What are our overall quality issues and what should management investigate first?"
        ]
    )
    
    if st.button("Generate Executive AI Briefing"):
        from ai.ai_business_assistant import ManufacturingIntelligenceEngine
        engine = ManufacturingIntelligenceEngine()
        response = engine.answer_question_grounded(user_query)
        st.code(response, language="markdown")
