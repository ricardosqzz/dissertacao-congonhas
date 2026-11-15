# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/projeto/temp/qa_seminarios/svg_word/manifesto.json | manifest.read_text.
# Entrada: E:/projeto/output/11_integracao/nova_modelagem/figuras_seminario_manifesto.json | .read_text.
# Entrada: Path(item['arquivo']).with_suffix('.svg') | source.read_bytes.
# Campos/chaves em style: stroke-opacity.
# Campos/chaves em item: arquivo.
# Campos/chaves em previous: output.
# Saída: E:/projeto/temp/qa_seminarios/svg_word/manifesto.json | manifest.write_text.
# Campos/chaves gerados em style: stroke.
# CÓDIGO DO PROCESSAMENTO

"""Mantém as espessuras finas ao converter SVG para PDF no Word."""
# INÍCIO DOS CAMINHOS PORTÁTEIS
import sys as _cp_sys
from pathlib import Path as _cp_Path
_cp_file = _cp_Path(globals().get('__file__', _cp_Path.cwd() / 'codigo' / 'script.py')).resolve()
for _cp_parent in [_cp_file.parent, *_cp_file.parents]:
    _cp_code = _cp_parent if (_cp_parent / 'caminhos_congonhas.py').is_file() else _cp_parent / 'codigo'
    if (_cp_code / 'caminhos_congonhas.py').is_file():
        if str(_cp_code) not in _cp_sys.path: _cp_sys.path.insert(0, str(_cp_code))
        break
from caminhos_congonhas import raiz_projeto as _cp_raiz, texto_caminho as _cp_texto, externo as _cp_externo, adaptar_texto as _cp_adaptar
# FIM DOS CAMINHOS PORTÁTEIS

from pathlib import Path
from xml.etree import ElementTree as E
from copy import deepcopy
from shapely.geometry import LineString
import json,re,hashlib
R=Path(_cp_texto('', 'native'));OUT=R/'temp/qa_seminarios/svg_word';VERSION=3

# Polygon path
def polygon_path(poly):
 def ring(coords):return 'M '+' L '.join(f'{x:.7f} {y:.7f}' for x,y in coords)+' z'
 return ' '.join(ring(v.coords) for v in [poly.exterior,*poly.interiors])

# Convert
def convert(source,target):
 d=E.parse(source);root=d.getroot();parents={x:p for p in root.iter() for x in p};count=0
 for p in list(root.iter()):
  if p.tag.rsplit('}',1)[-1]!='path':continue
  style=dict(v.strip().split(':',1) for v in (p.get('style') or '').split(';') if ':' in v);style={k:v.strip() for k,v in style.items()}
  color=style.get('stroke');width=float(style.get('stroke-width','1'))
  if not color or color=='none' or not (width<=.30 or color in ['#717d84','#b28d4f','#a54d40']):continue
  path=p.get('d','');commands=re.findall('[A-Za-z]',re.sub(r'[eE][+-]?\d+','',path))
  if set(commands)-set('MLZz'):continue
  paths=[]
  for part in re.split('[M]',path):
   if not part.strip():continue
   closed='z' in part.lower();values=[float(x) for x in re.findall(r'[-+]?(?:\d*\.\d+|\d+\.?\d*)(?:[eE][-+]?\d+)?',part)]
   if len(values)%2:raise ValueError('Coordenadas SVG inválidas')
   xy=list(zip(values[::2],values[1::2]))
   if len(xy)<2:continue
   if closed and xy[0]!=xy[-1]:xy.append(xy[0])
   poly=LineString(xy).buffer(width/2,cap_style='flat',join_style='round',quad_segs=3)
   for q in getattr(poly,'geoms',[poly]):
    if not q.is_empty:paths.append(polygon_path(q))
  if not paths:continue
  outline=deepcopy(p);outline.attrib.pop('id',None);outline.set('d',' '.join(paths));outline.set('style','fill: '+color+'; stroke: none'+('; fill-opacity: '+style['stroke-opacity'] if 'stroke-opacity' in style else ''))
  parent=parents[p];index=list(parent).index(p)
  if style.get('fill','black')!='none':
   style['stroke']='none';p.set('style','; '.join(k+': '+v for k,v in style.items()));parent.insert(index+1,outline)
  else:parent.remove(p);parent.insert(index,outline)
  count+=1
 if count:d.write(target,xml_declaration=True,encoding='utf-8')
 return count

# Run
def run():
 for prefix,uri in [('', 'http://www.w3.org/2000/svg'),('xlink','http://www.w3.org/1999/xlink'),('dc','http://purl.org/dc/elements/1.1/'),('cc','http://creativecommons.org/ns#'),('rdf','http://www.w3.org/1999/02/22-rdf-syntax-ns#')]:E.register_namespace(prefix,uri)
 OUT.mkdir(parents=True,exist_ok=True);manifest=OUT/'manifesto.json';old=json.loads(manifest.read_text(encoding='utf8')) if manifest.exists() else {};records={}
 source_manifest=json.loads((R/'output/11_integracao/nova_modelagem/figuras_seminario_manifesto.json').read_text(encoding='utf8'))
 for item in source_manifest:
  if item['arquivo']=='ORIGINAL':continue
  source=Path(item['arquivo']).with_suffix('.svg');sha=hashlib.sha256(source.read_bytes()).hexdigest();target=OUT/(source.stem+'_Word.svg');previous=old.get(str(source),{})
  if previous.get('version')==VERSION and previous.get('sha256')==sha and (not previous.get('converted') or Path(previous['output']).exists()):records[str(source)]=previous;continue
  count=convert(source,target);records[str(source)]={'source':str(source),'sha256':sha,'output':str(target) if count else str(source),'converted':count,'version':VERSION}
  print(source.name,count,'traços finos compatibilizados',flush=True)
 manifest.write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8')
 return records

if __name__=='__main__':run()
