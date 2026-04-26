# Instagram Reels Generator - Complete Guide

Create professional 9:16 vertical Instagram Reels from a Google Spreadsheet with automatic text overlays.

## Quick Start (5 minutes)

### 1. Prepare Your Canva Template

- Open Canva: https://www.canva.com
- Create or open a 1080×1920px design (portrait)
- Click **Download** → Select **PNG**
- Save as `canva_template.png` in this directory

Or create a sample template:
```bash
python3 generate_reels.py --create-sample
```

### 2. Prepare Your Text Data

Create a `reel_texts.json` file with your Instagram Reel text:

```json
[
  "Transform your health with proven nutrition science 🌱",
  "Your gut health directly impacts your mental clarity",
  "Learn why detoxification is your body's natural superpower",
  "Small changes today = Big results tomorrow 💪"
]
```

### 3. Generate Reels

```bash
python3 generate_reels.py
```

Your videos will be saved in `instagram_reels/` folder, ready to upload!

---

## Complete Workflow with Google Spreadsheet

This guide uses Claude Code's **Google Workspace MCP tools** to read directly from your Google Spreadsheet.

### Step 1: Set Up Your Google Spreadsheet

Your spreadsheet should have text in the **first column**:

| Column A (Your Reel Text) | Column B | Column C |
|---|---|---|
| Text for first reel | Optional data | Optional data |
| Text for second reel | Optional data | Optional data |
| Text for third reel | Optional data | Optional data |

### Step 2: Export Canva Template as PNG

1. Open your Canva design
2. Click **Download**
3. Choose **PNG** format
4. Save as `canva_template.png` in this directory

### Step 3: Use Claude Code's MCP Tools to Read Spreadsheet

Claude Code can read your Google Spreadsheet using:
- `search_files` - Find your spreadsheet by name
- `get_file_metadata` - Get file details
- `read_file_content` - Read spreadsheet data

**Ask Claude Code to:**

```
Use the Google Workspace MCP tools to:
1. Search for my spreadsheet: "Search for a file named 'Instagram Reels' or containing Instagram text"
2. Read the content and extract all text from the first column
3. Save it as reel_texts.json
4. Run: python3 generate_reels.py
```

### Step 4: Generate Your Reels

Claude will execute these MCP tools, then run:

```bash
python3 generate_reels.py
```

Videos are generated in `instagram_reels/` folder.

---

## Manual Setup (If Not Using Claude Code's MCP Tools)

### Option A: From CSV Export

1. Export your Google Sheet as CSV
2. Run: `python3 mcp_helper.py --process-data exported_sheet.csv`
3. Then: `python3 generate_reels.py`

### Option B: From JSON

1. Create `reel_texts.json` with your texts (see Quick Start)
2. Run: `python3 generate_reels.py`

### Option C: From Sample Data

```bash
python3 mcp_helper.py --create-sample
python3 generate_reels.py
```

---

## File Structure

```
/home/user/FM/
├── generate_reels.py              # Main generator script
├── spreadsheet_to_reels.py        # Spreadsheet orchestrator
├── mcp_helper.py                  # Helper for data processing
├── canva_template.png             # Your Canva design (PNG)
├── reel_texts.json                # Text data for reels
├── instagram_reels/               # Output folder with videos
│   ├── reel_001.mp4
│   ├── reel_002.mp4
│   └── reel_003.mp4
└── requirements.txt               # Python dependencies
```

---

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Dependencies:
- `moviepy` - Video generation
- `pillow` - Image processing
- `imageio-ffmpeg` - Video codec

### 2. Install FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**Windows:**
Download from: https://ffmpeg.org/download.html

### 3. Verify Installation

```bash
python3 --version  # Should be 3.8+
ffmpeg -version    # Should show version info
```

---

## Video Specifications

**Instagram Reels Requirements:**
- **Aspect Ratio:** 9:16 (portrait, vertical)
- **Resolution:** 1080×1920 pixels
- **Duration:** 3-90 seconds (optimized: 15-30 seconds, we use 9 seconds)
- **Format:** MP4, MOV
- **File Size:** Up to 4 GB

**Our Settings:**
- **Width:** 1080px
- **Height:** 1920px
- **Duration:** 9 seconds (configurable)
- **Frame Rate:** 30 FPS
- **Codec:** H.264 (libx264)

---

## Customization

### Change Video Duration

Edit `generate_reels.py`:
```python
DURATION = 9  # Change to 15, 20, 30, etc.
```

### Customize Text Appearance

Edit in `generate_reels.py` function `create_video_with_text()`:

```python
txt_clip = TextClip(
    text,
    fontsize=48,          # Increase for larger text
    color='white',        # Change text color
    font='Arial-Bold',    # Change font
    method='caption',
    size=(VIDEO_WIDTH - 100, None),
    align='center'        # 'left', 'center', or 'right'
).set_duration(DURATION)

# Change text position
txt_clip = txt_clip.set_position('center')  # Try 'top', 'bottom', or (x, y)
```

### Change Output Directory

```bash
python3 generate_reels.py --output-dir my_videos
```

---

## Troubleshooting

### "Canva template not found"
**Solution:** 
1. Export your Canva design as PNG
2. Save as `canva_template.png` in this directory
3. Or run: `python3 generate_reels.py --create-sample`

### "FFmpeg not found"
**Solution:** Install FFmpeg (see Installation section)

### Videos won't encode
**Solution:** Ensure FFmpeg has codecs:
```bash
ffmpeg -codecs | grep h264
```

### Text doesn't fit on video
**Solution:** Reduce `fontsize` in `create_video_with_text()`

### Out of memory
**Solution:** Process fewer videos at a time, or increase system RAM

---

## Using with Claude Code

### Integration

Claude Code can automate the entire workflow:

1. **Read your Google Spreadsheet** using MCP tools
2. **Extract text** from the first column
3. **Generate videos** automatically
4. **Save to folder** ready for upload

### Example Command

Ask Claude Code:
```
"Use Google Workspace MCP to read my Instagram Reels spreadsheet, 
extract the text from column A, create Instagram Reel videos with 
my Canva template, and save them to instagram_reels/ folder"
```

Claude will:
1. Use `mcp__Google-Drive__search_files` to find your spreadsheet
2. Use `mcp__Google-Drive__read_file_content` to read the data
3. Extract text from the first column
4. Run `generate_reels.py` to create videos
5. All videos saved to `instagram_reels/`

---

## Instagram Upload Instructions

### After Videos Are Generated

1. **Download Videos**
   - Videos are in `instagram_reels/` folder
   - Each file is `reel_NNN.mp4`

2. **Upload to Instagram**
   - Open Instagram app
   - Tap **+** → **Reel**
   - Upload video
   - Edit and add captions
   - Post!

3. **Tips for Success**
   - Add music and sounds from Instagram's library
   - Use captions for better engagement
   - Add stickers and effects
   - Hashtags in caption (5-10 relevant hashtags)
   - Post at peak engagement times

---

## Advanced Features

### Batch Processing Multiple Spreadsheets

```bash
for spreadsheet_id in "id1" "id2" "id3"; do
  python3 mcp_helper.py --spreadsheet-id $spreadsheet_id
  python3 generate_reels.py
done
```

### Custom Font

Edit `generate_reels.py`:
```python
font='Arial-Bold'  # Change to other available fonts
```

Available fonts: Arial, Helvetica, Courier, Times New Roman, etc.

### Add Music or Audio

Extend `create_video_with_text()` to add audio tracks using moviepy's `AudioFileClip`.

---

## API Integration

### Using Google Sheets API Directly

If you prefer direct API access (not using MCP):

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

creds = service_account.Credentials.from_service_account_file('credentials.json')
sheets = build('sheets', 'v4', credentials=creds)
result = sheets.spreadsheets().values().get(
    spreadsheetId='YOUR_SPREADSHEET_ID',
    range='Sheet1!A2:A'
).execute()
```

---

## Performance

**Time per Video:**
- Text extraction: ~1 second
- Video encoding: 20-40 seconds (depends on system)
- Total for 10 videos: 3-5 minutes

**File Sizes:**
- Small text: 2-3 MB per video
- Medium text: 3-5 MB per video
- Large text: 5-8 MB per video

---

## Support

### Check This First
1. Is FFmpeg installed? `ffmpeg -version`
2. Is canva_template.png present? `ls canva_template.png`
3. Are dependencies installed? `pip list | grep moviepy`
4. Is Python 3.8+? `python3 --version`

### Common Issues
- **Text cut off:** Reduce fontsize or text length
- **Slow video encoding:** System dependent, be patient
- **Memory issues:** Process fewer videos at once
- **Missing codec:** Reinstall FFmpeg with full library

---

## Examples

### Example 1: Fitness Motivation

```json
[
  "Your body is a mirror of your thoughts 💪",
  "30 days to a new you starts with ONE step",
  "Strength doesn't come from what you can do. It comes from overcoming things you once thought you couldn't",
  "The only bad workout is the one that didn't happen 🏋️"
]
```

### Example 2: Business Tips

```json
[
  "Your network is your net worth 🤝",
  "Build it before you need it",
  "Your first customer is your biggest marketing asset",
  "Consistency beats perfection every time ✨"
]
```

### Example 3: Personal Development

```json
[
  "Your limiting beliefs are just stories you accepted as truth",
  "Small daily progress compounds into massive results",
  "Growth happens outside your comfort zone 🌱",
  "The best time to start was yesterday. The second best time is today"
]
```

---

## Next Steps

1. ✅ Export your Canva design as PNG
2. ✅ Prepare your text data in Google Spreadsheet
3. ✅ Install dependencies: `pip install -r requirements.txt`
4. ✅ Install FFmpeg
5. ✅ Run: `python3 generate_reels.py`
6. ✅ Upload videos to Instagram!

---

## License

This tool is open source and free to use for personal and commercial projects.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review the example files and scripts
3. Ensure all dependencies are installed correctly
