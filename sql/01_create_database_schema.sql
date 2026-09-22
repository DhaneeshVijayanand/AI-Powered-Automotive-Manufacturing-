-- =============================================================================
-- Database Schema: Apex TurboTech Manufacturing BI & Quality System
-- Database Engine: MySQL 8.0+
-- File: sql/01_create_database_schema.sql
-- =============================================================================

-- Step 1: Create and select the database
CREATE DATABASE IF NOT EXISTS apex_manufacturing_db;
USE apex_manufacturing_db;

-- Step 2: Drop existing tables in reverse dependency order (to avoid FK errors)
DROP TABLE IF EXISTS quality;
DROP TABLE IF EXISTS production;
DROP TABLE IF EXISTS machines;
DROP TABLE IF EXISTS suppliers;
DROP TABLE IF EXISTS shifts;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS factories;

-- =============================================================================
-- MASTER / DIMENSION TABLES
-- =============================================================================

-- 1. FACTORIES
CREATE TABLE factories (
    factory_id VARCHAR(10) NOT NULL,
    factory_name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    factory_capacity INT NOT NULL,
    PRIMARY KEY (factory_id)
) ENGINE=InnoDB;

-- 2. PRODUCTS
CREATE TABLE products (
    product_id VARCHAR(10) NOT NULL,
    product_name VARCHAR(100) NOT NULL,
    product_category VARCHAR(50) NOT NULL,
    PRIMARY KEY (product_id)
) ENGINE=InnoDB;

-- 3. SHIFTS
CREATE TABLE shifts (
    shift_id VARCHAR(10) NOT NULL,
    shift_name VARCHAR(50) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    PRIMARY KEY (shift_id)
) ENGINE=InnoDB;

-- 4. SUPPLIERS
CREATE TABLE suppliers (
    supplier_id VARCHAR(10) NOT NULL,
    supplier_name VARCHAR(100) NOT NULL,
    material_type VARCHAR(100) NOT NULL,
    delivery_days INT NOT NULL,
    on_time_delivery_percent DECIMAL(5,2) NOT NULL,
    quality_score DECIMAL(5,2) NOT NULL,
    material_cost DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (supplier_id)
) ENGINE=InnoDB;

-- 5. MACHINES
CREATE TABLE machines (
    machine_id VARCHAR(10) NOT NULL,
    factory_id VARCHAR(10) NOT NULL,
    machine_name VARCHAR(100) NOT NULL,
    machine_type VARCHAR(100) NOT NULL,
    operating_hours DECIMAL(10,2) NOT NULL,
    downtime_hours DECIMAL(10,2) NOT NULL,
    temperature DECIMAL(5,2) NOT NULL,
    maintenance_count INT NOT NULL,
    PRIMARY KEY (machine_id),
    CONSTRAINT fk_machines_factory FOREIGN KEY (factory_id) 
        REFERENCES factories(factory_id) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- =============================================================================
-- TRANSACTIONAL / FACT TABLES
-- =============================================================================

-- 6. PRODUCTION (Fact Table: Daily Operations)
CREATE TABLE production (
    production_id VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    factory_id VARCHAR(10) NOT NULL,
    product_id VARCHAR(10) NOT NULL,
    machine_id VARCHAR(10) NOT NULL,
    shift_id VARCHAR(10) NOT NULL,
    planned_units INT NOT NULL,
    produced_units INT NOT NULL,
    production_cost DECIMAL(12,2) NOT NULL,
    PRIMARY KEY (production_id),
    CONSTRAINT fk_prod_factory FOREIGN KEY (factory_id) 
        REFERENCES factories(factory_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_prod_product FOREIGN KEY (product_id) 
        REFERENCES products(product_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_prod_machine FOREIGN KEY (machine_id) 
        REFERENCES machines(machine_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_prod_shift FOREIGN KEY (shift_id) 
        REFERENCES shifts(shift_id) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 7. QUALITY (Fact Table: Quality Inspection)
CREATE TABLE quality (
    quality_id VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    production_id VARCHAR(20) NOT NULL,
    product_id VARCHAR(10) NOT NULL,
    factory_id VARCHAR(10) NOT NULL,
    machine_id VARCHAR(10) NOT NULL,
    supplier_id VARCHAR(10) NOT NULL,
    inspected_units INT NOT NULL,
    defective_units INT NOT NULL,
    defect_type VARCHAR(100) NOT NULL,
    PRIMARY KEY (quality_id),
    CONSTRAINT fk_qual_production FOREIGN KEY (production_id) 
        REFERENCES production(production_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_qual_product FOREIGN KEY (product_id) 
        REFERENCES products(product_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_qual_factory FOREIGN KEY (factory_id) 
        REFERENCES factories(factory_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_qual_machine FOREIGN KEY (machine_id) 
        REFERENCES machines(machine_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_qual_supplier FOREIGN KEY (supplier_id) 
        REFERENCES suppliers(supplier_id) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- =============================================================================
-- PERFORMANCE INDEXES (Optimizes analytical aggregations and Power BI DirectQuery)
-- =============================================================================
CREATE INDEX idx_prod_date ON production(date);
CREATE INDEX idx_prod_factory ON production(factory_id);
CREATE INDEX idx_prod_product ON production(product_id);
CREATE INDEX idx_qual_date ON quality(date);
CREATE INDEX idx_qual_defect_type ON quality(defect_type);
CREATE INDEX idx_qual_supplier ON quality(supplier_id);
