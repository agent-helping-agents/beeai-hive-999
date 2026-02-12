"""
Energetic Lexicon Database - Database Connection & Session Management
🔒 PRIVATE - PROPRIETARY
© 2025 Bakery Street Project

SQLAlchemy database engine, session management, and initialization.
"""

import os
import logging
from pathlib import Path
from typing import Generator, Optional
from contextlib import contextmanager

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from .models import Base

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and sessions"""

    def __init__(
        self,
        db_path: Optional[str] = None,
        echo: bool = False,
        check_same_thread: bool = True
    ):
        """
        Initialize database manager

        Args:
            db_path: Path to SQLite database file (default: data/lexicon.db)
            echo: Enable SQL query logging
            check_same_thread: SQLite thread safety check (disable for multi-threaded)
        """
        # Default database path
        if db_path is None:
            project_root = Path(__file__).parent.parent.parent
            data_dir = project_root / 'data'
            data_dir.mkdir(exist_ok=True)
            db_path = str(data_dir / 'lexicon.db')

        self.db_path = db_path
        self.db_url = f"sqlite:///{db_path}"

        # Create engine
        connect_args = {"check_same_thread": check_same_thread}

        self.engine = create_engine(
            self.db_url,
            echo=echo,
            connect_args=connect_args,
            poolclass=StaticPool  # SQLite doesn't need pooling
        )

        # Enable foreign keys for SQLite
        @event.listens_for(self.engine, "connect")
        def set_sqlite_pragma(dbapi_conn, connection_record):
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

        # Create session factory
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

        logger.info(f"Database manager initialized: {self.db_url}")

    def create_all_tables(self):
        """Create all tables defined in models"""
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=self.engine)
        logger.info("Database tables created successfully")

    def drop_all_tables(self):
        """Drop all tables (DANGEROUS - use only in development)"""
        logger.warning("Dropping all database tables...")
        Base.metadata.drop_all(bind=self.engine)
        logger.warning("All tables dropped")

    def get_session(self) -> Session:
        """
        Get a new database session

        Returns:
            SQLAlchemy Session

        Example:
            session = db_manager.get_session()
            try:
                # Use session
                pass
            finally:
                session.close()
        """
        return self.SessionLocal()

    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        """
        Context manager for database sessions with automatic commit/rollback

        Yields:
            SQLAlchemy Session

        Example:
            with db_manager.session_scope() as session:
                repo = Repository(name="test-repo", url="https://...")
                session.add(repo)
                # Automatically committed on exit
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Session rollback due to error: {e}")
            raise
        finally:
            session.close()

    def execute_raw_sql(self, sql: str, params: Optional[dict] = None):
        """
        Execute raw SQL (use sparingly - prefer ORM)

        Args:
            sql: SQL query
            params: Query parameters

        Returns:
            Query result
        """
        with self.engine.connect() as conn:
            result = conn.execute(sql, params or {})
            conn.commit()
            return result

    def load_schema_from_file(self, schema_path: str):
        """
        Load and execute SQL schema file

        Args:
            schema_path: Path to schema.sql file
        """
        logger.info(f"Loading schema from {schema_path}")

        with open(schema_path, 'r') as f:
            schema_sql = f.read()

        # Split into individual statements
        statements = [s.strip() for s in schema_sql.split(';') if s.strip()]

        with self.engine.begin() as conn:
            for statement in statements:
                # Skip comments
                if statement.startswith('--'):
                    continue

                try:
                    conn.execute(statement)
                except Exception as e:
                    logger.error(f"Error executing statement: {statement[:100]}...")
                    logger.error(f"Error: {e}")
                    raise

        logger.info("Schema loaded successfully")

    def get_table_info(self) -> dict:
        """
        Get information about all tables in the database

        Returns:
            Dict with table names and row counts
        """
        info = {}

        with self.session_scope() as session:
            for table in Base.metadata.sorted_tables:
                count = session.query(table).count()
                info[table.name] = {
                    'row_count': count,
                    'columns': [col.name for col in table.columns]
                }

        return info

    def backup_database(self, backup_path: str):
        """
        Create a backup of the database file

        Args:
            backup_path: Path for backup file
        """
        import shutil

        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Database file not found: {self.db_path}")

        logger.info(f"Backing up database to {backup_path}")
        shutil.copy2(self.db_path, backup_path)
        logger.info("Backup completed")

    def vacuum(self):
        """Optimize database (reclaim space, rebuild indexes)"""
        logger.info("Vacuuming database...")
        with self.engine.begin() as conn:
            conn.execute("VACUUM")
        logger.info("Database vacuumed")


# ============================================================================
# GLOBAL DATABASE INSTANCE
# ============================================================================

# Singleton database manager instance
_db_manager: Optional[DatabaseManager] = None


def get_db_manager(
    db_path: Optional[str] = None,
    echo: bool = False
) -> DatabaseManager:
    """
    Get or create global database manager instance

    Args:
        db_path: Database file path (only used on first call)
        echo: Enable SQL logging (only used on first call)

    Returns:
        DatabaseManager instance
    """
    global _db_manager

    if _db_manager is None:
        _db_manager = DatabaseManager(db_path=db_path, echo=echo)

    return _db_manager


def get_session() -> Session:
    """
    Convenience function to get a database session

    Returns:
        SQLAlchemy Session
    """
    db = get_db_manager()
    return db.get_session()


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """
    Convenience context manager for database sessions

    Example:
        from src.storage.database import session_scope
        from src.storage.models import Repository

        with session_scope() as session:
            repo = Repository(name="test", url="https://...")
            session.add(repo)
    """
    db = get_db_manager()
    with db.session_scope() as session:
        yield session


# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def init_database(
    db_path: Optional[str] = None,
    load_schema: bool = False,
    schema_path: Optional[str] = None,
    reset: bool = False
):
    """
    Initialize the database

    Args:
        db_path: Database file path
        load_schema: Load from schema.sql file instead of using ORM
        schema_path: Path to schema.sql (default: project_root/schema.sql)
        reset: Drop all tables before creating (DANGEROUS)
    """
    db = get_db_manager(db_path=db_path)

    if reset:
        logger.warning("Resetting database (dropping all tables)...")
        db.drop_all_tables()

    if load_schema:
        if schema_path is None:
            project_root = Path(__file__).parent.parent.parent
            schema_path = str(project_root / 'schema.sql')

        db.load_schema_from_file(schema_path)
    else:
        db.create_all_tables()

    logger.info("Database initialization complete")

    # Log table info
    info = db.get_table_info()
    logger.info("Database tables:")
    for table_name, table_info in info.items():
        logger.info(f"  - {table_name}: {table_info['row_count']} rows")


# ============================================================================
# CLI INTERFACE
# ============================================================================

if __name__ == '__main__':
    import argparse

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    parser = argparse.ArgumentParser(description='Database Management Tool')
    parser.add_argument('action', choices=['init', 'info', 'backup', 'vacuum', 'reset'])
    parser.add_argument('--db', type=str, help='Database file path')
    parser.add_argument('--schema', type=str, help='Schema SQL file path')
    parser.add_argument('--output', type=str, help='Backup output path')
    parser.add_argument('--echo', action='store_true', help='Enable SQL logging')

    args = parser.parse_args()

    db = get_db_manager(db_path=args.db, echo=args.echo)

    if args.action == 'init':
        load_schema = args.schema is not None
        init_database(
            db_path=args.db,
            load_schema=load_schema,
            schema_path=args.schema
        )

    elif args.action == 'info':
        info = db.get_table_info()
        print("\nDatabase Information:")
        print(f"Path: {db.db_path}")
        print(f"\nTables ({len(info)}):")
        for table_name, table_info in info.items():
            print(f"\n  {table_name}:")
            print(f"    Rows: {table_info['row_count']}")
            print(f"    Columns: {', '.join(table_info['columns'])}")

    elif args.action == 'backup':
        if not args.output:
            print("Error: --output required for backup")
            exit(1)
        db.backup_database(args.output)

    elif args.action == 'vacuum':
        db.vacuum()

    elif args.action == 'reset':
        confirm = input("⚠️  This will DELETE ALL DATA. Type 'yes' to confirm: ")
        if confirm.lower() == 'yes':
            init_database(db_path=args.db, reset=True)
        else:
            print("Reset cancelled")
