"""Ajustes editoriais portáveis; não altera o texto nem rasteriza figuras."""
import sys,zipfile,tempfile,os,re
from pathlib import Path
from lxml import etree as ET

W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
ET.register_namespace('w',W)
def q(s):return '{'+W+'}'+s
def child(parent,name):
    node=parent.find(q(name))
    if node is None:
        node=ET.Element(q(name))
        if name in {'pPr','rPr','tblPr','tcPr','trPr'}:parent.insert(0,node)
        else:parent.append(node)
    return node

def run(path):
    path=Path(path)
    with zipfile.ZipFile(path) as archive:files={n:archive.read(n) for n in archive.namelist()}
    root=ET.fromstring(files['word/document.xml'])
    # Cabeçalhos das tabelas repetidos; dimensões preservadas no modelo.
    for table in root.iter(q('tbl')):
        rows=table.findall(q('tr'))
        if rows:child(child(rows[0],'trPr'),'tblHeader')
        for row_index,row in enumerate(rows):
            child(child(row,'trPr'),'cantSplit')
            if len(rows)<=12 and row_index<len(rows)-1:
                for paragraph in row.iter(q('p')):
                    pr=child(paragraph,'pPr');keep=child(pr,'keepNext');pr.remove(keep);pr.insert(1 if pr.find(q('pStyle')) is not None else 0,keep)
        for paragraph in table.iter(q('p')):
            pr=child(paragraph,'pPr');child(pr,'jc').set(q('val'),'left')
            spacing=child(pr,'spacing');spacing.set(q('line'),'240');spacing.set(q('lineRule'),'auto');spacing.set(q('before'),'0');spacing.set(q('after'),'60')
        for r in table.iter(q('r')):
            pr=child(r,'rPr');child(pr,'sz').set(q('val'),'20')
        if rows:
            for r in rows[0].iter(q('r')):child(child(r,'rPr'),'b')
        grid=table.find(q('tblGrid'))
        if grid is not None and len(grid)==6:
            widths=[1361,1451,1814,1542,1179,1724]
            for col,width in zip(grid,widths):col.set(q('w'),str(width))
            for row in rows:
                cells=row.findall(q('tc'))
                if len(cells)==6:
                    for cell,width in zip(cells,widths):
                        size=child(child(cell,'tcPr'),'tcW');size.set(q('w'),str(width));size.set(q('type'),'dxa')
    for p in root.iter(q('p')):
        pr=p.find(q('pPr'));style=pr.find(q('pStyle')) if pr is not None else None
        if style is not None and style.get(q('val'),'').startswith('Heading'):
            child(pr,'keepNext')
        label=''.join(p.itertext())
        if re.match(r'^(?:Tabela|Quadro|Figura|Table|Figure)\s+\d+\b',label):
            pr=child(p,'pPr');keep=child(pr,'keepNext');pr.remove(keep);pr.insert(1 if pr.find(q('pStyle')) is not None else 0,keep)
    if '--artigo' in sys.argv:
        # Ordem de autoria usual no manuscrito: título, autores e afiliações.
        body=root.find(q('body'))
        def style_of(p):
            pr=p.find(q('pPr'));st=pr.find(q('pStyle')) if pr is not None else None
            return st.get(q('val')) if st is not None else ''
        top=list(body)[:10]
        subtitle=next((p for p in top if style_of(p)=='Subtitle'),None)
        author=next((p for p in top if style_of(p)=='Author'),None)
        if subtitle is not None and author is not None:
            body.remove(subtitle);body.insert(body.index(author)+1,subtitle)
        for sec in root.iter(q('sectPr')):
            old=sec.find(q('lnNumType'))
            if old is not None:sec.remove(old)
            line=ET.Element(q('lnNumType'))
            for key,value in [('countBy','1'),('start','1'),('restart','continuous'),('distance','150')]:line.set(q(key),value)
            following=next((n for n in sec if n.tag in [q('pgNumType'),q('cols'),q('formProt'),q('vAlign')]),None)
            if following is not None:sec.insert(sec.index(following),line)
            else:sec.append(line)
    files['word/document.xml']=ET.tostring(root,encoding='utf-8',xml_declaration=True)
    settings=ET.fromstring(files['word/settings.xml']);child(settings,'updateFields').set(q('val'),'true')
    files['word/settings.xml']=ET.tostring(settings,encoding='utf-8',xml_declaration=True)
    fd,tmp=tempfile.mkstemp(suffix='.docx',dir=path.parent);os.close(fd)
    try:
        with zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED) as archive:
            for name,data in files.items():archive.writestr(name,data)
        os.replace(tmp,path)
    finally:
        if Path(tmp).exists():Path(tmp).unlink()
    print('Word preparado:',path)

if __name__=='__main__':run(sys.argv[1])

