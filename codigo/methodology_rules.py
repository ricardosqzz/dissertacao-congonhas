# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entradas: argumentos do chamador e módulos locais relacionados no relatório.
# Campos/chaves em a: annual_hours, emission_tpy.
# Campos/chaves em sub.loc: emission_tpy, group_id.
# Campos/chaves em daily: CONC, X, Y, date.
# Campos/chaves em row: ANNUAL_MODEL, P98_MODEL.
# Campos/chaves em lim: 24H, ANNUAL.
# Saídas: retorno de funções, verificações ou arquivos definidos pelo chamador.
# Campos/chaves gerados em a: _annual_hours, emission_gs, emission_tpy, group_id.
# Campos/chaves gerados em groups: annual_hours_max, annual_hours_min, annualization_basis, emission_class, high_emission, minor_threshold_tpy, threshold_tpy.
# Campos/chaves gerados em d: CONC, date, quarter, year.
# Campos/chaves gerados em result: MIN_QUARTER_COMPLETENESS, VALID_YEAR.
# X: coordenada leste em metros.
# Y: coordenada norte em metros.
# CÓDIGO DO PROCESSAMENTO

"""Regras compartilhadas do seminário; não executa simulações nem grava arquivos."""
from __future__ import annotations
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


import numpy as np
import pandas as pd
from standards import STANDARDS, STAGE_ORDER

MINOR_TPY = {'PM10':5., 'PM25':3., 'PTS':10., 'CO':10.,
             'NOX':10., 'SOX':10., 'COVNM':5.}

# Group mass classes
def group_mass_classes(allocations, zone_ids, pollutant, *, annual_hours=8760.,
                       annualization_basis='cenario_continuo'):
    """MMA 2026 §3.4 adaptado ao grupo dentro da zona; >100 t/ano é alta.

    Entrada: taxas TOTAIS em g/s, já convertidas da unidade nativa da fonte.
    Sem calendário, 8760 h é cenário contínuo, NÃO emissão real/potencial máximo.
    A coluna annual_hours, quando presente, prevalece por fonte. Sua ausência
    não deve ser preenchida silenciosamente dentro de uma coluna existente.
    Zero significa sem emissão alocada, não ausência real de fontes.
    """
    minor=MINOR_TPY[pollutant.upper()]
    if annualization_basis not in ('cenario_continuo','efetiva','potencial_maximo','inventario_conciliado'):
        raise ValueError('Base de anualização não reconhecida.')
    if annualization_basis in ('efetiva','potencial_maximo') and 'annual_hours' not in allocations:
        raise ValueError('Emissão efetiva/potencial exige calendário documentado por fonte.')
    zone_ids=list(zone_ids)
    a=allocations.copy()
    if a.zone_index.isna().any() or not a.zone_index.isin(zone_ids).all():
        raise ValueError('Alocação com zona ausente ou fora da lista de zonas.')
    a['group_id']=a.group_id.fillna('NAO_IDENTIFICADO')
    a['emission_gs']=pd.to_numeric(a.emission_gs,errors='raise')
    if (~np.isfinite(a.emission_gs) | (a.emission_gs<0)).any():
        raise ValueError('Emissão inválida; não substituir ausência por zero.')
    hours=pd.to_numeric(a['annual_hours'],errors='raise') if 'annual_hours' in a else pd.Series(annual_hours,index=a.index,dtype=float)
    if (~np.isfinite(hours)|(hours<0)|(hours>8784)).any():
        raise ValueError('Horas anuais inválidas; máximo de 8784 para ano bissexto.')
    if annualization_basis=='inventario_conciliado':
        a['emission_tpy']=pd.to_numeric(a['emission_tpy'],errors='raise')
        if (~np.isfinite(a.emission_tpy)|(a.emission_tpy<0)).any():
            raise ValueError('Massa anual inválida no inventário conciliado.')
        a['_annual_hours']=np.nan
    else:
        a['emission_tpy']=a.emission_gs*hours*3600./1_000_000.
        a['_annual_hours']=hours
    groups=a.groupby(['zone_index','group_id'],as_index=False)[['emission_gs','emission_tpy']].sum()
    groups['threshold_tpy']=100.
    groups['minor_threshold_tpy']=minor
    groups['annualization_basis']=annualization_basis
    groups['annual_hours_min']=a.groupby(['zone_index','group_id'])._annual_hours.min().to_numpy()
    groups['annual_hours_max']=a.groupby(['zone_index','group_id'])._annual_hours.max().to_numpy()

    groups['high_emission']=(groups.emission_tpy>100)&~np.isclose(groups.emission_tpy,100,rtol=0,atol=1e-10)
    mid=(groups.emission_tpy>minor)&~np.isclose(groups.emission_tpy,minor,rtol=0,atol=1e-10)
    groups['emission_class']=np.select([groups.high_emission,mid,groups.emission_tpy.gt(0)],
                                     ['Majoritária','Intermediária','Minoritária'],default='Sem emissão alocada')
    unidentified=groups.group_id.eq('NAO_IDENTIFICADO')&groups.emission_tpy.gt(0)
    groups.loc[unidentified,'emission_class']='Informação insuficiente'
    groups.loc[unidentified,'high_emission']=False
    rows=[]
    for zid in zone_ids:
        sub=groups[groups.zone_index==zid].sort_values(['emission_tpy','group_id'],ascending=[False,True])
        mx=float(sub.emission_tpy.max()) if len(sub) else 0.0
        unknown=float(sub.loc[sub.group_id.eq('NAO_IDENTIFICADO'),'emission_tpy'].sum())
        total=float(sub.emission_tpy.sum())
        high=total>100 and not np.isclose(total,100,rtol=0,atol=1e-10)
        rows.append({'zone_index':zid,'emission_total_gs':float(sub.emission_gs.sum()),
                     'emission_max_group_gs':float(sub.emission_gs.max()) if len(sub) else 0.,
                     'emission_total_tpy':float(sub.emission_tpy.sum()),'emission_max_group_tpy':mx,
                     'emission_threshold_tpy':100.,'emission_minor_threshold_tpy':minor,
                     'emission_annualization_basis':annualization_basis,
                     'emission_unidentified_tpy':unknown,
                     'emission_high':True if high else pd.NA if unknown>0 else False,
                     'emission_dominant_group':' | '.join(sub.loc[sub.emission_tpy.eq(mx)&sub.emission_tpy.gt(0),'group_id']),
                     'emission_high_groups':' | '.join(sub.loc[sub.high_emission,'group_id']),
                     'emission_class':'Majoritária' if high else 'Informação insuficiente' if unknown>0 else 'Intermediária' if total>minor else 'Minoritária' if total>0 else 'Sem emissão alocada'})
    return pd.DataFrame(rows).set_index('zone_index'),groups

# Concentration priority
def concentration_priority(statuses):
    """P0–P5 da menor à maior superação; lacuna impede classe conclusiva."""
    values=[statuses.get(stage) for stage in STAGE_ORDER]
    if any(v not in ('atendimento','nao_atendimento') for v in values):
        return 'Informação insuficiente'
    return 'P'+str(max([0]+[i for i,v in enumerate(values,1) if v=='nao_atendimento']))

# Add zone priorities
def add_zone_priorities(zones, pollutant):
    """Usa a classificação espacial já calculada, não sua média descritiva."""
    z=zones.copy()
    z[f'{pollutant}_concentration_priority']=[concentration_priority(
        {s:r[f'{pollutant}_{s}_status'] for s in STAGE_ORDER}) for _,r in z.iterrows()]
    return z

# Model annual metrics
def model_annual_metrics(daily):
    """Indicadores pareados por receptor/ano; 75% em CADA trimestre."""
    from standards import annual_p98
    d=daily[['X','Y','date','CONC']].copy()
    d['date']=pd.to_datetime(d.date).dt.normalize()
    if d.duplicated(['X','Y','date']).any():raise ValueError('Receptor/data duplicado entre POSTFILEs.')
    d['CONC']=pd.to_numeric(d.CONC,errors='coerce')
    d.loc[~np.isfinite(d.CONC)|(d.CONC<0),'CONC']=np.nan
    d['year']=d.date.dt.year;d['quarter']=d.date.dt.quarter
    result=d.groupby(['X','Y','year']).agg(ANNUAL_MEAN=('CONC','mean'),P98=('CONC',annual_p98),N_DAYS=('CONC','count'))
    counts=d.groupby(['X','Y','year','quarter']).CONC.count().unstack('quarter').reindex(columns=[1,2,3,4],fill_value=0).fillna(0)
    for quarter in range(1,5):
        expected=[(pd.Timestamp(int(y),quarter*3,1)+pd.offsets.MonthEnd(0)-pd.Timestamp(int(y),quarter*3-2,1)).days+1 for y in counts.index.get_level_values('year')]
        counts[quarter]=counts[quarter]/np.asarray(expected)
    result['MIN_QUARTER_COMPLETENESS']=counts.min(axis=1)
    result['VALID_YEAR']=result.MIN_QUARTER_COMPLETENESS.ge(.75)
    return result.reset_index()

# Model period metrics
def model_period_metrics(yearly, years, pollutant):
    """Janela explícita, sem procurar outro ano para substituir lacunas."""
    years=tuple(years); rows=[]
    for (x,y),sub in yearly.groupby(['X','Y'],sort=False):
        sub=sub.set_index('year').reindex(years)
        valid=sub.VALID_YEAR.eq(True)&np.isfinite(sub.ANNUAL_MEAN)&np.isfinite(sub.P98)
        complete=bool(valid.all())
        row={'X':x,'Y':y,'n_model_years':int(valid.sum()),'years_model':','.join(map(str,years)),
             'ANNUAL_MODEL':float(sub.ANNUAL_MEAN.mean()) if complete else np.nan,
             'P98_MODEL':float(sub.P98.mean()) if complete else np.nan}
        for scenario in ('PV',)+STAGE_ORDER:
            lim=STANDARDS[pollutant][scenario]
            row['status_'+scenario]='insuficiente' if not complete else 'nao_atendimento' if row['ANNUAL_MODEL']>lim['ANNUAL'] or row['P98_MODEL']>lim['24H'] else 'atendimento'
        rows.append(row)
    return pd.DataFrame(rows)

# Abc classes
def abc_classes(values, a_limit=80.0, b_limit=95.0):
    """Inclui o grupo que cruza o limite; empates exatos ficam na mesma classe.

    A classificação usa o acumulado ANTES do bloco de valores empatados.
    A entrada deve estar em ordem decrescente, como nas tabelas ABC existentes.
    Zero fica em C; ausência, negativo e infinito não são contribuições válidas.
    """
    if not 0 < a_limit < b_limit < 100:
        raise ValueError('Limites ABC devem satisfazer 0 < A < B < 100.')
    v=np.asarray(values,dtype=float)
    if np.any(~np.isfinite(v)) or np.any(v<0):
        raise ValueError('Contribuições devem ser finitas e não negativas.')
    if np.any(np.diff(v)>0):
        raise ValueError('Ordene as contribuições de forma decrescente.')
    if not len(v) or v.sum()<=0:
        return np.full(len(v),'insuficiente',dtype=object)
    result=[];before=0.0
    for i,x in enumerate(v):
        if i==0 or x!=v[i-1]:
            cls='C' if x==0 else ('A' if before<a_limit-1e-10 else 'B' if before<b_limit-1e-10 else 'C')
        result.append(cls)
        before+=100.0*x/v.sum()
    return np.asarray(result,dtype=object)

# Rolling station metrics
def rolling_station_metrics(yearly, start_year=2018, end_year=None):
    """Uma linha por estação/poluente/janela; nunca pula anos inválidos.

    Consome a tabela anual validada de stations.station_yearly_metrics.
    Não transforma ausência de dados em atendimento e não cria anos futuros.
    """
    if yearly is None or yearly.empty:return pd.DataFrame()
    keys=['station_id','pollutant','year']
    if yearly.duplicated(keys).any():raise ValueError('Estação/poluente/ano duplicado.')
    observed_end=int(yearly.year.max())
    last=observed_end if end_year is None else int(end_year)
    rows=[]
    for (sid,pol),group in yearly.groupby(keys[:2],sort=True):
        if pol not in STANDARDS:continue
        byyear=group.set_index('year')
        for end in range(start_year+2,last+1):
            years=list(range(end-2,end+1));d=byyear.reindex(years)
            valid=d.valid_year.eq(True) & d.annual_mean.notna() & d.p98.notna()
            valid &= np.isfinite(d.annual_mean) & np.isfinite(d.p98)
            complete=bool(valid.all())
            ann=float(d.annual_mean.mean()) if complete else np.nan
            p98=float(d.p98.mean()) if complete else np.nan
            r={'station_id':sid,'pollutant':pol,'start_year':end-2,'end_year':end,
               'period':f'{end-2}-{end}','n_design_years':int(valid.sum()),
               'years_valid':','.join(str(y) for y in years) if complete else '',
               'ANNUAL_3YR':ann,'P98_3YR':p98}
            for scenario in ('PV',)+STAGE_ORDER:
                lim=STANDARDS[pol][scenario]
                r['status_'+scenario]='insuficiente' if not complete else 'nao_atendimento' if ann>lim['ANNUAL'] or p98>lim['24H'] else 'atendimento'
            rows.append(r)
    return pd.DataFrame(rows)
