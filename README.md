# 🚗 AI-Powered Automotive Manufacturing Business Intelligence & Quality Analysis System

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-orange.svg)](https://www.mysql.com/)
[![Power BI](https://img.shields.io/badge/Power%20BI-Desktop-yellow.svg)](https://powerbi.microsoft.com/)
[![Role Focus](https://img.shields.io/badge/Target%20Role-Business%20%2F%20BI%20%2F%20Data%20Analyst-brightgreen.svg)]()
[![Domain](https://img.shields.io/badge/Industry-Automotive%20Turbocharger%20Manufacturing-red.svg)]()

> **An End-to-End Enterprise Analytics, Data Engineering, and Grounded AI Decision-Support Platform for Automotive Component Manufacturing.**

---

## 📌 Executive Summary

**Apex TurboTech** is a fictional Tier-1 automotive manufacturer producing precision turbocharger components (turbine wheels, compressor housings, ceramic bearings) across 5 global manufacturing plants (Bangalore, Pune, Mexicali, Bucharest, Wuhan). 

This project simulates a **real enterprise data pipeline and analytics platform** designed to solve shop-floor data fragmentation, identify machine downtime root causes, evaluate supplier quality risk, and empower plant leadership with **grounded AI decision support** without hallucination risks.

---

## 🏗️ System Architecture

```text
  [ Raw Data (55,000+ Records) ]
                │
                ▼
  [ Python + Pandas Data Pipeline ]  ───► Cleaning, deduplication, schema validation
                │
                ▼
      [ MySQL Central DWH ]          ───► 7-table Star Schema with PK/FK Constraints
                │
        ┌───────┴────────────────────────────┐
        ▼                                    ▼
  [ SQL Analytics Engine ]          [ Power BI Executive Dashboards ]
  • Multi-plant Benchmarking        • 6-Page Interactive Suite
  • Machine Downtime Pareto         • Custom DAX Measure Repository
  • Supplier Risk Quadrant          • Star Schema Data Modeling
        │                                    │
        └─────────────────┬──────────────────┘
                          ▼
             [ Grounded AI Business Assistant ]
             • Verified Metric Ingestion
             • Natural Language Root-Cause Briefings
             • Corrective Action Plans (CAPA)
```

---

## 📊 Business Intelligence & Analytical Insights Discovered

Through automated SQL and Power BI analytics across 55,000 batches (6.88M produced components):

| Focus Area | Key Data Finding | Management Root-Cause | Action Taken / Recommendation |
| :--- | :--- | :--- | :--- |
| **Plant Quality** | **Pune Plant** has the highest scrap rate at **3.82%** (vs 2.80% in Mexicali/Wuhan). | Concentrated thermal machine failures & high-risk supplier casting usage. | Prioritize engineering audits and equipment recalibration in Pune. |
| **Machine Downtime** | Machine **`MCH_007`** caused **385.5 hours** of downtime (11.06% downtime ratio). | Operating temperature reached **84.5°C** (critical threshold > 75°C) causing spindle drift. | Mandatory shutdown to replace cooling loops and install IoT thermal cutoff sensors. |
| **Supplier Risk** | **Apex Raw Castings (`SUP_04`)** has an **8.21% scrap rate** and **81.4% OTD**. | Raw casting porosity and sub-surface blowholes in nickel alloy housings. | Quarantine in-transit batches; reallocate 40% volume to EuroMetals (`SUP_05`). |
| **Shift Disparity** | **Night Shift** defect rate is **3.65%** (+33% higher than Morning Shift at 2.74%). | Fatigue and lack of senior quality engineering supervision off-hours. | Enforce mandatory 22:00 handover calibration sign-offs and rotate senior QA staff. |
| **Scrap Breakdown** | **Casting Porosity (26.86%)** & **Dimensional Out-of-Tolerance (20.45%)** lead defects. | Supplier metallurgy flaws and CNC thermal expansion. | Focus CAPA initiatives on the top 2 defect modes to eliminate >47% of scrap. |

---

## 🗄️ Relational Data Model (Star Schema)

The database schema `apex_manufacturing_db` consists of 7 normalized tables:

* **Dimension Tables:**
  * `factories` (5 global manufacturing plants)
  * `products` (8 turbocharger component types)
  * `shifts` (Morning, Evening, Night)
  * `suppliers` (10 raw material vendors with OTD and scorecards)
  * `machines` (20 precision CNC/balancing machines with temperatures and maintenance logs)
* **Fact Tables:**
  * `production` (55,000 batches: dates, planned vs actual units, production spend)
  * `quality` (55,000 records: inspected units, defective units, categorized defect types)

---

## 💻 Tech Stack & Tools

* **Programming & ETL:** Python 3.13, Pandas, NumPy
* **Relational Database:** MySQL 8.0, SQL (CTEs, Window Functions, DDL/DML, Indexes)
* **Business Intelligence:** Microsoft Power BI Desktop, DAX (Data Analysis Expressions)
* **AI & Decision Support:** Grounded LLM Prompt Engineering, Verified SQL Reasoning Engine
* **Version Control & Docs:** Git, GitHub, Markdown

---

## 🚀 Quickstart & Execution Guide

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/automotive-bi-project.git
cd automotive-bi-project
```

### 2. Install Python Dependencies
```bash
py -m pip install -r requirements.txt
```

### 3. Generate the Synthetic Manufacturing Dataset
```bash
py python/01_generate_master_data.py
py python/02_generate_production_data.py
py python/03_generate_quality_data.py
```

### 4. Run the Automated Data Cleaning Pipeline
```bash
py python/04_data_cleaning.py
```

### 5. Execute SQL Business Analytics
```bash
py python/06_run_sql_analysis.py
```

### 6. Run the Grounded AI Business Assistant
```bash
py ai/ai_business_assistant.py
```

---

## 📁 Repository Structure

```text
automotive-bi-project/
│
├── data/
│   ├── raw/                 # 7 raw generated CSV files
│   └── cleaned/             # 7 sanitized & validated CSV datasets
│
├── python/
│   ├── 01_generate_master_data.py       # Master dimension data generator
│   ├── 02_generate_production_data.py   # 55k production transaction generator
│   ├── 03_generate_quality_data.py      # 55k quality inspection generator
│   ├── 04_data_cleaning.py              # Automated 7-step cleaning pipeline
│   ├── 05_load_to_mysql.py              # Automated MySQL schema & bulk loader
│   └── 06_run_sql_analysis.py           # Standalone SQL query execution engine
│
├── sql/
│   ├── 01_create_database_schema.sql    # MySQL DDL with PK/FK constraints & indexes
│   └── 02_business_analysis_queries.sql # Executive business analytics queries
│
├── powerbi/
│   └── powerbi_dashboard_specification.md # 6-page visual layout & DAX measure formulas
│
├── ai/
│   ├── system_prompts.py                # Zero-hallucination executive system prompts
│   └── ai_business_assistant.py         # Grounded AI decision-support assistant
│
├── documentation/
│   ├── business_requirements_document.md # BRD, FRD, 10 User Stories, and RTM
│   ├── project_academic_report.md        # Complete 20-section academic/project report
│   ├── presentation_slides_and_script.md # 15-slide deck & 5-minute verbal presentation script
│   └── interview_preparation_guide.md    # Automotive BA/BI Analyst interview Q&A
│
├── requirements.txt         # Required Python packages
├── .gitignore               # Security & ignore rules
└── README.md                # Project documentation
```

---

## 🎯 Author & Career Objective
* **Author:** B.Tech Computer Science and Business Systems (CSBS)
* **Target Role:** Business Analyst / BI Analyst / Data Analyst
* **Target Industry:** Automotive Technology (Garrett Motion, Bosch, BorgWarner, Cummins)
