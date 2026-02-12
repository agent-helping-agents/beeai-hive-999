#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/booze/ai-development/aws-env/lib/python3.11/site-packages')

import duckdb

class LocalDataAnalyzer:
    def __init__(self):
        self.conn = duckdb.connect()
    
    def query_csv(self, file_path, limit=10):
        return self.conn.sql(f"SELECT * FROM '{file_path}' LIMIT {limit}")
    
    def query_json(self, file_path):
        return self.conn.sql(f"SELECT * FROM '{file_path}'")
    
    def analyze_folder(self, pattern):
        return self.conn.sql(f"SELECT * FROM '{pattern}'")

# Ready to use
analyzer = LocalDataAnalyzer()
print("🦆 DuckDB ready for local data analysis")