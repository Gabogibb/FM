# Using Google Workspace MCP for Instagram Reels

## What is Google Workspace MCP?

**MCP (Model Context Protocol)** is a secure way for Claude Code to access your Google Workspace files without storing credentials. Instead of managing API keys:

- ✅ Claude Code accesses your Google Drive/Sheets directly via MCP
- ✅ Uses your existing Google Workspace authentication (gabriel@unbreakablemind.co)
- ✅ Automatic file access based on your permissions
- ✅ No credential files to manage

## How It Works

### Step 1: Export Canva Template
1. Open your Canva design: https://www.canva.com/design/DAHCg_oIZbc/edit
2. Click **Download** → **PNG**
3. Save as `canva_template.png` in the project directory

### Step 2: Identify Your Spreadsheet
Option A - If you have the spreadsheet URL:
- Copy the ID from: `https://docs.google.com/spreadsheets/d/[ID HERE]/edit`

Option B - If you need to find it:
- Claude Code can search your Google Drive for spreadsheets
- Just tell it what the spreadsheet is called

### Step 3: Update Script Config
Edit `instagram_reels_generator.py`:

```python
SPREADSHEET_ID = "your-spreadsheet-id-here"  # Update this line
```

### Step 4: Run via Claude Code

**In Claude Code terminal:**

```bash
# Option 1: Local test (no Google access)
python test_reels_generator.py

# Option 2: Full automation with Google MCP
python instagram_reels_generator.py
```

Claude Code will:
1. 🔍 Use MCP to read your Google Spreadsheet
2. 🎬 Generate 9-second videos locally
3. 📤 Upload finished videos to Google Drive folder
4. ✅ Display confirmation with Drive folder link

## Workflow Example

**Spreadsheet Format** (First column = Reel text):

| Text for Reel | Source | Notes |
|---|---|---|
| Transform your health with better nutrition 🌱 | Blog | Wellness |
| Your gut health affects your mood | Research | Health facts |

**Result:**
- ✅ `reel_001.mp4` - Created locally & uploaded to Drive
- ✅ `reel_002.mp4` - Created locally & uploaded to Drive
- ✅ Google Drive folder: "Instagram Reels" 
  - Ready to download and upload to Instagram!

## Troubleshooting

### "File not found" (Spreadsheet)
- Verify the SPREADSHEET_ID is correct
- Make sure the spreadsheet is in your Google Drive
- Claude Code will need read access (usually automatic)

### "Canva template not found"
- Export the Canva design as PNG
- Save as `canva_template.png` in the same directory
- Re-run the script

### Videos not uploading to Drive
- Verify you have write access to Google Drive
- Check that the folder "Instagram Reels" doesn't already exist
- Claude Code will create it if needed

## Advantages Over Manual Setup

| Feature | Manual OAuth | Google Workspace MCP |
|---|---|---|
| **Setup Time** | 15-20 minutes | 2 minutes |
| **API Keys to Manage** | Yes (risky) | No (more secure) |
| **Works in Claude Code** | No | Yes ✅ |
| **Automatic Auth** | No | Yes ✅ |
| **No Credential Files** | No | Yes ✅ |

## Next Steps

1. ✅ Export Canva as PNG
2. ✅ Note your spreadsheet ID
3. ✅ Run: `python instagram_reels_generator.py`
4. ✅ Videos appear in Google Drive folder "Instagram Reels"
5. ✅ Download and upload to Instagram!

## Questions?

If you need to:
- **Find a spreadsheet**: "Find my Instagram Reels spreadsheet"
- **Check what's in a sheet**: "Show me what's in my spreadsheet"
- **Create new reels**: "Generate 10 reels from my spreadsheet"

Just ask Claude Code - it can handle all of this via MCP!
