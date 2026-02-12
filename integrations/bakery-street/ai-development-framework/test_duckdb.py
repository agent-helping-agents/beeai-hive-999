#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/booze/ai-development/aws-env/lib/python3.11/site-packages')

import duckdb

# Test DuckDB
print("✅ DuckDB installed and working")
print(f"Version: {duckdb.__version__}")

# Create sample data
result = duckdb.sql("SELECT 'Hello from DuckDB' as message, 42 as number")
print(f"Test query: {result.fetchall()}")

# Query local files example
duckdb.sql("CREATE TABLE test AS SELECT * FROM VALUES (1, 'AI'), (2, 'Development'), (3, 'Stack')")
result = duckdb.sql("SELECT * FROM test")
print(f"Local data: {result.fetchall()}")