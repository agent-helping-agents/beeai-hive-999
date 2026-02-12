"""
Caterpillar Artist Tool — loads Moebius-style ANSI art and returns sequences.

Reads .ans files from art/moebius/ and writes timestamped copies to art/generated/.
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from beeai_framework.tools import tool

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ART_DIR = PROJECT_ROOT / "art" / "moebius"
GENERATED_DIR = PROJECT_ROOT / "art" / "generated"

# Map friendly names to filenames
ART_CATALOG: dict[str, str] = {
    "queen bee": "queen_bee.ans",
    "queen": "queen_bee.ans",
    "hive": "hive_temple.ans",
    "hive temple": "hive_temple.ans",
    "ethereum": "ethereum_shrine.ans",
    "eth shrine": "ethereum_shrine.ans",
    "ethereum shrine": "ethereum_shrine.ans",
    "detective": "detective_221b.ans",
    "221b": "detective_221b.ans",
    "sherlock": "detective_221b.ans",
    "baker street": "bakerstreet_steampunk_ufo.ans",
    "steampunk": "bakerstreet_steampunk_ufo.ans",
    "ufo": "bakerstreet_steampunk_ufo.ans",
    "steampunk ufo": "bakerstreet_steampunk_ufo.ans",
    "bakerstreet": "bakerstreet_steampunk_ufo.ans",
}


@tool
def caterpillar_ansi_tool(art_name: str = "queen bee") -> str:
    """Load and return ANSI art from the Moebius collection.

    Also writes a timestamped copy to art/generated/.

    Args:
        art_name: Name of the art piece. Options: queen bee, hive, ethereum,
                  eth shrine, hive temple. Or a direct .ans filename.

    Returns:
        The ANSI art as a string, or an error message if not found.
    """
    # Resolve name to filename
    key = art_name.strip().lower()
    filename = ART_CATALOG.get(key, key)
    if not filename.endswith(".ans"):
        filename += ".ans"

    art_path = ART_DIR / filename
    if not art_path.exists():
        available = [p.stem for p in ART_DIR.glob("*.ans")] if ART_DIR.exists() else []
        return f"Art not found: {filename}. Available: {', '.join(available) or 'none (create art/moebius/*.ans files)'}"

    content = art_path.read_text(encoding="utf-8", errors="replace")

    # Write timestamped copy
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = GENERATED_DIR / f"{art_path.stem}_{ts}.ans"
    out_path.write_text(content, encoding="utf-8")

    return content
