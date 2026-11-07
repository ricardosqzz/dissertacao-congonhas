"""Configura o endereço; não cria repositório nem faz upload."""
import re,sys,json,subprocess
from pathlib import Path
def run(url):
    url=url.rstrip('/').removesuffix('.git')
    if not re.fullmatch(r'https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',url):raise ValueError('Informe https://github.com/CONTA/REPOSITORIO')
    root=Path(__file__).resolve().parents[1];p=root/'_quarto.yml';s=p.read_text(encoding='utf8')
    s=re.sub(r'^  repo-(?:url|branch|actions):.*\n','',s,flags=re.M)
    s=s.replace('book:\n','book:\n  repo-url: '+json.dumps(url)+'\n  repo-branch: main\n  repo-actions: [edit, issue, source]\n',1)
    p.write_text(s,encoding='utf8')
    article=root/'artigo/_quarto.yml'
    if article.exists():
        a=article.read_text(encoding='utf8');a=re.sub(r'^  repo-(?:url|branch|actions|subdir):.*\n','',a,flags=re.M)
        a=a.replace('book:\n','book:\n  repo-url: '+json.dumps(url)+'\n  repo-branch: main\n  repo-subdir: artigo\n  repo-actions: [edit, issue, source]\n',1);article.write_text(a,encoding='utf8')
    if (root/'.git').exists():
        remotes=subprocess.check_output(['git','remote'],cwd=root,text=True).split()
        subprocess.run(['git','remote','set-url' if 'origin' in remotes else 'add','origin',url+'.git'],cwd=root,check=True)
    (root/'repositorio.json').write_text(json.dumps(dict(url=url,branch='main',visibility='private',local_mirror=True),indent=2),encoding='utf8')
    print('Origem e links de edição configurados:',url)
if __name__=='__main__':run(sys.argv[1])

