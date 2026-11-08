"""Não publicar artefatos que contenham apenas outro formato de saída."""
from pathlib import Path
import zipfile
from lxml import etree as ET
root=Path(__file__).resolve().parents[1]
for folder,name in [(root,'Dissertacao_Congonhas'),(root/'artigo','Artigo_CMAS_Congonhas')]:
    html=folder/'_book/html/index.html';word=folder/f'_book/word/{name}.docx'
    assert html.is_file() and html.stat().st_size>1000,html
    assert '<html' in html.read_text(encoding='utf8'),html
    with zipfile.ZipFile(word) as f:
        body=ET.fromstring(f.read('word/document.xml'))
        if folder.name=='artigo':assert body.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}lnNumType'),'Artigo sem numeração de linhas'
    print(name+': HTML e Word presentes e verificados')
