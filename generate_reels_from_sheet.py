#!/usr/bin/env python3
"""
Instagram Reels Generator - Reads spreadsheet data and creates videos
"""

import os
import json
from pathlib import Path
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip

# Configuration
CANVA_IMAGE_PATH = "./canva_template.png"
VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
DURATION = 9
FPS = 30

# Spreadsheet data - extracted from the shared Google Sheet
REEL_DATA = [
    {
        "id": 1,
        "avatar": "AMT",
        "framework": "Looking for X Avatars",
        "hook": "You're not missing fitness.",
        "text": "We're looking for 10 ultra runners who've DNF'd before and have a revenge race coming up. Not because you weren't fit enough. Because the moment everything got dark — at the aid station, at 2am, at the point in the race where it always goes wrong — you had no plan. You had clichés. \"Just keep going.\" \"One step at a time.\" And when you were truly broken, those words felt empty. That's not a mental weakness. It's a missing skill. I break down the 3 areas most runners never train — the ones that decide whether you finish the race that beat you — in a free mental strength training for ultrarunners. Free training → link in bio or comment \"TOUGH\" and I'll send it."
    },
    {
        "id": 8,
        "avatar": "AMT",
        "framework": "Misdiagnosis Reframe",
        "hook": "If you keep DNFing but your fitness is fine, that's not a training problem. It's this...",
        "text": "Your brain quitting at km 80 isn't a fitness problem. And doing more miles won't fix it. The moment you sat in that chair, or made the call at 2am — your legs had more. You know it. What you didn't have was a plan for when your mind started manufacturing reasons to stop. That's not a training gap. It's a decision gap. In the free mental strength training for ultrarunners, I show you exactly what to build instead. Want it? Comment \"TOUGH\" and I'll send it."
    },
    {
        "id": 9,
        "avatar": "AMT",
        "framework": "Reject the Obvious",
        "hook": "If you've done the miles and you still DNF'd, you don't need more training. You need this.",
        "text": "If you've trained for months, finished races before, and you still DNF'd — you don't need more mileage. You've already proved the fitness is there. What breaks in that moment isn't your body. It's the decision-making process when your brain is sleep-deprived, emotional, and looking for a reason to stop. More mileage doesn't train that. A mental race plan does. In the free mental strength training for ultrarunners, I cover what does. Want it? Comment \"TOUGH\" and I'll send it."
    },
    {
        "id": 10,
        "avatar": "AMT",
        "framework": "Conditional Proof of Failure",
        "hook": "If more mileage was enough, you wouldn't still be quitting at the same point every race.",
        "text": "If more mileage was enough, you wouldn't still be DNFing at the same point every race. Your training log isn't the problem. The problem fires later — at the aid station chair, at 2am, at the moment when your brain starts looking for permission to stop. Mileage doesn't prepare you for that window. A mental race plan does. Want the free mental strength training for ultrarunners? Comment \"TOUGH\" and I'll send it."
    },
    {
        "id": 11,
        "avatar": "AMT",
        "framework": "Objection Quote Voice",
        "hook": "\"I've trained for months. I know this distance. Why do I keep making the same decision?\" This is why...",
        "text": "\"I've done the training. I've run this distance before. Why do I keep quitting at the same point?\" This is why. The breakdown isn't physical. It's a pattern — a predictable response that fires at the same cognitive state: sleep deprivation, isolation, accumulated fatigue. And patterns can be trained. In the free mental strength training for ultrarunners, I break down exactly how. Want it? Comment \"TOUGH\" and I'll send it."
    },
    {
        "id": 12,
        "avatar": "AMT",
        "framework": "Can't X Your Way Out",
        "hook": "You can't run your way out of a decision problem.",
        "text": "You can't run your way out of a decision problem. More mileage, more grit, more 'embrace the suck' — none of it changes what happens when you're 80km in, sleep-deprived, and your brain starts filing the wrong report. The DNF wasn't about fitness. It was about not having pre-decided rules for that specific moment. That's what the free mental strength training for ultrarunners gives you. Want it? Comment \"TOUGH\" and I'll send it."
    }
]


class ReelsGenerator:
    def __init__(self):
        self.output_dir = "instagram_reels"
        os.makedirs(self.output_dir, exist_ok=True)

    def create_video_with_text(self, text, output_path):
        """Create a 9-second vertical video with text overlay"""
        try:
            if not os.path.exists(CANVA_IMAGE_PATH):
                print(f"Error: Canva template not found at {CANVA_IMAGE_PATH}")
                return False

            # Base image clip
            base_clip = ImageClip(CANVA_IMAGE_PATH).set_duration(DURATION)
            base_clip = base_clip.resize((VIDEO_WIDTH, VIDEO_HEIGHT))

            # Text clip with word wrapping
            txt_clip = TextClip(
                text,
                fontsize=40,
                color='white',
                font='Arial-Bold',
                method='caption',
                size=(VIDEO_WIDTH - 100, None),
                align='center'
            ).set_duration(DURATION)

            txt_clip = txt_clip.set_position('center')
            final_clip = CompositeVideoClip([base_clip, txt_clip])

            final_clip.write_videofile(
                output_path,
                fps=FPS,
                codec='libx264',
                audio=False,
                verbose=False,
                logger=None
            )

            file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"✓ Created: {output_path} ({file_size_mb:.1f} MB)")
            return True

        except Exception as e:
            print(f"✗ Error creating video: {e}")
            return False

    def generate_all_reels(self):
        """Generate all reels from the spreadsheet data"""
        print("=" * 70)
        print("Instagram Reels Generator")
        print("=" * 70)
        print()

        if not os.path.exists(CANVA_IMAGE_PATH):
            print("⚠️  ERROR: Canva template not found!")
            print(f"Please export your Canva design as PNG and save as: {CANVA_IMAGE_PATH}")
            print()
            print("Spreadsheet data is ready. Once you provide the PNG template, run this script again.")
            return

        print(f"Found {len(REEL_DATA)} reels to create\n")

        created = 0
        for reel in REEL_DATA:
            print(f"[{reel['id']}] {reel['framework']}")
            print(f"    Hook: {reel['hook'][:50]}...")

            video_filename = f"reel_{reel['id']:03d}.mp4"
            video_path = os.path.join(self.output_dir, video_filename)

            if self.create_video_with_text(reel['text'], video_path):
                created += 1
            print()

        print("=" * 70)
        print(f"✓ Successfully created {created}/{len(REEL_DATA)} reels")
        print(f"📁 Videos saved to: {self.output_dir}/")
        print("=" * 70)


def main():
    generator = ReelsGenerator()
    generator.generate_all_reels()


if __name__ == "__main__":
    main()
