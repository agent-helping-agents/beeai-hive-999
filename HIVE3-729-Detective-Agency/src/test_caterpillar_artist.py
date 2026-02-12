#!/usr/bin/env python3
"""Test script for the Caterpillar Artist with new art."""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tools.art.caterpillar_artist import caterpillar_ansi_tool, ART_CATALOG


def test_art_catalog():
    """Test the art catalog."""
    print("Testing art catalog...")
    print(f"Total entries: {len(ART_CATALOG)}")

    # Check if all expected art is in the catalog
    expected = [
        "queen bee",
        "queen",
        "hive",
        "hive temple",
        "ethereum",
        "eth shrine",
        "ethereum shrine",
        "detective",
        "221b",
        "sherlock",
        "baker street",
        "steampunk",
        "ufo",
        "steampunk ufo",
        "bakerstreet",
    ]

    for name in expected:
        if name in ART_CATALOG:
            print(f"✅ '{name}' found in catalog (points to '{ART_CATALOG[name]}')")
        else:
            print(f"❌ '{name}' not found in catalog")

    print()


def test_art_loading():
    """Test loading of all art pieces."""
    print("Testing art loading...")

    for name, filename in ART_CATALOG.items():
        try:
            result = caterpillar_ansi_tool(name)
            if "Art not found" in result:
                print(f"❌ '{name}' ({filename}) - {result}")
            else:
                print(f"✅ '{name}' ({filename}) - {len(result)} bytes loaded")
        except Exception as e:
            print(f"❌ '{name}' ({filename}) - Error: {e}")

    print()


def test_new_art():
    """Test the new Baker Street steampunk UFO art specifically."""
    print("Testing new Baker Street steampunk UFO art...")

    # Try various aliases
    aliases = ["baker street", "steampunk", "ufo", "steampunk ufo", "bakerstreet"]

    for alias in aliases:
        try:
            result = caterpillar_ansi_tool(alias)
            if "Art not found" in result:
                print(f"❌ '{alias}' - {result}")
            else:
                print(f"✅ '{alias}' - {len(result)} bytes loaded")
                # Check if it contains specific elements
                if (
                    "BAKER STREET" in result
                    and "STEAMPUNK" in result
                    and "UFO" in result
                ):
                    print(f"   ✅ Contains expected elements")
        except Exception as e:
            print(f"❌ '{alias}' - Error: {e}")

    print()


if __name__ == "__main__":
    print("🎨 Caterpillar Artist Test Suite")
    print("=" * 50)
    print()

    test_art_catalog()
    test_art_loading()
    test_new_art()

    print("=" * 50)
    print("Test completed!")
