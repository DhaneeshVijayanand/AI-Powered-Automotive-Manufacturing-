"""
=============================================================================
Module: 02_generate_production_data.py
Project: AI-Powered Automotive Manufacturing BI & Quality Analysis System
Description: Generates 55,000+ realistic production records across 18 months
             with consistent foreign keys and business patterns.
=============================================================================
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Define directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")

print("[INFO] Loading Master Data for Production Simulation...")

# Load master tables
df_factories = pd.read_csv(os.path.join(RAW_DATA_DIR, "factories.csv"))
df_products = pd.read_csv(os.path.join(RAW_DATA_DIR, "products.csv"))
df_shifts = pd.read_csv(os.path.join(RAW_DATA_DIR, "shifts.csv"))
df_machines = pd.read_csv(os.path.join(RAW_DATA_DIR, "machines.csv"))

# Map machines to their respective factories to guarantee relational integrity
factory_machines = {
    fac_id: df_machines[df_machines["factory_id"] == fac_id]["machine_id"].tolist()
    for fac_id in df_factories["factory_id"]
}

# Base unit costs by product category for realistic financial calculations
base_product_cost = {
    "PRD_01": 280.0,  # Titanium Turbine Wheel (Aerospace grade)
    "PRD_02": 190.0,  # Billet Compressor Wheel
    "PRD_03": 140.0,  # Cast Iron Bearing Housing
    "PRD_04": 220.0,  # Nickel Alloy Turbine Housing
    "PRD_05": 110.0,  # Aluminum Compressor Housing
    "PRD_06": 95.0,   # Wastegate Actuator
    "PRD_07": 160.0,  # VNT Nozzle Ring
    "PRD_08": 85.0,   # Ball Bearing Unit
}

print("[INFO] Generating 55,000 Production Batch Records...")

start_date = datetime(2025, 1, 1)
end_date = datetime(2026, 6, 30)
days_range = (end_date - start_date).days

records = []
total_target_records = 55000

# Probabilistic weights for factories (Bangalore and Mexicali are larger capacity)
factory_weights = [0.24, 0.18, 0.26, 0.14, 0.18]
product_ids = df_products["product_id"].tolist()
shift_ids = df_shifts["shift_id"].tolist()

for i in range(1, total_target_records + 1):
    prod_id = f"PRD_BATCH_{i:06d}"
    
    # Random date within timeframe
    random_days = np.random.randint(0, days_range + 1)
    batch_date = (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")
    
    # Select factory according to capacity weight
    factory_id = np.random.choice(df_factories["factory_id"], p=factory_weights)
    
    # Select machine that physically exists in THAT factory
    valid_machines = factory_machines[factory_id]
    machine_id = np.random.choice(valid_machines)
    
    # Select product and shift
    product_id = np.random.choice(product_ids)
    shift_id = np.random.choice(shift_ids, p=[0.38, 0.35, 0.27]) # Morning/Evening/Night
    
    # Planned units (batch sizing)
    planned_units = int(np.random.choice([80, 100, 120, 150, 200, 250], p=[0.15, 0.25, 0.25, 0.20, 0.10, 0.05]))
    
    # Calculate produced units based on realistic operational behavior:
    # 1. Base efficiency is ~97-99%
    # 2. Night shift (SH_03) has slightly lower yield (down 2-3%)
    # 3. Problem Machine (MCH_007 in Pune) has occasional drops due to vibration/temperature
    efficiency_factor = np.random.uniform(0.95, 1.00)
    
    if shift_id == "SH_03":
        efficiency_factor -= np.random.uniform(0.015, 0.04)
        
    if machine_id == "MCH_007":
        efficiency_factor -= np.random.uniform(0.04, 0.09)
        
    produced_units = max(int(np.round(planned_units * efficiency_factor)), int(planned_units * 0.70))
    
    # Production cost = (Base Cost * Produced Units) + Machine Overhead + Shift Premium
    unit_base = base_product_cost[product_id]
    shift_premium = 1.12 if shift_id == "SH_03" else (1.05 if shift_id == "SH_02" else 1.0)
    machine_wear_cost = 1.15 if machine_id == "MCH_007" else 1.0
    
    total_cost = round(produced_units * unit_base * shift_premium * machine_wear_cost * np.random.uniform(0.98, 1.03), 2)
    
    records.append({
        "production_id": prod_id,
        "date": batch_date,
        "factory_id": factory_id,
        "product_id": product_id,
        "machine_id": machine_id,
        "shift_id": shift_id,
        "planned_units": planned_units,
        "produced_units": produced_units,
        "production_cost": total_cost
    })

df_production = pd.DataFrame(records)
# Sort chronologically
df_production = df_production.sort_values("date").reset_index(drop=True)

output_file = os.path.join(RAW_DATA_DIR, "production.csv")
df_production.to_csv(output_file, index=False)

print(f"\n[SUCCESS] Generated production.csv with {len(df_production):,} records!")
print(f"Total Produced Units: {df_production['produced_units'].sum():,}")
print(f"Total Production Cost: ${df_production['production_cost'].sum():,.2f}")
