#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/booze/ai-development/aws-env/lib/python3.11/site-packages')

import duckdb
import os

def show_menu():
    print("\n🦆 DuckDB Data Analyzer")
    print("1. Query CSV file")
    print("2. Query JSON file") 
    print("3. Query folder (*.csv)")
    print("4. Custom SQL query")
    print("5. Exit")
    return input("Choose option: ")

def main():
    conn = duckdb.connect()
    
    while True:
        choice = show_menu()
        
        if choice == "1":
            file = input("CSV file path: ")
            try:
                result = conn.sql(f"SELECT * FROM '{file}' LIMIT 10")
                print(result.fetchall())
            except Exception as e:
                print(f"Error: {e}")
                
        elif choice == "2":
            file = input("JSON file path: ")
            try:
                result = conn.sql(f"SELECT * FROM '{file}' LIMIT 10")
                print(result.fetchall())
            except Exception as e:
                print(f"Error: {e}")
                
        elif choice == "3":
            folder = input("Folder path: ")
            try:
                result = conn.sql(f"SELECT * FROM '{folder}/*.csv' LIMIT 10")
                print(result.fetchall())
            except Exception as e:
                print(f"Error: {e}")
                
        elif choice == "4":
            query = input("SQL query: ")
            try:
                result = conn.sql(query)
                print(result.fetchall())
            except Exception as e:
                print(f"Error: {e}")
                
        elif choice == "5":
            break

if __name__ == "__main__":
    main()