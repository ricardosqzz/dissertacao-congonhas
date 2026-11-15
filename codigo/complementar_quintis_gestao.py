# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/projeto/output/16_revisao_pos_banca/celulas_analise.gpkg | gpd.read_file.
# Entrada: E:/projeto/output/16_revisao_pos_banca/zoneamento_pos_banca.gpkg | gpd.read_file.
# Entrada: E:/projeto/output/16_revisao_pos_banca/vinculo_celula_zona.csv | pd.read_csv.
# Campos/chaves em cells: X, Y, receptor_id.
# Campos/chaves em v: kind.
# Campos/chaves em folds_here: basis, pollutant.
# Campos/chaves em links: receptor_id, zone_area_fraction, zone_index.
# Campos/chaves em z: zone_index.
# Saída: E:/projeto/output/16_revisao_pos_banca/{name}.gpkg | frame.to_file.
# Saída: E:/projeto/output/16_revisao_pos_banca/{name}.csv | .to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/limiares_cinco_faixas_validacao.csv | .to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/emissoes_por_faixa_concentracao.csv | .to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/ABC_regioes_gestao.csv | .to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/regioes_gestao_zoneamento.csv | .to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/resumo_quintis_gestao.json | .write_text.
# receptor_id: identificador do receptor.
# X: coordenada leste em metros.
# Y: coordenada norte em metros.
# CÓDIGO DO PROCESSAMENTO

"""Cinco faixas descritivas, cortes associativos testados e regiões de gestão."""
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

import json
import numpy as np
import pandas as pd
import geopandas as gpd
from scipy import sparse
from scipy.sparse.csgraph import connected_components
from revisao_espacial_pos_banca import relative_quintile,SEED
from groups import GROUPS
import config
ROOT=config.BASE/'output/16_revisao_pos_banca'

# Binary cut
def binary_cut(x,y):
    """Limiar crescente que maximiza a acurácia balanceada, sem causalidade."""
    x=np.asarray(x,float);y=np.asarray(y,bool);order=np.argsort(x,kind='stable');sx=x[order];sy=y[order];p=sy.sum();n=len(y)-p
    if min(p,n)==0 or np.unique(x).size<2:return np.nan
    cumulative=sy.cumsum()[:-1];j=np.arange(1,len(x));tn=j-cumulative;tp=p-cumulative;score=.5*(tp/p+tn/n)
    allowed=(sx[:-1]<sx[1:])&(j>=max(5,int(.05*len(x))))&(len(x)-j>=max(5,int(.05*len(x))))
    score[~allowed]=-np.inf
    if not np.isfinite(score).any():return np.nan
    idx=int(score.argmax());return float((sx[idx]+sx[idx+1])/2)

# Balanced accuracy
def balanced_accuracy(y,pred):
    y=np.asarray(y,bool);pred=np.asarray(pred,bool)
    return float(.5*(pred[y].mean()+(~pred[~y]).mean())) if y.any() and (~y).any() else np.nan

# Estimate cuts
def estimate_cuts(x,c,xy,pol,basis):
    concentration_cuts=np.quantile(c,[.2,.4,.6,.8]);rows=[];folds=[]
    for size in [2000,4000]:
        b=np.floor((xy-xy.min(0))/size).astype(int);keys=list(map(tuple,b));unique=sorted(set(keys));np.random.default_rng(SEED).shuffle(unique);lookup={key:i%5 for i,key in enumerate(unique)};folds.append((size,np.array([lookup[v] for v in keys])))
    for percentile,ccut in zip([20,40,60,80],concentration_cuts):
        y=c>ccut;cut=binary_cut(x,y)
        for size,f in folds:
            for fold in range(5):
                test=f==fold;train=~test;fit=binary_cut(x[train],y[train]);ba=balanced_accuracy(y[test],x[test]>fit) if np.isfinite(fit) else np.nan
                rows.append({'pollutant':pol,'basis':basis,'percentile_target':percentile,'concentration_cut':ccut,'cut_all_data':cut,'block_m':size,'fold':fold,'cut_train':fit,'balanced_accuracy_test':ba,'n_train':int(train.sum()),'n_test':int(test.sum())})
    return rows

# Run
def run():
    cells=gpd.read_file(ROOT/'celulas_analise.gpkg');z=gpd.read_file(ROOT/'zoneamento_pos_banca.gpkg');links=pd.read_csv(ROOT/'vinculo_celula_zona.csv');xy=cells[['X','Y']].to_numpy();results=[];conditional=[];summary={};regions=[];contrib=[];region_links=[]
    primary=[k for k,v in GROUPS.items() if v['kind']=='primary']
    for pol in ['PM10','PM25']:
        c=cells[pol+'_annual'].to_numpy();q,ccuts=relative_quintile(c);cells[pol+'_quintile']=q
        for basis,column in [('mass_tpy',pol+'_mass_tpy'),('density_tpy_km2',pol+'_density_tpy_km2')]:
            x=cells[column].to_numpy();results.extend(estimate_cuts(x,c,xy,pol,basis))
            for i in range(1,6):
                vals=x[q==i];conditional.append({'pollutant':pol,'basis':basis,'concentration_band':i,'n':len(vals),'emission_min':vals.min(),'emission_p20':np.quantile(vals,.2),'emission_median':np.median(vals),'emission_p80':np.quantile(vals,.8),'emission_max':vals.max(),'concentration_low':float(c[q==i].min()),'concentration_high':float(c[q==i].max())})
        e=cells[pol+'_density_tpy_km2'].to_numpy();cuts=np.array([binary_cut(e,c>v) for v in ccuts]);ordered=bool(np.isfinite(cuts).all() and np.all(np.diff(cuts)>0))
        cells[pol+'_emission_associated_band']=np.searchsorted(cuts,e,side='left')+1 if ordered else np.nan
        eq_rank,ecuts=relative_quintile(e);eq=(cells[pol+'_emission_associated_band'].to_numpy().astype(int) if ordered else eq_rank);cells[pol+'_emission_rank_quintile']=eq_rank;cells[pol+'_emission_q']=eq

        e80=cuts[-1];cells[pol+'_matrix_associative']=np.where(q==5,'Alta C','Demais C')+' / '+np.where(e>e80,'Alta E','Demais E')
        cells[pol+'_matrix']=np.where(q==5,'Alta C','Demais C')+' / '+np.where(eq==5,'Alta E','Demais E')
        labels=np.full(len(cells),'Acompanhamento',dtype=object);labels[(q<=2)&(eq<=2)]='Menor impacto relativo';labels[(eq==5)&(q<5)]='Controle de fontes';labels[q==5]='Prioridade receptora'
        cells[pol+'_management']=labels

        cells[pol+'_priority_LISA_confirmed']=(q==5)&cells[pol+'_lisa'].eq('Alto–alto').to_numpy()
        for label,code in [('Prioridade receptora','PRI'),('Controle de fontes','CON'),('Menor impacto relativo','MEN'),('Acompanhamento','ACO')]:
            sub=cells[cells[pol+'_management'].eq(label)].copy().reset_index(drop=True)
            if sub.empty:continue
            pairs=sub.sindex.query(sub.geometry,predicate='touches');keep=[]
            for a,b in pairs.T:
                if a!=b and sub.geometry.iloc[a].boundary.intersection(sub.geometry.iloc[b].boundary).length>.01:keep.append((a,b))
            pairs2=np.array(keep).T if keep else np.zeros((2,0),int);adj=sparse.coo_matrix((np.ones(pairs2.shape[1]),pairs2),shape=(len(sub),len(sub)));n,lab=connected_components(adj,directed=False)
            order=sorted(range(n),key=lambda k:(sub[lab==k].geometry.union_all().centroid.x,sub[lab==k].geometry.union_all().centroid.y))
            for j,k in enumerate(order,1):
                g=sub[lab==k];geom=g.geometry.union_all();area=g.area.to_numpy();mean=float(np.average(g[pol+'_annual'],weights=area));rid=f'{pol}_{code}_{j:02d}'
                regions.append({'region_id':rid,'pollutant':pol,'management_class':label,'n_receptors':len(g),'area_km2':geom.area/1e6,'annual_area_mean':mean,'lisa_hh_area_pct':100*float(g.loc[g[pol+'_lisa'].eq('Alto–alto')].area.sum())/geom.area,'geometry':geom})
                cum=0.;values=[(key,float(np.average(g[pol+'_annual']*g[pol+'_share_'+key]/100,weights=area))) for key in primary]
                assert np.isclose(sum(v for _,v in values),mean,rtol=3e-5)
                for key,value in sorted(values,key=lambda t:-t[1]):
                    share=100*value/mean;abc=('A' if cum<80 else 'B' if cum<95 else 'C') if code=='PRI' else None
                    contrib.append({'region_id':rid,'pollutant':pol,'management_class':label,'group_id':key,'group_name':GROUPS[key]['name'],'annual_contribution':value,'share_pct':share,'cumulative_before_pct':cum,'ABC':abc});cum+=share
                for row in z.itertuples():
                    a=row.geometry.intersection(geom).area
                    if a>0:region_links.append({'region_id':rid,'pollutant':pol,'zone_index':row.zone_index,'area_m2':a,'zone_area_pct':100*a/row.geometry.area})
        folds_here=pd.DataFrame(results);folds_here=folds_here[folds_here.pollutant.eq(pol)&folds_here.basis.eq('density_tpy_km2')]
        summary[pol]={'concentration_cuts_P20_P40_P60_P80':ccuts.tolist(),'emission_density_quintile_cuts':ecuts.tolist(),'candidate_associated_emission_cuts':cuts.tolist(),'five_emission_bands_identifiable':ordered,'matrix_basis':'C acima de P80 e E acima do corte associativo para P80; cortes exploratórios' if ordered else 'P80 de C e P80 da densidade de E, independentes; cortes associativos não ordenados','balanced_accuracy_by_target':folds_here.groupby('percentile_target').balanced_accuracy_test.mean().to_dict(),'management_counts':pd.Series(labels).value_counts().to_dict(),'priority_confirmed_HH':int(cells[pol+'_priority_LISA_confirmed'].sum())}
        ll=links[['zone_index','receptor_id','zone_area_fraction']].merge(cells[['receptor_id',pol+'_management',pol+'_matrix_associative']],on='receptor_id',validate='many_to_one')
        for label in np.unique(labels):z[pol+'_management_'+{'Prioridade receptora':'PRI','Controle de fontes':'CON','Menor impacto relativo':'MEN','Acompanhamento':'ACO'}[label]+'_pct']=100*z.zone_index.map(ll[ll[pol+'_management'].eq(label)].groupby('zone_index').zone_area_fraction.sum()).fillna(0)
    for name,frame in [('celulas_analise',cells),('zoneamento_pos_banca',z),('regioes_gestao',gpd.GeoDataFrame(regions,crs=cells.crs))]:
        path=ROOT/f'{name}.gpkg'
        if path.exists():path.unlink()
        frame.to_file(path,driver='GPKG');frame.drop(columns='geometry').to_csv(ROOT/f'{name}.csv',index=False)
    pd.DataFrame(results).to_csv(ROOT/'limiares_cinco_faixas_validacao.csv',index=False);pd.DataFrame(conditional).to_csv(ROOT/'emissoes_por_faixa_concentracao.csv',index=False);pd.DataFrame(contrib).to_csv(ROOT/'ABC_regioes_gestao.csv',index=False);pd.DataFrame(region_links).to_csv(ROOT/'regioes_gestao_zoneamento.csv',index=False)
    (ROOT/'resumo_quintis_gestao.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps(summary,ensure_ascii=False),flush=True)

if __name__=='__main__':run()
