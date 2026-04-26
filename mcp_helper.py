#!/usr/bin/env python3
"""
MCP Helper - Use Claude Code's Google Workspace MCP tools
This script shows how to use MCP tools to read from Google Sheets
"""

import json
import os
import sys
import subprocess
from pathlib import Path


def read_spreadsheet_via_mcp(spreadsheet_id):
    """
    Helper function to guide using MCP tools

    Claude Code's Google Workspace MCP tools can:
    1. Search for a Google Sheets file by name or ID
    2. Read the file content
    3. Extract spreadsheet data

    Usage:
    - Use mcp__Google-Drive__search_files to find your spreadsheet
    - Use mcp__Google-Drive__get_file_metadata to get details
    - Use mcp__Google-Drive__read_file_content to read spreadsheet data
    """

    print(f"""
To read from your Google Spreadsheet using Claude Code:

1. Get your Spreadsheet ID:
   - Open: https://docs.google.com/spreadsheets/d/{spreadsheet_id}
   - Copy the ID from the URL

2. Search for the spreadsheet:
   Claude will use: mcp__Google-Drive__search_files
   Query: title contains your spreadsheet name

3. Read the content:
   Claude will use: mcp__Google-Drive__read_file_content
   Pass the file ID returned from step 2

4. Extract the data:
   The spreadsheet content will be returned as JSON/data
   Extract text from the first column

Example command:
  mcp__Google-Drive__search_files(
    query="title='My Instagram Reels'"
  )
""")


def process_csv_data(csv_content):
    """
    Process CSV data from a Google Sheet export
    Assumes first column contains the reel text
    """
    import csv
    from io import StringIO

    texts = []
    try:
        reader = csv.reader(StringIO(csv_content))
        next(reader)  # Skip header
        for row in reader:
            if row and row[0].strip():
                texts.append(row[0].strip())
    except Exception as e:
        print(f"Error parsing CSV: {e}")

    return texts


def process_json_data(json_content):
    """
    Process JSON data from a Google Sheet
    Handles various formats commonly returned by APIs
    """
    texts = []

    try:
        data = json.loads(json_content) if isinstance(json_content, str) else json_content

        # Handle different data structures
        if isinstance(data, list):
            for item in data:
                if isinstance(item, list):
                    # Array of arrays - take first column
                    if item and item[0]:
                        texts.append(str(item[0]).strip())
                elif isinstance(item, dict):
                    # Array of objects - look for text field
                    for key in ['text', 'content', 'value', 'title']:
                        if key in item and item[key]:
                            texts.append(str(item[key]).strip())
                            break
                elif isinstance(item, str):
                    if item.strip():
                        texts.append(item.strip())

        elif isinstance(data, dict):
            # Handle Google Sheets API response format
            if 'values' in data:
                for row in data['values'][1:]:  # Skip header
                    if row and row[0]:
                        texts.append(str(row[0]).strip())

    except json.JSONDecodeError:
        print("Invalid JSON format")
    except Exception as e:
        print(f"Error processing JSON: {e}")

    return texts


def create_sample_spreadsheet_json():
    """Create a sample JSON file showing expected format"""
    sample_data = [
        "Transform your health with proven nutrition science 🌱",
        "Your gut health directly impacts your mental clarity",
        "Learn why detoxification is your body's natural superpower",
        "Small changes today = Big results tomorrow 💪",
        "The #1 mistake preventing your weight loss goals",
        "7 superfoods that heal your digestive system"
    ]

    with open('sample_spreadsheet_data.json', 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, indent=2, ensure_ascii=False)

    print("✓ Created sample_spreadsheet_data.json")
    return sample_data


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Helper for reading Google Sheets via MCP'
    )
    parser.add_argument('--spreadsheet-id', default='1iV-q-GmyS8K8_kQ-CGGQJwrOQdPAKyrE0SptuE7NF-c',
                       help='Google Spreadsheet ID')
    parser.add_argument('--create-sample', action='store_true',
                       help='Create sample spreadsheet data')
    parser.add_argument('--process-data', default=None,
                       help='Process data from JSON/CSV file')

    args = parser.parse_args()

    print("="*70)
    print("Google Workspace MCP Helper for Instagram Reels")
    print("="*70)
    print()

    if args.create_sample:
        print("Creating sample data...")
        sample_data = create_sample_spreadsheet_json()
        print(f"\nCreated {len(sample_data)} sample reel texts")
        print("\nNext: Use this data with generate_reels.py:")
        print("  python3 generate_reels.py")
        return

    if args.process_data:
        print(f"Processing data from: {args.process_data}")

        if not os.path.exists(args.process_data):
            print(f"✗ File not found: {args.process_data}")
            sys.exit(1)

        with open(args.process_data, 'r', encoding='utf-8') as f:
            content = f.read()

        # Try to process as JSON first
        try:
            texts = process_json_data(content)
            if not texts:
                texts = process_csv_data(content)
        except:
            texts = process_csv_data(content)

        if texts:
            print(f"✓ Extracted {len(texts)} text entries:")
            for i, text in enumerate(texts[:3], 1):
                print(f"  {i}. {text[:60]}{'...' if len(text) > 60 else ''}")
            if len(texts) > 3:
                print(f"  ... and {len(texts) - 3} more")

            # Save to reel_texts.json
            with open('reel_texts.json', 'w', encoding='utf-8') as f:
                json.dump(texts, f, indent=2, ensure_ascii=False)
            print(f"\n✓ Saved to reel_texts.json")
            print("\nNow generate reels:")
            print("  python3 generate_reels.py")
        else:
            print("✗ No valid text data found")
        return

    # Show MCP usage instructions
    read_spreadsheet_via_mcp(args.spreadsheet_id)


if __name__ == "__main__":
    main()
