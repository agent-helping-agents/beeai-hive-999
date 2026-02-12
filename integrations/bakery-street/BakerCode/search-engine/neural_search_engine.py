#!/usr/bin/env python3
"""
NEURAL SEARCH ENGINE
Advanced AI-powered search with semantic understanding
Based on original search engine components from portfolio
Vector embeddings, neural ranking, real-time indexing
"""

import asyncio
import json
import time
import hashlib
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any, Optional, Set
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import sqlite3
import aiohttp
import re
from collections import defaultdict, Counter
import math

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SearchType(Enum):
    WEB = "web"
    SEMANTIC = "semantic"
    CODE = "code"
    DOCUMENT = "document"
    IMAGE = "image"
    REAL_TIME = "real_time"

class ContentType(Enum):
    TEXT = "text"
    HTML = "html"
    CODE = "code"
    PDF = "pdf"
    JSON = "json"
    MARKDOWN = "markdown"

class RankingFactor(Enum):
    RELEVANCE = "relevance"
    FRESHNESS = "freshness"
    AUTHORITY = "authority"
    USER_ENGAGEMENT = "user_engagement"
    SEMANTIC_SIMILARITY = "semantic_similarity"

@dataclass
class SearchQuery:
    id: str
    query: str
    search_type: SearchType
    user_id: Optional[str]
    filters: Dict[str, Any]
    timestamp: datetime
    location: Optional[str] = None
    language: str = "en"
    max_results: int = 10

@dataclass
class Document:
    id: str
    url: str
    title: str
    content: str
    content_type: ContentType
    metadata: Dict[str, Any]
    indexed_at: datetime
    last_updated: datetime
    embedding: Optional[List[float]] = None
    page_rank: float = 0.0
    quality_score: float = 0.0

@dataclass
class SearchResult:
    document_id: str
    title: str
    url: str
    snippet: str
    relevance_score: float
    ranking_factors: Dict[str, float]
    metadata: Dict[str, Any]

class TextProcessor:
    """Advanced text processing and analysis"""
    
    def __init__(self):
        self.stop_words = {
            'en': {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        }
        self.stemming_rules = {
            'ing': '',
            'ed': '',
            'er': '',
            'est': '',
            'ly': '',
            'tion': 't',
            'sion': 's'
        }
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        # Convert to lowercase and split on non-alphanumeric characters
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens
    
    def remove_stop_words(self, tokens: List[str], language: str = 'en') -> List[str]:
        """Remove stop words from tokens"""
        stop_words = self.stop_words.get(language, set())
        return [token for token in tokens if token not in stop_words]
    
    def stem_word(self, word: str) -> str:
        """Simple stemming algorithm"""
        for suffix, replacement in self.stemming_rules.items():
            if word.endswith(suffix) and len(word) > len(suffix) + 2:
                return word[:-len(suffix)] + replacement
        return word
    
    def stem_tokens(self, tokens: List[str]) -> List[str]:
        """Apply stemming to tokens"""
        return [self.stem_word(token) for token in tokens]
    
    def extract_keywords(self, text: str, max_keywords: int = 20) -> List[Tuple[str, float]]:
        """Extract keywords with TF-IDF-like scoring"""
        tokens = self.tokenize(text)
        tokens = self.remove_stop_words(tokens)
        tokens = self.stem_tokens(tokens)
        
        # Calculate term frequency
        term_freq = Counter(tokens)
        total_terms = len(tokens)
        
        # Simple keyword scoring (would use IDF in production)
        keywords = []
        for term, freq in term_freq.items():
            if len(term) > 2:  # Skip very short terms
                score = freq / total_terms
                # Boost longer terms
                score *= min(2.0, len(term) / 5.0)
                keywords.append((term, score))
        
        # Sort by score and return top keywords
        keywords.sort(key=lambda x: x[1], reverse=True)
        return keywords[:max_keywords]
    
    def generate_snippet(self, content: str, query: str, max_length: int = 200) -> str:
        """Generate search result snippet"""
        query_terms = self.tokenize(query)
        content_lower = content.lower()
        
        # Find the best position to start the snippet
        best_pos = 0
        best_score = 0
        
        for i in range(0, len(content) - max_length, 50):
            snippet = content[i:i + max_length].lower()
            score = sum(1 for term in query_terms if term in snippet)
            if score > best_score:
                best_score = score
                best_pos = i
        
        # Extract snippet
        snippet = content[best_pos:best_pos + max_length]
        
        # Try to start and end at word boundaries
        if best_pos > 0:
            space_pos = snippet.find(' ')
            if space_pos > 0:
                snippet = snippet[space_pos + 1:]
        
        last_space = snippet.rfind(' ')
        if last_space > max_length * 0.8:
            snippet = snippet[:last_space]
        
        # Add ellipsis if needed
        if best_pos > 0:
            snippet = "..." + snippet
        if best_pos + len(snippet) < len(content):
            snippet = snippet + "..."
        
        return snippet.strip()

class VectorEmbedding:
    """Simple vector embedding system (would use transformers in production)"""
    
    def __init__(self, dimension: int = 300):
        self.dimension = dimension
        self.word_vectors = {}
        self.vocabulary = set()
        self.initialize_embeddings()
    
    def initialize_embeddings(self):
        """Initialize with simple random embeddings (would load pre-trained in production)"""
        # This is a simplified version - in production would use Word2Vec, GloVe, or BERT
        common_words = [
            'search', 'engine', 'web', 'page', 'content', 'document', 'text', 'query',
            'result', 'rank', 'score', 'relevance', 'algorithm', 'index', 'crawl',
            'data', 'information', 'knowledge', 'semantic', 'neural', 'machine', 'learning',
            'artificial', 'intelligence', 'computer', 'science', 'technology', 'software',
            'development', 'programming', 'code', 'function', 'method', 'class', 'object'
        ]
        
        for word in common_words:
            self.word_vectors[word] = np.random.normal(0, 0.1, self.dimension)
            self.vocabulary.add(word)
    
    def get_word_vector(self, word: str) -> np.ndarray:
        """Get vector for a word"""
        if word in self.word_vectors:
            return self.word_vectors[word]
        else:
            # Generate random vector for unknown words
            vector = np.random.normal(0, 0.1, self.dimension)
            self.word_vectors[word] = vector
            self.vocabulary.add(word)
            return vector
    
    def embed_text(self, text: str) -> np.ndarray:
        """Create embedding for text"""
        processor = TextProcessor()
        tokens = processor.tokenize(text)
        tokens = processor.remove_stop_words(tokens)
        tokens = processor.stem_tokens(tokens)
        
        if not tokens:
            return np.zeros(self.dimension)
        
        # Average word vectors
        vectors = [self.get_word_vector(token) for token in tokens]
        return np.mean(vectors, axis=0)
    
    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between vectors"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)

class SearchIndex:
    """Inverted index for fast text search"""
    
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.text_processor = TextProcessor()
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database for index"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                url TEXT,
                title TEXT,
                content TEXT,
                content_type TEXT,
                metadata TEXT,
                indexed_at TIMESTAMP,
                last_updated TIMESTAMP,
                embedding BLOB,
                page_rank REAL,
                quality_score REAL
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS inverted_index (
                term TEXT,
                document_id TEXT,
                term_frequency INTEGER,
                positions TEXT,
                PRIMARY KEY (term, document_id)
            )
        ''')
        
        self.conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_term ON inverted_index(term)
        ''')
        
        self.conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_document ON inverted_index(document_id)
        ''')
        
        self.conn.commit()
    
    def add_document(self, document: Document):
        """Add document to index"""
        # Store document
        self.conn.execute('''
            INSERT OR REPLACE INTO documents 
            (id, url, title, content, content_type, metadata, indexed_at, last_updated, page_rank, quality_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            document.id, document.url, document.title, document.content,
            document.content_type.value, json.dumps(document.metadata),
            document.indexed_at, document.last_updated,
            document.page_rank, document.quality_score
        ))
        
        # Index content
        self.index_document_content(document)
        
        self.conn.commit()
        logger.info(f"Indexed document: {document.title}")
    
    def index_document_content(self, document: Document):
        """Index document content for search"""
        # Combine title and content for indexing
        full_text = f"{document.title} {document.content}"
        tokens = self.text_processor.tokenize(full_text)
        tokens = self.text_processor.remove_stop_words(tokens)
        tokens = self.text_processor.stem_tokens(tokens)
        
        # Calculate term frequencies and positions
        term_positions = defaultdict(list)
        term_frequencies = Counter()
        
        for pos, token in enumerate(tokens):
            term_positions[token].append(pos)
            term_frequencies[token] += 1
        
        # Clear existing index entries for this document
        self.conn.execute('DELETE FROM inverted_index WHERE document_id = ?', (document.id,))
        
        # Add new index entries
        for term, frequency in term_frequencies.items():
            positions = json.dumps(term_positions[term])
            self.conn.execute('''
                INSERT INTO inverted_index (term, document_id, term_frequency, positions)
                VALUES (?, ?, ?, ?)
            ''', (term, document.id, frequency, positions))
    
    def search_documents(self, query: str, max_results: int = 10) -> List[Tuple[str, float]]:
        """Search for documents matching query"""
        query_terms = self.text_processor.tokenize(query)
        query_terms = self.text_processor.remove_stop_words(query_terms)
        query_terms = self.text_processor.stem_tokens(query_terms)
        
        if not query_terms:
            return []
        
        # Find documents containing query terms
        document_scores = defaultdict(float)
        
        for term in query_terms:
            cursor = self.conn.execute('''
                SELECT document_id, term_frequency FROM inverted_index WHERE term = ?
            ''', (term,))
            
            for doc_id, tf in cursor.fetchall():
                # Simple TF scoring (would add IDF in production)
                document_scores[doc_id] += tf
        
        # Sort by score and return top results
        sorted_docs = sorted(document_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_docs[:max_results]
    
    def get_document(self, document_id: str) -> Optional[Document]:
        """Get document by ID"""
        cursor = self.conn.execute('''
            SELECT * FROM documents WHERE id = ?
        ''', (document_id,))
        
        row = cursor.fetchone()
        if not row:
            return None
        
        return Document(
            id=row[0],
            url=row[1],
            title=row[2],
            content=row[3],
            content_type=ContentType(row[4]),
            metadata=json.loads(row[5]),
            indexed_at=datetime.fromisoformat(row[6]),
            last_updated=datetime.fromisoformat(row[7]),
            page_rank=row[9],
            quality_score=row[10]
        )

class NeuralRanker:
    """Neural ranking system for search results"""
    
    def __init__(self):
        self.embedding_system = VectorEmbedding()
        self.ranking_weights = {
            RankingFactor.RELEVANCE: 0.4,
            RankingFactor.FRESHNESS: 0.2,
            RankingFactor.AUTHORITY: 0.2,
            RankingFactor.USER_ENGAGEMENT: 0.1,
            RankingFactor.SEMANTIC_SIMILARITY: 0.1
        }
    
    def rank_results(self, query: SearchQuery, documents: List[Document]) -> List[SearchResult]:
        """Rank search results using multiple factors"""
        query_embedding = self.embedding_system.embed_text(query.query)
        results = []
        
        for doc in documents:
            # Calculate ranking factors
            factors = self.calculate_ranking_factors(query, doc, query_embedding)
            
            # Calculate overall score
            overall_score = sum(
                factors[factor] * weight 
                for factor, weight in self.ranking_weights.items()
            )
            
            # Generate snippet
            processor = TextProcessor()
            snippet = processor.generate_snippet(doc.content, query.query)
            
            result = SearchResult(
                document_id=doc.id,
                title=doc.title,
                url=doc.url,
                snippet=snippet,
                relevance_score=overall_score,
                ranking_factors=factors,
                metadata=doc.metadata
            )
            
            results.append(result)
        
        # Sort by relevance score
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results[:query.max_results]
    
    def calculate_ranking_factors(self, query: SearchQuery, document: Document, query_embedding: np.ndarray) -> Dict[RankingFactor, float]:
        """Calculate individual ranking factors"""
        factors = {}
        
        # Relevance (text matching)
        factors[RankingFactor.RELEVANCE] = self.calculate_text_relevance(query.query, document)
        
        # Freshness
        factors[RankingFactor.FRESHNESS] = self.calculate_freshness_score(document)
        
        # Authority (PageRank-like)
        factors[RankingFactor.AUTHORITY] = document.page_rank
        
        # User engagement (would be based on click-through rates, etc.)
        factors[RankingFactor.USER_ENGAGEMENT] = document.quality_score
        
        # Semantic similarity
        if document.embedding is None:
            document.embedding = self.embedding_system.embed_text(document.content)
        
        doc_embedding = np.array(document.embedding)
        factors[RankingFactor.SEMANTIC_SIMILARITY] = self.embedding_system.cosine_similarity(
            query_embedding, doc_embedding
        )
        
        return factors
    
    def calculate_text_relevance(self, query: str, document: Document) -> float:
        """Calculate text-based relevance score"""
        processor = TextProcessor()
        
        # Extract keywords from query and document
        query_keywords = dict(processor.extract_keywords(query))
        doc_keywords = dict(processor.extract_keywords(document.content))
        
        # Calculate overlap score
        overlap_score = 0.0
        total_query_weight = sum(query_keywords.values())
        
        for keyword, weight in query_keywords.items():
            if keyword in doc_keywords:
                overlap_score += (weight / total_query_weight) * doc_keywords[keyword]
        
        # Boost if query terms appear in title
        title_boost = 0.0
        query_terms = processor.tokenize(query)
        title_terms = processor.tokenize(document.title.lower())
        
        for term in query_terms:
            if term in title_terms:
                title_boost += 0.1
        
        return min(1.0, overlap_score + title_boost)
    
    def calculate_freshness_score(self, document: Document) -> float:
        """Calculate freshness score based on document age"""
        now = datetime.now()
        age_days = (now - document.last_updated).days
        
        # Exponential decay with half-life of 30 days
        return math.exp(-age_days / 30.0)

class WebCrawler:
    """Web crawler for indexing content"""
    
    def __init__(self, max_concurrent: int = 10):
        self.max_concurrent = max_concurrent
        self.crawled_urls = set()
        self.robots_cache = {}
        self.session = None
    
    async def crawl_urls(self, urls: List[str], max_depth: int = 2) -> List[Document]:
        """Crawl URLs and return documents"""
        async with aiohttp.ClientSession() as session:
            self.session = session
            documents = []
            
            for url in urls:
                try:
                    doc = await self.crawl_url(url, max_depth)
                    if doc:
                        documents.append(doc)
                except Exception as e:
                    logger.error(f"Failed to crawl {url}: {e}")
            
            return documents
    
    async def crawl_url(self, url: str, max_depth: int) -> Optional[Document]:
        """Crawl a single URL"""
        if url in self.crawled_urls or max_depth <= 0:
            return None
        
        self.crawled_urls.add(url)
        
        try:
            async with self.session.get(url, timeout=10) as response:
                if response.status != 200:
                    return None
                
                content = await response.text()
                
                # Extract title
                title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
                title = title_match.group(1) if title_match else url
                
                # Extract text content (simple HTML stripping)
                text_content = re.sub(r'<[^>]+>', ' ', content)
                text_content = re.sub(r'\s+', ' ', text_content).strip()
                
                # Create document
                document = Document(
                    id=hashlib.md5(url.encode()).hexdigest(),
                    url=url,
                    title=title,
                    content=text_content,
                    content_type=ContentType.HTML,
                    metadata={
                        'content_length': len(content),
                        'response_status': response.status,
                        'content_type': response.headers.get('content-type', '')
                    },
                    indexed_at=datetime.now(),
                    last_updated=datetime.now(),
                    page_rank=0.5,  # Default PageRank
                    quality_score=0.5  # Default quality score
                )
                
                return document
                
        except Exception as e:
            logger.error(f"Error crawling {url}: {e}")
            return None

class SearchEngine:
    """Main Neural Search Engine"""
    
    def __init__(self, db_path: str = "search_engine.db"):
        self.index = SearchIndex(db_path)
        self.ranker = NeuralRanker()
        self.crawler = WebCrawler()
        self.query_history = []
        self.performance_metrics = defaultdict(list)
        
        # Initialize with some sample documents
        self.initialize_sample_data()
        
        logger.info("🔍 Neural Search Engine initialized")
    
    def initialize_sample_data(self):
        """Initialize with sample documents"""
        sample_docs = [
            {
                'title': 'Introduction to Machine Learning',
                'content': 'Machine learning is a subset of artificial intelligence that focuses on algorithms that can learn from data. It includes supervised learning, unsupervised learning, and reinforcement learning approaches.',
                'url': 'https://example.com/ml-intro',
                'metadata': {'category': 'education', 'difficulty': 'beginner'}
            },
            {
                'title': 'Neural Networks Deep Dive',
                'content': 'Neural networks are computing systems inspired by biological neural networks. They consist of layers of interconnected nodes that process information using connectionist approaches to computation.',
                'url': 'https://example.com/neural-networks',
                'metadata': {'category': 'education', 'difficulty': 'advanced'}
            },
            {
                'title': 'Search Engine Optimization Guide',
                'content': 'SEO is the practice of increasing the quantity and quality of traffic to your website through organic search engine results. It involves keyword research, content optimization, and technical improvements.',
                'url': 'https://example.com/seo-guide',
                'metadata': {'category': 'marketing', 'difficulty': 'intermediate'}
            },
            {
                'title': 'Python Programming Tutorial',
                'content': 'Python is a high-level programming language known for its simplicity and readability. It supports multiple programming paradigms and has extensive libraries for data science, web development, and automation.',
                'url': 'https://example.com/python-tutorial',
                'metadata': {'category': 'programming', 'difficulty': 'beginner'}
            },
            {
                'title': 'Advanced Database Design',
                'content': 'Database design involves creating a detailed data model of a database. This includes defining tables, relationships, indexes, and constraints to ensure data integrity and optimal performance.',
                'url': 'https://example.com/database-design',
                'metadata': {'category': 'database', 'difficulty': 'advanced'}
            }
        ]
        
        for doc_data in sample_docs:
            document = Document(
                id=hashlib.md5(doc_data['url'].encode()).hexdigest(),
                url=doc_data['url'],
                title=doc_data['title'],
                content=doc_data['content'],
                content_type=ContentType.TEXT,
                metadata=doc_data['metadata'],
                indexed_at=datetime.now(),
                last_updated=datetime.now(),
                page_rank=0.5,
                quality_score=0.7
            )
            self.index.add_document(document)
    
    async def search(self, query_text: str, search_type: SearchType = SearchType.SEMANTIC, 
                    user_id: Optional[str] = None, filters: Dict[str, Any] = None,
                    max_results: int = 10) -> Dict[str, Any]:
        """Perform search query"""
        start_time = time.time()
        
        # Create search query
        query = SearchQuery(
            id=hashlib.md5(f"{query_text}_{time.time()}".encode()).hexdigest()[:8],
            query=query_text,
            search_type=search_type,
            user_id=user_id,
            filters=filters or {},
            timestamp=datetime.now(),
            max_results=max_results
        )
        
        # Store query in history
        self.query_history.append(query)
        
        try:
            # Search index for matching documents
            matching_docs = self.index.search_documents(query.query, max_results * 2)
            
            # Get full document objects
            documents = []
            for doc_id, score in matching_docs:
                doc = self.index.get_document(doc_id)
                if doc:
                    documents.append(doc)
            
            # Apply filters
            if query.filters:
                documents = self.apply_filters(documents, query.filters)
            
            # Rank results
            results = self.ranker.rank_results(query, documents)
            
            # Calculate performance metrics
            search_time = time.time() - start_time
            self.performance_metrics['search_time'].append(search_time)
            self.performance_metrics['results_count'].append(len(results))
            
            logger.info(f"Search completed: '{query.query}' - {len(results)} results in {search_time:.3f}s")
            
            return {
                'query_id': query.id,
                'query': query.query,
                'search_type': search_type.value,
                'results': [asdict(result) for result in results],
                'total_results': len(results),
                'search_time': search_time,
                'timestamp': query.timestamp.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            return {
                'query_id': query.id,
                'query': query.query,
                'error': str(e),
                'results': [],
                'total_results': 0,
                'search_time': time.time() - start_time
            }
    
    def apply_filters(self, documents: List[Document], filters: Dict[str, Any]) -> List[Document]:
        """Apply filters to search results"""
        filtered_docs = []
        
        for doc in documents:
            include_doc = True
            
            # Category filter
            if 'category' in filters:
                doc_category = doc.metadata.get('category', '')
                if doc_category != filters['category']:
                    include_doc = False
            
            # Difficulty filter
            if 'difficulty' in filters:
                doc_difficulty = doc.metadata.get('difficulty', '')
                if doc_difficulty != filters['difficulty']:
                    include_doc = False
            
            # Date range filter
            if 'date_from' in filters:
                date_from = datetime.fromisoformat(filters['date_from'])
                if doc.last_updated < date_from:
                    include_doc = False
            
            if 'date_to' in filters:
                date_to = datetime.fromisoformat(filters['date_to'])
                if doc.last_updated > date_to:
                    include_doc = False
            
            if include_doc:
                filtered_docs.append(doc)
        
        return filtered_docs
    
    async def index_url(self, url: str) -> Dict[str, Any]:
        """Index a single URL"""
        try:
            documents = await self.crawler.crawl_urls([url], max_depth=1)
            
            indexed_count = 0
            for doc in documents:
                self.index.add_document(doc)
                indexed_count += 1
            
            return {
                'status': 'success',
                'url': url,
                'documents_indexed': indexed_count
            }
            
        except Exception as e:
            logger.error(f"Failed to index URL {url}: {e}")
            return {
                'status': 'error',
                'url': url,
                'error': str(e)
            }
    
    async def index_urls(self, urls: List[str], max_depth: int = 2) -> Dict[str, Any]:
        """Index multiple URLs"""
        try:
            documents = await self.crawler.crawl_urls(urls, max_depth)
            
            indexed_count = 0
            for doc in documents:
                self.index.add_document(doc)
                indexed_count += 1
            
            return {
                'status': 'success',
                'urls_processed': len(urls),
                'documents_indexed': indexed_count
            }
            
        except Exception as e:
            logger.error(f"Failed to index URLs: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def get_search_suggestions(self, partial_query: str, max_suggestions: int = 5) -> List[str]:
        """Get search suggestions based on partial query"""
        suggestions = []
        
        # Simple suggestion based on query history
        for query in self.query_history:
            if partial_query.lower() in query.query.lower():
                suggestions.append(query.query)
        
        # Remove duplicates and limit results
        suggestions = list(set(suggestions))
        return suggestions[:max_suggestions]
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get search engine analytics"""
        total_queries = len(self.query_history)
        avg_search_time = np.mean(self.performance_metrics['search_time']) if self.performance_metrics['search_time'] else 0
        avg_results = np.mean(self.performance_metrics['results_count']) if self.performance_metrics['results_count'] else 0
        
        # Query analysis
        query_types = Counter(query.search_type.value for query in self.query_history)
        popular_queries = Counter(query.query for query in self.query_history).most_common(10)
        
        return {
            'total_queries': total_queries,
            'average_search_time': avg_search_time,
            'average_results_per_query': avg_results,
            'query_types': dict(query_types),
            'popular_queries': popular_queries,
            'indexed_documents': self.get_document_count(),
            'uptime': time.time()  # Would be actual uptime
        }
    
    def get_document_count(self) -> int:
        """Get total number of indexed documents"""
        cursor = self.index.conn.execute('SELECT COUNT(*) FROM documents')
        return cursor.fetchone()[0]

# Example usage and testing
if __name__ == "__main__":
    print("🔍 NEURAL SEARCH ENGINE")
    print("=======================")
    print("Advanced AI-Powered Search System")
    print("- Semantic Understanding")
    print("- Vector Embeddings")
    print("- Neural Ranking")
    print("- Real-time Indexing")
    print("- Web Crawling")
    print()
    
    # Initialize search engine
    search_engine = SearchEngine()
    
    # Example searches
    async def demo_search():
        print("🔍 Demo Search Queries:")
        print()
        
        # Search for machine learning
        result1 = await search_engine.search("machine learning algorithms")
        print(f"Query: 'machine learning algorithms'")
        print(f"Results: {result1['total_results']}")
        print(f"Search time: {result1['search_time']:.3f}s")
        print()
        
        # Search with filters
        result2 = await search_engine.search(
            "programming tutorial", 
            filters={'category': 'programming', 'difficulty': 'beginner'}
        )
        print(f"Query: 'programming tutorial' (filtered)")
        print(f"Results: {result2['total_results']}")
        print()
        
        # Semantic search
        result3 = await search_engine.search(
            "neural networks deep learning", 
            search_type=SearchType.SEMANTIC
        )
        print(f"Query: 'neural networks deep learning' (semantic)")
        print(f"Results: {result3['total_results']}")
        print()
        
        # Analytics
        analytics = search_engine.get_analytics()
        print("📊 Search Analytics:")
        print(f"Total queries: {analytics['total_queries']}")
        print(f"Average search time: {analytics['average_search_time']:.3f}s")
        print(f"Indexed documents: {analytics['indexed_documents']}")
    
    # Run demo
    import asyncio
    asyncio.run(demo_search())