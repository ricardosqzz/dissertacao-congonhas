# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/projeto/output/16_revisao_pos_banca/zoneamento_pos_banca.gpkg | gpd.read_file.
# Entrada: E:/projeto/output/16_revisao_pos_banca/celulas_analise.gpkg | gpd.read_file.
# Entrada: E:/projeto/output/11_integracao/apendices/resumo_figuras.json | .read_text.
# Entrada: E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/{p}_{t}_receptores.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/vento/{p}_envelopes_{'horarios' if t == '1h' else 'diarios_persistentes'}.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/perfis_normalizados_grupos_estacoes.csv | pd.read_csv.
# Entrada: E:/projeto/output/15_auditoria_metodologica/revisao_cientifica/vinculos_estacoes_receptores.csv | pd.read_csv.
# Entrada: E:/projeto/output/11_integracao/nova_modelagem/estacoes_trienio_comum.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/figuras/index.html | p.read_text.
# Campos/chaves em eligible: n_design_years, pollutant.
# Campos/chaves em v: name.
# Campos/chaves em cells: geometry, receptor_id.
# Saída: os.environ.get('CONGONHAS_PAIRED_OUTPUT', str(DATA / 'pares'))/index.html | .write_text.
# Saída: E:/projeto/output/16_revisao_pos_banca/figuras/index.html | p.write_text.
# Campos/chaves gerados em sub: Q, Q_common, dominant_name.
# receptor_id: identificador do receptor.
# CÓDIGO DO PROCESSAMENTO

"""Um encarte MP10/MP2,5 por direção e duração, sem recalcular os dados."""
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

import json,html,sys,argparse,subprocess,os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import numpy as np,pandas as pd,geopandas as gpd
from matplotlib.colors import LogNorm
from paleta_concentracoes import concentration_cmap
import config,cartografia_apendices as cart
from figuras_analises_direcionais import QUINT,LISA,MATRIX,ROLES,NETWORK
from groups import GROUPS
ROOT=config.BASE/'output/16_revisao_pos_banca';DATA=ROOT/'vento/analises_espaciais';OUT=Path(os.environ.get('CONGONHAS_PAIRED_OUTPUT',str(DATA/'pares')))
DIRS=['N','NE','L','SE','S','SO','O','NO'];NAMES=['Norte','Nordeste','Leste','Sudeste','Sul','Sudoeste','Oeste','Noroeste']
SPECS=[('Quintis','Q',QUINT),('Quintis_referencia_comum','Q_common',QUINT),('Moran_local','lisa',LISA),('Moran_bivariado','bivariate',LISA),('Emissao_concentracao','matrix',MATRIX),('Regioes_gestao','management',ROLES),('Cobertura_prioridades','network_priority',NETWORK),('Grupo_predominante','dominant_name',cart.COLORS)]

# Run
def run(directions,periods=None,concentrations_only=False):
    OUT.mkdir(parents=True,exist_ok=True);cart.OUT=OUT
    z=gpd.read_file(ROOT/'zoneamento_pos_banca.gpkg');cells=gpd.read_file(ROOT/'celulas_analise.gpkg');muni=gpd.GeoDataFrame(geometry=[z.geometry.union_all()],crs=z.crs)
    extent=json.loads((config.BASE/'output/11_integracao/apendices/resumo_figuras.json').read_text(encoding='utf8'))['bounds_degrees']
    tables={(p,t):pd.read_csv(DATA/f'{p}_{t}_receptores.csv') for p in ['PM10','PM25'] for t in ['1h','24h']}
    envelopes={(p,t):pd.read_csv(ROOT/'vento'/f'{p}_envelopes_{"horarios" if t=="1h" else "diarios_persistentes"}.csv') for p in ['PM10','PM25'] for t in ['1h','24h']}
    present=pd.read_csv(ROOT/'perfis_grupos/perfis_normalizados_grupos_estacoes.csv')[['pollutant','station_id']].drop_duplicates()
    st=pd.read_csv(config.BASE/'output/15_auditoria_metodologica/revisao_cientifica/vinculos_estacoes_receptores.csv').merge(present,on=['pollutant','station_id'],validate='one_to_one')
    eligible=pd.read_csv(config.BASE/'output/11_integracao/nova_modelagem/estacoes_trienio_comum.csv');stations=[]
    for p in ['PM10','PM25']:
        f=st[st.pollutant.eq(p)&st.station_id.isin(eligible[eligible.pollutant.eq(p)&eligible.n_design_years.eq(3)].station_id)]
        stations.append(gpd.GeoDataFrame(f,geometry=gpd.points_from_xy(f.X,f.Y),crs=cells.crs))
    for direction in directions:
        for period in periods or ['1h','24h']:
            pair=[];surfaces=[]
            for pol in ['PM10','PM25']:
                table=tables[pol,period];sub=table[table.direction.eq(direction)].copy()
                common=np.quantile(table.groupby('receptor_id').concentration.max(),[.2,.4,.6,.8])
                sub['Q']=sub.quintile.map(lambda v:'Q'+str(v));sub['Q_common']=['Q'+str(v) for v in np.searchsorted(common,sub.concentration,side='left')+1]
                sub['dominant_name']=sub.dominant_group.map({k:v['name'] for k,v in GROUPS.items()})
                pair.append(cells[['receptor_id','geometry']].merge(sub,on='receptor_id',validate='one_to_one'))
                raw=envelopes[pol,period];raw=raw[raw.direction.eq(direction)];v=table.concentration;positive=v[v>0]
                low=max(10.**np.floor(np.log10(positive.quantile(.02))),.01);cap=float(positive.quantile(.99));unit=10.**np.floor(np.log10(cap));cap=max(10*low,np.floor(cap/unit)*unit)
                ticks=np.unique(np.r_[low,10.**np.arange(np.ceil(np.log10(low)),np.floor(np.log10(cap))+1),cap])
                geo=gpd.GeoSeries(gpd.points_from_xy(raw.X,raw.Y),crs=z.crs).to_crs(4674);col='max_1h' if period=='1h' else 'daily_from_1h'
                surfaces.append(dict(x=geo.x.to_numpy(),y=geo.y.to_numpy(),values=raw[col].to_numpy(),limits=[low,cap],norm=LogNorm(low,cap),cmap=concentration_cmap(),ticks=ticks,actual_max=float(sub.concentration.max()),max_in_label=True))
            base=f'{period}_{direction}';ft='Vento de '+NAMES[DIRS.index(direction)]+' · '+('máximos de 1 h' if period=='1h' else 'máximos de 24 h')
            common=dict(zone_layer=z,wind_directions=[direction]*2,png_dpi=600)
            cart.render(z,muni,['concentration']*2,base,['MP₁₀','MP₂,₅'],'',extent,surfaces=surfaces,filename=base+'_Concentracoes',figure_title=ft,**common)
            for name,field,palette in ([] if concentrations_only else SPECS):
                categories=list(palette) if name!='Grupo_predominante' else sorted(set(pd.concat(pair).dominant_name))
                opts={'station_overlay':stations} if name=='Cobertura_prioridades' else {}
                cart.render(z,muni,[field]*2,base,['MP₁₀','MP₂,₅'],'',extent,panel_layers=pair,palette=palette,legend_categories=categories,filename=base+'_'+name,figure_title=ft+' · '+name.replace('_',' '),**common,**opts)
            print('Concluídos pares',direction,period,flush=True)

# Index
def index():
    sections=[]
    for direction,name in zip(DIRS,NAMES):
        parts=[]
        for period in ['1h','24h']:
            figs=[]
            for item in ['Concentracoes']+[s[0] for s in SPECS]:
                stem=f'{period}_{direction}_{item}'
                figs.append(f'<section><h3>{html.escape(item.replace("_"," "))}</h3><a href="{stem}.svg"><img loading="lazy" src="{stem}.svg"></a><p><a href="{stem}.pdf">PDF vetorial</a> · <a href="{stem}.svg">SVG</a> · <a href="{stem}.png">PNG</a></p></section>')
            parts.append('<details><summary>'+period+'</summary>'+''.join(figs)+'</details>')
        sections.append('<h2>Vento de '+name+'</h2>'+''.join(parts))
    (OUT/'index.html').write_text('''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Mapas direcionais pareados</title><style>body{font:16px/1.6 Arial;color:#183d4c;max-width:1120px;margin:30px auto;padding:0 20px}img{width:100%}details{border:1px solid #dbe4e6;padding:14px;margin:12px 0}summary{cursor:pointer;font-size:20px}section{border-top:1px solid #ddd;margin-top:25px}a{color:#176b88}</style><h1>MP10 e MP2,5 por direção do vento</h1><p>Um mesmo encarte reúne os dois poluentes para a mesma direção e duração. O pequeno ícone destaca o setor de origem selecionado e não representa frequência ou velocidade. Os dados, os filtros meteorológicos e as análises anteriores foram preservados.</p><p>Os máximos podem ocorrer em eventos diferentes entre receptores e poluentes. As barras de concentração são independentes por poluente; seus limites permanecem fixos entre as oito direções do mesmo poluente e duração. Os mapas de 24 h usam os dias com direção persistente. As definições dos testes constam no índice analítico.</p><p><a href="../index.html">Métodos e análises completas</a> · <a href="../../../cenario_geral/index.html">Cenário geral</a> · <a href="../../Relatorio_recortes_vento.pdf">Relatório dos recortes</a></p>'''+''.join(sections)+'</html>',encoding='utf8')
    p=OUT/'index.html';s=p.read_text(encoding='utf8')
    s=s.replace('O pequeno ícone destaca o setor de origem selecionado e não representa frequência ou velocidade.','A rosa meteorológica junto à legenda preserva as frequências e as classes de velocidade da entrada. Somente o setor de origem selecionado recebe destaque em cores.')
    s=s.replace('<h1>MP10 e MP2,5 por direção do vento</h1>','<h1>MP10 e MP2,5 por direção do vento</h1><p><a href="../../../visualizador/index.html">Abrir o visualizador com seleção pela rosa dos ventos</a></p>')
    p.write_text(s,encoding='utf8')
    p=DATA/'index.html';s=p.read_text(encoding='utf8');link='<p><a href="pares/index.html">Mapas pareados: MP10 e MP2,5 lado a lado por direção e duração</a></p>'
    if link not in s:s=s.replace('</h1>','</h1>'+link,1)
    p.write_text(s,encoding='utf8')
    p=ROOT/'figuras/index.html'
    s=p.read_text(encoding='utf8')
    link='<p><a href="../visualizador/index.html">Visualizador interativo privado</a> · <a href="../vento/analises_espaciais/pares/index.html">Mapas pareados por direção e duração</a> · <a href="../../../dissertacao/_book/html/index.html">Dissertação</a> · <a href="../../../dissertacao/artigo/_book/html/index.html">Artigo</a></p>'
    if link not in s:s=s.replace('</h1>','</h1>'+link,1)
    p.write_text(s,encoding='utf8')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--worker',nargs='+');parser.add_argument('--concentrations-only',action='store_true');a=parser.parse_args()
    if a.worker:run(a.worker,concentrations_only=a.concentrations_only)
    else:
        def job(d):subprocess.run([sys.executable,str(Path(__file__).resolve()),'--worker',*d,*(['--concentrations-only'] if a.concentrations_only else [])],check=True,cwd=Path(__file__).parent)
        with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(job,[DIRS[:4],DIRS[4:]]))
        if not a.concentrations_only:index()
