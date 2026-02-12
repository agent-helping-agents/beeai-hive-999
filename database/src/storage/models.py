"""
Energetic Lexicon Database - SQLAlchemy ORM Models
🔒 PRIVATE - PROPRIETARY
© 2025 Bakery Street Project

SQLAlchemy models for unified knowledge graph database.
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Float,
    DateTime, ForeignKey, CheckConstraint, UniqueConstraint
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
import json

Base = declarative_base()


# ============================================================================
# REPOSITORIES
# ============================================================================

class Repository(Base):
    """GitHub repository metadata"""
    __tablename__ = 'repos'

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Core metadata
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(Text)
    url = Column(String, nullable=False)

    # Repository attributes
    is_private = Column(Boolean, nullable=False, default=True, index=True)
    language = Column(String, index=True)
    stars = Column(Integer, default=0)
    forks = Column(Integer, default=0)

    # Classification
    automation_role = Column(String)
    geometry_quadrant = Column(
        String,
        CheckConstraint("geometry_quadrant IN ('theoretical', 'experimental', 'implementation', 'interdisciplinary')")
    )

    # Tags (JSON stored as text)
    _tags = Column('tags', Text)

    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    last_synced_at = Column(DateTime)

    # GitHub metadata
    github_id = Column(Integer, unique=True)
    default_branch = Column(String, default='main')

    # Flags
    is_archived = Column(Boolean, default=False)
    is_fork = Column(Boolean, default=False)

    # Full-text search
    readme_content = Column(Text)
    _topics = Column('topics', Text)

    # Relationships
    pdfs = relationship('PDF', back_populates='related_repo')
    automation_runs = relationship('AutomationRun', back_populates='repo', cascade='all, delete-orphan')

    @property
    def tags(self) -> List[str]:
        """Parse tags from JSON"""
        if self._tags:
            try:
                return json.loads(self._tags)
            except json.JSONDecodeError:
                return []
        return []

    @tags.setter
    def tags(self, value: List[str]):
        """Store tags as JSON"""
        self._tags = json.dumps(value)

    @property
    def topics(self) -> List[str]:
        """Parse topics from JSON"""
        if self._topics:
            try:
                return json.loads(self._topics)
            except json.JSONDecodeError:
                return []
        return []

    @topics.setter
    def topics(self, value: List[str]):
        """Store topics as JSON"""
        self._topics = json.dumps(value)

    def __repr__(self):
        return f"<Repository(name='{self.name}', quadrant='{self.geometry_quadrant}')>"


# ============================================================================
# PDFS
# ============================================================================

class PDF(Base):
    """PDF document metadata and content"""
    __tablename__ = 'pdfs'

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Core metadata
    title = Column(String, nullable=False, index=True)
    file_path = Column(String, nullable=False, unique=True)
    file_hash = Column(String, nullable=False, index=True)

    # PDF attributes
    page_count = Column(Integer)
    file_size = Column(Integer)

    # Content
    extracted_text = Column(Text)

    # Embedding metadata
    indexed_at = Column(DateTime)
    embedding_model = Column(String)
    embedding_dimensions = Column(Integer)

    # Classification
    _tags = Column('tags', Text)
    category = Column(String, index=True)

    # Relationships
    related_repo_id = Column(Integer, ForeignKey('repos.id', ondelete='SET NULL'), index=True)
    related_repo = relationship('Repository', back_populates='pdfs')

    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    @property
    def tags(self) -> List[str]:
        """Parse tags from JSON"""
        if self._tags:
            try:
                return json.loads(self._tags)
            except json.JSONDecodeError:
                return []
        return []

    @tags.setter
    def tags(self, value: List[str]):
        """Store tags as JSON"""
        self._tags = json.dumps(value)

    def __repr__(self):
        return f"<PDF(title='{self.title}', hash='{self.file_hash[:8]}...')>"


# ============================================================================
# CONCEPTS
# ============================================================================

class Concept(Base):
    """Concept definition in Energetic Lexicon"""
    __tablename__ = 'concepts'

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Core definition
    term = Column(String, nullable=False, unique=True, index=True)
    definition = Column(Text, nullable=False)

    # Extended definition
    _excluded_meanings = Column('excluded_meanings', Text)
    _metaphors = Column('metaphors', Text)

    # Classification
    domain = Column(String, index=True)
    abstraction_level = Column(
        Integer,
        CheckConstraint('abstraction_level BETWEEN 1 AND 5')
    )

    # Context
    first_seen_in = Column(String)
    _usage_examples = Column('usage_examples', Text)

    # Relationships
    parent_concept_id = Column(Integer, ForeignKey('concepts.id', ondelete='SET NULL'), index=True)
    children = relationship('Concept', remote_side=[id])

    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    @property
    def excluded_meanings(self) -> List[str]:
        """Parse excluded meanings from JSON"""
        if self._excluded_meanings:
            try:
                return json.loads(self._excluded_meanings)
            except json.JSONDecodeError:
                return []
        return []

    @excluded_meanings.setter
    def excluded_meanings(self, value: List[str]):
        """Store excluded meanings as JSON"""
        self._excluded_meanings = json.dumps(value)

    @property
    def metaphors(self) -> List[str]:
        """Parse metaphors from JSON"""
        if self._metaphors:
            try:
                return json.loads(self._metaphors)
            except json.JSONDecodeError:
                return []
        return []

    @metaphors.setter
    def metaphors(self, value: List[str]):
        """Store metaphors as JSON"""
        self._metaphors = json.dumps(value)

    @property
    def usage_examples(self) -> List[str]:
        """Parse usage examples from JSON"""
        if self._usage_examples:
            try:
                return json.loads(self._usage_examples)
            except json.JSONDecodeError:
                return []
        return []

    @usage_examples.setter
    def usage_examples(self, value: List[str]):
        """Store usage examples as JSON"""
        self._usage_examples = json.dumps(value)

    def __repr__(self):
        return f"<Concept(term='{self.term}', domain='{self.domain}')>"


# ============================================================================
# RELATIONS
# ============================================================================

class Relation(Base):
    """Knowledge graph edge (relationship between entities)"""
    __tablename__ = 'relations'
    __table_args__ = (
        UniqueConstraint('source_id', 'source_type', 'target_id', 'target_type', 'relation_type'),
    )

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Graph edge
    source_id = Column(Integer, nullable=False, index=True)
    source_type = Column(
        String,
        nullable=False,
        CheckConstraint("source_type IN ('repo', 'pdf', 'concept')")
    )

    target_id = Column(Integer, nullable=False, index=True)
    target_type = Column(
        String,
        nullable=False,
        CheckConstraint("target_type IN ('repo', 'pdf', 'concept')")
    )

    # Relationship metadata
    relation_type = Column(String, nullable=False, index=True)
    strength = Column(
        Float,
        default=1.0,
        CheckConstraint('strength BETWEEN 0.0 AND 1.0')
    )

    # Context
    evidence = Column(Text)

    # Timestamps
    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<Relation({self.source_type}:{self.source_id} --[{self.relation_type}]--> {self.target_type}:{self.target_id})>"


# ============================================================================
# AUTOMATION RUNS
# ============================================================================

class AutomationRun(Base):
    """CI/CD pipeline execution tracking"""
    __tablename__ = 'automation_runs'

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Run metadata
    repo_id = Column(Integer, ForeignKey('repos.id', ondelete='CASCADE'), nullable=False, index=True)
    repo = relationship('Repository', back_populates='automation_runs')

    # Pipeline information
    pipeline_name = Column(String, nullable=False, index=True)
    run_id = Column(String)

    # Status
    status = Column(
        String,
        nullable=False,
        CheckConstraint("status IN ('pending', 'running', 'success', 'failure', 'cancelled')"),
        index=True
    )

    # Results
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    duration_seconds = Column(Integer)

    # Logs
    logs_path = Column(String)
    error_message = Column(Text)

    # Metrics
    records_processed = Column(Integer, default=0)
    records_updated = Column(Integer, default=0)
    records_failed = Column(Integer, default=0)

    # Timestamps
    created_at = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<AutomationRun(pipeline='{self.pipeline_name}', status='{self.status}')>"


# ============================================================================
# USERS
# ============================================================================

class User(Base):
    """User account for authentication & authorization"""
    __tablename__ = 'users'

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Authentication
    username = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, unique=True)
    password_hash = Column(String, nullable=False)

    # Authorization
    role = Column(
        String,
        nullable=False,
        default='readonly',
        CheckConstraint("role IN ('admin', 'developer', 'readonly')"),
        index=True
    )

    # API access
    api_key_hash = Column(String, unique=True)
    api_key_created_at = Column(DateTime)
    api_key_expires_at = Column(DateTime)

    # Status
    is_active = Column(Boolean, default=True, index=True)
    last_login_at = Column(DateTime)

    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}')>"


# ============================================================================
# AUDIT LOG
# ============================================================================

class AuditLog(Base):
    """Immutable audit trail for security & compliance"""
    __tablename__ = 'audit_log'

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Event metadata
    timestamp = Column(DateTime, default=func.now(), index=True)
    event_type = Column(String, nullable=False, index=True)

    # User information
    user_id = Column(Integer, index=True)
    username = Column(String)
    ip_address = Column(String)

    # Action details
    table_name = Column(String, index=True)
    record_id = Column(Integer)
    action = Column(String, nullable=False)

    # Before/after state (JSON)
    _old_values = Column('old_values', Text)
    _new_values = Column('new_values', Text)

    # Result
    success = Column(Boolean, nullable=False)
    error_message = Column(Text)

    # Context
    request_id = Column(String)
    user_agent = Column(String)

    @property
    def old_values(self) -> dict:
        """Parse old values from JSON"""
        if self._old_values:
            try:
                return json.loads(self._old_values)
            except json.JSONDecodeError:
                return {}
        return {}

    @old_values.setter
    def old_values(self, value: dict):
        """Store old values as JSON"""
        self._old_values = json.dumps(value)

    @property
    def new_values(self) -> dict:
        """Parse new values from JSON"""
        if self._new_values:
            try:
                return json.loads(self._new_values)
            except json.JSONDecodeError:
                return {}
        return {}

    @new_values.setter
    def new_values(self, value: dict):
        """Store new values as JSON"""
        self._new_values = json.dumps(value)

    def __repr__(self):
        return f"<AuditLog(event='{self.event_type}', user='{self.username}', success={self.success})>"
