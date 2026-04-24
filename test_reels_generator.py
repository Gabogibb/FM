#!/usr/bin/env python3
"""
Simple Test Version - Generates sample Instagram Reels locally
No Google authentication required for testing
"""

import os
from moviepy.editor import (
    ImageClip, TextClip, CompositeVideoClip,
    ColorClip, concatenate_videoclips
)
from PIL import Image, ImageDraw, ImageFont
import csv

# Configuration
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
DURATION = 9
FPS = 30


def create_sample_canva_template(output_path="canva_template.png"):
    """Create a sample template image (substitute for real Canva export)"""
    img = Image.new('RGB', (VIDEO_WIDTH, VIDEO_HEIGHT), color='#1a1a1a')
    draw = ImageDraw.Draw(img)

    # Add some design elements (simple version)
    # Gradient-like effect with rectangles
    for i in range(0, VIDEO_HEIGHT, 50):
        color_val = int(255 * (i / VIDEO_HEIGHT))
        draw.rectangle([(0, i), (VIDEO_WIDTH, i + 50)], fill=(color_val, color_val // 2, 255 - color_val))

    # Add a title area
    title_y = 100
    draw.rectangle([(0, title_y), (VIDEO_WIDTH, title_y + 100)], fill=(0, 0, 0))

    img.save(output_path)
    print(f"✓ Created sample template: {output_path}")
    return output_path


def create_video_with_text(text, output_path, template_path="canva_template.png"):
    """Create a 9-second vertical video with text overlay"""
    try:
        # Load template
        if not os.path.exists(template_path):
            print(f"Creating sample template...")
            create_sample_canva_template(template_path)

        # Create base video clip from image
        base_clip = ImageClip(template_path).set_duration(DURATION)
        base_clip = base_clip.resize((VIDEO_WIDTH, VIDEO_HEIGHT))

        # Create text clip with wrapping
        txt_clip = TextClip(
            text,
            fontsize=48,
            color='white',
            font='Arial-Bold',
            method='caption',
            size=(VIDEO_WIDTH - 100, None),
            align='center'
        ).set_duration(DURATION)

        # Center the text
        txt_clip = txt_clip.set_position('center')

        # Composite the clips
        final_clip = CompositeVideoClip([base_clip, txt_clip])

        # Write video with H.264 codec
        print(f"  Encoding video... this may take a moment")
        final_clip.write_videofile(
            output_path,
            fps=FPS,
            codec='libx264',
            audio=False,
            verbose=False,
            logger=None
        )

        # Get file size
        file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"  ✓ Created: {output_path} ({file_size_mb:.1f} MB)")
        return True

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def read_csv_data(csv_file="sample_data.csv"):
    """Read text from CSV file"""
    if not os.path.exists(csv_file):
        print(f"Creating sample CSV file: {csv_file}")
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Text for Reel'])
            writer.writerow(['Transform your health with proven nutrition science 🌱'])
            writer.writerow(['Your gut health directly impacts your mental clarity'])
            writer.writerow(['Learn why detoxification is your body\'s natural superpower'])
            writer.writerow(['Small changes today = Big results tomorrow 💪'])
        print(f"✓ Created sample CSV with 4 test reels")

    data = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            if row and row[0].strip():
                data.append(row[0])

    return data


def main():
    print("=" * 70)
    print("Instagram Reels Generator - Test Version (Local)")
    print("=" * 70)
    print()

    # Configuration
    output_dir = "instagram_reels_test"
    csv_file = "sample_data.csv"

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Read data
    print(f"📊 Reading data from: {csv_file}")
    data = read_csv_data(csv_file)

    if not data:
        print("No data found!")
        return

    print(f"Found {len(data)} reels to create\n")

    # Generate videos
    for idx, text in enumerate(data, 1):
        print(f"[{idx}/{len(data)}] Creating reel...")
        print(f"  Text: {text[:60]}{'...' if len(text) > 60 else ''}")

        video_filename = f"reel_{idx:03d}.mp4"
        video_path = os.path.join(output_dir, video_filename)

        create_video_with_text(text, video_path)
        print()

    print("=" * 70)
    print(f"✓ All {len(data)} reels created!")
    print(f"📁 Output folder: {output_dir}")
    print()
    print("Next steps:")
    print("  1. Review the videos in the output folder")
    print("  2. Upload to Instagram Reels")
    print()
    print("To use with Google Spreadsheet:")
    print("  1. Use instagram_reels_generator.py instead")
    print("  2. Follow SETUP_GUIDE.md for Google authentication")
    print("=" * 70)


if __name__ == "__main__":
    main()
