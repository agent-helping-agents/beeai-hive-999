#!/usr/bin/env python3
"""
Energetic Lexicon Database - Initialization Script
🔒 PRIVATE - PROPRIETARY
© 2025 Bakery Street Project

Initializes the database with schema, creates admin user, and optionally encrypts.
"""

import sys
import os
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.storage.database import init_database, get_db_manager, session_scope
from src.storage.models import User, Concept
from scripts.encryption import EncryptionWrapper

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_sample_data():
    """Create sample concepts for testing"""
    logger.info("Creating sample data...")

    with session_scope() as session:
        # Check if sample data already exists
        existing = session.query(Concept).filter(Concept.term == 'AutomationCodex').first()
        if existing:
            logger.info("Sample data already exists, skipping...")
            return

        # Create core concepts
        concepts = [
            {
                'term': 'AutomationCodex',
                'definition': 'Automation-first philosophy underlying all Bakery Street infrastructure. '
                             'Combines graph theory, information theory, and MDPs for resilient AI systems.',
                'domain': 'tech',
                'abstraction_level': 4,
                'metaphors': [
                    'Autonomous nervous system for distributed systems',
                    'Self-organizing orchestra',
                    'Resilient mycelial network'
                ]
            },
            {
                'term': 'Research Geometry',
                'definition': 'Framework treating research as geometric/coordinate space rather than Q&A. '
                             'Uses 4-quadrant classification: Theoretical, Experimental, Implementation, Interdisciplinary.',
                'domain': 'science',
                'abstraction_level': 5,
                'excluded_meanings': [
                    'Not just a folder of markdown files',
                    'Not a static template',
                    'Not traditional research methodology'
                ],
                'metaphors': [
                    'Semantic constellation',
                    'Multi-dimensional knowledge topology',
                    'Epistemic coordinate system'
                ]
            },
            {
                'term': 'Energetic Lexicon',
                'definition': 'Unified knowledge graph of entire Bakery Street ecosystem. '
                             'Maps repositories, PDFs, concepts, and automation patterns into queryable semantic database.',
                'domain': 'tech',
                'abstraction_level': 4,
                'metaphors': [
                    'Mycelial network connecting all repos',
                    'Living organism that self-updates',
                    'Quantum-entangled knowledge base'
                ]
            },
            {
                'term': 'PRIMAX',
                'definition': 'Self-learning neuromorphic AI system via AutomationCodex. '
                             'Core runtime for dynamic tool discovery and agent orchestration.',
                'domain': 'tech',
                'abstraction_level': 3,
                'first_seen_in': 'PRIMAX-ai repository'
            },
            {
                'term': 'AgenticSeek',
                'definition': 'AGPL-licensed local AI assistant. Requires clean separation from proprietary core '
                             'via JSON/REST API boundary for license compliance.',
                'domain': 'tech',
                'abstraction_level': 2,
                'first_seen_in': 'https://github.com/Fosowl/agenticSeek'
            }
        ]

        for concept_data in concepts:
            concept = Concept(**concept_data)
            session.add(concept)

        logger.info(f"Created {len(concepts)} sample concepts")


def verify_admin_user():
    """Verify admin user exists"""
    logger.info("Verifying admin user...")

    with session_scope() as session:
        admin = session.query(User).filter(User.username == 'admin').first()

        if admin:
            logger.info("✅ Admin user exists")
            logger.warning("⚠️  Default password is 'changeme' - CHANGE THIS IN PRODUCTION")
        else:
            logger.error("❌ Admin user not found - check schema.sql sample data")


def encrypt_database(db_path: str):
    """Encrypt the database file"""
    logger.info("Encrypting database...")

    try:
        encryptor = EncryptionWrapper()
        encrypted_path = encryptor.encrypt_file(
            db_path,
            output_path=f"{db_path}.gpg"
        )
        logger.info(f"✅ Database encrypted: {encrypted_path}")
        logger.info("   Decryption command: gpg --decrypt --batch --passphrase-file ~/.primax_vault_password --output lexicon.db lexicon.db.gpg")
    except Exception as e:
        logger.error(f"❌ Encryption failed: {e}")


def main():
    """Main initialization function"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Initialize Energetic Lexicon Database'
    )
    parser.add_argument(
        '--db',
        type=str,
        default=None,
        help='Database file path (default: data/lexicon.db)'
    )
    parser.add_argument(
        '--schema',
        type=str,
        default=None,
        help='Load from schema.sql file instead of ORM'
    )
    parser.add_argument(
        '--reset',
        action='store_true',
        help='⚠️  Drop all tables before creating (DANGEROUS)'
    )
    parser.add_argument(
        '--encrypt',
        action='store_true',
        help='Encrypt database after creation'
    )
    parser.add_argument(
        '--sample-data',
        action='store_true',
        help='Create sample concepts'
    )

    args = parser.parse_args()

    logger.info("=" * 70)
    logger.info("ENERGETIC LEXICON DATABASE - INITIALIZATION")
    logger.info("=" * 70)

    # Initialize database
    init_database(
        db_path=args.db,
        load_schema=(args.schema is not None),
        schema_path=args.schema,
        reset=args.reset
    )

    # Create sample data if requested
    if args.sample_data:
        create_sample_data()

    # Verify admin user
    verify_admin_user()

    # Get database info
    db = get_db_manager()
    info = db.get_table_info()

    logger.info("\n" + "=" * 70)
    logger.info("DATABASE INITIALIZATION COMPLETE")
    logger.info("=" * 70)
    logger.info(f"Database: {db.db_path}")
    logger.info(f"Tables: {len(info)}")

    for table_name, table_info in info.items():
        logger.info(f"  - {table_name}: {table_info['row_count']} rows")

    # Encrypt if requested
    if args.encrypt:
        logger.info("\n" + "=" * 70)
        logger.info("ENCRYPTING DATABASE")
        logger.info("=" * 70)
        encrypt_database(db.db_path)

    logger.info("\n" + "=" * 70)
    logger.info("NEXT STEPS")
    logger.info("=" * 70)
    logger.info("1. Change admin password (default: 'changeme')")
    logger.info("2. Create your user account")
    logger.info("3. Start ingesting repository data")
    logger.info("4. Configure CI/CD automation")
    logger.info("\n✅ Database ready for Phase 2: Ingestion")


if __name__ == '__main__':
    main()
