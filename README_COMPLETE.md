# Instagram Reels Generator - Complete System

**Create professional 9:16 vertical Instagram Reels directly from a Google Spreadsheet with automatic text overlays.**

This system uses Claude Code's Google Workspace MCP tools to read from your spreadsheet and generate Instagram-ready videos in minutes.

## 🚀 Quick Start (3 Steps)

### 1️⃣ Prepare Your Canva Design

Export your Canva design as PNG and save as `canva_template.png`:

```bash
# Or create a sample template
python3 generate_reels.py --create-sample
```

### 2️⃣ Prepare Your Text Data

Create `reel_texts.json` with your Instagram Reel text:

```json
[
  "Transform your health with nutrition science 🌱",
  "Small changes today = Big results tomorrow 💪",
  "Your gut health impacts your mental clarity"
]
```

### 3️⃣ Generate Videos

```bash
python3 generate_reels.py
```

✅ Videos are ready in `instagram_reels/` folder!

---

## 📊 Integration with Google Spreadsheet

### Automatic Workflow Using Claude Code

Ask Claude Code to automate the complete process:

```
"Read my Google Spreadsheet named 'Instagram Reels', extract the text 
from column A, and generate Instagram Reel videos with my Canva 
template. Save them to the instagram_reels/ folder."
```

Claude Code will:
1. 🔍 Search for your spreadsheet using `mcp__Google-Drive__search_files`
2. 📖 Read the content with `mcp__Google-Drive__read_file_content`
3. ✂️ Extract text from the first column
4. 🎬 Generate videos with `generate_reels.py`
5. 💾 Save to `instagram_reels/` ready to upload

### Manual Workflow

If not using Claude Code's MCP tools:

```bash
# Export Google Sheet as CSV, then:
python3 mcp_helper.py --process-data your_export.csv

# Or manually create reel_texts.json
python3 generate_reels.py
```

---

## 📁 Scripts Overview

### `generate_reels.py` - Main Video Generator
**Creates 9:16 vertical videos with text overlays**

```bash
# Generate videos from reel_texts.json
python3 generate_reels.py

# Create sample template
python3 generate_reels.py --create-sample

# Custom output directory
python3 generate_reels.py --output-dir my_reels
```

### `spreadsheet_to_reels.py` - Orchestrator
**Coordinates the complete workflow**

```bash
python3 spreadsheet_to_reels.py
```

### `mcp_helper.py` - Data Processing Helper
**Process spreadsheet data from various formats**

```bash
# Create sample spreadsheet data
python3 mcp_helper.py --create-sample

# Process exported CSV or JSON
python3 mcp_helper.py --process-data exported.csv
```

---

## 🎥 Video Specifications

| Spec | Value |
|------|-------|
| **Aspect Ratio** | 9:16 (vertical) |
| **Resolution** | 1080×1920 pixels |
| **Duration** | 9 seconds |
| **Frame Rate** | 30 FPS |
| **Codec** | H.264 (libx264) |
| **Format** | MP4 |
| **Instagram Compatible** | ✅ Yes |

---

## 📦 Installation

### Requirements
- Python 3.8+
- FFmpeg
- 2GB free disk space for video encoding

### Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `moviepy>=1.0.3` - Video editing
- `pillow>=10.0.0` - Image processing
- `imageio-ffmpeg>=0.4.9` - Video codec

### Install FFmpeg

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

### Verify Installation

```bash
python3 --version  # Should be 3.8+
ffmpeg -version    # Should show version
python3 -c "import moviepy; print('✓ MoviePy installed')"
```

---

## 📊 Spreadsheet Format

Your Google Spreadsheet should have text in the **first column**:

| Column A | Column B | Column C |
|----------|----------|----------|
| Your reel text 1 | Optional | Optional |
| Your reel text 2 | Optional | Optional |
| Your reel text 3 | Optional | Optional |

Example for health/wellness niche:
| Column A | Category | Notes |
|----------|----------|-------|
| Transform your health with nutrition science 🌱 | Wellness | Posted Friday |
| Your gut health impacts mental clarity | Health | High engagement |
| Learn why detoxification is natural | Wellness | 5K views |

---

## 🎨 Customization

### Text Size and Color

Edit `generate_reels.py`:

```python
txt_clip = TextClip(
    text,
    fontsize=48,          # Increase for larger text
    color='white',        # Change color: 'red', 'blue', etc.
    font='Arial-Bold',    # Other fonts: 'Courier', 'Times-New-Roman'
    method='caption',
    size=(VIDEO_WIDTH - 100, None),
    align='center'        # 'left', 'center', 'right'
)
```

### Text Position

```python
# Center (default)
txt_clip = txt_clip.set_position('center')

# Other options
txt_clip = txt_clip.set_position('top')      # Top center
txt_clip = txt_clip.set_position('bottom')   # Bottom center
txt_clip = txt_clip.set_position((x, y))     # Specific coordinates
```

### Video Duration

```python
DURATION = 9  # Change to 15, 20, 30, etc.
```

### Output Folder

```bash
python3 generate_reels.py --output-dir custom_folder
```

---

## 🔧 Using Claude Code's MCP Tools

Claude Code has built-in Google Workspace MCP tools for seamless integration:

### Available Tools

1. **Search Files**
   ```
   mcp__Google-Drive__search_files(
     query="title contains 'Instagram Reels'"
   )
   ```

2. **Get File Metadata**
   ```
   mcp__Google-Drive__get_file_metadata(
     fileId="spreadsheet_id"
   )
   ```

3. **Read File Content**
   ```
   mcp__Google-Drive__read_file_content(
     fileId="spreadsheet_id"
   )
   ```

### How Claude Integrates

When you ask Claude to read your spreadsheet:

1. Claude searches for your file
2. Claude reads the spreadsheet content
3. Claude extracts text from column A
4. Claude saves to `reel_texts.json`
5. Claude runs `generate_reels.py`
6. Claude verifies videos were created
7. Videos are ready in `instagram_reels/`!

---

## 📈 Performance

**Time per Video:**
- Video encoding: 20-40 seconds (varies by system)
- 10 videos: 3-5 minutes
- 50 videos: 15-30 minutes

**File Sizes:**
- Small text: 2-3 MB
- Medium text: 3-5 MB
- Large text: 5-8 MB

**Tips for Faster Processing:**
- Close other applications
- Use SSD for faster disk I/O
- Reduce system load while encoding

---

## 🐛 Troubleshooting

### "Canva template not found"
```bash
# Export from Canva and save as canva_template.png
# OR create sample:
python3 generate_reels.py --create-sample
```

### "FFmpeg not found"
```bash
# Install FFmpeg (see Installation section)
ffmpeg -version  # Verify installation
```

### "No data found in reel_texts.json"
```bash
# Create example data
cp reel_texts_example.json reel_texts.json
```

### "Video encoding is very slow"
- This is normal! Video encoding is CPU-intensive
- Close other applications
- Consider upgrading system RAM or CPU

### "Out of memory"
```bash
# Process fewer videos, or upgrade system RAM
# Or reduce video duration to save memory
```

### "Text not displaying correctly"
- Reduce fontsize in `generate_reels.py`
- Make sure template image exists
- Try a different font (Arial, Courier, Helvetica)

---

## 📱 Instagram Upload

### After Videos Are Generated

1. **Download Videos**
   - Find videos in `instagram_reels/` folder
   - Files: `reel_001.mp4`, `reel_002.mp4`, etc.

2. **Upload to Instagram**
   - Open Instagram app
   - Tap **+** icon
   - Select **Reel**
   - Upload video
   - Add caption, hashtags, music
   - Post!

3. **Tips for Maximum Engagement**
   - Add trending sounds from Instagram's library
   - Use 5-10 relevant hashtags
   - Post during peak hours (weekdays 9-10am, 6-9pm)
   - Engage with comments quickly
   - Use captions for accessibility

---

## 📚 File Structure

```
instagram_reels_generator/
├── generate_reels.py              ← Main video generator
├── spreadsheet_to_reels.py        ← Orchestrator
├── mcp_helper.py                  ← Data processing helper
├── canva_template.png             ← Your Canva design
├── reel_texts.json                ← Text data (generated by Claude)
├── reel_texts_example.json        ← Example data
├── instagram_reels/               ← Output videos
│   ├── reel_001.mp4
│   ├── reel_002.mp4
│   └── reel_003.mp4
├── requirements.txt               ← Python dependencies
├── INSTAGRAM_REELS_GUIDE.md       ← Detailed guide
└── README_COMPLETE.md             ← This file
```

---

## 🎯 Use Cases

### Health & Wellness
```json
[
  "Transform your health with nutrition science 🌱",
  "Your gut health impacts your mental clarity",
  "7 superfoods that heal your digestive system"
]
```

### Business Tips
```json
[
  "Your network is your net worth 🤝",
  "Build it before you need it",
  "Consistency beats perfection every time"
]
```

### Personal Development
```json
[
  "Your limiting beliefs are just stories",
  "Small daily progress compounds into massive results",
  "The best time to start was yesterday"
]
```

### E-commerce
```json
[
  "Transform your space with our premium collection",
  "Limited time: 30% off all home essentials",
  "Customer favorite: This product has 5-star reviews"
]
```

---

## 💡 Tips & Tricks

### Best Practices
- Keep text to 1-3 short sentences
- Use emojis for visual interest
- Match text to your Canva design
- Test first video before bulk generation
- Use consistent branding across all reels

### Engagement Tips
- Ask questions in captions ("What's your favorite?")
- Use trending sounds and music
- Post consistently (2-3x per week)
- Respond to comments within first hour
- Collaborate with other creators

### Technical Tips
- Precompile Canva designs for consistent branding
- Keep text font size readable (48pt+ recommended)
- Test videos on mobile before posting
- Backup reel_texts.json for easy re-generation

---

## 🚀 Advanced Features

### Batch Processing
```bash
# Process multiple spreadsheets
for id in "id1" "id2" "id3"; do
  python3 mcp_helper.py --spreadsheet-id $id
  python3 generate_reels.py --output-dir "batch_$id"
done
```

### Add Custom Fonts
```python
# In generate_reels.py
font='Courier-Bold'  # System fonts available
```

### Custom Aspect Ratios
```python
# Modify dimensions for different formats
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920  # Change for other ratios
```

---

## 📞 Support & Help

### Getting Help

1. **Installation Issues**
   - Verify Python 3.8+: `python3 --version`
   - Verify FFmpeg: `ffmpeg -version`
   - Check dependencies: `pip list`

2. **Data Issues**
   - Ensure `reel_texts.json` is valid JSON
   - Check spreadsheet has text in column A
   - Verify file encoding is UTF-8

3. **Video Issues**
   - Ensure `canva_template.png` exists
   - Check template is PNG format
   - Verify template dimensions are landscape or portrait

4. **Claude Code Integration**
   - Ask Claude to search for your spreadsheet
   - Provide spreadsheet name or ID
   - Claude will handle the rest!

---

## 📄 License

Open source and free for personal and commercial use.

---

## 🎉 Next Steps

1. ✅ Export your Canva design as PNG
2. ✅ Create/prepare your Google Spreadsheet
3. ✅ Install dependencies: `pip install -r requirements.txt`
4. ✅ Install FFmpeg
5. ✅ Ask Claude Code to read your spreadsheet
6. ✅ Videos generate automatically
7. ✅ Download and upload to Instagram!

---

**Happy creating! 🎬📱**
