-- =============================================================================
-- APEX TURBOTECH - EXECUTIVE SQL BUSINESS INTELLIGENCE ANALYSIS
-- Database: apex_manufacturing_db
-- File: sql/02_business_analysis_queries.sql
-- =============================================================================

USE apex_manufacturing_db;

-- =============================================================================
-- QUERY 1: EXECUTIVE KPI SUMMARY
-- Business Question: What is our total production volume, total defects, 
-- overall defect rate, and total production expenditure across all plants?
-- =============================================================================
SELECT 
    COUNT(DISTINCT p.production_id) AS total_batches,
    SUM(p.produced_units) AS total_produced_units,
    SUM(q.inspected_units) AS total_inspected_units,
    SUM(q.defective_units) AS total_defective_units,
    ROUND((SUM(q.defective_units) / SUM(q.inspected_units)) * 100, 2) AS overall_defect_rate_pct,
    CONCAT('$', FORMAT(SUM(p.production_cost), 2)) AS total_production_cost
FROM production p
JOIN quality q ON p.production_id = q.production_id;

-- Business Meaning:
-- Gives the CEO/COO a 1-second pulse check on company-wide volume, scrap rate, and operational spend.


-- =============================================================================
-- QUERY 2: FACTORY BENCHMARKING & PERFORMANCE RANKING
-- Business Question: Which factory is performing best, and which factory has the 
-- highest defect rate and lowest production efficiency?
-- =============================================================================
SELECT 
    f.factory_name,
    f.city,
    f.country,
    SUM(p.planned_units) AS total_planned,
    SUM(p.produced_units) AS total_produced,
    ROUND((SUM(p.produced_units) / SUM(p.planned_units)) * 100, 2) AS production_efficiency_pct,
    SUM(q.inspected_units) AS total_inspected,
    SUM(q.defective_units) AS total_defects,
    ROUND((SUM(q.defective_units) / SUM(q.inspected_units)) * 100, 2) AS defect_rate_pct,
    RANK() OVER (ORDER BY (SUM(q.defective_units) / SUM(q.inspected_units)) ASC) AS quality_rank
FROM factories f
JOIN production p ON f.factory_id = p.factory_id
JOIN quality q ON p.production_id = q.production_id
GROUP BY f.factory_id, f.factory_name, f.city, f.country
ORDER BY defect_rate_pct DESC;

-- Business Meaning:
-- Ranks factories by quality. Pinpoints Pune (FAC_02) as the lowest performing plant in defect rate.


-- =============================================================================
-- QUERY 3: MACHINE DOWNTIME, TEMPERATURE & RELIABILITY RANKING
-- Business Question: Which machines cause the most downtime and maintenance overhead? 
-- Is high operating temperature correlated with downtime?
-- =============================================================================
SELECT 
    m.machine_id,
    m.machine_name,
    f.factory_name,
    m.machine_type,
    m.operating_hours,
    m.downtime_hours,
    ROUND((m.downtime_hours / (m.operating_hours + m.downtime_hours)) * 100, 2) AS downtime_pct,
    m.temperature AS current_temp_celsius,
    m.maintenance_count,
    CASE 
        WHEN m.temperature > 75.0 THEN 'CRITICAL (Overheating)'
        WHEN m.temperature > 65.0 THEN 'WARNING (Elevated)'
        ELSE 'NORMAL'
    END AS thermal_status
FROM machines m
JOIN factories f ON m.factory_id = f.factory_id
ORDER BY m.downtime_hours DESC
LIMIT 5;

-- Business Meaning:
-- Identifies MCH_007 (Pune CNC Lathe) running at 84.5°C with 385+ downtime hours and 14 maintenance events.


-- =============================================================================
-- QUERY 4: SUPPLIER QUALITY & ON-TIME DELIVERY (OTD) RISK MATRIX
-- Business Question: Which suppliers supply the highest defect rates, and are they 
-- failing on-time delivery commitments?
-- =============================================================================
SELECT 
    s.supplier_id,
    s.supplier_name,
    s.material_type,
    s.on_time_delivery_percent,
    s.quality_score AS vendor_scorecard_rating,
    COUNT(q.quality_id) AS total_batches_supplied,
    SUM(q.inspected_units) AS total_units_inspected,
    SUM(q.defective_units) AS total_defective_units,
    ROUND((SUM(q.defective_units) / SUM(q.inspected_units)) * 100, 2) AS actual_scrap_rate_pct,
    CASE 
        WHEN (SUM(q.defective_units) / SUM(q.inspected_units)) * 100 > 5.0 THEN 'HIGH RISK - Immediate Audit'
        WHEN (SUM(q.defective_units) / SUM(q.inspected_units)) * 100 > 2.5 THEN 'MODERATE RISK - Monitor'
        ELSE 'PREFERRED VENDOR'
    END AS vendor_risk_tier
FROM suppliers s
JOIN quality q ON s.supplier_id = q.supplier_id
GROUP BY s.supplier_id, s.supplier_name, s.material_type, s.on_time_delivery_percent, s.quality_score
ORDER BY actual_scrap_rate_pct DESC;

-- Business Meaning:
-- Identifies SUP_04 (Apex Raw Castings Ltd) with ~7.2% actual scrap rate and poor 81.4% OTD.


-- =============================================================================
-- QUERY 5: SHIFT-LEVEL PERFORMANCE & DEFECT VARIANCE
-- Business Question: Is there a significant quality disparity between Morning, 
-- Evening, and Night shifts?
-- =============================================================================
SELECT 
    sh.shift_id,
    sh.shift_name,
    sh.start_time,
    sh.end_time,
    SUM(p.produced_units) AS total_produced,
    SUM(q.defective_units) AS total_defects,
    ROUND((SUM(q.defective_units) / SUM(q.inspected_units)) * 100, 2) AS shift_defect_rate_pct,
    ROUND(AVG(p.production_cost / p.produced_units), 2) AS avg_cost_per_unit
FROM shifts sh
JOIN production p ON sh.shift_id = p.shift_id
JOIN quality q ON p.production_id = q.production_id
GROUP BY sh.shift_id, sh.shift_name, sh.start_time, sh.end_time
ORDER BY shift_defect_rate_pct DESC;

-- Business Meaning:
-- Confirms Night Shift (SH_03) produces higher defect rates due to fatigue/reduced supervisory coverage.


-- =============================================================================
-- QUERY 6: PRODUCT LINE QUALITY & DEFECT CONTRIBUTION
-- Business Question: Which turbocharger components experience the highest defect rates?
-- =============================================================================
SELECT 
    prd.product_id,
    prd.product_name,
    prd.product_category,
    SUM(p.produced_units) AS total_units_produced,
    SUM(q.defective_units) AS total_defects,
    ROUND((SUM(q.defective_units) / SUM(q.inspected_units)) * 100, 2) AS product_defect_rate_pct,
    ROUND((SUM(q.defective_units) * 100.0 / (SELECT SUM(defective_units) FROM quality)), 2) AS pct_of_all_global_defects
FROM products prd
JOIN production p ON prd.product_id = p.product_id
JOIN quality q ON p.production_id = q.production_id
GROUP BY prd.product_id, prd.product_name, prd.product_category
ORDER BY product_defect_rate_pct DESC;

-- Business Meaning:
-- Cast Iron Bearing Housings (PRD_03) and Nickel Alloy Turbine Housings (PRD_04) carry the highest scrap rates.


-- =============================================================================
-- QUERY 7: DEFECT TYPE PARETO ANALYSIS (80/20 Rule)
-- Business Question: What are the primary root-cause defect categories causing scrap?
-- =============================================================================
WITH DefectSummary AS (
    SELECT 
        defect_type,
        COUNT(*) AS occurrence_count,
        SUM(defective_units) AS total_defective_pieces
    FROM quality
    WHERE defect_type <> 'None'
    GROUP BY defect_type
)
SELECT 
    defect_type,
    total_defective_pieces,
    ROUND((total_defective_pieces * 100.0 / (SELECT SUM(defective_units) FROM quality)), 2) AS pct_share,
    SUM(ROUND((total_defective_pieces * 100.0 / (SELECT SUM(defective_units) FROM quality)), 2)) 
        OVER (ORDER BY total_defective_pieces DESC) AS cumulative_pareto_pct
FROM DefectSummary
ORDER BY total_defective_pieces DESC;

-- Business Meaning:
-- "Casting Porosity / Blowholes" and "Dimensional Out-of-Tolerance" account for > 60% of all rejected parts.


-- =============================================================================
-- QUERY 8: MONTH-OVER-MONTH (MoM) PRODUCTION & DEFECT TREND
-- Business Question: How has production volume and defect rate evolved over time?
-- =============================================================================
WITH MonthlyData AS (
    SELECT 
        DATE_FORMAT(p.date, '%Y-%m') AS prod_month,
        SUM(p.produced_units) AS monthly_production,
        SUM(q.defective_units) AS monthly_defects,
        ROUND((SUM(q.defective_units) / SUM(q.inspected_units)) * 100, 2) AS monthly_defect_rate
    FROM production p
    JOIN quality q ON p.production_id = q.production_id
    GROUP BY DATE_FORMAT(p.date, '%Y-%m')
)
SELECT 
    prod_month,
    monthly_production,
    monthly_defects,
    monthly_defect_rate,
    LAG(monthly_defect_rate, 1) OVER (ORDER BY prod_month) AS prev_month_defect_rate,
    ROUND(monthly_defect_rate - LAG(monthly_defect_rate, 1) OVER (ORDER BY prod_month), 2) AS defect_rate_delta
FROM MonthlyData
ORDER BY prod_month ASC;

-- Business Meaning:
-- Allows executive leadership to track whether quality improvement programs are driving scrap rates down.
