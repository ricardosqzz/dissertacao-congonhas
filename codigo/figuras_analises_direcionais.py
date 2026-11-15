# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/projeto/output/16_revisao_pos_banca/vento/{pol}_envelopes_{'horarios' if period == '1h' else 'diarios_persistentes'}.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/zoneamento_pos_banca.gpkg | gpd.read_file.
# Entrada: E:/projeto/output/16_revisao_pos_banca/celulas_analise.gpkg | gpd.read_file.
# Entrada: E:/projeto/output/11_integracao/apendices/resumo_figuras.json | .read_text.
# Entrada: E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/resumo.json | .read_text.
# Entrada: E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/comparacao_agrupamentos.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/correlogramas.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/limiares_cinco_faixas.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/regioes_direcionais.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/ABC_contribuicoes_regioes.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/perfis_normalizados_grupos_estacoes.csv | pd.read_csv.
# Entrada: E:/projeto/output/15_auditoria_metodologica/revisao_cientifica/vinculos_estacoes_receptores.csv | pd.read_csv.
# Entrada: E:/projeto/output/11_integracao/nova_modelagem/estacoes_trienio_comum.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/{pol}_{period}_receptores.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/figuras/catalogo_{pol}_{period}.json | .read_text.
# Entrada: E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/PM10_1h_receptores.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/figuras/index.html | main.read_text.
# Campos/chaves em table.loc: concentration.
# Campos/chaves em raw: direction.
# Campos/chaves em table: concentration, direction, dominant_group, period, pollutant, quintile, quintile_reference_union, receptor_id.
# Campos/chaves em cells: geometry, receptor_id.
# Campos/chaves em v: name.
# Campos/chaves em eligible: n_design_years, pollutant.
# Campos/chaves em limits: basis, direction, period, pollutant.
# Campos/chaves em abc: label, period, pollutant, region_type.
# Campos/chaves em regions: area_km2, concentration_area_mean, region_id.
# Campos/chaves em joint_table: direction.
# Campos/chaves em corr: direction, period, pollutant.
# Campos/chaves em cluster: direction, method.
# Campos/chaves em r: direction, five_emission_bands_identifiable, lisa_counts, management_counts, period, pollutant.
# Campos/chaves em summary: cases.
# Campos/chaves em counts: five_emission_bands, pollutant.
# Saída: E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/figuras/{name}.{ext} | fig.savefig.
# Saída: E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/{pol}_{period}_cortes_comuns.csv | .to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/{pol}_{period}_referencia_comum.json | .write_text.
# Saída: {fig} | save.
# Saída: E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/figuras/catalogo_{polls[0]}_{periods[0]}.json | .write_text.
# Saída: E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/figuras/legendas.json | .write_text.
# Saída: E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/index.html | .write_text.
# Saída: E:/projeto/output/16_revisao_pos_banca/figuras/index.html | main.write_text.
# Campos/chaves gerados em table: quintile_reference_union.
# Campos/chaves gerados em f: Q, Q_common, best_cluster_label, dominant_name, label, ward4_label.
# Campos/chaves gerados em opts: station_overlay.
# Campos/chaves gerados em joined: weighted_C.
# Campos/chaves gerados em plot: Demais grupos.
# Campos/chaves gerados em counts: five_emission_bands, pollutant.
# receptor_id: identificador do receptor.
# concentration: concentração do período em µg/m³.
# CÓDIGO DO PROCESSAMENTO

"""Pranchas das análises de cada direção no encarte cartográfico consolidado."""
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
import argparse,sys,subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
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

ROOT=config.BASE/'output/16_revisao_pos_banca'
DATA=ROOT/'vento/analises_espaciais'
OUT=DATA/'figuras'
DIRS=['N','NE','L','SE','S','SO','O','NO']
QUINT={f'Q{i}':c for i,c in enumerate(['#b8dce9','#a9d7b6','#f2dc87','#ee9d58','#ce4147'],1)}
LISA={'Alto–alto':'#ce4147','Baixo–baixo':'#377ea3','Alto–baixo':'#e3a279','Baixo–alto':'#84bdb5','Não significativo':'#e3e3df'}
MATRIX={'Demais C / Demais E':'#d8e1de','Demais C / Alta E':'#428e99','Alta C / Demais E':'#e69a52','Alta C / Alta E':'#894f78'}
ROLES={'Prioridade receptora':'#ce4147','Controle de fontes':'#478c9c','Menor impacto relativo':'#a9d3b8','Acompanhamento':'#e9d295'}
NETWORK={'Prioridade: cobertura ≥50%':'#287c90','Prioridade: cobertura <50%':'#e2a357','Demais áreas':'#e3e7e2'}
CLUSTERS={f'Grupo {i}':c for i,c in enumerate(['#d1e5e3','#8bc5bc','#47a4a5','#467f9d','#a287b2','#bb695d'],1)}

# Save
def save(fig,name,caption,catalog):
    for ext in ['svg','png','pdf']:fig.savefig(OUT/f'{name}.{ext}',dpi=450,bbox_inches='tight',facecolor='white')
    plt.close(fig);catalog[name]=caption

# Concentration maps
def concentration_maps(pol,period,z,muni,extent,table):
    """Receptores externos sustentam a interpolação junto à divisa municipal."""
    old_out=cart.OUT;cart.OUT=ROOT/'figuras'
    raw=pd.read_csv(ROOT/'vento'/f'{pol}_envelopes_{"horarios" if period=="1h" else "diarios_persistentes"}.csv')
    field='max_1h' if period=='1h' else 'daily_from_1h'
    positive=table.loc[table.concentration>0,'concentration']
    low=max(10.**np.floor(np.log10(positive.quantile(.02))),.01);cap=float(positive.quantile(.99));unit=10.**np.floor(np.log10(cap));cap=max(10*low,np.floor(cap/unit)*unit);norm=LogNorm(low,cap)
    ticks=np.unique(np.r_[low,np.power(10.,np.arange(np.ceil(np.log10(low)),np.floor(np.log10(cap))+1)),cap])
    surfaces=[]
    for direction in DIRS:
        f=raw[raw.direction.eq(direction)].copy()
        geo=gpd.GeoSeries(gpd.points_from_xy(f.X,f.Y),crs=z.crs).to_crs(4674)
        surfaces.append(dict(x=geo.x.to_numpy(),y=geo.y.to_numpy(),values=f[field].to_numpy(),limits=[low,cap],norm=norm,cmap=concentration_cmap(),ticks=ticks,actual_max=float(table.concentration.max())))
    cart.render(z,muni,['concentration']*8,'PB15_'+pol+'_'+period,['Vento de '+v for v in DIRS],'',extent,surfaces=surfaces,panel_shape=(4,2),zone_layer=z,atlas_scale=440000,figure_title=('MP₁₀' if pol=='PM10' else 'MP₂,₅')+' · concentrações máximas '+period)
    cart.OUT=old_out

# Run
def run(polls=None,periods=None,worker=False,finalize_only=False):
    OUT.mkdir(parents=True,exist_ok=True);cart.OUT=OUT
    z=gpd.read_file(ROOT/'zoneamento_pos_banca.gpkg');cells=gpd.read_file(ROOT/'celulas_analise.gpkg')
    muni=gpd.GeoDataFrame(geometry=[z.geometry.union_all()],crs=z.crs)
    extent=json.loads((config.BASE/'output/11_integracao/apendices/resumo_figuras.json').read_text(encoding='utf8'))['bounds_degrees']
    summary=json.loads((DATA/'resumo.json').read_text(encoding='utf8'))
    catalog={};title=lambda pol:'MP₁₀' if pol=='PM10' else 'MP₂,₅'
    cluster=pd.read_csv(DATA/'comparacao_agrupamentos.csv');corr=pd.read_csv(DATA/'correlogramas.csv');limits=pd.read_csv(DATA/'limiares_cinco_faixas.csv')
    regions=pd.read_csv(DATA/'regioes_direcionais.csv');abc=pd.read_csv(DATA/'ABC_contribuicoes_regioes.csv')
    present=pd.read_csv(ROOT/'perfis_grupos/perfis_normalizados_grupos_estacoes.csv')[['pollutant','station_id']].drop_duplicates()
    stations=pd.read_csv(config.BASE/'output/15_auditoria_metodologica/revisao_cientifica/vinculos_estacoes_receptores.csv').merge(present,on=['pollutant','station_id'],validate='one_to_one')
    eligible=pd.read_csv(config.BASE/'output/11_integracao/nova_modelagem/estacoes_trienio_comum.csv')
    for period in ([] if finalize_only else (periods or ['1h','24h'])):
        for pol in (polls or ['PM10','PM25']):
            table=pd.read_csv(DATA/f'{pol}_{period}_receptores.csv');layers=[]
            union_peak=table.groupby('receptor_id').concentration.max()
            reference_cuts=np.quantile(union_peak,[.2,.4,.6,.8])
            table['quintile_reference_union']=np.searchsorted(reference_cuts,table.concentration,side='left')+1
            table[['receptor_id','pollutant','period','direction','concentration','quintile','quintile_reference_union']].to_csv(DATA/f'{pol}_{period}_cortes_comuns.csv',index=False)
            (DATA/f'{pol}_{period}_referencia_comum.json').write_text(json.dumps(dict(pollutant=pol,period=period,reference='Quintis do envelope união das oito direções, nos 1008 receptores',cuts=reference_cuts.tolist()),ensure_ascii=False,indent=2),encoding='utf8')
            for direction in DIRS:
                f=cells[['receptor_id','geometry']].merge(table[table.direction.eq(direction)],on='receptor_id',validate='one_to_one')
                f['Q']=f.quintile.map(lambda v:'Q'+str(v));f['dominant_name']=f.dominant_group.map({k:v['name'] for k,v in GROUPS.items()})
                f['Q_common']=f.quintile_reference_union.map(lambda v:'Q'+str(v))
                f['best_cluster_label']=f.best_cluster.map(lambda v:'Grupo '+str(v));f['ward4_label']=f.ward4.map(lambda v:'Grupo '+str(v))
                layers.append(f)
            common=dict(panel_layers=layers,panel_shape=(4,2),zone_layer=z,atlas_scale=440000)
            stem=f'{pol}_{period}'
            specs=[('Quintis','Q',QUINT,'Quintis dos máximos condicionados à direção, com P20/P40/P60/P80 recalculados em cada direção. As cores expressam posições relativas e não o atendimento a padrões.'),
                   ('Quintis_referencia_comum','Q_common',QUINT,'Os quatro cortes são os quintis do envelope união das oito direções, para o mesmo poluente e duração. Eles permanecem fixos nos oito painéis, permitindo comparar a magnitude relativa entre direções. No produto de 24 h, a união considera os dias de direção persistente.'),
                   ('Moran_local','lisa',LISA,'Moran local de log(1+C), oito vizinhos, 999 permutações condicionais bilaterais e ajuste BH nominal de 5% em cada mapa. Cinza não significa ausência de concentração. A correção adicional conjunta dos oito campos direcionais está nas tabelas.'),
                   ('Moran_bivariado','bivariate',LISA,'Moran local bivariado entre concentração do envelope e densidade anual de emissão na vizinhança. Não representa uma trajetória de transporte ou emissão do evento.'),
                   ('Emissao_concentracao','matrix',MATRIX,'Alta concentração acima de P80 de cada envelope; alta emissão acima do corte associativo treinado para esse alvo. Massa anual inventariada, sem transformar o corte em emissão permissível.'),
                   ('Regioes_gestao','management',ROLES,'Papéis propostos de gestão. A prioridade receptora está acima de P80; controle de fontes destaca emissão elevada fora dessa faixa. Classes relativas ao cenário e direção.'),
                   ('Cobertura_prioridades','network_priority',NETWORK,'Regiões de prioridade receptora com pelo menos 50% ou menos de 50% da área dentro dos entornos de 4 km das estações elegíveis em 2021-2023. Pontos são as estações. O raio é uma aproximação do estudo, sem demonstrar representatividade física uniforme.'),
                   ('Grupo_predominante','dominant_name',cart.COLORS,'Grupo com maior contribuição no mesmo horário ou dia do máximo ALL de cada receptor. AEX e subgrupos urbanos não disputam com as empresas e Urbano Total, para evitar dupla contagem.')]
            for name,field,palette,caption in specs:
                name_full=f'{stem}_{name}';categories=list(palette) if name!='Grupo_predominante' else sorted(set(table.dominant_group.map({k:v['name'] for k,v in GROUPS.items()})))
                opts={}
                if name=='Cobertura_prioridades':
                    st=stations[stations.pollutant.eq(pol)].copy();st=st[st.station_id.isin(eligible[eligible.pollutant.eq(pol)&eligible.n_design_years.eq(3)].station_id)]
                    sg=gpd.GeoDataFrame(st,geometry=gpd.points_from_xy(st.X,st.Y),crs=cells.crs);opts['station_overlay']=[sg]*8
                cart.render(z,muni,[field]*8,name_full,['Vento de '+v for v in DIRS],'',extent,palette=palette,legend_categories=categories,filename=name_full,figure_title=title(pol)+' · '+period+' · '+name.replace('_',' '),**common,**opts)
                catalog[name_full]=caption
                print('Prancha',name_full,flush=True)

            concentration_maps(pol,period,z,muni,extent,table)

            fig,axs=plt.subplots(4,2,figsize=(8.27,11.69),layout='constrained')
            for ax,direction in zip(axs.ravel(),DIRS):
                f=table[table.direction.eq(direction)];lim=limits[limits.pollutant.eq(pol)&limits.period.eq(period)&limits.direction.eq(direction)&limits.basis.eq('density_tpy_km2')]
                ax.scatter(f.emission_density,f.concentration,s=5,c=f.quintile.map(lambda v:QUINT['Q'+str(v)]),alpha=.65,linewidths=0)
                for _,r in lim.drop_duplicates('percentile_target').iterrows():
                    if np.isfinite(r.cut_all_data):ax.axvline(r.cut_all_data,color='#405b64',lw=.55,ls='--')
                    ax.axhline(r.concentration_cut,color='#405b64',lw=.45,ls=':')
                ax.set_xscale('symlog',linthresh=.001);ax.set_yscale('log');ax.set_xlim(left=0);ax.set(title='Vento de '+direction,xlabel='Emissão anual (t/ano/km²)',ylabel='Concentração (µg/m³)');ax.tick_params(labelsize=7)
            fig.suptitle(title(pol)+' · '+period+' · associação emissão e concentração',fontweight='bold')
            save(fig,stem+'_Limiares','Cada ponto corresponde a um receptor e sua célula. As linhas mostram os alvos de concentração e os cortes associativos de emissão. Cortes podem coincidir ou não ser crescentes; nesse caso não se afirmam cinco classes de emissão identificáveis.',catalog)
            fig,axs=plt.subplots(4,2,figsize=(8.27,11.69),layout='constrained')
            for ax,direction in zip(axs.ravel(),DIRS):
                ss=limits[limits.pollutant.eq(pol)&limits.period.eq(period)&limits.direction.eq(direction)&limits.basis.eq('density_tpy_km2')]
                data=[ss[ss.percentile_target.eq(v)].cut_train.dropna() for v in [20,40,60,80]]
                ax.boxplot(data,tick_labels=['P20','P40','P60','P80'],patch_artist=True,boxprops=dict(facecolor='#94c7c5'),medianprops=dict(color='#194f68'))
                ax.set_yscale('symlog',linthresh=.01);ax.set(title='Vento de '+direction,ylabel='Corte (t/ano/km²)');ax.tick_params(labelsize=7)
            fig.suptitle(title(pol)+' · '+period+' · estabilidade dos cortes',fontweight='bold')
            save(fig,stem+'_Estabilidade_limiares','Variação dos cortes nos dez ajustes de treino em blocos de 2 e 4 km. Não são intervalos de confiança de uma emissão autorizável.',catalog)

            sub=abc[abc.pollutant.eq(pol)&abc.period.eq(period)&abc.region_type.eq('gestao')&abc.label.eq('Prioridade receptora')]
            joined=sub.merge(regions[['region_id','area_km2','concentration_area_mean']],on='region_id',validate='many_to_one')
            joined['weighted_C']=joined.contribution*joined.area_km2;contribution=joined.groupby(['direction','group_name']).weighted_C.sum().unstack(fill_value=0).reindex(DIRS)
            shares=100*contribution.div(contribution.sum(axis=1),axis=0)
            top=contribution.sum().nlargest(6).index.tolist();plot=shares[top].copy();plot['Demais grupos']=shares.drop(columns=top).sum(axis=1)
            fig,ax=plt.subplots(figsize=(9,4.4),layout='constrained');left=np.zeros(8);colors=['#247c96','#64ada8','#bdc77c','#d6b06a','#b77f79','#8c83aa','#d9e1de']
            for group,color in zip(plot.columns,colors):ax.barh(DIRS,plot[group],left=left,label=group,color=color);left+=plot[group].to_numpy()
            ax.set(xlim=(0,100),xlabel='Contribuição nas regiões prioritárias (%)',ylabel='Direção de origem do vento');ax.invert_yaxis()
            fig.set_layout_engine(None);fig.subplots_adjust(left=.12,right=.99,top=.98,bottom=.31)
            handles,_=ax.get_legend_handles_labels();cart.centered_legend(fig,handles,ncol=3,y=.16,fontsize=9,row_step=.055,center=.535)
            save(fig,stem+'_Contribuicoes_prioridades','Razão das contribuições ponderadas pela área nas regiões acima de P80 em cada direção. A ABC de cada região está no CSV. Os máximos selecionados não são simultâneos entre receptores.',catalog)
    if worker:
        (OUT/f'catalogo_{polls[0]}_{periods[0]}.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf8')
        return
    if finalize_only:
        for pol in ['PM10','PM25']:
            for period in ['1h','24h']:
                catalog.update(json.loads((OUT/f'catalogo_{pol}_{period}.json').read_text(encoding='utf8')))

    joint_table=pd.read_csv(DATA/'PM10_1h_receptores.csv')
    for field,caption in [('best_cluster','Agrupamento com melhor silhueta entre Ward e k-means, K de 2 a 6, usando os máximos de 1 h e 24 h dos dois poluentes. Os grupos podem ser espacialmente descontínuos.'),
                          ('ward4','Solução Ward com quatro grupos, mantida como comparação ao agrupamento de melhor silhueta.')]:
        layers=[]
        for direction in DIRS:
            f=cells[['receptor_id','geometry']].merge(joint_table[joint_table.direction.eq(direction)],on='receptor_id',validate='one_to_one');f['label']=f[field].map(lambda v:'Grupo '+str(v));layers.append(f)
        name='Conjunto_'+field
        categories=sorted(set(v for f in layers for v in f.label))
        cart.render(z,muni,['label']*8,name,['Vento de '+v for v in DIRS],'',extent,panel_layers=layers,panel_shape=(4,2),zone_layer=z,atlas_scale=440000,palette=CLUSTERS,legend_categories=categories,filename=name,figure_title='Agrupamentos · dois poluentes · máximos 1 h e 24 h')
        catalog[name]=caption
    for period in ['1h','24h']:
        fig,axs=plt.subplots(4,2,figsize=(8.27,11.69),layout='constrained')
        for ax,direction in zip(axs.ravel(),DIRS):
            for pol,color,marker in [('PM10','#176b88','o'),('PM25','#bd5b4b','s')]:
                ss=corr[corr.period.eq(period)&corr.direction.eq(direction)&corr.pollutant.eq(pol)]
                ax.plot((ss.min_distance_m+ss.max_distance_m)/2000,ss.I,marker+'-',ms=3,lw=1.1,label=title(pol),color=color)
            ax.axhline(0,color='#777',ls=':',lw=.6);ax.set(title='Vento de '+direction,xlabel='Distância média da banda (km)',ylabel='Moran I');ax.tick_params(labelsize=8)
        axs.ravel()[0].legend(frameon=False,fontsize=8);fig.suptitle('Correlogramas · máximos '+period,fontweight='bold')
        save(fig,'Correlogramas_'+period,'Moran em bandas de 750 m até 7,5 km, com 199 permutações por banda. Mostra a escala de associação do envelope, sem estimar sozinho uma distância de transporte de fontes.',catalog)
    fig,axs=plt.subplots(4,2,figsize=(8.27,11.69),layout='constrained')
    for ax,direction in zip(axs.ravel(),DIRS):
        for method,color in [('ward','#176b88'),('kmeans','#bd5b4b')]:
            ss=cluster[cluster.direction.eq(direction)&cluster.method.eq(method)];ax.plot(ss.k,ss.silhouette,'o-',ms=3,label=method,color=color)
        ax.set(title='Vento de '+direction,xlabel='Número de grupos',ylabel='Silhueta média',xticks=range(2,7));ax.tick_params(labelsize=8)
    axs.ravel()[0].legend(frameon=False,fontsize=8);fig.suptitle('Separação dos agrupamentos por direção',fontweight='bold')
    save(fig,'Comparacao_agrupamentos','Silhueta interna para Ward e k-means, K=2 a 6. Não representa concordância do AERMOD com as observações.',catalog)
    (OUT/'legendas.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf8')
    sections=[]
    for name,caption in catalog.items():
        sections.append('<section id="'+name+'"><h2>'+html.escape(name.replace('_',' '))+'</h2><a href="figuras/'+name+'.svg"><img loading="lazy" src="figuras/'+name+'.svg"></a><p>'+html.escape(caption)+'</p><p><a href="figuras/'+name+'.pdf">PDF</a> · <a href="figuras/'+name+'.png">PNG</a></p></section>')
    intro='''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Análises por direção do vento</title><style>body{font:16px/1.6 Arial;max-width:1120px;margin:30px auto;padding:0 22px;color:#183d4c}img{width:100%;height:auto}section{margin-top:40px;border-top:1px solid #dbe3e5}a{color:#176b88}table{border-collapse:collapse;font-size:13px}td,th{padding:6px;border-bottom:1px solid #ddd}</style><h1>Análises dos piores cenários por direção do vento</h1><p>Os 32 campos correspondem a oito direções, dois poluentes e duas durações. Os máximos de cada receptor podem ocorrer em datas distintas. Todos os testes numéricos usam os receptores originais. A interpolação aparece apenas nas pranchas de concentração.</p><p>Percentis e limiares são recalculados em cada direção. A emissão é a massa anual inventariada, e não uma massa estimada para o evento. Os cortes associativos não são limites de emissão. As participações dos grupos são recuperadas no mesmo horário ou dia do máximo ALL em cada receptor.</p><p><a href="../../figuras/index.html">Índice geral</a> · <a href="../../perfis_grupos/index.html">Séries nas estações</a> · <a href="zoneamento_direcional.csv">311 zonas em cada campo</a> · <a href="regioes_direcionais.csv">Regiões e cobertura da rede</a> · <a href="ABC_contribuicoes_regioes.csv">ABC e contribuições</a> · <a href="limiares_cinco_faixas.csv">Limiares e validação</a> · <a href="sensibilidade_espacial.csv">Estabilidade espacial e anual</a></p>'''
    counts=pd.DataFrame([dict(pollutant=r['pollutant'],period=r['period'],direction=r['direction'],HH=r['lisa_counts'].get('Alto–alto',0),priority=r['management_counts'].get('Prioridade receptora',0),five_emission_bands=r['five_emission_bands_identifiable']) for r in summary['cases']])
    counts['pollutant']=counts.pollutant.map({'PM10':'MP₁₀','PM25':'MP₂,₅'});counts['five_emission_bands']=counts.five_emission_bands.map({True:'Sim',False:'Não'})
    counts=counts.rename(columns={'pollutant':'Poluente','period':'Duração','direction':'Vento','priority':'Receptores prioritários','five_emission_bands':'Cinco faixas de emissão'})
    navigation='<details><summary>Localizar uma análise</summary><ul>'+''.join('<li><a href="#'+k+'">'+html.escape(k.replace('_',' '))+'</a></li>' for k in catalog)+'</ul></details>'
    (DATA/'index.html').write_text(intro+'<p><a href="LEIA_ME_metodologia.md">Métodos e interpretação dos resultados</a></p>'+navigation+counts.to_html(index=False,border=0)+''.join(sections)+'</html>',encoding='utf8')
    main=ROOT/'figuras/index.html';content=main.read_text(encoding='utf8');link='<p><a href="../vento/analises_espaciais/index.html">Análises espaciais completas dos oito cenários direcionais, para os dois poluentes e durações</a></p>'
    if link not in content:content=content.replace('</h1>','</h1>'+link,1)
    main.write_text(content,encoding='utf8');print('Pranchas direcionais e índices concluídos.',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--worker',nargs=2,metavar=('POL','PERIOD'));parser.add_argument('--plume',nargs=2);parser.add_argument('--plumes-only',action='store_true');parser.add_argument('--finalize-only',action='store_true');args=parser.parse_args()
    if args.plume:
        pol,period=args.plume;z=gpd.read_file(ROOT/'zoneamento_pos_banca.gpkg');muni=gpd.GeoDataFrame(geometry=[z.geometry.union_all()],crs=z.crs)
        extent=json.loads((config.BASE/'output/11_integracao/apendices/resumo_figuras.json').read_text(encoding='utf8'))['bounds_degrees']
        concentration_maps(pol,period,z,muni,extent,pd.read_csv(DATA/f'{pol}_{period}_receptores.csv'))
    elif args.worker:run([args.worker[0]],[args.worker[1]],worker=True)
    elif args.finalize_only:run(finalize_only=True)
    else:
        jobs=[(p,t) for p in ['PM10','PM25'] for t in ['1h','24h']]
        def execute(job):
            subprocess.run([sys.executable,str(Path(__file__).resolve()),'--plume' if args.plumes_only else '--worker',*job],check=True,cwd=Path(__file__).parent)
        with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(execute,jobs))
        if not args.plumes_only:run(finalize_only=True)
