# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/projeto/descontinuado/2026_11_08_poster_detalhado/manifesto.json | f.read_text.
# Entrada: {p} | p.read_bytes.
# Entrada: E:/projeto/output/16_revisao_pos_banca/zoneamento_pos_banca.gpkg | gp.read_file.
# Entrada: E:/projeto/output/16_revisao_pos_banca/celulas_analise.gpkg | gp.read_file.
# Entrada: E:/projeto/output/13_rateio_emissoes/fontes_rateio_PM25.gpkg | gp.read_file.
# Entrada: E:/projeto/output/16_revisao_pos_banca/limiares_cinco_faixas_validacao.csv | pd.read_csv.
# Entrada: E:/projeto/output/11_integracao/apendices/resumo_figuras.json | .read_text.
# Campos/chaves em z: density, high_area_pct, zone_index.
# Campos/chaves em f: balanced_accuracy_test, basis, cut_all_data, cut_train, percentile_target, pollutant.
# Saída: E:/projeto/descontinuado/2026_11_08_poster_detalhado/manifesto.json | f.write_text.
# Saída: E:/projeto/output/13_cmas_posters/Congonhas/Rateio_emissoes_MP25_por_fonte_zona.csv | .to_csv.
# Saída: E:/projeto/output/13_cmas_posters/Congonhas/Emissoes_densidade_sensibilidade_por_zona.csv | .to_csv.
# Saída: E:/projeto/output/13_cmas_posters/Congonhas/Emissoes_densidade_sensibilidade_por_zona.gpkg | z.to_file.
# Saída: E:/projeto/output/13_cmas_posters/Congonhas/Auditoria_mapas_emissao_poster.json | .write_text.
# Campos/chaves gerados em z: area_km2, density, high_area_pct, high_band, mass_tpy, unstable_area_pct.
# mass_tpy: massa anual em t/ano.
# CÓDIGO DO PROCESSAMENTO

"""Insumos cartográficos do pôster, com rateio zonal auditável e escala física."""
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
import json,hashlib,shutil,copy,xml.etree.ElementTree as ET
import numpy as np,pandas as pd,geopandas as gp
from shapely import make_valid
from matplotlib import pyplot as plt
from matplotlib.colors import BoundaryNorm,ListedColormap
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from matplotlib.path import Path as MPath
import cartografia_apendices as cart

R=Path(_cp_texto('', 'posix'));O=R/'output/13_cmas_posters/Congonhas';A=R/'codigo/recursos_poster/assets';T=R/'temp/revisao_poster_teco_20261108'
S='{http://www.w3.org/2000/svg}';B=R/'descontinuado/2026_11_08_poster_detalhado'

# Archive
def archive(p):
    if not p.exists():return
    q=B/p.relative_to(R)
    if q.exists():return
    q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
    f=B/'manifesto.json';rows=json.loads(f.read_text(encoding='utf8')) if f.exists() else []
    rows.append({'origem':str(p),'arquivo_preservado':str(q),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'motivo':'Substituído pela revisão do pôster e guias de estudo em 08/11/2026.'})
    f.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')

# Svg path
def svg_path(path):
    out=[]
    for v,c in path.iter_segments(curves=True,simplify=False):
        if c==MPath.MOVETO:out.append('M '+' '.join(f'{x:.5f}' for x in v))
        elif c==MPath.LINETO:out.append('L '+' '.join(f'{x:.5f}' for x in v))
        elif c==MPath.CURVE3:out.append('Q '+' '.join(f'{x:.5f}' for x in v))
        elif c==MPath.CURVE4:out.append('C '+' '.join(f'{x:.5f}' for x in v))
        elif c==MPath.CLOSEPOLY:out.append('Z')
    return ' '.join(out)

# Prepare svg
def prepare_svg(source,target,scale=200000,method=False):
    tree=ET.parse(source);root=tree.getroot();definitions=[];seen=set()
    for d in list(root.iter(S+'defs')):
        for item in d:
            ident=item.get('id')
            if ident and ident in seen:continue
            definitions.append(copy.deepcopy(item));seen.add(ident)
    for parent in list(root.iter()):
        for child in list(parent):
            if child.tag==S+'defs':parent.remove(child)
    defs=ET.SubElement(root,S+'defs')
    for item in definitions:defs.append(item)
    axes=next(g for g in root.iter(S+'g') if g.get('id')=='axes_1')
    rects=root.findall('.//'+S+'clipPath/'+S+'rect');rect=max(rects,key=lambda e:float(e.get('width'))*float(e.get('height')))
    x,y,w,h=[float(rect.get(k)) for k in ('x','y','width','height')]

    for g in list(axes):
        if g.get('id')=='datum_scale_poster':axes.remove(g);continue
        if g.get('id','').startswith('text_'):
            if g.find(S+'g/'+S+'path') is None and any(z.get('id','').startswith('patch_') for z in g):axes.remove(g)
            elif any('5.7' in (z.get('style','')) or '0.057' in z.get('transform','') for z in g.iter()):axes.remove(g)
        if method and g.get('id','').startswith('matplotlib.axis_'):axes.remove(g)

    for g in list(axes):
        if g.get('id')=='text_21':axes.remove(g)
    bw,bh=62,28;bx=x+w-bw-4;by=y+h-bh-4
    box=ET.SubElement(axes,S+'g',{'id':'datum_scale_poster','data-scale':str(scale)})
    ET.SubElement(box,S+'rect',{'x':str(bx),'y':str(by),'width':str(bw),'height':str(bh),'rx':'1.3','fill':'white','fill-opacity':'.95','stroke':'#b9bdb6','stroke-width':'.45'})
    for line,yy in zip(['SIRGAS 2000','EPSG:4674',f'Escala 1:{scale:,}'.replace(',','.')],[by+7.3,by+15,by+22.7]):
        path=TextPath((0,0),line,size=5.7,prop=FontProperties(family='DejaVu Sans'));bb=path.get_extents()
        tx=bx+bw/2-(bb.x0+bb.x1)/2
        ET.SubElement(box,S+'path',{'d':svg_path(path),'transform':f'translate({tx:.6f} {yy:.6f}) scale(1 -1)','fill':'#646962'})

    root.set('viewBox',f'{x-14.99:.6f} {y-4.218359:.6f} {w+24.99:.6f} {h+18.218359:.6f}')
    root.set('width',f'{w+24.99:.6f}pt');root.set('height',f'{h+18.218359:.6f}pt')
    for child in list(root):
        if child.tag==S+'g':

            for sub in list(child):
                if sub.tag==S+'g' and sub is not axes and sub.get('id','').startswith(('axes_','legend_')):child.remove(sub)
    archive(target);tree.write(target,encoding='utf-8',xml_declaration=True)

# Run
def run():
    O.mkdir(parents=True,exist_ok=True);T.mkdir(parents=True,exist_ok=True)
    ET.register_namespace('','http://www.w3.org/2000/svg');ET.register_namespace('xlink','http://www.w3.org/1999/xlink')
    z=gp.read_file(R/'output/16_revisao_pos_banca/zoneamento_pos_banca.gpkg');z.geometry=z.geometry.make_valid();union=z.geometry.union_all()
    c=gp.read_file(R/'output/16_revisao_pos_banca/celulas_analise.gpkg').to_crs(z.crs)
    src=gp.read_file(R/'output/13_rateio_emissoes/fontes_rateio_PM25.gpkg').to_crs(z.crs)
    rows=[];mass=np.zeros(len(z));expected=0.
    for r in src.itertuples():
        geom=make_valid(r.geometry)
        if geom.is_empty or not np.isfinite(r.massa):continue
        mode='area' if geom.area>0 else 'length' if geom.length>0 else 'point';den=geom.area if mode=='area' else geom.length if mode=='length' else 1
        inside=geom.intersection(union);expected+=r.massa*(inside.area/den if mode=='area' else inside.length/den if mode=='length' else float(union.covers(geom)))
        ids=list(z.sindex.query(geom,predicate='intersects'))
        if mode=='point' and ids:ids=[min(ids,key=lambda i:(z.geometry.iloc[i].representative_point().distance(geom),i))]

        remaining=geom
        for i in sorted(ids,key=lambda j:(z.geometry.iloc[j].area,j)):
            it=remaining.intersection(z.geometry.iloc[i]);f=it.area/den if mode=='area' else it.length/den if mode=='length' else float(not it.is_empty)
            if f<=0:continue
            m=float(r.massa*f);mass[i]+=m;rows.append({'zone_index':int(z.zone_index.iloc[i]),'source_id':r.source_id,'group_id':r.group_id,'fraction':f,'mass_tpy':m})
            if mode!='point':remaining=remaining.difference(z.geometry.iloc[i])
    assert abs(mass.sum()-expected)<.001,(mass.sum(),expected)
    z['mass_tpy']=mass;z['area_km2']=z.area/1e6;z['density']=np.divide(mass,z.area/1e6,out=np.full(len(z),np.nan),where=z.area>0)
    f=pd.read_csv(R/'output/16_revisao_pos_banca/limiares_cinco_faixas_validacao.csv');f=f[(f.pollutant=='PM25')&(f.basis=='density_tpy_km2')&(f.percentile_target==80)]
    cut=float(f.cut_all_data.iloc[0]);lo=float(f.cut_train.min());hi=float(f.cut_train.max())
    high=np.zeros(len(z));unstable=np.zeros(len(z));covered=np.zeros(len(z))
    for r in c.itertuples():
        for i in z.sindex.query(r.geometry,predicate='intersects'):
            area=r.geometry.intersection(z.geometry.iloc[i]).area;covered[i]+=area
            high[i]+=area*(r.PM25_density_tpy_km2>cut);unstable[i]+=area*(lo<r.PM25_density_tpy_km2<=hi)
    z['high_area_pct']=100*np.divide(high,z.area,out=np.zeros(len(z)),where=z.area>0)
    z['unstable_area_pct']=100*np.divide(unstable,z.area,out=np.zeros(len(z)),where=z.area>0)
    z['high_band']=pd.cut(z.high_area_pct,[-.001,.000001,25,50,75,100.001],labels=['None','>0–25%','>25–50%','>50–75%','>75–100%']).astype(str)
    pd.DataFrame(rows).to_csv(O/'Rateio_emissoes_MP25_por_fonte_zona.csv',index=False)
    z.drop(columns='geometry').to_csv(O/'Emissoes_densidade_sensibilidade_por_zona.csv',index=False)
    target=O/'Emissoes_densidade_sensibilidade_por_zona.gpkg';archive(target)
    if target.exists():target.unlink()
    z.to_file(target,driver='GPKG')
    audit={'municipal_expected_mass_tpy':expected,'zone_allocated_mass_tpy':float(mass.sum()),'absolute_error_tpy':abs(float(mass.sum())-expected),'zones':len(z),'zone_area_sum_km2':float(z.area.sum()/1e6),'union_area_km2':union.area/1e6,'overlap_treatment':'Ratear a interseção remanescente em ordem crescente de área zonal, sem duplicar massa; conservar todos os 311 registros.','high_emission_cell_cut_tpy_km2':cut,'spatial_fold_cut_min':lo,'spatial_fold_cut_max':hi,'balanced_accuracy_test_mean':float(f.balanced_accuracy_test.mean()),'high_zone_map':'Porcentagem da área zonal que intercepta células acima do limiar ajustado no suporte original. Não reaplicar o limiar celular à média zonal.','stability_map':'Área que altera classe dentro do intervalo dos cortes de validação; não é probabilidade ou intervalo de confiança.','zones_without_area':int((z.area<=0).sum()),'zones_under_1m2':int((z.area<1).sum()),'maximum_zonal_density':float(z.density.max())}
    (O/'Auditoria_mapas_emissao_poster.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf8')
    extent=json.loads((R/'output/11_integracao/apendices/resumo_figuras.json').read_text(encoding='utf8'))['bounds_degrees']
    old=cart.OUT;cart.OUT=O;muni=gp.GeoDataFrame(geometry=[union],crs=z.crs)

    bins=[0,1,5,10,25,50,100,250]
    pal=['#fff2b2','#ffdb84','#fcb65e','#f28b42','#e45c32','#c9372b','#922322']
    cmap=ListedColormap(pal);norm=BoundaryNorm(bins,cmap.N,clip=True)
    surface={'values':z.density.to_numpy(),'norm':norm,'cmap':cmap,'ticks':bins,'actual_max':float(z.density.max())}
    cart.render(z,muni,['density'],'PD', [''],'',extent,numeric=True,numeric_options=[{'norm':norm,'cmap':cmap,'ticks':bins,'label':'Emission density (t/year/km²)','show_missing':False}],filename='Poster_Densidade_emissao_zonas',png_dpi=350)
    highpal=dict(zip(['None','>0–25%','>25–50%','>50–75%','>75–100%'],['#edf1ef','#f8dc8f','#eeb05e','#dd7952','#a74650']))

    from matplotlib.figure import Figure
    original_save=Figure.savefig
    sensitive=c[(c.PM25_density_tpy_km2>lo)&(c.PM25_density_tpy_km2<=hi)].to_crs(4674)
    def save_with_stability(fig,*args,**kwargs):
        if not getattr(fig,'_stability_drawn',False):
            sensitive.plot(ax=fig.axes[0],facecolor='none',edgecolor='#35413d',hatch='////',linewidth=.08,alpha=.72,zorder=6.8)
            fig._stability_drawn=True
        return original_save(fig,*args,**kwargs)
    Figure.savefig=save_with_stability
    try:cart.render(z,muni,['high_band'],'PH',[''],'',extent,palette=highpal,filename='Poster_Alta_emissao_fracao_zonal',png_dpi=350)
    finally:Figure.savefig=original_save
    cart.OUT=old
    from svg_compativel_word import convert
    for key,stem in [('E','Poster_Densidade_emissao_zonas'),('H','Poster_Alta_emissao_fracao_zonal')]:
        compatible=T/f'{stem}_vetorial.svg'
        n=convert(O/f'{stem}.svg',compatible)
        prepare_svg(compatible if n else O/f'{stem}.svg',A/f'poster_{key}_MAIN.svg')
    for key in ['Q','K','B','Z']:prepare_svg(A/f'poster_{key}_PDF.svg' if (A/f'poster_{key}_PDF.svg').exists() else A/f'poster_{key}_MAIN.svg',A/f'poster_{key}_MAIN.svg')
    for key in ['Q','K','D','Z']:prepare_svg(A/f'poster_{key}_PDF.svg',A/f'poster_{key}_METHOD.svg',440000,True)
    print(json.dumps(audit,ensure_ascii=False))

if __name__=='__main__':run()
