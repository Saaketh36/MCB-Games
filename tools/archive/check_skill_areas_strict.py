import json

cat = json.load(open('full_games_catalog.json', encoding='utf-8'))
skills = json.load(open('skill_areas_data.json', encoding='utf-8'))

print("Catalog count:", len(cat))
print("Skills count:", len(skills))

# Check unique skill areas in skills
sa_set = set(s['skillArea'] for s in skills if s.get('skillArea'))
print("\nUnique skill areas in skill_areas_data.json:")
for sa in sorted(sa_set):
    print(" -", sa)

# Compare with catalog
cat_sa_set = set(c['skillArea'] for c in cat if c.get('skillArea'))
diff = cat_sa_set - sa_set
print("\nIn catalog but not in skills:", diff)
