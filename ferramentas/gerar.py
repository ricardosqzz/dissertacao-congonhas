"""Gera os quatro produtos sem sobrescrever o formato anterior."""
from pathlib import Path
import os,sys,shutil,subprocess
ROOT=Path(__file__).resolve().parents[1]
def run():
    quarto=os.environ.get('QUARTO_PATH') or shutil.which('quarto')
    if not quarto:
        candidate=ROOT.parent/'codigo/ferramentas/quarto-1.11.9/bin/quarto.exe'
        if candidate.exists():quarto=str(candidate)
    if not quarto:raise SystemExit('Instale o Quarto ou defina QUARTO_PATH para seu executável.')
    for folder,name,extra in [(ROOT,'Dissertacao_Congonhas',[]),(ROOT/'artigo','Artigo_CMAS_Congonhas',['--artigo'])]:
        for format,destination in [('html','_book/html'),('docx','_book/word')]:
            subprocess.run([quarto,'render','--to',format,'--output-dir',destination],cwd=folder,check=True)
        subprocess.run([sys.executable,str(ROOT/'ferramentas/ajustar_word.py'),str(folder/f'_book/word/{name}.docx'),*extra],check=True)
    subprocess.run([sys.executable,str(ROOT/'ferramentas/verificar_exportacoes.py')],check=True)
if __name__=='__main__':run()
