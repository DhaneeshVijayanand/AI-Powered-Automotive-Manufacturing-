# Executive Presentation Deck & 5-Minute Verbal Presentation Script
## AI-Powered Automotive Manufacturing BI & Quality Analysis System

---

## 15-Slide Presentation Deck Outline

### Slide 1: Title & Author
* **Title:** AI-Powered Automotive Manufacturing BI & Quality Analysis System
* **Subtitle:** An Enterprise Data Engineering, Power BI, and Grounded AI Decision-Support Platform
* **Presenter:** B.Tech CSBS Student (Business Analyst / BI Specialist Aspirant)
* **Domain Focus:** Tier-1 Automotive Component Manufacturing (Turbocharger Systems)

### Slide 2: Industry Problem Statement
* Disparate shop-floor Excel logbooks across global manufacturing plants.
* Unplanned CNC machine downtime costing thousands of dollars per hour.
* Inability to correlate final assembly scrap with raw casting suppliers.
* 3–5 day lag in corporate executive operational visibility.

### Slide 3: Project Objectives
* Ingest and clean 55,000+ manufacturing batches across 5 plants.
* Implement a normalized Star Schema in MySQL with strict referential integrity.
* Build a 6-page interactive Power BI dashboard suite with custom DAX KPIs.
* Develop a Grounded AI Business Assistant that explains verified metrics without hallucination.

### Slide 4: System Architecture
* Visual flow: Raw CSVs ➔ Python Cleaning Pipeline ➔ MySQL Star Schema ➔ SQL/Power BI ➔ Grounded AI Assistant.

### Slide 5: The Manufacturing Data Model
* **Fact Tables:** `production` (55k batches), `quality` (55k inspection records).
* **Dimension Tables:** `factories`, `products`, `shifts`, `suppliers`, `machines`.

### Slide 6: Automated Data Cleaning & ETL
* 7-step validation pipeline: Primary key deduplication, ISO date normalization, logical bounds checking (`defects <= inspected`), and foreign key validation.

### Slide 7: Core Business Intelligence Metrics
* Overall Defect Rate %, Production Efficiency %, Machine Downtime %, Vendor Quality Scorecard, and Shift Disparity Index.

### Slide 8: Executive Dashboard — Multi-Plant Benchmarking
* Demonstrating Power BI Page 1 & 2: Volume trends, efficiency comparison, and identifying Pune Plant's 3.82% defect rate anomaly.

### Slide 9: Root-Cause Scrap & Defect Pareto Analysis
* Demonstrating Power BI Page 3: Defect distribution showing Casting Porosity (26.86%) and Dimensional Variance (20.45%) as primary scrap drivers.

### Slide 10: Predictive Machine Downtime & Thermal Stress
* Demonstrating Power BI Page 4: Thermal correlation plot showing Machine MCH_007 in Pune operating at 84.5°C with 385.5 hours downtime.

### Slide 11: Supplier Procurement Risk Matrix
* Demonstrating Power BI Page 5: Quadrant risk analysis identifying Apex Raw Castings (`SUP_04`) delivering 8.21% scrap and failing OTD commitments (81.4%).

### Slide 12: Zero-Hallucination AI Business Assistant
* Architecture of the AI reasoning module: SQL verification first ➔ JSON grounding payload ➔ Structured executive briefing generation.

### Slide 13: Business Benefits & Estimated Financial ROI
* Potential to reduce global scrap by 0.8%, generating an estimated **$9.35M annual savings** in raw material and rework costs.

### Slide 14: System Limitations & Future Scope
* Future expansion: Live IoT Kafka streaming for vibration telemetry; automated ERP webhook integration for supplier PO holds.

### Slide 15: Conclusion & Key Takeaways
* Demonstrates the complete synergy of Computer Science and Business Systems: turning raw manufacturing logs into actionable business ROI.

---

## 5-Minute Verbal Presentation Script (Word-for-Word)

> *"Good morning, respected panel and interviewers.*
>
> *Today, I am excited to present my major project: the **AI-Powered Automotive Manufacturing Business Intelligence & Quality Analysis System**.*
>
> *In precision automotive manufacturing—such as turbocharger components produced by companies like Garrett Motion—components operate at extreme temperatures up to 1050°C and rotational speeds exceeding 250,000 RPM. In this industry, quality tolerances are measured in micrometers. A 1% increase in scrap rate or an unexpected CNC breakdown costs millions of dollars.*
>
> *However, many manufacturing organizations still struggle with fragmented data: production logs, machine maintenance sheets, and supplier quality scores are trapped in disconnected spreadsheets. Management only discovers quality crises days after they happen.*
>
> *To solve this, I designed and developed an end-to-end analytics platform.*
>
> *First, I simulated 55,000 realistic production and quality inspection records across 5 global manufacturing plants—spanning 8 turbocharger products, 20 CNC machines, and 10 suppliers.*
>
> *Second, using Python and Pandas, I built an automated 7-step data cleaning pipeline that enforces relational integrity, removes duplicate entries, standardizes date formats, and validates physical engineering bounds.*
>
> *Third, I modeled this clean data into a 7-table Star Schema in a MySQL database, indexing critical dimensions to enable sub-second analytical aggregations.*
>
> *Fourth, using advanced SQL and Power BI with custom DAX formulas, I answered critical management questions and built a 6-page interactive executive dashboard. Through this analysis, I uncovered three critical operational bottlenecks:*
> *1. The Pune manufacturing plant had the highest scrap rate at 3.82% compared to the global 2.80% benchmark.*
> *2. Drilling down into machines revealed that Machine MCH_007 in Pune had 385.5 hours of downtime and was overheating at 84.5°C.*
> *3. In supplier analytics, Supplier SUP_04 was delivering raw castings with an 8.21% defect rate, directly explaining why Casting Porosity was our top defect mode.*
>
> *Finally, to help non-technical plant managers make fast decisions, I built a **Grounded AI Business Assistant**. Unlike standard chatbots that hallucinate numbers, my AI engine calculates verified SQL metrics first and passes them as a structured grounding context to the language model. The AI provides structured executive briefings, clearly separating verified facts from strategic Corrective and Preventive Actions (CAPA).*
>
> *This project embodies the core of my CSBS training—combining data engineering, relational databases, business analysis, and artificial intelligence to deliver measurable financial value.*
>
> *Thank you, and I am now ready for your questions."*
