#!/usr/bin/env python3
"""
Main orchestrator: Reads Google Spreadsheet data and generates Instagram Reels
This script integrates with Claude Code's Google Workspace MCP tools
"""

import json
import subprocess
import sys
import os
from pathlib import Path

OUTPUT_DIR = "instagram_reels"
REELS_DATA_FILE = "reel_texts.json"


def save_texts_to_file(texts, output_file=REELS_DATA_FILE):
    """Save extracted texts to a JSON file for generate_reels.py to use"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(texts, f, indent=2, ensure_ascii=False)
        print(f"✓ Saved {len(texts)} text entries to {output_file}")
        return True
    except Exception as e:
        print(f"✗ Error saving texts: {e}")
        return False


def extract_texts_from_spreadsheet_json(data):
    """
    Extract text from Google Sheets JSON data
    Assumes data is in the format returned by get_design_content

    The spreadsheet should have text in the first column
    """
    texts = []

    try:
        # If it's a raw list of values
        if isinstance(data, list):
            for row in data:
                if isinstance(row, list) and len(row) > 0:
                    text = row[0]
                    if text and str(text).strip():
                        texts.append(str(text).strip())
                elif isinstance(row, str) and row.strip():
                    texts.append(row.strip())

        # If it's a dict with specific structure
        elif isinstance(data, dict):
            # Try various common structures
            for key in ['values', 'data', 'rows', 'sheets']:
                if key in data and isinstance(data[key], list):
                    for row in data[key]:
                        if isinstance(row, list) and len(row) > 0:
                            text = row[0]
                            if text and str(text).strip():
                                texts.append(str(text).strip())
                    if texts:
                        break

            # Try direct iteration if dict items look like rows
            if not texts and isinstance(data, dict):
                for value in data.values():
                    if isinstance(value, str) and value.strip():
                        texts.append(value.strip())
                    elif isinstance(value, list) and len(value) > 0:
                        for item in value:
                            if isinstance(item, str) and item.strip():
                                texts.append(item.strip())

    except Exception as e:
        print(f"Error parsing spreadsheet data: {e}")
        return []

    return texts


def run_generator(output_dir=OUTPUT_DIR):
    """Execute the generate_reels.py script"""
    try:
        result = subprocess.run(
            ['python3', 'generate_reels.py', '--output-dir', output_dir],
            capture_output=False,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"✗ Error running generator: {e}")
        return False


def main():
    print("="*70)
    print("Instagram Reels Generator - Spreadsheet Integration")
    print("="*70)
    print()

    print("This script integrates with Google Workspace MCP to:")
    print("  1. Read text from your Google Spreadsheet")
    print("  2. Generate 9:16 vertical Instagram Reel videos")
    print("  3. Save them ready for upload")
    print()

    # Check if generate_reels.py exists
    if not os.path.exists('generate_reels.py'):
        print("✗ generate_reels.py not found!")
        print("  Both scripts must be in the same directory")
        sys.exit(1)

    # Check for canva template
    if not os.path.exists('canva_template.png'):
        print("⚠️  canva_template.png not found")
        print()
        print("To set up:")
        print("  1. Export your Canva design as PNG")
        print("  2. Save as: canva_template.png")
        print()
        print("Or create a sample template:")
        print("  python3 generate_reels.py --create-sample")
        print()

    # Load spreadsheet data if it exists
    if os.path.exists(REELS_DATA_FILE):
        print(f"Found existing data file: {REELS_DATA_FILE}")
        with open(REELS_DATA_FILE, 'r', encoding='utf-8') as f:
            texts = json.load(f)
        print(f"Loaded {len(texts)} text entries")
        print()

        # Run generator
        print("Starting video generation...")
        print()
        run_generator(OUTPUT_DIR)

    else:
        print("ℹ️  No spreadsheet data loaded yet")
        print()
        print("To use this with a Google Spreadsheet:")
        print("  1. Use Claude Code's Google Workspace MCP tools to read the spreadsheet")
        print("  2. Extract the text column from your spreadsheet")
        print("  3. Save as reel_texts.json (JSON array of strings)")
        print()
        print("Or manually create reel_texts.json:")
        print('  [')
        print('    "Your first reel text",')
        print('    "Your second reel text",')
        print('    "Your third reel text"')
        print('  ]')
        print()
        print("Then run: python3 spreadsheet_to_reels.py")


if __name__ == "__main__":
    main()
