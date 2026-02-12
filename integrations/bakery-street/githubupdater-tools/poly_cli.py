#!/usr/bin/env python3
"""
Poly-AI Framework CLI - Command Line Interface
"""

import asyncio
import click
import json
import yaml
from typing import Optional
from poly_framework import PolyAIFramework

@click.group()
@click.option('--config', '-c', default='poly_config.yaml', help='Configuration file path')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.pass_context
def cli(ctx, config, verbose):
    """Poly-AI Framework - Advanced GitHub Automation Suite"""
    ctx.ensure_object(dict)
    ctx.obj['config'] = config
    ctx.obj['verbose'] = verbose

@cli.command()
@click.argument('query', default='automation')
@click.option('--per-page', '-p', default=10, help='Number of results to return')
@click.option('--output', '-o', type=click.Choice(['table', 'json', 'yaml']), default='table', help='Output format')
@click.pass_context
def discover(ctx, query, per_page, output):
    """Discover and rank GitHub automation tools"""
    async def _discover():
        framework = PolyAIFramework(ctx.obj['config'])
        tools = await framework.discover_tools(query, per_page)
        ranked_tools = framework.rank_tools(tools)
        
        if output == 'json':
            result = [{"tool": tool, "score": score} for tool, score in ranked_tools]
            click.echo(json.dumps(result, indent=2))
        elif output == 'yaml':
            result = [{"tool": tool, "score": score} for tool, score in ranked_tools]
            click.echo(yaml.dump(result, default_flow_style=False))
        else:
            click.echo(f"🔍 Top {len(ranked_tools)} GitHub Automation Tools for '{query}':")
            click.echo("=" * 60)
            for i, (tool, score) in enumerate(ranked_tools, 1):
                click.echo(f"{i:2d}. {tool['name']} (Score: {score:.3f})")
                click.echo(f"    ⭐ {tool['detailed_metrics'].stars:,} stars | "
                          f"🍴 {tool['detailed_metrics'].forks:,} forks")
                click.echo(f"    📝 {tool['description'][:80]}...")
                click.echo(f"    🔗 {tool['url']}")
                click.echo()
    
    asyncio.run(_discover())

@cli.command()
@click.option('--enterprise', is_flag=True, help='Enterprise workflow')
@click.option('--open-source', is_flag=True, help='Open source workflow')
@click.option('--ai-ml', is_flag=True, help='AI/ML workflow')
@click.option('--web-app', is_flag=True, help='Web application workflow')
@click.pass_context
def workflow(ctx, enterprise, open_source, ai_ml, web_app):
    """Generate GitHub workflow configuration"""
    framework = PolyAIFramework(ctx.obj['config'])
    
    # Determine workflow type
    if enterprise:
        workflow_type = "enterprise"
    elif open_source:
        workflow_type = "open_source"
    elif ai_ml:
        workflow_type = "ai_ml"
    elif web_app:
        workflow_type = "web_app"
    else:
        workflow_type = "default"
    
    workflow_config = framework.generate_workflow(workflow_type)
    
    click.echo(f"⚙️  Generated {workflow_type} workflow:")
    click.echo(f"Name: {workflow_config.name}")
    click.echo(f"Triggers: {', '.join(workflow_config.triggers)}")
    click.echo(f"Jobs: {list(workflow_config.jobs.keys())}")
    click.echo(f"Environment: {workflow_config.environment}")
    
    # Show workflow YAML
    workflow_yaml = framework._create_workflow_yaml(workflow_config)
    click.echo("\n📄 Workflow YAML:")
    click.echo("-" * 30)
    click.echo(workflow_yaml)

@cli.command()
@click.argument('repo_name')
@click.option('--workflow-type', '-t', default='default', help='Workflow type to deploy')
@click.pass_context
def deploy(ctx, repo_name, workflow_type):
    """Deploy workflow to GitHub repository"""
    framework = PolyAIFramework(ctx.obj['config'])
    
    workflow_config = framework.generate_workflow(workflow_type)
    success = framework.deploy_workflow(repo_name, workflow_config)
    
    if success:
        click.echo(f"✅ Successfully deployed {workflow_type} workflow to {repo_name}")
    else:
        click.echo(f"❌ Failed to deploy workflow to {repo_name}")
        raise click.Abort()

@cli.command()
@click.argument('query')
@click.option('--output', '-o', type=click.Choice(['text', 'json']), default='text', help='Output format')
@click.pass_context
def recommend(ctx, query, output):
    """Get AI-powered recommendations"""
    async def _recommend():
        framework = PolyAIFramework(ctx.obj['config'])
        
        if not framework.config.perplexity_api_key:
            click.echo("❌ Perplexity API key not configured")
            return
        
        recommendations = await framework.fetch_ai_recommendations(query)
        
        if "error" in recommendations:
            click.echo(f"❌ Error: {recommendations['error']}")
            return
        
        if output == 'json':
            click.echo(json.dumps(recommendations, indent=2))
        else:
            click.echo(f"🤖 AI Recommendations for: {query}")
            click.echo("=" * 50)
            click.echo(recommendations['recommendations'])
    
    asyncio.run(_recommend())

@cli.command()
@click.pass_context
def status(ctx):
    """Show framework status and metrics"""
    framework = PolyAIFramework(ctx.obj['config'])
    metrics = framework.get_metrics()
    
    click.echo("📊 Poly-AI Framework Status")
    click.echo("=" * 30)
    click.echo(f"GitHub Token: {'✅ Configured' if framework.config.github_token else '❌ Not configured'}")
    click.echo(f"AI Services: {len(framework.ai_services)} configured")
    click.echo(f"Cache: {'✅ Enabled' if framework.config.cache_enabled else '❌ Disabled'}")
    click.echo()
    click.echo("📈 Metrics:")
    for key, value in metrics.items():
        click.echo(f"  {key}: {value}")

@cli.command()
@click.option('--filename', '-f', default='poly_config.yaml', help='Configuration file name')
@click.pass_context
def init(ctx, filename):
    """Initialize Poly-AI Framework configuration"""
    framework = PolyAIFramework()
    framework.create_config_file(filename)
    click.echo(f"✅ Configuration file created: {filename}")
    click.echo("Please edit the file and set your API keys and tokens.")

@cli.command()
@click.argument('repos', nargs=-1)
@click.option('--workflow-type', '-t', default='default', help='Workflow type to deploy')
@click.option('--dry-run', is_flag=True, help='Show what would be deployed without actually deploying')
@click.pass_context
def bulk_deploy(ctx, repos, workflow_type, dry_run):
    """Deploy workflows to multiple repositories"""
    if not repos:
        click.echo("❌ No repositories specified")
        return
    
    framework = PolyAIFramework(ctx.obj['config'])
    workflow_config = framework.generate_workflow(workflow_type)
    
    click.echo(f"🚀 Bulk deploying {workflow_type} workflow to {len(repos)} repositories...")
    
    for repo in repos:
        if dry_run:
            click.echo(f"  [DRY RUN] Would deploy to {repo}")
        else:
            success = framework.deploy_workflow(repo, workflow_config)
            status = "✅" if success else "❌"
            click.echo(f"  {status} {repo}")

@cli.command()
@click.option('--port', '-p', default=8080, help='Dashboard port')
@click.pass_context
def dashboard(ctx, port):
    """Start monitoring dashboard"""
    click.echo(f"🌐 Starting Poly-AI Framework dashboard on port {port}")
    click.echo("Dashboard features:")
    click.echo("  • Real-time metrics")
    click.echo("  • Tool discovery history")
    click.echo("  • Workflow deployment status")
    click.echo("  • AI recommendation logs")
    click.echo()
    click.echo("Note: Dashboard implementation requires FastAPI setup")
    click.echo("Run: pip install fastapi uvicorn to enable dashboard")

if __name__ == '__main__':
    cli()
