import sys
sys.path.append('.')

try:
    import curriculum_reading_passages
    print("Passages in curriculum_reading_passages:", dir(curriculum_reading_passages))
    if hasattr(curriculum_reading_passages, 'READING_PASSAGES'):
        print("READING_PASSAGES count:", len(curriculum_reading_passages.READING_PASSAGES))
        for k in list(curriculum_reading_passages.READING_PASSAGES.keys())[:5]:
            print(" ", k)
except Exception as e:
    print("Error:", e)
