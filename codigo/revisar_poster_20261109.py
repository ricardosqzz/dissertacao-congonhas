# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/projeto/descontinuado/2026_11_09_poster_rodovias_inventariadas/manifesto.json | m.read_text.
# Entrada: {path} | path.read_bytes.
# Entrada: E:/projeto/output/13_cmas_posters/Congonhas/Emissoes_densidade_sensibilidade_por_zona.gpkg | gp.read_file.
# Entrada: E:/projeto/output/16_revisao_pos_banca/celulas_analise.gpkg | gp.read_file.
# Entrada: E:/projeto/output/16_revisao_pos_banca/cenario_geral/PM25_anual_receptores.csv | pd.read_csv.
# Entrada: E:/projeto/output/13_rateio_emissoes/fontes_rateio_PM25.gpkg | gp.read_file.
# Entrada: E:/projeto/output/11_integracao/apendices/resumo_figuras.json | .read_text.
# Entrada: E:/projeto/output/16_revisao_pos_banca/limiares_cinco_faixas_validacao.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/cenario_geral/PM25_1h_receptores.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/cenario_geral/{pol}_{per}_receptores.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/contribuicoes_prioridades_pooled_PM25.csv | pd.read_csv.
# Campos/chaves em c: PM25_annual, geometry, receptor_id.
# Campos/chaves em annual: concentration, dominant_group, receptor_id.
# Campos/chaves em d: ID.
# Campos/chaves em roads: corridor_m2, length_m, massa, source_id, source_type, width_m.
# Campos/chaves em v: name, value.
# Campos/chaves em cuts: basis, pollutant.
# Campos/chaves em pooled.loc: share_pct.
# Campos/chaves em pooled: group_id.
# Saída: E:/projeto/descontinuado/2026_11_09_poster_rodovias_inventariadas/manifesto.json | m.write_text.
# Saída: E:/projeto/output/13_cmas_posters/Congonhas/Auditoria_vias_inventariadas_densidade.csv | .to_csv.
# Saída: E:/projeto/codigo/recursos_poster/assets/dados_poster_20261109.json | .write_text.
# Saída: E:/projeto/output/13_cmas_posters/Congonhas/Perfis_conjuntos_estatisticas.csv | .to_csv.
# Saída: E:/projeto/output/13_cmas_posters/Congonhas/Cortes_emissao_boxplot_PM25.csv | cuts.to_csv.
# Saída: E:/projeto/output/13_cmas_posters/Congonhas/Auditoria_revisao_poster_20261109.json | .write_text.
# Campos/chaves gerados em roads: corridor_m2, density_corridor, length_m, width_m.
# Campos/chaves gerados em g: dominant_name.
# receptor_id: identificador do receptor.
# concentration: concentração do período em µg/m³.
# CÓDIGO DO PROCESSAMENTO

"""Revisão do pôster: vias, suporte físico e dados rastreáveis dos gráficos."""
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
import json, hashlib, shutil, xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import geopandas as gp
import matplotlib
matplotlib.use('Agg')
from matplotlib.figure import Figure
from matplotlib.colors import BoundaryNorm, ListedColormap
import cartografia_apendices as cart
import revisar_poster_e_guias_20261108 as previous
from svg_compativel_word import convert
from groups import GROUPS

R=Path(_cp_texto('', 'posix')); O=R/'output/13_cmas_posters/Congonhas'
A=R/'codigo/recursos_poster/assets'; P=R/'output/16_revisao_pos_banca'
T=R/'temp/poster_20261109'; B=R/'descontinuado/2026_11_09_poster_rodovias_inventariadas'

# Archive
def archive(path):
    path=Path(path)
    if not path.exists(): return
    dest=B/path.relative_to(R)
    if dest.exists(): return
    dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,dest)
    m=B/'manifesto.json'; rows=json.loads(m.read_text(encoding='utf8')) if m.exists() else []
    rows.append(dict(origem=str(path),preservado=str(dest),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),motivo='Substituído pela revisão do pôster de 09/11/2026; arquivos-base preservados.'))
    m.write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf8')

# Run
def run():
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
    T.mkdir(parents=True,exist_ok=True);previous.archive=archive
    for name in ['gerar_poster_cmas.mjs','auditar_escalas_poster.py']:
        archive(R/'codigo'/name)
    for name in ['Poster_CMAS_Session12_Congonhas.pptx','Poster_CMAS_Session12_Congonhas.pdf','Poster_CMAS_Session12_Congonhas_previa.png','auditoria_escalas.json','manifesto_entrega_poster_guias.json','Guia_estudo_poster_Congonhas.docx','Guia_estudo_poster_Congonhas.pdf','Roteiro_detalhado_poster_EN.docx','Roteiro_detalhado_poster_EN.pdf']:
        archive(O/name)
    for name in ['guia-detalhado.md','roteiro-detalhado-em-ingles.md','README.md']:
        archive(R/'dissertacao/poster'/name)
    z=gp.read_file(O/'Emissoes_densidade_sensibilidade_por_zona.gpkg')
    c=gp.read_file(P/'celulas_analise.gpkg')
    annual=pd.read_csv(P/'cenario_geral/PM25_anual_receptores.csv')
    comp=c[['receptor_id','PM25_annual']].merge(annual[['receptor_id','concentration']],on='receptor_id',validate='one_to_one')
    assert np.allclose(comp.PM25_annual,comp.concentration,rtol=0,atol=1e-6)

    import openpyxl
    wb=openpyxl.load_workbook(R/'entrada_aermod/PM2-5_Sources.xlsx',read_only=True,data_only=True)
    rows=wb.active.iter_rows(values_only=True)
    for row in rows:
        if 'Type' in row and 'ID' in row:
            headers=list(row);break
    widths={}
    for row in rows:
        d=dict(zip(headers,row))
        if not isinstance(d.get('Num_Coords'),(int,float)):continue
        field='Length_X' if d.get('Type')=='LINE_AREA' else 'PlumeWidth'
        if d.get('Type') in ('LINE_AREA','LINE_VOLUME'):
            widths[str(d['ID'])]=float(d[field])
    wb.close()
    roads=gp.read_file(R/'output/13_rateio_emissoes/fontes_rateio_PM25.gpkg')
    roads=roads[roads.source_type.isin(['LINE_AREA','LINE_VOLUME']) & ~roads.source_id.str.startswith('FER')].copy()
    roads['width_m']=roads.source_id.map(widths)
    assert roads.width_m.notna().all() and (roads.width_m>0).all()
    roads['length_m']=roads.length
    roads['corridor_m2']=roads.length_m*roads.width_m
    roads['density_corridor']=roads.massa/roads.corridor_m2*1e6
    roads.drop(columns='geometry').to_csv(O/'Auditoria_vias_inventariadas_densidade.csv',index=False)
    roads=roads.to_crs(4674)
    extent=json.loads((R/'output/11_integracao/apendices/resumo_figuras.json').read_text(encoding='utf8'))['bounds_degrees']
    muni=gp.GeoDataFrame(geometry=[z.geometry.union_all()],crs=z.crs)
    roads=roads[roads.intersects(muni.to_crs(4674).geometry.union_all())]
    original_save=Figure.savefig
    def save_with_roads(fig,*args,**kwargs):
        if not getattr(fig,'_roads_drawn',False):
            roads.plot(ax=fig.axes[0],column='density_corridor',cmap=cmap,norm=norm,linewidth=.65,alpha=1,zorder=7.2,aspect=None)
            fig._roads_drawn=True
        return original_save(fig,*args,**kwargs)
    cart.OUT=O;bins=[0,1,5,10,25,50,100,250]
    pal=['#fff2b2','#ffdb84','#fcb65e','#f28b42','#e45c32','#c9372b','#922322']
    for ext in ['svg','pdf','png']:archive(O/f'Poster_Densidade_emissao_zonas.{ext}')
    Figure.savefig=save_with_roads
    try:
        cmap=ListedColormap(pal);norm=BoundaryNorm(bins,cmap.N,clip=True)
        cart.render(z,muni,['density'],'PD',[''],'',extent,numeric=True,numeric_options=[dict(norm=norm,cmap=cmap,ticks=bins,label='PM₂,₅ emission density (t/year/km²)',show_missing=False)],filename='Poster_Densidade_emissao_zonas',png_dpi=350)
    finally: Figure.savefig=original_save
    g=c[['receptor_id','geometry']].merge(annual[['receptor_id','dominant_group']],on='receptor_id',validate='one_to_one')
    g['dominant_name']=g.dominant_group.map({k:v['name'] for k,v in GROUPS.items()})
    categories=sorted(g.dominant_name.unique())
    for ext in ['svg','pdf','png']:archive(O/f'Poster_Grupo_predominante.{ext}')
    cart.render(z,muni,['dominant_name'],'PS',[''],'',extent,panel_layers=[g],zone_layer=z,palette=cart.COLORS,legend_categories=categories,filename='Poster_Grupo_predominante',png_dpi=350)
    for key,stem in [('E','Poster_Densidade_emissao_zonas'),('D','Poster_Grupo_predominante')]:
        compatible=T/f'{stem}_compatible.svg';convert(O/f'{stem}.svg',compatible)
        previous.prepare_svg(compatible,A/f'poster_{key}_MAIN.svg',220000)
    for key in ['Q','K','B','Z']:
        source=A/f'poster_{key}_PDF.svg'
        previous.prepare_svg(source if source.exists() else A/f'poster_{key}_MAIN.svg',A/f'poster_{key}_MAIN.svg',220000)
    previous.prepare_svg(T/'Poster_Grupo_predominante_compatible.svg',A/'poster_D_METHOD.svg',440000,True)
    cuts=pd.read_csv(P/'limiares_cinco_faixas_validacao.csv')
    cuts=cuts[(cuts.pollutant=='PM25')&(cuts.basis=='density_tpy_km2')]
    box=[]
    for q,d in cuts.groupby('percentile_target',sort=True):
        assert len(d)==10
        vals=d.cut_train.to_numpy()
        box.append(dict(percentile=int(q),concentration=float(d.concentration_cut.iloc[0]),full_cut=float(d.cut_all_data.iloc[0]),values=vals.tolist(),q25=float(np.quantile(vals,.25)),median=float(np.median(vals)),q75=float(np.quantile(vals,.75)),minimum=float(vals.min()),maximum=float(vals.max()),balanced_accuracy_mean=float(d.balanced_accuracy_test.mean())))
    cluster=[]
    labels=pd.read_csv(P/'cenario_geral/PM25_1h_receptores.csv')[['receptor_id','best_cluster']]
    for pol in ['PM10','PM25']:
        for per in ['1h','24h','anual']:
            f=pd.read_csv(P/f'cenario_geral/{pol}_{per}_receptores.csv')
            for k,d in f.groupby('best_cluster'):
                cluster.append(dict(pollutant=pol,period=per,cluster=int(k),n=len(d),median=float(d.concentration.median()),mean=float(d.concentration.mean())))
    dom=[]
    display={'GERDAU':'Gerdau','URB':'Urban total','CSN-CDP':'CSN Casa de Pedra','VALE_FAB':'Vale Fábrica','VALE_VIG':'Vale Viga','FERRO':'Ferro+','SCOF':'SCOF','LGA':'LGA','NOGD':'Nogueira Duarte'}
    for k in sorted(annual.dominant_group.unique()):
        name=GROUPS[k]['name'];dom.append(dict(id=k,label=display[k],color=cart.COLORS[name],n=int(annual.dominant_group.eq(k).sum())))
    pooled=pd.read_csv(P/'contribuicoes_prioridades_pooled_PM25.csv')
    vals=[]
    for k in ['GERDAU','URB','VALE_FAB','LGA']:
        vals.append(dict(id=k,label=display[k],value=float(pooled.loc[pooled.group_id.eq(k),'share_pct'].iloc[0])))
    vals.append(dict(id='OTHER',label='Other groups',value=100-sum(v['value'] for v in vals)))
    from pyproj import Geod
    ex=[extent[0]-.018,extent[1]-.025,extent[2]+.015,extent[3]+.026]
    ground=Geod(ellps='GRS80').inv(ex[0],(ex[1]+ex[3])/2,ex[2],(ex[1]+ex[3])/2)[2]
    out=dict(date='2026-11-09',ground_width_m=ground,boxplots=box,cluster_profiles=cluster,dominant_groups=dom,contributions=vals,road_features=len(roads),period_note='Annual panels: mean of three native annual AERMOD concentrations, 2021–2023. Joint profiles: 1 h and 24 h maxima plus annual means for both pollutants.',methods_scale=440000,results_scale=220000)
    (A/'dados_poster_20261109.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
    pd.DataFrame(cluster).to_csv(O/'Perfis_conjuntos_estatisticas.csv',index=False)
    cuts.to_csv(O/'Cortes_emissao_boxplot_PM25.csv',index=False)
    (O/'Auditoria_revisao_poster_20261109.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(dict(roads=len(roads),dominant=dom,boxplots=box),ensure_ascii=False))

if __name__=='__main__':run()
