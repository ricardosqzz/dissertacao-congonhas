# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/projeto/adi_ado_sum/'PM10.ADO' if pol == 'PM10' else 'PM25.ADO' | p.read_text.
# Entrada: cache.with_name(cache.stem + '_manifesto.json') | manifest.read_text.
# Entrada: E:/projeto/output/16_revisao_pos_banca/cenario_geral/eventos_{pol}_{period}.npz | np.load.
# Campos/chaves em cells: X, Y.
# Campos/chaves em paths: ALL.
# Campos/chaves em check: concentration, from_1h.
# Saída: E:/projeto/output/16_revisao_pos_banca/cenario_geral/envelope_{pol}_{period}.csv | envelope.to_csv.
# Campos/chaves gerados em daily: day.
# concentration: concentração do período em µg/m³.
# X: coordenada leste em metros.
# Y: coordenada norte em metros.
# Novas variáveis: config/analise_extensivel.json; definir origem, campo, agregação, transformação e peso.
# CÓDIGO DO PROCESSAMENTO

"""Meteorologia completa: envelopes 1h/24h e média anual nativa do triênio.

Sem filtro por direção, hora do dia ou persistência do vento. Preserva os
filtros de validade meteorológica e recupera cada grupo no evento de ALL.
"""
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
import json,re
import numpy as np
import pandas as pd
import geopandas as gpd
import config
from groups import GROUPS
from post_amostragem import FixedPost
from out_aermod_reader import discover,annual
from medias_horarias_verificadas import identity,met_calendar,cached_daily
from analisar_espacial_direcoes import run as spatial_run,dump,PRIMARY

ROOT=config.BASE/'output/16_revisao_pos_banca'
OUT=ROOT/'cenario_geral'
PERIODS=['1h','24h','anual']

# Excluded days
def excluded_days(pol):
    p=config.BASE/'adi_ado_sum'/('PM10.ADO' if pol=='PM10' else 'PM25.ADO')
    result=set()
    for line in p.read_text(errors='replace').splitlines():
        if 'W732' in line:
            m=re.search(r'(20\d{8})\s*$',line)
            if m:result.add(int(m[1][2:8]))
    return result,p

# Peak from valid
def peak_from_valid(values,codes,valid):
    """Máximo por coluna; empates mantêm o primeiro instante cronológico."""
    v=values[valid];t=np.asarray(codes)[valid]
    if not len(t):raise ValueError('Sem períodos válidos')
    arg=v.argmax(axis=0)
    return v[arg,np.arange(v.shape[1])],t[arg]

# Load general
def load_general(pol,period,cells):
    paths_all,_=discover(config.BASE/'out-aermod'/('PM10' if pol=='PM10' else 'PM2-5'))
    native={'1h':'1H','24h':'24H','anual':'ANNUAL'}[period]
    paths={g:p for (g,a),p in paths_all.items() if a==native}
    groups=sorted(paths)
    if set(groups)!=(set(GROUPS)|{'ALL'}):raise ValueError('Esperados 29 grupos')
    cal,met=met_calendar();bad,log=excluded_days(pol)
    stamp=dict(version=1,files={g:identity(p) for g,p in paths.items()},meteorology=met,log=identity(log),support=identity(ROOT/'celulas_analise.gpkg'),period=period,wind_filter=False)
    cache=OUT/f'eventos_{pol}_{period}.npz';manifest=cache.with_name(cache.stem+'_manifesto.json')
    if cache.exists() and manifest.exists() and json.loads(manifest.read_text(encoding='utf8'))==stamp:
        with np.load(cache) as f:return {k:f[k] for k in f.files}
    xy=cells[['X','Y']].to_numpy()
    if period=='anual':
        group_values=[];yearly=None;coords=None
        for group in groups:
            a=annual(paths[group]);pivot=a.pivot(index=['X','Y'],columns='year',values='CONC').sort_index()
            if coords is None:coords=np.array(pivot.index.tolist());yearly_full=pivot[[2021,2022,2023]].to_numpy().T
            if not np.array_equal(coords,np.array(pivot.index.tolist())):raise ValueError('Receptores anuais divergentes')
            if group=='ALL':yearly_full=pivot[[2021,2022,2023]].to_numpy().T
            selected=pd.DataFrame(xy,columns=['X','Y']).merge(pivot.mean(axis=1).rename('value').reset_index(),on=['X','Y'],validate='one_to_one')
            group_values.append(selected.value.to_numpy())
        index=pd.MultiIndex.from_arrays(coords.T).get_indexer(pd.MultiIndex.from_arrays(xy.T))
        if (index<0).any():raise ValueError('Receptor anual ausente')
        maximum=yearly_full.mean(axis=0);codes=np.zeros(len(coords),dtype=np.int64)
        yearly=yearly_full[:,index][:,None,:];counts=cal.groupby('year').valid.sum().to_numpy()[:,None]
        envelope=pd.DataFrame(dict(X=coords[:,0],Y=coords[:,1],concentration=maximum,event_code=codes,
                                   annual_max=yearly_full.max(axis=0),annual_max_year=2021+yearly_full.argmax(axis=0)))
        contributions=np.stack(group_values,axis=-1)[None,:,:]
    else:
        f=FixedPost(paths['ALL'])
        try:
            coords=f.coords.copy();index=f.receptor_indices(xy);values=f.values();codes_native=f.codes.copy()
        finally:f.close()
        if period=='1h':
            valid=pd.Series(codes_native).map(cal.set_index('CODE').valid).fillna(False).to_numpy(dtype=bool)
        else:
            valid_hours=cal.groupby('day').valid.sum()
            days=codes_native//100
            valid=pd.Series(days).map(valid_hours).fillna(0).ge(18).to_numpy() & ~np.isin(days,list(bad))
        maximum,codes=peak_from_valid(values,codes_native,valid)
        yearly=np.empty((3,1,len(cells)));counts=np.zeros((3,1),int)
        for yi,year in enumerate([2021,2022,2023]):
            mask=valid&(2000+codes_native//1_000_000==year)
            yearly[yi,0]=values[mask][:,index].max(axis=0);counts[yi,0]=int(mask.sum())
        envelope=pd.DataFrame(dict(X=coords[:,0],Y=coords[:,1],concentration=maximum,event_code=codes))
        if period=='24h':

            daily=cached_daily(paths['ALL']);daily['day']=daily.date.dt.strftime('%y%m%d').astype(int)
            days=codes_native[valid]//100
            peak=daily[daily.day.isin(days)].groupby(['X','Y']).CONC.max().rename('from_1h').reset_index()
            check=envelope.merge(peak,on=['X','Y'],validate='one_to_one')
            if not np.allclose(check.concentration,check.from_1h,rtol=2e-7,atol=1e-5):raise ValueError('Máximo 24h diverge da reconstrução de 1h')
        del values
        contributions=[]
        for group in groups:
            f=FixedPost(paths[group])
            try:contributions.append(f.sample(codes[index],xy))
            finally:f.close()
            print('Geral',pol,period,group,'mesmo evento ALL',flush=True)
        contributions=np.stack(contributions,axis=-1)[None,:,:]
    envelope.to_csv(OUT/f'envelope_{pol}_{period}.csv',index=False)
    if period=='anual':
        geo=pd.DataFrame(coords,columns=['X','Y'])
        index=pd.MultiIndex.from_frame(geo).get_indexer(pd.MultiIndex.from_arrays(xy.T))
    all_values=maximum[index][None,:];all_codes=codes[index][None,:]
    if not np.allclose(contributions[:,:,groups.index('ALL')],all_values,rtol=2e-7,atol=1e-5):raise ValueError('ALL não reproduz o campo geral')
    closure=contributions[:,:,[groups.index(g) for g in PRIMARY]].sum(axis=-1)
    if not np.allclose(closure,all_values,rtol=3e-5,atol=2e-4):raise ValueError('Grupos exclusivos não fecham com ALL')
    result=dict(concentrations=all_values,codes=all_codes,group_values=contributions,groups=np.array(groups),yearly=yearly,counts=counts)
    np.savez_compressed(cache,**result);dump(manifest,stamp)
    dump(OUT/f'periodos_{pol}_{period}.json',dict(pollutant=pol,period=period,years=[2021,2022,2023],wind_filter=False,eligible_periods_by_year=counts.ravel().tolist(),annual_definition='Média aritmética das três médias anuais nativas' if period=='anual' else None,daily_definition='Máximo das médias diárias completas; mínimo 18h e exclusão W732' if period=='24h' else None,group_closure_max_abs=float(np.abs(closure-all_values).max()),regional_receptors=len(coords),municipal_receptors=len(cells)))
    return result

# Run
def run():
    OUT.mkdir(parents=True,exist_ok=True)
    spatial_run(directions=['GERAL'],periods=PERIODS,output=OUT,loader=load_general)

if __name__=='__main__':run()
