# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/projeto/output/16_revisao_pos_banca/zoneamento_pos_banca.gpkg | gpd.read_file.
# Entrada: E:/projeto/output/16_revisao_pos_banca/celulas_analise.gpkg | gpd.read_file.
# Entrada: E:/projeto/output/11_integracao/apendices/resumo_figuras.json | .read_text.
# Entrada: E:/projeto/output/16_revisao_pos_banca/cenario_geral/{pol}_{period}_receptores.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/perfis_normalizados_grupos_estacoes.csv | pd.read_csv.
# Entrada: E:/projeto/output/15_auditoria_metodologica/revisao_cientifica/vinculos_estacoes_receptores.csv | pd.read_csv.
# Entrada: E:/projeto/output/11_integracao/nova_modelagem/estacoes_trienio_comum.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/cenario_geral/envelope_{pol}_{period}.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/cenario_geral/correlogramas.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/cenario_geral/limiares_cinco_faixas.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/cenario_geral/comparacao_agrupamentos.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/cenario_geral/resumo.json | .read_text.
# Entrada: {p} | p.read_text.
# Campos/chaves em cells: geometry, receptor_id.
# Campos/chaves em v: name.
# Campos/chaves em eligible: n_design_years, pollutant.
# Campos/chaves em f: X, Y, concentration, emission_density, quintile.
# Campos/chaves em layers: 1h, PM10.
# Campos/chaves em corr: period, pollutant.
# Campos/chaves em comparison: method.
# Campos/chaves em limits: basis, period, pollutant.
# Campos/chaves em r: five_emission_bands_identifiable, global_moran, lisa_counts, management_counts, n_receptors, period, pollutant.
# Campos/chaves em summary: cases.
# Saída: E:/projeto/output/16_revisao_pos_banca/cenario_geral/figuras/{stem}.{ext} | fig.savefig.
# Saída: {fig} | save.
# Saída: E:/projeto/output/16_revisao_pos_banca/cenario_geral/index.html | .write_text.
# Saída: E:/projeto/output/16_revisao_pos_banca/cenario_geral/figuras/legendas.json | .write_text.
# Saída: {p} | p.write_text.
# Campos/chaves gerados em g: Q, best_cluster_label, dominant_name, ward4_label.
# receptor_id: identificador do receptor.
# concentration: concentração do período em µg/m³.
# emission_density: densidade de emissão em t/ano/km².
# X: coordenada leste em metros.
# Y: coordenada norte em metros.
# Novas variáveis: config/analise_extensivel.json; definir origem, campo, agregação, transformação e peso.
# CÓDIGO DO PROCESSAMENTO

"""Mapas pareados do cenário sem condicionamento pelo vento."""
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

import json,html
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from paleta_concentracoes import concentration_cmap
import config
import cartografia_apendices as cart
from groups import GROUPS
from figuras_analises_direcionais import QUINT,LISA,MATRIX,ROLES,NETWORK,CLUSTERS

ROOT=config.BASE/'output/16_revisao_pos_banca'
DATA=ROOT/'cenario_geral';OUT=DATA/'figuras'
PERIODS=['1h','24h','anual']
LABEL={'1h':'Máximos de 1 h','24h':'Máximos de 24 h','anual':'Média anual do triênio'}
POLLS=['PM10','PM25'];PN={'PM10':'MP₁₀','PM25':'MP₂,₅'}

# Run
def run(concentrations_only=False):
    OUT.mkdir(parents=True,exist_ok=True);cart.OUT=OUT
    z=gpd.read_file(ROOT/'zoneamento_pos_banca.gpkg');cells=gpd.read_file(ROOT/'celulas_analise.gpkg')
    muni=gpd.GeoDataFrame(geometry=[z.geometry.union_all()],crs=z.crs)
    extent=json.loads((config.BASE/'output/11_integracao/apendices/resumo_figuras.json').read_text(encoding='utf8'))['bounds_degrees']
    catalog={};table={};layers={}
    for period in PERIODS:
        for pol in POLLS:
            f=pd.read_csv(DATA/f'{pol}_{period}_receptores.csv');table[pol,period]=f
            g=cells[['receptor_id','geometry']].merge(f,on='receptor_id',validate='one_to_one')
            g['Q']=g.quintile.map(lambda v:'Q'+str(v));g['dominant_name']=g.dominant_group.map({k:v['name'] for k,v in GROUPS.items()})
            g['best_cluster_label']=g.best_cluster.map(lambda v:'Grupo '+str(v));g['ward4_label']=g.ward4.map(lambda v:'Grupo '+str(v))
            layers[pol,period]=g
    present=pd.read_csv(ROOT/'perfis_grupos/perfis_normalizados_grupos_estacoes.csv')[['pollutant','station_id']].drop_duplicates()
    st=pd.read_csv(config.BASE/'output/15_auditoria_metodologica/revisao_cientifica/vinculos_estacoes_receptores.csv').merge(present,on=['pollutant','station_id'],validate='one_to_one')
    eligible=pd.read_csv(config.BASE/'output/11_integracao/nova_modelagem/estacoes_trienio_comum.csv')
    stations=[]
    for pol in POLLS:
        ss=st[st.pollutant.eq(pol)&st.station_id.isin(eligible[eligible.pollutant.eq(pol)&eligible.n_design_years.eq(3)].station_id)]
        stations.append(gpd.GeoDataFrame(ss,geometry=gpd.points_from_xy(ss.X,ss.Y),crs=cells.crs))
    specs=[('Quintis','Q',QUINT,'Cinco classes relativas nos receptores municipais, delimitadas por P20, P40, P60 e P80 de cada poluente e duração. Não expressam atendimento aos padrões de qualidade do ar.'),
           ('Moran_local','lisa',LISA,'Moran local de log(1+C), oito vizinhos, 999 permutações condicionais bilaterais e BH nominal de 5% por campo.'),
           ('Moran_bivariado','bivariate',LISA,'Moran local bivariado entre concentração e densidade anual de emissão na vizinhança. Não representa trajetórias de transporte.'),
           ('Emissao_concentracao','matrix',MATRIX,'Alta C acima de P80. Alta E acima do corte associativo para esse alvo. O corte não constitui limite permissível de emissão.'),
           ('Regioes_gestao','management',ROLES,'Prioridade receptora acima de P80. Controle de fontes identifica alta emissão fora dessa faixa. Menor impacto relativo combina C até P40 e E até o corte associado a P40.'),
           ('Cobertura_prioridades','network_priority',NETWORK,'Área das regiões prioritárias dentro dos entornos de 4 km das estações com dados elegíveis no triênio. A aproximação geométrica não comprova representatividade uniforme.'),
           ('Grupo_predominante','dominant_name',cart.COLORS,'Maior contribuição entre os grupos exclusivos. Nos máximos, as parcelas são consultadas no evento de ALL; no anual, usam as médias nativas dos três anos. AEX e subgrupos urbanos não são somados novamente.')]
    for period in PERIODS:
        pair=[layers[p,period] for p in POLLS]
        for name,field,palette,caption in ([] if concentrations_only else specs):
            stem=f'Geral_{period}_{name}';categories=list(palette) if name!='Grupo_predominante' else sorted(set(pd.concat(pair).dominant_name))
            cart.render(z,muni,[field]*2,stem,[PN[p] for p in POLLS],'',extent,panel_layers=pair,zone_layer=z,palette=palette,legend_categories=categories,filename=stem,figure_title=LABEL[period]+' · '+name.replace('_',' '),**({'station_overlay':stations} if name=='Cobertura_prioridades' else {}))
            catalog[stem]=caption
            print('Mapa geral',stem,flush=True)
        surfaces=[]
        for pol in POLLS:
            f=pd.read_csv(DATA/f'envelope_{pol}_{period}.csv');v=table[pol,period].concentration;positive=v[v>0]
            low=max(10.**np.floor(np.log10(positive.quantile(.02))),.01);cap=float(positive.quantile(.99));unit=10.**np.floor(np.log10(cap));cap=max(10*low,np.floor(cap/unit)*unit)
            ticks=np.unique(np.r_[low,10.**np.arange(np.ceil(np.log10(low)),np.floor(np.log10(cap))+1),cap])
            geo=gpd.GeoSeries(gpd.points_from_xy(f.X,f.Y),crs=z.crs).to_crs(4674)
            surfaces.append(dict(x=geo.x.to_numpy(),y=geo.y.to_numpy(),values=f.concentration.to_numpy(),limits=[low,cap],norm=LogNorm(low,cap),cmap=concentration_cmap(),ticks=ticks,actual_max=float(v.max()),max_in_label=True))
        stem=f'Geral_{period}_Concentracoes'
        cart.render(z,muni,['concentration']*2,stem,[PN[p] for p in POLLS],'',extent,surfaces=surfaces,zone_layer=z,filename=stem,figure_title=LABEL[period]+' · meteorologia completa')
        catalog[stem]='Superfície visual interpolada com apoio dos 1497 receptores regionais e recortada ao município. Cores e barra logarítmica independentes por poluente; ponta indica valores superiores ao último corte. Testes usam os 1008 receptores municipais, sem interpolação.'
    if concentrations_only:return
    for field in ['best_cluster_label','ward4_label']:
        g=layers['PM10','1h'];stem='Geral_Conjunto_'+field;categories=sorted(set(g[field]))
        cart.render(z,muni,[field],stem,['Agrupamento conjunto'],'',extent,panel_layers=[g],zone_layer=z,palette=CLUSTERS,legend_categories=categories,filename=stem,figure_title='Perfis conjuntos · meteorologia completa')
        catalog[stem]='Agrupamento conjunto com seis variáveis log1p padronizadas: máximos de 1 h, máximos de 24 h e média anual trienal de MP10 e MP2,5. Melhor silhueta entre Ward/k-means, K=2 a 6, e solução Ward de quatro grupos como comparação.'
    corr=pd.read_csv(DATA/'correlogramas.csv');limits=pd.read_csv(DATA/'limiares_cinco_faixas.csv');comparison=pd.read_csv(DATA/'comparacao_agrupamentos.csv')
    def save(fig,stem,caption):
        for ext in ['svg','pdf','png']:fig.savefig(OUT/f'{stem}.{ext}',dpi=450,bbox_inches='tight',facecolor='white')
        plt.close(fig);catalog[stem]=caption
    fig,axes=plt.subplots(1,3,figsize=(12,3.6),layout='constrained')
    for ax,period in zip(axes,PERIODS):
        for pol,color in zip(POLLS,['#176b88','#bd5b4b']):
            s=corr[corr.period.eq(period)&corr.pollutant.eq(pol)];ax.plot((s.min_distance_m+s.max_distance_m)/2000,s.I,'o-',color=color,label=PN[pol],ms=3)
        ax.axhline(0,color='#777',lw=.6,ls=':');ax.set(title=LABEL[period],xlabel='Distância média da banda (km)',ylabel='Moran I')
    axes[0].legend(frameon=False)
    save(fig,'Geral_Correlogramas','Moran global por bandas de 750 m até 7,5 km, 199 permutações. Mostra a escala da associação espacial, sem definir sozinho o alcance de uma fonte.')
    fig,ax=plt.subplots(figsize=(6.5,3.6),layout='constrained')
    for method,color in [('ward','#176b88'),('kmeans','#bd5b4b')]:
        s=comparison[comparison.method.eq(method)];ax.plot(s.k,s.silhouette,'o-',label=method,color=color)
    ax.set(xlabel='Número de grupos',ylabel='Silhueta média',xticks=range(2,7),title='Perfis conjuntos dos dois poluentes');ax.legend(frameon=False)
    save(fig,'Geral_Comparacao_agrupamentos','Separação interna dos perfis com seis indicadores. A silhueta não mede concordância observado–modelado.')
    for period in PERIODS:
        fig,axes=plt.subplots(1,2,figsize=(9,3.7),layout='constrained')
        for ax,pol in zip(axes,POLLS):
            s=limits[limits.period.eq(period)&limits.pollutant.eq(pol)&limits.basis.eq('density_tpy_km2')];f=table[pol,period]
            ax.scatter(f.emission_density,f.concentration,s=6,c=f.quintile.map(lambda v:QUINT['Q'+str(v)]),alpha=.65,linewidths=0)
            for r in s.drop_duplicates('percentile_target').itertuples():
                if np.isfinite(r.cut_all_data):ax.axvline(r.cut_all_data,color='#405b64',ls='--',lw=.6)
                ax.axhline(r.concentration_cut,color='#405b64',ls=':',lw=.5)
            ax.set_xscale('symlog',linthresh=.001);ax.set_yscale('log');ax.set(xlim=(0,None),xlabel='Emissão anual (t/ano/km²)',ylabel='Concentração (µg/m³)',title=PN[pol])
        save(fig,f'Geral_{period}_Limiares','Associação entre densidade anual inventariada e o indicador de concentração. Quatro alvos de concentração e seus cortes de emissão, sujeitos à validação espacial. Se não forem ordenados e distintos, não se afirmam cinco faixas associativas de emissão.')
        fig,axes=plt.subplots(1,2,figsize=(8,3.6),layout='constrained')
        for ax,pol in zip(axes,POLLS):
            s=limits[limits.period.eq(period)&limits.pollutant.eq(pol)&limits.basis.eq('density_tpy_km2')]
            ax.boxplot([s[s.percentile_target.eq(p)].cut_train.dropna() for p in [20,40,60,80]],tick_labels=['P20','P40','P60','P80'],patch_artist=True,boxprops=dict(facecolor='#94c7c5'),medianprops=dict(color='#194f68'))
            ax.set_yscale('symlog',linthresh=.01);ax.set(title=PN[pol],ylabel='Corte (t/ano/km²)')
        save(fig,f'Geral_{period}_Estabilidade_limiares','Variação dos cortes nos dez ajustes em blocos espaciais de 2 e 4 km. Não são intervalos de confiança de emissões autorizáveis.')
    summary=json.loads((DATA/'resumo.json').read_text(encoding='utf8'))
    counts=pd.DataFrame([dict(Poluente=PN[r['pollutant']],Indicador=LABEL[r['period']],Receptores=r['n_receptors'],Zonas=311,HH=r['lisa_counts'].get('Alto–alto',0),Prioritarios=r['management_counts'].get('Prioridade receptora',0),Moran_I=round(r['global_moran']['I'],3),Cinco_faixas_E='Sim' if r['five_emission_bands_identifiable'] else 'Não') for r in summary['cases']])
    sections=[]
    for name,caption in catalog.items():
        sections.append(f'<section id="{name}"><h2>{html.escape(name.replace("_"," "))}</h2><a href="figuras/{name}.svg"><img loading="lazy" src="figuras/{name}.svg"></a><p>{html.escape(caption)}</p><p><a href="figuras/{name}.pdf">PDF vetorial</a> · <a href="figuras/{name}.png">PNG</a></p></section>')
    intro='''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Cenário geral · meteorologia completa</title><style>body{font:16px/1.6 Arial;max-width:1120px;margin:30px auto;padding:0 22px;color:#183d4c}img{width:100%;height:auto}section{margin-top:40px;border-top:1px solid #dbe3e5}a{color:#176b88}table{border-collapse:collapse;font-size:13px}td,th{padding:7px;border-bottom:1px solid #ddd}</style><h1>Cenário geral · meteorologia completa</h1><p>MP10 e MP2,5 em 2021-2023, sem recorte por direção do vento, hora do dia ou estação do ano. Os máximos de 1 h e 24 h são envelopes por receptor e podem ocorrer em datas diferentes. A análise anual usa a média das três médias anuais nativas, preservando a avaliação de longa duração.</p><p>O cenário diário inclui todos os dias válidos, inclusive aqueles sem direção persistente. Mantêm-se os filtros meteorológicos, o mínimo de 18 horas por dia e a exclusão W732. O dia técnico de 2024 não participa. As médias de 24 h foram reconstruídas de 1 h e conferidas contra o POST nativo.</p><p>As classes relativas, clusters e limiares associativos são instrumentos exploratórios. Não substituem a avaliação normativa, não corrigem o viés do modelo e não definem emissões permissíveis. Foram preservados os dados de entrada e a simulação original.</p><p><a href="../vento/analises_espaciais/index.html">Cenários por direção</a> · <a href="../figuras/index.html">Índice geral</a> · <a href="abc_por_regiao.html">ABC de cada região</a> · <a href="zoneamento_geral.csv">311 zonas</a> · <a href="regioes_gerais.csv">Regiões e cobertura</a> · <a href="limiares_cinco_faixas.csv">Limiares e validação</a> · <a href="sensibilidade_espacial.csv">Estabilidade</a> · <a href="LEIA_ME_metodologia.md">Métodos</a> · <a href="auditoria_final.json">Auditoria</a></p>'''
    navigation='<details><summary>Localizar uma análise</summary><ul>'+''.join(f'<li><a href="#{k}">{html.escape(k.replace("_"," "))}</a></li>' for k in catalog)+'</ul></details>'
    (DATA/'index.html').write_text(intro+counts.to_html(index=False,border=0)+navigation+''.join(sections)+'</html>',encoding='utf8')
    (OUT/'legendas.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf8')
    for p,link in [(ROOT/'figuras/index.html','../cenario_geral/index.html'),(ROOT/'vento/analises_espaciais/index.html','../../cenario_geral/index.html')]:
        text=p.read_text(encoding='utf8');entry=f'<p><a href="{link}">Cenário geral com meteorologia completa · 1 h, 24 h e anual</a></p>'
        if entry not in text:text=text.replace('</h1>','</h1>'+entry,1)
        p.write_text(text,encoding='utf8')
    from visualizar_abc_direcional import run as abc_view
    abc_view(DATA)
    print('Galeria do cenário geral concluída:',len(catalog),'figuras',flush=True)

if __name__=='__main__':
    import sys
    run(concentrations_only='--concentrations-only' in sys.argv)
