#!/usr/bin/env python3
"""
Instagram Reels Generator - Final Production Version
Produces 6 reels with real video background + PIL overlay:
  - 1080x1920, 30fps, 9 seconds, libx264
  - Center-cropped from 3840x2160 source video (looped from 2.5s)
  - White rounded-rectangle text box in upper portion
  - Bold dark hook text, word-wrapped
  - Black rounded pill "Caption ⬇️" badge below text box
"""

import os
import sys
import subprocess
import tempfile
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ── Constants ──────────────────────────────────────────────────────────────────
W, H        = 1080, 1920
FPS         = 30
DURATION    = 9          # seconds
TOTAL_FRAMES = FPS * DURATION  # 270

SOURCE_VIDEO = "/home/user/FM/source_video.mp4"
OUTPUT_DIR   = Path("/home/user/FM/final_reels")

FONT_BOLD_PATH    = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REGULAR_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# ── Hook texts (6 reels) ───────────────────────────────────────────────────────
HOOKS = [
    "You're not missing fitness.",
    "If you keep DNFing but your fitness is fine, that's not a training problem. It's this...",
    "If you've done the miles and you still DNF'd, you don't need more training. You need this.",
    "If more mileage was enough, you wouldn't still be quitting at the same point every race.",
    '"I\'ve trained for months. I know this distance. Why do I keep making the same decision?" This is why...',
    "You can't run your way out of a decision problem.",
]

# ── Font loader ────────────────────────────────────────────────────────────────
def load_font(path, size):
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()

# ── Rounded rectangle helper ──────────────────────────────────────────────────
def rounded_rect(draw, xy, radius, fill):
    """Draw a filled rounded rectangle. xy = (x1, y1, x2, y2)."""
    x1, y1, x2, y2 = xy
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    draw.ellipse([x1, y1, x1 + 2*radius, y1 + 2*radius], fill=fill)
    draw.ellipse([x2 - 2*radius, y1, x2, y1 + 2*radius], fill=fill)
    draw.ellipse([x1, y2 - 2*radius, x1 + 2*radius, y2], fill=fill)
    draw.ellipse([x2 - 2*radius, y2 - 2*radius, x2, y2], fill=fill)

# ── Build overlay PNG for one hook text ───────────────────────────────────────
def build_overlay(hook_text: str) -> Image.Image:
    """
    Returns a 1080x1920 RGBA image (transparent background) with:
      - White rounded-rect text box (upper-center area)
      - Bold dark hook text inside
      - Black rounded pill "Caption ⬇️" below
    """
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    font_hook    = load_font(FONT_BOLD_PATH, 52)
    font_caption = load_font(FONT_BOLD_PATH, 32)

    # Word-wrap hook text at ~38 chars per line
    wrapped = textwrap.fill(hook_text, width=38)
    lines   = wrapped.split("\n")

    LINE_H   = 52 + 16   # font size + leading
    BOX_PAD  = 36        # padding inside white box
    BOX_W    = 920       # box width
    BOX_RADIUS = 22

    text_block_h = len(lines) * LINE_H - 16  # subtract trailing extra leading
    box_h = text_block_h + BOX_PAD * 2

    # Position: center horizontally, place box top at y=160
    box_x1 = (W - BOX_W) // 2
    box_y1 = 160
    box_x2 = box_x1 + BOX_W
    box_y2 = box_y1 + box_h

    # Draw white rounded rect (semi-transparent: 0.92 alpha = 235/255)
    white_fill = (255, 255, 255, 235)
    rounded_rect(draw, (box_x1, box_y1, box_x2, box_y2), BOX_RADIUS, white_fill)

    # Draw each line of hook text centered inside the box
    text_color = (26, 26, 26, 255)  # #1a1a1a
    ty = box_y1 + BOX_PAD
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_hook)
        tw = bbox[2] - bbox[0]
        tx = (W - tw) // 2
        draw.text((tx, ty), line, font=font_hook, fill=text_color)
        ty += LINE_H

    # ── Caption pill ─────────────────────────────────────────────────────────
    PILL_W      = 210
    PILL_H      = 52
    PILL_RADIUS = PILL_H // 2
    PILL_GAP    = 22     # gap between box bottom and pill top

    pill_x1 = (W - PILL_W) // 2
    pill_y1 = box_y2 + PILL_GAP
    pill_x2 = pill_x1 + PILL_W
    pill_y2 = pill_y1 + PILL_H

    pill_fill = (26, 26, 26, 255)
    rounded_rect(draw, (pill_x1, pill_y1, pill_x2, pill_y2), PILL_RADIUS, pill_fill)

    caption_text = "Caption ⬇️"
    cbbox = draw.textbbox((0, 0), caption_text, font=font_caption)
    cw = cbbox[2] - cbbox[0]
    ch = cbbox[3] - cbbox[1]
    cx = (W - cw) // 2
    cy = pill_y1 + (PILL_H - ch) // 2 - cbbox[1]
    draw.text((cx, cy), caption_text, font=font_caption, fill=(255, 255, 255, 255))

    return overlay

# ── Extract & crop video frames ───────────────────────────────────────────────
def extract_video_frames(tmp_dir: str) -> list[str]:
    """
    Use ffmpeg to:
      1. Loop the 2.5s source video to fill 9 seconds
      2. Center-crop 3840x2160 → 1080x1920
      3. Dump as PNG frames
    Returns sorted list of frame PNG paths.
    """
    print("  Extracting & cropping video frames...")
    frame_pattern = os.path.join(tmp_dir, "frame_%04d.png")

    # Center crop: from 3840x2160 take 1080px wide centered horizontally
    # crop=w:h:x:y  →  1080:1920:(3840-1080)/2:(2160-1920)/2 = 1080:1920:1380:120
    crop_x = (3840 - 1080) // 2   # 1380
    crop_y = (2160 - 1920) // 2   # 120

    cmd = [
        "ffmpeg", "-y",
        "-stream_loop", "-1",          # loop source indefinitely
        "-i", SOURCE_VIDEO,
        "-t", str(DURATION),           # stop at 9 seconds
        "-vf", f"crop=1080:1920:{crop_x}:{crop_y},fps={FPS}",
        "-vsync", "vfr",
        frame_pattern
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ffmpeg frame extraction error:\n{result.stderr[-500:]}")
        sys.exit(1)

    frames = sorted(Path(tmp_dir).glob("frame_*.png"))
    print(f"  Extracted {len(frames)} frames")
    return [str(f) for f in frames]

# ── Composite overlay onto every frame ────────────────────────────────────────
def composite_frames(frame_paths: list[str], overlay: Image.Image, out_dir: str) -> list[str]:
    """Paste the overlay onto each video frame and save to out_dir."""
    composite_paths = []
    total = len(frame_paths)
    for i, fp in enumerate(frame_paths):
        if i % 30 == 0:
            print(f"  Compositing frame {i+1}/{total}...")
        bg = Image.open(fp).convert("RGBA")
        bg.paste(overlay, (0, 0), overlay)
        out_path = os.path.join(out_dir, f"comp_{i:04d}.png")
        bg.convert("RGB").save(out_path)
        composite_paths.append(out_path)
    return composite_paths

# ── Encode frames → MP4 ────────────────────────────────────────────────────────
def encode_video(comp_dir: str, output_path: str):
    frame_pattern = os.path.join(comp_dir, "comp_%04d.png")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", frame_pattern,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "slow",
        "-movflags", "+faststart",
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ffmpeg encode error:\n{result.stderr[-500:]}")
        return False
    return True

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Determine which reels to build (skip existing valid ones)
    to_build = []
    for idx, hook in enumerate(HOOKS, 1):
        out_path = OUTPUT_DIR / f"reel_{idx:02d}.mp4"
        if out_path.exists():
            # Validate via ffprobe
            probe = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries",
                 "stream=codec_type,width,height,duration",
                 "-of", "default=noprint_wrappers=1", str(out_path)],
                capture_output=True, text=True
            )
            if "1080" in probe.stdout and "1920" in probe.stdout:
                print(f"[{idx:02d}] reel_{idx:02d}.mp4 already valid — skipping")
                continue
        to_build.append((idx, hook))

    if not to_build:
        print("All 6 reels already exist and are valid.")
        return

    print(f"\nWill build {len(to_build)} reel(s): {[i for i,_ in to_build]}")

    # Extract video frames ONCE (shared across all reels)
    with tempfile.TemporaryDirectory(prefix="fm_video_") as video_tmp:
        frame_paths = extract_video_frames(video_tmp)

        for idx, hook in to_build:
            out_path = OUTPUT_DIR / f"reel_{idx:02d}.mp4"
            print(f"\n[{idx:02d}/06] Hook: {hook[:60]}{'...' if len(hook)>60 else ''}")

            # Build overlay
            overlay = build_overlay(hook)
            print("  Overlay built.")

            # Composite in a temp directory
            with tempfile.TemporaryDirectory(prefix="fm_comp_") as comp_tmp:
                comp_paths = composite_frames(frame_paths, overlay, comp_tmp)
                print(f"  Encoding {len(comp_paths)} frames → {out_path.name} ...")
                ok = encode_video(comp_tmp, str(out_path))

            if ok:
                size_mb = out_path.stat().st_size / (1024 * 1024)
                print(f"  DONE: {out_path} ({size_mb:.1f} MB)")
            else:
                print(f"  FAILED: {out_path}")

    print("\n" + "="*60)
    print("QA check:")
    for idx in range(1, 7):
        p = OUTPUT_DIR / f"reel_{idx:02d}.mp4"
        if p.exists():
            probe = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries",
                 "stream=codec_type,width,height,duration",
                 "-of", "default=noprint_wrappers=1", str(p)],
                capture_output=True, text=True
            )
            size_mb = p.stat().st_size / (1024 * 1024)
            valid = "1080" in probe.stdout and "1920" in probe.stdout
            status = "PASS" if valid else "FAIL"
            print(f"  [{status}] reel_{idx:02d}.mp4  {size_mb:.1f}MB  {p}")
        else:
            print(f"  [MISS] reel_{idx:02d}.mp4  NOT FOUND")
    print("="*60)


if __name__ == "__main__":
    main()
