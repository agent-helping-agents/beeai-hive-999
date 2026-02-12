-- Energetic Lexicon Database Schema
-- 🔒 PRIVATE - PROPRIETARY
-- © 2025 Bakery Street Project
--
-- SQLite database schema for unified knowledge graph
-- Designed for migration to PostgreSQL if needed

-- ============================================================================
-- REPOSITORIES TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS repos (
    -- Primary key
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Core metadata
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    url TEXT NOT NULL,

    -- Repository attributes
    is_private BOOLEAN NOT NULL DEFAULT 1,
    language TEXT,
    stars INTEGER DEFAULT 0,
    forks INTEGER DEFAULT 0,

    -- Classification
    automation_role TEXT,  -- e.g., "CI/CD template", "AI framework", "DevOps"
    geometry_quadrant TEXT CHECK(geometry_quadrant IN (
        'theoretical',
        'experimental',
        'implementation',
        'interdisciplinary'
    )),

    -- Tags (JSON array stored as text in SQLite)
    tags TEXT,  -- JSON: ["automation", "AI", "security"]

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_synced_at TIMESTAMP,

    -- GitHub metadata
    github_id INTEGER UNIQUE,
    default_branch TEXT DEFAULT 'main',

    -- Flags
    is_archived BOOLEAN DEFAULT 0,
    is_fork BOOLEAN DEFAULT 0,

    -- Full-text search support
    readme_content TEXT,
    topics TEXT  -- JSON array
);

CREATE INDEX idx_repos_name ON repos(name);
CREATE INDEX idx_repos_quadrant ON repos(geometry_quadrant);
CREATE INDEX idx_repos_private ON repos(is_private);
CREATE INDEX idx_repos_language ON repos(language);

-- ============================================================================
-- PDFS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS pdfs (
    -- Primary key
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Core metadata
    title TEXT NOT NULL,
    file_path TEXT NOT NULL UNIQUE,
    file_hash TEXT NOT NULL,  -- SHA256 hash for deduplication

    -- PDF attributes
    page_count INTEGER,
    file_size INTEGER,  -- bytes

    -- Content
    extracted_text TEXT,  -- Full text extracted from PDF

    -- Embedding metadata
    indexed_at TIMESTAMP,
    embedding_model TEXT,  -- e.g., "all-MiniLM-L6-v2"
    embedding_dimensions INTEGER,

    -- Classification
    tags TEXT,  -- JSON array
    category TEXT,  -- e.g., "research", "documentation", "guide"

    -- Relationships
    related_repo_id INTEGER,
    FOREIGN KEY (related_repo_id) REFERENCES repos(id) ON DELETE SET NULL,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_pdfs_hash ON pdfs(file_hash);
CREATE INDEX idx_pdfs_title ON pdfs(title);
CREATE INDEX idx_pdfs_category ON pdfs(category);
CREATE INDEX idx_pdfs_repo ON pdfs(related_repo_id);

-- ============================================================================
-- CONCEPTS TABLE (Energetic Lexicon)
-- ============================================================================

CREATE TABLE IF NOT EXISTS concepts (
    -- Primary key
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Core definition
    term TEXT NOT NULL UNIQUE,
    definition TEXT NOT NULL,

    -- Extended definition
    excluded_meanings TEXT,  -- What this term does NOT mean (JSON array)
    metaphors TEXT,  -- Metaphorical explanations (JSON array)

    -- Classification
    domain TEXT,  -- e.g., "tech", "science", "business", "security"
    abstraction_level INTEGER CHECK(abstraction_level BETWEEN 1 AND 5),

    -- Context
    first_seen_in TEXT,  -- Repo name or PDF title
    usage_examples TEXT,  -- JSON array of usage examples

    -- Relationships (see relations table for graph)
    parent_concept_id INTEGER,
    FOREIGN KEY (parent_concept_id) REFERENCES concepts(id) ON DELETE SET NULL,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_concepts_term ON concepts(term);
CREATE INDEX idx_concepts_domain ON concepts(domain);
CREATE INDEX idx_concepts_parent ON concepts(parent_concept_id);

-- ============================================================================
-- RELATIONS TABLE (Knowledge Graph Edges)
-- ============================================================================

CREATE TABLE IF NOT EXISTS relations (
    -- Primary key
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Graph edge definition
    source_id INTEGER NOT NULL,
    source_type TEXT NOT NULL CHECK(source_type IN ('repo', 'pdf', 'concept')),

    target_id INTEGER NOT NULL,
    target_type TEXT NOT NULL CHECK(target_type IN ('repo', 'pdf', 'concept')),

    -- Relationship metadata
    relation_type TEXT NOT NULL,  -- e.g., "depends_on", "references", "implements", "extends"
    strength REAL DEFAULT 1.0 CHECK(strength BETWEEN 0.0 AND 1.0),

    -- Context
    evidence TEXT,  -- Why this relation exists (commit message, code reference, etc.)

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Ensure unique relations
    UNIQUE(source_id, source_type, target_id, target_type, relation_type)
);

CREATE INDEX idx_relations_source ON relations(source_id, source_type);
CREATE INDEX idx_relations_target ON relations(target_id, target_type);
CREATE INDEX idx_relations_type ON relations(relation_type);

-- ============================================================================
-- AUTOMATION RUNS TABLE (CI/CD Tracking)
-- ============================================================================

CREATE TABLE IF NOT EXISTS automation_runs (
    -- Primary key
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Run metadata
    repo_id INTEGER NOT NULL,
    FOREIGN KEY (repo_id) REFERENCES repos(id) ON DELETE CASCADE,

    -- Pipeline information
    pipeline_name TEXT NOT NULL,  -- e.g., "update-repos", "index-pdfs", "backup"
    run_id TEXT,  -- GitHub Actions run ID or external identifier

    -- Status
    status TEXT NOT NULL CHECK(status IN ('pending', 'running', 'success', 'failure', 'cancelled')),

    -- Results
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    duration_seconds INTEGER,

    -- Logs (encrypted separately if sensitive)
    logs_path TEXT,  -- Path to log file
    error_message TEXT,

    -- Metrics
    records_processed INTEGER DEFAULT 0,
    records_updated INTEGER DEFAULT 0,
    records_failed INTEGER DEFAULT 0,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_automation_repo ON automation_runs(repo_id);
CREATE INDEX idx_automation_status ON automation_runs(status);
CREATE INDEX idx_automation_pipeline ON automation_runs(pipeline_name);

-- ============================================================================
-- USERS TABLE (Authentication & Authorization)
-- ============================================================================

CREATE TABLE IF NOT EXISTS users (
    -- Primary key
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Authentication
    username TEXT NOT NULL UNIQUE,
    email TEXT UNIQUE,
    password_hash TEXT NOT NULL,  -- bcrypt hash

    -- Authorization
    role TEXT NOT NULL DEFAULT 'readonly' CHECK(role IN ('admin', 'developer', 'readonly')),

    -- API access
    api_key_hash TEXT UNIQUE,
    api_key_created_at TIMESTAMP,
    api_key_expires_at TIMESTAMP,

    -- Status
    is_active BOOLEAN DEFAULT 1,
    last_login_at TIMESTAMP,

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_active ON users(is_active);

-- ============================================================================
-- AUDIT LOG TABLE (Security & Compliance)
-- ============================================================================

CREATE TABLE IF NOT EXISTS audit_log (
    -- Primary key
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Event metadata
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    event_type TEXT NOT NULL,  -- e.g., "create", "read", "update", "delete", "login", "logout"

    -- User information
    user_id INTEGER,
    username TEXT,
    ip_address TEXT,

    -- Action details
    table_name TEXT,  -- Which table was affected
    record_id INTEGER,  -- Which record was affected
    action TEXT NOT NULL,

    -- Before/after state (JSON)
    old_values TEXT,
    new_values TEXT,

    -- Result
    success BOOLEAN NOT NULL,
    error_message TEXT,

    -- Context
    request_id TEXT,  -- For tracing across multiple log entries
    user_agent TEXT
);

CREATE INDEX idx_audit_timestamp ON audit_log(timestamp);
CREATE INDEX idx_audit_user ON audit_log(user_id);
CREATE INDEX idx_audit_event ON audit_log(event_type);
CREATE INDEX idx_audit_table ON audit_log(table_name);

-- ============================================================================
-- VIEWS (Convenience queries)
-- ============================================================================

-- Active repositories with recent activity
CREATE VIEW IF NOT EXISTS active_repos AS
SELECT
    r.*,
    COUNT(DISTINCT ar.id) as automation_run_count,
    MAX(ar.completed_at) as last_automation_run
FROM repos r
LEFT JOIN automation_runs ar ON r.id = ar.repo_id
WHERE r.is_archived = 0
GROUP BY r.id
ORDER BY last_automation_run DESC;

-- Concept graph (direct relationships)
CREATE VIEW IF NOT EXISTS concept_graph AS
SELECT
    c1.term as source_term,
    rel.relation_type,
    c2.term as target_term,
    rel.strength,
    rel.evidence
FROM relations rel
JOIN concepts c1 ON rel.source_id = c1.id AND rel.source_type = 'concept'
JOIN concepts c2 ON rel.target_id = c2.id AND rel.target_type = 'concept';

-- Repository knowledge graph (repos + concepts + PDFs)
CREATE VIEW IF NOT EXISTS knowledge_graph AS
SELECT
    rel.id,
    rel.source_type || ':' || rel.source_id as source,
    rel.target_type || ':' || rel.target_id as target,
    rel.relation_type,
    rel.strength,
    CASE rel.source_type
        WHEN 'repo' THEN (SELECT name FROM repos WHERE id = rel.source_id)
        WHEN 'concept' THEN (SELECT term FROM concepts WHERE id = rel.source_id)
        WHEN 'pdf' THEN (SELECT title FROM pdfs WHERE id = rel.source_id)
    END as source_name,
    CASE rel.target_type
        WHEN 'repo' THEN (SELECT name FROM repos WHERE id = rel.target_id)
        WHEN 'concept' THEN (SELECT term FROM concepts WHERE id = rel.target_id)
        WHEN 'pdf' THEN (SELECT title FROM pdfs WHERE id = rel.target_id)
    END as target_name
FROM relations rel;

-- ============================================================================
-- TRIGGERS (Auto-update timestamps)
-- ============================================================================

-- Update repos.updated_at on modification
CREATE TRIGGER IF NOT EXISTS update_repos_timestamp
AFTER UPDATE ON repos
FOR EACH ROW
BEGIN
    UPDATE repos SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

-- Update concepts.updated_at on modification
CREATE TRIGGER IF NOT EXISTS update_concepts_timestamp
AFTER UPDATE ON concepts
FOR EACH ROW
BEGIN
    UPDATE concepts SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

-- Update pdfs.updated_at on modification
CREATE TRIGGER IF NOT EXISTS update_pdfs_timestamp
AFTER UPDATE ON pdfs
FOR EACH ROW
BEGIN
    UPDATE pdfs SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

-- Update users.updated_at on modification
CREATE TRIGGER IF NOT EXISTS update_users_timestamp
AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

-- ============================================================================
-- SAMPLE DATA (Development/Testing)
-- ============================================================================

-- Insert sample admin user (password: changeme - CHANGE THIS IN PRODUCTION)
INSERT OR IGNORE INTO users (username, email, password_hash, role, is_active)
VALUES (
    'admin',
    'admin@bakerystreet.local',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS6NovFW6',  -- bcrypt: "changeme"
    'admin',
    1
);

-- Insert sample concepts
INSERT OR IGNORE INTO concepts (term, definition, domain, abstraction_level)
VALUES
    ('AutomationCodex', 'Automation-first philosophy underlying all Bakery Street infrastructure', 'tech', 4),
    ('Research Geometry', 'Framework treating research as geometric/coordinate space rather than Q&A', 'science', 5),
    ('Energetic Lexicon', 'Unified knowledge graph of entire Bakery Street ecosystem', 'tech', 4);

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================
