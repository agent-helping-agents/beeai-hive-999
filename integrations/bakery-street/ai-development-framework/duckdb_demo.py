#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/booze/ai-development/aws-env/lib/python3.11/site-packages')

import duckdb

# DuckDB works perfectly in Cursor/Linux
print("🦆 DuckDB Demo")

# Query CSV files directly
duckdb.sql("SELECT 'CSV file' as source, count(*) as files FROM glob('*.csv')")

# Query JSON files
duckdb.sql("SELECT 'JSON file' as source, count(*) as files FROM glob('*.json')")

# In-memory analytics
result = duckdb.sql("""
    SELECT 'AI Development' as project, 
           'DuckDB' as tool,
           'Fast local SQL' as benefit
""")
print(result.fetchall())