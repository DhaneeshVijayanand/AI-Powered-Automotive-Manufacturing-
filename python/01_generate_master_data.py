"""
=============================================================================
Module: 01_generate_master_data.py
Project: AI-Powered Automotive Manufacturing BI & Quality Analysis System
Description: Generates master/dimension tables (Factories, Products, Shifts, 
             Suppliers, Machines) for Apex TurboTech.
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
os.makedirs(RAW_DATA_DIR, exist_ok=True)

print("[INFO] Generating Master Data for Apex TurboTech...")

# -------------------------------------------------------------------------
# 1. FACTORIES (5 Manufacturing Plants)
# -------------------------------------------------------------------------
factories_data = [
    {"factory_id": "FAC_01", "factory_name": "Bangalore Plant", "city": "Bangalore", "country": "India", "factory_capacity": 15000},
    {"factory_id": "FAC_02", "factory_name": "Pune Plant", "city": "Pune", "country": "India", "factory_capacity": 12000},
    {"factory_id": "FAC_03", "factory_name": "Mexicali Plant", "city": "Mexicali", "country": "Mexico", "factory_capacity": 18000},
    {"factory_id": "FAC_04", "factory_name": "Bucharest Plant", "city": "Bucharest", "country": "Romania", "factory_capacity": 14000},
    {"factory_id": "FAC_05", "factory_name": "Wuhan Plant", "city": "Wuhan", "country": "China", "factory_capacity": 16000},
]
df_factories = pd.DataFrame(factories_data)
df_factories.to_csv(os.path.join(RAW_DATA_DIR, "factories.csv"), index=False)
print(f" -> Generated factories.csv ({len(df_factories)} records)")

# -------------------------------------------------------------------------
# 2. PRODUCTS (8 Turbocharger Components)
# -------------------------------------------------------------------------
products_data = [
    {"product_id": "PRD_01", "product_name": "Titanium Turbine Wheel", "product_category": "Rotor Assemblies"},
    {"product_id": "PRD_02", "product_name": "Billet Compressor Wheel", "product_category": "Rotor Assemblies"},
    {"product_id": "PRD_03", "product_name": "Cast Iron Bearing Housing", "product_category": "Center Housings"},
    {"product_id": "PRD_04", "product_name": "Nickel Alloy Turbine Housing", "product_category": "Housings"},
    {"product_id": "PRD_05", "product_name": "Aluminum Compressor Housing", "product_category": "Housings"},
    {"product_id": "PRD_06", "product_name": "Electronic Wastegate Actuator", "product_category": "Actuation & Controls"},
    {"product_id": "PRD_07", "product_name": "VNT Nozzle Ring Assembly", "product_category": "Variable Geometry"},
    {"product_id": "PRD_08", "product_name": "Dual Ceramic Ball Bearing Unit", "product_category": "Bearings & Bushings"},
]
df_products = pd.DataFrame(products_data)
df_products.to_csv(os.path.join(RAW_DATA_DIR, "products.csv"), index=False)
print(f" -> Generated products.csv ({len(df_products)} records)")

# -------------------------------------------------------------------------
# 3. SHIFTS (3 Operating Shifts)
# -------------------------------------------------------------------------
shifts_data = [
    {"shift_id": "SH_01", "shift_name": "Morning Shift", "start_time": "06:00:00", "end_time": "14:00:00"},
    {"shift_id": "SH_02", "shift_name": "Evening Shift", "start_time": "14:00:00", "end_time": "22:00:00"},
    {"shift_id": "SH_03", "shift_name": "Night Shift", "start_time": "22:00:00", "end_time": "06:00:00"},
]
df_shifts = pd.DataFrame(shifts_data)
df_shifts.to_csv(os.path.join(RAW_DATA_DIR, "shifts.csv"), index=False)
print(f" -> Generated shifts.csv ({len(df_shifts)} records)")

# -------------------------------------------------------------------------
# 4. SUPPLIERS (10 Specialized Material Vendors)
# -------------------------------------------------------------------------
# Note: SUP_04 (Apex Castings Ltd) is intentionally assigned lower quality score
# and lower on-time delivery to simulate realistic supplier risk for analysis.
suppliers_data = [
    {"supplier_id": "SUP_01", "supplier_name": "Precision Alloys Corp", "material_type": "Titanium Ingot", "delivery_days": 5, "on_time_delivery_percent": 96.5, "quality_score": 94.2, "material_cost": 450.0},
    {"supplier_id": "SUP_02", "supplier_name": "Aerospace Forgings Ltd", "material_type": "Billet Aluminum", "delivery_days": 4, "on_time_delivery_percent": 95.0, "quality_score": 92.8, "material_cost": 210.0},
    {"supplier_id": "SUP_03", "supplier_name": "Global Foundry Solutions", "material_type": "Ductile Cast Iron", "delivery_days": 7, "on_time_delivery_percent": 92.3, "quality_score": 89.5, "material_cost": 135.0},
    {"supplier_id": "SUP_04", "supplier_name": "Apex Raw Castings Ltd", "material_type": "Nickel-Resist Alloy", "delivery_days": 10, "on_time_delivery_percent": 81.4, "quality_score": 76.5, "material_cost": 310.0}, # Risk Supplier
    {"supplier_id": "SUP_05", "supplier_name": "EuroMetals Casting SA", "material_type": "Stainless Steel", "delivery_days": 6, "on_time_delivery_percent": 94.8, "quality_score": 93.1, "material_cost": 280.0},
    {"supplier_id": "SUP_06", "supplier_name": "DynoActuators GmbH", "material_type": "Actuator Components", "delivery_days": 5, "on_time_delivery_percent": 97.2, "quality_score": 96.0, "material_cost": 175.0},
    {"supplier_id": "SUP_07", "supplier_name": "Nippon Micro Vanes KK", "material_type": "High-Temp Inconel", "delivery_days": 8, "on_time_delivery_percent": 93.5, "quality_score": 91.4, "material_cost": 390.0},
    {"supplier_id": "SUP_08", "supplier_name": "Ceramic Dynamics Inc", "material_type": "Silicon Nitride Balls", "delivery_days": 4, "on_time_delivery_percent": 98.1, "quality_score": 97.5, "material_cost": 120.0},
    {"supplier_id": "SUP_09", "supplier_name": "Pacific Precision Cast", "material_type": "Die-Cast Aluminum", "delivery_days": 6, "on_time_delivery_percent": 91.0, "quality_score": 87.0, "material_cost": 160.0},
    {"supplier_id": "SUP_10", "supplier_name": "Vortex Fasteners & Seals", "material_type": "High-Pressure Seals", "delivery_days": 3, "on_time_delivery_percent": 99.0, "quality_score": 98.2, "material_cost": 45.0},
]
df_suppliers = pd.DataFrame(suppliers_data)
df_suppliers.to_csv(os.path.join(RAW_DATA_DIR, "suppliers.csv"), index=False)
print(f" -> Generated suppliers.csv ({len(df_suppliers)} records)")

# -------------------------------------------------------------------------
# 5. MACHINES (20 High-Precision CNC & Milling Units across Factories)
# -------------------------------------------------------------------------
# 4 machines per factory (20 total)
machine_types = [
    ("5-Axis CNC Milling Center", 68.5),
    ("CNC Precision Lathe", 62.0),
    ("High-Speed Dynamic Balancer", 55.0),
    ("Automated CMM Quality Scanner", 48.0),
]

machines_data = []
machine_idx = 1

for factory in factories_data:
    fac_id = factory["factory_id"]
    for m_type, base_temp in machine_types:
        m_id = f"MCH_{machine_idx:03d}"
        
        # Realistic initial baseline metrics
        # Machine MCH_007 in Pune (FAC_02) is designed with high downtime and higher temp for root-cause analysis
        if m_id == "MCH_007":
            operating_hours = 3100.0
            downtime_hours = 385.5      # Unusually high downtime
            temperature = 84.5          # Running significantly hotter
            maintenance_count = 14      # Frequent breakdowns
        else:
            operating_hours = round(np.random.uniform(2800, 3600), 1)
            downtime_hours = round(np.random.uniform(35, 110), 1)
            temperature = round(base_temp + np.random.uniform(-3.5, 4.0), 1)
            maintenance_count = int(np.random.randint(1, 6))
            
        machines_data.append({
            "machine_id": m_id,
            "factory_id": fac_id,
            "machine_name": f"{factory['city']} {m_type} #{((machine_idx-1)%4)+1}",
            "machine_type": m_type,
            "operating_hours": operating_hours,
            "downtime_hours": downtime_hours,
            "temperature": temperature,
            "maintenance_count": maintenance_count
        })
        machine_idx += 1

df_machines = pd.DataFrame(machines_data)
df_machines.to_csv(os.path.join(RAW_DATA_DIR, "machines.csv"), index=False)
print(f" -> Generated machines.csv ({len(df_machines)} records)")

print("\n[SUCCESS] Master data generation complete! Files saved to data/raw/")
