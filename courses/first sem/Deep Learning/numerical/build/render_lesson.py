"""Render one reviewed lesson specification into PDF, PNG pages and Obsidian note.

Usage: python render_lesson.py ../01-single-feature-linear-regression/lesson.json
Requires reportlab, matplotlib, Pillow and Poppler. No network resources.
"""
from pathlib import Path
from io import BytesIO
import json, sys, subprocess, textwrap
import matplotlib
matplotlib.use('Agg')
from matplotlib.mathtext import math_to_image
from matplotlib.font_manager import FontProperties
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader

W,H=800,600
INK='#172B43';TEAL='#006E73';MUTED='#526477'
def render(spec_path):
    spec_path=Path(spec_path); spec=json.loads(spec_path.read_text(encoding='utf-8'))
    out=spec_path.parent; pdf=out/'lesson.pdf'; pages=out/'pages';pages.mkdir(exist_ok=True)
    c=canvas.Canvas(str(pdf),pagesize=(W,H));c.setTitle(spec['title']);c.setAuthor('Course study support')
    def txt(s,x,y,size=16,bold=False,color=INK):
        font='Helvetica-Bold' if bold else 'Helvetica';c.setFont(font,size);c.setFillColor(HexColor(color))
        assert c.stringWidth(s,font,size)<=W-x-40,(s,'too wide')
        c.drawString(x,H-y,s)
    def para(s,y,size=16,bold=False,color=INK):
        font='Helvetica-Bold' if bold else 'Helvetica';words=s.split();line=''
        for word in words:
            if c.stringWidth((line+' '+word).strip(),font,size)>704:
                txt(line,48,y,size,bold,color);y+=23;line=word
            else:line=(line+' '+word).strip()
        if line:txt(line,48,y,size,bold,color);y+=23
        return y
    for n,page in enumerate(spec['pages'],1):
        c.setFillColor(HexColor('#FAFCFD'));c.rect(0,0,W,H,fill=1,stroke=0)
        txt(f"DEEP LEARNING / NUMERICAL {spec['number']:02d}",48,34,11,True,TEAL)
        txt(page.get('stage','WORKED EXAMPLE').upper(),48,66,12,True,TEAL)
        txt(page['title'],48,107,27,True)
        y=para(page.get('subtitle',''),138,14,color=MUTED)
        c.setStrokeColor(HexColor('#D7E3E9'));c.line(48,H-169,752,H-169)
        y=196
        for block in page['blocks']:
            if isinstance(block,str):y=para(block,y)+7
            elif 'eq' in block:
                size=block.get('size',23);buf=BytesIO()
                math_to_image('$'+block['eq']+'$',buf,dpi=210,format='png',color=INK,prop=FontProperties(size=size))
                buf.seek(0);im=Image.open(buf);ww,hh=(v*72/210 for v in im.size)
                assert ww<=704,(page['title'],block['eq'],ww)
                c.drawImage(ImageReader(im),48,H-y-hh,width=ww,height=hh,mask='auto');y+=hh+19
            elif 'heading' in block:y=para(block['heading'],y,bold=True,color=TEAL)+4
            elif 'image' in block:
                im=Image.open(out/block['image']);ww=block.get('width',650);hh=ww*im.height/im.width
                c.drawImage(ImageReader(im),48,H-y-hh,width=ww,height=hh,mask='auto');y+=hh+14
            elif 'table' in block:
                data=block['table'];widths=block.get('widths',[704/len(data[0])]*len(data[0]));rh=block.get('row_height',27)
                for ri,row in enumerate(data):
                    xx=48
                    if ri==0:c.setFillColor(HexColor('#EAF3F7'));c.rect(xx,H-y-rh,sum(widths),rh,fill=1,stroke=0)
                    for item,ww in zip(row,widths):
                        txt(str(item),xx+6,y+18,block.get('size',14),ri==0,TEAL if ri==0 else INK);xx+=ww
                    y+=rh
                y+=17
            elif 'gap' in block:y+=block['gap']
        assert y<=545,(page['title'],'page overflow',y)
        txt(spec['source_short'],48,573,10,color=MUTED)
        txt(f'{n} / {len(spec["pages"])}',708,573,11,True,TEAL)
        c.showPage()
    c.save()
    poppler=Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftoppm.exe'
    result=subprocess.run([str(poppler),'-r','120','-png',str(pdf),str(pages/'page')],capture_output=True,text=True)
    if result.returncode:raise RuntimeError(result.stderr)
    for p in pages.glob('page-*.png'):
        dst=pages/f'page-{int(p.stem.split("-")[-1]):02d}.png'
        if p!=dst:p.replace(dst)
    md=[f'# {spec["number"]:02d}. {spec["title"]}', '',spec['description'],'', '[Open the PDF](lesson.pdf)','',f'Lecture reference: {spec["source"]}', '', '## Illustrated walkthrough','']
    for n,p in enumerate(spec['pages'],1):md += [f'### {n}. {p["title"]}','',f'![{p["title"]}](pages/page-{n:02d}.png)','']
    md += ['Original study example. Read the practice question before revealing the following answer pages.','', '[Back to numerical index](../README.md)','']
    (out/'README.md').write_text('\n'.join(md),encoding='utf-8')
    print(json.dumps({'pdf':str(pdf),'pages':len(spec['pages']),'status':'awaiting TA visual review'}))
if __name__=='__main__':render(sys.argv[1])
