# ===== HUMAN-AI COLLABORATIVE AUDITING INTERFACE =====
# Advanced Interactive Query Processing and Collaborative Decision-Making
# Human-in-the-Loop Validation and Audit Session Management

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import re
import json
import warnings
warnings.filterwarnings('ignore')

class NaturalLanguageQueryProcessor:
    """
    Natural language query processing for audit investigations
    Based on: "Interactive Entity Search with Natural Language Queries"
    """

    def __init__(self):
        self.query_patterns = {
            'entity_search': [
                r'find.*entities?.*related to',
                r'search.*for.*entities?.*with',
                r'locate.*entities?.*connected to',
                r'identify.*entities?.*associated with'
            ],
            'relationship_analysis': [
                r'how.*connected',
                r'what.*relationship.*between',
                r'analyze.*connections.*between',
                r'examine.*links.*between'
            ],
            'temporal_analysis': [
                r'when.*happened',
                r'timeline.*of',
                r'evolution.*over.*time',
                r'changes.*over.*time'
            ],
            'anomaly_investigation': [
                r'investigate.*unusual',
                r'examine.*anomalies?.*in',
                r'analyze.*suspicious.*activity',
                r'review.*outliers.*in'
            ],
            'impact_assessment': [
                r'impact.*of',
                r'effect.*on',
                r'influence.*of',
                r'consequences.*of'
            ]
        }

        self.entity_keywords = [
            'blackrock', 'biden', 'deese', 'adeyemo', 'pyle', 'fink',
            'sec', 'fed', 'treasury', 'democrat', 'republican',
            'climate', 'esg', 'proxy', 'voting', 'lobbying'
        ]

        self.query_history = []

    def process_query(self, query_text: str, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process natural language query and generate AI-powered response
        """
        query_lower = query_text.lower()

        # Analyze query intent
        intent_analysis = self._analyze_query_intent(query_lower)

        # Extract entities and keywords
        entity_extraction = self._extract_entities_and_keywords(query_lower)

        # Generate AI suggestions
        ai_suggestions = self._generate_ai_suggestions(intent_analysis, entity_extraction, context_data)

        # Create collaborative response
        collaborative_response = {
            'original_query': query_text,
            'intent_analysis': intent_analysis,
            'entity_extraction': entity_extraction,
            'ai_suggestions': ai_suggestions,
            'confidence_score': self._calculate_query_confidence(intent_analysis, entity_extraction),
            'follow_up_questions': self._generate_follow_up_questions(intent_analysis),
            'processing_timestamp': datetime.now(),
            'session_context': context_data.get('session_id', 'unknown')
        }

        # Store query for learning
        self.query_history.append(collaborative_response)

        return collaborative_response

    def _analyze_query_intent(self, query_text: str) -> Dict[str, Any]:
        """Analyze the intent of the query"""
        intent_scores = {}

        for intent_type, patterns in self.query_patterns.items():
            max_score = 0
            for pattern in patterns:
                matches = re.findall(pattern, query_text, re.IGNORECASE)
                if matches:
                    score = len(matches) * len(pattern.split()) / len(query_text.split())
                    max_score = max(max_score, score)

            intent_scores[intent_type] = max_score

        # Determine primary intent
        primary_intent = max(intent_scores.items(), key=lambda x: x[1])

        return {
            'primary_intent': primary_intent[0],
            'intent_confidence': primary_intent[1],
            'all_intents': intent_scores,
            'query_complexity': self._assess_query_complexity(query_text)
        }

    def _extract_entities_and_keywords(self, query_text: str) -> Dict[str, Any]:
        """Extract entities and keywords from query"""
        words = query_text.split()
        entities_found = []
        keywords_found = []

        # Find entity matches
        for word in words:
            word_lower = word.lower().strip('.,!?')
            if word_lower in self.entity_keywords:
                entities_found.append({
                    'entity': word,
                    'type': self._classify_entity(word_lower),
                    'confidence': 0.9
                })

        # Extract additional keywords
        for word in words:
            if len(word) > 3 and word.lower() not in ['find', 'search', 'analyze', 'what', 'how', 'when']:
                keywords_found.append(word.lower())

        return {
            'entities': entities_found,
            'keywords': list(set(keywords_found)),
            'query_structure': self._analyze_query_structure(query_text)
        }

    def _classify_entity(self, entity: str) -> str:
        """Classify entity type"""
        person_entities = ['fink', 'deese', 'adeyemo', 'pyle', 'biden']
        org_entities = ['blackrock', 'sec', 'fed', 'treasury']
        political_entities = ['democrat', 'republican']
        policy_entities = ['climate', 'esg', 'proxy', 'voting', 'lobbying']

        if entity in person_entities:
            return 'person'
        elif entity in org_entities:
            return 'organization'
        elif entity in political_entities:
            return 'political'
        elif entity in policy_entities:
            return 'policy'
        else:
            return 'other'

    def _analyze_query_structure(self, query_text: str) -> Dict[str, Any]:
        """Analyze the structural elements of the query"""
        structure = {
            'has_question_word': any(word in query_text.lower() for word in ['what', 'how', 'when', 'where', 'why', 'who']),
            'has_comparison': any(word in query_text.lower() for word in ['versus', 'vs', 'compared', 'versus']),
            'has_temporal_element': any(word in query_text.lower() for word in ['when', 'time', 'timeline', 'evolution', 'changes']),
            'has_quantitative_element': any(word in query_text.lower() for word in ['how many', 'how much', 'percentage', 'amount']),
            'sentence_count': len([s for s in query_text.split('.') if s.strip()])
        }

        return structure

    def _generate_ai_suggestions(self, intent_analysis: Dict, entity_extraction: Dict, context_data: Dict) -> List[Dict[str, Any]]:
        """Generate AI-powered suggestions based on query analysis"""
        suggestions = []

        intent = intent_analysis['primary_intent']
        entities = entity_extraction['entities']

        if intent == 'entity_search':
            suggestions.extend(self._generate_entity_search_suggestions(entities, context_data))

        elif intent == 'relationship_analysis':
            suggestions.extend(self._generate_relationship_suggestions(entities, context_data))

        elif intent == 'temporal_analysis':
            suggestions.extend(self._generate_temporal_suggestions(entities, context_data))

        elif intent == 'anomaly_investigation':
            suggestions.extend(self._generate_anomaly_suggestions(entities, context_data))

        elif intent == 'impact_assessment':
            suggestions.extend(self._generate_impact_suggestions(entities, context_data))

        # Add general suggestions
        suggestions.extend(self._generate_general_suggestions(intent_analysis, entity_extraction))

        return suggestions[:5]  # Limit to top 5 suggestions

    def _generate_entity_search_suggestions(self, entities: List, context_data: Dict) -> List[Dict]:
        """Generate suggestions for entity search queries"""
        suggestions = []

        if entities:
            entity_names = [e['entity'] for e in entities]
            suggestions.append({
                'type': 'entity_expansion',
                'description': f"Search for entities connected to {', '.join(entity_names)}",
                'confidence': 0.9,
                'action': 'expand_entity_network'
            })

        suggestions.append({
            'type': 'relationship_mapping',
            'description': 'Map relationships between identified entities',
            'confidence': 0.8,
            'action': 'generate_relationship_map'
        })

        return suggestions

    def _generate_relationship_suggestions(self, entities: List, context_data: Dict) -> List[Dict]:
        """Generate suggestions for relationship analysis"""
        suggestions = []

        if len(entities) >= 2:
            suggestions.append({
                'type': 'relationship_depth',
                'description': 'Analyze multi-step relationships and indirect connections',
                'confidence': 0.85,
                'action': 'analyze_relationship_depth'
            })

        suggestions.append({
            'type': 'influence_pathways',
            'description': 'Identify pathways of influence and power dynamics',
            'confidence': 0.8,
            'action': 'map_influence_pathways'
        })

        return suggestions

    def _generate_temporal_suggestions(self, entities: List, context_data: Dict) -> List[Dict]:
        """Generate suggestions for temporal analysis"""
        suggestions = []

        suggestions.append({
            'type': 'timeline_construction',
            'description': 'Construct detailed timeline of entity interactions',
            'confidence': 0.9,
            'action': 'build_entity_timeline'
        })

        suggestions.append({
            'type': 'evolution_analysis',
            'description': 'Analyze how relationships evolved over time',
            'confidence': 0.85,
            'action': 'analyze_relationship_evolution'
        })

        return suggestions

    def _generate_anomaly_suggestions(self, entities: List, context_data: Dict) -> List[Dict]:
        """Generate suggestions for anomaly investigation"""
        suggestions = []

        suggestions.append({
            'type': 'statistical_anomalies',
            'description': 'Identify statistical outliers in entity behavior patterns',
            'confidence': 0.9,
            'action': 'detect_statistical_anomalies'
        })

        suggestions.append({
            'type': 'pattern_recognition',
            'description': 'Recognize unusual patterns in entity interactions',
            'confidence': 0.85,
            'action': 'analyze_behavioral_patterns'
        })

        return suggestions

    def _generate_impact_suggestions(self, entities: List, context_data: Dict) -> List[Dict]:
        """Generate suggestions for impact assessment"""
        suggestions = []

        suggestions.append({
            'type': 'quantitative_impact',
            'description': 'Quantify the measurable impact of entity actions',
            'confidence': 0.9,
            'action': 'calculate_quantitative_impact'
        })

        suggestions.append({
            'type': 'systemic_effects',
            'description': 'Assess broader systemic implications and ripple effects',
            'confidence': 0.85,
            'action': 'analyze_systemic_effects'
        })

        return suggestions

    def _generate_general_suggestions(self, intent_analysis: Dict, entity_extraction: Dict) -> List[Dict]:
        """Generate general-purpose suggestions"""
        suggestions = []

        # Data visualization suggestion
        suggestions.append({
            'type': 'visualization',
            'description': 'Create visual representation of findings',
            'confidence': 0.7,
            'action': 'generate_visualization'
        })

        # Report generation suggestion
        suggestions.append({
            'type': 'reporting',
            'description': 'Generate comprehensive analysis report',
            'confidence': 0.75,
            'action': 'create_analysis_report'
        })

        return suggestions

    def _calculate_query_confidence(self, intent_analysis: Dict, entity_extraction: Dict) -> float:
        """Calculate overall confidence in query understanding"""
        intent_confidence = intent_analysis['intent_confidence']
        entity_confidence = min(1.0, len(entity_extraction['entities']) * 0.3)
        structure_confidence = 0.8 if entity_extraction['query_structure']['has_question_word'] else 0.6

        overall_confidence = (intent_confidence * 0.4 + entity_confidence * 0.3 + structure_confidence * 0.3)

        return min(1.0, overall_confidence)

    def _assess_query_complexity(self, query_text: str) -> str:
        """Assess the complexity level of the query"""
        word_count = len(query_text.split())

        if word_count <= 5:
            return 'simple'
        elif word_count <= 15:
            return 'moderate'
        elif word_count <= 25:
            return 'complex'
        else:
            return 'very_complex'

    def _generate_follow_up_questions(self, intent_analysis: Dict) -> List[str]:
        """Generate follow-up questions to refine the query"""
        intent = intent_analysis['primary_intent']
        questions = []

        if intent == 'entity_search':
            questions.extend([
                'What specific types of entities are you interested in?',
                'What time period should the search cover?',
                'Are there specific relationship types to focus on?'
            ])
        elif intent == 'relationship_analysis':
            questions.extend([
                'What depth of relationship analysis are you looking for?',
                'Are you interested in direct or indirect relationships?',
                'Should we include historical relationship data?'
            ])
        elif intent == 'temporal_analysis':
            questions.extend([
                'What specific time period interests you?',
                'Are you looking for patterns or specific events?',
                'Should we include future projections?'
            ])

        return questions[:3]

class CollaborativeDecisionEngine:
    """
    Collaborative decision-making between humans and AI
    Based on: "Human-in-the-Loop Audit with Override Capabilities"
    """

    def __init__(self):
        self.decision_history = []
        self.human_feedback = []
        self.ai_confidence_thresholds = {
            'high_confidence': 0.9,
            'medium_confidence': 0.7,
            'low_confidence': 0.5
        }
        self.collaboration_modes = ['fully_autonomous', 'human_guided', 'human_override', 'consensus_required']

    def process_collaborative_decision(self, ai_decision: Dict, human_input: Optional[Dict] = None, collaboration_mode: str = 'human_guided') -> Dict[str, Any]:
        """
        Process a collaborative decision between AI and human
        """
        decision_record = {
            'ai_decision': ai_decision,
            'human_input': human_input,
            'collaboration_mode': collaboration_mode,
            'timestamp': datetime.now(),
            'decision_outcome': None,
            'confidence_assessment': self._assess_decision_confidence(ai_decision),
            'human_override_reason': None
        }

        # Process decision based on collaboration mode
        if collaboration_mode == 'fully_autonomous':
            decision_record['decision_outcome'] = ai_decision
            decision_record['final_decision'] = 'ai_autonomous'

        elif collaboration_mode == 'human_override':
            if human_input and human_input.get('override_decision'):
                decision_record['decision_outcome'] = human_input['override_decision']
                decision_record['final_decision'] = 'human_override'
                decision_record['human_override_reason'] = human_input.get('reason', 'Not specified')
            else:
                decision_record['decision_outcome'] = ai_decision
                decision_record['final_decision'] = 'ai_default'

        elif collaboration_mode == 'consensus_required':
            decision_record['decision_outcome'] = self._reach_consensus(ai_decision, human_input)
            decision_record['final_decision'] = 'consensus'

        else:  # human_guided
            decision_record['decision_outcome'] = self._apply_human_guidance(ai_decision, human_input)
            decision_record['final_decision'] = 'human_guided'

        # Store decision for learning
        self.decision_history.append(decision_record)

        # Process human feedback for learning
        if human_input and 'feedback' in human_input:
            self._process_human_feedback(human_input['feedback'], ai_decision)

        return decision_record

    def _assess_decision_confidence(self, ai_decision: Dict) -> Dict[str, Any]:
        """Assess confidence in AI decision"""
        confidence_score = ai_decision.get('confidence', 0.5)

        if confidence_score >= self.ai_confidence_thresholds['high_confidence']:
            confidence_level = 'high'
            human_review_required = False
        elif confidence_score >= self.ai_confidence_thresholds['medium_confidence']:
            confidence_level = 'medium'
            human_review_required = True
        else:
            confidence_level = 'low'
            human_review_required = True

        return {
            'confidence_score': confidence_score,
            'confidence_level': confidence_level,
            'human_review_required': human_review_required,
            'review_priority': 'high' if confidence_score < 0.6 else 'normal'
        }

    def _reach_consensus(self, ai_decision: Dict, human_input: Dict) -> Dict:
        """Reach consensus between AI and human decision"""
        if not human_input:
            return ai_decision

        ai_confidence = ai_decision.get('confidence', 0.5)
        human_confidence = human_input.get('confidence', 0.8)

        # Weighted consensus based on confidence levels
        if ai_confidence > human_confidence + 0.2:
            return ai_decision  # AI decision prevails
        elif human_confidence > ai_confidence + 0.2:
            return human_input.get('decision', ai_decision)  # Human decision prevails
        else:
            # Merge decisions
            return self._merge_decisions(ai_decision, human_input.get('decision', ai_decision))

    def _apply_human_guidance(self, ai_decision: Dict, human_input: Optional[Dict]) -> Dict:
        """Apply human guidance to AI decision"""
        if not human_input:
            return ai_decision

        guided_decision = ai_decision.copy()

        # Apply human modifications
        if 'modifications' in human_input:
            modifications = human_input['modifications']
            for key, value in modifications.items():
                if key in guided_decision:
                    guided_decision[key] = value

        # Apply human priorities
        if 'priorities' in human_input:
            guided_decision['human_priorities'] = human_input['priorities']

        return guided_decision

    def _merge_decisions(self, ai_decision: Dict, human_decision: Dict) -> Dict:
        """Merge AI and human decisions into consensus"""
        merged_decision = {}

        # Combine all keys from both decisions
        all_keys = set(ai_decision.keys()) | set(human_decision.keys())

        for key in all_keys:
            ai_value = ai_decision.get(key)
            human_value = human_decision.get(key)

            if ai_value is None:
                merged_decision[key] = human_value
            elif human_value is None:
                merged_decision[key] = ai_value
            elif ai_value == human_value:
                merged_decision[key] = ai_value
            else:
                # Conflict resolution - prefer human input for subjective decisions
                if key in ['interpretation', 'assessment', 'recommendation']:
                    merged_decision[key] = human_value
                else:
                    # For objective decisions, use AI value
                    merged_decision[key] = ai_value

        return merged_decision

    def _process_human_feedback(self, feedback: Dict, ai_decision: Dict):
        """Process human feedback for system learning"""
        feedback_record = {
            'feedback': feedback,
            'ai_decision': ai_decision,
            'timestamp': datetime.now(),
            'feedback_type': feedback.get('type', 'general'),
            'usefulness_rating': feedback.get('usefulness', 5),
            'accuracy_rating': feedback.get('accuracy', 5),
            'areas_for_improvement': feedback.get('improvements', [])
        }

        self.human_feedback.append(feedback_record)

        # Update AI confidence thresholds based on feedback
        self._update_confidence_thresholds(feedback_record)

    def _update_confidence_thresholds(self, feedback_record: Dict):
        """Update AI confidence thresholds based on human feedback"""
        usefulness = feedback_record['usefulness_rating']
        accuracy = feedback_record['accuracy_rating']

        # Adjust thresholds based on feedback
        if usefulness < 3 or accuracy < 3:  # Poor feedback
            # Increase threshold to be more conservative
            self.ai_confidence_thresholds['high_confidence'] = min(0.95, self.ai_confidence_thresholds['high_confidence'] + 0.02)
            self.ai_confidence_thresholds['medium_confidence'] = min(0.8, self.ai_confidence_thresholds['medium_confidence'] + 0.02)
        elif usefulness > 4 and accuracy > 4:  # Good feedback
            # Decrease threshold to be more confident
            self.ai_confidence_thresholds['high_confidence'] = max(0.8, self.ai_confidence_thresholds['high_confidence'] - 0.01)
            self.ai_confidence_thresholds['medium_confidence'] = max(0.6, self.ai_confidence_thresholds['medium_confidence'] - 0.01)

class AuditSessionManager:
    """
    Interactive audit session management with human-AI collaboration
    Based on: "Audit Session Management with Interactive Controls"
    """

    def __init__(self):
        self.active_sessions = {}
        self.session_history = []
        self.query_processors = {}
        self.collaborative_engines = {}

    def create_audit_session(self, session_config: Dict) -> str:
        """Create a new audit session"""
        session_id = f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        session = {
            'session_id': session_id,
            'created_at': datetime.now(),
            'status': 'active',
            'config': session_config,
            'queries': [],
            'decisions': [],
            'findings': [],
            'human_interactions': [],
            'ai_contributions': [],
            'session_metrics': {
                'total_queries': 0,
                'human_decisions': 0,
                'ai_suggestions': 0,
                'collaboration_score': 0.0
            }
        }

        # Initialize session components
        self.query_processors[session_id] = NaturalLanguageQueryProcessor()
        self.collaborative_engines[session_id] = CollaborativeDecisionEngine()

        self.active_sessions[session_id] = session

        return session_id

    def process_session_query(self, session_id: str, query: str, context: Dict = None) -> Dict[str, Any]:
        """Process a query within an audit session"""
        if session_id not in self.active_sessions:
            return {'error': 'Session not found'}

        session = self.active_sessions[session_id]
        query_processor = self.query_processors[session_id]

        # Process query
        query_result = query_processor.process_query(query, context or {})

        # Store query in session
        session['queries'].append({
            'query': query,
            'result': query_result,
            'timestamp': datetime.now()
        })

        session['session_metrics']['total_queries'] += 1

        return query_result

    def make_collaborative_decision(self, session_id: str, ai_decision: Dict, human_input: Dict = None) -> Dict[str, Any]:
        """Make a collaborative decision within the session"""
        if session_id not in self.active_sessions:
            return {'error': 'Session not found'}

        session = self.active_sessions[session_id]
        collaborative_engine = self.collaborative_engines[session_id]

        # Process collaborative decision
        decision_result = collaborative_engine.process_collaborative_decision(
            ai_decision, human_input, session['config'].get('collaboration_mode', 'human_guided')
        )

        # Store decision in session
        session['decisions'].append(decision_result)

        # Update session metrics
        if decision_result['final_decision'] in ['human_override', 'human_guided']:
            session['session_metrics']['human_decisions'] += 1
        else:
            session['session_metrics']['ai_suggestions'] += 1

        return decision_result

    def add_session_finding(self, session_id: str, finding: Dict):
        """Add a finding to the audit session"""
        if session_id not in self.active_sessions:
            return {'error': 'Session not found'}

        session = self.active_sessions[session_id]

        finding_record = {
            'finding': finding,
            'timestamp': datetime.now(),
            'session_context': session_id,
            'validation_status': 'pending'
        }

        session['findings'].append(finding_record)

        return {'status': 'finding_added', 'finding_id': len(session['findings']) - 1}

    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get comprehensive session summary"""
        if session_id not in self.active_sessions:
            return {'error': 'Session not found'}

        session = self.active_sessions[session_id]

        summary = {
            'session_id': session_id,
            'duration': (datetime.now() - session['created_at']).total_seconds(),
            'status': session['status'],
            'metrics': session['session_metrics'],
            'query_summary': {
                'total_queries': len(session['queries']),
                'query_types': self._analyze_query_types(session['queries']),
                'avg_query_complexity': self._calculate_avg_query_complexity(session['queries'])
            },
            'decision_summary': {
                'total_decisions': len(session['decisions']),
                'collaboration_modes': self._analyze_decision_modes(session['decisions']),
                'human_ai_balance': self._calculate_human_ai_balance(session['decisions'])
            },
            'findings_summary': {
                'total_findings': len(session['findings']),
                'findings_by_type': self._analyze_findings_types(session['findings']),
                'validation_status': self._analyze_validation_status(session['findings'])
            },
            'collaboration_effectiveness': self._assess_collaboration_effectiveness(session)
        }

        return summary

    def close_audit_session(self, session_id: str) -> Dict[str, Any]:
        """Close an audit session and generate final report"""
        if session_id not in self.active_sessions:
            return {'error': 'Session not found'}

        session = self.active_sessions[session_id]

        # Generate final session report
        final_report = {
            'session_summary': self.get_session_summary(session_id),
            'key_findings': session['findings'],
            'recommendations': self._generate_session_recommendations(session),
            'lessons_learned': self._extract_lessons_learned(session),
            'closed_at': datetime.now(),
            'session_duration': (datetime.now() - session['created_at']).total_seconds()
        }

        # Update session status
        session['status'] = 'closed'
        session['final_report'] = final_report

        # Move to history
        self.session_history.append(session)
        del self.active_sessions[session_id]

        return final_report

    def _analyze_query_types(self, queries: List) -> Dict[str, int]:
        """Analyze types of queries in the session"""
        query_types = {}

        for query_record in queries:
            intent = query_record['result'].get('intent_analysis', {}).get('primary_intent', 'unknown')
            query_types[intent] = query_types.get(intent, 0) + 1

        return query_types

    def _calculate_avg_query_complexity(self, queries: List) -> float:
        """Calculate average query complexity"""
        if not queries:
            return 0

        complexities = []
        for query_record in queries:
            complexity = query_record['result'].get('intent_analysis', {}).get('query_complexity', 'moderate')

            if complexity == 'simple':
                score = 1
            elif complexity == 'moderate':
                score = 2
            elif complexity == 'complex':
                score = 3
            else:  # very_complex
                score = 4

            complexities.append(score)

        return np.mean(complexities) if complexities else 0

    def _analyze_decision_modes(self, decisions: List) -> Dict[str, int]:
        """Analyze decision collaboration modes"""
        modes = {}

        for decision in decisions:
            mode = decision.get('collaboration_mode', 'unknown')
            modes[mode] = modes.get(mode, 0) + 1

        return modes

    def _calculate_human_ai_balance(self, decisions: List) -> Dict[str, float]:
        """Calculate balance between human and AI decisions"""
        human_decisions = 0
        ai_decisions = 0

        for decision in decisions:
            final_decision = decision.get('final_decision', 'unknown')
            if final_decision in ['human_override', 'human_guided']:
                human_decisions += 1
            elif final_decision in ['ai_autonomous', 'consensus']:
                ai_decisions += 1

        total_decisions = human_decisions + ai_decisions

        if total_decisions == 0:
            return {'human_percentage': 0, 'ai_percentage': 0}

        return {
            'human_percentage': human_decisions / total_decisions,
            'ai_percentage': ai_decisions / total_decisions,
            'collaboration_balance': min(human_decisions, ai_decisions) / max(human_decisions, ai_decisions) if max(human_decisions, ai_decisions) > 0 else 0
        }

    def _analyze_findings_types(self, findings: List) -> Dict[str, int]:
        """Analyze types of findings"""
        finding_types = {}

        for finding in findings:
            finding_type = finding.get('finding', {}).get('type', 'unknown')
            finding_types[finding_type] = finding_types.get(finding_type, 0) + 1

        return finding_types

    def _analyze_validation_status(self, findings: List) -> Dict[str, int]:
        """Analyze validation status of findings"""
        validation_status = {}

        for finding in findings:
            status = finding.get('validation_status', 'unknown')
            validation_status[status] = validation_status.get(status, 0) + 1

        return validation_status

    def _assess_collaboration_effectiveness(self, session: Dict) -> Dict[str, Any]:
        """Assess effectiveness of human-AI collaboration"""
        metrics = session['session_metrics']

        # Calculate collaboration effectiveness score
        if metrics['total_queries'] > 0 and metrics['total_decisions'] > 0:
            query_decision_ratio = metrics['total_decisions'] / metrics['total_queries']
            human_ai_balance = metrics.get('human_ai_balance', {}).get('collaboration_balance', 0)

            effectiveness_score = (query_decision_ratio * 0.4 + human_ai_balance * 0.6)
        else:
            effectiveness_score = 0

        return {
            'effectiveness_score': effectiveness_score,
            'collaboration_quality': self._assess_collaboration_quality(effectiveness_score),
            'key_metrics': metrics
        }

    def _assess_collaboration_quality(self, score: float) -> str:
        """Assess quality of collaboration based on score"""
        if score >= 0.8:
            return 'excellent'
        elif score >= 0.6:
            return 'good'
        elif score >= 0.4:
            return 'adequate'
        else:
            return 'needs_improvement'

    def _generate_session_recommendations(self, session: Dict) -> List[str]:
        """Generate recommendations based on session analysis"""
        recommendations = []

        metrics = session['session_metrics']

        # Query-related recommendations
        if metrics['total_queries'] > 20:
            recommendations.append("Consider batching similar queries for efficiency")

        # Decision-related recommendations
        human_ai_balance = metrics.get('human_ai_balance', {})
        if human_ai_balance.get('human_percentage', 0) > 0.8:
            recommendations.append("AI capabilities may be underutilized - consider increasing AI confidence thresholds")
        elif human_ai_balance.get('ai_percentage', 0) > 0.8:
            recommendations.append("Consider increasing human oversight for critical decisions")

        # General recommendations
        recommendations.extend([
            "Regular review of collaboration patterns",
            "Continuous training on system capabilities",
            "Feedback integration for system improvement"
        ])

        return recommendations

    def _extract_lessons_learned(self, session: Dict) -> List[str]:
        """Extract lessons learned from the session"""
        lessons = []

        # Analyze successful patterns
        successful_queries = [q for q in session['queries'] if q['result'].get('confidence_score', 0) > 0.8]
        if successful_queries:
            lessons.append("High-confidence queries typically involve specific entity names and clear intent")

        # Analyze collaboration effectiveness
        effective_decisions = [d for d in session['decisions'] if d.get('confidence_assessment', {}).get('confidence_level') == 'high']
        if effective_decisions:
            lessons.append("Effective collaboration achieved when AI confidence aligns with human expertise areas")

        return lessons

# ===== MAIN HUMAN-AI COLLABORATIVE AUDITING ENGINE =====

class HumanAICollaborativeAuditingEngine:
    """
    Complete human-AI collaborative auditing engine
    Integrates natural language processing, collaborative decision-making, and audit session management
    """

    def __init__(self):
        self.session_manager = AuditSessionManager()
        self.active_sessions = {}

    def initialize_collaborative_audit(self, audit_config: Dict) -> Dict[str, Any]:
        """
        Initialize a collaborative audit session
        """

        print("🤝 Initializing Human-AI Collaborative Auditing Engine...")
        print("="*70)

        # Create audit session
        session_id = self.session_manager.create_audit_session(audit_config)

        # Initialize session components
        self.active_sessions[session_id] = {
            'session_id': session_id,
            'config': audit_config,
            'start_time': datetime.now(),
            'interaction_history': [],
            'learning_insights': []
        }

        initialization_result = {
            'session_id': session_id,
            'status': 'initialized',
            'collaboration_mode': audit_config.get('collaboration_mode', 'human_guided'),
            'capabilities': {
                'natural_language_processing': True,
                'collaborative_decision_making': True,
                'interactive_query_processing': True,
                'real_time_feedback': True,
                'audit_session_management': True
            },
            'available_features': [
                'Natural language query processing',
                'AI-powered suggestions and insights',
                'Collaborative decision-making',
                'Interactive audit session management',
                'Human feedback integration',
                'Learning from interaction patterns'
            ]
        }

        print("✅ Human-AI Collaborative Auditing Engine Initialized!")
        print("="*70)

        return initialization_result

    def process_audit_query(self, session_id: str, query: str, context: Dict = None) -> Dict[str, Any]:
        """Process an audit query with human-AI collaboration"""
        if session_id not in self.active_sessions:
            return {'error': 'Session not found'}

        # Process query through session manager
        query_result = self.session_manager.process_session_query(session_id, query, context)

        # Store interaction for learning
        interaction_record = {
            'type': 'query',
            'query': query,
            'result': query_result,
            'timestamp': datetime.now(),
            'context': context
        }

        self.active_sessions[session_id]['interaction_history'].append(interaction_record)

        return query_result

    def make_collaborative_decision(self, session_id: str, ai_decision: Dict, human_input: Dict = None) -> Dict[str, Any]:
        """Make a collaborative decision within the audit session"""
        if session_id not in self.active_sessions:
            return {'error': 'Session not found'}

        # Process collaborative decision
        decision_result = self.session_manager.make_collaborative_decision(session_id, ai_decision, human_input)

        # Store interaction for learning
        interaction_record = {
            'type': 'decision',
            'ai_decision': ai_decision,
            'human_input': human_input,
            'decision_result': decision_result,
            'timestamp': datetime.now()
        }

        self.active_sessions[session_id]['interaction_history'].append(interaction_record)

        return decision_result

    def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get comprehensive session status"""
        if session_id not in self.active_sessions:
            return {'error': 'Session not found'}

        session_summary = self.session_manager.get_session_summary(session_id)
        session_data = self.active_sessions[session_id]

        status = {
            'session_id': session_id,
            'session_status': session_data,
            'session_summary': session_summary,
            'interaction_summary': {
                'total_interactions': len(session_data['interaction_history']),
                'interaction_types': self._analyze_interaction_types(session_data['interaction_history']),
                'collaboration_patterns': self._analyze_collaboration_patterns(session_data['interaction_history'])
            },
            'learning_insights': session_data['learning_insights'],
            'performance_metrics': self._calculate_session_performance(session_data)
        }

        return status

    def close_audit_session(self, session_id: str) -> Dict[str, Any]:
        """Close audit session and generate comprehensive report"""
        if session_id not in self.active_sessions:
            return {'error': 'Session not found'}

        # Close session through manager
        final_report = self.session_manager.close_audit_session(session_id)

        # Add collaborative insights
        session_data = self.active_sessions[session_id]
        final_report['collaborative_insights'] = {
            'interaction_analysis': self._analyze_interaction_types(session_data['interaction_history']),
            'collaboration_effectiveness': self._analyze_collaboration_patterns(session_data['interaction_history']),
            'learning_outcomes': session_data['learning_insights'],
            'recommendations_for_improvement': self._generate_improvement_recommendations(session_data)
        }

        # Clean up active session
        del self.active_sessions[session_id]

        return final_report

    def _analyze_interaction_types(self, interactions: List) -> Dict[str, int]:
        """Analyze types of interactions in the session"""
        interaction_types = {}

        for interaction in interactions:
            interaction_type = interaction.get('type', 'unknown')
            interaction_types[interaction_type] = interaction_types.get(interaction_type, 0) + 1

        return interaction_types

    def _analyze_collaboration_patterns(self, interactions: List) -> Dict[str, Any]:
        """Analyze patterns in human-AI collaboration"""
        patterns = {
            'query_response_times': [],
            'decision_agreement_rates': [],
            'human_override_frequency': [],
            'ai_suggestion_adoption': []
        }

        for interaction in interactions:
            if interaction['type'] == 'query':
                # Analyze query processing
                if 'result' in interaction and 'confidence_score' in interaction['result']:
                    confidence = interaction['result']['confidence_score']
                    patterns['query_response_times'].append(confidence)

            elif interaction['type'] == 'decision':
                # Analyze decision patterns
                decision_result = interaction.get('decision_result', {})
                final_decision = decision_result.get('final_decision')

                if final_decision == 'human_override':
                    patterns['human_override_frequency'].append(1)
                else:
                    patterns['human_override_frequency'].append(0)

                if final_decision in ['ai_autonomous', 'consensus']:
                    patterns['ai_suggestion_adoption'].append(1)
                else:
                    patterns['ai_suggestion_adoption'].append(0)

        # Calculate summary statistics
        if patterns['query_response_times']:
            patterns['avg_query_confidence'] = np.mean(patterns['query_response_times'])

        if patterns['human_override_frequency']:
            patterns['human_override_rate'] = np.mean(patterns['human_override_frequency'])

        if patterns['ai_suggestion_adoption']:
            patterns['ai_adoption_rate'] = np.mean(patterns['ai_suggestion_adoption'])

        return patterns

    def _calculate_session_performance(self, session_data: Dict) -> Dict[str, Any]:
        """Calculate session performance metrics"""
        interactions = session_data['interaction_history']

        if not interactions:
            return {'message': 'No interactions to analyze'}

        performance = {
            'session_duration': (datetime.now() - session_data['start_time']).total_seconds(),
            'interaction_rate': len(interactions) / max(1, (datetime.now() - session_data['start_time']).total_seconds() / 3600),  # per hour
            'query_success_rate': 0,
            'decision_effectiveness': 0,
            'collaboration_efficiency': 0
        }

        # Calculate query success rate
        queries = [i for i in interactions if i['type'] == 'query']
        if queries:
            successful_queries = [q for q in queries if q.get('result', {}).get('confidence_score', 0) > 0.7]
            performance['query_success_rate'] = len(successful_queries) / len(queries)

        # Calculate decision effectiveness
        decisions = [i for i in interactions if i['type'] == 'decision']
        if decisions:
            effective_decisions = [d for d in decisions if d.get('decision_result', {}).get('confidence_assessment', {}).get('confidence_level') in ['high', 'medium']]
            performance['decision_effectiveness'] = len(effective_decisions) / len(decisions)

        return performance

    def _generate_improvement_recommendations(self, session_data: Dict) -> List[str]:
        """Generate recommendations for improving future sessions"""
        recommendations = []
        performance = self._calculate_session_performance(session_data)

        # Query-related recommendations
        if performance.get('query_success_rate', 0) < 0.7:
            recommendations.append("Improve natural language query processing and entity recognition")

        # Decision-related recommendations
        if performance.get('decision_effectiveness', 0) < 0.8:
            recommendations.append("Enhance collaborative decision-making algorithms")

        # General recommendations
        recommendations.extend([
            "Increase user training on system capabilities",
            "Implement more intuitive interaction interfaces",
            "Add real-time collaboration feedback mechanisms",
            "Develop session templates for common audit scenarios"
        ])

        return recommendations

print("🧠 Human-AI Collaborative Auditing Interface Ready")
print("   - Natural Language Query Processing")
print("   - Collaborative Decision-Making")
print("   - Interactive Audit Session Management")
print("   - Human Feedback Integration")
print("   - Learning from Interaction Patterns")
print("="*60)
