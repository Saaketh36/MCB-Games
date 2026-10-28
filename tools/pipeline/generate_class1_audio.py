#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate audio files for Class I using pyttsx3 (offline text-to-speech)
"""

import os
import json

try:
    import pyttsx3
    HAS_PYTTSX3 = True
except ImportError:
    HAS_PYTTSX3 = False
    print("[INFO] pyttsx3 not installed. Installing...")
    os.system('pip install pyttsx3')
    import pyttsx3

# Audio scripts for all Class I activities
AUDIO_SCRIPTS = {
    "class1_listen_&_do_adventure": "Good morning Class I! Listen carefully to my instructions. First, open your book to page five. Next, draw a small blue star next to the heading. Then read the three sentences aloud. After that, circle the picture of a red bus. Finally, close your book and wait for the bell. Great job, everyone!",

    "class1_story_time_quiz": "A tall tree stood near Nana's house. Every morning a small bird called Twee came to sing on its top branch. One day a storm broke the branch and Twee fell into the grass. Nana picked him up gently and kept him in a box near the window. The next morning Twee sang again, and this time a whole flock came to listen.",

    "class1_rhyme_gap_fill": "Let's learn about rhyming words! Listen to these pairs: cat and bat, they rhyme! Dog and log, they rhyme! Can you find the word that rhymes with ball? Is it call, wall, or doll? Yes! All three rhyme with ball!",

    "class1_picture_story_teller": "Look at the pictures in order. Picture one shows a girl playing in the park. Picture two shows her climbing a tree. Picture three shows her friends joining her. Picture four shows them all laughing together. Now tell the story in your own words!",

    "class1_question_word_match": "Let's learn question words! Who is for asking about people. What is for asking about things. Where is for asking about places. When is for asking about time. Why is for asking reasons. How is for asking about ways. Can you match the question word to the correct question?",

    "class1_sight_word_memory_match": "Today we will practice sight words! These are words we see every day: the, and, a, to, in, is, you, that, he, was, for, are, but, not, all, can, had, her, what, so. Let's remember these words by finding matching pairs!",

    "class1_letter_sound_safari": "Welcome to Letter Sound Safari! Let's explore animal sounds and letter sounds. A is for Apple and Ant, sound is ahhh. B is for Ball and Bear, sound is buh. C is for Cat and Car, sound is cuh. D is for Dog and Door, sound is duh. Let's find more animals!",

    "class1_trace_the_pattern_path": "Let's trace patterns! Pattern one is: line, circle, line, circle. Pattern two is: square, triangle, square, triangle. Pattern three is: dot, dash, dot, dash. Can you trace these patterns and continue them?",

    "class1_word_builder": "Let's build words! Start with c-a-t for cat. Now change c to b-a-t for bat. Change the a to i-t for bit. Add s for sit. Add r for r-i-s-e makes rise! Can you build more words by changing one letter at a time?",

    "class1_picture_word_hunt": "Look at these pictures and find the words! Apple picture - the word is apple. Ball picture - the word is ball. Cat picture - the word is cat. Dog picture - the word is dog. Find all the words hidden in the pictures!",

    "class1_noun_basket_sort": "Nouns are words for people, places, and things! Let's sort nouns into baskets. People basket: teacher, student, friend. Places basket: school, park, home. Things basket: book, pencil, desk. Can you sort these nouns correctly?",

    "class1_place_value_tower": "Welcome to Place Value Tower! In the number 23, we have 2 tens and 3 ones. In 45, we have 4 tens and 5 ones. In 67, we have 6 tens and 7 ones. Let's build towers to show place values!",

    "class1_add_&_subtract_sprint": "Let's practice addition and subtraction! Two plus three equals five. Four plus one equals five. Ten minus three equals seven. Eight minus two equals six. Let's race to solve more problems!",

    "class1_odd_one_out_zoo": "In this zoo game, find the animal that is different! Group one: cat, dog, bird, car. The car is not an animal, so it's odd one out. Group two: apple, banana, orange, chair. The chair is not a fruit. Can you find more odd ones out?",

    "class1_solid_shape_safari": "Explore 3D shapes in our Shape Safari! Sphere: round like a ball. Cube: square on all sides. Cylinder: round like a can. Cone: pointed like a hat. Can you find these shapes in nature?",

    "class1_ruler_race": "Learn to measure with a ruler! The pencil is 5 centimeters long. The eraser is 3 centimeters long. The notebook is 10 centimeters long. Let's measure more objects and see who can estimate the fastest!",

    "class1_pattern_train": "The pattern train chugs along! Pattern one: 1, 2, 1, 2, 1, 2. Pattern two: 1, 2, 3, 1, 2, 3. Pattern three: 2, 4, 6, 8, 10. Can you continue the patterns?",

    "class1_tally_marks_survey": "Let's count with tally marks! One mark is one. Two marks is two. When we reach four marks with a line through them, that equals five. Survey question: What is your favorite fruit? Count the votes using tally marks!"
}

print("[INFO] Generating audio files for Class I activities...")
print("[INFO] Using pyttsx3 (offline text-to-speech)")
print()

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 120)  # Speed
engine.setProperty('volume', 0.9)  # Volume

# Create audio directory if it doesn't exist
os.makedirs('audio', exist_ok=True)

generated_count = 0
for filename, script in AUDIO_SCRIPTS.items():
    audio_file = f'audio/{filename}.wav'

    try:
        engine.save_to_file(script, audio_file)
        engine.runAndWait()
        print(f"[OK] Generated: {audio_file}")
        generated_count += 1
    except Exception as e:
        print(f"[ERROR] Failed to generate {audio_file}: {str(e)}")

print()
print("=" * 70)
print(f"AUDIO FILES GENERATED: {generated_count}/18")
print("=" * 70)
print()
print("Audio files are ready!")
print("Location: audio/class1_*.wav")
