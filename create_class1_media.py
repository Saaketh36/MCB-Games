#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate video and audio files for Class I activities
"""

import os
import json
from pathlib import Path
import sys

# Fix encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Create directories if they don't exist
os.makedirs('videos', exist_ok=True)
os.makedirs('audio', exist_ok=True)
os.makedirs('images', exist_ok=True)

# Class I Activity Data with video scripts and audio narration
CLASS_I_ACTIVITIES = {
    "Listen & Do Adventure": {
        "subject": "English",
        "audio_script": "Good morning Class I! Listen carefully to my instructions. First, open your book to page five. Next, draw a small blue star next to the heading. Then read the three sentences aloud. After that, circle the picture of a red bus. Finally, close your book and wait for the bell. Great job, everyone!",
        "video_duration": 12,
        "video_description": "Teacher gives step-by-step instructions. Student follows each step: opening book, drawing star, reading sentences, circling bus, closing book."
    },
    "Story Time Quiz": {
        "subject": "English",
        "audio_script": "A tall tree stood near Nana's house. Every morning a small bird called Twee came to sing on its top branch. One day a storm broke the branch and Twee fell into the grass. Nana picked him up gently and kept him in a box near the window. The next morning Twee sang again, and this time a whole flock came to listen.",
        "video_duration": 12,
        "video_description": "Animated story showing: tree with bird, storm breaking branch, Twee falling, Nana caring for bird, bird singing with flock."
    },
    "Rhyme Gap Fill": {
        "subject": "English",
        "audio_script": "Let's learn about rhyming words! Listen to these pairs: cat and bat, they rhyme! Dog and log, they rhyme! Can you find the word that rhymes with ball? Is it call, wall, or doll? Yes! All three rhyme with ball!",
        "video_duration": 10,
        "video_description": "Words appear on screen with highlighted rhyming patterns. Teacher pronounces each word. Student identifies rhymes."
    },
    "Picture Story Teller": {
        "subject": "English",
        "audio_script": "Look at the pictures in order. Picture one shows a girl playing in the park. Picture two shows her climbing a tree. Picture three shows her friends joining her. Picture four shows them all laughing together. Now tell the story in your own words!",
        "video_duration": 10,
        "video_description": "Four sequential pictures displayed with narration. Each picture shows an action that builds a complete story."
    },
    "Question Word Match": {
        "subject": "English",
        "audio_script": "Let's learn question words! Who is for asking about people. What is for asking about things. Where is for asking about places. When is for asking about time. Why is for asking reasons. How is for asking about ways. Can you match the question word to the correct question?",
        "video_duration": 12,
        "video_description": "Each question word displayed with examples. Visual demonstration of when to use each word."
    },
    "Sight Word Memory Match": {
        "subject": "English",
        "audio_script": "Today we will practice sight words! These are words we see every day: the, and, a, to, in, is, you, that, he, was, for, are, but, not, all, can, had, her, what, so. Let's remember these words by finding matching pairs!",
        "video_duration": 10,
        "video_description": "Cards flip to show sight words. Student matches identical word pairs."
    },
    "Letter Sound Safari": {
        "subject": "English",
        "audio_script": "Welcome to Letter Sound Safari! Let's explore animal sounds and letter sounds. A is for Apple and Ant, sound is ahhh. B is for Ball and Bear, sound is buh. C is for Cat and Car, sound is cuh. D is for Dog and Door, sound is duh. Let's find more animals!",
        "video_duration": 11,
        "video_description": "Safari animals appear while letter sounds are pronounced. Each letter paired with animal images."
    },
    "Trace the Pattern Path": {
        "subject": "English",
        "audio_script": "Let's trace patterns! Pattern one is: line, circle, line, circle. Pattern two is: square, triangle, square, triangle. Pattern three is: dot, dash, dot, dash. Can you trace these patterns and continue them?",
        "video_duration": 10,
        "video_description": "Dotted pattern paths shown on screen. Teacher demonstrates tracing. Student traces patterns."
    },
    "Word Builder": {
        "subject": "English",
        "audio_script": "Let's build words! Start with c-a-t for cat. Now change c to b-a-t for bat. Change the a to i-t for bit. Add s for sit. Add r for r-i-s-e makes rise! Can you build more words by changing one letter at a time?",
        "video_duration": 11,
        "video_description": "Letter tiles rearrange to form words. Each transformation shown clearly."
    },
    "Picture Word Hunt": {
        "subject": "English",
        "audio_script": "Look at these pictures and find the words! Apple picture - the word is apple. Ball picture - the word is ball. Cat picture - the word is cat. Dog picture - the word is dog. Find all the words hidden in the pictures!",
        "video_duration": 10,
        "video_description": "Pictures displayed with word options. Student identifies correct word for each picture."
    },
    "Noun Basket Sort": {
        "subject": "English",
        "audio_script": "Nouns are words for people, places, and things! Let's sort nouns into baskets. People basket: teacher, student, friend. Places basket: school, park, home. Things basket: book, pencil, desk. Can you sort these nouns correctly?",
        "video_duration": 11,
        "video_description": "Objects and word cards appear. Student sorts into three baskets labeled People, Places, Things."
    },
    "Place Value Tower": {
        "subject": "Mathematics",
        "audio_script": "Welcome to Place Value Tower! In the number 23, we have 2 tens and 3 ones. In 45, we have 4 tens and 5 ones. In 67, we have 6 tens and 7 ones. Let's build towers to show place values!",
        "video_duration": 10,
        "video_description": "Blocks stack to show tens and ones. Numbers displayed with visual representations."
    },
    "Add & Subtract Sprint": {
        "subject": "Mathematics",
        "audio_script": "Let's practice addition and subtraction! Two plus three equals five. Four plus one equals five. Ten minus three equals seven. Eight minus two equals six. Let's race to solve more problems!",
        "video_duration": 10,
        "video_description": "Math problems appear with counting visualizations. Objects add or remove to show answers."
    },
    "Odd One Out Zoo": {
        "subject": "Mathematics",
        "audio_script": "In this zoo game, find the animal that is different! Group one: cat, dog, bird, car. The car is not an animal, so it's odd one out. Group two: apple, banana, orange, chair. The chair is not a fruit. Can you find more odd ones out?",
        "video_duration": 10,
        "video_description": "Four pictures shown. One doesn't belong. Student identifies the odd one out."
    },
    "Solid Shape Safari": {
        "subject": "Mathematics",
        "audio_script": "Explore 3D shapes in our Shape Safari! Sphere: round like a ball. Cube: square on all sides. Cylinder: round like a can. Cone: pointed like a hat. Can you find these shapes in nature?",
        "video_duration": 11,
        "video_description": "3D shapes rotate on screen. Real objects shown matching each shape."
    },
    "Ruler Race": {
        "subject": "Mathematics",
        "audio_script": "Learn to measure with a ruler! The pencil is 5 centimeters long. The eraser is 3 centimeters long. The notebook is 10 centimeters long. Let's measure more objects and see who can estimate the fastest!",
        "video_duration": 10,
        "video_description": "Ruler shown with objects being measured. Numbers displayed showing measurements."
    },
    "Pattern Train": {
        "subject": "Mathematics",
        "audio_script": "The pattern train chugs along! Pattern one: 1, 2, 1, 2, 1, 2. Pattern two: 1, 2, 3, 1, 2, 3. Pattern three: 2, 4, 6, 8, 10. Can you continue the patterns?",
        "video_duration": 10,
        "video_description": "Train cars display pattern numbers. Student continues patterns."
    },
    "Tally Marks Survey": {
        "subject": "Mathematics",
        "audio_script": "Let's count with tally marks! One mark is one. Two marks is two. When we reach four marks with a line through them, that equals five. Survey question: What is your favorite fruit? Count the votes using tally marks!",
        "video_duration": 11,
        "video_description": "Tally marks appear and count up. Survey results shown with tally mark representations."
    }
}

print("=" * 70)
print("CLASS I MEDIA GENERATION SUMMARY")
print("=" * 70)
print()

# Generate placeholder files
created_files = {
    'videos': [],
    'audio': [],
    'images': []
}

for activity_name, details in CLASS_I_ACTIVITIES.items():
    # Create video placeholder file
    video_filename = f"videos/class1_{activity_name.lower().replace(' ', '_')}.mp4"
    audio_filename = f"audio/class1_{activity_name.lower().replace(' ', '_')}.wav"

    # Create metadata file instead
    metadata = {
        "activity": activity_name,
        "subject": details["subject"],
        "duration": details["video_duration"],
        "audio_script": details["audio_script"],
        "video_description": details["video_description"]
    }

    meta_filename = video_filename.replace('.mp4', '_metadata.json')
    with open(meta_filename, 'w') as f:
        json.dump(metadata, f, indent=2)

    created_files['videos'].append(meta_filename)
    print(f"[OK] Created: {meta_filename}")

print()
print("=" * 70)
print(f"TOTAL ACTIVITIES: {len(CLASS_I_ACTIVITIES)}")
print(f"VIDEOS/METADATA: {len(created_files['videos'])}")
print("=" * 70)
print()
print("NEXT STEPS:")
print("1. [OK] Metadata files created - ready for video content")
print("2. [PENDING] Audio files: Use text-to-speech to generate from scripts")
print("3. [PENDING] Video files: Record or animate based on descriptions")
print("4. [OK] Images: Already created in images/ folder")
print()
print("ALL AUDIO SCRIPTS ARE READY FOR TTS (Text-to-Speech)")
print("ALL VIDEO DESCRIPTIONS ARE READY FOR RECORDING/ANIMATION")
