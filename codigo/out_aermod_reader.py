# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: {path} | .open.
# Entrada: {path} | pd.read_csv.
# Entrada: {path} | read_table.
# Entrada: {log} | .read_text.
# Campos/chaves em h: group, has_data, n_receptors, period.
# Campos/chaves em df: CONC, GRP, X, Y.
# Campos/chaves em d: AVE, CODE, CONC, X, Y, date, year.
# Campos/chaves em config.DIRS: post.
# Campos/chaves em coords: X, Y.
# Campos/chaves em zones: geometry, zone_index.
# Campos/chaves em original: X, Y, geometry.
# Campos/chaves em merged.loc: geometry.
# Campos/chaves em p.loc: geometry.
# Campos/chaves em strict: X, Y, zone_index.
# Campos/chaves em links: X, Y, zone_index.
# Saídas: retorno de funções, verificações ou arquivos definidos pelo chamador.
# Campos/chaves gerados em PLT_GROUPS: GALL.
# Campos/chaves gerados em d: date, year.
# Campos/chaves gerados em original: X, Y.
# Campos/chaves gerados em links: spatial_support.
# X: coordenada leste em metros.
# Y: coordenada norte em metros.
# CÓDIGO DO PROCESSAMENTO

"""Saídas nativas por período, sem misturar POST anual, diário e horário."""
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
import re
import numpy as np
import pandas as pd
from groups import canonical_post_group

PLT_GROUPS=dict(zip([f'G{i:03d}' for i in range(1,29)],
    ['AEX','BVC','CDA','COC','COOPERA','CSN-CDP','CSN-PIR','ECOMIN','FERRO','GERDAU','LGA','LL-TRANS','LM-MIN','MONT-MIN','NOGD','RODEIRO','SAPPORO','SILVANO','TERRA-MI','TERRAMAR','URB','URB-FER','URB-NUC','URB-VIA','VALE_FAB','VALE_VIG','WGM','SCOF']))
PLT_GROUPS['GALL']='ALL'

# Filename identity
def filename_identity(path):
    name=Path(path).stem.upper()
    match=re.search(r'(01H(?:1)?|24H(?:1)?|AN00)(G(?:\d{3}|ALL))$',name)
    if match:return PLT_GROUPS.get(match[2]), 'ANNUAL' if match[1]=='AN00' else '24H' if match[1].startswith('24') else '1H'
    match=re.match(r'(01|24|AN)_(.+)$',name)
    if match:return canonical_post_group(match[2]), {'01':'1H','24':'24H','AN':'ANNUAL'}[match[1]]
    return None,None

# Header
def header(path):
    lines=[];line=''
    with Path(path).open(encoding='latin1') as f:
        for line in f:
            if not line.startswith('*'):break
            lines.append(line)
    text=''.join(lines)
    group=re.search(r'SOURCE GROUP:\s*(\S+)',text)
    count=re.search(r'TOTAL OF\s+(\d+)\s+RECEPTORS',text)
    period='ANNUAL' if 'ANNUAL' in text else '24H' if '24-HR' in text else '1H' if '1-HR' in text else None
    fg,fp=filename_identity(path)
    hg=canonical_post_group(group[1]) if group else None
    if hg and fg and hg!=fg:raise ValueError(f'Grupo do nome diverge do cabeçalho: {path}')
    if period and fp and period!=fp:raise ValueError(f'Período do nome diverge do cabeçalho: {path}')
    return dict(group=hg or fg,period=period or fp,n_receptors=int(count[1]) if count else None,has_data=bool(line.strip()) and not line.startswith('*'))

# Discover
def discover(folder):
    selected={};ignored=[]
    for p in sorted(Path(folder).glob('*.POS')):
        h=header(p)
        if not h['has_data']:
            ignored.append(str(p));continue
        key=(h['group'],h['period'])
        if None in key:raise ValueError(f'Cabeçalho desconhecido: {p}')
        if key in selected:raise ValueError(f'Saídas duplicadas para {key}: {p} e {selected[key]}')
        selected[key]=p
    return selected,ignored

# Read table
def read_table(path):
    h=header(path)
    df=pd.read_csv(path,sep=r'\s+',comment='*',header=None,usecols=[0,1,2,6,7,8],names=['X','Y','CONC','AVE','GRP','CODE'],engine='c')
    if df.empty:raise ValueError(f'Sem registros: {path}')
    if not np.isfinite(df[['X','Y','CONC']]).all().all() or df.CONC.lt(0).any():
        raise ValueError(f'Concentração/coordenada inválida: {path}')
    if h['n_receptors'] is not None and df[['X','Y']].drop_duplicates().shape[0]!=h['n_receptors']:raise ValueError(f'Número de receptores inconsistente: {path}')
    if df.duplicated(['X','Y','CODE']).any():raise ValueError(f'Receptor/período duplicado: {path}')
    if {canonical_post_group(g) for g in df.GRP.unique()}!={h['group']}:raise ValueError(f'Grupo divergente: {path}')
    return df

# Annual
def annual(path,years=(2021,2022,2023)):
    d=read_table(path)
    if set(d.AVE)!={'ANNUAL'} or set(d.CODE)!={1,2,3}:raise ValueError(f'Anos anuais inesperados: {path}')
    d['year']=d.CODE.map(dict(enumerate(years,1)))
    return d[['X','Y','year','CONC']]

# Daily
def daily(path,log=None,years=(2021,2022,2023)):
    import config
    project_post=Path(path).resolve().is_relative_to(config.DIRS['post'].resolve())
    if project_post and header(path)['group']=='ALL':
        from medias_horarias_verificadas import cached_daily
        d=cached_daily(path)
    else:
        d=read_table(path)
        if set(d.AVE)!={'24-HR'}:raise ValueError('A série diária deve ser 24-HR')
        code=d.CODE.astype(str).str.zfill(8)
        d['date']=pd.to_datetime(code.str[:6],format='%y%m%d',errors='raise');d['year']=d.date.dt.year
    d=d[d.year.isin(years)].copy()

    excluded=set()
    if log:
        for line in Path(log).read_text(errors='replace').splitlines():
            if 'W732' in line:
                match=re.search(r'(20\d{8})\s*$',line)
                if match:excluded.add(pd.to_datetime(match[1][:8],format='%Y%m%d'))
    d.loc[d.date.isin(excluded),'CONC']=np.nan
    return d[['X','Y','date','year','CONC']],sorted(str(x.date()) for x in excluded)

# Saturation class
def saturation_class(value):
    if not np.isfinite(value):return 'Informação insuficiente'
    return 'Abaixo da faixa preventiva' if value<=90 else 'Próxima do padrão' if value<=100 else 'Acima do padrão'

# Exploratory four class
def exploratory_four_class(value):
    """Proposta para avaliação; corte 50% exploratório, sem alterar índice PD."""
    if not np.isfinite(value):return 'Informação insuficiente'
    return 'Baixa' if value<=50 else 'Média' if value<=90 else 'Alta' if value<=100 else 'Muito alta'

# Link receptors
def link_receptors(coords,zones,grid):
    """Recupera posição original somente quando a exportação arredondada coincide.

    A concentração permanece vinculada ao X/Y do POST. Não usa vizinho mais
    próximo nem amplia zonas; guarda evidência da correção subcentimétrica.
    """
    import geopandas as gpd
    original=grid.to_crs(zones.crs).copy()
    original['X']=original.geometry.x.round(2);original['Y']=original.geometry.y.round(2)
    if original.duplicated(['X','Y']).any():raise ValueError('Grade ambígua após arredondamento')
    xy=coords[['X','Y']].drop_duplicates().copy()
    p=gpd.GeoDataFrame(xy,geometry=gpd.points_from_xy(xy.X,xy.Y),crs=zones.crs)
    initial=gpd.sjoin(p,zones[['zone_index','geometry']],how='inner',predicate='within')
    merged=xy.merge(original[['X','Y','geometry']],how='left',on=['X','Y'])
    resolved=merged.geometry.notna();distance=gpd.GeoSeries(merged.loc[resolved,'geometry'],crs=zones.crs).distance(p.loc[resolved,'geometry'])
    if distance.max()>.0072:raise ValueError('Deslocamento incompatível com arredondamento centimétrico')
    p.loc[resolved,'geometry']=merged.loc[resolved,'geometry'].to_numpy()
    strict=gpd.sjoin(p,zones[['zone_index','geometry']],how='inner',predicate='within')[['X','Y','zone_index']]

    boundary=zones[['zone_index','geometry']].copy();boundary.geometry=boundary.geometry.buffer(1e-7)
    links=gpd.sjoin(p,boundary,how='inner',predicate='intersects')[['X','Y','zone_index']]
    keys=set(map(tuple,strict[['X','Y','zone_index']].to_numpy()))
    links['spatial_support']=['interior' if tuple(r) in keys else 'fronteira_numerica' for r in links[['X','Y','zone_index']].to_numpy()]
    return links,dict(zones_strict_export=int(initial.zone_index.nunique()),zones_original_precision=int(strict.zone_index.nunique()),zones_with_boundary=int(links.zone_index.nunique()),boundary_tolerance_m=1e-7,matched_original_points=int(resolved.sum()),max_rounding_shift_m=float(distance.max()))
