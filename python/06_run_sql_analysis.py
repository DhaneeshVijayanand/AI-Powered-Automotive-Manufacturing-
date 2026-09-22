"""
=============================================================================
Module: 06_run_sql_analysis.py
Project: AI-Powered Automotive Manufacturing BI & Quality Analysis System
Description: Executes the SQL analytics queries directly against the cleaned
             data and prints formatted business intelligence results.
=============================================================================
"""

import os
import sqlite3
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN_DIR = os.path.join(BASE_DIR, "data", "cleaned")

# Create in-memory SQL database for fast, self-contained SQL execution
conn = sqlite3.connect(":memory:")

print("[INFO] Loading cleaned CSV datasets into SQL engine...")
for table_name in ["factories", "products", "shifts", "suppliers", "machines", "production", "quality"]:
    df = pd.read_csv(os.path.join(CLEAN_DIR, f"{table_name}.csv"))
    df.to_sql(table_name, conn, index=False, if_exists="replace")

print("[SUCCESS] All tables loaded into SQL engine.\n")

def run_query(title, query):
    print("=" * 75)
    print(f" {title.upper()}")
    print("=" * 75)
    df_res = pd.read_sql_query(query, conn)
    print(df_res.to_string(index=False))
    print()

# Query 1: KPI Summary
q1 = """
SELECT 
    COUNT(DISTINCT p.production_id) AS total_batches,
    SUM(p.produced_units) AS total_produced_units,
    SUM(q.inspected_units) AS total_inspected_units,
    SUM(q.defective_units) AS total_defective_units,
    ROUND((CAST(SUM(q.defective_units) AS FLOAT) / SUM(q.inspected_units)) * 100, 2) AS defect_rate_pct,
    PRINTF('$%,.2f', SUM(p.production_cost)) AS total_production_spend
FROM production p
JOIN quality q ON p.production_id = q.production_id;
"""
run_query("1. Executive Global KPI Summary", q1)

# Query 2: Factory Benchmarking
q2 = """
SELECT 
    f.factory_name,
    f.city,
    f.country,
    SUM(p.produced_units) AS total_produced,
    SUM(q.defective_units) AS total_defects,
    ROUND((CAST(SUM(q.defective_units) AS FLOAT) / SUM(q.inspected_units)) * 100, 2) AS defect_rate_pct,
    ROUND((CAST(SUM(p.produced_units) AS FLOAT) / SUM(p.planned_units)) * 100, 2) AS efficiency_pct,
    RANK() OVER (ORDER BY (CAST(SUM(q.defective_units) AS FLOAT) / SUM(q.inspected_units)) ASC) AS quality_rank
FROM factories f
JOIN production p ON f.factory_id = p.factory_id
JOIN quality q ON p.production_id = q.production_id
GROUP BY f.factory_id
ORDER BY defect_rate_pct DESC;
"""
run_query("2. Factory Quality & Efficiency Ranking", q2)

# Query 3: Machine Downtime & Thermal Status
q3 = """
SELECT 
    m.machine_id,
    m.machine_name,
    m.operating_hours,
    m.downtime_hours,
    ROUND((m.downtime_hours / (m.operating_hours + m.downtime_hours)) * 100, 2) AS downtime_pct,
    m.temperature AS temp_celsius,
    m.maintenance_count,
    CASE 
        WHEN m.temperature > 75.0 THEN 'CRITICAL (Overheating)'
        WHEN m.temperature > 65.0 THEN 'WARNING (Elevated)'
        ELSE 'NORMAL'
    END AS thermal_status
FROM machines m
ORDER BY m.downtime_hours DESC
LIMIT 5;
"""
run_query("3. Top 5 Machines by Downtime & Thermal Stress", q3)

# Query 4: Supplier Risk Matrix
q4 = """
SELECT 
    s.supplier_id,
    s.supplier_name,
    s.material_type,
    s.on_time_delivery_percent AS otd_pct,
    s.quality_score AS vendor_score,
    SUM(q.inspected_units) AS units_inspected,
    SUM(q.defective_units) AS defective_units,
    ROUND((CAST(SUM(q.defective_units) AS FLOAT) / SUM(q.inspected_units)) * 100, 2) AS scrap_rate_pct,
    CASE 
        WHEN (CAST(SUM(q.defective_units) AS FLOAT) / SUM(q.inspected_units)) * 100 > 5.0 THEN 'HIGH RISK - Immediate Audit'
        WHEN (CAST(SUM(q.defective_units) AS FLOAT) / SUM(q.inspected_units)) * 100 > 2.5 THEN 'MODERATE RISK - Monitor'
        ELSE 'PREFERRED VENDOR'
    END AS risk_tier
FROM suppliers s
JOIN quality q ON s.supplier_id = q.supplier_id
GROUP BY s.supplier_id
ORDER BY scrap_rate_pct DESC;
"""
run_query("4. Supplier Quality & Delivery Risk Matrix", q4)

# Query 5: Shift Performance
q5 = """
SELECT 
    sh.shift_name,
    SUM(p.produced_units) AS total_produced,
    SUM(q.defective_units) AS total_defects,
    ROUND((CAST(SUM(q.defective_units) AS FLOAT) / SUM(q.inspected_units)) * 100, 2) AS shift_defect_rate_pct
FROM shifts sh
JOIN production p ON sh.shift_id = p.shift_id
JOIN quality q ON p.production_id = q.production_id
GROUP BY sh.shift_id
ORDER BY shift_defect_rate_pct DESC;
"""
run_query("5. Shift-Level Defect Analysis", q5)

# Query 6: Top Defect Types Pareto
q6 = """
SELECT 
    defect_type,
    SUM(defective_units) AS defective_pieces,
    ROUND((CAST(SUM(defective_units) AS FLOAT) / (SELECT SUM(defective_units) FROM quality)) * 100, 2) AS pct_of_total_defects
FROM quality
WHERE defect_type != 'None'
GROUP BY defect_type
ORDER BY defective_pieces DESC;
"""
run_query("6. Defect Category Breakdown (Pareto Analysis)", q6)
