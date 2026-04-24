#!/usr/bin/env python3
"""
Generate Instagram Reels from Canva design text + spreadsheet content.
Uses PIL to create frames and ffmpeg to produce 9-second MP4 videos.
"""

import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
import textwrap

W, H = 1080, 1920
DURATION = 9
FPS = 30
OUTPUT_DIR = "instagram_reels"

# Each reel: (hook_text, sub_text)
# Text sourced directly from the "UM April 14 - Reels" Canva design
REELS = [
    (
        "Most runners quit at mile 20.\nHere's why.",
        "Your brain gives up 30%\nbefore your body actually does"
    ),
    (
        "You don't need more miles.\nYou need this.",
        "What elite ultrarunners\ntrain differently"
    ),
    (
        "The 5am run myth is quietly\nkilling your race performance.",
        "Here's what the science\nactually says"
    ),
    (
        "Pain at mile 50 isn't physical.\nIt's a story you're telling yourself.",
        "Here's how to rewrite it"
    ),
    (
        "No matter how many miles\nyou log, you still dread race day?",
        "That's not a fitness problem.\nThis is what's actually holding you back"
    ),
    (
        "Trained for months,\ndone everything right,\nbut crumbled mentally on race day?",
        "Your fitness isn't the problem.\nThis is why it happens and how to fix it"
    ),
    (
        "Comparing your weekly miles\nto other runners?",
        "That's costing you finish lines.\nHere's why and what to do instead"
    ),
    (
        "The voice at mile 30\nthat says \"stop\" is lying to you.",
        "Here's how to train your mind\nto keep going"
    ),
    (
        "Every missed training day\nsends you into a guilt spiral?",
        "That's capping your performance.\nHere's how to fix it"
    ),
    (
        "You know exactly what you need\nto run your best race, but\nyou keep holding yourself back.",
        "You don't need a new training plan.\nDo this instead"
    ),
    (
        "My athlete ran his first 100-miler\non 45 miles per week and finished\nstrong in the top 20%.",
        "We didn't focus on mileage.\nWe focused on this instead"
    ),
]


def load_font(size):
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()


def load_font_regular(size):
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()


def draw_centered_text(draw, text, y, font, fill, max_width):
    lines = text.split("\n")
    line_height = font.size + 12
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        x = (W - tw) // 2
        draw.text((x, y), line, font=font, fill=fill)
        y += line_height
    return y


def create_frame(hook, sub):
    img = Image.new("RGB", (W, H), color=(10, 10, 10))
    draw = ImageDraw.Draw(img)

    # Subtle gradient overlay — dark top to slightly lighter middle
    for row in range(H):
        alpha = int(20 * (row / H))
        draw.line([(0, row), (W, row)], fill=(alpha, alpha, alpha + 10))

    # Accent bar
    bar_y = H // 2 - 20
    draw.rectangle([(80, bar_y), (W - 80, bar_y + 4)], fill=(255, 80, 0))

    # Hook text
    hook_font = load_font(72)
    sub_font = load_font_regular(48)

    hook_lines = hook.split("\n")
    line_h = hook_font.size + 18
    total_hook_h = len(hook_lines) * line_h
    hook_y = bar_y - total_hook_h - 40

    draw_centered_text(draw, hook, hook_y, hook_font, (255, 255, 255), W - 160)

    sub_y = bar_y + 30
    draw_centered_text(draw, sub, sub_y, sub_font, (200, 200, 200), W - 160)

    # Branding
    brand_font = load_font_regular(36)
    brand = "@unbreakablemind.co"
    bbox = draw.textbbox((0, 0), brand, font=brand_font)
    bw = bbox[2] - bbox[0]
    draw.text(((W - bw) // 2, H - 100), brand, font=brand_font, fill=(150, 150, 150))

    return img


def make_video(img, output_path):
    frame_path = output_path.replace(".mp4", "_frame.png")
    img.save(frame_path)

    cmd = [
        "ffmpeg", "-y",
        "-loop", "1",
        "-i", frame_path,
        "-t", str(DURATION),
        "-vf", f"scale={W}:{H}",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-r", str(FPS),
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    os.remove(frame_path)

    if result.returncode != 0:
        print(f"  ffmpeg error: {result.stderr[-200:]}")
        return False
    return True


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("=" * 60)
    print("Generating Instagram Reels")
    print("=" * 60)

    created = []
    for i, (hook, sub) in enumerate(REELS, 1):
        out = os.path.join(OUTPUT_DIR, f"reel_{i:02d}.mp4")
        print(f"[{i:02d}/{len(REELS)}] {hook.splitlines()[0][:50]}...")
        img = create_frame(hook, sub)
        if make_video(img, out):
            size_mb = os.path.getsize(out) / (1024 * 1024)
            print(f"       ✓ {out} ({size_mb:.1f} MB)")
            created.append(out)
        else:
            print(f"       ✗ Failed")

    print()
    print("=" * 60)
    print(f"✓ {len(created)}/{len(REELS)} reels created in ./{OUTPUT_DIR}/")
    print("=" * 60)
    return created


if __name__ == "__main__":
    main()
