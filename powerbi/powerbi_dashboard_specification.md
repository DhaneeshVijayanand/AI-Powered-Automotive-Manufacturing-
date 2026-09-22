# Power BI Dashboard Specification & DAX Architecture
## Project: AI-Powered Automotive Manufacturing BI & Quality Analysis System
### Company: Apex TurboTech (Turbocharger Components)

---

## 1. Data Model (Star Schema)

In Power BI, load the cleaned CSV files from `data/cleaned/` (or connect directly to the MySQL database `apex_manufacturing_db`).

```
                 ┌───────────────┐
                 │   factories   │
                 └───────┬───────┘
                         │ 1:N
 ┌──────────────┐        │        ┌──────────────┐
 │   products   ├────────┼───────►│   machines   │
 └──────┬───────┘        │        └──────┬───────┘
        │ 1:N            ▼ 1:N           │ 1:N
        │        ┌───────────────┐       │
        ├───────►│  production   │◄──────┘
        │        │ (Fact Table)  │
        │        └───────┬───────┘
        │ 1:N            │ 1:1
        │                ▼
        │        ┌───────────────┐
        ├───────►│    quality    │◄──────┬──────────────┐
        │        │ (Fact Table)  │       │ 1:N          │ 1:N
        │        └───────────────┘       │              │
 ┌──────┴───────┐                 ┌──────┴───────┐ ┌────┴─────────┐
 │    shifts    │                 │  suppliers   │ │ Dim_Calendar │
 └──────────────┘                 └──────────────┘ └──────────────┘
```

---

## 2. Core DAX Measures Table

Create a dedicated measures table in Power BI named `_Key_Measures`.

```dax
// --- PRODUCTION MEASURES ---
Total Planned Units = SUM(production[planned_units])

Total Produced Units = SUM(production[produced_units])

Production Efficiency % = 
DIVIDE([Total Produced Units], [Total Planned Units], 0)

Total Production Cost = SUM(production[production_cost])

Avg Cost Per Unit = 
DIVIDE([Total Production Cost], [Total Produced Units], 0)


// --- QUALITY MEASURES ---
Total Inspected Units = SUM(quality[inspected_units])

Total Defective Units = SUM(quality[defective_units])

Defect Rate % = 
DIVIDE([Total Defective Units], [Total Inspected Units], 0)

Defect-Free Batches = 
COUNTROWS(FILTER(quality, quality[defective_units] = 0))


// --- MACHINE & MAINTENANCE MEASURES ---
Total Operating Hours = SUM(machines[operating_hours])

Total Downtime Hours = SUM(machines[downtime_hours])

Machine Downtime % = 
DIVIDE([Total Downtime Hours], [Total Operating Hours] + [Total Downtime Hours], 0)

Avg Machine Temperature = AVERAGE(machines[temperature])

Total Maintenance Events = SUM(machines[maintenance_count])


// --- SUPPLIER METRICS ---
Avg Supplier Quality Score = AVERAGE(suppliers[quality_score])

Avg On-Time Delivery % = AVERAGE(suppliers[on_time_delivery_percent])
```

---

## 3. Six-Page Executive Dashboard Layout

### Page 1: Executive Overview (The CEO/COO Pulse Check)
* **KPI Card 1:** `[Total Produced Units]` (6.88M)
* **KPI Card 2:** `[Total Defective Units]` (195.4K)
* **KPI Card 3:** `[Defect Rate %]` (2.99%)
* **KPI Card 4:** `[Total Production Cost]` (\$1.17B)
* **KPI Card 5:** `[Total Downtime Hours]` (1,595 hrs)
* **KPI Card 6:** `[Avg On-Time Delivery %]` (94.2%)
* **Chart 1 (Area Chart):** Monthly Produced Units vs Defect Rate % Trend (`date[Year-Month]`)
* **Chart 2 (Clustered Bar Chart):** Defect Rate % by Factory (`factories[factory_name]`)
* **Chart 3 (Donut Chart):** Production Volume Share by Product Category (`products[product_category]`)
* **Slicers:** Date Range Slider, Factory Selector, Product Category

### Page 2: Production Operations Analysis
* **Visual 1 (Stacked Column Chart):** Planned vs Actual Produced Units by Factory
* **Visual 2 (Line & Clustered Column Chart):** Monthly Production Efficiency % & Total Cost
* **Visual 3 (Matrix Grid):** Factory vs Shift Production Breakdown (Rows: `factory_name`, Columns: `shift_name`, Values: `[Total Produced Units]`, `[Production Efficiency %]`)
* **Visual 4 (Treemap):** Production Share by Product Name

### Page 3: Quality & Scrap Root-Cause Analysis
* **Visual 1 (Pareto Chart):** Defect Count by `defect_type` with Cumulative % line
* **Visual 2 (Heatmap Matrix):** Product Name vs Defect Type scrap density
* **Visual 3 (Clustered Column Chart):** Defect Rate % by Shift (`Morning`, `Evening`, `Night`)
* **Visual 4 (Scatter Plot):** Factory Capacity vs Defect Rate %

### Page 4: Machine Reliability & Predictive Maintenance
* **Visual 1 (Scatter Plot):** Machine Operating Temperature (°C) vs Downtime Hours (Color by `factory_name`)
* **Visual 2 (Bar Chart):** Top 10 Machines Ranked by Downtime Hours (Highlights `MCH_007` in red)
* **Visual 3 (Gauge / Radial KPI):** Average Machine Utilization Rate %
* **Visual 4 (Table Visual):** Machine ID, Machine Name, Machine Type, Maintenance Count, Operating Hours, Downtime Hours, Thermal Status

### Page 5: Supplier Quality & Procurement Risk
* **Visual 1 (Quadrant Bubble Chart):** On-Time Delivery % (X-axis) vs Actual Scrap Rate % (Y-axis), Size: Inspected Volume (Highlights `SUP_04` in the critical danger quadrant)
* **Visual 2 (Clustered Bar Chart):** Supplier Quality Rating vs Actual Defect Rate
* **Visual 3 (Table):** Supplier Name, Material Type, Total Batches Supplied, Total Scrap Units, Material Cost, Risk Tier

### Page 6: Management Insights & Actionable Recommendations
* **Visual 1 (Multi-row Card):** Identified Operational Bottlenecks
* **Visual 2 (Callout Box):** AI-Generated Verified Root-Cause Summaries
* **Visual 3 (Action Matrix):** High-Priority Plant & Supplier Corrective Actions (CAPA)
