"""Ajustes editoriais portáveis; não altera o texto nem rasteriza figuras."""
import sys,zipfile,tempfile,os
from pathlib import Path
from lxml import etree as ET

W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
ET.register_namespace('w',W)
def q(s):return '{'+W+'}'+s
def child(parent,name):
    node=parent.find(q(name))
    if node is None:node=ET.SubElement(parent,q(name))
    return node

def run(path):
    path=Path(path)
    with zipfile.ZipFile(path) as archive:files={n:archive.read(n) for n in archive.namelist()}
    root=ET.fromstring(files['word/document.xml'])
    # Cabeçalhos das tabelas repetidos; dimensões preservadas no modelo.
    for table in root.iter(q('tbl')):
        rows=table.findall(q('tr'))
        if rows:child(child(rows[0],'trPr'),'tblHeader')
        for r in table.iter(q('r')):
            pr=child(r,'rPr');child(pr,'sz').set(q('val'),'20')
    for p in root.iter(q('p')):
        pr=p.find(q('pPr'));style=pr.find(q('pStyle')) if pr is not None else None
        if style is not None and style.get(q('val'),'').startswith('Heading'):
            child(pr,'keepNext')
    if '--artigo' in sys.argv:
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

