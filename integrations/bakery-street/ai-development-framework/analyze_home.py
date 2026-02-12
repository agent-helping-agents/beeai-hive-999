#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/booze/ai-development/aws-env/lib/python3.11/site-packages')

import duckdb
import os
from pathlib import Path

def analyze_home_folder():
    conn = duckdb.connect()
    home = "/home/booze"
    
    print("🏠 Analyzing Home Folder with DuckDB")
    
    # Find all CSV files
    try:
        result = conn.sql(f"SELECT * FROM glob('{home}/**/*.csv')")
        csv_files = result.fetchall()
        print(f"📊 Found {len(csv_files)} CSV files")
        for file in csv_files[:10]:  # Show first 10
            print(f"  - {file[0]}")
    except Exception as e:
        print(f"CSV search: {e}")
    
    # Find all JSON files
    try:
        result = conn.sql(f"SELECT * FROM glob('{home}/**/*.json')")
        json_files = result.fetchall()
        print(f"📄 Found {len(json_files)} JSON files")
        for file in json_files[:10]:  # Show first 10
            print(f"  - {file[0]}")
    except Exception as e:
        print(f"JSON search: {e}")
    
    # Analyze file sizes and types
    try:
        result = conn.sql(f"""
        SELECT 
            regexp_extract(file, '\.([^.]+)$', 1) as extension,
            COUNT(*) as count
        FROM glob('{home}/**/*.*') 
        WHERE extension IS NOT NULL
        GROUP BY extension 
        ORDER BY count DESC 
        LIMIT 20
        """)
        print("\n📈 File Types Analysis:")
        for row in result.fetchall():
            print(f"  .{row[0]}: {row[1]} files")
    except Exception as e:
        print(f"File analysis: {e}")

if __name__ == "__main__":
    analyze_home_folder()