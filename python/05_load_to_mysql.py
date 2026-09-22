"""
=============================================================================
Module: 05_load_to_mysql.py
Project: AI-Powered Automotive Manufacturing BI & Quality Analysis System
Description: Connects to MySQL Server, executes the schema DDL, and bulk
             inserts all 7 cleaned datasets with error handling and progress.
=============================================================================
"""

import os
import sys
import getpass
import pandas as pd
import mysql.connector
from mysql.connector import Error

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN_DIR = os.path.join(BASE_DIR, "data", "cleaned")
SQL_SCHEMA_FILE = os.path.join(BASE_DIR, "sql", "01_create_database_schema.sql")

def connect_mysql(host="localhost", user="root", password=""):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            allow_local_infile=True
        )
        if conn.is_connected():
            print(f"[SUCCESS] Connected to MySQL Server at {host} as '{user}'")
            return conn
    except Error as e:
        print(f"[ERROR] Could not connect to MySQL: {e}")
        return None

def execute_schema(cursor, schema_path):
    print("\n[STEP 1] Applying Database Schema (DDL)...")
    with open(schema_path, "r") as f:
        schema_sql = f.read()
        
    statements = [stmt.strip() for stmt in schema_sql.split(";") if stmt.strip()]
    for stmt in statements:
        cursor.execute(stmt)
    print("  [OK] Database 'apex_manufacturing_db' and 7 tables created successfully.")

def bulk_insert_df(cursor, table_name, df, chunk_size=5000):
    cols = list(df.columns)
    cols_str = ", ".join([f"`{c}`" for c in cols])
    placeholders = ", ".join(["%s"] * len(cols))
    sql = f"INSERT INTO `{table_name}` ({cols_str}) VALUES ({placeholders})"
    
    total_rows = len(df)
    values = [tuple(x) for x in df.to_numpy()]
    
    for i in range(0, total_rows, chunk_size):
        chunk = values[i : i + chunk_size]
        cursor.executemany(sql, chunk)
        
    print(f"  [OK] Inserted {total_rows:,} records into `{table_name}`")

def main():
    print("=" * 70)
    print(" APEX TURBOTECH - MYSQL DATABASE IMPORTER")
    print("=" * 70)
    
    # Check if credentials exist in environment, otherwise prompt user
    host = os.getenv("MYSQL_HOST", "localhost")
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD")
    
    if not password:
        print("\nPlease enter your MySQL root password (set during installation):")
        password = getpass.getpass("Password: ")
        
    conn = connect_mysql(host, user, password)
    if not conn:
        print("\n[!] Please verify your password and that MySQL service is running.")
        sys.exit(1)
        
    cursor = conn.cursor()
    
    # 1. Create Schema
    execute_schema(cursor, SQL_SCHEMA_FILE)
    cursor.execute("USE apex_manufacturing_db;")
    
    # 2. Insert Master Tables (In strict FK order)
    print("\n[STEP 2] Loading Master / Dimension Data...")
    tables_order = ["factories", "products", "shifts", "suppliers", "machines"]
    for tbl in tables_order:
        df = pd.read_csv(os.path.join(CLEAN_DIR, f"{tbl}.csv"))
        bulk_insert_df(cursor, tbl, df)
        
    # 3. Insert Transactional Fact Tables
    print("\n[STEP 3] Loading Transactional Fact Data (55k batches each)...")
    for tbl in ["production", "quality"]:
        df = pd.read_csv(os.path.join(CLEAN_DIR, f"{tbl}.csv"))
        bulk_insert_df(cursor, tbl, df)
        
    conn.commit()
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 70)
    print(" [SUCCESS] All 7 tables populated in MySQL: 'apex_manufacturing_db'")
    print("=" * 70)

if __name__ == "__main__":
    main()
