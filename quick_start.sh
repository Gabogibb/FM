#!/bin/bash

echo "======================================================================"
echo "Instagram Reels Generator - Quick Start"
echo "======================================================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi
echo "✓ Python 3 found"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found"
    exit 1
fi
echo "✓ pip3 found"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -q -r requirements.txt
echo "✓ Dependencies installed"

# Check FFmpeg
echo ""
echo "🎬 Checking FFmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ FFmpeg not found. Please install:"
    echo "   macOS: brew install ffmpeg"
    echo "   Ubuntu/Debian: sudo apt-get install ffmpeg"
    echo "   Windows: Download from https://ffmpeg.org/download.html"
    exit 1
fi
echo "✓ FFmpeg found"

# Test with local version
echo ""
echo "🧪 Running test version (no Google auth needed)..."
python3 test_reels_generator.py

echo ""
echo "======================================================================"
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Export your Canva design as PNG and save as canva_template.png"
echo "  2. Follow SETUP_GUIDE.md for Google authentication"
echo "  3. Run: python3 instagram_reels_generator.py"
echo "======================================================================"
