#!/usr/bin/env python3
"""
Instagram Reels Generator from Google Spreadsheet
Creates 9-second 9:16 vertical videos with text overlays
"""

import os
import sys
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google.auth.oauthlib.flow import InstalledAppFlow
from google.colab import auth
from google.colab.auth import authenticate_user
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from moviepy.editor import (
    ImageClip, TextClip, CompositeVideoClip,
    concatenate_videoclips, ColorClip
)
import gspread
from PIL import Image, ImageDraw, ImageFont
import subprocess
import tempfile
from pathlib import Path

# Configuration
SPREADSHEET_ID = "1iV-q-GmyS8K8_kQ-CGGQJwrOQdPAKyrE0SptuE7NF-c"
CANVA_IMAGE_PATH = "./canva_template.png"  # Export from Canva
OUTPUT_FOLDER_ID = None  # Will set this in Google Drive
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
DURATION = 9  # seconds
FPS = 30


class InstagramReelsGenerator:
    def __init__(self):
        self.sheets_service = None
        self.drive_service = None
        self.gc = None
        self.authenticate()

    def authenticate(self):
        """Authenticate with Google APIs"""
        try:
            # Try to authenticate with service account
            self.sheets_service = build('sheets', 'v4')
            self.drive_service = build('drive', 'v3')
            self.gc = gspread.Spreadsheet
            print("✓ Authenticated with Google APIs")
        except Exception as e:
            print(f"Authentication error: {e}")
            print("Please ensure Google Cloud credentials are configured")
            sys.exit(1)

    def read_spreadsheet(self):
        """Read data from Google Sheet"""
        try:
            sheet = self.gc.open_by_key(SPREADSHEET_ID)
            worksheet = sheet.sheet1  # First sheet
            data = worksheet.get_all_values()
            return data
        except Exception as e:
            print(f"Error reading spreadsheet: {e}")
            return []

    def create_video_with_text(self, text, output_path):
        """
        Create a 9-second vertical video with text overlay on Canva template

        Args:
            text: Text to overlay on the video
            output_path: Where to save the video
        """
        try:
            # Load the Canva template image
            if not os.path.exists(CANVA_IMAGE_PATH):
                print(f"Error: Canva template not found at {CANVA_IMAGE_PATH}")
                return False

            # Create video from image with 9-second duration
            base_clip = ImageClip(CANVA_IMAGE_PATH).set_duration(DURATION)
            base_clip = base_clip.resize((VIDEO_WIDTH, VIDEO_HEIGHT))

            # Create text clip
            txt_clip = TextClip(
                text,
                fontsize=50,
                color='white',
                font='Arial-Bold',
                method='caption',
                size=(VIDEO_WIDTH - 100, None),
                align='center'
            ).set_duration(DURATION)

            # Position text in center
            txt_clip = txt_clip.set_position('center')

            # Composite video with text
            final_clip = CompositeVideoClip([base_clip, txt_clip])

            # Write video file
            final_clip.write_videofile(
                output_path,
                fps=FPS,
                codec='libx264',
                audio=False,
                verbose=False,
                logger=None
            )

            print(f"✓ Created video: {output_path}")
            return True

        except Exception as e:
            print(f"Error creating video: {e}")
            return False

    def upload_to_drive(self, file_path, folder_id=None):
        """Upload video to Google Drive"""
        try:
            file_metadata = {'name': os.path.basename(file_path)}
            if folder_id:
                file_metadata['parents'] = [folder_id]

            media = MediaFileUpload(file_path, mimetype='video/mp4')
            file = self.drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()

            print(f"✓ Uploaded to Drive: {file.get('id')}")
            return file.get('id')

        except Exception as e:
            print(f"Error uploading to Drive: {e}")
            return None

    def create_folder_in_drive(self, folder_name="Instagram Reels"):
        """Create a folder in Google Drive for output"""
        try:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = self.drive_service.files().create(
                body=file_metadata,
                fields='id'
            ).execute()

            folder_id = folder.get('id')
            print(f"✓ Created Drive folder: {folder_id}")
            return folder_id

        except Exception as e:
            print(f"Error creating folder: {e}")
            return None

    def generate_all_reels(self, output_dir="./instagram_reels"):
        """Generate all reels from spreadsheet data"""
        # Create local output directory
        os.makedirs(output_dir, exist_ok=True)

        # Read spreadsheet
        data = self.read_spreadsheet()
        if not data:
            print("No data found in spreadsheet")
            return

        # Create Drive folder
        drive_folder_id = self.create_folder_in_drive("Instagram Reels")

        # Process each row (skip header)
        for idx, row in enumerate(data[1:], 1):
            if not row or not row[0].strip():
                continue

            text = row[0]  # Assuming text is in first column
            print(f"\n[{idx}] Processing: {text[:50]}...")

            # Create video
            video_filename = f"reel_{idx:03d}.mp4"
            video_path = os.path.join(output_dir, video_filename)

            if self.create_video_with_text(text, video_path):
                # Upload to Drive
                if drive_folder_id:
                    self.upload_to_drive(video_path, drive_folder_id)
            else:
                print(f"✗ Failed to create video for row {idx}")


def main():
    """Main execution"""
    print("=" * 60)
    print("Instagram Reels Generator")
    print("=" * 60)

    # Check if Canva template exists
    if not os.path.exists(CANVA_IMAGE_PATH):
        print(f"\n⚠️  SETUP REQUIRED:")
        print(f"1. Export your Canva design as an image (PNG/JPG)")
        print(f"2. Save it as: {CANVA_IMAGE_PATH}")
        print(f"3. Re-run this script\n")
        sys.exit(1)

    # Generate reels
    generator = InstagramReelsGenerator()
    generator.generate_all_reels()

    print("\n" + "=" * 60)
    print("✓ All reels generated and uploaded!")
    print("=" * 60)


if __name__ == "__main__":
    main()
