# Instagram Reels Generator - Setup Guide

## Overview
This automation tool uses **Google Workspace MCP** to read text from your Google Spreadsheet and creates 9-second vertical Instagram Reels (9:16 ratio) with your Canva design template.

**Advantage**: No authentication setup needed! Uses your existing Google Workspace account via MCP.

## Prerequisites

### 1. Export Your Canva Design
- Open your Canva design: https://www.canva.com/design/DAHCg_oIZbc/edit
- Click **Download** (top right)
- Choose **PNG** format
- Save as `canva_template.png` in this project directory

### 2. Google Workspace Setup (Using MCP)
No authentication needed! The system uses Google Workspace MCP which automatically handles authentication:
- Your Google account (gabriel@unbreakablemind.co) is already authenticated
- Claude Code will use MCP tools to read/write from Google Drive
- All files are accessed via your existing permissions

### 3. Identify Your Google Spreadsheet
Locate the spreadsheet containing your Instagram Reel text:
- **Spreadsheet URL format**: `https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit`
- Extract the ID between `/d/` and `/edit`
- Example: `1iV-q-GmyS8K8_kQ-CGGQJwrOQdPAKyrE0SptuE7NF-c`

Update `SPREADSHEET_ID` in the Python script with your ID

## Spreadsheet Format

Your spreadsheet should have text in the **first column** of each row:

| Column A (Text for Reel) | Column B | Column C |
|---|---|---|
| First text for reel | Additional data | More data |
| Second text for reel | Additional data | More data |
| Third text for reel | Additional data | More data |

**Current Spreadsheet ID:** `1iV-q-GmyS8K8_kQ-CGGQJwrOQdPAKyrE0SptuE7NF-c`

To use a different spreadsheet:
1. Open `instagram_reels_generator.py`
2. Change `SPREADSHEET_ID` to your spreadsheet's ID (from the URL)

## Installation

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Verify FFmpeg
The script requires FFmpeg for video creation:

**macOS (Homebrew):**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html or use:
```bash
choco install ffmpeg
```

### Step 3: Update Your Spreadsheet ID
Edit `instagram_reels_generator.py`:

```python
SPREADSHEET_ID = "1iV-q-GmyS8K8_kQ-CGGQJwrOQdPAKyrE0SptuE7NF-c"  # ← Update this
```

Replace with your actual spreadsheet ID (see prerequisite step 3 for how to find it)

## Usage

### Run the Generator
```bash
python instagram_reels_generator.py
```

**What it does:**
1. ✅ Reads all rows from your Google Spreadsheet
2. ✅ Creates 9-second vertical videos (1080×1920px)
3. ✅ Overlays text from your spreadsheet onto the Canva template
4. ✅ Saves videos locally to `./instagram_reels/`
5. ✅ Uploads all videos to a Google Drive folder named "Instagram Reels"

## Output

### Local Files
Videos are saved in `./instagram_reels/` as:
- `reel_001.mp4`
- `reel_002.mp4`
- `reel_003.mp4`
- etc.

### Google Drive
A folder called "Instagram Reels" is created with all the video files.

## Customization

### Change Video Duration
Edit this line in `instagram_reels_generator.py`:
```python
DURATION = 9  # Change to desired seconds
```

### Change Text Size/Color
Modify the `create_video_with_text()` method:
```python
txt_clip = TextClip(
    text,
    fontsize=50,      # Change font size
    color='white',    # Change color (white, black, red, etc.)
    font='Arial-Bold' # Change font
)
```

### Change Text Position
Modify this line:
```python
txt_clip = txt_clip.set_position('center')  # Try 'bottom', 'top', or specific coordinates
```

## Troubleshooting

### "Canva template not found"
- Make sure you exported your Canva design as PNG
- Save it as `canva_template.png` in the same directory as the script

### "Error reading spreadsheet"
- Verify you've granted access to the service account email
- Check the SPREADSHEET_ID is correct
- Make sure Google Sheets API is enabled in Cloud Console

### "FFmpeg not found"
- Ensure FFmpeg is installed and in your PATH
- Verify with: `ffmpeg -version`

### "Video codec error"
- This usually means FFmpeg is missing optional codecs
- Reinstall FFmpeg with all libraries

## Advanced Features

### Batch Processing
To generate reels from multiple sheets:
```bash
python instagram_reels_generator.py --sheet-id sheet_id_1
python instagram_reels_generator.py --sheet-id sheet_id_2
```

### Upload Only
To only upload existing videos to Drive without regenerating:
```bash
python instagram_reels_generator.py --upload-only
```

## Instagram Upload Tips

1. **Video Format**: MP4 is supported by Instagram
2. **Dimensions**: 9:16 vertical format is perfect for Reels
3. **Duration**: 9 seconds fits Instagram Reels
4. **Captions**: Add in Instagram's native caption editor for better engagement

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Verify all files are in the correct location
3. Run with `--verbose` flag for detailed logs

## Next Steps

1. ✅ Export Canva design as PNG
2. ✅ Set up Google Cloud credentials
3. ✅ Install Python dependencies
4. ✅ Run `python instagram_reels_generator.py`
5. ✅ Videos will appear in Google Drive folder "Instagram Reels"
6. ✅ Download and upload to Instagram!
