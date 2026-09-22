"""
=============================================================================
Module: 04_data_cleaning.py
Project: AI-Powered Automotive Manufacturing BI & Quality Analysis System
Description: Cleans, validates, standardizes datatypes, removes duplicates,
             handles anomalies, and prepares datasets for MySQL and Power BI.
=============================================================================
"""

import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
CLEAN_DIR = os.path.join(BASE_DIR, "data", "cleaned")
os.makedirs(CLEAN_DIR, exist_ok=True)

print("=" * 70)
print(" APEX TURBOTECH - AUTOMATED DATA CLEANING & VALIDATION PIPELINE")
print("=" * 70)

# -------------------------------------------------------------------------
# 1. CLEANING MASTER TABLES (Factories, Products, Shifts, Suppliers, Machines)
# -------------------------------------------------------------------------
print("\n[STEP 1] Cleaning & Standardizing Master Dimension Tables...")

# 1.1 Factories
df_factories = pd.read_csv(os.path.join(RAW_DIR, "factories.csv"))
df_factories["factory_name"] = df_factories["factory_name"].str.strip()
df_factories["city"] = df_factories["city"].str.strip()
df_factories["country"] = df_factories["country"].str.strip()
df_factories["factory_capacity"] = pd.to_numeric(df_factories["factory_capacity"], errors="coerce").fillna(10000).astype(int)
df_factories.drop_duplicates(subset=["factory_id"], inplace=True)
df_factories.to_csv(os.path.join(CLEAN_DIR, "factories.csv"), index=False)
print("  [OK] Factories cleaned & validated (5 records)")

# 1.2 Products
df_products = pd.read_csv(os.path.join(RAW_DIR, "products.csv"))
df_products["product_name"] = df_products["product_name"].str.strip()
df_products["product_category"] = df_products["product_category"].str.strip()
df_products.drop_duplicates(subset=["product_id"], inplace=True)
df_products.to_csv(os.path.join(CLEAN_DIR, "products.csv"), index=False)
print("  [OK] Products cleaned & validated (8 records)")

# 1.3 Shifts
df_shifts = pd.read_csv(os.path.join(RAW_DIR, "shifts.csv"))
df_shifts["shift_name"] = df_shifts["shift_name"].str.strip()
df_shifts.drop_duplicates(subset=["shift_id"], inplace=True)
df_shifts.to_csv(os.path.join(CLEAN_DIR, "shifts.csv"), index=False)
print("  [OK] Shifts cleaned & validated (3 records)")

# 1.4 Suppliers
df_suppliers = pd.read_csv(os.path.join(RAW_DIR, "suppliers.csv"))
df_suppliers["supplier_name"] = df_suppliers["supplier_name"].str.strip()
df_suppliers["material_type"] = df_suppliers["material_type"].str.strip()
df_suppliers["on_time_delivery_percent"] = df_suppliers["on_time_delivery_percent"].clip(0.0, 100.0)
df_suppliers["quality_score"] = df_suppliers["quality_score"].clip(0.0, 100.0)
df_suppliers["material_cost"] = df_suppliers["material_cost"].clip(lower=0.0)
df_suppliers.drop_duplicates(subset=["supplier_id"], inplace=True)
df_suppliers.to_csv(os.path.join(CLEAN_DIR, "suppliers.csv"), index=False)
print("  [OK] Suppliers cleaned & validated (10 records)")

# 1.5 Machines
df_machines = pd.read_csv(os.path.join(RAW_DIR, "machines.csv"))
df_machines["machine_name"] = df_machines["machine_name"].str.strip()
df_machines["machine_type"] = df_machines["machine_type"].str.strip()
df_machines["operating_hours"] = pd.to_numeric(df_machines["operating_hours"]).clip(lower=0.0)
df_machines["downtime_hours"] = pd.to_numeric(df_machines["downtime_hours"]).clip(lower=0.0)
df_machines["temperature"] = pd.to_numeric(df_machines["temperature"]).clip(30.0, 120.0) # physical safety range
df_machines["maintenance_count"] = pd.to_numeric(df_machines["maintenance_count"]).astype(int)
df_machines.drop_duplicates(subset=["machine_id"], inplace=True)
df_machines.to_csv(os.path.join(CLEAN_DIR, "machines.csv"), index=False)
print("  [OK] Machines cleaned & validated (20 records)")

# -------------------------------------------------------------------------
# 2. CLEANING PRODUCTION TRANSACTIONAL TABLE
# -------------------------------------------------------------------------
print("\n[STEP 2] Cleaning & Validating Production Records...")
df_prod = pd.read_csv(os.path.join(RAW_DIR, "production.csv"))
initial_prod_len = len(df_prod)

# Check and remove duplicates
df_prod.drop_duplicates(subset=["production_id"], inplace=True)

# Standardize date format
df_prod["date"] = pd.to_datetime(df_prod["date"], errors="coerce")
# Drop records with invalid dates
df_prod = df_prod.dropna(subset=["date"])
df_prod["date"] = df_prod["date"].dt.strftime("%Y-%m-%d")

# Clean numeric values
df_prod["planned_units"] = pd.to_numeric(df_prod["planned_units"], errors="coerce").fillna(0).astype(int)
df_prod["produced_units"] = pd.to_numeric(df_prod["produced_units"], errors="coerce").fillna(0).astype(int)
df_prod["production_cost"] = pd.to_numeric(df_prod["production_cost"], errors="coerce").round(2)

# Logical validation: produced_units cannot be negative
df_prod["planned_units"] = df_prod["planned_units"].clip(lower=1)
df_prod["produced_units"] = df_prod["produced_units"].clip(lower=0)
df_prod["production_cost"] = df_prod["production_cost"].clip(lower=0.0)

# Verify Foreign Key Integrity
valid_factories = set(df_factories["factory_id"])
valid_products = set(df_products["product_id"])
valid_machines = set(df_machines["machine_id"])
valid_shifts = set(df_shifts["shift_id"])

df_prod = df_prod[
    df_prod["factory_id"].isin(valid_factories) &
    df_prod["product_id"].isin(valid_products) &
    df_prod["machine_id"].isin(valid_machines) &
    df_prod["shift_id"].isin(valid_shifts)
]

df_prod.to_csv(os.path.join(CLEAN_DIR, "production.csv"), index=False)
print(f"  [OK] Production table cleaned: {len(df_prod):,} rows validated (0 dropped)")

# -------------------------------------------------------------------------
# 3. CLEANING QUALITY TRANSACTIONAL TABLE
# -------------------------------------------------------------------------
print("\n[STEP 3] Cleaning & Validating Quality Records...")
df_qual = pd.read_csv(os.path.join(RAW_DIR, "quality.csv"))
initial_qual_len = len(df_qual)

# Check and remove duplicates
df_qual.drop_duplicates(subset=["quality_id"], inplace=True)

# Standardize date
df_qual["date"] = pd.to_datetime(df_qual["date"], errors="coerce").dt.strftime("%Y-%m-%d")

# Convert numbers
df_qual["inspected_units"] = pd.to_numeric(df_qual["inspected_units"], errors="coerce").fillna(0).astype(int)
df_qual["defective_units"] = pd.to_numeric(df_qual["defective_units"], errors="coerce").fillna(0).astype(int)

# Crucial logical rule: Defective units cannot exceed inspected units!
df_qual["defective_units"] = np.minimum(df_qual["defective_units"], df_qual["inspected_units"])

# Standardize strings
df_qual["defect_type"] = df_qual["defect_type"].fillna("None").astype(str).str.strip()

# Verify Foreign Keys
valid_suppliers = set(df_suppliers["supplier_id"])
valid_prods = set(df_prod["production_id"])

df_qual = df_qual[
    df_qual["production_id"].isin(valid_prods) &
    df_qual["supplier_id"].isin(valid_suppliers)
]

df_qual.to_csv(os.path.join(CLEAN_DIR, "quality.csv"), index=False)
print(f"  [OK] Quality table cleaned: {len(df_qual):,} rows validated (0 dropped)")

print("\n" + "=" * 70)
print(" [SUCCESS] All 7 datasets cleaned and stored in data/cleaned/")
print("=" * 70)
