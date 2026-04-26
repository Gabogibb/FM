#!/usr/bin/env python3
"""
Instagram Reels Generator - Complete Solution
Reads from Google Spreadsheet and creates 9:16 vertical videos
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont

# Configuration
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
DURATION = 9
FPS = 30
OUTPUT_DIR = "instagram_reels"
CANVA_TEMPLATE = "canva_template.png"


def create_sample_template(output_path=CANVA_TEMPLATE):
    """Create a sample Canva template if one doesn't exist"""
    if os.path.exists(output_path):
        return

    print(f"📸 Creating sample template: {output_path}")
    img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), color='#0a0a0a')
    draw = ImageDraw.Draw(img)

    # Add gradient-like background
    for i in range(0, VIDEO_HEIGHT, 60):
        color_val = int(255 * (i / VIDEO_HEIGHT))
        color = (color_val // 3, color_val // 4, 255 - color_val // 2)
        draw.rectangle([(0, i), (VIDEO_WIDTH, i + 60)], fill=color)

    # Add accent bar
    draw.rectangle([(0, 0), (VIDEO_WIDTH, 80)], fill=(255, 100, 50))

    img.save(output_path)
    print(f"✓ Sample template created: {output_path}")


def create_video_with_text(text, output_path, template_path=CANVA_TEMPLATE):
    """Create a 9-second vertical video with text overlay on template"""
    try:
        if not os.path.exists(template_path):
            print(f"⚠️  Template not found at {template_path}")
            print(f"   Create one by exporting your Canva design as PNG")
            print(f"   Or run with --create-sample to use a sample template")
            return False

        print(f"  Encoding: {text[:50]}...")

        # Load template and create base clip
        base_clip = ImageClip(template_path).set_duration(DURATION)
        base_clip = base_clip.resize((VIDEO_WIDTH, VIDEO_HEIGHT))

        # Create text clip with word wrapping
        txt_clip = TextClip(
            text,
            fontsize=48,
            color='white',
            font='Arial-Bold',
            method='caption',
            size=(VIDEO_WIDTH - 100, None),
            align='center'
        ).set_duration(DURATION)

        # Position text in center
        txt_clip = txt_clip.set_position('center')

        # Composite the clips
        final_clip = CompositeVideoClip([base_clip, txt_clip])

        # Encode video
        final_clip.write_videofile(
            output_path,
            fps=FPS,
            codec='libx264',
            audio=False,
            verbose=False,
            logger=None
        )

        # Report result
        file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"  ✓ {file_size_mb:.1f} MB")
        return True

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def generate_from_spreadsheet_data(texts, output_dir=OUTPUT_DIR):
    """
    Generate Instagram Reels from list of text entries

    Args:
        texts: List of strings to use as reel text
        output_dir: Where to save the output videos
    """
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n📹 Generating {len(texts)} Instagram Reels...")
    print(f"   Output: {os.path.abspath(output_dir)}\n")

    successful = 0
    failed = 0

    for idx, text in enumerate(texts, 1):
        if not text or not text.strip():
            continue

        print(f"[{idx}/{len(texts)}] {text[:60]}{'...' if len(text) > 60 else ''}")

        video_filename = f"reel_{idx:03d}.mp4"
        video_path = os.path.join(output_dir, video_filename)

        if create_video_with_text(text, video_path):
            successful += 1
        else:
            failed += 1

    print(f"\n{'='*70}")
    print(f"✓ Created: {successful} reels")
    if failed > 0:
        print(f"✗ Failed: {failed} reels")
    print(f"{'='*70}")
    print(f"\n📁 Videos saved to: {os.path.abspath(output_dir)}")
    print(f"📱 Ready to upload to Instagram!\n")

    return successful, failed


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Generate Instagram Reels from text data')
    parser.add_argument('--create-sample', action='store_true',
                       help='Create a sample Canva template')
    parser.add_argument('--output-dir', default=OUTPUT_DIR,
                       help='Output directory for videos')
    parser.add_argument('--data-file', default='reel_texts.json',
                       help='JSON file with list of texts to use')

    args = parser.parse_args()

    print("="*70)
    print("Instagram Reels Generator")
    print("="*70)

    # Create sample template if requested
    if args.create_sample:
        create_sample_template()
        print("\nTo generate reels, provide text data in reel_texts.json:")
        print('  [')
        print('    "Your first reel text here",')
        print('    "Your second reel text here"')
        print('  ]')
        return

    # Load text data
    if not os.path.exists(args.data_file):
        print(f"\n❌ Data file not found: {args.data_file}")
        print(f"\nCreate {args.data_file} with your reel texts:")
        print('  [')
        print('    "Transform your health with nutrition science 🌱",')
        print('    "Small changes today = Big results tomorrow 💪"')
        print('  ]')
        return

    try:
        with open(args.data_file, 'r', encoding='utf-8') as f:
            texts = json.load(f)
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON in {args.data_file}")
        return
    except Exception as e:
        print(f"❌ Error reading {args.data_file}: {e}")
        return

    if not texts:
        print(f"❌ No text data found in {args.data_file}")
        return

    # Check for template
    if not os.path.exists(CANVA_TEMPLATE):
        print(f"\n⚠️  Canva template not found: {CANVA_TEMPLATE}")
        print(f"\nOptions:")
        print(f"  1. Export your Canva design as PNG and save as: {CANVA_TEMPLATE}")
        print(f"  2. Use --create-sample to generate a sample template")
        return

    # Generate reels
    generate_from_spreadsheet_data(texts, args.output_dir)


if __name__ == "__main__":
    main()
