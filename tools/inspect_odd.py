import json
import re

s = open('question_bank.js', encoding='utf-8').read()
keys = re.findall(r'"([^"]*Odd One Out[^"]*)":\s*\{', s)
print('Odd One Out activities in bank:')
for k in keys:
    print('  -', k)

data = json.loads(s[s.index('{'):s.rindex('}') + 1])
for k in keys:
    e = data[k]
    print()
    print('===', k)
    print('   game questions:', len(e.get('questions', [])))
    for q in e.get('questions', []):
        print('   Q:', q['question'])
        print('     options:', q['options'])
        print('     answer  :', q['answer'])
        print('     image   :', repr(q.get('image', '')))