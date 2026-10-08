"""Build the downloadable teaching handbook from the blog's single Markdown source.
Requires ReportLab, Pillow and pypdf; CJK fonts are resolved from Windows by default.
"""
from pathlib import Path
import html
import re
import shutil
import os
from urllib.parse import urljoin
from PIL import Image as PILImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'src/content/blog/mixed-vr-iqa-mini-encyclopedia.md'
OUT=ROOT/'output/pdf/mixed-vr-iqa-mini-encyclopedia.pdf'
OUT.parent.mkdir(parents=True,exist_ok=True)
SITE='https://shawreal2004.github.io/blog/mixed-vr-iqa-mini-encyclopedia/'
pdfmetrics.registerFont(TTFont('BodyCJK',os.environ.get('PDF_CJK_FONT','C:/Windows/Fonts/simsun.ttc'),subfontIndex=0))
pdfmetrics.registerFont(TTFont('BoldCJK',os.environ.get('PDF_CJK_BOLD_FONT','C:/Windows/Fonts/simhei.ttf')))
pdfmetrics.registerFontFamily('BodyCJK',normal='BodyCJK',bold='BoldCJK',italic='BodyCJK',boldItalic='BoldCJK')
BLACK=colors.black
MUTED=colors.HexColor('#58615a')
WIDTH=A4[0]-96
styles={
    'title':ParagraphStyle('title',fontName='BoldCJK',fontSize=24,leading=33,textColor=BLACK,spaceAfter=12,wordWrap='CJK'),
    'body':ParagraphStyle('body',fontName='BodyCJK',fontSize=10.5,leading=17,textColor=BLACK,spaceAfter=8,wordWrap='CJK',allowWidows=0,allowOrphans=0),
    'meta':ParagraphStyle('meta',fontName='BodyCJK',fontSize=9,leading=15,textColor=MUTED,spaceAfter=12,wordWrap='CJK'),
    'h2':ParagraphStyle('h2',fontName='BoldCJK',fontSize=14,leading=21,textColor=BLACK,spaceBefore=15,spaceAfter=8,keepWithNext=True,wordWrap='CJK'),
    'h3':ParagraphStyle('h3',fontName='BoldCJK',fontSize=11.5,leading=18,textColor=BLACK,spaceBefore=8,spaceAfter=4,keepWithNext=True,wordWrap='CJK'),
    'caption':ParagraphStyle('caption',fontName='BodyCJK',fontSize=9,leading=14.5,textColor=MUTED,spaceAfter=10,wordWrap='CJK'),
    'cell':ParagraphStyle('cell',fontName='BodyCJK',fontSize=9.2,leading=14.5,textColor=BLACK,wordWrap='CJK'),
    'th':ParagraphStyle('th',fontName='BoldCJK',fontSize=9.2,leading=14.5,textColor=BLACK,wordWrap='CJK'),
}

def inline(text):
    text=html.escape(text)
    def link(m):
        url=urljoin(SITE,html.unescape(m.group(2)))
        return f'<link href="{html.escape(url,quote=True)}" color="#365e48"><u>{m.group(1)}</u></link>'
    text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,text)
    text=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',text)
    text=re.sub(r'`([^`]+)`',r'\1',text)
    return text

class Handbook(SimpleDocTemplate):
    def afterFlowable(self,flowable):
        if isinstance(flowable,Paragraph) and flowable.style.name in ['h2','h3']:
            text=flowable.getPlainText()
            key=flowable.style.name+'-'+re.sub(r'[^a-zA-Z0-9]','',text.split(' ')[0])
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text,key,level=0 if flowable.style.name=='h2' else 1,closed=True)

def page_frame(canvas,doc):
    canvas.saveState()
    canvas.setFont('BodyCJK',8)
    canvas.setFillColor(MUTED)
    if doc.page>1:
        canvas.drawString(48,A4[1]-30,'我的 VR 图像质量评价入门百科')
    canvas.setStrokeColor(colors.HexColor('#d9d9d9'))
    canvas.setLineWidth(.5)
    canvas.line(48,37,A4[0]-48,37)
    canvas.drawString(48,24,'shaw chenyu · 上海大学 · 2026.10.08')
    canvas.drawRightString(A4[0]-48,24,str(doc.page))
    canvas.restoreState()

raw=SOURCE.read_text(encoding='utf-8')
_,front,content=raw.split('---',2)
title=re.search(r'title: "(.+)"',front).group(1)
story=[Paragraph(title,styles['title']),Paragraph('shaw chenyu  上海大学  电子信息<br/>研究方向 AIGC 与 UGC 混合的 360° VR 图片数据库和算法<br/>整理日期 2026年10月8日',styles['meta'])]
lines=content.strip().splitlines()
i=0
figures=0
terms=0
while i<len(lines):
    line=lines[i].strip()
    if not line or line.startswith('作者：') or line.startswith('[下载图文手册 PDF]'):
        i+=1;continue
    if line.startswith('<figure'):
        chunk=[]
        while i<len(lines):
            chunk.append(lines[i]);i+=1
            if '</figure>' in chunk[-1]:break
        figure='\n'.join(chunk)
        image_src=re.search(r'<img src="([^"]+)"',figure).group(1)
        caption=re.search(r'<figcaption>(.*?)</figcaption>',figure,re.S).group(1)
        filename=ROOT/'public'/image_src.replace('../../','')
        with PILImage.open(filename) as image: w,h=image.size
        # Keep a figure together with its explanation; maximum height avoids empty pages.
        draw_width=WIDTH
        if h/w*draw_width>375: draw_width=375*w/h
        flow=[Spacer(1,5),Image(str(filename),width=draw_width,height=draw_width*h/w),Spacer(1,6),Paragraph(inline(caption),styles['caption'])]
        story.append(KeepTogether(flow));figures+=1;continue
    if line.startswith('|'):
        rows=[]
        while i<len(lines) and lines[i].strip().startswith('|'):
            cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r'[-: ]+',c) for c in cells):rows.append(cells)
            i+=1
        ratios=[.22,.19,.59] if 'PSNR' in str(rows) else [.17,.32,.51]
        data=[[Paragraph(inline(c),styles['th' if r==0 else 'cell']) for c in row] for r,row in enumerate(rows)]
        table=Table(data,colWidths=[WIDTH*v for v in ratios],repeatRows=1,hAlign='LEFT')
        table.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e7edf1')),
            ('GRID',(0,0),(-1,-1),.5,colors.HexColor('#d9d9d9')),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('ALIGN',(0,1),(1,-1),'CENTER'),
            ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
            ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ]))
        story.extend([table,Spacer(1,10)]);continue
    if line.startswith('## '):story.append(Paragraph(inline(line[3:]),styles['h2']))
    elif line.startswith('### '):
        story.append(Paragraph(inline(line[4:]),styles['h3']));terms+=1
    else:story.append(Paragraph(inline(line),styles['body']))
    i+=1

doc=Handbook(str(OUT),pagesize=A4,rightMargin=48,leftMargin=48,topMargin=47,bottomMargin=49,title=title,author='shaw chenyu',subject='混合来源360度全景图像质量评价入门概念手册')
doc.build(story,onFirstPage=page_frame,onLaterPages=page_frame)
reader=PdfReader(OUT)
assert figures==9 and terms>=60
text='\n'.join(page.extract_text() or '' for page in reader.pages)
for term in ['像素','AIGC','UGC','模糊','噪声','伪影','MOS','ERP','LoRA','数据泄漏','5.5']:
    assert term in text,term
public=ROOT/'public/reports'/OUT.name
public.parent.mkdir(parents=True,exist_ok=True)
shutil.copyfile(OUT,public)
print(f'Created {len(reader.pages)} pages, {terms} grouped entries and {figures} figures. {OUT}')
