# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/projeto/0_ref/seminarios_02/Resumo_Inventario_Congonhas_2023-R1.xlsx | pd.read_excel.
# Campos/chaves em inv: key, matched_geometry, row, tpy.
# Campos/chaves em ids.loc: group.
# Campos/chaves em inv.loc: tpy.
# Campos/chaves em out.loc: emission_total_gs, inventory_match, inventory_row, line_rate_gs_m, source_area_m2, source_length_m.
# Saída: {output}/{pol}_{name}.csv | table.to_csv.
# Campos/chaves gerados em inv: description, group, key, matched_geometry, row, tpy.
# Campos/chaves gerados em out: emission_annual_tpy, emission_basis, emission_total_gs, inventory_coordinate_distance_m, inventory_match, inventory_row, inventory_source_id, model_emission_total_gs.
# Campos/chaves gerados em audit: inventory_file, inventory_year.
# Campos/chaves gerados em alloc: emission_tpy.
# Campos/chaves gerados em mass: emission_audit_status, emission_fallback_tpy, emission_inventory_pending_sources, emission_inventory_tpy.
# Campos/chaves gerados em balance: allocated_tpy, overlap_warning, rate_basis, source_total_tpy, unallocated_tpy.
# CÓDIGO DO PROCESSAMENTO

"""Vínculo conservador do inventário anual com geometrias Lakes existentes.

Não associa por proximidade nem transfere o total de empresas para cada zona.
Somente ID exato ou descrição única dentro do mesmo empreendimento.
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

import numpy as np
import pandas as pd
import config
from groups import canonical_group,norm_token

PATH=config.BASE/'inventario/Resumo_Inventario_Congonhas_2023-R1.xlsx'
if not PATH.exists():PATH=config.BASE/'0_ref/seminarios_02/Resumo_Inventario_Congonhas_2023-R1.xlsx'

# Apply inventory
def apply_inventory(sources,pol):
    inv=pd.read_excel(PATH,header=None)
    assert inv.iloc[0,22]=='Taxa de Emissão [ton/ano]'
    col={'PM10':23,'PM25':24}[pol]
    expected={'PM10':'MP10','PM25':'MP2,5'}[pol]
    assert inv.iloc[1,col]==expected
    inv=inv.iloc[2:].copy();inv['row']=inv.index+1
    inv['key']=inv[4].map(norm_token)
    inv['group']=inv[3].map(canonical_group)
    inv.loc[inv[1].eq('Emissão Urbana'),'group']='URB'
    inv['description']=inv[5].map(norm_token)
    inv['tpy']=pd.to_numeric(inv[col],errors='coerce')
    if inv.key.duplicated().any():raise ValueError('IDs duplicados no inventário')
    ids=inv.set_index('key');desc={}
    for key,sub in inv.groupby(['group','description']):
        if len(sub)==1:desc[key]=sub.iloc[0]
    out=sources.copy();out['inventory_row']=np.nan;out['inventory_source_id']=''
    out['inventory_match']='sem correspondência inequívoca'
    out['inventory_coordinate_distance_m']=np.nan
    out['model_emission_total_gs']=out.emission_total_gs
    for idx,r in out.iterrows():
        key=norm_token(r.source_id);match=None;basis=''
        if key in ids.index and ids.loc[key,'group']==r.group_id:
            match=ids.loc[key];basis='ID exato e grupo'
        elif (r.group_id,norm_token(r.desc)) in desc:
            match=desc[(r.group_id,norm_token(r.desc))];basis='descrição única no grupo'
        if match is not None and pd.notna(match.tpy) and match.tpy>=0:
            out.loc[idx,['inventory_row','inventory_source_id','inventory_match']]=[match.row,match[4],basis]
    out['emission_annual_tpy']=out.emission_total_gs*31.536
    out['emission_basis']='AERMOD anualizado 8760 h; conferir inventário'
    for row,sub in out.dropna(subset=['inventory_row']).groupby('inventory_row'):
        total=float(inv.loc[inv.row.eq(row),'tpy'].iloc[0])

        weights=sub.model_emission_total_gs.clip(lower=0)
        if len(sub)>1 and (not np.isfinite(weights).all() or weights.sum()<=0):

            if sub.geometry.geom_type.isin(['Polygon','MultiPolygon']).all():
                weights=sub.geometry.area
            elif sub.geometry.geom_type.isin(['LineString','MultiLineString']).all():
                weights=sub.geometry.length
            else:
                out.loc[sub.index,'inventory_match']='partição sem pesos válidos; mantida taxa AERMOD'
                continue
            if not np.isfinite(weights).all() or weights.sum()<=0:
                out.loc[sub.index,'inventory_match']='partição sem medida geométrica válida'
                continue
            out.loc[sub.index,'inventory_match']=out.loc[sub.index,'inventory_match']+'; partição por medida geométrica'
        weights=weights/weights.sum() if len(sub)>1 else pd.Series(1.,index=sub.index)

        from shapely.geometry import Point
        from shapely.ops import unary_union
        inventory_record=inv.loc[inv.row.eq(row)].iloc[0]
        x=pd.to_numeric(inventory_record[6],errors='coerce')
        y=pd.to_numeric(inventory_record[7],errors='coerce')
        if np.isfinite(x) and np.isfinite(y):
            distance=unary_union(sub.geometry.tolist()).distance(Point(x,y))
            out.loc[sub.index,'inventory_coordinate_distance_m']=distance
            if distance>5000:
                out.loc[sub.index,'inventory_match']='divergência espacial >5 km; mantida taxa AERMOD'
                continue
        out.loc[sub.index,'emission_annual_tpy']=total*weights
        out.loc[sub.index,'emission_basis']='Inventário 2023 t/ano'

    out['emission_total_gs']=out.emission_annual_tpy/31.536
    polygon=out.geometry.geom_type.isin(['Polygon','MultiPolygon'])
    line=out.geometry.geom_type.isin(['LineString','MultiLineString'])
    out.loc[polygon,'surface_rate_gs_m2']=out.loc[polygon,'emission_total_gs']/out.loc[polygon,'source_area_m2']
    out.loc[line,'line_rate_gs_m']=out.loc[line,'emission_total_gs']/out.loc[line,'source_length_m']

    sel=line&out.source_type.eq('RLINEXT')
    out.loc[sel,'emission_rate_native']=out.loc[sel,'line_rate_gs_m']
    audit=out.drop(columns='geometry').copy()
    audit['inventory_file']=str(PATH);audit['inventory_year']=2023
    inv['matched_geometry']=inv.row.isin(out.loc[out.emission_basis.eq('Inventário 2023 t/ano'),'inventory_row'])
    missing=inv.loc[inv.tpy.gt(0)&~inv.matched_geometry,[0,3,4,5,'row','tpy','group']].copy()
    missing.columns=['municipality','enterprise','inventory_id','description','inventory_row','tpy','group_id']
    return out,audit,missing

# Calculate zone emissions
def calculate_zone_emissions(sources,zones,pol,output):
    """Inventário anual conciliado; resíduos ficam explícitos, sem alterar POSTFILES."""
    from aermod_sources import allocate_emissions_to_zones,emission_mass_balance_audit
    from methodology_rules import group_mass_classes
    from pathlib import Path
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    sources,audit,missing=apply_inventory(sources,pol)
    _,alloc=allocate_emissions_to_zones(sources,zones)
    meta=sources.set_index('source_id')
    for col in ('inventory_source_id','inventory_row','inventory_match','emission_basis'):
        alloc[col]=alloc.source_id.map(meta[col])
    alloc['emission_tpy']=alloc.allocated_fraction*alloc.source_id.map(meta.emission_annual_tpy)
    mass,groups=group_mass_classes(alloc,zones.index,pol,annualization_basis='inventario_conciliado')
    mass['emission_inventory_tpy']=alloc.loc[alloc.emission_basis.eq('Inventário 2023 t/ano')].groupby('zone_index').emission_tpy.sum().reindex(zones.index,fill_value=0)
    mass['emission_fallback_tpy']=mass.emission_total_tpy-mass.emission_inventory_tpy
    mass['emission_inventory_pending_sources']=len(missing)
    mass['emission_audit_status']='Inventário conciliado parcialmente; consultar fontes pendentes'
    balance=emission_mass_balance_audit(sources,alloc)
    balance['source_total_tpy']=balance.emission_total_gs*31.536
    balance['allocated_tpy']=balance.allocated_gs*31.536
    balance['unallocated_tpy']=balance.unallocated_gs*31.536
    balance['overlap_warning']=balance.allocated_pct.gt(100.000001)
    balance['rate_basis']='g/s equivalente da massa anual; não substitui entrada AERMOD'
    for name,table in [('alocacao_fontes',alloc),('massa_grupo_zona',groups),('balanco_massa',balance),('conciliacao_inventario',audit),('inventario_sem_geometria_conciliada',missing)]:
        table.to_csv(output/f'{pol}_{name}.csv',index=False,encoding='utf-8-sig')
    return mass,groups,alloc,audit,missing
