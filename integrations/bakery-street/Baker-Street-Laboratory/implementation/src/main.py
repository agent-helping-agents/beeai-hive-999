#!/usr/bin/env python3
"""
Baker Street Laboratory - Main Entry Point
This is the primary entry point for the research pipeline.
"""

import argparse
import asyncio
import logging
import sys
from pathlib import Path
from typing import Optional

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from core.config import Config
from core.logger import setup_logging
from orchestrator.research_orchestrator import ResearchOrchestrator
from utils.environment import check_environment


def setup_argument_parser() -> argparse.ArgumentParser:
    """Set up command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Baker Street Laboratory - AI-Augmented Research Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --mode research --query "machine learning trends 2024"
  python main.py --mode interactive
  python main.py --mode pipeline --config config/custom_agents.yaml
        """
    )
    
    parser.add_argument(
        "--mode",
        choices=["research", "interactive", "pipeline"],
        default="interactive",
        help="Execution mode (default: interactive)"
    )
    
    parser.add_argument(
        "--query",
        type=str,
        help="Research query for research mode"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        default="config/agents.yaml",
        help="Configuration file path (default: config/agents.yaml)"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default="research",
        help="Output directory for research results (default: research)"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    return parser


async def run_research_mode(config: Config, query: str, output_dir: str) -> None:
    """Run the research pipeline with a specific query."""
    logging.info(f"Starting research mode with query: {query}")
    
    orchestrator = ResearchOrchestrator(config)
    
    try:
        results = await orchestrator.conduct_research(
            query=query,
            output_dir=output_dir
        )
        
        logging.info("Research completed successfully")
        print(f"\n✅ Research completed! Results saved to: {output_dir}")
        
        if results.get("summary"):
            print(f"\n📋 Summary: {results['summary']}")
        
    except Exception as e:
        logging.error(f"Research failed: {e}")
        print(f"\n❌ Research failed: {e}")
        sys.exit(1)


async def run_interactive_mode(config: Config, output_dir: str) -> None:
    """Run the interactive research mode."""
    logging.info("Starting interactive mode")
    
    orchestrator = ResearchOrchestrator(config)
    
    print("\n🔬 Baker Street Laboratory - Interactive Research Mode")
    print("=" * 55)
    print("Enter your research queries or commands. Type 'help' for assistance.")
    print("Type 'quit' or 'exit' to end the session.\n")
    
    while True:
        try:
            user_input = input("🔍 Research Query: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ["quit", "exit", "q"]:
                print("\n👋 Goodbye! Happy researching!")
                break
                
            if user_input.lower() == "help":
                print_help()
                continue
                
            if user_input.lower() == "status":
                await show_status(orchestrator)
                continue
            
            # Process the research query
            print(f"\n🔄 Processing: {user_input}")
            
            results = await orchestrator.conduct_research(
                query=user_input,
                output_dir=output_dir
            )
            
            print(f"\n✅ Research completed!")
            if results.get("summary"):
                print(f"📋 Summary: {results['summary']}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Session interrupted. Goodbye!")
            break
        except Exception as e:
            logging.error(f"Error in interactive mode: {e}")
            print(f"\n❌ Error: {e}")


async def run_pipeline_mode(config: Config, output_dir: str) -> None:
    """Run a specific pipeline configuration."""
    logging.info("Starting pipeline mode")
    
    orchestrator = ResearchOrchestrator(config)
    
    try:
        results = await orchestrator.run_pipeline(output_dir=output_dir)
        
        logging.info("Pipeline completed successfully")
        print(f"\n✅ Pipeline completed! Results saved to: {output_dir}")
        
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        print(f"\n❌ Pipeline failed: {e}")
        sys.exit(1)


def print_help() -> None:
    """Print help information for interactive mode."""
    print("""
Available commands:
  help     - Show this help message
  status   - Show system status
  quit/exit - End the session
  
Research queries:
  Simply type your research question or topic, for example:
  - "What are the latest developments in quantum computing?"
  - "Analyze trends in renewable energy adoption"
  - "Compare different machine learning architectures"
    """)


async def show_status(orchestrator: ResearchOrchestrator) -> None:
    """Show system status."""
    print("\n📊 System Status:")
    print("-" * 20)
    
    status = await orchestrator.get_status()
    
    for key, value in status.items():
        print(f"{key}: {value}")


async def main() -> None:
    """Main entry point."""
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    # Set up logging
    log_level = args.log_level
    if args.verbose:
        log_level = "DEBUG"
    
    setup_logging(level=log_level)
    
    # Check environment
    env_check = check_environment()
    if not env_check["valid"]:
        print(f"❌ Environment check failed: {env_check['message']}")
        sys.exit(1)
    
    # Load configuration
    try:
        config = Config.from_file(args.config)
        logging.info(f"Configuration loaded from: {args.config}")
    except Exception as e:
        logging.error(f"Failed to load configuration: {e}")
        print(f"❌ Configuration error: {e}")
        sys.exit(1)
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Run the appropriate mode
    try:
        if args.mode == "research":
            if not args.query:
                print("❌ Research mode requires a query. Use --query option.")
                sys.exit(1)
            await run_research_mode(config, args.query, str(output_dir))
            
        elif args.mode == "interactive":
            await run_interactive_mode(config, str(output_dir))
            
        elif args.mode == "pipeline":
            await run_pipeline_mode(config, str(output_dir))
            
    except KeyboardInterrupt:
        print("\n\n👋 Operation interrupted. Goodbye!")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
