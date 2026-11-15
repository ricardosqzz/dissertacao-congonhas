# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/projeto/output/13_rateio_emissoes/fontes_rateio_{pol}.gpkg | gpd.read_file.
# Entrada: E:/projeto/output/11_integracao/nova_modelagem/zoneamento_nova_modelagem.gpkg | gpd.read_file.
# Entrada: E:/projeto/output/11_integracao/nova_modelagem/{pol}_indicadores_trienais_receptores.csv | pd.read_csv.
# Entrada: E:/projeto/output/11_integracao/nova_modelagem/{pol}_indicadores_trienais_receptores.csv | path.read_bytes.
# Entrada: E:/projeto/output/11_integracao/nova_modelagem/PM10_indicadores_trienais_receptores.csv | pd.read_csv.
# Entrada: E:/projeto/output/11_integracao/nova_modelagem/{pol}_fechamento_receptores.csv | pd.read_csv.
# Entrada: E:/projeto/output/11_integracao/nova_modelagem/{pol}_receptores_anuais.csv | pd.read_csv.
# Campos/chaves em v: kind.
# Campos/chaves em cells: geometry, receptor_id.
# Campos/chaves em d: ANNUAL_MODEL, P98_MODEL, X, Y.
# Campos/chaves em points: PM25_annual, X, Y, receptor_id.
# Campos/chaves em stats: pols.
# Campos/chaves em r: silhouette.
# Campos/chaves em best: k, method.
# Campos/chaves em a: year.
# Campos/chaves em z: geometry, zone_index.
# Campos/chaves em z.loc: zone_index.
# Saída: {path} | path.write_text.
# Saída: E:/projeto/output/16_revisao_pos_banca/{pol}_fontes_celulas.csv | .to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/{pol}_lisa_receptores.csv | .to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/{pol}_lisa_bivariado.csv | .to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/{name}.gpkg | frame.to_file.
# Saída: E:/projeto/output/16_revisao_pos_banca/{name}.csv | .to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/vinculo_celula_zona.csv | links.to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/correlogramas.csv | .to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/sensibilidade_espacial.csv | .to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/comparacao_agrupamentos.csv | .to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/limiares_associativos_validacao_espacial.csv | .to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/contribuicoes_regioes.csv | .to_csv.
# Campos/chaves gerados em points: cluster_profile, receptor_id.
# Campos/chaves gerados em stats: cell_area_conservation_relative_error, clustering_selection, geometric_fragments, k8_distance_m, zone_coverage, zone_quintile_area_sums.
# Campos/chaves gerados em inter: area_m2, support_method, zone_area_fraction.
# Campos/chaves gerados em z: fragmento_menor_1m2.
# receptor_id: identificador do receptor.
# X: coordenada leste em metros.
# Y: coordenada norte em metros.
# Novas variáveis: config/analise_extensivel.json; definir origem, campo, agregação, transformação e peso.
# CÓDIGO DO PROCESSAMENTO

"""Análise exploratória pós-banca, independente dos produtos de seminários.

Saídas não substituem o cenário AERMOD nem a classificação normativa.
Moran local usa permutação condicional bilateral e FDR por campo analisado.
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
import json,hashlib,math,sys
import numpy as np
import pandas as pd
import geopandas as gpd
from scipy import sparse
from scipy.spatial import cKDTree,distance
from scipy.cluster.hierarchy import linkage,fcluster
from scipy.cluster.vq import kmeans2
from scipy.sparse.csgraph import connected_components
from shapely import MultiPoint,voronoi_polygons,make_valid
from shapely.geometry import Point
import config
from groups import GROUPS

BASE=config.BASE;SRC=BASE/'output/11_integracao/nova_modelagem'
OUT=BASE/'output/16_revisao_pos_banca';SEED=20261105
PRIMARY=[k for k,v in GROUPS.items() if v['kind']=='primary']
POLLS=['PM10','PM25']

# Save json
def save_json(path,data):
 path.write_text(json.dumps(data,ensure_ascii=False,indent=2,default=lambda v:v.item() if isinstance(v,np.generic) else str(v)),encoding='utf8')

# Bh
def bh(p):
 p=np.asarray(p,float);order=np.argsort(p);q=np.minimum.accumulate((p[order]*len(p)/np.arange(1,len(p)+1))[::-1])[::-1]
 out=np.empty_like(q);out[order]=np.minimum(q,1);return out

# Weights
def weights(xy,k):
 n=len(xy);dist,ids=cKDTree(xy).query(xy,k=min(k+1,n));ids=ids[:,1:];dist=dist[:,1:]
 w=sparse.csr_matrix((np.full(ids.size,1/ids.shape[1]),(np.repeat(np.arange(n),ids.shape[1]),ids.ravel())),shape=(n,n))
 return w,ids,dist

# Moran
def moran(z,w,permutations=999,seed=SEED):
 z=np.asarray(z,float)-np.mean(z);n=len(z);den=z@z;scale=n/w.sum()
 observed=float(scale*(z@(w@z))/den);rng=np.random.default_rng(seed);sim=[]
 for _ in range(permutations):
  q=rng.permutation(z);sim.append(float(scale*(q@(w@q))/den))
 sim=np.asarray(sim);expected=-1/(n-1)
 p=(1+np.count_nonzero(np.abs(sim-expected)>=abs(observed-expected)))/(permutations+1)
 return {'I':observed,'expected':expected,'p_two_sided':p,'permutations':permutations}

# Local moran
def local_moran(x,ids,y=None,permutations=999,seed=SEED):
 """Igual peso nos k vizinhos. Bivariado: X_i versus média de Y_j."""
 x=np.asarray(x,float);z=(x-x.mean())/x.std(ddof=1);n=len(z);k=ids.shape[1]
 zy=z if y is None else (np.asarray(y,float)-np.mean(y))/np.std(y,ddof=1)
 lag=zy[ids].mean(axis=1);stat=z*lag;rng=np.random.default_rng(seed);p=np.empty(n)
 for i in range(n):

  draws=rng.integers(0,n-1,size=(permutations,k))
  bad=np.any(np.diff(np.sort(draws,axis=1),axis=1)==0,axis=1)
  while bad.any():
   draws[bad]=rng.integers(0,n-1,size=(int(bad.sum()),k));bad=np.any(np.diff(np.sort(draws,axis=1),axis=1)==0,axis=1)
  draws+=draws>=i;sim=z[i]*zy[draws].mean(axis=1)
  expect=-z[i]*zy[i]/(n-1)
  p[i]=(1+np.count_nonzero(np.abs(sim-expect)>=abs(stat[i]-expect)))/(permutations+1)
 q=bh(p);quad=np.where(z>=0,np.where(lag>=0,'Alto–alto','Alto–baixo'),np.where(lag>=0,'Baixo–alto','Baixo–baixo'))
 return pd.DataFrame({'local_I':stat,'p_conditional':p,'q_FDR':q,'z':z,'spatial_lag':lag,'quadrant':quad,'cluster':np.where(q<=.05,quad,'Não significativo')})

# Silhouette
def silhouette(x,labels):
 d=distance.cdist(x,x);classes=np.unique(labels);s=[]
 for i,label in enumerate(labels):
  same=labels==label;n=same.sum()
  if n<=1:s.append(0.);continue
  a=d[i,same].sum()/(n-1);b=min(d[i,labels==c].mean() for c in classes if c!=label)
  s.append((b-a)/max(a,b) if max(a,b)>0 else 0.)
 return float(np.mean(s))

# Ari
def ari(a,b):
 a=np.unique(a,return_inverse=True)[1];b=np.unique(b,return_inverse=True)[1];t=np.zeros((a.max()+1,b.max()+1));np.add.at(t,(a,b),1)
 c=lambda v:np.sum(v*(v-1)/2)
 n=len(a);total=n*(n-1)/2;s=c(t);expected=c(t.sum(0))*c(t.sum(1))/total;mx=(c(t.sum(0))+c(t.sum(1)))/2
 return float((s-expected)/(mx-expected)) if mx>expected else 1.

# Relative quartile
def relative_quartile(v):
 q=np.quantile(v,[.25,.5,.75]);return np.searchsorted(q,np.asarray(v),side='left')+1,q

# Relative quintile
def relative_quintile(v):
 """Cinco faixas P20/P40/P60/P80; empates permanecem juntos."""
 q=np.quantile(v,[.2,.4,.6,.8]);return np.searchsorted(q,np.asarray(v),side='left')+1,q

# Cells for
def cells_for(points,municipality):
 parts=voronoi_polygons(MultiPoint(points.geometry.to_list()),extend_to=municipality.envelope,ordered=True)
 cells=gpd.GeoDataFrame({'receptor_id':points.receptor_id.to_numpy()},geometry=[v.intersection(municipality) for v in parts.geoms],crs=config.CRS_PROJECT)
 cells.geometry=make_valid(cells.geometry);assert len(cells)==len(points) and cells.area.gt(0).all()
 assert abs(cells.area.sum()-municipality.area)/municipality.area<1e-7
 return cells

# Emission allocation
def emission_allocation(cells,municipality,pol):
 sources=gpd.read_file(BASE/f'output/13_rateio_emissoes/fontes_rateio_{pol}.gpkg').to_crs(cells.crs)
 masses=np.zeros(len(cells));records=[];expected=0.;missing=0
 for r in sources.itertuples():
  geom=make_valid(r.geometry)
  if geom.is_empty or not np.isfinite(r.massa):missing+=1;continue
  mode='area' if geom.area>0 else 'length' if geom.length>0 else 'point'
  denominator=geom.area if mode=='area' else geom.length if mode=='length' else 1
  inside=geom.intersection(municipality)
  fraction=inside.area/denominator if mode=='area' else inside.length/denominator if mode=='length' else float(municipality.covers(geom))
  expected+=r.massa*fraction
  candidates=cells.sindex.query(geom,predicate='intersects')
  if mode=='point' and len(candidates)>1:
   candidates=np.array([min(candidates,key=lambda j:(cells.geometry.iloc[j].representative_point().distance(geom),j))])
  for j in candidates:
   it=geom.intersection(cells.geometry.iloc[j]);f=it.area/denominator if mode=='area' else it.length/denominator if mode=='length' else 1.
   if f<=0:continue
   mass=float(r.massa*f);masses[j]+=mass;records.append({'pollutant':pol,'source_id':r.source_id,'group_id':r.group_id,'source_type':r.source_type,'receptor_id':int(cells.receptor_id.iloc[j]),'fraction':f,'mass_tpy':mass})
 err=abs(masses.sum()-expected);assert err<=max(.001,expected*1e-7),(pol,err,expected)
 pd.DataFrame(records).to_csv(OUT/f'{pol}_fontes_celulas.csv',index=False)
 return masses,{'total_source_mass_tpy':float(sources.massa.sum()),'municipal_mass_expected_tpy':expected,'allocated_mass_tpy':float(masses.sum()),'absolute_error_tpy':err,'sources_missing_geometry_or_mass':missing,'volume_geometry':'Suporte geométrico do cadastro; não área física emissora comprovada.'}

# Stump
def stump(x,y,min_fraction=.1):
 order=np.argsort(x);sx=x[order];sy=y[order];n=len(x);a=np.cumsum(sy);b=np.cumsum(sy*sy);j=np.arange(1,n);minn=max(5,int(n*min_fraction))
 score=(b[:-1]-a[:-1]**2/j)+(b[-1]-b[:-1]-(a[-1]-a[:-1])**2/(n-j));ok=(j>=minn)&(j<=n-minn)&(sx[:-1]<sx[1:]);score[~ok]=np.inf
 if not np.isfinite(score).any():return None
 cut=np.argmin(score);return (float((sx[cut]+sx[cut+1])/2),float(sy[:cut+1].mean()),float(sy[cut+1:].mean()))

# Thresholds
def thresholds(x,y,xy,pol,unit):
 out=[];lx=np.log1p(x);ly=np.log1p(y);fit=stump(lx,ly)
 for size in [2000,4000]:
  blocks=np.floor((xy-xy.min(0))/size).astype(int);keys=[tuple(v) for v in blocks];unique=sorted(set(keys));rng=np.random.default_rng(SEED);rng.shuffle(unique);fold={b:i%5 for i,b in enumerate(unique)};folds=np.array([fold[k] for k in keys])
  for k in range(5):
   test=folds==k;train=~test
   if min(test.sum(),train.sum())<10:continue
   f=stump(lx[train],ly[train]);
   if f is None:continue
   pred=np.where(lx[test]<=f[0],f[1],f[2]);mse=np.mean((pred-ly[test])**2);null=np.mean((ly[train].mean()-ly[test])**2)
   out.append({'pollutant':pol,'emission_basis':unit,'block_m':size,'fold':k,'threshold':np.expm1(f[0]),'threshold_all_data':np.expm1(fit[0]) if fit else np.nan,'skill_vs_mean':1-mse/null if null>0 else np.nan,'rmse_log1p':np.sqrt(mse),'n_train':int(train.sum()),'n_test':int(test.sum()),'low_mean_conc':np.expm1(f[1]),'high_mean_conc':np.expm1(f[2])})
 return out

# Main
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 z=gpd.read_file(SRC/'zoneamento_nova_modelagem.gpkg').to_crs(config.CRS_PROJECT)
 municipality=make_valid(z.geometry.union_all())
 points=None;inputs=[]
 for pol in POLLS:
  path=SRC/f'{pol}_indicadores_trienais_receptores.csv';d=pd.read_csv(path)
  inputs.append({'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'rows':len(d)})
  d=d[['X','Y','ANNUAL_MODEL','P98_MODEL']].rename(columns={'ANNUAL_MODEL':pol+'_annual','P98_MODEL':pol+'_p98'})
  points=d if points is None else points.merge(d,on=['X','Y'],validate='one_to_one')
 points=gpd.GeoDataFrame(points,geometry=gpd.points_from_xy(points.X,points.Y),crs=z.crs)
 points=points[points.geometry.map(municipality.covers)].sort_values(['X','Y']).reset_index(drop=True)
 assert np.isfinite(points.drop(columns='geometry').to_numpy()).all()
 points['receptor_id']=np.arange(1,len(points)+1);xy=points[['X','Y']].to_numpy();n=len(points);cells=cells_for(points,municipality)
 nearest=cKDTree(xy).query(xy,k=2)[0][:,1];print('Receptores municipais',n,'zonas',len(z),flush=True)
 stats={'inputs':inputs,'receptors_municipal':n,'receptors_total':len(pd.read_csv(SRC/'PM10_indicadores_trienais_receptores.csv')),'zones':len(z),'municipality_km2':municipality.area/1e6,'nearest_distance_m':{'min':float(nearest.min()),'median':float(np.median(nearest)),'max':float(nearest.max())},'spatial_support':'Voronoi dos receptores existentes, recortado pela união do zoneamento. Não constitui nova simulação nem grade uniforme.','pols':{}}
 w,ids,wd=weights(xy,8);stats['k8_distance_m']={'median':float(np.median(wd[:,-1])),'max':float(wd[:,-1].max())}
 sens=[];corr=[];threshold_rows=[];group_rows=[];annual={}
 for pol in POLLS:
  print(pol,'emissões e associação espacial',flush=True)
  v=points[pol+'_annual'].to_numpy();lv=np.log1p(v);q,cut=relative_quintile(v);points[pol+'_quintile']=q
  lisa=local_moran(lv,ids);points[pol+'_lisa']=lisa.cluster.to_numpy();points[pol+'_qFDR']=lisa.q_FDR.to_numpy()
  lisa.assign(receptor_id=points.receptor_id).to_csv(OUT/f'{pol}_lisa_receptores.csv',index=False)
  mass,audit=emission_allocation(cells,municipality,pol);points[pol+'_mass_tpy']=mass;points[pol+'_density_tpy_km2']=mass/(cells.area.to_numpy()/1e6)
  bivar=local_moran(lv,ids,np.log1p(points[pol+'_density_tpy_km2']));points[pol+'_bivariate']=bivar.cluster.to_numpy();bivar.assign(receptor_id=points.receptor_id).to_csv(OUT/f'{pol}_lisa_bivariado.csv',index=False)
  eq,ecut=relative_quintile(points[pol+'_density_tpy_km2']);points[pol+'_emission_q']=eq
  points[pol+'_matrix']=np.where(q==5,'Alta C','Demais C')+' / '+np.where(eq==5,'Alta E','Demais E')
  for k in [4,12]:
   _,ii,_=weights(xy,k);ss=local_moran(lv,ii,permutations=999,seed=SEED+k);a=set(np.where(lisa.cluster.eq('Alto–alto'))[0]);b=set(np.where(ss.cluster.eq('Alto–alto'))[0]);sens.append({'pollutant':pol,'comparison':f'LISA k8 vs k{k}','ARI':ari(lisa.cluster,ss.cluster),'HH_jaccard':len(a&b)/len(a|b) if a|b else 1})
  D=distance.cdist(xy,xy)
  for upper in range(750,8250,750):
   keep=(D>upper-750)&(D<=upper);wc=sparse.csr_matrix(keep.astype(float));rs=np.asarray(wc.sum(1)).ravel();wc=sparse.diags(np.divide(1,rs,out=np.zeros_like(rs),where=rs>0))@wc
   if wc.sum()==0:continue
   res=moran(lv,wc,199,seed=SEED+upper);corr.append({'pollutant':pol,'min_distance_m':upper-750,'max_distance_m':upper,'directed_pairs':int(keep.sum()),'isolates':int((rs==0).sum()),**res})
  for col,unit in [(pol+'_mass_tpy','t/ano na célula'),(pol+'_density_tpy_km2','t/ano/km² na célula')]:threshold_rows.extend(thresholds(points[col].to_numpy(),v,xy,pol,unit))
  g=pd.read_csv(SRC/f'{pol}_fechamento_receptores.csv').groupby(['X','Y'])[PRIMARY+['ALL']].mean().reset_index()
  g=points[['receptor_id','X','Y']].merge(g,on=['X','Y'],validate='one_to_one');assert len(g)==n
  closure=float((g[PRIMARY].sum(axis=1)-g.ALL).abs().max());assert np.allclose(g[PRIMARY].sum(axis=1),g.ALL,rtol=2e-5,atol=1e-4)
  for col in PRIMARY:points[pol+'_share_'+col]=100*g[col].to_numpy()/g.ALL.to_numpy()
  points[pol+'_dominant']=g[PRIMARY].idxmax(axis=1).map({k:GROUPS[k]['name'] for k in PRIMARY}).to_numpy()
  crit=lisa.cluster.eq('Alto–alto').to_numpy();areas=cells.area.to_numpy()
  for mask,name in [(crit,'Alto–alto FDR'),(q==5,'Quintil 5'),(np.ones(n,bool),'Município')]:
   for group in PRIMARY:
    weighted=float(np.average(g[group][mask],weights=areas[mask])) if mask.any() else np.nan
    denom=float(np.average(g.ALL[mask],weights=areas[mask])) if mask.any() else np.nan
    group_rows.append({'pollutant':pol,'region':name,'group_id':group,'group_name':GROUPS[group]['name'],'annual_area_weighted':weighted,'share_pct':100*weighted/denom if denom else np.nan,'n_receptors':int(mask.sum())})
  a=pd.read_csv(SRC/f'{pol}_receptores_anuais.csv');annual[pol]=a
  stats['pols'][pol]={'annual_quintiles_ug_m3':cut.tolist(),'emission_density_quintiles':ecut.tolist(),'moran_log_annual':moran(lv,w),'LISA_FDR_counts':lisa.cluster.value_counts().to_dict(),'bivariate_FDR_counts':bivar.cluster.value_counts().to_dict(),'mass_allocation':audit,'source_group_closure_max_abs':closure,'annual_min':float(v.min()),'annual_max':float(v.max())}

 feature_cols=[p+s for p in POLLS for s in ['_annual','_p98']];f=np.log1p(points[feature_cols].to_numpy());f=(f-f.mean(0))/f.std(0);cluster_results=[];labels={}
 tree=linkage(f,method='ward')
 for method in ['ward','kmeans']:
  for k in range(2,7):
   if method=='ward':lab=fcluster(tree,k,criterion='maxclust')-1
   else:
    solutions=[kmeans2(f,k,minit='++',iter=100,rng=np.random.default_rng(SEED+j)) for j in range(10)]
    _,lab=min(solutions,key=lambda a:np.sum((f-a[0][a[1]])**2))

   order=pd.Series(points.PM25_annual.to_numpy()).groupby(lab).mean().sort_values().index;mapping={old:i+1 for i,old in enumerate(order)};lab=np.array([mapping[x] for x in lab]);score=silhouette(f,lab)
   labels[method,k]=lab;points[f'{method}_k{k}']=lab;cluster_results.append({'method':method,'k':k,'silhouette':score,'smallest_cluster':int(pd.Series(lab).value_counts().min())})
 best=max(cluster_results,key=lambda r:r['silhouette']);points['cluster_profile']=labels[best['method'],best['k']];stats['clustering_selection']=best

 for pol in POLLS:
  ref=points[pol+'_quintile'].to_numpy()
  for year in [2021,2022,2023]:
   a=annual[pol];av=points[['X','Y']].merge(a[a.year==year][['X','Y','ANNUAL_MEAN']],on=['X','Y'],validate='one_to_one').ANNUAL_MEAN
   lab,_=relative_quintile(av);sens.append({'pollutant':pol,'comparison':f'Quintis trienais vs {year}','ARI':ari(ref,lab),'HH_jaccard':len(set(np.where(ref==5)[0])&set(np.where(lab==5)[0]))/len(set(np.where(ref==5)[0])|set(np.where(lab==5)[0]))})
  for dx,dy in [(0,0),(250,0),(0,250),(250,250)]:
   xmin,ymin,xmax,ymax=municipality.bounds;xx=np.arange(np.ceil(xmin/500)*500+dx,xmax,500);yy=np.arange(np.ceil(ymin/500)*500+dy,ymax,500)
   target=np.array([(x,y) for x in xx for y in yy if municipality.covers(Point(x,y))]);dist,idx=cKDTree(xy).query(target);supported=dist<=354

   val=points[pol+'_annual'].to_numpy()[idx[supported]];_,qt=relative_quintile(val)
   lab=np.searchsorted(qt,points[pol+'_annual'],side='left')+1
   sens.append({'pollutant':pol,'comparison':f'Reamostragem suporte {dx}/{dy} m','ARI':ari(ref,lab),'supported_targets':int(supported.sum()),'unsupported_targets':int((~supported).sum()),'unique_existing_receptors':len(np.unique(idx[supported])),'p80':float(qt[3]),'new_simulation':False})

 cells=cells.merge(points.drop(columns='geometry'),on='receptor_id',validate='one_to_one')
 inter=gpd.overlay(z[['zone_index','geometry']],cells[['receptor_id','geometry']],how='intersection',keep_geom_type=False);inter=inter[inter.area>0].copy();inter['area_m2']=inter.area;inter['support_method']='Interseção areal'
 missing=z[~z.zone_index.isin(inter.zone_index)]
 fallback=[]
 for r in missing.itertuples():
  if r.geometry.area>=1:raise ValueError(f'Zona de área relevante sem suporte: {r.zone_index}')
  j=int(np.argmin([r.geometry.distance(p) for p in points.geometry]));fallback.append({'zone_index':r.zone_index,'receptor_id':int(points.receptor_id.iloc[j]),'geometry':r.geometry,'area_m2':r.geometry.area,'support_method':'Fragmento geométrico sem interseção estável; receptor mais próximo'})
 if fallback:inter=pd.concat([inter,gpd.GeoDataFrame(fallback,crs=z.crs)],ignore_index=True)
 z['fragmento_menor_1m2']=z.area<1
 stats['geometric_fragments']={'below_0_01_m2':int((z.area<.01).sum()),'below_1_m2':int((z.area<1).sum()),'ids_below_1_m2':z.loc[z.area<1,'zone_index'].astype(int).tolist(),'fallback_zone_ids':missing.zone_index.astype(int).tolist(),'interpretation':'IDs preservados. Fragmentos cartográficos não representam unidades territoriais de dimensão usual e exigem conferência do cadastro original.'}
 zonetotal=inter.groupby('zone_index').area_m2.sum();inter['zone_area_fraction']=inter.area_m2/inter.zone_index.map(zonetotal)
 links=inter.drop(columns='geometry').merge(points.drop(columns='geometry'),on='receptor_id',validate='many_to_one');assert z.zone_index.isin(links.zone_index).all()
 for pol in POLLS:
  for q in [1,2,3,4,5]:z[f'{pol}_Q{q}_area_pct']=z.zone_index.map(links[links[pol+'_quintile'].eq(q)].groupby('zone_index').zone_area_fraction.sum()).fillna(0)*100
  for label,short in [('Alto–alto','HH'),('Baixo–baixo','LL'),('Alto–baixo','HL'),('Baixo–alto','LH'),('Não significativo','NS')]:z[f'{pol}_LISA_{short}_area_pct']=z.zone_index.map(links[links[pol+'_lisa'].eq(label)].groupby('zone_index').zone_area_fraction.sum()).fillna(0)*100
  z[pol+'_annual_area_mean']=z.zone_index.map((links[pol+'_annual']*links.zone_area_fraction).groupby(links.zone_index).sum())
  for group in PRIMARY:
   weighted_cg=(links[pol+'_annual']*links[pol+'_share_'+group]/100*links.zone_area_fraction).groupby(links.zone_index).sum()
   z[pol+'_share_'+group]=100*z.zone_index.map(weighted_cg)/z[pol+'_annual_area_mean']
  z[pol+'_relative_label']=z[[f'{pol}_Q{q}_area_pct' for q in range(1,6)]].idxmax(axis=1).str.extract(r'_Q(\d)')[0].map(lambda q:'Quintil '+q)
 for name,frame in [('receptores',points),('celulas_analise',cells),('zoneamento_pos_banca',z)]:
  path=OUT/f'{name}.gpkg'
  if path.exists():path.unlink()
  frame.to_file(path,driver='GPKG');frame.drop(columns='geometry').to_csv(OUT/f'{name}.csv',index=False)
 links.to_csv(OUT/'vinculo_celula_zona.csv',index=False);pd.DataFrame(corr).to_csv(OUT/'correlogramas.csv',index=False);pd.DataFrame(sens).to_csv(OUT/'sensibilidade_espacial.csv',index=False);pd.DataFrame(cluster_results).to_csv(OUT/'comparacao_agrupamentos.csv',index=False);pd.DataFrame(threshold_rows).to_csv(OUT/'limiares_associativos_validacao_espacial.csv',index=False);pd.DataFrame(group_rows).to_csv(OUT/'contribuicoes_regioes.csv',index=False)
 stats['zone_coverage']=len(zonetotal);stats['cell_area_conservation_relative_error']=abs(cells.area.sum()-municipality.area)/municipality.area;stats['zone_quintile_area_sums']={p:float(z[[f'{p}_Q{q}_area_pct' for q in range(1,6)]].sum(axis=1).sub(100).abs().max()) for p in POLLS}
 save_json(OUT/'resumo.json',stats);print(json.dumps({'n':n,'clustering':best,'LISA':{p:stats['pols'][p]['LISA_FDR_counts'] for p in POLLS}},ensure_ascii=False),flush=True)

if __name__=='__main__':main()
