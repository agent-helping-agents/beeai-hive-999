#!/usr/bin/env python3
"""
Baker Street Laboratory - Database Initialization
Creates and initializes the metadata database with proper schema.
"""

import sqlite3
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

def create_database_schema(db_path: str) -> bool:
    """
    Create the complete database schema for Baker Street Laboratory.
    
    Args:
        db_path: Path to the SQLite database file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Ensure the data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Connect to database (creates file if it doesn't exist)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Research Sessions Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS research_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                query TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP NULL,
                output_directory TEXT,
                metadata TEXT -- JSON metadata
            )
        """)
        
        # Agent Execution Logs Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                agent_name TEXT NOT NULL,
                agent_type TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'running',
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP NULL,
                execution_time_ms INTEGER NULL,
                input_tokens INTEGER NULL,
                output_tokens INTEGER NULL,
                cost_usd REAL NULL,
                error_message TEXT NULL,
                metadata TEXT, -- JSON metadata
                FOREIGN KEY (session_id) REFERENCES research_sessions(session_id)
            )
        """)
        
        # Agent Performance Metrics Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name TEXT NOT NULL,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                metric_unit TEXT,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                session_id TEXT,
                metadata TEXT, -- JSON metadata
                FOREIGN KEY (session_id) REFERENCES research_sessions(session_id)
            )
        """)
        
        # Data Sources Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data_sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id TEXT UNIQUE NOT NULL,
                source_type TEXT NOT NULL, -- 'api', 'web', 'database', 'file'
                source_name TEXT NOT NULL,
                source_url TEXT,
                access_method TEXT,
                last_accessed TIMESTAMP,
                status TEXT DEFAULT 'active',
                reliability_score REAL DEFAULT 1.0,
                metadata TEXT -- JSON metadata
            )
        """)
        
        # Citations and References Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS citations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                source_id TEXT NOT NULL,
                citation_type TEXT NOT NULL, -- 'primary', 'secondary', 'reference'
                title TEXT,
                authors TEXT,
                publication_date DATE,
                doi TEXT,
                url TEXT,
                accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                relevance_score REAL,
                metadata TEXT, -- JSON metadata
                FOREIGN KEY (session_id) REFERENCES research_sessions(session_id),
                FOREIGN KEY (source_id) REFERENCES data_sources(source_id)
            )
        """)
        
        # Research Outputs Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS research_outputs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                output_id TEXT UNIQUE NOT NULL,
                output_type TEXT NOT NULL, -- 'report', 'analysis', 'visualization', 'code'
                file_path TEXT NOT NULL,
                file_size INTEGER,
                file_hash TEXT, -- SHA256 hash for integrity
                version INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_by TEXT, -- Agent or user name
                status TEXT DEFAULT 'active',
                metadata TEXT, -- JSON metadata
                FOREIGN KEY (session_id) REFERENCES research_sessions(session_id)
            )
        """)
        
        # Research Output Versions Table (for tracking changes)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS output_versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                output_id TEXT NOT NULL,
                version_number INTEGER NOT NULL,
                file_path TEXT NOT NULL,
                file_hash TEXT NOT NULL,
                changes_description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_by TEXT,
                metadata TEXT, -- JSON metadata
                FOREIGN KEY (output_id) REFERENCES research_outputs(output_id),
                UNIQUE(output_id, version_number)
            )
        """)
        
        # System Configuration Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                config_key TEXT UNIQUE NOT NULL,
                config_value TEXT NOT NULL,
                config_type TEXT DEFAULT 'string',
                description TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_by TEXT DEFAULT 'system'
            )
        """)
        
        # Audit Trail Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_trail (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_name TEXT NOT NULL,
                record_id TEXT NOT NULL,
                action TEXT NOT NULL, -- 'INSERT', 'UPDATE', 'DELETE'
                old_values TEXT, -- JSON
                new_values TEXT, -- JSON
                changed_by TEXT,
                changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                session_id TEXT
            )
        """)
        
        # Create indexes for better performance
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_research_sessions_status ON research_sessions(status)",
            "CREATE INDEX IF NOT EXISTS idx_research_sessions_created ON research_sessions(created_at)",
            "CREATE INDEX IF NOT EXISTS idx_agent_executions_session ON agent_executions(session_id)",
            "CREATE INDEX IF NOT EXISTS idx_agent_executions_agent ON agent_executions(agent_name)",
            "CREATE INDEX IF NOT EXISTS idx_agent_performance_agent ON agent_performance(agent_name)",
            "CREATE INDEX IF NOT EXISTS idx_citations_session ON citations(session_id)",
            "CREATE INDEX IF NOT EXISTS idx_research_outputs_session ON research_outputs(session_id)",
            "CREATE INDEX IF NOT EXISTS idx_audit_trail_table ON audit_trail(table_name, record_id)"
        ]
        
        for index_sql in indexes:
            cursor.execute(index_sql)
        
        # Insert initial system configuration
        initial_config = [
            ('db_version', '1.0.0', 'string', 'Database schema version'),
            ('initialized_at', datetime.now().isoformat(), 'datetime', 'Database initialization timestamp'),
            ('framework_version', '1.0.0', 'string', 'Baker Street Laboratory framework version')
        ]
        
        cursor.executemany("""
            INSERT OR IGNORE INTO system_config (config_key, config_value, config_type, description)
            VALUES (?, ?, ?, ?)
        """, initial_config)
        
        # Commit all changes
        conn.commit()
        conn.close()
        
        print(f"✅ Database schema created successfully at: {db_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating database schema: {e}")
        return False

def verify_database(db_path: str) -> bool:
    """
    Verify the database connection and schema integrity.
    
    Args:
        db_path: Path to the SQLite database file
        
    Returns:
        bool: True if verification successful, False otherwise
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if all required tables exist
        required_tables = [
            'research_sessions', 'agent_executions', 'agent_performance',
            'data_sources', 'citations', 'research_outputs', 
            'output_versions', 'system_config', 'audit_trail'
        ]
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        missing_tables = set(required_tables) - set(existing_tables)
        if missing_tables:
            print(f"❌ Missing tables: {missing_tables}")
            return False
        
        # Test basic operations
        cursor.execute("SELECT COUNT(*) FROM system_config")
        config_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT config_value FROM system_config WHERE config_key = 'db_version'")
        db_version = cursor.fetchone()
        
        conn.close()
        
        print(f"✅ Database verification successful")
        print(f"   - All {len(required_tables)} tables present")
        print(f"   - {config_count} configuration entries")
        print(f"   - Database version: {db_version[0] if db_version else 'Unknown'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database verification failed: {e}")
        return False

def main():
    """Main initialization function."""
    print("🔬 Baker Street Laboratory - Database Initialization")
    print("=" * 55)
    
    # Default database path
    db_path = "data/metadata.db"
    
    # Check if database already exists
    if os.path.exists(db_path):
        print(f"⚠️  Database already exists at: {db_path}")
        response = input("Do you want to recreate it? (y/N): ").lower().strip()
        if response != 'y':
            print("Database initialization cancelled.")
            return False
        else:
            os.remove(db_path)
            print("Existing database removed.")
    
    # Create database schema
    print("\n📊 Creating database schema...")
    if not create_database_schema(db_path):
        return False
    
    # Verify database
    print("\n🔍 Verifying database integrity...")
    if not verify_database(db_path):
        return False
    
    print(f"\n🎉 Database initialization complete!")
    print(f"Database location: {os.path.abspath(db_path)}")
    print("\nYou can now run: ./run.sh status")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
