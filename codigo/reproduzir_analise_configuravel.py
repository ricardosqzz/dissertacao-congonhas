# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: caminho(spec['arquivo']) | gpd.read_file.
# Entrada: caminho(spec['arquivo']) | pd.read_csv.
# Entrada: caminho(spec['arquivo']) | rasterio.open.
# Entrada: args.config | .read_text.
# Campos/chaves em spec: arquivo, camada, campo, nome.
# Campos/chaves em support: geometry.
# Campos/chaves em src: geometry.
# Campos/chaves em overlap: _a, _av.
# Campos/chaves em s: _a, _av.
# Campos/chaves em config: base, campo_bacia, cenarios, chaves, inicializacoes, k_testados, normalizacao, saida, semente, suporte_calculo, variaveis.
# Campos/chaves em v: nome.
# Campos/chaves em setting: pesos.
# Campos/chaves em table: cenario.
# Campos/chaves em local: cluster, q.
# Saída: caminho(config['saida'])/analise_configuravel.gpkg | out.to_file.
# Saída: caminho(config['saida'])/indicadores.csv | .to_csv.
# Saída: caminho(config['saida'])/comparacao_k.csv | table.to_csv.
# Saída: caminho(config['saida'])/normalizacao.csv | params.to_csv.
# Saída: caminho(config['saida'])/sensibilidade.csv | .to_csv.
# Saída: caminho(config['saida'])/moran.csv | .to_csv.
# Saída: caminho(config['saida'])/manifesto.json | .write_text.
# Campos/chaves gerados em work: _i.
# Campos/chaves gerados em overlap: _a, _av.
# Campos/chaves gerados em out: completo, estabilidade, q_fdr, r_moran, r_quintil.
# Novas variáveis: config/analise_extensivel.json; definir origem, campo, agregação, transformação e peso.
# CÓDIGO DO PROCESSAMENTO

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
import argparse
import hashlib
import importlib.metadata
import json
import warnings
import numpy as np
import pandas as pd
import geopandas as gpd
import rasterio
from rasterio.features import geometry_mask
from rasterio.windows import from_bounds
from scipy.spatial import distance
from scipy.cluster.vq import kmeans2
from scipy.cluster.hierarchy import linkage,fcluster
from scipy.sparse import csr_matrix
from scipy.optimize import linear_sum_assignment
from scipy.stats import spearmanr
from caminhos_congonhas import caminho
SEED=20261105
PERM=999

# Ler camada
def ler_camada(spec):
    path=caminho(spec['arquivo'])
    return gpd.read_file(path,layer=spec['camada']) if spec.get('camada') else gpd.read_file(path)

# Anexar variavel
def anexar_variavel(base,spec,support):
    origin=spec.get('origem','base');field=spec['campo']
    if origin=='base':
        if field not in base:raise KeyError('Campo ausente: '+field)
        return pd.to_numeric(base[field],errors='coerce').to_numpy()
    aggregation=spec.get('agregacao','por_chave')
    if origin=='tabela':
        src=pd.read_csv(caminho(spec['arquivo']),sep=spec.get('separador',','),dtype=spec.get('tipos'))
    elif origin=='vetor':src=ler_camada(spec).to_crs(base.crs)
    elif origin=='raster':
        if aggregation!='media_raster':raise ValueError('Raster requer agregacao=media_raster')
        with rasterio.open(caminho(spec['arquivo'])) as raster:
            geometries=support.to_crs(raster.crs).geometry;result=[]
            for geometry in geometries:
                win=from_bounds(*geometry.bounds,transform=raster.transform).round_offsets().round_lengths()
                win=win.intersection(rasterio.windows.Window(0,0,raster.width,raster.height))
                a=raster.read(spec.get('banda',1),window=win,masked=True)
                mask=geometry_mask([geometry.__geo_interface__],a.shape,raster.window_transform(win),invert=True)
                values=np.asarray(a.data)[mask&~np.ma.getmaskarray(a)];values=values[np.isfinite(values)]
                result.append(values.mean() if len(values) else np.nan)
            return np.array(result)
    else:raise ValueError('Origem não implementada: '+origin)
    if field not in src:raise KeyError('Campo ausente na nova entrada: '+field)
    if aggregation=='por_chave':
        left=spec.get('chave_base','receptor_id');right=spec.get('chave_origem',left)
        if src.duplicated(right).any():raise ValueError('Chave duplicada em '+spec['arquivo'])
        return pd.to_numeric(base[[left]].merge(src[[right,field]],left_on=left,right_on=right,how='left',validate='many_to_one')[field],errors='coerce').to_numpy()
    if origin!='vetor':raise ValueError('Agregação espacial exige origem=vetor')
    work=support[['geometry']].reset_index(drop=True);work['_i']=np.arange(len(work));src=src[[field,'geometry']].copy()
    if aggregation=='media_area':
        overlap=gpd.overlay(work,src,how='intersection',keep_geom_type=False);overlap['_a']=overlap.area;overlap['_av']=overlap['_a']*pd.to_numeric(overlap[field],errors='coerce')
        overlap=overlap[np.isfinite(overlap['_av'])];s=overlap.groupby('_i')[['_a','_av']].sum();s=s['_av']/s['_a'];return s.reindex(range(len(base))).to_numpy()
    if aggregation=='soma_pontos':
        hit=gpd.sjoin(work,src,how='inner',predicate='intersects');v=hit.groupby('_i')[field].sum();return v.reindex(range(len(base)),fill_value=0).to_numpy()
    raise ValueError('Agregação não implementada: '+aggregation)

# Matriz
def matriz(base,support,config):
    fields=[];columns=[]
    for spec in config['variaveis']:
        values=anexar_variavel(base,spec,support);transform=spec.get('transformacao','identidade')
        if transform=='log1p':
            if np.any(values[np.isfinite(values)]<0):raise ValueError('log1p exige valores não negativos nesta análise')
            values=np.log1p(values)
        elif transform!='identidade':raise ValueError('Transformação desconhecida: '+transform)
        columns.append(values);fields.append(spec['nome'])
    x=np.column_stack(columns);valid=np.isfinite(x).all(axis=1)
    if valid.sum()<8:raise ValueError('Menos de oito registros completos; revisar entradas e lacunas')
    if config['normalizacao']=='minmax':
        center=x[valid].min(0);scale=x[valid].max(0)-center
    elif config['normalizacao']=='zscore':center=x[valid].mean(0);scale=x[valid].std(0)
    else:raise ValueError('Normalização desconhecida')
    norm=(x-center)/np.where(scale>0,scale,1)
    return norm,valid,pd.DataFrame({'variavel':fields,'centro_ou_minimo':center,'escala_ou_amplitude':scale})

# Ari
def ari(a,b):
    _,a=np.unique(a,return_inverse=True);_,b=np.unique(b,return_inverse=True);n=len(a)
    tab=np.bincount(a*(b.max()+1)+b,minlength=(a.max()+1)*(b.max()+1)).reshape(a.max()+1,b.max()+1)
    comb=lambda x:(x*(x-1)/2).sum()
    x=comb(tab);r=comb(tab.sum(0));s=comb(tab.sum(1));e=r*s/(n*(n-1)/2);den=(r+s)/2-e
    return (x-e)/den if den else 1.

# Fitkm
def fitkm(x,k,seed,starts=12):
    best=None
    for r in range(starts):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore');cent,l=kmeans2(x,k,iter=100,minit='++',rng=np.random.default_rng(seed+r))
        if len(np.unique(l))!=k:continue
        loss=np.sum((x-cent[l])**2)
        if best is None or loss<best[0]:best=(loss,cent,l)
    if best is None:raise RuntimeError('K-means sem todos os grupos')
    return best

# Silhouette
def silhouette(x,l):
    d=distance.cdist(x,x);s=[]
    for i,cl in enumerate(l):
        same=l==cl;n=same.sum()
        if n<=1:s.append(0);continue
        a=d[i,same].sum()/(n-1);b=min(d[i,l==k].mean() for k in np.unique(l) if k!=cl)
        s.append((b-a)/max(a,b) if max(a,b) else 0)
    return float(np.mean(s))

# Bh
def bh(p):
    p=np.asarray(p);order=np.argsort(p);q=np.minimum.accumulate((p[order]*len(p)/np.arange(1,len(p)+1))[::-1])[::-1];o=np.empty(len(p));o[order]=np.minimum(q,1);return o

# Align
def align(labels,reference):
 k=max(labels.max(),reference.max())+1;tab=np.bincount(reference*k+labels,minlength=k*k).reshape(k,k)
 rr,cc=linear_sum_assignment(-tab);lookup=dict(zip(cc,rr));return np.array([lookup[v] for v in labels])

# Queen
def queen(g):
 pairs=g.sindex.query(g.geometry,predicate='touches');n=len(g)
 w=csr_matrix((np.ones(pairs.shape[1]),(pairs[0],pairs[1])),shape=(n,n));w=w.maximum(w.T);w.setdiag(0);w.eliminate_zeros();return w

# Moran w
def moran_w(values,w,local=False,seed=SEED):
 good=np.asarray(w.sum(1)).ravel()>0;original=np.flatnonzero(good);w=w[good][:,good].tocsr();v=np.asarray(values)[good];n=len(v)
 if n<4 or v.std()==0:return {'n':n,'isolados':int((~good).sum()),'I':np.nan,'p':np.nan},None,original
 w=w.multiply(1/np.asarray(w.sum(1))).tocsr();z=(v-v.mean())/v.std();lag=w@z;I=float(z@lag/(z@z));expected=-1/(n-1);rng=np.random.default_rng(seed)
 ss=[]
 for _ in range(PERM):zp=rng.permutation(z);ss.append(zp@(w@zp)/(zp@zp))
 pv=(1+(np.abs(np.array(ss)-expected)>=abs(I-expected)).sum())/(PERM+1)
 rec={'n':n,'isolados':int((~good).sum()),'I':I,'p':pv,'permutacoes':PERM}
 if not local:return rec,None,original
 Ii=z*lag;p=np.empty(n)
 for i in range(n):
  start,end=w.indptr[i:i+2];ww=w.data[start:end];m=len(ww);draws=rng.integers(0,n-1,size=(PERM,m))
  for col in range(1,m):
   bad=(draws[:,col,None]==draws[:,:col]).any(1)
   while bad.any():draws[bad,col]=rng.integers(0,n-1,size=bad.sum());bad=(draws[:,col,None]==draws[:,:col]).any(1)
  draws+=draws>=i;sim=z[i]*(z[draws]@ww);ex=-z[i]*z[i]/(n-1);p[i]=(1+(np.abs(sim-ex)>=abs(Ii[i]-ex)).sum())/(PERM+1)
 q=bh(p);cl=np.where((z>=0)&(lag>=0),'HH',np.where((z<0)&(lag<0),'LL',np.where(z>=0,'HL','LH')));cl=np.where(q<=.05,cl,'NS')
 return rec,{'p':p,'q':q,'cluster':cl,'Ii':Ii},original

# Executar
def executar(config):
    base=ler_camada(config['base']).reset_index(drop=True)
    support=ler_camada(config['suporte_calculo']) if config.get('suporte_calculo') else base.copy()
    if len(base)!=len(support):raise ValueError('Base e suporte com contagens diferentes')
    keys=config['chaves']
    if config.get('suporte_calculo'):
        support=base[keys].merge(support,on=keys,how='left',validate='one_to_one');support=gpd.GeoDataFrame(support,geometry='geometry',crs=base.crs)
    norm,valid,params=matriz(base,support,config);x=norm[valid];names=[v['nome'] for v in config['variaveis']]
    output=caminho(config['saida']);output.mkdir(parents=True,exist_ok=True);out=base.copy();out['completo']=valid
    for j in range(len(names)):out['N'+str(j+1)]=norm[:,j]
    rows=[];models={};scores={};scenario_keys=list(config['cenarios'])
    for i,(scenario,setting) in enumerate(config['cenarios'].items()):
        weights=np.array([setting['pesos'].get(n,0) for n in names],float)
        if (weights<0).any() or weights.sum()<=0:raise ValueError('Pesos devem ser não negativos e somar mais de zero')
        xx=x*np.sqrt(weights);scores[scenario]=(norm@weights)/weights.sum();out['I_'+scenario]=100*scores[scenario] if config['normalizacao']=='minmax' else scores[scenario]
        for method in config.get('metodos',['kmeans']):
            tree=linkage(xx,method='ward') if method=='ward' else None
            for k in config['k_testados']:
                if method=='ward':lab=fcluster(tree,k,criterion='maxclust')-1;loss=float('nan')
                else:loss,cent,lab=fitkm(xx,k,config['semente']+i*config.get('passo_semente',0),starts=config['inicializacoes'])
                sil=silhouette(xx,lab);models[scenario,method,k]=lab
                rows.append({'cenario':scenario,'metodo':method,'k':k,'silhouette':sil,'inercia':loss,'menor_grupo':int(np.bincount(lab).min())})
    table=pd.DataFrame(rows);first=scenario_keys[0];best=table[table.cenario.eq(first)].sort_values('silhouette',ascending=False).iloc[0];k0=int(best.k);method=best.metodo
    reference=models[first,method,k0];rank=sorted(np.unique(reference),key=lambda g: scores[first][valid][reference==g].mean());remap=dict(zip(rank,range(len(rank))));reference=np.array([remap[v] for v in reference]);stability=[];comparisons=[]
    for scenario in scenario_keys:
        lab=align(models[scenario,method,k0],reference);out['K_'+scenario]=0;out.loc[valid,'K_'+scenario]=lab+1;stability.append(lab==reference)
        comparisons.append({'cenario':scenario,'k_comum':k0,'ARI':ari(reference,lab),'concordancia_pct':100*np.mean(lab==reference),'rho_indice':float(spearmanr(scores[first][valid],scores[scenario][valid]).statistic)})
    out['estabilidade']=np.nan;out.loc[valid,'estabilidade']=100*np.mean(stability,axis=0);out['r_quintil']=0
    out.loc[valid,'r_quintil']=pd.qcut(pd.Series(scores[first][valid]).rank(method='average'),5,labels=False,duplicates='drop').to_numpy()+1
    moran_rows=[]
    if config.get('moran'):
        out['r_moran']='ND';out['q_fdr']=np.nan
        for basin,g in out[valid].groupby(config['campo_bacia']):
            if 'COB_ESG' in g:g=g[g.COB_ESG.ge(95)]
            rec,local,ids=moran_w(g['I_'+first].to_numpy(),queen(g),local=True,seed=config['semente']);moran_rows.append({'bacia':basin,**rec})
            out.loc[g.index,'r_moran']='ISO'
            if local is not None:out.loc[g.index[ids],'r_moran']=local['cluster'];out.loc[g.index[ids],'q_fdr']=local['q']
    out.to_file(output/'analise_configuravel.gpkg',layer='resultados',driver='GPKG')
    out.drop(columns='geometry').to_csv(output/'indicadores.csv',index=False)
    table.to_csv(output/'comparacao_k.csv',index=False);params.to_csv(output/'normalizacao.csv',index=False);pd.DataFrame(comparisons).to_csv(output/'sensibilidade.csv',index=False)
    pd.DataFrame(moran_rows).to_csv(output/'moran.csv',index=False)
    evidence={'registros':len(base),'completos':int(valid.sum()),'k':k0,'metodo':method,'silhouette':float(best.silhouette),'variaveis':names,'configuracao':config,'bibliotecas':{n:importlib.metadata.version(n) for n in ['numpy','pandas','geopandas','scipy','rasterio']},'aviso':'Reprodução configurável separada dos produtos publicados; índice não mede genes nem corrige concentrações.'}
    (output/'manifesto.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({k:v for k,v in evidence.items() if k not in ['configuracao']},ensure_ascii=True))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--config',default=str(caminho('config/analise_extensivel.json')));args=parser.parse_args();executar(json.loads(Path(args.config).read_text('utf-8-sig')))
