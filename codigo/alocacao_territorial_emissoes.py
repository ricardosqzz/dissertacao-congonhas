# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/projeto/config.DIRS['out']/14_auditoria_entradas/revalidacao_final/validacao_final.json | validation.read_text.
# Entrada: E:/projeto/entrada_aermod/{name} | path.read_bytes.
# Entrada: E:/projeto/config.DIRS['out']/13_rateio_emissoes/Resumo_zonas.csv | pd.read_csv.
# Entrada: E:/projeto/config.DIRS['out']/11_integracao/zoneamento_integrado.gpkg | gpd.read_file.
# Entrada: E:/projeto/config.DIRS['out']/14_auditoria_entradas/revalidacao_final/Massas_fontes_2021_2023.csv | pd.read_csv.
# Entrada: E:/projeto/config.DIRS['out']/14_auditoria_entradas/revalidacao_final/fontes_correntes.json | .read_text.
# Campos/chaves em config.DIRS: out.
# Campos/chaves em evidence: arquivos.
# Campos/chaves em source: source_type.
# Campos/chaves em table: poluente.
# Campos/chaves em r: id, poluente.
# Campos/chaves em masses: poluente.
# Campos/chaves em rec: inventario_ids, status.
# Campos/chaves em zones.loc: nome.
# Campos/chaves em a: zona.
# Campos/chaves em sub.loc: massa_zona_t_ano.
# Campos/chaves em tables: Balanco_fontes, Resumo_zonas.
# Campos/chaves em report: classes.
# Saída: E:/projeto/config.DIRS['out']/13_rateio_emissoes/{name}.csv | table.to_csv.
# Saída: Argumento fornecido pelo chamador | table.to_json.
# Saída: E:/projeto/config.DIRS['out']/13_rateio_emissoes/tabelas_planilha.json | .write_text.
# Saída: E:/projeto/config.DIRS['out']/13_rateio_emissoes/auditoria_rateio.json | .write_text.
# Campos/chaves gerados em report: classes.
# CÓDIGO DO PROCESSAMENTO

"""Rateio territorial auditável, com classificação principal pela soma da zona.

Produz uma revisão separada; não substitui concentrações nem mapas publicados.
Geometrias de rateio são distintas das usadas na conversão da taxa nativa.
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
import json
import hashlib
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString, GeometryCollection
from shapely.ops import unary_union
from aermod_sources import build_source_gdf,read_lakes_sources,_coord_pairs,_clean_geometry,source_geometry
from inventario_anual import apply_inventory
from groups import GROUPS
import config

LINE_TYPES={'LINE','LINE_AREA','LINE_VOLUME','RLINE','RLINEXT'}

# Refined sources
def refined_sources(pol,name):
    """Geometrias atuais e massas integradas; não reutiliza planilhas antigas."""
    path=config.BASE/'entrada_aermod'/name
    validation=config.DIRS['out']/'14_auditoria_entradas/revalidacao_final/validacao_final.json'
    evidence=json.loads(validation.read_text(encoding='utf8'))
    filepol='PM2-5' if pol=='PM25' else pol
    assert hashlib.sha256(path.read_bytes()).hexdigest()==evidence['arquivos'][filepol]['sha256'],'Entrada alterada após validação: executar validar_massas_entrada.py'
    raw=read_lakes_sources(path).set_index('ID',drop=False)
    sources=build_source_gdf(path,pol)
    assert set(raw.index)==set(sources.source_id),'Fonte sem geometria deve ser investigada'
    return raw,sources

# Geometry for allocation
def geometry_for_allocation(source,raw):
    typ=source['source_type'];coords=_coord_pairs(raw)
    if typ=='POINT':
        return (Point(coords[0]),'ponto') if coords else (None,'ponto ausente')
    if typ in LINE_TYPES:
        if len(coords)<2:return None,'eixo linear ausente'

        line=unary_union(LineString(coords))
        return (line,'comprimento') if line.length>0 else (None,'eixo linear degenerado')
    if typ=='AREA_CIRC':

        radius=raw.get('Radius',raw.get('Diam'))
        if coords and pd.notna(radius) and radius>0:
            return Point(coords[0]).buffer(float(radius),quad_segs=64),'área'
    if typ in ('AREA','AREA_POLY'):
        geom=_clean_geometry(source_geometry(raw))
        if geom is not None and geom.geom_type in ('Polygon','MultiPolygon') and geom.area>0:
            return geom,'área'
    geom=_clean_geometry(source.geometry)
    if geom is not None and geom.geom_type in ('Polygon','MultiPolygon') and geom.area>0:
        return geom,'área horizontal' if typ=='VOLUME' else 'área'
    return None,'projeção horizontal ausente'

# Partition
def partition(geom,zones,basis):
    """Retorna parcelas únicas e resíduos sem normalizar ou duplicar sobreposições."""
    if basis=='comprimento':

        allocated={};outside=0.;ambiguous=0.;total=0.
        lines=[geom] if geom.geom_type=='LineString' else list(geom.geoms)
        def line_parts(g):
            if g.geom_type=='LineString':return [g]
            if hasattr(g,'geoms'):return [p for x in g.geoms for p in line_parts(x)]
            return []
        for line in lines:
            coords=list(line.coords)
            for a,b in zip(coords,coords[1:]):
                seg=LineString([a,b]);length=seg.length
                if length==0:continue
                total+=length;intervals=[];cuts={0.,1.}
                for pos in zones.sindex.query(seg,predicate='intersects'):
                    zid=zones.index[pos]
                    for part in line_parts(seg.intersection(zones.geometry.iloc[pos])):
                        ts=[seg.project(Point(c),normalized=True) for c in part.coords]
                        lo=max(0.,min(ts));hi=min(1.,max(ts))
                        if hi>lo:
                            intervals.append((lo,hi,zid));cuts.update([lo,hi])
                cuts=sorted(cuts)
                for lo,hi in zip(cuts,cuts[1:]):
                    mid=(lo+hi)/2;amount=(hi-lo)*length
                    owners={z for l,h,z in intervals if l<=mid<=h}
                    if len(owners)==1:
                        zid=next(iter(owners));allocated[zid]=allocated.get(zid,0.)+amount
                    elif owners:ambiguous+=amount
                    else:outside+=amount
        result=[(z,v/total,v) for z,v in allocated.items()]
        assert abs(sum(v for _,v,_ in result)+(outside+ambiguous)/total-1)<1e-6
        return result,outside/total,ambiguous/total,total
    positions=zones.sindex.query(geom,predicate='intersects')
    hits=[(zones.index[i],geom.intersection(zones.geometry.iloc[i])) for i in positions]
    if basis=='ponto':
        if len(hits)==1:return [(hits[0][0],1.,1.)],0.,0.,1.
        return [],float(not hits),float(len(hits)>1),1.
    measure=(lambda g:g.length) if basis=='comprimento' else (lambda g:g.area)
    total=measure(geom);hits=[(i,g) for i,g in hits if measure(g)>0]
    if not hits:return [],1.,0.,total
    overlaps=[]
    for i,(_,g) in enumerate(hits):
        for _,h in hits[i+1:]:
            overlap=g.intersection(h)
            if measure(overlap)>0:overlaps.append(overlap)
    conflict=unary_union(overlaps) if overlaps else GeometryCollection()
    result=[]
    for zid,piece in hits:
        amount=measure(piece.difference(conflict))
        if amount>0:result.append((zid,amount/total,amount))
    covered=unary_union([g for _,g in hits]);outside=measure(geom.difference(covered))/total
    ambiguous=measure(conflict)/total
    assert abs(sum(f for _,f,_ in result)+outside+ambiguous-1)<1e-6, (basis,total,sum(f for _,f,_ in result),outside,ambiguous)
    return result,outside,ambiguous,total

# Emission class
def emission_class(value,minor):
    if value>100 and not np.isclose(value,100,atol=1e-10,rtol=0):return 'Alta (>100 t/ano)'
    if value>minor and not np.isclose(value,minor,atol=1e-10,rtol=0):return 'Intermediária'
    if value>0:return 'Baixa / minoritária'
    return 'Sem massa quantificada'

# Apply territorial totals
def apply_territorial_totals(zones):
    """Aplica a nova regra aos mapas sem alterar o cadastro geográfico original."""
    table=pd.read_csv(config.DIRS['out']/'13_rateio_emissoes/Resumo_zonas.csv')
    z=zones.copy()
    for pol in ['PM10','PM25']:
        sub=table[table.poluente.eq(pol)].set_index('zona').reindex(z.index)
        if sub.total_quantificado_t_ano.isna().any():raise ValueError('Zoneamento incompatível com rateio')
        mass=sub.total_quantificado_t_ano
        z[f'{pol}_emission_class']=np.where(mass>100,'Majoritária','Não majoritária')
        pending=sub.n_fontes.eq(0)|sub.n_fontes_sem_massa.gt(0)
        if 'n_fontes_geometria_ambigua' in sub:pending|=sub.n_fontes_geometria_ambigua.gt(0)
        z.loc[pending&mass.le(100),f'{pol}_emission_class']='Informação insuficiente'
        z[f'{pol}_massa_rateada_t_ano']=mass
        z[f'{pol}_emission_total_tpy']=mass
        z[f'{pol}_emission_basis_year']=2023
        z[f'{pol}_emission_audit_status']='Entradas corrigidas + HOUREMISS 2023; memoriais e ambiguidades pendentes identificados'
    return z

# Run
def run():
    out=config.DIRS['out']/'13_rateio_emissoes';out.mkdir(parents=True,exist_ok=True)
    zones=gpd.read_file(config.DIRS['out']/'11_integracao/zoneamento_integrado.gpkg').set_index('zone_index',drop=False).to_crs(config.CRS_PROJECT)
    zones.geometry=zones.geometry.map(_clean_geometry)
    assert zones.index.is_unique and len(zones)==311
    conflicts=[]
    for i,zid in enumerate(zones.index):
        geom=zones.geometry.iloc[i]
        for j in zones.sindex.query(geom,predicate='intersects'):
            if j>i:conflicts.append((zid,zones.index[j],geom.intersection(zones.geometry.iloc[j])))
    details=[];balances=[];associations=[];missing_all=[];summary_all=[];groups_all=[]
    refined=config.DIRS['out']/'14_auditoria_entradas/revalidacao_final'
    masses=pd.read_csv(refined/'Massas_fontes_2021_2023.csv')
    source_records={(r['poluente'],r['id']):r for r in json.loads((refined/'fontes_correntes.json').read_text(encoding='utf8'))}
    for pol,name in [('PM10','PM10_Sources.xlsx'),('PM25','PM2-5_Sources.xlsx')]:
        raw,sources=refined_sources(pol,name)
        annual=masses[masses.poluente.eq(pol)].pivot(index='id',columns='ano',values='massa_t_ano')
        missing=[]
        ambiguous_zones={z:set() for z in zones.index}
        for _,source in sources.iterrows():
            sid=source.source_id;geom,basis=geometry_for_allocation(source,raw.loc[sid])
            rec=source_records[(pol,sid)];mass=float(annual.loc[sid,2023]);status=rec['status']
            inventory=status=='conciliada'
            if status=='HOUREMISS':status='HOUREMISS integrado em 2023; massa conservada'
            if not inventory and rec['status']!='HOUREMISS':
                missing_all.append({'poluente':pol,'id_fonte':sid,'situacao':status,'massa_quantificada_t_ano':mass})
            if not np.isfinite(mass) or mass<0:mass=np.nan
            group=source.group_id if pd.notna(source.group_id) else 'NAO_IDENTIFICADO'
            enterprise=GROUPS.get(group,{}).get('name',group)
            base={'poluente':pol,'id_fonte':sid,'id_inventario':rec['inventario_ids'],
                  'tipo_fonte':source.source_type,'grupo':group,
                  'empreendimento':enterprise,'descricao':source.desc,'ano_base':2023,
                  'origem_massa':'Inventário conciliado nas entradas' if inventory else status,'situacao_massa':status,
                  'taxa_nativa':source.emission_rate_native,'unidade_nativa':source.native_unit,
                  'massa_fonte_t_ano':mass,'taxa_equivalente_fonte_g_s':mass/31.536,
                  'metodo_rateio':basis,'origem_geometria':source.geometry_source,
                  'criterio_vinculo':'ID da entrada corrente; massa horária integrada ou taxa total × 31,536',
                  **{f'massa_fonte_{y}_t':float(annual.loc[sid,y]) for y in (2021,2022,2023)}}
            associations.append(base.copy())
            if geom is None:
                pieces=[];outside=0.;ambiguous=1.;measure=np.nan
            else:
                try:pieces,outside,ambiguous,measure=partition(geom,zones,basis)
                except AssertionError as exc:raise ValueError(f'Balanço geométrico inválido em {sid}: {exc}') from exc
                if ambiguous>1e-8:
                    for za,zb,conflict in conflicts:
                        hit=geom.intersection(conflict)
                        affected=(not hit.is_empty) if basis=='ponto' else hit.length>1e-8 if basis=='comprimento' else hit.area>1e-8
                        if affected:
                            ambiguous_zones[za].add(sid);ambiguous_zones[zb].add(sid)
            for zid,fraction,inter in pieces:
                details.append({**base,'zona':zid,'nome_zona':zones.loc[zid,'nome'],
                                'medida_fonte':measure,'medida_intersecao':inter,
                                'unidade_medida':'m' if basis=='comprimento' else 'unidade' if basis=='ponto' else 'm²',
                                'fracao':fraction,'massa_zona_t_ano':mass*fraction,
                                'taxa_equivalente_zona_g_s':mass*fraction/31.536})
            frac=sum(f for _,f,_ in pieces)
            balances.append({**base,'fracao_alocada':frac,'fracao_fora_zoneamento':outside,
                             'fracao_ambigua':ambiguous,'massa_alocada_t_ano':mass*frac,
                             'massa_fora_zoneamento_t_ano':mass*outside,'massa_ambigua_t_ano':mass*ambiguous,
                             'residuo_fracao':1-frac-outside-ambiguous,
                             'situacao_geometria':'pendente' if ambiguous>1e-8 else 'sem duplicação'})
        a=pd.DataFrame([r for r in details if r['poluente']==pol]);minor=5 if pol=='PM10' else 3
        for zid in zones.index:
            sub=a.loc[a.zona.eq(zid)];known=sub.massa_zona_t_ano.sum(min_count=1)
            if sub.empty:known=0.
            total=float(known) if pd.notna(known) else 0.
            invtotal=sub.loc[sub.origem_massa.eq('Inventário conciliado nas entradas'),'massa_zona_t_ano'].sum()
            hourlytotal=sub.loc[sub.origem_massa.str.startswith('HOUREMISS',na=False),'massa_zona_t_ano'].sum()
            summary_all.append({'poluente':pol,'zona':zid,'nome_zona':zones.loc[zid,'nome'],
                 'n_fontes':sub.id_fonte.nunique(),'n_empreendimentos':sub.grupo.nunique(),
                 'n_fontes_sem_massa':int(sub.massa_zona_t_ano.isna().sum()),
                 'n_fontes_geometria_ambigua':len(ambiguous_zones[zid]),
                 'n_fontes_memorial_pendente':int(sub.situacao_massa.eq('massa de entrada; memorial pendente').sum()),
                 'total_quantificado_t_ano':total,'inventario_t_ano':invtotal,
                 'houremiss_t_ano':hourlytotal,'cenario_fallback_t_ano':total-invtotal-hourlytotal,'g_s_equivalente':total/31.536,
                 'classe_preliminar_total':emission_class(total,minor),
                 'criterio':'soma de todas as fontes na zona; não máximo por grupo',
                 'validade':'massa 2023 das entradas e EMI; memoriais e ambiguidades pendentes',
                 **{f'total_{y}_t_ano':float((sub[f'massa_fonte_{y}_t']*sub.fracao).sum()) for y in (2021,2022,2023)}})
        for (zid,grp),sub in a.groupby(['zona','grupo']):
            total=sub.massa_zona_t_ano.sum(min_count=1)
            groups_all.append({'poluente':pol,'zona':zid,'grupo':grp,'empreendimento':sub.empreendimento.iloc[0],
                'n_fontes':sub.id_fonte.nunique(),'massa_t_ano':total,'g_s_equivalente':total/31.536,
                'classe_grupo':emission_class(total,minor) if pd.notna(total) else 'Sem massa quantificada'})
        print(pol,'fontes',len(sources),'parcelas',len(a),'inventário pendente',len(missing),flush=True)
    tables={'Resumo_zonas':pd.DataFrame(summary_all),'Empreendimentos':pd.DataFrame(groups_all),
            'Fracoes_fontes':pd.DataFrame(details),'Balanco_fontes':pd.DataFrame(balances),
            'Correspondencia_ID':pd.DataFrame(associations),'Inventario_pendente':pd.DataFrame(missing_all)}
    for name,table in tables.items():table.to_csv(out/(name+'.csv'),index=False,encoding='utf-8-sig')

    payload={name:{'columns':list(table.columns),'rows':json.loads(table.to_json(orient='values',force_ascii=False))} for name,table in tables.items()}
    (out/'tabelas_planilha.json').write_text(json.dumps(payload,ensure_ascii=False),encoding='utf-8')
    b=tables['Balanco_fontes'];assert b.residuo_fracao.abs().max()<1e-6
    report={'zonas':len(zones),'fontes_poluente':len(b),'parcelas':len(details),
            'fracao_max_erro':float(b.residuo_fracao.abs().max()),
            'fontes_com_sobreposicao_ou_geometria_pendente':int(b.fracao_ambigua.gt(1e-8).sum()),
            'fontes_sem_massa_quantificada':int(b.massa_fonte_t_ano.isna().sum()),
            'classes':tables['Resumo_zonas'].groupby('poluente').classe_preliminar_total.value_counts().to_dict()}
    report['classes']={f'{a}/{c}':v for (a,c),v in report['classes'].items()}
    (out/'auditoria_rateio.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return tables

if __name__=='__main__':run()
