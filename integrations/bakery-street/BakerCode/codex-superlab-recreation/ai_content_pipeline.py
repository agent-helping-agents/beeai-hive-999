#!/usr/bin/env python3
"""
Codex-SuperLab AI Content Pipeline
Based on original 17.5K LOC implementation
8-stage workflow with GPT-4 for content automation
"""

import openai
import os
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
import logging
from dataclasses import dataclass
from enum import Enum

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentType(Enum):
    ARTICLE = "article"
    BLOG_POST = "blog_post"
    SOCIAL_MEDIA = "social_media"
    TECHNICAL_DOC = "technical_doc"
    MARKETING_COPY = "marketing_copy"

class PipelineStage(Enum):
    RESEARCH = "research"
    OUTLINE = "outline"
    DRAFT = "draft"
    ENHANCEMENT = "enhancement"
    FACT_CHECK = "fact_check"
    SEO_OPTIMIZATION = "seo_optimization"
    FORMATTING = "formatting"
    FINAL_REVIEW = "final_review"

@dataclass
class ContentRequest:
    id: str
    title: str
    content_type: ContentType
    topic: str
    target_audience: str
    keywords: List[str]
    word_count: int
    tone: str
    requirements: Dict[str, Any]
    created_at: datetime
    status: str = "pending"

@dataclass
class StageResult:
    stage: PipelineStage
    content: str
    metadata: Dict[str, Any]
    timestamp: datetime
    tokens_used: int
    success: bool

class AIContentPipeline:
    def __init__(self, openai_api_key: str):
        self.openai_client = openai.OpenAI(api_key=openai_api_key)
        self.pipeline_stages = [
            PipelineStage.RESEARCH,
            PipelineStage.OUTLINE,
            PipelineStage.DRAFT,
            PipelineStage.ENHANCEMENT,
            PipelineStage.FACT_CHECK,
            PipelineStage.SEO_OPTIMIZATION,
            PipelineStage.FORMATTING,
            PipelineStage.FINAL_REVIEW
        ]
        self.active_requests = {}
        self.completed_requests = {}
    
    async def process_content_request(self, request: ContentRequest) -> Dict[str, Any]:
        """Process a content request through all 8 stages"""
        logger.info(f"Starting content pipeline for request: {request.id}")
        
        self.active_requests[request.id] = {
            'request': request,
            'stages': {},
            'current_stage': 0,
            'started_at': datetime.now()
        }
        
        current_content = ""
        pipeline_context = {
            'request': request,
            'accumulated_content': "",
            'research_data': {},
            'seo_data': {},
            'metadata': {}
        }
        
        try:
            for i, stage in enumerate(self.pipeline_stages):
                logger.info(f"Processing stage {i+1}/8: {stage.value}")
                
                stage_result = await self.execute_stage(stage, pipeline_context)
                
                if stage_result.success:
                    self.active_requests[request.id]['stages'][stage.value] = stage_result
                    self.active_requests[request.id]['current_stage'] = i + 1
                    
                    # Update pipeline context
                    pipeline_context['accumulated_content'] = stage_result.content
                    pipeline_context['metadata'].update(stage_result.metadata)
                    
                    logger.info(f"Stage {stage.value} completed successfully")
                else:
                    logger.error(f"Stage {stage.value} failed")
                    return self.handle_pipeline_failure(request.id, stage)
            
            # Pipeline completed successfully
            return self.finalize_content_request(request.id)
            
        except Exception as e:
            logger.error(f"Pipeline error for request {request.id}: {e}")
            return self.handle_pipeline_failure(request.id, None, str(e))
    
    async def execute_stage(self, stage: PipelineStage, context: Dict[str, Any]) -> StageResult:
        """Execute a specific pipeline stage"""
        request = context['request']
        
        try:
            if stage == PipelineStage.RESEARCH:
                return await self.stage_research(request, context)
            elif stage == PipelineStage.OUTLINE:
                return await self.stage_outline(request, context)
            elif stage == PipelineStage.DRAFT:
                return await self.stage_draft(request, context)
            elif stage == PipelineStage.ENHANCEMENT:
                return await self.stage_enhancement(request, context)
            elif stage == PipelineStage.FACT_CHECK:
                return await self.stage_fact_check(request, context)
            elif stage == PipelineStage.SEO_OPTIMIZATION:
                return await self.stage_seo_optimization(request, context)
            elif stage == PipelineStage.FORMATTING:
                return await self.stage_formatting(request, context)
            elif stage == PipelineStage.FINAL_REVIEW:
                return await self.stage_final_review(request, context)
            else:
                raise ValueError(f"Unknown stage: {stage}")
                
        except Exception as e:
            logger.error(f"Error in stage {stage.value}: {e}")
            return StageResult(
                stage=stage,
                content="",
                metadata={'error': str(e)},
                timestamp=datetime.now(),
                tokens_used=0,
                success=False
            )
    
    async def stage_research(self, request: ContentRequest, context: Dict[str, Any]) -> StageResult:
        """Stage 1: Research and information gathering"""
        prompt = f"""
        Conduct comprehensive research for a {request.content_type.value} about "{request.topic}".
        
        Target audience: {request.target_audience}
        Keywords to focus on: {', '.join(request.keywords)}
        
        Please provide:
        1. Key facts and statistics
        2. Current trends and developments
        3. Expert opinions and quotes
        4. Relevant case studies or examples
        5. Common questions and concerns
        6. Competitive landscape overview
        
        Format as structured research notes with sources and credibility indicators.
        """
        
        response = await self.call_openai(prompt, max_tokens=2000)
        
        return StageResult(
            stage=PipelineStage.RESEARCH,
            content=response['content'],
            metadata={
                'research_points': self.extract_research_points(response['content']),
                'tokens_used': response['tokens_used']
            },
            timestamp=datetime.now(),
            tokens_used=response['tokens_used'],
            success=True
        )
    
    async def stage_outline(self, request: ContentRequest, context: Dict[str, Any]) -> StageResult:
        """Stage 2: Create detailed outline"""
        research_content = context.get('accumulated_content', '')
        
        prompt = f"""
        Based on this research:
        {research_content}
        
        Create a detailed outline for a {request.content_type.value} titled "{request.title}".
        
        Requirements:
        - Target word count: {request.word_count}
        - Tone: {request.tone}
        - Target audience: {request.target_audience}
        - Must include keywords: {', '.join(request.keywords)}
        
        Provide:
        1. Compelling headline/title
        2. Hook/introduction strategy
        3. Main sections with subsections
        4. Key points for each section
        5. Call-to-action strategy
        6. Estimated word count per section
        """
        
        response = await self.call_openai(prompt, max_tokens=1500)
        
        return StageResult(
            stage=PipelineStage.OUTLINE,
            content=response['content'],
            metadata={
                'outline_structure': self.parse_outline_structure(response['content']),
                'tokens_used': response['tokens_used']
            },
            timestamp=datetime.now(),
            tokens_used=response['tokens_used'],
            success=True
        )
    
    async def stage_draft(self, request: ContentRequest, context: Dict[str, Any]) -> StageResult:
        """Stage 3: Write initial draft"""
        outline = context.get('accumulated_content', '')
        research = context.get('metadata', {}).get('research_points', '')
        
        prompt = f"""
        Write a complete {request.content_type.value} based on this outline:
        {outline}
        
        Research context:
        {research}
        
        Requirements:
        - Title: {request.title}
        - Word count: approximately {request.word_count} words
        - Tone: {request.tone}
        - Target audience: {request.target_audience}
        - Include keywords naturally: {', '.join(request.keywords)}
        
        Write engaging, well-structured content that flows naturally and provides value to the reader.
        """
        
        response = await self.call_openai(prompt, max_tokens=3000)
        
        return StageResult(
            stage=PipelineStage.DRAFT,
            content=response['content'],
            metadata={
                'word_count': len(response['content'].split()),
                'keyword_density': self.calculate_keyword_density(response['content'], request.keywords),
                'tokens_used': response['tokens_used']
            },
            timestamp=datetime.now(),
            tokens_used=response['tokens_used'],
            success=True
        )
    
    async def stage_enhancement(self, request: ContentRequest, context: Dict[str, Any]) -> StageResult:
        """Stage 4: Enhance and improve content"""
        draft = context.get('accumulated_content', '')
        
        prompt = f"""
        Enhance and improve this {request.content_type.value}:
        {draft}
        
        Focus on:
        1. Improving clarity and readability
        2. Adding compelling examples and analogies
        3. Strengthening transitions between sections
        4. Enhancing the hook and conclusion
        5. Ensuring consistent tone: {request.tone}
        6. Adding emotional appeal where appropriate
        7. Improving sentence variety and flow
        
        Maintain the core message while making it more engaging and impactful.
        """
        
        response = await self.call_openai(prompt, max_tokens=3500)
        
        return StageResult(
            stage=PipelineStage.ENHANCEMENT,
            content=response['content'],
            metadata={
                'improvements_made': self.identify_improvements(draft, response['content']),
                'readability_score': self.calculate_readability_score(response['content']),
                'tokens_used': response['tokens_used']
            },
            timestamp=datetime.now(),
            tokens_used=response['tokens_used'],
            success=True
        )
    
    async def stage_fact_check(self, request: ContentRequest, context: Dict[str, Any]) -> StageResult:
        """Stage 5: Fact-checking and accuracy verification"""
        content = context.get('accumulated_content', '')
        
        prompt = f"""
        Review this content for factual accuracy and credibility:
        {content}
        
        Please:
        1. Identify any claims that need verification
        2. Flag potentially outdated information
        3. Suggest more credible sources where needed
        4. Check for logical consistency
        5. Verify statistics and data points
        6. Ensure claims are properly qualified
        
        Provide the corrected content with fact-check annotations.
        """
        
        response = await self.call_openai(prompt, max_tokens=3000)
        
        return StageResult(
            stage=PipelineStage.FACT_CHECK,
            content=response['content'],
            metadata={
                'fact_check_issues': self.extract_fact_check_issues(response['content']),
                'credibility_score': self.assess_credibility(response['content']),
                'tokens_used': response['tokens_used']
            },
            timestamp=datetime.now(),
            tokens_used=response['tokens_used'],
            success=True
        )
    
    async def stage_seo_optimization(self, request: ContentRequest, context: Dict[str, Any]) -> StageResult:
        """Stage 6: SEO optimization"""
        content = context.get('accumulated_content', '')
        
        prompt = f"""
        Optimize this content for SEO while maintaining quality and readability:
        {content}
        
        Target keywords: {', '.join(request.keywords)}
        
        Please:
        1. Optimize keyword placement and density
        2. Improve title and headings for SEO
        3. Add meta description suggestion
        4. Suggest internal linking opportunities
        5. Optimize for featured snippets
        6. Ensure proper heading hierarchy (H1, H2, H3)
        7. Add semantic keywords and LSI terms
        
        Provide the optimized content with SEO recommendations.
        """
        
        response = await self.call_openai(prompt, max_tokens=3500)
        
        return StageResult(
            stage=PipelineStage.SEO_OPTIMIZATION,
            content=response['content'],
            metadata={
                'seo_score': self.calculate_seo_score(response['content'], request.keywords),
                'meta_description': self.extract_meta_description(response['content']),
                'heading_structure': self.analyze_heading_structure(response['content']),
                'tokens_used': response['tokens_used']
            },
            timestamp=datetime.now(),
            tokens_used=response['tokens_used'],
            success=True
        )
    
    async def stage_formatting(self, request: ContentRequest, context: Dict[str, Any]) -> StageResult:
        """Stage 7: Formatting and structure optimization"""
        content = context.get('accumulated_content', '')
        
        prompt = f"""
        Format this content for optimal presentation and readability:
        {content}
        
        Apply appropriate formatting for {request.content_type.value}:
        1. Add proper markdown formatting
        2. Create bullet points and numbered lists where appropriate
        3. Add emphasis (bold, italic) for key points
        4. Structure with clear headings and subheadings
        5. Add call-out boxes or quotes if relevant
        6. Ensure proper paragraph breaks
        7. Add table of contents if needed
        
        Provide the fully formatted content ready for publication.
        """
        
        response = await self.call_openai(prompt, max_tokens=3000)
        
        return StageResult(
            stage=PipelineStage.FORMATTING,
            content=response['content'],
            metadata={
                'formatting_elements': self.identify_formatting_elements(response['content']),
                'structure_score': self.assess_structure_quality(response['content']),
                'tokens_used': response['tokens_used']
            },
            timestamp=datetime.now(),
            tokens_used=response['tokens_used'],
            success=True
        )
    
    async def stage_final_review(self, request: ContentRequest, context: Dict[str, Any]) -> StageResult:
        """Stage 8: Final review and quality assurance"""
        content = context.get('accumulated_content', '')
        
        prompt = f"""
        Perform a final quality review of this {request.content_type.value}:
        {content}
        
        Check for:
        1. Overall coherence and flow
        2. Grammar and spelling errors
        3. Consistency in tone and style
        4. Completeness of requirements
        5. Call-to-action effectiveness
        6. Reader engagement level
        7. Professional polish
        
        Provide the final, publication-ready version with a quality assessment.
        """
        
        response = await self.call_openai(prompt, max_tokens=3500)
        
        return StageResult(
            stage=PipelineStage.FINAL_REVIEW,
            content=response['content'],
            metadata={
                'quality_score': self.calculate_quality_score(response['content']),
                'final_word_count': len(response['content'].split()),
                'completion_status': 'ready_for_publication',
                'tokens_used': response['tokens_used']
            },
            timestamp=datetime.now(),
            tokens_used=response['tokens_used'],
            success=True
        )
    
    async def call_openai(self, prompt: str, max_tokens: int = 2000) -> Dict[str, Any]:
        """Make API call to OpenAI"""
        try:
            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert content creator and editor with deep knowledge across multiple domains."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return {
                'content': response.choices[0].message.content,
                'tokens_used': response.usage.total_tokens
            }
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    # Helper methods for content analysis
    def extract_research_points(self, content: str) -> List[str]:
        """Extract key research points from content"""
        # Simple implementation - would be more sophisticated in production
        lines = content.split('\n')
        return [line.strip() for line in lines if line.strip().startswith(('•', '-', '1.', '2.', '3.'))]
    
    def calculate_keyword_density(self, content: str, keywords: List[str]) -> Dict[str, float]:
        """Calculate keyword density"""
        word_count = len(content.split())
        density = {}
        
        for keyword in keywords:
            count = content.lower().count(keyword.lower())
            density[keyword] = (count / word_count) * 100 if word_count > 0 else 0
        
        return density
    
    def calculate_seo_score(self, content: str, keywords: List[str]) -> int:
        """Calculate basic SEO score"""
        score = 0
        
        # Check keyword presence in title/headings
        if any(keyword.lower() in content[:200].lower() for keyword in keywords):
            score += 25
        
        # Check keyword density
        densities = self.calculate_keyword_density(content, keywords)
        if any(1 <= density <= 3 for density in densities.values()):
            score += 25
        
        # Check content length
        word_count = len(content.split())
        if 300 <= word_count <= 2000:
            score += 25
        
        # Check heading structure
        if '##' in content or '#' in content:
            score += 25
        
        return score
    
    def finalize_content_request(self, request_id: str) -> Dict[str, Any]:
        """Finalize completed content request"""
        request_data = self.active_requests[request_id]
        
        final_result = {
            'request_id': request_id,
            'status': 'completed',
            'final_content': request_data['stages'][PipelineStage.FINAL_REVIEW.value].content,
            'pipeline_summary': {
                'total_stages': len(self.pipeline_stages),
                'completed_stages': len(request_data['stages']),
                'total_tokens_used': sum(stage.tokens_used for stage in request_data['stages'].values()),
                'processing_time': (datetime.now() - request_data['started_at']).total_seconds(),
                'quality_metrics': self.compile_quality_metrics(request_data['stages'])
            },
            'completed_at': datetime.now().isoformat()
        }
        
        # Move to completed requests
        self.completed_requests[request_id] = final_result
        del self.active_requests[request_id]
        
        logger.info(f"Content request {request_id} completed successfully")
        return final_result
    
    def handle_pipeline_failure(self, request_id: str, failed_stage: Optional[PipelineStage], error: str = "") -> Dict[str, Any]:
        """Handle pipeline failure"""
        request_data = self.active_requests.get(request_id, {})
        
        failure_result = {
            'request_id': request_id,
            'status': 'failed',
            'failed_at_stage': failed_stage.value if failed_stage else 'unknown',
            'error': error,
            'completed_stages': len(request_data.get('stages', {})),
            'partial_content': request_data.get('stages', {}).get(list(request_data.get('stages', {}).keys())[-1], {}).get('content', '') if request_data.get('stages') else '',
            'failed_at': datetime.now().isoformat()
        }
        
        # Move to completed requests (as failed)
        self.completed_requests[request_id] = failure_result
        if request_id in self.active_requests:
            del self.active_requests[request_id]
        
        logger.error(f"Content request {request_id} failed at stage {failed_stage}")
        return failure_result
    
    def compile_quality_metrics(self, stages: Dict[str, StageResult]) -> Dict[str, Any]:
        """Compile quality metrics from all stages"""
        metrics = {}
        
        if PipelineStage.FINAL_REVIEW.value in stages:
            final_stage = stages[PipelineStage.FINAL_REVIEW.value]
            metrics.update(final_stage.metadata)
        
        if PipelineStage.SEO_OPTIMIZATION.value in stages:
            seo_stage = stages[PipelineStage.SEO_OPTIMIZATION.value]
            metrics['seo_score'] = seo_stage.metadata.get('seo_score', 0)
        
        return metrics

# Example usage
if __name__ == "__main__":
    print("AI Content Pipeline - 8-Stage Workflow")
    print("Configure with OPENAI_API_KEY environment variable")
    
    # Example request creation
    example_request = ContentRequest(
        id="example_001",
        title="The Future of AI in Content Creation",
        content_type=ContentType.ARTICLE,
        topic="AI content generation and automation",
        target_audience="Content creators and marketers",
        keywords=["AI content", "automation", "content creation", "artificial intelligence"],
        word_count=1500,
        tone="professional yet accessible",
        requirements={"include_examples": True, "add_statistics": True},
        created_at=datetime.now()
    )
    
    print(f"Example request created: {example_request.title}")