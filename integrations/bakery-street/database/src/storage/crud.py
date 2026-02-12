"""
Energetic Lexicon Database - CRUD Operations
🔒 PRIVATE - PROPRIETARY
© 2025 Bakery Street Project

Create, Read, Update, Delete operations for all models.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from .models import (
    Repository, PDF, Concept, Relation,
    AutomationRun, User, AuditLog
)

import logging

logger = logging.getLogger(__name__)


# ============================================================================
# REPOSITORIES CRUD
# ============================================================================

class RepositoryCRUD:
    """CRUD operations for repositories"""

    @staticmethod
    def create(
        session: Session,
        name: str,
        url: str,
        description: Optional[str] = None,
        is_private: bool = True,
        **kwargs
    ) -> Repository:
        """
        Create a new repository

        Args:
            session: Database session
            name: Repository name
            url: Repository URL
            description: Repository description
            is_private: Private repository flag
            **kwargs: Additional repository attributes

        Returns:
            Created Repository object
        """
        repo = Repository(
            name=name,
            url=url,
            description=description,
            is_private=is_private,
            **kwargs
        )
        session.add(repo)
        session.flush()  # Get ID without committing
        logger.info(f"Created repository: {name}")
        return repo

    @staticmethod
    def get_by_id(session: Session, repo_id: int) -> Optional[Repository]:
        """Get repository by ID"""
        return session.query(Repository).filter(Repository.id == repo_id).first()

    @staticmethod
    def get_by_name(session: Session, name: str) -> Optional[Repository]:
        """Get repository by name"""
        return session.query(Repository).filter(Repository.name == name).first()

    @staticmethod
    def get_all(
        session: Session,
        quadrant: Optional[str] = None,
        is_private: Optional[bool] = None,
        is_archived: bool = False
    ) -> List[Repository]:
        """
        Get all repositories with optional filtering

        Args:
            session: Database session
            quadrant: Filter by geometry quadrant
            is_private: Filter by privacy
            is_archived: Include archived repositories

        Returns:
            List of Repository objects
        """
        query = session.query(Repository)

        if quadrant:
            query = query.filter(Repository.geometry_quadrant == quadrant)

        if is_private is not None:
            query = query.filter(Repository.is_private == is_private)

        if not is_archived:
            query = query.filter(Repository.is_archived == False)

        return query.all()

    @staticmethod
    def update(session: Session, repo_id: int, **kwargs) -> Optional[Repository]:
        """
        Update repository

        Args:
            session: Database session
            repo_id: Repository ID
            **kwargs: Fields to update

        Returns:
            Updated Repository object
        """
        repo = session.query(Repository).filter(Repository.id == repo_id).first()
        if repo:
            for key, value in kwargs.items():
                if hasattr(repo, key):
                    setattr(repo, key, value)
            session.flush()
            logger.info(f"Updated repository: {repo.name}")
        return repo

    @staticmethod
    def delete(session: Session, repo_id: int) -> bool:
        """Delete repository"""
        repo = session.query(Repository).filter(Repository.id == repo_id).first()
        if repo:
            session.delete(repo)
            session.flush()
            logger.info(f"Deleted repository: {repo.name}")
            return True
        return False

    @staticmethod
    def search(
        session: Session,
        query: str,
        fields: Optional[List[str]] = None
    ) -> List[Repository]:
        """
        Search repositories by text

        Args:
            session: Database session
            query: Search query
            fields: Fields to search in (default: name, description, readme_content)

        Returns:
            List of matching Repository objects
        """
        if fields is None:
            fields = ['name', 'description', 'readme_content']

        filters = []
        for field in fields:
            if hasattr(Repository, field):
                filters.append(getattr(Repository, field).contains(query))

        return session.query(Repository).filter(or_(*filters)).all()


# ============================================================================
# PDFS CRUD
# ============================================================================

class PDFCRUD:
    """CRUD operations for PDFs"""

    @staticmethod
    def create(
        session: Session,
        title: str,
        file_path: str,
        file_hash: str,
        **kwargs
    ) -> PDF:
        """Create a new PDF record"""
        pdf = PDF(
            title=title,
            file_path=file_path,
            file_hash=file_hash,
            **kwargs
        )
        session.add(pdf)
        session.flush()
        logger.info(f"Created PDF: {title}")
        return pdf

    @staticmethod
    def get_by_id(session: Session, pdf_id: int) -> Optional[PDF]:
        """Get PDF by ID"""
        return session.query(PDF).filter(PDF.id == pdf_id).first()

    @staticmethod
    def get_by_hash(session: Session, file_hash: str) -> Optional[PDF]:
        """Get PDF by file hash (for deduplication)"""
        return session.query(PDF).filter(PDF.file_hash == file_hash).first()

    @staticmethod
    def get_all(
        session: Session,
        category: Optional[str] = None,
        repo_id: Optional[int] = None
    ) -> List[PDF]:
        """Get all PDFs with optional filtering"""
        query = session.query(PDF)

        if category:
            query = query.filter(PDF.category == category)

        if repo_id:
            query = query.filter(PDF.related_repo_id == repo_id)

        return query.all()

    @staticmethod
    def update(session: Session, pdf_id: int, **kwargs) -> Optional[PDF]:
        """Update PDF"""
        pdf = session.query(PDF).filter(PDF.id == pdf_id).first()
        if pdf:
            for key, value in kwargs.items():
                if hasattr(pdf, key):
                    setattr(pdf, key, value)
            session.flush()
            logger.info(f"Updated PDF: {pdf.title}")
        return pdf

    @staticmethod
    def delete(session: Session, pdf_id: int) -> bool:
        """Delete PDF"""
        pdf = session.query(PDF).filter(PDF.id == pdf_id).first()
        if pdf:
            session.delete(pdf)
            session.flush()
            logger.info(f"Deleted PDF: {pdf.title}")
            return True
        return False

    @staticmethod
    def search_content(session: Session, query: str) -> List[PDF]:
        """Search PDFs by extracted text content"""
        return session.query(PDF).filter(
            PDF.extracted_text.contains(query)
        ).all()


# ============================================================================
# CONCEPTS CRUD
# ============================================================================

class ConceptCRUD:
    """CRUD operations for concepts"""

    @staticmethod
    def create(
        session: Session,
        term: str,
        definition: str,
        **kwargs
    ) -> Concept:
        """Create a new concept"""
        concept = Concept(
            term=term,
            definition=definition,
            **kwargs
        )
        session.add(concept)
        session.flush()
        logger.info(f"Created concept: {term}")
        return concept

    @staticmethod
    def get_by_id(session: Session, concept_id: int) -> Optional[Concept]:
        """Get concept by ID"""
        return session.query(Concept).filter(Concept.id == concept_id).first()

    @staticmethod
    def get_by_term(session: Session, term: str) -> Optional[Concept]:
        """Get concept by term"""
        return session.query(Concept).filter(Concept.term == term).first()

    @staticmethod
    def get_all(
        session: Session,
        domain: Optional[str] = None,
        abstraction_level: Optional[int] = None
    ) -> List[Concept]:
        """Get all concepts with optional filtering"""
        query = session.query(Concept)

        if domain:
            query = query.filter(Concept.domain == domain)

        if abstraction_level:
            query = query.filter(Concept.abstraction_level == abstraction_level)

        return query.all()

    @staticmethod
    def update(session: Session, concept_id: int, **kwargs) -> Optional[Concept]:
        """Update concept"""
        concept = session.query(Concept).filter(Concept.id == concept_id).first()
        if concept:
            for key, value in kwargs.items():
                if hasattr(concept, key):
                    setattr(concept, key, value)
            session.flush()
            logger.info(f"Updated concept: {concept.term}")
        return concept

    @staticmethod
    def delete(session: Session, concept_id: int) -> bool:
        """Delete concept"""
        concept = session.query(Concept).filter(Concept.id == concept_id).first()
        if concept:
            session.delete(concept)
            session.flush()
            logger.info(f"Deleted concept: {concept.term}")
            return True
        return False

    @staticmethod
    def search(session: Session, query: str) -> List[Concept]:
        """Search concepts by term or definition"""
        return session.query(Concept).filter(
            or_(
                Concept.term.contains(query),
                Concept.definition.contains(query)
            )
        ).all()


# ============================================================================
# RELATIONS CRUD
# ============================================================================

class RelationCRUD:
    """CRUD operations for relations (knowledge graph edges)"""

    @staticmethod
    def create(
        session: Session,
        source_id: int,
        source_type: str,
        target_id: int,
        target_type: str,
        relation_type: str,
        strength: float = 1.0,
        **kwargs
    ) -> Relation:
        """Create a new relation"""
        relation = Relation(
            source_id=source_id,
            source_type=source_type,
            target_id=target_id,
            target_type=target_type,
            relation_type=relation_type,
            strength=strength,
            **kwargs
        )
        session.add(relation)
        session.flush()
        logger.info(f"Created relation: {source_type}:{source_id} --[{relation_type}]--> {target_type}:{target_id}")
        return relation

    @staticmethod
    def get_by_id(session: Session, relation_id: int) -> Optional[Relation]:
        """Get relation by ID"""
        return session.query(Relation).filter(Relation.id == relation_id).first()

    @staticmethod
    def get_relations_from(
        session: Session,
        source_id: int,
        source_type: str
    ) -> List[Relation]:
        """Get all relations from a source entity"""
        return session.query(Relation).filter(
            and_(
                Relation.source_id == source_id,
                Relation.source_type == source_type
            )
        ).all()

    @staticmethod
    def get_relations_to(
        session: Session,
        target_id: int,
        target_type: str
    ) -> List[Relation]:
        """Get all relations to a target entity"""
        return session.query(Relation).filter(
            and_(
                Relation.target_id == target_id,
                Relation.target_type == target_type
            )
        ).all()

    @staticmethod
    def get_by_type(session: Session, relation_type: str) -> List[Relation]:
        """Get all relations of a specific type"""
        return session.query(Relation).filter(
            Relation.relation_type == relation_type
        ).all()

    @staticmethod
    def delete(session: Session, relation_id: int) -> bool:
        """Delete relation"""
        relation = session.query(Relation).filter(Relation.id == relation_id).first()
        if relation:
            session.delete(relation)
            session.flush()
            logger.info(f"Deleted relation ID: {relation_id}")
            return True
        return False


# ============================================================================
# AUTOMATION RUNS CRUD
# ============================================================================

class AutomationRunCRUD:
    """CRUD operations for automation runs"""

    @staticmethod
    def create(
        session: Session,
        repo_id: int,
        pipeline_name: str,
        status: str = 'pending',
        **kwargs
    ) -> AutomationRun:
        """Create a new automation run"""
        run = AutomationRun(
            repo_id=repo_id,
            pipeline_name=pipeline_name,
            status=status,
            **kwargs
        )
        session.add(run)
        session.flush()
        logger.info(f"Created automation run: {pipeline_name} for repo {repo_id}")
        return run

    @staticmethod
    def get_by_id(session: Session, run_id: int) -> Optional[AutomationRun]:
        """Get automation run by ID"""
        return session.query(AutomationRun).filter(AutomationRun.id == run_id).first()

    @staticmethod
    def get_by_repo(session: Session, repo_id: int) -> List[AutomationRun]:
        """Get all automation runs for a repository"""
        return session.query(AutomationRun).filter(
            AutomationRun.repo_id == repo_id
        ).order_by(AutomationRun.created_at.desc()).all()

    @staticmethod
    def update_status(
        session: Session,
        run_id: int,
        status: str,
        error_message: Optional[str] = None
    ) -> Optional[AutomationRun]:
        """Update automation run status"""
        run = session.query(AutomationRun).filter(AutomationRun.id == run_id).first()
        if run:
            run.status = status
            if error_message:
                run.error_message = error_message
            if status == 'success' or status == 'failure':
                run.completed_at = datetime.utcnow()
                if run.started_at:
                    run.duration_seconds = int((run.completed_at - run.started_at).total_seconds())
            session.flush()
            logger.info(f"Updated automation run {run_id}: {status}")
        return run


# ============================================================================
# USERS CRUD
# ============================================================================

class UserCRUD:
    """CRUD operations for users"""

    @staticmethod
    def create(
        session: Session,
        username: str,
        password_hash: str,
        role: str = 'readonly',
        **kwargs
    ) -> User:
        """Create a new user"""
        user = User(
            username=username,
            password_hash=password_hash,
            role=role,
            **kwargs
        )
        session.add(user)
        session.flush()
        logger.info(f"Created user: {username} with role: {role}")
        return user

    @staticmethod
    def get_by_id(session: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return session.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_username(session: Session, username: str) -> Optional[User]:
        """Get user by username"""
        return session.query(User).filter(User.username == username).first()

    @staticmethod
    def update_last_login(session: Session, user_id: int) -> Optional[User]:
        """Update user's last login timestamp"""
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            user.last_login_at = datetime.utcnow()
            session.flush()
        return user


# ============================================================================
# AUDIT LOG CRUD
# ============================================================================

class AuditLogCRUD:
    """CRUD operations for audit log"""

    @staticmethod
    def create(
        session: Session,
        event_type: str,
        action: str,
        success: bool,
        user_id: Optional[int] = None,
        username: Optional[str] = None,
        **kwargs
    ) -> AuditLog:
        """Create a new audit log entry"""
        log_entry = AuditLog(
            event_type=event_type,
            action=action,
            success=success,
            user_id=user_id,
            username=username,
            **kwargs
        )
        session.add(log_entry)
        session.flush()
        return log_entry

    @staticmethod
    def get_by_user(session: Session, user_id: int, limit: int = 100) -> List[AuditLog]:
        """Get audit logs for a specific user"""
        return session.query(AuditLog).filter(
            AuditLog.user_id == user_id
        ).order_by(AuditLog.timestamp.desc()).limit(limit).all()

    @staticmethod
    def get_by_event_type(session: Session, event_type: str, limit: int = 100) -> List[AuditLog]:
        """Get audit logs by event type"""
        return session.query(AuditLog).filter(
            AuditLog.event_type == event_type
        ).order_by(AuditLog.timestamp.desc()).limit(limit).all()

    @staticmethod
    def get_recent(session: Session, limit: int = 100) -> List[AuditLog]:
        """Get recent audit logs"""
        return session.query(AuditLog).order_by(
            AuditLog.timestamp.desc()
        ).limit(limit).all()


# ============================================================================
# CONVENIENCE EXPORTS
# ============================================================================

__all__ = [
    'RepositoryCRUD',
    'PDFCRUD',
    'ConceptCRUD',
    'RelationCRUD',
    'AutomationRunCRUD',
    'UserCRUD',
    'AuditLogCRUD',
]
