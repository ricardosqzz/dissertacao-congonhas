# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/eventos_{pol}_{period}_manifesto.json | signature.read_text.
# Entrada: E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/eventos_{pol}_{period}.npz | np.load.
# Entrada: E:/projeto/output/16_revisao_pos_banca/vento/{pol}_envelopes_{'horarios' if period == '1h' else 'diarios_persistentes'}.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/vento/'calendario_vento_horario.csv' if period == '1h' else 'dias_direcao_persistente.csv' | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/celulas_analise.gpkg | gpd.read_file.
# Entrada: E:/projeto/output/16_revisao_pos_banca/zoneamento_pos_banca.gpkg | gpd.read_file.
# Entrada: E:/projeto/output/16_revisao_pos_banca/vinculo_celula_zona.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/perfis_normalizados_grupos_estacoes.csv | pd.read_csv.
# Entrada: E:/projeto/output/15_auditoria_metodologica/revisao_cientifica/vinculos_estacoes_receptores.csv | pd.read_csv.
# Entrada: E:/projeto/output/11_integracao/nova_modelagem/estacoes_trienio_comum.csv | pd.read_csv.
# Entrada: {p} | load.
# Campos/chaves em v: kind.
# Campos/chaves em cells: X, Y, geometry, receptor_id.
# Campos/chaves em raw: direction.
# Campos/chaves em paths: ALL.
# Campos/chaves em calendar: CODE, day.
# Campos/chaves em r: silhouette.
# Campos/chaves em best: k, method.
# Campos/chaves em labels: ward.
# Campos/chaves em eligible: n_design_years, pollutant.
# Campos/chaves em sg: station_id.
# Campos/chaves em d: codes, concentrations, counts, group_values, groups, yearly.
# Campos/chaves em sg.loc: station_id.
# Campos/chaves em z: zone_index.
# Campos/chaves em spatial: network_priority.
# Saída: {path} | path.write_text.
# Saída: Path(output) if output is not None else globals()['OUT']/comparacao_agrupamentos.csv | .to_csv.
# Saída: Path(output) if output is not None else globals()['OUT']/{pol}_{period}_receptores.csv | table.to_csv.
# Saída: Path(output) if output is not None else globals()['OUT']/correlogramas.csv | .to_csv.
# Saída: Path(output) if output is not None else globals()['OUT']/sensibilidade_espacial.csv | .to_csv.
# Saída: Path(output) if output is not None else globals()['OUT']/limiares_cinco_faixas.csv | .to_csv.
# Saída: Path(output) if output is not None else globals()['OUT']/limiares_regressao_complementar.csv | .to_csv.
# Saída: Path(output) if output is not None else globals()['OUT']/distribuicoes_emissao_por_faixa.csv | .to_csv.
# Saída: Path(output) if output is not None else globals()['OUT']/'regioes_gerais' if general else 'regioes_direcionais'.gpkg | region_frame.to_file.
# Saída: Path(output) if output is not None else globals()['OUT']/'regioes_gerais' if general else 'regioes_direcionais'.csv | .to_csv.
# Saída: Path(output) if output is not None else globals()['OUT']/ABC_contribuicoes_regioes.csv | .to_csv.
# Saída: Path(output) if output is not None else globals()['OUT']/regioes_zoneamento.csv | .to_csv.
# Saída: Path(output) if output is not None else globals()['OUT']/'zoneamento_geral' if general else 'zoneamento_direcional'.csv | zones.to_csv.
# Saída: Path(output) if output is not None else globals()['OUT']/contribuicoes_receptores_no_evento_ALL.csv.gz | .to_csv.
# Campos/chaves gerados em calendar: native_code.
# Campos/chaves gerados em f: best_cluster, dominant_group, emission_band, emission_band_basis, emission_density, five_emission_bands_identifiable, management, mass_tpy, matrix, network_priority, ward4.
# Campos/chaves gerados em spatial: network_priority.
# Campos/chaves gerados em summary: clustering_joint_1h_24h_anual.
# receptor_id: identificador do receptor.
# mass_tpy: massa anual em t/ano.
# emission_density: densidade de emissão em t/ano/km².
# X: coordenada leste em metros.
# Y: coordenada norte em metros.
# best_cluster: perfil conjunto selecionado pela silhouette.
# Novas variáveis: config/analise_extensivel.json; definir origem, campo, agregação, transformação e peso.
# CÓDIGO DO PROCESSAMENTO

"""Repete a análise espacial nos envelopes, preservando evento e suporte.

Máximos de receptores diferentes não são um evento simultâneo. Contribuições
sempre são consultadas no horário/dia do máximo de ALL no mesmo receptor.
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
import json
import numpy as np
import pandas as pd
import geopandas as gpd
from scipy import sparse
from scipy.spatial import distance,cKDTree
from scipy.cluster.hierarchy import linkage,fcluster
from scipy.cluster.vq import kmeans2
from scipy.sparse.csgraph import connected_components
from shapely.geometry import Point
import config
from groups import GROUPS
from out_aermod_reader import discover
from post_amostragem import FixedPost
from medias_horarias_verificadas import identity
from revisao_espacial_pos_banca import (weights,moran,local_moran,relative_quintile,ari,bh,thresholds,SEED)
from complementar_quintis_gestao import estimate_cuts,binary_cut

ROOT=config.BASE/'output/16_revisao_pos_banca'
OUT=ROOT/'vento/analises_espaciais'
DIRS=['N','NE','L','SE','S','SO','O','NO']
PRIMARY=[k for k,v in GROUPS.items() if v['kind']=='primary']
ROLES=['Prioridade receptora','Controle de fontes','Menor impacto relativo','Acompanhamento']

# Dump
def dump(path,obj):
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2,default=lambda v:v.item() if isinstance(v,np.generic) else str(v)),encoding='utf8')

# Peak data
def peak_data(pol,period,cells):
    folder=config.BASE/f'out-aermod/{"PM10" if pol=="PM10" else "PM2-5"}'
    selected,_=discover(folder);native='1H' if period=='1h' else '24H'
    paths={g:p for (g,a),p in selected.items() if a==native}
    groups=sorted(paths)
    if set(groups)!=(set(GROUPS)|{'ALL'}):raise ValueError('Conjunto dos 29 grupos incompleto')
    source=ROOT/'vento'/f'{pol}_envelopes_{"horarios" if period=="1h" else "diarios_persistentes"}.csv'
    met=ROOT/'vento'/('calendario_vento_horario.csv' if period=='1h' else 'dias_direcao_persistente.csv')
    stamp={'version':2,'files':{g:identity(p) for g,p in paths.items()},'envelope':identity(source),'calendar':identity(met),'support':identity(ROOT/'celulas_analise.gpkg')}
    cache=OUT/f'eventos_{pol}_{period}.npz';signature=OUT/f'eventos_{pol}_{period}_manifesto.json'
    if cache.exists() and signature.exists() and json.loads(signature.read_text(encoding='utf8'))==stamp:
        with np.load(cache) as f:return {k:f[k] for k in f.files}
    raw=pd.read_csv(source);xy=cells[['X','Y']];col='max_1h' if period=='1h' else 'daily_from_1h'
    c=[];code=[]
    for direction in DIRS:
        s=xy.merge(raw[raw.direction.eq(direction)],on=['X','Y'],validate='one_to_one')
        if len(s)!=len(cells) or s[col].isna().any():raise ValueError('Envelope direcional incompleto')
        c.append(s[col].to_numpy());code.append(s.max_code.to_numpy() if period=='1h' else s.day.to_numpy()*100+24)
    all_values=np.array(c);codes=np.array(code,dtype=np.int64);sample_xy=np.tile(xy.to_numpy(),(8,1));contribution=[]
    for group in groups:
        f=FixedPost(paths[group])
        try:contribution.append(f.sample(codes.ravel(),sample_xy).reshape(8,len(cells)))
        finally:f.close()
        print(pol,period,group,'evento ALL recuperado',flush=True)
    contribution=np.stack(contribution,axis=-1);all_index=groups.index('ALL')
    if not np.allclose(contribution[:,:,all_index],all_values,rtol=2e-7,atol=1e-5):
        raise ValueError('Evento recuperado diverge do máximo ALL')
    indexes=[groups.index(g) for g in PRIMARY]
    if not np.allclose(contribution[:,:,indexes].sum(axis=-1),all_values,rtol=3e-5,atol=2e-4):
        raise ValueError('Grupos exclusivos não fecham com ALL no evento')
    f=FixedPost(paths['ALL'])
    try:
        values=f.values(receptor_indices=f.receptor_indices(xy.to_numpy()))
        calendar=pd.read_csv(met)
        calendar['native_code']=calendar.CODE if period=='1h' else calendar.day*100+24
        lookup=calendar.set_index('native_code').direction_idx
        sectors=pd.Series(f.codes).map(lookup).fillna(-1).to_numpy()
        years=2000+f.codes//1_000_000
        yearly=np.full((3,8,len(cells)),np.nan);counts=np.zeros((3,8),int)
        for yi,year in enumerate([2021,2022,2023]):
            for di in range(8):
                mask=(years==year)&(sectors==di);counts[yi,di]=int(mask.sum())
                if mask.any():yearly[yi,di]=values[mask].max(axis=0)
        if not np.allclose(np.nanmax(yearly,axis=0),all_values,rtol=2e-7,atol=1e-5):
            raise ValueError('Máximos anuais não reproduzem o envelope trienal')
    finally:f.close()
    result=dict(concentrations=all_values,codes=codes,group_values=contribution,groups=np.array(groups),yearly=yearly,counts=counts)
    np.savez_compressed(cache,**result);dump(signature,stamp)
    print(pol,period,'contribuições nos eventos e envelopes anuais conferidos',flush=True)
    return result

# Partition
def partition(frame,field):
    """Conectividade por segmento compartilhado, sem unir somente vértices."""
    for value,sub in frame.groupby(field,sort=True):
        sub=sub.copy().reset_index(drop=True)
        pairs=sub.sindex.query(sub.geometry,predicate='touches')
        edges=[(a,b) for a,b in pairs.T if a!=b and sub.geometry.iloc[a].boundary.intersection(sub.geometry.iloc[b].boundary).length>.01]
        e=np.array(edges).T if edges else np.zeros((2,0),int)
        adjacency=sparse.coo_matrix((np.ones(e.shape[1]),e),shape=(len(sub),len(sub)))
        n,labels=connected_components(adjacency,directed=False)
        order=sorted(range(n),key=lambda k:(sub[labels==k].geometry.union_all().centroid.x,sub[labels==k].geometry.union_all().centroid.y))
        for j,k in enumerate(order,1):yield value,j,sub[labels==k]

# Silhouette fast
def silhouette_fast(dm,labels):
    groups=np.unique(labels);means=np.stack([dm[:,labels==g].mean(axis=1) for g in groups],axis=1)
    size=np.array([(labels==g).sum() for g in groups]);membership=np.searchsorted(groups,labels)
    own=means[np.arange(len(labels)),membership]
    a=own*np.divide(size[membership],size[membership]-1,out=np.zeros(len(labels)),where=size[membership]>1)
    means[np.arange(len(labels)),membership]=np.inf;b=means.min(axis=1);den=np.maximum(a,b)
    score=np.divide(b-a,den,out=np.zeros(len(a)),where=den>0);score[size[membership]==1]=0
    return float(score.mean())

# Clustering
def clustering(features):
    x=np.log1p(features);scale=x.std(0);x=(x-x.mean(0))/np.where(scale>0,scale,1);dm=distance.cdist(x,x);tree=linkage(x,method='ward');records=[];labels={}
    for method in ['ward','kmeans']:
        for k in range(2,7):
            if method=='ward':lab=fcluster(tree,k,criterion='maxclust')-1
            else:
                fits=[kmeans2(x,k,minit='++',iter=100,rng=np.random.default_rng(SEED+j)) for j in range(10)]
                _,lab=min(fits,key=lambda v:((x-v[0][v[1]])**2).sum())
            rank=pd.Series(x.mean(axis=1)).groupby(lab).mean().sort_values().index
            mapping={old:i+1 for i,old in enumerate(rank)};lab=np.array([mapping[v] for v in lab])
            labels[method,k]=lab;records.append(dict(method=method,k=k,silhouette=silhouette_fast(dm,lab),smallest_cluster=int(pd.Series(lab).value_counts().min())))
    best=max(records,key=lambda r:r['silhouette'])
    return records,labels[best['method'],best['k']],labels['ward',4],best

# Run
def run(*, directions=None, periods=None, output=None, loader=None):
    DIRS=directions or globals()['DIRS']
    PERIODS=periods or ['1h','24h']
    OUT=Path(output) if output is not None else globals()['OUT']
    load=loader or peak_data
    general=directions==['GERAL']
    region_stem='regioes_gerais' if general else 'regioes_direcionais'
    zone_stem='zoneamento_geral' if general else 'zoneamento_direcional'
    feature_description='Máximos 1h e 24h e média anual trienal dos dois poluentes' if general else 'Máximos 1h e 24h dos dois poluentes em cada direção'
    OUT.mkdir(parents=True,exist_ok=True);cells=gpd.read_file(ROOT/'celulas_analise.gpkg').reset_index(drop=True)
    z=gpd.read_file(ROOT/'zoneamento_pos_banca.gpkg');links=pd.read_csv(ROOT/'vinculo_celula_zona.csv',usecols=['zone_index','receptor_id','zone_area_fraction'])
    xy=cells[['X','Y']].to_numpy();areas=cells.area.to_numpy();n=len(cells)
    w,ids,_=weights(xy,8);neighbors={k:weights(xy,k)[1] for k in [4,12]};dm=distance.cdist(xy,xy)
    band_weights=[]
    for upper in range(750,8250,750):
        keep=(dm>upper-750)&(dm<=upper);wc=sparse.csr_matrix(keep.astype(float));rs=np.asarray(wc.sum(1)).ravel()
        wc=sparse.diags(np.divide(1,rs,out=np.zeros_like(rs),where=rs>0))@wc
        band_weights.append((upper,wc,int(keep.sum()),int((rs==0).sum())))
    support=[]
    municipality=z.geometry.union_all();xmin,ymin,xmax,ymax=municipality.bounds
    for dx,dy in [(0,0),(250,0),(0,250),(250,250)]:
        xx=np.arange(np.ceil(xmin/500)*500+dx,xmax,500);yy=np.arange(np.ceil(ymin/500)*500+dy,ymax,500)
        target=np.array([(x,y) for x in xx for y in yy if municipality.covers(Point(x,y))]);dist,index=cKDTree(xy).query(target)
        support.append((dx,dy,index[dist<=354],int((dist>354).sum())))
    present=pd.read_csv(ROOT/'perfis_grupos/perfis_normalizados_grupos_estacoes.csv')[['pollutant','station_id']].drop_duplicates()
    station_coords=pd.read_csv(config.BASE/'output/15_auditoria_metodologica/revisao_cientifica/vinculos_estacoes_receptores.csv').merge(present,on=['pollutant','station_id'],validate='one_to_one')
    eligible=pd.read_csv(config.BASE/'output/11_integracao/nova_modelagem/estacoes_trienio_comum.csv');eligible=eligible[eligible.n_design_years.eq(3)]
    networks={}
    for pol in ['PM10','PM25']:
        st=station_coords[station_coords.pollutant.eq(pol)].copy()
        sg=gpd.GeoDataFrame(st,geometry=gpd.points_from_xy(st.X,st.Y),crs=cells.crs)
        es=sg[sg.station_id.isin(eligible[eligible.pollutant.eq(pol)].station_id)]
        networks[pol]=(sg,sg.buffer(config.REPRESENTATIVITY_RADIUS_M).union_all(),es.buffer(config.REPRESENTATIVITY_RADIUS_M).union_all(),es)
    raw={(p,t):load(p,t,cells) for p in ['PM10','PM25'] for t in PERIODS}
    cluster_rows=[];joint={}
    for di,direction in enumerate(DIRS):
        feat=np.column_stack([raw[p,t]['concentrations'][di] for p in ['PM10','PM25'] for t in PERIODS])
        records,lab,ward4,best=clustering(feat);joint[direction]=(lab,ward4,best)
        cluster_rows.extend(dict(direction=direction,feature_set=feature_description,**r) for r in records)
    pd.DataFrame(cluster_rows).to_csv(OUT/'comparacao_agrupamentos.csv',index=False)
    rows=[];corr=[];stability=[];cut_rows=[];regression=[];conditional=[];region_rows=[];abc=[];zone_rows=[];region_zone=[];audit=[]
    field_tables={};group_event_rows=[];cov_cluster=[]
    for period in PERIODS:
        for pol in ['PM10','PM25']:
            d=raw[pol,period];group_ids=d['groups'].tolist();primary_idx=[group_ids.index(g) for g in PRIMARY]
            sg,union,eligible_union,es=networks[pol];e=cells[pol+'_density_tpy_km2'].to_numpy();mass=cells[pol+'_mass_tpy'].to_numpy();tables=[]
            for di,direction in enumerate(DIRS):
                print('Análise espacial',pol,period,direction,flush=True)
                c=d['concentrations'][di];q,cuts=relative_quintile(c);lv=np.log1p(c)
                lisa=local_moran(lv,ids);biv=local_moran(lv,ids,np.log1p(e));global_i=moran(lv,w)
                f=pd.DataFrame({'receptor_id':cells.receptor_id,'X':cells.X,'Y':cells.Y,'pollutant':pol,'period':period,'direction':direction,'concentration':c,'event_code':d['codes'][di],
                                'quintile':q,'lisa':lisa.cluster,'local_I':lisa.local_I,'p_local':lisa.p_conditional,'q_local':lisa.q_FDR,
                                'bivariate':biv.cluster,'p_bivariate':biv.p_conditional,'q_bivariate':biv.q_FDR})
                ecut=np.array([binary_cut(e,c>cut) for cut in cuts]);ordered=bool(np.isfinite(ecut).all() and (np.diff(ecut)>0).all())
                eq=np.searchsorted(ecut,e,side='left')+1 if ordered else relative_quintile(e)[0]
                e80=ecut[3] if np.isfinite(ecut[3]) else np.quantile(e,.8)
                matrix=np.where(q==5,'Alta C','Demais C')+' / '+np.where(e>e80,'Alta E','Demais E')
                f['emission_band']=eq;f['matrix']=matrix;f['emission_density']=e;f['mass_tpy']=mass
                f['emission_band_basis']='cortes associativos ordenados' if ordered else 'quintis independentes da densidade; cinco cortes associativos não identificáveis'
                f['five_emission_bands_identifiable']=ordered

                e40=ecut[1] if np.isfinite(ecut[1]) else np.quantile(e,.4)
                role=np.full(n,'Acompanhamento',object);role[(q<=2)&(e<=e40)]='Menor impacto relativo';role[(q<5)&(e>e80)]='Controle de fontes';role[q==5]='Prioridade receptora'
                f['management']=role;f['best_cluster']=joint[direction][0];f['ward4']=joint[direction][1]
                event=d['group_values'][di][:,primary_idx]
                f['dominant_group']=np.array(PRIMARY)[event.argmax(axis=1)]
                for j,group in enumerate(PRIMARY):f['C_'+group]=event[:,j]
                for label,k in [('p20',0),('p40',1),('p60',2),('p80',3)]:f[label]=cuts[k]
                for basis,x in [('density_tpy_km2',e),('mass_tpy',mass)]:
                    cut_rows.extend(dict(period=period,direction=direction,**r) for r in estimate_cuts(x,c,xy,pol,basis))
                    regression.extend(dict(period=period,direction=direction,**r) for r in thresholds(x,c,xy,pol,basis))
                    for band in range(1,6):
                        v=x[q==band]
                        if len(v):conditional.append(dict(pollutant=pol,period=period,direction=direction,quintile=band,basis=basis,n=len(v),min=v.min(),p20=np.quantile(v,.2),median=np.median(v),p80=np.quantile(v,.8),max=v.max()))
                for k,ii in neighbors.items():
                    ss=local_moran(lv,ii,seed=SEED+k);a=lisa.cluster.eq('Alto–alto').to_numpy();b=ss.cluster.eq('Alto–alto').to_numpy()
                    stability.append(dict(pollutant=pol,period=period,direction=direction,comparison=f'LISA k8 vs k{k}',ARI=ari(lisa.cluster,ss.cluster),HH_jaccard=(a&b).sum()/(a|b).sum() if (a|b).any() else 1))
                for year_i,year in enumerate([2021,2022,2023]):
                    yc=d['yearly'][year_i,di]
                    if not np.isfinite(yc).all():
                        stability.append(dict(pollutant=pol,period=period,direction=direction,comparison=f'Envelope {year}',n_eligible=d['counts'][year_i,di],status='Sem horas/dias da direção neste ano'));continue
                    yrank,_=relative_quintile(yc);fixed=np.searchsorted(cuts,yc,side='left')+1
                    stability.append(dict(pollutant=pol,period=period,direction=direction,comparison=f'Quintis recalculados {year}',ARI=ari(q,yrank),n_eligible=d['counts'][year_i,di],pct_same_fixed_cut=float((fixed==q).mean()*100)))
                for dx,dy,index,unsupported in support:
                    _,cc=relative_quintile(c[index]);lab=np.searchsorted(cc,c,side='left')+1
                    stability.append(dict(pollutant=pol,period=period,direction=direction,comparison=f'Reamostragem suporte {dx}/{dy} m',ARI=ari(q,lab),supported_targets=len(index),unsupported_targets=unsupported,p80=cc[3]))
                for upper,wc,pairs,isolates in band_weights:
                    corr.append(dict(pollutant=pol,period=period,direction=direction,min_distance_m=upper-750,max_distance_m=upper,directed_pairs=pairs,isolates=isolates,**moran(lv,wc,199,seed=SEED+upper)))
                spatial=cells[['receptor_id','geometry']].merge(f,on='receptor_id',validate='one_to_one')
                spatial['network_priority']='Demais áreas'
                for kind,field in [('gestao','management'),('LISA','lisa'),('perfil','best_cluster')]:
                    subset=spatial[spatial.lisa.ne('Não significativo')] if kind=='LISA' else spatial
                    for label,j,g in partition(subset,field):
                        geom=g.geometry.union_all();area=g.area.to_numpy();total=float(np.average(g.concentration,weights=area));area_total=geom.area
                        covered=100*geom.intersection(union).area/area_total;cov_eligible=100*geom.intersection(eligible_union).area/area_total
                        rid=f'{pol}_{period}_{direction}_{kind}_{str(label).replace(" ","").replace("–","-")}_{j:02d}'
                        record=dict(region_id=rid,pollutant=pol,period=period,direction=direction,region_type=kind,label=str(label),n_receptors=len(g),area_km2=area_total/1e6,concentration_area_mean=total,
                                    monitored_area_pct=covered,eligible_monitored_area_pct=cov_eligible,
                                    stations_intersecting=';'.join(sg.loc[sg.buffer(config.REPRESENTATIVITY_RADIUS_M).intersects(geom),'station_id']),
                                    expansion_candidate=bool(kind=='gestao' and label in ['Prioridade receptora','Controle de fontes'] and cov_eligible<50),geometry=geom)
                        region_rows.append(record)
                        if kind=='gestao' and label=='Prioridade receptora':
                            spatial.loc[spatial.receptor_id.isin(g.receptor_id),'network_priority']='Prioridade: cobertura ≥50%' if cov_eligible>=50 else 'Prioridade: cobertura <50%'
                        cumulative=0.
                        values=[(group,float(np.average(g['C_'+group],weights=area))) for group in PRIMARY]
                        for group,val in sorted(values,key=lambda v:-v[1]):
                            share=100*val/total if total>0 else np.nan
                            cls=('A' if cumulative<80 else 'B' if cumulative<95 else 'C') if ((kind=='gestao' and label=='Prioridade receptora') or (kind=='LISA' and label=='Alto–alto')) else None
                            abc.append(dict(region_id=rid,pollutant=pol,period=period,direction=direction,region_type=kind,label=str(label),group_id=group,group_name=GROUPS[group]['name'],contribution=val,share_pct=share,cumulative_before_pct=cumulative,ABC=cls))
                            cumulative+=share
                        overlaps=z.geometry.intersection(geom).area
                        for zi,a in zip(z.zone_index[overlaps>0],overlaps[overlaps>0]):
                            region_zone.append(dict(region_id=rid,zone_index=int(zi),area_m2=float(a)))
                f['network_priority']=spatial['network_priority'].to_numpy()
                ll=links.merge(f.drop(columns=['X','Y']),on='receptor_id',validate='many_to_one')
                for zid,zz in ll.groupby('zone_index'):
                    weights_zone=zz.zone_area_fraction.to_numpy()
                    rec=dict(pollutant=pol,period=period,direction=direction,zone_index=int(zid),concentration_area_mean=np.average(zz.concentration,weights=weights_zone),
                             dominant_group=PRIMARY[int(np.argmax([np.average(zz['C_'+g],weights=weights_zone) for g in PRIMARY]))])
                    for v in range(1,6):rec[f'Q{v}_area_pct']=100*weights_zone[zz.quintile.eq(v)].sum()
                    for label in ['Alto–alto','Alto–baixo','Baixo–alto','Baixo–baixo','Não significativo']:rec['LISA_'+label+'_pct']=100*weights_zone[zz.lisa.eq(label)].sum()
                    for label in ROLES:rec['management_'+label+'_pct']=100*weights_zone[zz.management.eq(label)].sum()
                    zone_rows.append(rec)
                for gj,group in enumerate(group_ids):
                    group_event_rows.append(pd.DataFrame(dict(pollutant=pol,period=period,direction=direction,receptor_id=cells.receptor_id,group_id=group,concentration_at_ALL_event=d['group_values'][di,:,gj],ALL_event_code=d['codes'][di])))
                summary=dict(pollutant=pol,period=period,direction=direction,n_receptors=n,concentration_cuts=cuts.tolist(),emission_cuts=ecut.tolist(),five_emission_bands_identifiable=ordered,
                             lisa_counts=lisa.cluster.value_counts().to_dict(),management_counts=pd.Series(role).value_counts().to_dict(),
                             global_moran=global_i,max_concentration=float(c.max()),n_hours_or_days_by_year=d['counts'][:,di].tolist(),clustering_joint_1h_24h=joint[direction][2],
                             group_closure_max_abs=float(np.abs(event.sum(1)-c).max()))
                if general:summary['clustering_joint_1h_24h_anual']=summary.pop('clustering_joint_1h_24h')
                rows.append(summary);tables.append(f)
            table=pd.concat(tables,ignore_index=True)
            table['q_local_family_8_directions' if not general else 'q_local_family_scenario']=bh(table.p_local)
            table['q_bivariate_family_8_directions' if not general else 'q_bivariate_family_scenario']=bh(table.p_bivariate)
            table.to_csv(OUT/f'{pol}_{period}_receptores.csv',index=False);field_tables[pol,period]=table
            audit.append(dict(pollutant=pol,period=period,rows=len(table),all_fields_classified=bool(table.quintile.between(1,5).all()),field_FDR='BH nominal por mapa',additional_family_FDR='BH nos campos do mesmo poluente e duração'))
    pd.DataFrame(corr).to_csv(OUT/'correlogramas.csv',index=False);pd.DataFrame(stability).to_csv(OUT/'sensibilidade_espacial.csv',index=False)
    pd.DataFrame(cut_rows).to_csv(OUT/'limiares_cinco_faixas.csv',index=False);pd.DataFrame(regression).to_csv(OUT/'limiares_regressao_complementar.csv',index=False)
    pd.DataFrame(conditional).to_csv(OUT/'distribuicoes_emissao_por_faixa.csv',index=False)
    region_frame=gpd.GeoDataFrame(region_rows,crs=cells.crs)
    target=OUT/(region_stem+'.gpkg')
    if target.exists():target.unlink()
    region_frame.to_file(target,driver='GPKG');region_frame.drop(columns='geometry').to_csv(OUT/(region_stem+'.csv'),index=False)
    pd.DataFrame(abc).to_csv(OUT/'ABC_contribuicoes_regioes.csv',index=False);pd.DataFrame(region_zone).to_csv(OUT/'regioes_zoneamento.csv',index=False)
    zones=pd.DataFrame(zone_rows);zones.to_csv(OUT/(zone_stem+'.csv'),index=False)
    pd.concat(group_event_rows,ignore_index=True).to_csv(OUT/'contribuicoes_receptores_no_evento_ALL.csv.gz',index=False,compression='gzip')
    assert zones.groupby(['pollutant','period','direction']).zone_index.nunique().eq(311).all()
    assert np.allclose(zones[[f'Q{i}_area_pct' for i in range(1,6)]].sum(axis=1),100)
    contrib=pd.DataFrame(abc);sums=contrib.groupby('region_id').share_pct.sum();assert np.allclose(sums,100,atol=.01)
    dump(OUT/'resumo.json',dict(cases=rows,audit=audit,source_contribution='Mesmo evento ALL para 1h/24h; médias nativas dos três anos para anual' if general else 'Mesmo horário/dia do máximo ALL em cada receptor; máximo não simultâneo',emission_basis='Massa anual inventariada estática; não massa emitida no evento',cluster_features=feature_description+', log1p e padronização por variável',network_radius_m=config.REPRESENTATIVITY_RADIUS_M,network_period='2021-2023',inputs_preserved=True,new_simulation=False))
    print(f'Análises de {len(rows)} campos concluídas; 311 zonas em cada campo.',flush=True)

if __name__=='__main__':run()
