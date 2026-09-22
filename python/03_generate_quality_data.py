"""
=============================================================================
Module: 03_generate_quality_data.py
Project: AI-Powered Automotive Manufacturing BI & Quality Analysis System
Description: Generates 55,000 corresponding quality inspection records with 
             relational integrity, realistic defect distributions, and 
             identifiable root-cause patterns.
=============================================================================
"""

import os
import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Define directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")

print("[INFO] Loading Production and Supplier Data...")

df_production = pd.read_csv(os.path.join(RAW_DATA_DIR, "production.csv"))
df_suppliers = pd.read_csv(os.path.join(RAW_DATA_DIR, "suppliers.csv"))

supplier_ids = df_suppliers["supplier_id"].tolist()

# Realistic defect types in precision turbocharger manufacturing
defect_types_general = [
    "Dimensional Out-of-Tolerance",
    "Dynamic Unbalance",
    "Thread / Fastener Defect",
    "Rough Surface Finish",
    "Surface Micro-Crack",
    "Casting Porosity / Blowholes"
]

quality_records = []
total_batches = len(df_production)

print(f"[INFO] Generating Quality Inspection Data for {total_batches:,} Batches...")

for idx, row in df_production.iterrows():
    quality_id = f"QLT_{idx+1:06d}"
    prod_id = row["production_id"]
    batch_date = row["date"]
    fac_id = row["factory_id"]
    prd_id = row["product_id"]
    mch_id = row["machine_id"]
    shf_id = row["shift_id"]
    produced_units = int(row["produced_units"])
    
    # 100% or high-percentage inline inspection (typical for turbo safety components)
    inspected_units = int(np.round(produced_units * np.random.uniform(0.90, 1.00)))
    
    # Assign supplier based on product category requirements
    # SUP_04 provides raw castings for PRD_03, PRD_04, PRD_05
    if prd_id in ["PRD_03", "PRD_04", "PRD_05"]:
        supplier_id = np.random.choice(["SUP_03", "SUP_04", "SUP_05", "SUP_09"], p=[0.25, 0.35, 0.25, 0.15])
    elif prd_id in ["PRD_01", "PRD_02"]:
        supplier_id = np.random.choice(["SUP_01", "SUP_02"], p=[0.55, 0.45])
    elif prd_id == "PRD_06":
        supplier_id = "SUP_06"
    elif prd_id == "PRD_07":
        supplier_id = "SUP_07"
    else:
        supplier_id = np.random.choice(["SUP_08", "SUP_10"], p=[0.60, 0.40])
        
    # ---------------------------------------------------------------------
    # Defect Rate Calculation with Realistic Embedded Patterns:
    # 1. Base defect rate: ~1.5% to 2.2%
    # 2. Risk Supplier (SUP_04): +4.5% to 7.0% defect surge (Porosity & Cracks)
    # 3. Problem Machine (MCH_007): +3.0% to 5.5% defect surge (Dimensional & Finish)
    # 4. Night Shift (SH_03): +0.8% defect surge
    # ---------------------------------------------------------------------
    base_rate = np.random.uniform(0.012, 0.024)
    
    if supplier_id == "SUP_04":
        base_rate += np.random.uniform(0.045, 0.075)
        
    if mch_id == "MCH_007":
        base_rate += np.random.uniform(0.030, 0.055)
        
    if shf_id == "SH_03":
        base_rate += np.random.uniform(0.005, 0.012)
        
    # Calculate defective units (capped at inspected units)
    defective_units = int(np.round(inspected_units * base_rate))
    defective_units = min(defective_units, inspected_units)
    
    # Assign Defect Type based on root-cause pattern
    if defective_units == 0:
        defect_type = "None"
    else:
        if supplier_id == "SUP_04":
            # High probability of casting flaws
            defect_type = np.random.choice(
                ["Casting Porosity / Blowholes", "Surface Micro-Crack", "Dimensional Out-of-Tolerance"],
                p=[0.55, 0.30, 0.15]
            )
        elif mch_id == "MCH_007":
            # High probability of thermal / dimensional machining errors
            defect_type = np.random.choice(
                ["Dimensional Out-of-Tolerance", "Rough Surface Finish", "Thread / Fastener Defect"],
                p=[0.50, 0.35, 0.15]
            )
        elif prd_id in ["PRD_01", "PRD_02"]:
            # Rotating parts prone to balancing variance
            defect_type = np.random.choice(
                ["Dynamic Unbalance", "Dimensional Out-of-Tolerance", "Rough Surface Finish"],
                p=[0.50, 0.30, 0.20]
            )
        else:
            defect_type = np.random.choice(defect_types_general)
            
    quality_records.append({
        "quality_id": quality_id,
        "date": batch_date,
        "production_id": prod_id,
        "product_id": prd_id,
        "factory_id": fac_id,
        "machine_id": mch_id,
        "supplier_id": supplier_id,
        "inspected_units": inspected_units,
        "defective_units": defective_units,
        "defect_type": defect_type
    })

df_quality = pd.DataFrame(quality_records)
output_file = os.path.join(RAW_DATA_DIR, "quality.csv")
df_quality.to_csv(output_file, index=False)

print(f"\n[SUCCESS] Generated quality.csv with {len(df_quality):,} records!")
print(f"Total Inspected Units: {df_quality['inspected_units'].sum():,}")
print(f"Total Defective Units: {df_quality['defective_units'].sum():,}")
overall_defect_rate = (df_quality['defective_units'].sum() / df_quality['inspected_units'].sum()) * 100
print(f"Overall Manufacturing Defect Rate: {overall_defect_rate:.2f}%")
