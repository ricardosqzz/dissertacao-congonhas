"""Reúne livro, artigo, visualizador e Word no diretório do GitHub Pages."""
from pathlib import Path
import shutil,json

ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/'_site_publico'

def run():
    TARGET.mkdir(exist_ok=True)
    for source,destination in [(ROOT/'_book/html',TARGET),(ROOT/'artigo/_book/html',TARGET/'artigo'),(ROOT/'_visualizador',TARGET/'visualizador')]:
        assert (source/'index.html').is_file(),source
        shutil.copytree(source,destination,dirs_exist_ok=True)
    downloads=TARGET/'downloads';downloads.mkdir(exist_ok=True)
    for source in [ROOT/'_book/word/Dissertacao_Congonhas.docx',ROOT/'artigo/_book/word/Artigo_CMAS_Congonhas.docx']:
        assert source.is_file(),source
        shutil.copy2(source,downloads/source.name)
    (TARGET/'.nojekyll').touch()
    catalog=json.loads((ROOT/'visualizador/catalogo.json').read_text(encoding='utf8'))
    for item in catalog['catalog']:assert (TARGET/'visualizador'/item['src']).is_file(),item['src']
    assert len(catalog['catalog'])==195
    print('Site preparado: dissertação, artigo, 195 figuras do visualizador e dois arquivos Word.')

if __name__=='__main__':run()
