import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

with open('js/class2_games.js', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'runWordTrain\(', text)
if m:
    pos = m.start()
    print(text[pos:pos+2000])
