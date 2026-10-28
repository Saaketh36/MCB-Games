import sys
sys.path.append('.')
import listening_content

print("Stories in LISTENING_STORIES:", len(listening_content.LISTENING_STORIES))
for title, data in listening_content.LISTENING_STORIES.items():
    print(f"- {title}: has story={bool(data.get('story'))}, questions={len(data.get('questions', []))}")
