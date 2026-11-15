# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: {path} | path.open.
# Entrada: io.BytesIO(subset.tobytes()) | pd.read_csv.
# Entrada: E:/projeto/output/15_auditoria_metodologica/revisao_cientifica/vinculos_estacoes_receptores.csv | pd.read_csv.
# Entrada: E:/projeto/adi_ado_sum/'PM10.ADI' if pol == 'PM10' else 'PM25.ADI' | adi.read_text.
# Entrada: E:/projeto/output/13_rateio_emissoes/fontes_rateio_{pol}.gpkg | gpd.read_file.
# Entrada: E:/projeto/output/09_projeto_dissertacao/seminarios_02/apresentacao/apoio_meteorologia_perfis/pares_horarios_{pol}.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/{pol}_{group}_cache.json | meta.read_text.
# Entrada: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/{pol}_{group}_estacoes.csv.gz | pd.read_csv.
# Campos/chaves em cal.loc: CODE.
# Campos/chaves em stations: pollutant.
# Campos/chaves em observed: CODE.
# Campos/chaves em d: CODE.
# Saída: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/{pol}_grupos_estaticos_auxiliares.INC | .write_text.
# Saída: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/{pol}_grupos_estaticos_auxiliares.csv | .to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/{pol}_{group}_estacoes.csv.gz | d.to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/{pol}_{group}_cache.json | meta.write_text.
# Saída: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/perfis_normalizados_grupos_estacoes.csv | .to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/diagnostico_concordancia_grupos.csv | .to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/distancias_grupos_estacoes.csv | .to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/grupos_fontes_horarias_e_estaticas.csv | .to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/manifesto.json | .write_text.
# Campos/chaves gerados em groups: ALL.
# Campos/chaves gerados em d: hour.
# Campos/chaves gerados em p: group_id, group_norm, observed_norm, pollutant, station_id.
# CÓDIGO DO PROCESSAMENTO

"""Extrai somente receptores das estações dos POST fixos e documenta identificabilidade."""
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
import json,io,re
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from out_aermod_reader import discover,header
from groups import GROUPS,canonical_post_group
from medias_horarias_verificadas import met_calendar,identity
import config
ROOT=config.BASE/'output/16_revisao_pos_banca';OUT=ROOT/'perfis_grupos'

# Station records
def station_records(path,stations):
    nr=header(path)['n_receptors']
    if not nr:raise ValueError('Número de receptores ausente do cabeçalho')
    with path.open('rb') as f:
        offset=0
        for line in f:
            if not line.startswith(b'*'):break
            offset+=len(line)
        size=len(line);f.seek(offset);first=f.read(size*nr)
    if (path.stat().st_size-offset)%size:raise ValueError('POST sem comprimento fixo consistente')
    n=(path.stat().st_size-offset)//size;assert n%nr==0
    coords=np.array([[float(r[:14]),float(r[14:28])] for r in first.splitlines()]);indexes=[]
    for r in stations.itertuples():
        found=np.where(np.isclose(coords[:,0],r.X,atol=.001,rtol=0)&np.isclose(coords[:,1],r.Y,atol=.001,rtol=0))[0];assert len(found)==1;indexes.append(found[0])
    mmap=np.memmap(path,dtype='S'+str(size),mode='r',offset=offset,shape=(n//nr,nr));subset=mmap[:,indexes].copy();del mmap
    d=pd.read_csv(io.BytesIO(subset.tobytes()),sep=r'\s+',header=None,usecols=[0,1,2,8],names=['X','Y','modelled','CODE']);return d.merge(stations,on=['X','Y'],validate='many_to_one')

# Run
def run():
    OUT.mkdir(exist_ok=True,parents=True);cal,met=met_calendar();good=set(cal.loc[cal.valid,'CODE']);profiles=[];diagnostics=[];distances=[];source_flags=[]
    stations=pd.read_csv(config.BASE/'output/15_auditoria_metodologica/revisao_cientifica/vinculos_estacoes_receptores.csv')
    for pol,folder in [('PM10','PM10'),('PM25','PM2-5')]:
        st=stations[stations.pollutant.eq(pol)][['station_id','X','Y']].drop_duplicates();selected,_=discover(config.BASE/f'out-aermod/{folder}')
        adi=config.BASE/'adi_ado_sum'/('PM10.ADI' if pol=='PM10' else 'PM25.ADI');hourly=set();groups={};all_ids=set()
        for line in adi.read_text(encoding='latin1').splitlines():
            p=line.split();p=p[1:] if p[:1]==['SO'] else p
            if p[:1]==['HOUREMIS']:hourly.update(p[2:])
            if p[:1]==['SRCGROUP']:groups.setdefault(canonical_post_group(p[1]),set()).update(p[2:])
            if p[:1]==['LOCATION']:all_ids.add(p[1])
        groups['ALL']=all_ids
        for group,ids in groups.items():
            source_flags.append({'pollutant':pol,'group_id':group,'sources':len(ids),'hourly_sources':len(ids&hourly),'static_sources':len(ids-hourly),'multiplication_of_whole_group_valid':not bool(ids&hourly)})

        aux=['** Auxiliary static-source groups for a future identifiability run','** Insert within SO pathway; unchanged emissions and HOUREMIS files'];mapping=[]
        for i,(group,ids) in enumerate(sorted(groups.items()),1):
            if group not in GROUPS or GROUPS[group]['kind']!='primary':continue
            static=sorted(ids-hourly);gid=f'S{i:03d}'
            for a in range(0,len(static),6):aux.append('SO SRCGROUP '+gid+' '+' '.join(static[a:a+6]))
            mapping.append({'pollutant':pol,'group_id':group,'aux_static_group':gid,'n_static':len(static),'n_excluded_emi':len(ids&hourly)})
        (OUT/f'{pol}_grupos_estaticos_auxiliares.INC').write_text('\n'.join(aux)+'\n',encoding='ascii');pd.DataFrame(mapping).to_csv(OUT/f'{pol}_grupos_estaticos_auxiliares.csv',index=False)
        src=gpd.read_file(config.BASE/f'output/13_rateio_emissoes/fontes_rateio_{pol}.gpkg')
        for group,g in src.groupby('group_id'):
            geom=g.geometry.union_all();weight=np.maximum(g.massa.to_numpy(),0);centers=g.geometry.centroid
            if weight.sum():cx=np.average(centers.x,weights=weight);cy=np.average(centers.y,weights=weight)
            else:cx=geom.centroid.x;cy=geom.centroid.y
            for r in st.itertuples():distances.append({'pollutant':pol,'group_id':group,'station_id':r.station_id,'distance_min_geometry_km':geom.distance(Point(r.X,r.Y))/1000,'distance_emission_centroid_km':np.hypot(cx-r.X,cy-r.Y)/1000,'bearing_station_to_emission_centroid':np.rad2deg(np.arctan2(cx-r.X,cy-r.Y))%360})
        observed=pd.read_csv(config.BASE/f'output/09_projeto_dissertacao/seminarios_02/apresentacao/apoio_meteorologia_perfis/pares_horarios_{pol}.csv',usecols=['station_id','CODE','observed']);observed=observed[observed.CODE.isin(good)]
        for (group,period),path in selected.items():
            if period!='1H':continue
            cache=OUT/f'{pol}_{group}_estacoes.csv.gz';meta=OUT/f'{pol}_{group}_cache.json'
            if cache.exists() and meta.exists() and json.loads(meta.read_text())==identity(path):d=pd.read_csv(cache)
            else:
                d=station_records(path,st);d=d[d.CODE.isin(good)];d.to_csv(cache,index=False,compression='gzip');meta.write_text(json.dumps(identity(path)),encoding='utf8')
            d=d.merge(observed,on=['station_id','CODE'],validate='one_to_one');d['hour']=d.CODE%100-1
            for station,s in d.groupby('station_id'):
                p=s.groupby('hour')[['observed','modelled']].mean();p['observed_norm']=p.observed/p.observed.mean();p['group_norm']=p.modelled/p.modelled.mean() if p.modelled.mean()>0 else np.nan;p['pollutant']=pol;p['group_id']=group;p['station_id']=station;profiles.append(p.reset_index());diagnostics.append({'pollutant':pol,'group_id':group,'station_id':station,'hours_paired':len(s),'observed_mean':s.observed.mean(),'group_mean':s.modelled.mean(),'hourly_r':s.observed.corr(s.modelled),'shape_r_24h':p.observed_norm.corr(p.group_norm)})
            print(pol,group,'perfis nas estações extraídos',flush=True)
    pd.concat(profiles).to_csv(OUT/'perfis_normalizados_grupos_estacoes.csv',index=False);pd.DataFrame(diagnostics).to_csv(OUT/'diagnostico_concordancia_grupos.csv',index=False);pd.DataFrame(distances).to_csv(OUT/'distancias_grupos_estacoes.csv',index=False);pd.DataFrame(source_flags).to_csv(OUT/'grupos_fontes_horarias_e_estaticas.csv',index=False)
    (OUT/'manifesto.json').write_text(json.dumps({'met':met,'clock':'Hipótese prévia UTC→UTC−3, início do intervalo AERMOD. Pendente confirmação documental.','fit_to_observations_applied':False,'reason':'Curvas de grupo misturam fontes horárias e estáticas; observação é mistura transportada. Requer matriz estática isolada, regularização, metadados e avaliação fora da amostra.','normalization':'Média por hora do dia dividida pela média das 24 médias, nas mesmas horas pareadas.','distance_role':'Diagnóstico geométrico, não peso inverso de distância para atribuir emissão.'},ensure_ascii=False,indent=2),encoding='utf8')

if __name__=='__main__':run()
