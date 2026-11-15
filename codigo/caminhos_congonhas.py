# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: Path(override).expanduser() if override else CONFIG_FILE | path.read_text.
# Campos/chaves em entry: chave, original.
# Saídas: retorno de funções, verificações ou arquivos definidos pelo chamador.
# CÓDIGO DO PROCESSAMENTO

from pathlib import Path
import json
import os
import re
import sys

PROJETO = "congonhas"
ENV_RAIZ = "CONGONHAS_PROJECT_ROOT"
BASE_CODIGO = Path(__file__).resolve().parent
CONFIG_FILE = BASE_CODIGO / 'caminhos_projeto.json'

# Configuração e raiz dos dados
def configuracao():
    override=os.environ.get(ENV_RAIZ+'_CONFIG','').strip()
    path=Path(override).expanduser() if override else CONFIG_FILE
    return json.loads(path.read_text('utf-8-sig')) if path.exists() else {}

def raiz_projeto():
    cfg=configuracao()
    explicit=os.environ.get(ENV_RAIZ,'').strip() or (os.environ.get('EMI_PROJECT_ROOT','').strip() if PROJETO=='congonhas' else '') or cfg.get('raiz_projeto','')
    if explicit:
        p=Path(explicit).expanduser()
        return p if p.is_absolute() else (BASE_CODIGO/p).resolve()
    if cfg.get('modo_entrega'):
        for p in BASE_CODIGO.parents:
            if (p/'01_entradas').is_dir() and (p/'02_saidas').is_dir():return p
    return BASE_CODIGO.parent

# Resolução de pastas e arquivos
def caminho(relativo=''):
    cfg=configuracao();root=raiz_projeto();rel=str(relativo).replace('\\','/').strip('/')
    mappings={**cfg.get('pastas',{}),**cfg.get('arquivos',{})}
    for key in sorted(mappings,key=len,reverse=True):
        normalized=key.replace('\\','/').strip('/')
        if rel==normalized or rel.startswith(normalized+'/'):
            base=Path(mappings[key]).expanduser();base=base if base.is_absolute() else root/base
            suffix=rel[len(normalized):].lstrip('/')
            return base/suffix if suffix else base
    return root/rel if rel else root

def texto_caminho(relativo='',estilo='posix'):
    p=caminho(relativo)
    return p.as_posix() if estilo=='posix' else str(p)

# Arquivos externos e programas
def externo(chave):
    cfg=configuracao();entry=cfg.get('externos',{}).get(chave)
    if entry is None:raise KeyError('Caminho externo não configurado: '+chave)
    text=entry.get('caminho','') if isinstance(entry,dict) else str(entry)
    if not text:raise ValueError('Preencha extern os.'+chave+' em '+str(CONFIG_FILE))
    p=Path(text).expanduser()
    if not p.is_absolute():p=raiz_projeto()/p
    if not p.exists() and 'OpenAI.CodexPrimaryRuntime.' in str(p) and 'dependencies' in p.parts:
        suffix=Path(*p.parts[p.parts.index('dependencies')+1:])
        apps=Path(os.environ.get('ProgramFiles','C:/Program Files'))/'WindowsApps'
        try:
            candidates=[x/'dependencies'/suffix for x in apps.glob('OpenAI.CodexPrimaryRuntime.*') if (x/'dependencies'/suffix).exists()]
            if candidates:p=sorted(candidates,key=lambda x:x.stat().st_mtime,reverse=True)[0]
        except OSError:pass
    return p.as_posix() if '/' in text and '\\' not in text else str(p)

# Textos com caminhos incorporados
def adaptar_texto(texto):
    cfg=configuracao();original=cfg.get('raiz_original','');roots=[original,original.replace('/','\\'),original.replace('/','\\\\')]
    pairs={}
    for old in roots:
        if not old:continue
        style='posix' if '/' in old else 'native';value=texto_caminho('',style)
        if '\\\\' in old:value=value.replace('\\','\\\\')
        pairs[old]=value
        for key in {**cfg.get('pastas',{}),**cfg.get('arquivos',{})}:
            separator='/' if '/' in old else '\\\\' if '\\\\' in old else '\\'
            target=texto_caminho(key,style)
            if '\\\\' in old:target=target.replace('\\','\\\\')
            pairs[old+separator+key.replace('/',separator)]=target
    for entry in cfg.get('externos',{}).values():
        if isinstance(entry,dict) and entry.get('original') and entry.get('chave'):
            pairs[entry['original']]=externo(entry['chave'])
    if not pairs:return texto
    pattern=re.compile('|'.join(re.escape(k) for k in sorted(pairs,key=len,reverse=True)))
    return pattern.sub(lambda m:pairs[m[0]],str(texto))
