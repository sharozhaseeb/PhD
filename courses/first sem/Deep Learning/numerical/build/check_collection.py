"""Check the delivered PDFs, page images, local links, and review coverage."""
from pathlib import Path
from urllib.parse import unquote
import json
import re
from pypdf import PdfReader

root = Path(__file__).resolve().parents[1]
results = []
errors = []
for folder in sorted(root.glob('[0-9][0-9]-*')):
    pdf = folder / 'lesson.pdf'
    if not pdf.exists():
        continue
    count = len(PdfReader(pdf).pages)
    images = sorted((folder / 'pages').glob('page-*.png'))
    if len(images) != count:
        errors.append(f'{folder.name}: {count} PDF pages but {len(images)} images')
    note = folder / 'README.md'
    if not note.exists():
        errors.append(f'{folder.name}: missing illustrated note')
    else:
        text = note.read_text(encoding='utf-8')
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if target.startswith(('http:', 'https:', '#')):
                continue
            path = unquote(target.split('#')[0])
            if not (folder / path).resolve().exists():
                errors.append(f'{folder.name}: broken link {target}')
        if len(re.findall(r'!\[.*?\]\(pages/', text)) != count:
            errors.append(f'{folder.name}: embedded image count differs from PDF')
    reviews = list((root / 'reviews').glob(folder.name[:2] + '*'))
    passed = any(re.search(r'Final.*(?:PASS|Pass)', f.read_text(encoding='utf-8')) for f in reviews)
    results.append({'lesson': folder.name, 'pages': count, 'final_ta_pass': passed})
report = {'lessons': results, 'total_pages': sum(x['pages'] for x in results), 'errors': errors}
(root / 'collection-check.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
if errors:
    raise SystemExit(1)
