import json
with open('full_games_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

for gid in ['VIII-ENG-01', 'I-ENG-01', 'I-ENG-02', 'IV-ENG-05', 'III-ENG-06', 'IV-MAT-02', 'III-EVS-08']:
    g = next((x for x in catalog if x.get('id') == gid), None)
    if g:
        print('='*50)
        print(f"{g.get('id')} - {g.get('title')} ({g.get('gameType')})")
        print('Has story:', bool(g.get('story')), 'Has audio_script:', bool(g.get('audio_script')), 'Has instructions:', bool(g.get('instructions')))
        if g.get('instructions'):
            print('Instructions:', g.get('instructions'))
        if g.get('audio_script'):
            print('Audio script:', g.get('audio_script')[:100] + '...')
        for q in g.get('questions', []):
            print(' Q:', q.get('prompt'))
            print('  Opts:', q.get('options'))
