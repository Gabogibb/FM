#!/usr/bin/env python3
"""
Instagram Reels production script.
Produces 1080x1920 vertical reels with:
  - Center-cropped 4K source video (looped to 9s at 30fps)
  - White rounded-rectangle text overlay (upper-center)
  - Bold dark hook text inside the box (word-wrapped)
  - Black rounded-pill "Caption ⬇️" badge below the text box
"""

import subprocess
import sys
import os
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ── Configuration ──────────────────────────────────────────────────────────────
SOURCE_VIDEO   = "/home/user/FM/source_video.mp4"
OUTPUT_DIR     = Path("/home/user/FM/final_reels")
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

OUTPUT_W, OUTPUT_H = 1080, 1920
FPS          = 30
DURATION_S   = 9
TOTAL_FRAMES = FPS * DURATION_S   # 270 frames

# Text box
BOX_W        = 900
BOX_PADDING  = 30
BOX_RADIUS   = 20
BOX_COLOR    = (255, 255, 255, 234)   # rgba 255,255,255,0.92
BOX_X        = (OUTPUT_W - BOX_W) // 2  # horizontally centered → 90
BOX_TOP_Y    = 120                       # distance from top of frame

# Hook text
HOOK_FONT_SIZE  = 52
HOOK_COLOR      = (26, 26, 26)       # #1a1a1a
WRAP_WIDTH      = 28                 # characters per line (tighter for large font)

# Caption pill
PILL_W       = 220
PILL_H       = 54
PILL_RADIUS  = 27   # fully rounded ends
PILL_COLOR   = (26, 26, 26, 255)
PILL_TEXT    = "Caption ⬇️"
PILL_FONT_SIZE = 32
PILL_TEXT_COLOR = (255, 255, 255)
PILL_GAP     = 24   # gap between text box and pill

# Hook texts (6 reels)
HOOKS = [
    "You're not missing fitness.",
    "If you keep DNFing but your fitness is fine, that's not a training problem. It's this...",
    "If you've done the miles and you still DNF'd, you don't need more training. You need this.",
    "If more mileage was enough, you wouldn't still be quitting at the same point every race.",
    '"I\'ve trained for months. I know this distance. Why do I keep making the same decision?" This is why...',
    "You can't run your way out of a decision problem.",
]

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ── Helper: rounded-rectangle draw ─────────────────────────────────────────────
def rounded_rect(draw, xy, radius, fill):
    """Draw a filled rounded rectangle onto 'draw'."""
    x0, y0, x1, y1 = xy
    draw.rectangle([x0 + radius, y0, x1 - radius, y1], fill=fill)
    draw.rectangle([x0, y0 + radius, x1, y1 - radius], fill=fill)
    draw.ellipse([x0, y0, x0 + 2*radius, y0 + 2*radius], fill=fill)
    draw.ellipse([x1 - 2*radius, y0, x1, y0 + 2*radius], fill=fill)
    draw.ellipse([x0, y1 - 2*radius, x0 + 2*radius, y1], fill=fill)
    draw.ellipse([x1 - 2*radius, y1 - 2*radius, x1, y1], fill=fill)


# ── Build one overlay PNG for a given hook text ─────────────────────────────────
def make_overlay(hook_text: str) -> Image.Image:
    hook_font  = ImageFont.truetype(FONT_BOLD_PATH, HOOK_FONT_SIZE)
    pill_font  = ImageFont.truetype(FONT_BOLD_PATH, PILL_FONT_SIZE)

    # Word-wrap
    wrapped_lines = textwrap.wrap(hook_text, width=WRAP_WIDTH)

    # Measure text block
    dummy = Image.new("RGBA", (1, 1))
    dd = ImageDraw.Draw(dummy)
    line_heights = []
    line_widths  = []
    for line in wrapped_lines:
        bb = dd.textbbox((0, 0), line, font=hook_font)
        line_widths.append(bb[2] - bb[0])
        line_heights.append(bb[3] - bb[1])

    line_spacing  = 12
    text_block_w  = max(line_widths) if line_widths else 0
    text_block_h  = sum(line_heights) + line_spacing * (len(wrapped_lines) - 1)

    # Box dimensions
    box_h = text_block_h + BOX_PADDING * 2
    box_x0 = BOX_X
    box_y0 = BOX_TOP_Y
    box_x1 = box_x0 + BOX_W
    box_y1 = box_y0 + box_h

    # Pill position (centered, below box)
    pill_x0 = (OUTPUT_W - PILL_W) // 2
    pill_y0 = box_y1 + PILL_GAP
    pill_x1 = pill_x0 + PILL_W
    pill_y1 = pill_y0 + PILL_H

    # Create transparent canvas
    overlay = Image.new("RGBA", (OUTPUT_W, OUTPUT_H), (0, 0, 0, 0))
    draw    = ImageDraw.Draw(overlay)

    # Draw white rounded box
    rounded_rect(draw, (box_x0, box_y0, box_x1, box_y1), BOX_RADIUS, BOX_COLOR)

    # Draw hook text (centered in box)
    text_start_y = box_y0 + BOX_PADDING
    for i, line in enumerate(wrapped_lines):
        bb = draw.textbbox((0, 0), line, font=hook_font)
        lw = bb[2] - bb[0]
        lh = bb[3] - bb[1]
        lx = box_x0 + (BOX_W - lw) // 2
        draw.text((lx, text_start_y), line, font=hook_font, fill=HOOK_COLOR)
        text_start_y += lh + line_spacing

    # Draw pill badge
    rounded_rect(draw, (pill_x0, pill_y0, pill_x1, pill_y1), PILL_RADIUS, PILL_COLOR)
    pbb = draw.textbbox((0, 0), PILL_TEXT, font=pill_font)
    pw  = pbb[2] - pbb[0]
    ph  = pbb[3] - pbb[1]
    px  = pill_x0 + (PILL_W - pw) // 2
    py  = pill_y0 + (PILL_H - ph) // 2
    draw.text((px, py), PILL_TEXT, font=pill_font, fill=PILL_TEXT_COLOR)

    return overlay


# ── Render one reel via ffmpeg ──────────────────────────────────────────────────
def render_reel(hook_index: int, hook_text: str) -> Path:
    output_path = OUTPUT_DIR / f"reel_{hook_index:02d}.mp4"
    overlay_path = OUTPUT_DIR / f"_overlay_{hook_index:02d}.png"

    print(f"\n[{hook_index:02d}] Building overlay for: {hook_text[:60]}...")
    overlay_img = make_overlay(hook_text)
    overlay_img.save(str(overlay_path))
    print(f"  Overlay saved → {overlay_path}")

    # ffmpeg command:
    #   1. Loop source video to 9s (trim + loop)
    #   2. Center-crop 3840x2160 → 1080x1920 (take center 1080w, top 1920h of 2160 — centered vertically)
    #   3. Overlay the PNG (RGBA) onto the video
    #   4. Encode h264 at 30fps, 9s
    cmd = [
        "ffmpeg", "-y",
        # Input 0: looped source video (stream_loop -1 = infinite loop, trimmed to 9s)
        "-stream_loop", "-1",
        "-t", str(DURATION_S),
        "-i", SOURCE_VIDEO,
        # Input 1: static overlay PNG
        "-loop", "1",
        "-t", str(DURATION_S),
        "-i", str(overlay_path),
        # Filter graph
        "-filter_complex",
        (
            # Step 1: crop center 1080x1920 from 3840x2160
            # x offset = (3840-1080)/2 = 1380, y offset = (2160-1920)/2 = 120
            "[0:v]crop=1080:1920:1380:120,fps=30[bg];"
            # Step 2: ensure overlay is same size (it already is 1080x1920)
            "[1:v]format=rgba[ol];"
            # Step 3: overlay RGBA on top of bg using alpha compositing
            "[bg][ol]overlay=0:0:format=auto[out]"
        ),
        "-map", "[out]",
        "-t", str(DURATION_S),
        "-c:v", "libx264",
        "-profile:v", "high",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "medium",
        "-r", str(FPS),
        "-an",   # no audio
        str(output_path),
    ]

    print(f"  Running ffmpeg...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ERROR: ffmpeg failed!\n{result.stderr[-2000:]}")
        sys.exit(1)

    # Clean up temp overlay
    overlay_path.unlink(missing_ok=True)

    size_mb = output_path.stat().st_size / 1_048_576
    print(f"  Done → {output_path}  ({size_mb:.1f} MB)")
    return output_path


# ── QA check ───────────────────────────────────────────────────────────────────
def qa_check(path: Path) -> bool:
    """Verify the output file is a valid video with expected properties."""
    probe_cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_streams", str(path)
    ]
    result = subprocess.run(probe_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  QA FAIL: ffprobe error on {path}")
        return False

    import json
    data = json.loads(result.stdout)
    for s in data.get("streams", []):
        if s.get("codec_type") == "video":
            w = s.get("width")
            h = s.get("height")
            dur = float(s.get("duration", 0))
            codec = s.get("codec_name")
            print(f"  QA: {w}x{h}, {dur:.1f}s, codec={codec}")
            if w == 1080 and h == 1920 and dur >= 8.9 and codec == "h264":
                print(f"  QA PASS ✓")
                return True
            else:
                print(f"  QA FAIL: expected 1080x1920, >=8.9s, h264")
                return False
    print(f"  QA FAIL: no video stream found")
    return False


# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    # Determine which reels to build
    if len(sys.argv) > 1:
        indices = [int(a) for a in sys.argv[1:]]
    else:
        indices = list(range(1, len(HOOKS) + 1))

    failed = []
    for idx in indices:
        hook_text = HOOKS[idx - 1]
        out_path  = render_reel(idx, hook_text)
        if not qa_check(out_path):
            failed.append(idx)

    print("\n" + "="*60)
    if failed:
        print(f"FAILED reels: {failed}")
        sys.exit(1)
    else:
        print(f"All {len(indices)} reel(s) created successfully in {OUTPUT_DIR}")
        for idx in indices:
            p = OUTPUT_DIR / f"reel_{idx:02d}.mp4"
            print(f"  {p}")


if __name__ == "__main__":
    main()
