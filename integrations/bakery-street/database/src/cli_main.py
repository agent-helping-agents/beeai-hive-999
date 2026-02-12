#!/usr/bin/env python3
"""
Energetic Lexicon - CLI Entry Point
🔒 PRIVATE - PROPRIETARY
© 2025 Baker Street Laboratory

Main executable entry point for PyInstaller bundle.
Provides unified CLI for all database operations and tool integrations.
"""

import sys
import os
from pathlib import Path
from typing import Optional

# Fix frozen app paths (PyInstaller bundle)
if getattr(sys, 'frozen', False):
    # Running as PyInstaller bundle
    BASE_DIR = Path(sys._MEIPASS)
    os.environ['ENERGETIC_LEXICON_FROZEN'] = '1'
else:
    # Running as script
    BASE_DIR = Path(__file__).parent.parent

# Add base dir to path
sys.path.insert(0, str(BASE_DIR))

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

# Import database modules
try:
    from src.storage.database import init_database, get_db_manager, session_scope
    from src.storage.crud import RepositoryCRUD, ConceptCRUD, PDFCRUD
    from src.storage.models import Repository, Concept, PDF
    from scripts.encryption import EncryptionWrapper
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"sys.path: {sys.path}")
    sys.exit(1)

# Initialize Typer app
app = typer.Typer(
    name="energetic-lexicon",
    help="🔬 Energetic Lexicon Database - Baker Street Laboratory",
    add_completion=False,
    rich_markup_mode="rich"
)

console = Console()

# Version info
__version__ = "0.1.0"
__author__ = "Baker Street Laboratory"


# ============================================================================
# DATABASE COMMANDS
# ============================================================================

@app.command()
def init(
    reset: bool = typer.Option(False, "--reset", help="⚠️  Drop all tables first (DANGEROUS)"),
    encrypt: bool = typer.Option(False, "--encrypt", help="🔒 Encrypt database after creation"),
    sample_data: bool = typer.Option(True, "--sample-data/--no-sample", help="📝 Create sample concepts"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
):
    """
    Initialize the Energetic Lexicon database

    Creates tables, optionally adds sample data, and encrypts the database.
    """

    console.print(Panel.fit(
        "[bold blue]Initializing Energetic Lexicon Database[/bold blue]",
        border_style="blue"
    ))

    if reset:
        if not typer.confirm("⚠️  This will DELETE ALL DATA. Continue?"):
            console.print("[yellow]Cancelled.[/yellow]")
            raise typer.Abort()

    try:
        # Initialize database
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:

            task1 = progress.add_task("Creating database schema...", total=None)
            init_database(reset=reset)
            progress.update(task1, completed=True)

            if sample_data:
                task2 = progress.add_task("Creating sample data...", total=None)
                _create_sample_data()
                progress.update(task2, completed=True)

            if encrypt:
                task3 = progress.add_task("Encrypting database...", total=None)
                _encrypt_database()
                progress.update(task3, completed=True)

        console.print("[bold green]✅ Database initialized successfully![/bold green]")

        # Show summary
        db = get_db_manager()
        info = db.get_table_info()

        table = Table(title="Database Status", box=box.ROUNDED)
        table.add_column("Table", style="cyan")
        table.add_column("Rows", justify="right", style="green")

        for table_name, table_info in info.items():
            table.add_row(table_name, str(table_info['row_count']))

        console.print(table)

    except Exception as e:
        console.print(f"[bold red]❌ Error: {e}[/bold red]")
        if verbose:
            console.print_exception()
        raise typer.Exit(1)


@app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    type: str = typer.Option("all", "--type", "-t", help="Search type: repos, concepts, pdfs, all"),
    limit: int = typer.Option(10, "--limit", "-n", help="Maximum results"),
):
    """
    Search the Energetic Lexicon

    Searches repositories, concepts, and PDFs for matching content.
    """

    console.print(f"\n[bold]🔍 Searching for:[/bold] {query}\n")

    try:
        with session_scope() as session:
            results_found = False

            if type in ['repos', 'all']:
                repos = RepositoryCRUD.search(session, query)
                if repos:
                    results_found = True
                    _display_repos(repos[:limit])

            if type in ['concepts', 'all']:
                concepts = ConceptCRUD.search(session, query)
                if concepts:
                    results_found = True
                    _display_concepts(concepts[:limit])

            if type in ['pdfs', 'all']:
                pdfs = PDFCRUD.search_content(session, query)
                if pdfs:
                    results_found = True
                    _display_pdfs(pdfs[:limit])

            if not results_found:
                console.print("[yellow]No results found.[/yellow]")

    except Exception as e:
        console.print(f"[bold red]❌ Error: {e}[/bold red]")
        raise typer.Exit(1)


@app.command()
def info():
    """Show database information and statistics"""

    try:
        db = get_db_manager()

        # Database info
        console.print(Panel.fit(
            f"[bold cyan]Database:[/bold cyan] {db.db_path}",
            title="Energetic Lexicon",
            border_style="cyan"
        ))

        # Table statistics
        info = db.get_table_info()

        table = Table(title="Database Statistics", box=box.ROUNDED)
        table.add_column("Table", style="cyan", no_wrap=True)
        table.add_column("Rows", justify="right", style="green")
        table.add_column("Columns", justify="right", style="blue")

        for table_name, table_info in info.items():
            table.add_row(
                table_name,
                str(table_info['row_count']),
                str(len(table_info['columns']))
            )

        console.print(table)

        # Database size
        if os.path.exists(db.db_path):
            size_bytes = os.path.getsize(db.db_path)
            size_mb = size_bytes / (1024 * 1024)
            console.print(f"\n[bold]Size:[/bold] {size_mb:.2f} MB")

    except Exception as e:
        console.print(f"[bold red]❌ Error: {e}[/bold red]")
        raise typer.Exit(1)


# ============================================================================
# INTEGRATION COMMANDS
# ============================================================================

@app.command()
def integrate(
    tool: str = typer.Argument(..., help="Tool: primax, novapis, dreamscript, amphetamemes, agenticseek"),
    action: str = typer.Option("status", "--action", "-a", help="Action: status, test, config")
):
    """
    Integrate with external tools (PRIMAX, NovAPIS, Dream Script, etc.)

    Manages connections to your proprietary AI tools and AgenticSeek.
    """

    console.print(f"\n[bold blue]🔗 Integration:[/bold blue] {tool}\n")

    try:
        if tool.lower() == "primax":
            _integrate_primax(action)
        elif tool.lower() == "novapis":
            _integrate_novapis(action)
        elif tool.lower() == "dreamscript":
            _integrate_dreamscript(action)
        elif tool.lower() == "amphetamemes":
            _integrate_amphetamemes(action)
        elif tool.lower() == "agenticseek":
            _integrate_agenticseek(action)
        else:
            console.print(f"[red]Unknown tool: {tool}[/red]")
            console.print("\nAvailable tools:")
            console.print("  - primax")
            console.print("  - novapis")
            console.print("  - dreamscript")
            console.print("  - amphetamemes")
            console.print("  - agenticseek")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"[bold red]❌ Error: {e}[/bold red]")
        raise typer.Exit(1)


@app.command()
def version():
    """Show version information"""

    table = Table(title="Energetic Lexicon", box=box.DOUBLE_EDGE)
    table.add_column("Component", style="cyan", no_wrap=True)
    table.add_column("Version", style="green")

    table.add_row("Core", __version__)
    table.add_row("Author", __author__)
    table.add_row("Python", sys.version.split()[0])
    table.add_row("Frozen", str(getattr(sys, 'frozen', False)))
    table.add_row("Base Dir", str(BASE_DIR))

    console.print(table)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _create_sample_data():
    """Create sample concepts for testing"""

    with session_scope() as session:
        # Check if data exists
        existing = session.query(Concept).count()
        if existing > 0:
            console.print("[yellow]Sample data already exists, skipping...[/yellow]")
            return

        # Create sample concepts
        concepts = [
            {
                'term': 'AutomationCodex',
                'definition': 'Automation-first philosophy underlying all Bakery Street infrastructure',
                'domain': 'tech',
                'abstraction_level': 4
            },
            {
                'term': 'Research Geometry',
                'definition': 'Framework treating research as geometric/coordinate space',
                'domain': 'science',
                'abstraction_level': 5
            },
            {
                'term': 'Energetic Lexicon',
                'definition': 'Unified knowledge graph of entire Bakery Street ecosystem',
                'domain': 'tech',
                'abstraction_level': 4
            },
        ]

        for concept_data in concepts:
            concept = Concept(**concept_data)
            session.add(concept)


def _encrypt_database():
    """Encrypt the database file"""

    db = get_db_manager()
    encryptor = EncryptionWrapper()

    encrypted_path = encryptor.encrypt_file(
        db.db_path,
        output_path=f"{db.db_path}.gpg"
    )

    console.print(f"[green]Encrypted:[/green] {encrypted_path}")


def _display_repos(repos):
    """Display repository search results"""

    table = Table(title="Repositories", box=box.ROUNDED)
    table.add_column("Name", style="cyan")
    table.add_column("Quadrant", style="yellow")
    table.add_column("Private", justify="center")

    for repo in repos:
        table.add_row(
            repo.name,
            repo.geometry_quadrant or "N/A",
            "🔒" if repo.is_private else "🌐"
        )

    console.print(table)


def _display_concepts(concepts):
    """Display concept search results"""

    table = Table(title="Concepts", box=box.ROUNDED)
    table.add_column("Term", style="cyan")
    table.add_column("Domain", style="yellow")
    table.add_column("Definition", style="white")

    for concept in concepts:
        table.add_row(
            concept.term,
            concept.domain or "N/A",
            concept.definition[:60] + "..." if len(concept.definition) > 60 else concept.definition
        )

    console.print(table)


def _display_pdfs(pdfs):
    """Display PDF search results"""

    table = Table(title="PDFs", box=box.ROUNDED)
    table.add_column("Title", style="cyan")
    table.add_column("Pages", justify="right")
    table.add_column("Category", style="yellow")

    for pdf in pdfs:
        table.add_row(
            pdf.title,
            str(pdf.page_count) if pdf.page_count else "N/A",
            pdf.category or "N/A"
        )

    console.print(table)


def _integrate_primax(action: str):
    """PRIMAX integration"""
    console.print("[cyan]PRIMAX integration not yet implemented[/cyan]")
    console.print("Status: [yellow]Pending implementation[/yellow]")


def _integrate_novapis(action: str):
    """NovAPIS integration"""
    console.print("[cyan]NovAPIS integration not yet implemented[/cyan]")
    console.print("Status: [yellow]Pending implementation[/yellow]")


def _integrate_dreamscript(action: str):
    """Dream Script integration"""
    console.print("[cyan]Dream Script integration not yet implemented[/cyan]")
    console.print("Status: [yellow]Pending implementation[/yellow]")


def _integrate_amphetamemes(action: str):
    """Amphetamemes integration"""
    console.print("[cyan]Amphetamemes integration not yet implemented[/cyan]")
    console.print("Status: [yellow]Pending implementation[/yellow]")


def _integrate_agenticseek(action: str):
    """AgenticSeek integration"""
    console.print("[cyan]AgenticSeek integration not yet implemented[/cyan]")
    console.print("Status: [yellow]Pending implementation[/yellow]")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    app()
