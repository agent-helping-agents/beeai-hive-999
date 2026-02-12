#!/usr/bin/env python3
"""
Advanced usage examples for Poly-AI Framework
"""

import asyncio
import os
import json
from poly_framework import PolyAIFramework

async def enterprise_automation_example():
    """Example of enterprise-level automation setup"""
    print("🏢 Enterprise Automation Example")
    print("=" * 40)
    
    # Initialize framework with enterprise configuration
    framework = PolyAIFramework("poly_config.yaml")
    
    # Enterprise environment variables
    env_vars = {
        "ENTERPRISE": "true",
        "SECURITY_SCAN": "true",
        "COMPLIANCE": "required",
        "DEPLOYMENT_ENV": "production"
    }
    
    # Generate enterprise workflow
    workflow_type = framework.pick_workflow_type(env_vars)
    workflow_config = framework.generate_workflow(workflow_type)
    
    print(f"Generated {workflow_type} workflow:")
    print(f"  Name: {workflow_config.name}")
    print(f"  Jobs: {list(workflow_config.jobs.keys())}")
    print(f"  Enterprise Features: {workflow_config.enterprise_features}")
    
    # Deploy to multiple repositories
    repositories = [
        "Bakery-street-projct/ai-development-framework",
        "Bakery-street-projct/dynamic-asynchronous-data-streamliner",
        "Bakery-street-projct/githubupdater-tools"
    ]
    
    print(f"\nDeploying to {len(repositories)} repositories...")
    for repo in repositories:
        success = framework.deploy_workflow(repo, workflow_config)
        status = "✅" if success else "❌"
        print(f"  {status} {repo}")
    
    return framework

async def ai_powered_discovery_example():
    """Example of AI-powered tool discovery and recommendations"""
    print("\n🤖 AI-Powered Discovery Example")
    print("=" * 40)
    
    framework = PolyAIFramework()
    
    # Discover tools for specific use cases
    use_cases = [
        "machine learning automation",
        "devops ci cd",
        "security scanning",
        "code quality"
    ]
    
    all_tools = []
    for use_case in use_cases:
        print(f"\nDiscovering tools for: {use_case}")
        tools = await framework.discover_tools(use_case, per_page=5)
        ranked_tools = framework.rank_tools(tools)
        
        print(f"  Found {len(tools)} tools:")
        for i, (tool, score) in enumerate(ranked_tools[:3], 1):
            print(f"    {i}. {tool['name']} (Score: {score:.3f})")
        
        all_tools.extend(tools)
    
    # Get AI recommendations for the best tools
    if framework.config.perplexity_api_key:
        print(f"\nGetting AI recommendations for top tools...")
        query = "best practices for GitHub automation in enterprise environments"
        recommendations = await framework.fetch_ai_recommendations(query)
        
        if "error" not in recommendations:
            print("AI Recommendations:")
            print(f"  {recommendations['recommendations'][:200]}...")
        else:
            print(f"AI Error: {recommendations['error']}")
    
    return all_tools

async def bulk_repository_management_example():
    """Example of bulk repository management"""
    print("\n📦 Bulk Repository Management Example")
    print("=" * 40)
    
    framework = PolyAIFramework()
    
    # Simulate bulk operations
    operations = [
        {
            "action": "update_workflows",
            "repositories": [
                "Bakery-street-projct/voidshatterecho",
                "Bakery-street-projct/PeakyBlenders",
                "Bakery-street-projct/sentiment-analysis-bert"
            ],
            "workflow_type": "open_source"
        },
        {
            "action": "security_audit",
            "repositories": [
                "Bakery-street-projct/ai-development-framework",
                "Bakery-street-projct/dynamic-asynchronous-data-streamliner"
            ],
            "workflow_type": "enterprise"
        }
    ]
    
    for operation in operations:
        print(f"\nPerforming {operation['action']} on {len(operation['repositories'])} repositories...")
        
        workflow_config = framework.generate_workflow(operation['workflow_type'])
        
        for repo in operation['repositories']:
            success = framework.deploy_workflow(repo, workflow_config)
            status = "✅" if success else "❌"
            print(f"  {status} {repo} - {operation['workflow_type']} workflow")
    
    return framework

async def performance_monitoring_example():
    """Example of performance monitoring and metrics"""
    print("\n📊 Performance Monitoring Example")
    print("=" * 40)
    
    framework = PolyAIFramework()
    
    # Simulate some operations to generate metrics
    print("Running operations to generate metrics...")
    
    # Discover tools
    tools = await framework.discover_tools("python automation", per_page=10)
    ranked_tools = framework.rank_tools(tools)
    
    # Generate workflows
    for workflow_type in ["enterprise", "open_source", "ai_ml"]:
        workflow_config = framework.generate_workflow(workflow_type)
    
    # Get AI recommendations
    if framework.config.perplexity_api_key:
        await framework.fetch_ai_recommendations("GitHub automation best practices")
    
    # Display metrics
    metrics = framework.get_metrics()
    print("\nFramework Metrics:")
    print("-" * 20)
    for key, value in metrics.items():
        print(f"  {key}: {value}")
    
    # Performance analysis
    print(f"\nPerformance Analysis:")
    print(f"  Tools discovered: {metrics['tools_discovered']}")
    print(f"  Workflows generated: {metrics['workflows_generated']}")
    print(f"  AI recommendations: {metrics['ai_recommendations']}")
    print(f"  Cache efficiency: {metrics['cache_size']} items cached")
    print(f"  GitHub API rate limit: {metrics['github_rate_limit']} remaining")
    
    return metrics

async def custom_workflow_generation_example():
    """Example of custom workflow generation"""
    print("\n⚙️  Custom Workflow Generation Example")
    print("=" * 40)
    
    framework = PolyAIFramework()
    
    # Create custom workflow configurations
    custom_workflows = {
        "ai_research": {
            "name": "AI Research Pipeline",
            "triggers": ["push", "pull_request", "schedule"],
            "jobs": {
                "data_preprocessing": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {"name": "Setup Python", "uses": "actions/setup-python@v4", "with": {"python-version": "3.11"}},
                        {"name": "Install dependencies", "run": "pip install -r requirements.txt"},
                        {"name": "Preprocess data", "run": "python scripts/preprocess.py"},
                        {"name": "Validate data", "run": "python scripts/validate_data.py"}
                    ]
                },
                "model_experiment": {
                    "runs-on": "ubuntu-latest",
                    "needs": "data_preprocessing",
                    "steps": [
                        {"name": "Run experiments", "run": "python experiments/run_experiments.py"},
                        {"name": "Generate reports", "run": "python scripts/generate_reports.py"},
                        {"name": "Upload artifacts", "uses": "actions/upload-artifact@v3", "with": {"name": "results", "path": "results/"}}
                    ]
                },
                "publish_results": {
                    "runs-on": "ubuntu-latest",
                    "needs": "model_experiment",
                    "if": "github.ref == 'refs/heads/main'",
                    "steps": [
                        {"name": "Publish to MLflow", "run": "python scripts/publish_to_mlflow.py"},
                        {"name": "Update documentation", "run": "python scripts/update_docs.py"}
                    ]
                }
            },
            "environment": "research",
            "enterprise_features": False
        }
    }
    
    # Generate and display custom workflows
    for workflow_name, workflow_data in custom_workflows.items():
        print(f"\nCustom Workflow: {workflow_name}")
        print(f"  Name: {workflow_data['name']}")
        print(f"  Jobs: {list(workflow_data['jobs'].keys())}")
        print(f"  Environment: {workflow_data['environment']}")
        
        # Create workflow config object
        from poly_framework import WorkflowConfig
        workflow_config = WorkflowConfig(
            name=workflow_data['name'],
            triggers=workflow_data['triggers'],
            jobs=workflow_data['jobs'],
            environment=workflow_data['environment'],
            enterprise_features=workflow_data['enterprise_features']
        )
        
        # Generate YAML
        yaml_content = framework._create_workflow_yaml(workflow_config)
        print(f"  YAML length: {len(yaml_content)} characters")
    
    return custom_workflows

async def main():
    """Main function running all examples"""
    print("🚀 Poly-AI Framework - Advanced Usage Examples")
    print("=" * 60)
    
    # Check for required environment variables
    if not os.getenv("GITHUB_TOKEN"):
        print("⚠️  Warning: GITHUB_TOKEN not set. Some examples may not work.")
    
    if not os.getenv("PERPLEXITY_API_KEY"):
        print("⚠️  Warning: PERPLEXITY_API_KEY not set. AI features will be limited.")
    
    print()
    
    try:
        # Run all examples
        await enterprise_automation_example()
        await ai_powered_discovery_example()
        await bulk_repository_management_example()
        await performance_monitoring_example()
        await custom_workflow_generation_example()
        
        print("\n🎉 All examples completed successfully!")
        print("The Poly-AI Framework is ready for production use!")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("Please check your configuration and try again.")

if __name__ == "__main__":
    asyncio.run(main())
