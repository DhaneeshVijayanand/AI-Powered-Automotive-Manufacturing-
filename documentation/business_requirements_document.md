# Business Requirements Document (BRD) & Functional Specification
## Project: AI-Powered Automotive Manufacturing BI & Quality Analysis System
**Target Organization:** Apex TurboTech (Automotive Turbocharger Systems)  
**Author:** Business Systems Analyst / BI Specialist  
**Target Domain:** Automotive Manufacturing & Quality Intelligence  

---

## 1. Executive Summary & Problem Statement

### 1.1 Problem Statement
Apex TurboTech operates 5 global manufacturing facilities producing mission-critical turbocharger components. Currently, operations data is logged in siloed spreadsheets and disparate shop-floor terminals. Plant managers and corporate executive leadership suffer from:
1. **Lack of Centralized Operational Visibility:** 3–5 day lag in identifying high scrap rates across plants.
2. **Unplanned Downtime:** Inability to correlate machine operating temperatures with machine failure and maintenance schedules.
3. **Supplier Quality Blind Spots:** Inability to link final component defect rates back to specific raw casting vendors.
4. **Shift Inefficiencies:** Unmonitored quality variances between morning and night shifts.

### 1.2 Proposed System Objective
To implement an integrated, automated **Business Intelligence and Quality Analysis Platform** that aggregates manufacturing transactions into a central data repository, provides sub-second interactive KPI reporting via Power BI, and integrates an AI Business Assistant to generate verified root-cause explanations and corrective action recommendations.

---

## 2. Stakeholder Matrix

| Stakeholder Role | Primary Need | Key Success Metric |
| :--- | :--- | :--- |
| **Chief Operating Officer (COO)** | Global multi-plant performance benchmarking. | Overall Equipment Efficiency (OEE), Scrap % < 3.0%. |
| **Quality Assurance Director** | Early detection of defect spikes, supplier scrap attribution. | PPM Defect Rate reduction, Vendor Quality Score > 90. |
| **Plant / Production Manager** | Daily batch progress, shift efficiency, machine status. | Planned vs. Actual Production yield > 97%. |
| **Maintenance Lead** | Overheating machine alerts, MTBF (Mean Time Between Failures). | Downtime reduction by 15%. |
| **Procurement Specialist** | Vendor risk scoring based on actual plant floor scrap. | Supplier On-Time Delivery (OTD) > 95%. |

---

## 3. As-Is vs. To-Be Process Flow

### As-Is Process (Manual & Disconnected):
```
[Shop Floor Logbooks] ──► [Manual Excel Entry] ──► [Weekly Email Reports] ──► [Delayed Management Action (5-7 Days Late)]
```

### To-Be Process (Automated & Intelligent):
```
[Automated Sensor & Batch Logs] ──► [Python Cleaning Pipeline] ──► [MySQL Central Data Warehouse]
                                                                                │
                                           ┌────────────────────────────────────┴────────────────────────────────────┐
                                           ▼                                                                         ▼
                              [Power BI Executive Dashboards]                                           [AI Root-Cause Assistant]
                                (Real-time Drill-Downs & KPIs)                                          (Verified Business Action Insights)
```

---

## 4. 10 Comprehensive User Stories & Acceptance Criteria

### US-01: Global Executive Performance Summary
* **User Story:** *As a Chief Operating Officer*, I want an executive KPI dashboard showing total production volume, scrap rate, and operational spend across all 5 plants, so that I can evaluate global performance at a glance.
* **Acceptance Criteria:**
  * Displays Total Produced Units, Total Scrap Units, Defect Rate %, and Spend.
  * Allows filtering by Date Range, Plant, and Product Line.
  * Loads within 2 seconds.

### US-02: Plant Benchmarking & Quality Ranking
* **User Story:** *As a Global Quality Director*, I want to compare defect rates across all 5 factories, so that I can identify low-performing plants and allocate engineering support.
* **Acceptance Criteria:**
  * Displays a ranking table sorting plants from highest to lowest defect rate.
  * Highlights plants exceeding the 3.0% company defect tolerance in visual red alerts.

### US-03: Machine Downtime & Thermal Anomaly Detection
* **User Story:** *As a Plant Maintenance Lead*, I want to monitor machine operating temperatures and downtime hours, so that I can schedule preventive maintenance before catastrophic failure occurs.
* **Acceptance Criteria:**
  * Displays a top 5 downtime ranking for all CNC/grinding machines.
  * Automatically classifies machines with temperature > 75°C as "CRITICAL (Overheating)".

### US-04: Supplier Quality & Scrap Attribution
* **User Story:** *As a Procurement Manager*, I want to evaluate raw material suppliers based on their real plant scrap rate, so that I can renegotiate contracts or audit underperforming vendors.
* **Acceptance Criteria:**
  * Categorizes suppliers into Risk Tiers: High Risk (>5% scrap), Moderate (2.5-5%), Preferred (<2.5%).
  * Correlates vendor on-time delivery (OTD) with quality scores.

### US-05: Shift-Level Disparity Analysis
* **User Story:** *As a Plant Operations Manager*, I want to compare scrap rates between Morning, Evening, and Night shifts, so that I can address nighttime training gaps or supervision shortages.
* **Acceptance Criteria:**
  * Shows produced units, total defects, and defect rate % broken down by shift ID.
  * Highlights any shift that deviates by > 20% from the plant average.

### US-06: Product Line Scrap Pareto Analysis
* **User Story:** *As a Product Quality Engineer*, I want a Pareto 80/20 analysis of defect types for turbocharger components, so that our engineering team tackles the root causes with the highest financial impact.
* **Acceptance Criteria:**
  * Visualizes defect categories sorted descending with cumulative percentage line.
  * Identifies the top 2 defect types contributing to over 50% of scrap volume.

### US-07: Month-over-Month (MoM) Trend Monitoring
* **User Story:** *As a Financial / Business Analyst*, I want to track monthly production costs and scrap rate deltas, so that I can measure the financial return of quality improvement initiatives.
* **Acceptance Criteria:**
  * Displays monthly production volume, monthly scrap %, and month-over-month rate change.

### US-08: Automated Data Cleaning & Relational Validation
* **User Story:** *As a Data Engineer / BI Developer*, I want an automated Python validation script to sanitize raw inputs before database loading, so that invalid records and negative quantities do not corrupt analytics.
* **Acceptance Criteria:**
  * Rejects duplicate batch IDs, negative numbers, and out-of-range timestamps.
  * Verifies foreign key constraints against master dimension tables.

### US-09: Natural Language AI Business Recommendations
* **User Story:** *As a Non-Technical Plant Manager*, I want to query the system in plain English (e.g., "Why did Pune defects spike?"), so that I receive an instant, verified explanation without writing SQL.
* **Acceptance Criteria:**
  * AI must calculate/query verified metrics first before composing the response.
  * AI must cite actual numbers (e.g., "Pune defect rate is 3.82% driven by Machine MCH_007").
  * AI must never hallucinate non-existent figures.

### US-10: Requirement Traceability & Security Governance
* **User Story:** *As an IT Compliance Officer*, I want all database access credentials and API tokens managed securely via environment files (.env), so that sensitive infrastructure is protected.
* **Acceptance Criteria:**
  * `.gitignore` prevents `.env` or credential files from being pushed to public GitHub repositories.

---

## 5. Requirement Traceability Matrix (RTM)

| Req ID | User Story | Component | Target Artifact | Verification Method |
| :--- | :--- | :--- | :--- | :--- |
| **REQ-01** | US-01 (Executive KPIs) | SQL / Power BI | `sql/02_business_analysis_queries.sql` (Q1), Power BI Page 1 | Automated Query Test |
| **REQ-02** | US-02 (Plant Benchmark) | SQL / Power BI | `sql/02_business_analysis_queries.sql` (Q2), Power BI Page 2 | Benchmarking Matrix |
| **REQ-03** | US-03 (Machine Downtime) | SQL / Power BI | `sql/02_business_analysis_queries.sql` (Q3), Power BI Page 4 | Scatter Plot & Table |
| **REQ-04** | US-04 (Supplier Risk) | SQL / Power BI | `sql/02_business_analysis_queries.sql` (Q4), Power BI Page 5 | Quadrant Risk Chart |
| **REQ-05** | US-05 (Shift Disparity) | SQL / Power BI | `sql/02_business_analysis_queries.sql` (Q5), Power BI Page 3 | Shift Breakdown Grid |
| **REQ-06** | US-06 (Pareto Analysis) | SQL / Power BI | `sql/02_business_analysis_queries.sql` (Q7), Power BI Page 3 | Pareto Curve Check |
| **REQ-07** | US-07 (MoM Trends) | SQL / Power BI | `sql/02_business_analysis_queries.sql` (Q8), Power BI Page 2 | Monthly Trend Check |
| **REQ-08** | US-08 (Data Pipeline) | Python / Pandas | `python/04_data_cleaning.py` | Automated Pipeline Run |
| **REQ-09** | US-09 (AI Assistant) | Python / LLM API | `ai/ai_business_assistant.py` | Verified Fact Check |
| **REQ-10** | US-10 (Security) | Git / Environment | `.gitignore`, `.env.example` | Repository Audit |
