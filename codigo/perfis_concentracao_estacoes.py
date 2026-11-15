# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/projeto/wrf/AERMET-3Y.SFC | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/periodos_secos_meteorologicos.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/dados_series/{pol}_basilica.js | .read_text.
# Entrada: E:/projeto/output/16_revisao_pos_banca/figuras/index.html | p.read_text.
# Entrada: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/distancias_grupos_estacoes.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/grupos_fontes_horarias_e_estaticas.csv | pd.read_csv.
# Entrada: E:/projeto/output/09_projeto_dissertacao/seminarios_02/apresentacao/apoio_meteorologia_perfis/pares_horarios_{pol}.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/perfis_normalizados_grupos_estacoes.csv | pd.read_csv.
# Entrada: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/{pol}_{group}_cache.json | .read_text.
# Entrada: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/{pol}_{g}_estacoes.csv.gz | pd.read_csv.
# Campos/chaves em wd: count, sum.
# Campos/chaves em config.DIRS: cache.
# Campos/chaves em daily: count, sum.
# Campos/chaves em payload: daily, groups, observed, profiles, stats.
# Campos/chaves em p: mean, p10, p90.
# Campos/chaves em periods: source.
# Campos/chaves em v: name.
# Campos/chaves em observed: station_id.
# Campos/chaves em metadata: stations.
# Campos/chaves em full_observed: CODE, station_id.
# Campos/chaves em check: observed.
# Campos/chaves em profiles.loc: group_id.
# Campos/chaves em profiles: pollutant.
# Campos/chaves em selected: 1H.
# Campos/chaves em obs_daily: count, mean.
# Campos/chaves em md: count, mean.
# Campos/chaves em paired: dry, modelled, observed.
# Campos/chaves em pr: mean, p10, p90.
# Campos/chaves em season_table: group_id.
# Saída: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/precipitacao_diaria_estacoes.csv | wide.to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/periodos_secos_meteorologicos.csv | periods.to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/precipitacao_referencia_diaria.csv | ref.to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/precipitacao_mensal_conferencia.csv | bymonth.to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/figuras/PB17_perfis_grupos.{ext} | fig.savefig.
# Saída: E:/projeto/output/16_revisao_pos_banca/figuras/index.html | p.write_text.
# Saída: Argumento fornecido pelo chamador | .to_json.
# Saída: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/dados_series/{key}.js | .write_text.
# Saída: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/Concentracoes_{pol}_{sid}.{ext} | fig.savefig.
# Saída: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/perfis_concentracao_por_estacao_grupo.csv | .to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/comparacao_periodo_seco_grupos_estacoes.csv | season_table.to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/sintese_seco_demais_dias_ALL.csv | selected.to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/metodologia_periodo_seco.json | .write_text.
# Saída: E:/projeto/output/16_revisao_pos_banca/perfis_grupos/dados_series/metadados.js | .write_text.
# Campos/chaves gerados em s: day, rain.
# Campos/chaves gerados em raw: PP, day.
# Campos/chaves gerados em ref: dry_WRF, dry_regional.
# Campos/chaves gerados em caps: PB17_perfis_grupos.
# Campos/chaves gerados em cal: dry.
# Campos/chaves gerados em metadata: distances, flags.
# Campos/chaves gerados em full_observed: CODE.
# Campos/chaves gerados em : observed.
# Campos/chaves gerados em data: modelled.
# Campos/chaves gerados em p: group_id, pollutant, season, station_id.
# CÓDIGO DO PROCESSAMENTO

"""Séries absolutas e sazonalidade meteorológica, com os dados já auditados."""
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
import re
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import config
from groups import GROUPS
from medias_horarias_verificadas import met_calendar,identity

ROOT=config.BASE/'output/16_revisao_pos_banca'
OUT=ROOT/'perfis_grupos'
LABELS={'basilica':'Basílica','j-prof':'Jardim Profeta','lobo-leite':'Lobo Leite','matriz':'Matriz','motas':'Motas','n-plat':'Nova Plataforma','pires':'Pires'}
DRY_COLOR='#f3deb5'

# Dry interval
def dry_interval(series,reference):
    """Maior queda cronológica da anomalia acumulada P - referência."""
    values=series.to_numpy(float)
    if not np.isfinite(values).all():raise ValueError('Não inferir estação seca preenchendo chuva ausente com zero')
    anomaly=np.r_[0,np.cumsum(values-reference)]
    end=int(np.argmax(np.maximum.accumulate(anomaly)-anomaly))
    if end==0:raise ValueError('Sem intervalo de déficit pluviométrico')
    start=int(np.argmax(anomaly[:end]))
    return start,end,float(anomaly[start]-anomaly[end])

# Meteorology
def meteorology():
    sfc=config.BASE/'wrf/AERMET-3Y.SFC';s=pd.read_csv(sfc,sep=r'\s+',skiprows=1,header=None);s=s[s[0].between(21,23)].copy()
    s['day']=pd.to_datetime(dict(year=s[0]+2000,month=s[1],day=s[2]))

    s['rain']=s[21].where(s[20].ne(99)&s[21].between(0,500))
    wd=s.groupby('day').rain.agg(['sum','count']);wd.loc[wd['count']<18,'sum']=np.nan
    path=config.DIRS['cache']/'monitoramento_mma/horas.pkl.gz';raw=pd.read_pickle(path)
    raw=raw[raw.datetime.dt.year.between(2021,2023)].copy()

    raw['day']=(raw.datetime-pd.Timedelta(hours=3)).dt.floor('D')
    raw=raw[raw.day.dt.year.between(2021,2023)]
    raw['PP']=raw.PP.where(raw.PP.between(0,500))
    daily=raw.groupby(['station_id','day']).PP.agg(['sum','count']);daily.loc[daily['count']<18,'sum']=np.nan
    wide=daily['sum'].unstack('station_id').dropna(axis=1,how='all')
    calendar=pd.date_range('2021-01-01','2023-12-31',freq='D',name='day');wide=wide.reindex(calendar)
    n=wide.count(axis=1);regional=wide.median(axis=1).where(n>=3)
    if regional.isna().any():raise ValueError('Chuva regional insuficiente; revisar antes de sombrear automaticamente')
    ref=pd.DataFrame({'observed_regional_mm':regional,'n_rain_stations':n,'WRF_SFC_mm':wd['sum']}).reindex(calendar)
    wide.to_csv(OUT/'precipitacao_diaria_estacoes.csv')
    intervals=[]
    for source,column in [('Rede regional','observed_regional_mm'),('WRF/SFC','WRF_SFC_mm')]:
        baseline=ref[column].mean()
        for year,g in ref[column].groupby(ref.index.year):
            a,b,deficit=dry_interval(g,baseline)
            intervals.append(dict(source=source,year=int(year),start=str(g.index[a].date()),end=str(g.index[b-1].date()),duration_days=b-a,deficit_mm=deficit,reference_mm_day=baseline,rain_interval_mm=float(g.iloc[a:b].sum())))
    periods=pd.DataFrame(intervals);periods.to_csv(OUT/'periodos_secos_meteorologicos.csv',index=False)
    ref['dry_regional']=False;ref['dry_WRF']=False
    for r in periods.itertuples():ref.loc[r.start:r.end,'dry_regional' if r.source=='Rede regional' else 'dry_WRF']=True
    ref.to_csv(OUT/'precipitacao_referencia_diaria.csv')
    bymonth=ref.groupby([ref.index.year,ref.index.month]).agg(regional_mm=('observed_regional_mm','sum'),WRF_mm=('WRF_SFC_mm','sum'),minimum_stations=('n_rain_stations','min'))
    bymonth.to_csv(OUT/'precipitacao_mensal_conferencia.csv')
    return ref,periods,dict(regional_source=identity(path),SFC=identity(sfc),rain_stations=wide.columns.tolist(),
         method='Maior queda da anomalia acumulada diária em cada ano, relativa à média diária 2021-2023. Mediana de >=3 estações com >=18 horas de precipitação por dia. Não é climatologia de 30 anos.',
         literature=['https://www.frontiersin.org/journals/earth-science/articles/10.3389/feart.2017.00014/full','https://www.scielo.br/j/rbmet/a/wnJMXG9LspR78p3wtddZWNm/?lang=en'],
         clock='Hipótese UTC das observações convertida para UTC-3, ainda pendente de confirmação documental.',
         rainfall_valid_independent_of_dispersion='Chuva válida em horas de calmaria também é utilizada.')

# Numeric
def numeric(values):
    return [None if not np.isfinite(v) else round(float(v),4) for v in values]

# Clean json
def clean_json(value):
    if isinstance(value,dict):return {k:clean_json(v) for k,v in value.items()}
    if isinstance(value,list):return [clean_json(v) for v in value]
    if isinstance(value,(float,np.floating)) and not np.isfinite(value):return None
    return value

# Summary figure
def summary_figure():
    """Figura corrente substitui a antiga comparação somente normalizada."""
    periods=pd.read_csv(OUT/'periodos_secos_meteorologicos.csv')
    fig,axs=plt.subplots(4,2,figsize=(12,9),layout='constrained')
    for col,pol in enumerate(['PM10','PM25']):
        text=(OUT/f'dados_series/{pol}_basilica.js').read_text(encoding='utf8');payload=json.loads(text[text.index(']=')+2:-1])
        date=pd.date_range('2021-01-01',periods=26280,freq='h')
        for row,key,color,label in [(0,'observed','#1b657e','Observado'),(1,'modelled','#bd4e48','Modelado · ALL')]:
            p=payload['profiles']['ALL']['Total'][key];h=np.arange(24);ax=axs[row,col]
            ax.fill_between(h,np.array(p['p10'],float),np.array(p['p90'],float),color=color,alpha=.18);ax.plot(h,p['mean'],color=color,lw=1.7)
            ax.set(title=('MP₁₀' if pol=='PM10' else 'MP₂,₅')+' · '+label,xlabel='Hora inicial',ylabel='Concentração (µg/m³)',xticks=range(0,24,3),ylim=(0,None));ax.grid(alpha=.15)
        for row,values,color,label in [(2,payload['observed'],'#1b657e','Série observada'),(3,payload['groups']['ALL'],'#bd4e48','Série modelada · ALL')]:
            ax=axs[row,col]
            for r in periods[periods.source.eq('Rede regional')].itertuples():ax.axvspan(pd.Timestamp(r.start),pd.Timestamp(r.end)+pd.Timedelta(days=1),color=DRY_COLOR,alpha=.65)
            ax.plot(date,np.array(values,float),color=color,lw=.35);ax.set(title=label,ylabel='Concentração (µg/m³)',ylim=(0,None));ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6));ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'));ax.grid(alpha=.15)
    for ext in ['svg','png','pdf']:fig.savefig(ROOT/f'figuras/PB17_perfis_grupos.{ext}',dpi=450,bbox_inches='tight')
    plt.close(fig)
    caption='Basílica, 2021-2023. Perfis em concentração absoluta nas mesmas horas pareadas, com P10-P90, e séries horárias completas. Painéis observado e modelado possuem eixos verticais próprios. Sombreado indica o período menos chuvoso identificado pela precipitação regional. Todos os grupos e estações estão disponíveis no visualizador. Hipótese de relógio pendente de confirmação.'
    p=ROOT/'figuras/legendas.json';caps=json.loads(p.read_text(encoding='utf8'));caps['PB17_perfis_grupos']=caption;p.write_text(json.dumps(caps,ensure_ascii=False,indent=2),encoding='utf8')
    p=ROOT/'figuras/index.html';s=p.read_text(encoding='utf8')
    s=re.sub(r'<section[^>]*>\s*<h2>[^<]*PB17[^<]*</h2>.*?</section>','',s,flags=re.S)
    s+='<section><h2>PB17 Concentrações e séries na Basílica</h2><a href="PB17_perfis_grupos.svg"><img loading="lazy" src="PB17_perfis_grupos.svg"></a><p>'+caption+'</p><p><a href="../perfis_grupos/index.html">Explorar todos os grupos e estações</a></p></section>'
    p.write_text(s,encoding='utf8')

# Run
def run():
    OUT.mkdir(exist_ok=True,parents=True);assets=OUT/'dados_series';assets.mkdir(exist_ok=True)
    rain,periods,met=meteorology();cal,_=met_calendar()
    times=pd.to_datetime((cal.CODE//100).astype(str),format='%y%m%d')+pd.to_timedelta(cal.CODE%100-1,unit='h')
    cal=cal.assign(datetime=times,daydate=times.dt.floor('D'));cal['dry']=cal.daydate.map(rain.dry_regional).fillna(False)
    allcodes=cal.CODE.to_numpy();calendar_index=pd.Index(allcodes);metadata={'stations':{},'names':{'ALL':'Todas as fontes',**{k:v['name'] for k,v in GROUPS.items()}},'station_names':LABELS,'periods':periods.to_dict('records'),'start':'2021-01-01','hours':len(cal),'rain':{'observed':numeric(rain.observed_regional_mm),'model':numeric(rain.WRF_SFC_mm)},'meteorology':met}
    metadata['distances']=json.loads(pd.read_csv(OUT/'distancias_grupos_estacoes.csv').to_json(orient='records'))
    metadata['flags']=json.loads(pd.read_csv(OUT/'grupos_fontes_horarias_e_estaticas.csv').to_json(orient='records'))
    full_observed=pd.read_pickle(config.DIRS['cache']/'monitoramento_mma/horas.pkl.gz')
    clock=full_observed.datetime-pd.Timedelta(hours=3)
    full_observed['CODE']=(((clock.dt.year%100*100+clock.dt.month)*100+clock.dt.day)*100+clock.dt.hour+1).astype('int64')
    allprofiles=[];seasons=[]
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    for pol in ['PM10','PM25']:
        observed=pd.read_csv(config.BASE/f'output/09_projeto_dissertacao/seminarios_02/apresentacao/apoio_meteorologia_perfis/pares_horarios_{pol}.csv',usecols=['station_id','CODE','observed'])
        station_ids=sorted(observed.station_id.unique());metadata['stations'][pol]=station_ids
        check=observed.merge(full_observed[['station_id','CODE',pol]],on=['station_id','CODE'],validate='one_to_one')
        if len(check)!=len(observed) or not np.allclose(check.observed,check[pol],equal_nan=True):
            raise ValueError('Mudança de relógio ou de valores em relação aos pares auditados')
        profiles=pd.read_csv(OUT/'perfis_normalizados_grupos_estacoes.csv')
        group_ids=sorted(profiles.loc[profiles.pollutant.eq(pol),'group_id'].unique())
        from out_aermod_reader import discover
        selected,_=discover(config.BASE/f'out-aermod/{"PM10" if pol=="PM10" else "PM2-5"}')
        for group in group_ids:
            stamp=json.loads((OUT/f'{pol}_{group}_cache.json').read_text())
            if stamp!=identity(selected[group,'1H']):
                raise ValueError('POST alterado: executar diagnosticar_perfis_grupos.py ou a opção --perfis-grupos antes do visualizador')
        cached={g:pd.read_csv(OUT/f'{pol}_{g}_estacoes.csv.gz',usecols=['CODE','station_id','modelled']) for g in group_ids}
        for sid in station_ids:
            obs=full_observed[full_observed.station_id.eq(sid)].set_index('CODE')[pol].reindex(allcodes).to_numpy()
            payload={'observed':numeric(obs),'groups':{},'profiles':{},'daily':{'observed':[],'groups':{}},'stats':{}}
            data=pd.DataFrame({'datetime':cal.datetime,'day':cal.daydate,'hour':cal.CODE%100-1,'dry':cal.dry,'observed':obs})
            obs_daily=data.groupby('day')['observed'].agg(['mean','count']);payload['daily']['observed']=numeric(obs_daily['mean'].where(obs_daily['count']>=config.MONITOR_MIN_VALID_HOURS_DAY))
            for group,cache in cached.items():
                model=cache[cache.station_id.eq(sid)].set_index('CODE').modelled.reindex(allcodes).to_numpy()
                data['modelled']=model;payload['groups'][group]=numeric(model)
                md=data.groupby('day').modelled.agg(['mean','count']);payload['daily']['groups'][group]=numeric(md['mean'].where(md['count']>=18))
                paired=data.dropna(subset=['observed','modelled'])
                payload['profiles'][group]={}
                for season,sub in [('Total',paired),('Período seco',paired[paired.dry]),('Demais dias',paired[~paired.dry])]:
                    prof=sub.groupby('hour')[['observed','modelled']].mean().reindex(range(24));low=sub.groupby('hour')[['observed','modelled']].quantile(.1).reindex(range(24));high=sub.groupby('hour')[['observed','modelled']].quantile(.9).reindex(range(24));maximum=sub.groupby('hour')[['observed','modelled']].max().reindex(range(24))
                    payload['profiles'][group][season]={}
                    for variable in ['observed','modelled']:
                        payload['profiles'][group][season][variable]={'mean':numeric(prof[variable]),'p10':numeric(low[variable]),'p90':numeric(high[variable]),'max':numeric(maximum[variable])}
                    p=prof.reset_index();p['pollutant']=pol;p['station_id']=sid;p['group_id']=group;p['season']=season;allprofiles.append(p)
                    seasons.append(dict(pollutant=pol,station_id=sid,group_id=group,season=season,n_pairs=len(sub),observed_mean=sub.observed.mean(),modelled_mean=sub.modelled.mean(),observed_max=sub.observed.max(),modelled_max=sub.modelled.max(),hourly_r=sub.observed.corr(sub.modelled)))
                stats={'paired_hours':len(paired),'observed_mean':float(paired.observed.mean()),'modelled_mean':float(paired.modelled.mean()),'observed_max':float(paired.observed.max()),'modelled_max':float(paired.modelled.max()),'hourly_r':float(paired.observed.corr(paired.modelled))}
                payload['stats'][group]=stats
            key=pol+'_'+sid
            (assets/f'{key}.js').write_text('window.PERFIS=window.PERFIS||{};window.PERFIS['+json.dumps(key)+']='+json.dumps(clean_json(payload),ensure_ascii=False,allow_nan=False,separators=(',',':'))+';',encoding='utf8')

            if 'ALL' in payload['groups']:
                model=np.array([np.nan if v is None else v for v in payload['groups']['ALL']])
                fig,axs=plt.subplots(4,1,figsize=(10,9),layout='constrained',gridspec_kw={'height_ratios':[1,1,1.3,1.3]})
                for ax,var,color,title in [(axs[0],'observed','#1b657e','Observado'),(axs[1],'modelled','#bd4e48','Modelado · ALL')]:
                    pr=payload['profiles']['ALL']['Total'][var];h=np.arange(24);ax.fill_between(h,np.array(pr['p10'],float),np.array(pr['p90'],float),color=color,alpha=.18);ax.plot(h,pr['mean'],color=color,lw=1.7);ax.set(title=title,xlabel='Hora inicial do intervalo',ylabel='Concentração (µg/m³)',xticks=range(0,24,3),ylim=(0,None));ax.grid(alpha=.15)
                for ax,values,color,title in [(axs[2],obs,'#1b657e','Série horária observada'),(axs[3],model,'#bd4e48','Série horária modelada · ALL')]:
                    for r in periods[periods.source.eq('Rede regional')].itertuples():ax.axvspan(pd.Timestamp(r.start),pd.Timestamp(r.end)+pd.Timedelta(days=1),color=DRY_COLOR,alpha=.65,zorder=0)
                    ax.plot(cal.datetime,values,color=color,lw=.35);ax.set(title=title,ylabel='Concentração (µg/m³)',ylim=(0,None));ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4));ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'));ax.grid(alpha=.15)
                fig.suptitle(('MP₁₀' if pol=='PM10' else 'MP₂,₅')+' · '+LABELS.get(sid,sid),fontweight='bold')
                for ext in ['svg','png','pdf']:fig.savefig(OUT/f'Concentracoes_{pol}_{sid}.{ext}',dpi=450,bbox_inches='tight')
                plt.close(fig)
            print(pol,sid,'concentrações e séries completas preparadas',flush=True)
    pd.concat(allprofiles).to_csv(OUT/'perfis_concentracao_por_estacao_grupo.csv',index=False)
    season_table=pd.DataFrame(seasons);season_table.to_csv(OUT/'comparacao_periodo_seco_grupos_estacoes.csv',index=False)
    selected=season_table[season_table.group_id.eq('ALL')].pivot(index=['pollutant','station_id'],columns='season',values=['observed_mean','modelled_mean','n_pairs'])
    selected.to_csv(OUT/'sintese_seco_demais_dias_ALL.csv')
    (OUT/'metodologia_periodo_seco.json').write_text(json.dumps(met,ensure_ascii=False,indent=2),encoding='utf8')
    (assets/'metadados.js').write_text('const META='+json.dumps(metadata,ensure_ascii=False,allow_nan=False,separators=(',',':'))+';',encoding='utf8')

    from perfis_concentracao_viewer import write_viewer
    write_viewer(OUT,metadata)
    summary_figure()
    print('Perfis em concentração, séries horárias e diagnóstico pluviométrico concluídos.',flush=True)

if __name__=='__main__':run()
