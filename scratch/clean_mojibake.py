with open('skill_areas_data.json', 'r', encoding='utf-8', errors='replace') as f:
    text = f.read()

cleaned = text.replace('\u00e2\u20ac\u201c', '–').replace('â€“', '–').replace('\u00e2\u20ac\u2122', "'").replace('â€™', "'")
with open('skill_areas_data.json', 'w', encoding='utf-8') as f:
    f.write(cleaned)

print("Cleaned skill_areas_data.json mojibake successfully.")
