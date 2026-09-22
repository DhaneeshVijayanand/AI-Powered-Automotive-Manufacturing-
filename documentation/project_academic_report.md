# Academic & Engineering Project Report
## AI-Powered Automotive Manufacturing Business Intelligence & Quality Analysis System

---

## Table of Contents
1. Abstract
2. Introduction
3. Problem Statement
4. Existing System vs. Proposed System
5. Project Objectives
6. Scope of the System
7. Requirements Analysis (BRD, FRD, NFR)
8. System Architecture
9. Relational Data Model (Star Schema)
10. Methodology & Data Engineering
11. Data Cleaning & Validation Pipeline
12. Relational Database Implementation (MySQL)
13. Executive SQL Analytics
14. Power BI Interactive Dashboard Suite
15. Grounded AI Decision-Support Module
16. Experimental Results & Operational Insights
17. Business Benefits & ROI Impact
18. System Limitations
19. Future Enhancements
20. Conclusion & References

---

## 1. Abstract
In modern automotive component manufacturing, strict zero-defect tolerance and high overall equipment effectiveness (OEE) are critical to maintaining profitability and Tier-1 supplier certification. This project designs and implements an end-to-end Business Intelligence (BI) and Quality Analysis System for a multi-plant automotive manufacturer specializing in precision turbocharger assemblies. The platform aggregates 55,000+ manufacturing batch records across 5 global plants, cleanses anomalies through an automated Python/Pandas data pipeline, models a normalized Star Schema in MySQL, delivers sub-second executive visual analytics in Microsoft Power BI, and integrates a zero-hallucination Grounded AI Business Assistant to translate verified SQL metrics into actionable Corrective and Preventive Actions (CAPA).

---

## 2. Introduction
Automotive turbocharger components (titanium turbine wheels, billet compressor wheels, ceramic bearing units) operate in extreme environments of up to 1050°C and 280,000 RPM. Consequently, manufacturing tolerances are measured in micrometers. In such high-precision settings, even a 0.5% spike in scrap rate or unplanned machine downtime represents millions of dollars in scrapped raw materials, delayed customer delivery, and warranty liabilities. 

---

## 3. Problem Statement
Currently, shop-floor operators log batch yields, machine downtime, and inspection results into disconnected spreadsheets across disparate plants. Executive leadership lacks a centralized single source of truth, resulting in:
* Delayed detection of scrap rate anomalies across plants.
* Inability to trace component failures to raw material casting suppliers.
* Unmonitored thermal degradation of precision CNC machinery.
* Lack of decision-support tools for plant managers who lack SQL programming skills.

---

## 4. Existing System vs. Proposed System

| Dimension | Existing System | Proposed BI & AI System |
| :--- | :--- | :--- |
| **Data Storage** | Disconnected local Excel sheets per plant | Centralized MySQL Relational Database (Star Schema) |
| **Data Validation** | Manual entry with missing & invalid records | Automated Python 7-step validation pipeline |
| **Query Speed** | Slow manual Excel lookups (VLOOKUP) | Indexed SQL queries executing in milliseconds |
| **Visual Reporting**| Static weekly PDF/PPT summaries | Interactive 6-page Power BI Dashboard with DAX |
| **Insights** | Human guesswork on root causes | Grounded AI Assistant with verified metric evidence |

---

## 5. Project Objectives
1. Build a realistic synthetic manufacturing dataset (>50,000 batches) modeling real automotive engineering patterns.
2. Develop an automated data cleaning and validation pipeline in Python.
3. Design and deploy a normalized 7-table Star Schema in MySQL with strict referential integrity.
4. Construct executive SQL analytical queries utilizing CTEs, Window Functions, and aggregations.
5. Create a professional 6-page Power BI reporting suite with custom DAX business measures.
6. Build a Grounded AI Assistant that translates verified database numbers into strategic business recommendations without hallucinations.

---

## 6. Scope of the System
* **In Scope:** Master data management (Factories, Products, Shifts, Suppliers, Machines), Production transaction tracking, Quality inspection logs, Downtime analytics, Supplier risk scoring, Automated KPI dashboards, and Natural language executive briefings.
* **Out of Scope:** Physical PLC / SCADA hardware sensor deployment; proprietary confidential OEM engineering CAD schematics.

---

## 7. Requirements Analysis
* **Functional Requirements (FR):** System must calculate production efficiency, scrap rate %, supplier risk tier, machine downtime %, and shift variances.
* **Non-Functional Requirements (NFR):** Sub-second query response time, referential integrity across all tables, zero-hallucination response grounding for the AI module.

---

## 8. System Architecture
The platform follows a decoupled 5-tier architecture:
1. **Raw Ingestion Layer:** Batch generation and multi-format CSV handling.
2. **ETL & Cleansing Layer:** Python Pandas pipeline enforcing business validation rules.
3. **Database Layer:** MySQL 8.0 Enterprise Relational Schema with B-Tree indexes.
4. **Analytics & BI Layer:** SQL analytical queries and Power BI Desktop dashboards.
5. **Cognitive AI Layer:** Grounded LLM reasoning engine operating on structured SQL outputs.

---

## 9. Relational Data Model (Star Schema)
* **Master Dimension Tables:** `factories` (5 plants), `products` (8 components), `shifts` (3 shifts), `suppliers` (10 vendors), `machines` (20 units).
* **Transactional Fact Tables:** `production` (55,000 batches, PK: `production_id`), `quality` (55,000 inspection records, PK: `quality_id`).

---

## 10. Methodology & Data Engineering
The project utilizes modular Python scripts:
* `01_generate_master_data.py`: Creates plants, products, suppliers, machines.
* `02_generate_production_data.py`: Simulates 55,000 production transactions across 18 months.
* `03_generate_quality_data.py`: Implements inline quality inspections and defect mode allocations.

---

## 11. Data Cleaning & Validation Pipeline
The `04_data_cleaning.py` script applies 7 validation checks:
1. Duplicate removal on Primary Keys.
2. Datatype casting and date normalization (ISO 8601).
3. Logical constraints (`defective_units <= inspected_units`, `cost >= 0`).
4. String standardization (stripping whitespace, consistent casing).
5. Thermal sensor range clipping (30°C to 120°C).
6. Foreign key relational validation.
7. Clean CSV persistence to `data/cleaned/`.

---

## 12. Relational Database Implementation (MySQL)
Defined in `sql/01_create_database_schema.sql`, the schema utilizes InnoDB tables, primary keys, cascading updates, restricted deletions, and performance indexes on `date`, `factory_id`, `product_id`, `supplier_id`, and `defect_type`.

---

## 13. Executive SQL Analytics
Structured in `sql/02_business_analysis_queries.sql`, the queries answer key operational questions using:
* Window Functions: `RANK() OVER (ORDER BY defect_rate_pct ASC)`
* Analytical CTEs: Month-over-Month growth calculations using `LAG()`
* Pareto defect frequency distribution.

---

## 14. Power BI Interactive Dashboard Suite
Comprises 6 dedicated pages:
1. Executive Overview (Global Volume, Spend, Scrap %)
2. Production Operations (Planned vs. Actual, Efficiency)
3. Quality & Scrap Analysis (Defect Pareto, Shift Heatmaps)
4. Machine Reliability & Downtime (Thermal vs. Downtime Scatter)
5. Supplier Quality & Delivery Risk (Vendor Risk Quadrant)
6. Management Action Matrix (CAPA Prioritization)

---

## 15. Grounded AI Decision-Support Module
The AI Assistant (`ai/ai_business_assistant.py`) operates strictly on verified SQL metrics. Prompt templates in `ai/system_prompts.py` enforce:
* Grounding only on verified numbers.
* Clear distinction between factual evidence and strategic recommendations.
* Explicit admission when requested data is absent.

---

## 16. Experimental Results & Operational Insights
From 55,000 batches (6,884,204 produced units):
* **Overall Defect Rate:** 2.99% (195,410 scrapped components).
* **Plant Variance:** Pune Plant had highest scrap rate (3.82%) vs Mexicali (2.80%).
* **Critical Machine:** MCH_007 generated 385.5 hours downtime at 84.5°C operating temperature.
* **High-Risk Supplier:** SUP_04 (Apex Raw Castings) generated 8.21% scrap and 81.4% OTD.
* **Shift Variance:** Night shift defect rate was 3.65% vs 2.74% on morning shift.
* **Top Defect Modes:** Casting Porosity (26.86%) and Dimensional Out-of-Tolerance (20.45%) constituted 47.31% of total scrap.

---

## 17. Business Benefits & ROI Impact
* **Scrap Reduction:** Eliminating the root cause on SUP_04 and MCH_007 reduces global scrap by an estimated 0.8% ($9.35M annual savings).
* **Downtime Minimization:** Preventive thermal alerts prevent catastrophic CNC spindle seizures.
* **Executive Decision Velocity:** Reduces reporting preparation time from 5 days to real-time.

---

## 18. System Limitations
* Synthetic dataset simulates operational behavior rather than live IoT streaming telemetry.
* AI recommendations require human managerial authorization before execution.

---

## 19. Future Enhancements
* Integration of real-time Kafka streaming for second-by-second vibration sensor telemetry.
* Automated webhook triggers into ERP systems (e.g., SAP/Oracle) to freeze supplier purchase orders upon quality threshold breaches.

---

## 20. Conclusion & References
This system demonstrates how pairing robust data engineering and SQL modeling with interactive Power BI dashboards and grounded AI decision support solves mission-critical quality problems in the automotive industry.

### Key References:
1. Juran, J. M., & Godfrey, A. B. (1999). *Juran's Quality Handbook*. McGraw-Hill.
2. Kimball, R., & Ross, M. (2013). *The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling*. Wiley.
3. Microsoft Power BI DAX Reference Documentation (2024).
