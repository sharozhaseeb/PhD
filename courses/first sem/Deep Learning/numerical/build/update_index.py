"""Refresh the student index using explicit final TA verdicts, never file existence alone."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
roadmap = ROOT.parent / 'Visual worked examples - roadmap.md'
source = roadmap.read_text(encoding='utf-8')
topics = re.findall(r'- \[([ x])\] \*\*(\d+)\. (.*?):\*\*', source)
rows = []
completed = []
for _, number, title in topics:
    number = int(number)
    key = 4 if number == 5 else number
    folders = sorted(p for p in ROOT.glob(f'{key:02d}-*') if p.is_dir())
    reviews = list((ROOT / 'reviews').glob(f'{key:02d}*'))
    passed = any(re.search(r'Final.*(?:PASS|Pass)', p.read_text(encoding='utf-8')) for p in reviews)
    if folders and passed and (folders[0] / 'lesson.pdf').exists():
        folder = folders[0].name
        status = f'Complete — [Illustrated lesson]({folder}/README.md) · [PDF]({folder}/lesson.pdf)'
        completed.append(number)
    elif folders and (folders[0] / 'lesson.pdf').exists():
        status = 'Created; TA review/fixes in progress'
    elif reviews:
        status = 'Planning / TA discussion'
    else:
        status = 'Planned'
    rows.append(f'| {number} | {title} | {status} |')
text = '''# Deep Learning numerical lessons

Step-by-step visual examples matched to the course notes. Each lesson follows **plan → TA discussion → PDF and images → TA review → fixes → final pass** before the next lesson is created.

[Topic roadmap](../Visual%20worked%20examples%20-%20roadmap.md) · [Numerical practice](../numerical-practice.md) · [Course support](../support.md)

## Lessons and progress

'''
text += f'**{len(completed)} of {len(topics)} roadmap items complete.** Items 4 and 5 share the expanded logistic-regression lesson.\n\n'
text += '| Item | Topic | Status / lesson |\n| --- | --- | --- |\n' + '\n'.join(rows)
text += '''

## Reading and checking a lesson

Open the illustrated lesson in Obsidian, or its PDF to read and print. Read the practice question before looking at its worked answer. Lecture references count PDF pages including title slides. Examples are study exercises, not predictions of exam questions.

TA plan discussions and final reviews are in `reviews`. Reproducible sources and checks are kept with each lesson or in `build`.
'''
(ROOT / 'README.md').write_text(text, encoding='utf-8')
for number in completed:
    source = source.replace(f'- [ ] **{number}.', f'- [x] **{number}.')
roadmap.write_text(source, encoding='utf-8')
print(f'Index refreshed: {len(completed)}/{len(topics)} roadmap items passed')
