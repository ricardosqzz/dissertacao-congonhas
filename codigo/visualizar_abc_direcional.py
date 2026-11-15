# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: Path(output) if output is not None else globals()['OUT']/'regioes_gerais.csv' if general else 'regioes_direcionais.csv' | pd.read_csv.
# Entrada: Path(output) if output is not None else globals()['OUT']/ABC_contribuicoes_regioes.csv | pd.read_csv.
# Entrada: Path(output) if output is not None else globals()['OUT']/index.html | entry.read_text.
# Entrada: Path(output) if output is not None else globals()['OUT']/regioes_direcionais.csv | pd.read_csv.
# Campos/chaves em regions: label, region_id, region_type.
# Campos/chaves em abc: region_id.
# Campos/chaves em values: ABC, cumulative_before_pct, group_name, share_pct.
# Campos/chaves em all_abc: label, period, pollutant, region_type.
# Campos/chaves em all_regions: area_km2, region_id.
# Saída: Path(output) if output is not None else globals()['OUT']/abc_por_regiao.html | .write_text.
# Saída: Path(output) if output is not None else globals()['OUT']/index.html | entry.write_text.
# Saída: Path(output) if output is not None else globals()['OUT']/figuras/{pol}_{period}_Contribuicoes_prioridades.{ext} | fig.savefig.
# Campos/chaves gerados em d: weighted.
# Campos/chaves gerados em plot: Demais grupos.
# CÓDIGO DO PROCESSAMENTO

"""ABC consultável por região, evitando centenas de páginas estáticas."""
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
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import config
import cartografia_apendices as cart
OUT=config.BASE/'output/16_revisao_pos_banca/vento/analises_espaciais'

# Run
def run(output=None):
    OUT=Path(output) if output is not None else globals()['OUT']
    general=OUT.name=='cenario_geral'
    region_file='regioes_gerais.csv' if general else 'regioes_direcionais.csv'
    regions=pd.read_csv(OUT/region_file)
    keep=(regions.region_type.eq('gestao')&regions.label.eq('Prioridade receptora'))|(regions.region_type.eq('LISA')&regions.label.eq('Alto–alto'))
    regions=regions[keep].copy();abc=pd.read_csv(OUT/'ABC_contribuicoes_regioes.csv');abc=abc[abc.region_id.isin(regions.region_id)]
    data={}
    for r in regions.itertuples():
        values=abc[abc.region_id.eq(r.region_id)].sort_values('share_pct',ascending=False)
        data[r.region_id]=dict(pol=r.pollutant,period=r.period,direction=r.direction,kind=r.region_type,area=r.area_km2,
                               coverage=r.eligible_monitored_area_pct,receptors=r.n_receptors,C=r.concentration_area_mean,
                               groups=values[['group_name','share_pct','cumulative_before_pct','ABC']].rename(columns={'group_name':'name','share_pct':'share','cumulative_before_pct':'before','ABC':'abc'}).to_dict('records'))
    template=r'''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ABC das regiões direcionais</title>
<style>body{font:16px/1.6 Arial;max-width:1200px;margin:30px auto;padding:0 20px;color:#193f4c}label{display:inline-block;margin:0 15px 12px 0}select{font:inherit;display:block;padding:7px;max-width:400px}svg{width:100%;height:auto;background:#fff}table{border-collapse:collapse;width:100%;font-size:14px}td,th{padding:6px 10px;text-align:left;border-bottom:1px solid #dce4e6}a{color:#176b88}</style>
<h1>Contribuições e curva ABC por região</h1>
<p>Selecione uma região para examinar quais grupos contribuem para as concentrações do envelope. As parcelas são consultadas no mesmo horário ou dia do máximo ALL de cada receptor e depois ponderadas pela área. Os máximos dos receptores podem ocorrer em momentos diferentes.</p>
<label>Poluente<select id="pol"></select></label><label>Duração<select id="period"></select></label><label>Vento de<select id="direction"></select></label><label>Recorte<select id="kind"></select></label><label>Região<select id="region"></select></label>
<p id="stats"></p><svg id="bars" viewBox="0 0 1150 590" aria-label="Participação dos grupos"></svg><svg id="curve" viewBox="0 0 1150 310" aria-label="Curva ABC acumulada"></svg>
<p>As barras mostram a participação de cada grupo. Na curva, a posição horizontal é a ordem do grupo na tabela e a posição vertical é a participação acumulada. A linha pontilhada em 80% delimita a classe A e a de 95% a classe B. O grupo que atravessa um corte permanece na classe anterior. A classe C contém as parcelas restantes.</p>
<table><thead><tr><th>Ordem</th><th>Grupo</th><th>Participação (%)</th><th>Acumulada (%)</th><th>ABC</th></tr></thead><tbody id="table"></tbody></table>
<p>Empresas e Urbano Total formam a partição exclusiva. AEX e subgrupos urbanos não são somados novamente. Urbano Total reúne ferrovias, núcleos urbanos e vias urbanas. A participação em concentração recebida não corresponde à participação na massa emitida dentro da região.</p>
<p><a href="ABC_contribuicoes_regioes.csv">Tabela completa de contribuições e ABC</a> · <a href="regioes_direcionais.csv">Áreas e cobertura</a> · <a href="index.html">Voltar às análises por direção</a></p><script>
const DATA=__DATA__, $=id=>document.getElementById(id), pol=$('pol'),period=$('period'),direction=$('direction'),kind=$('kind'),region=$('region');
function options(el,values,labels={}){let old=el.value;el.replaceChildren();for(let v of values){let o=document.createElement('option');o.value=v;o.textContent=labels[v]||v;el.appendChild(o)}if(values.includes(old))el.value=old;}
const fmt=v=>v.toLocaleString('pt-BR',{maximumFractionDigits:2});
options(pol,['PM10','PM25'],{PM10:'MP10',PM25:'MP2,5'});options(period,__PERIODS__,{'1h':'1 h','24h':'24 h','anual':'Média anual trienal'});options(direction,__DIRECTIONS__,{GERAL:'Meteorologia completa'});options(kind,['gestao','LISA'],{gestao:'Regiões prioritárias acima de P80',LISA:'Clusters HH significativos'});
function update(){let ids=Object.keys(DATA).filter(k=>{let r=DATA[k];return r.pol===pol.value&&r.period===period.value&&r.direction===direction.value&&r.kind===kind.value}).sort((a,b)=>DATA[b].area-DATA[a].area);let labels={};ids.forEach((v,j)=>labels[v]='R'+String(j+1).padStart(2,'0')+' · '+fmt(DATA[v].area)+' km² · cobertura '+fmt(DATA[v].coverage)+'%');options(region,ids,labels);draw();}
function draw(){let r=DATA[region.value];if(!r){$('stats').textContent='Não há região elegível neste recorte.';$('bars').innerHTML='';$('curve').innerHTML='';$('table').replaceChildren();return;}
$('stats').textContent=region.value+' · '+r.receptors+' receptores · área '+fmt(r.area)+' km² · cobertura elegível '+fmt(r.coverage)+'% · '+(r.period==='anual'?'média espacial do indicador anual ':'média espacial dos máximos ')+fmt(r.C)+' µg/m³.';
let top=28,bottom=560,left=280,right=1110,step=(bottom-top)/r.groups.length,max=Math.max(...r.groups.map(g=>g.share))*1.05,x=v=>left+v/max*(right-left),s='';
for(let j=0;j<=4;j++){let v=max*j/4;s+='<line x1="'+x(v)+'" x2="'+x(v)+'" y1="'+top+'" y2="'+bottom+'" stroke="#dce4e6"/><text x="'+x(v)+'" y="585" text-anchor="middle" font-size="13">'+fmt(v)+'%</text>';}
r.groups.forEach((g,i)=>{let y=top+i*step;let color=g.abc==='A'?'#247c96':g.abc==='B'?'#d6b06a':'#aabbb9';s+='<rect x="'+left+'" y="'+(y+step*.13)+'" width="'+(x(g.share)-left)+'" height="'+(step*.74)+'" fill="'+color+'"/><text x="265" y="'+(y+step*.68)+'" text-anchor="end" font-size="13">'+g.name+'</text>';});
$('bars').innerHTML=s;let pts=[],c='',n=r.groups.length,cx=i=>90+i/Math.max(1,n-1)*1020,cy=v=>250-v/100*220;
for(let v of [0,20,40,60,80,95,100])c+='<line x1="90" x2="1110" y1="'+cy(v)+'" y2="'+cy(v)+'" stroke="'+([80,95].includes(v)?'#b28647':'#ddd')+'" stroke-dasharray="'+([80,95].includes(v)?'5 3':'0')+'"/><text x="75" y="'+(cy(v)+4)+'" text-anchor="end" font-size="13">'+v+'%</text>';
r.groups.forEach((g,i)=>{let v=g.before+g.share;pts.push(cx(i)+','+cy(v));c+='<circle cx="'+cx(i)+'" cy="'+cy(v)+'" r="3" fill="#247c96"/><text x="'+cx(i)+'" y="277" text-anchor="middle" font-size="12">'+(i+1)+'</text>';});
c+='<polyline points="'+pts.join(' ')+'" fill="none" stroke="#247c96" stroke-width="2"/><text x="600" y="305" text-anchor="middle" font-size="14">Ordem do grupo na tabela</text>';$('curve').innerHTML=c;
$('table').replaceChildren();r.groups.forEach((g,i)=>{let tr=document.createElement('tr');for(let text of [i+1,g.name,fmt(g.share),fmt(g.before+g.share),g.abc]){let td=document.createElement('td');td.textContent=text;tr.appendChild(td)}$('table').appendChild(tr)});}
[pol,period,direction,kind].forEach(el=>el.onchange=update);region.onchange=draw;update();</script></html>'''
    if general:
        template=template.replace('ABC das regiões direcionais','ABC das regiões · cenário geral').replace('<label>Vento de','<label>Cenário')
        template=template.replace('As parcelas são consultadas no mesmo horário ou dia do máximo ALL de cada receptor e depois ponderadas pela área.','Nos máximos de 1 h e 24 h, as parcelas são consultadas no mesmo horário ou dia do máximo ALL de cada receptor. No anual, são usadas as médias nativas dos três anos. As parcelas regionais são ponderadas pela área.')
        template=template.replace('regioes_direcionais.csv','regioes_gerais.csv').replace('Voltar às análises por direção','Voltar ao cenário geral')
    periods=['1h','24h','anual'] if general else ['1h','24h']
    directions=['GERAL'] if general else ['N','NE','L','SE','S','SO','O','NO']
    template=template.replace('__PERIODS__',json.dumps(periods)).replace('__DIRECTIONS__',json.dumps(directions))
    (OUT/'abc_por_regiao.html').write_text(template.replace('__DATA__',json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')),encoding='utf8')
    entry=OUT/'index.html';s=entry.read_text(encoding='utf8');link='<p><a href="abc_por_regiao.html">Explorar a ABC de cada região e de cada cluster HH</a></p>'
    if link not in s:s=s.replace('</h1>','</h1>'+link,1)
    entry.write_text(s,encoding='utf8')
    if general:
        print('ABC interativa geral:',len(data),'regiões',flush=True)
        return

    DIRS=['N','NE','L','SE','S','SO','O','NO']
    all_abc=pd.read_csv(OUT/'ABC_contribuicoes_regioes.csv');all_regions=pd.read_csv(OUT/'regioes_direcionais.csv')
    for pol in ['PM10','PM25']:
        for period in ['1h','24h']:
            sub=all_abc[all_abc.pollutant.eq(pol)&all_abc.period.eq(period)&all_abc.region_type.eq('gestao')&all_abc.label.eq('Prioridade receptora')]
            d=sub.merge(all_regions[['region_id','area_km2']],on='region_id',validate='many_to_one');d['weighted']=d.contribution*d.area_km2
            v=d.groupby(['direction','group_name']).weighted.sum().unstack(fill_value=0).reindex(DIRS)
            shares=100*v.div(v.sum(axis=1),axis=0);names=v.sum().nlargest(6).index.tolist();plot=shares[names].copy();plot['Demais grupos']=shares.drop(columns=names).sum(axis=1)
            fig,ax=plt.subplots(figsize=(9,4.4));left=np.zeros(8)
            for group,color in zip(plot.columns,['#247c96','#64ada8','#bdc77c','#d6b06a','#b77f79','#8c83aa','#d9e1de']):
                ax.barh(DIRS,plot[group],left=left,color=color,label=group);left+=plot[group].to_numpy()
            ax.set(xlim=(0,100),xlabel='Contribuição nas regiões prioritárias (%)',ylabel='Direção de origem do vento');ax.invert_yaxis();fig.subplots_adjust(left=.12,right=.99,top=.98,bottom=.31)
            handles,_=ax.get_legend_handles_labels();cart.centered_legend(fig,handles,ncol=3,y=.16,fontsize=9,row_step=.055,center=.535)
            for ext in ['svg','pdf','png']:fig.savefig(OUT/f'figuras/{pol}_{period}_Contribuicoes_prioridades.{ext}',dpi=450,bbox_inches='tight')
            plt.close(fig)
    print('ABC interativa de',len(data),'regiões, com quatro figuras de síntese atualizadas.',flush=True)

if __name__=='__main__':run()
