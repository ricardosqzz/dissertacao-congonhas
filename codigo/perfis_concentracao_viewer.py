# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entradas: argumentos do chamador e módulos locais relacionados no relatório.
# Saída: {out}/index.html | .write_text.
# CÓDIGO DO PROCESSAMENTO

"""Interface offline com valores absolutos e carregamento por estação."""
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

# Write viewer
def write_viewer(out,metadata):
    template=r'''<!doctype html><html lang="pt-BR"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Concentrações nas estações</title>
<style>
body{font:16px/1.55 Arial,sans-serif;max-width:1250px;margin:30px auto;padding:0 22px;color:#183d4c;background:#fff}
h1{font-size:29px}h2{font-size:21px;margin-top:35px}p{max-width:1080px}
.controls{display:flex;gap:16px;flex-wrap:wrap;align-items:end;padding:16px 0;border-top:1px solid #d8e0e1;border-bottom:1px solid #d8e0e1}
label{display:flex;flex-direction:column;font-size:14px;color:#375563}select,input{font:16px Arial;padding:8px;max-width:360px;border:1px solid #abbfc7;border-radius:4px;background:#fff}
.check{display:inline-flex;flex-direction:row;align-items:center;gap:8px}.check input{width:auto}
svg{width:100%;height:auto;display:block;background:white}a{color:#176b88}small{color:#526974}
#status,#stats{padding:12px 0}.swatch{display:inline-block;width:16px;height:12px;background:#f3deb5;margin-right:6px}
table{border-collapse:collapse;margin-top:15px;font-size:14px}td,th{padding:7px 13px;border-bottom:1px solid #dce4e7;text-align:left}
.tag{font-weight:bold;color:#1b657e}#tip{min-height:24px;font-variant-numeric:tabular-nums}
</style>
<h1>Concentrações modeladas e observadas nas estações</h1>
<p>Valores em µg/m³ no período 2021-2023. As duas séries ocupam painéis alinhados, com eixos verticais próprios por padrão. As lacunas permanecem visíveis e os picos horários são preservados. A contribuição de uma empresa é uma parcela modelada, enquanto a estação observa a mistura das fontes.</p>
<div class="controls"><label>Poluente<select id="pol"></select></label><label>Estação<select id="station"></select></label><label>Grupo modelado<select id="group"></select></label><label class="check"><input id="same" type="checkbox">Mesma escala vertical</label></div>
<div id="status">Carregando dados…</div>
<h2>Perfil por hora do dia</h2><div class="controls"><label>Recorte sazonal<select id="season"><option>Total</option><option>Período seco</option><option>Demais dias</option></select></label><label class="check"><input id="showmax" type="checkbox">Mostrar máximo de cada hora</label></div>
<p><small>A linha é a média nas mesmas horas pareadas. A faixa representa P10-P90 dos valores horários, e não um intervalo de confiança. O máximo pode ser ativado para examinar os extremos.</small></p>
<svg id="profile" viewBox="0 0 1150 500" role="img" aria-label="Perfis horários em concentração"></svg>
<h2>Série histórica no mesmo período</h2><div class="controls"><label>Resolução<select id="resolution"><option value="hourly">Horária</option><option value="daily">Média diária</option></select></label><label>De<input id="from" type="date" value="2021-01-01" min="2021-01-01" max="2023-12-31"></label><label>Até<input id="to" type="date" value="2023-12-31" min="2021-01-01" max="2023-12-31"></label></div>
<p><span class="swatch"></span>Período menos chuvoso identificado na rede meteorológica regional. Passe o cursor para consultar os valores de cada intervalo. Dias observados exigem pelo menos 16 horas e dias modelados pelo menos 18 horas efetivas nesta visualização.</p>
<svg id="history" viewBox="0 0 1150 540" role="img" aria-label="Séries históricas em concentração com período seco"></svg><div id="tip"></div><div id="stats"></div>
<h2>Chuva e delimitação do período menos chuvoso</h2>
<p>A referência é a mediana diária de pelo menos três pluviômetros regionais, cada um com pelo menos 18 horas de dados. O intervalo sombreado corresponde à maior queda da anomalia acumulada de chuva em cada ano, relativa à média diária de 2021-2023. As datas derivam dos dados, sem fixar abril e outubro. A meteorologia WRF/SFC é mostrada para comparação. Três anos não constituem uma climatologia.</p>
<svg id="rain" viewBox="0 0 1150 290" role="img" aria-label="Chuva regional e meteorologia de entrada"></svg><div id="periods"></div>
<p><small>O relógio segue a hipótese anterior de observações em UTC e conversão para UTC-3, ainda pendente de confirmação documental. Os dados observados válidos são mostrados mesmo quando não há hora meteorológica válida no modelo. Nenhum perfil de emissão foi ajustado por estas curvas.</small></p>
<p><a href="perfis_concentracao_por_estacao_grupo.csv">Perfis horários em concentração</a> · <a href="comparacao_periodo_seco_grupos_estacoes.csv">Comparação seco e demais dias</a> · <a href="periodos_secos_meteorologicos.csv">Datas do período seco</a> · <a href="precipitacao_referencia_diaria.csv">Precipitação diária</a> · <a href="distancias_grupos_estacoes.csv">Distâncias às fontes</a> · <a href="grupos_fontes_horarias_e_estaticas.csv">Fontes horárias e estáticas</a> · <a href="../figuras/index.html">Mapas e análises espaciais</a></p>
<h2>Figuras estáticas por estação</h2><div id="static"></div>
<script src="dados_series/metadados.js"></script><script>
const $=id=>document.getElementById(id), pol=$('pol'),st=$('station'),gr=$('group');
const HOUR=3600000,BASE=Date.UTC(2021,0,1);let current=null,token=0,historyState=null;
const valid=v=>typeof v==='number'&&Number.isFinite(v),fmt=v=>valid(v)?v.toLocaleString('pt-BR',{maximumFractionDigits:2}):'sem dado';
function options(el,values,labels={}){let old=el.value;el.replaceChildren();values.forEach(v=>{let o=document.createElement('option');o.value=v;o.textContent=labels[v]||v;el.appendChild(o)});if(values.includes(old))el.value=old;}
options(pol,['PM10','PM25'],{PM10:'MP10',PM25:'MP2,5'});
function stations(){options(st,META.stations[pol.value],META.station_names);load();}
function load(){let key=pol.value+'_'+st.value;let mine=++token;$('status').textContent='Carregando '+META.station_names[st.value]+'…';const ready=()=>{if(mine!==token)return;let prior=gr.value;current=window.PERFIS[key];options(gr,Object.keys(current.groups).sort(),META.names);gr.value=prior&&current.groups[prior]?prior:'ALL';$('status').textContent='Período 2021-2023 · valores absolutos · '+META.station_names[st.value];draw();};
if(window.PERFIS&&window.PERFIS[key]){ready();return;}let script=document.createElement('script');script.src='dados_series/'+key+'.js';script.onload=ready;script.onerror=()=>{$('status').textContent='Não foi possível carregar o arquivo local da estação.';};document.body.appendChild(script);}
function dryRanges(){return META.periods.filter(r=>r.source==='Rede regional').map(r=>[(Date.parse(r.start+'T00:00:00Z')-BASE)/HOUR,(Date.parse(r.end+'T00:00:00Z')-BASE)/HOUR+24]);}
function labelDate(i){return new Date(BASE+i*HOUR).toISOString().slice(0,10).split('-').reverse().join('/');}
function path(values,x,y,indices){let s='',on=false;for(let i=0;i<values.length;i++){let v=values[i];if(!valid(v)){on=false;continue;}s+=(on?'L':'M')+x(indices[i]).toFixed(2)+','+y(v).toFixed(2);on=true;}return s;}
function panel(values,indices,top,height,label,color,lo,hi,maxOverride,bands=null,dry=false,kind='time',maxline=null){
 const left=100,right=1120,plotTop=top+26,plotBottom=top+height-35;
 let vals=values.filter(valid);if(bands)vals=vals.concat(bands[1].filter(valid));if(maxline)vals=vals.concat(maxline.filter(valid));
 let max=maxOverride||Math.max(1,...vals)*1.08,x=v=>left+(v-lo)/(hi-lo)*(right-left),y=v=>plotBottom-v/max*(plotBottom-plotTop),s='';
 if(dry){for(let [a,b] of dryRanges()){a=Math.max(a,lo);b=Math.min(b,hi);if(b>a)s+='<rect x="'+x(a)+'" y="'+plotTop+'" width="'+(x(b)-x(a))+'" height="'+(plotBottom-plotTop)+'" fill="#f3deb5" fill-opacity=".65"/>';}}
 for(let j=0;j<=4;j++){let v=max*j/4;s+='<line x1="'+left+'" x2="'+right+'" y1="'+y(v)+'" y2="'+y(v)+'" stroke="#dde4e6"/><text x="89" y="'+(y(v)+5)+'" text-anchor="end" font-size="13">'+fmt(v)+'</text>';}
 s+='<text x="'+left+'" y="'+(top+15)+'" font-size="16" font-weight="bold" fill="'+color+'">'+label+'</text><text transform="translate(27 '+((plotTop+plotBottom)/2)+') rotate(-90)" font-size="14" text-anchor="middle">Concentração (µg/m³)</text>';
 if(bands){for(let i=0;i<values.length-1;i++){if([bands[0][i],bands[1][i],bands[0][i+1],bands[1][i+1]].every(valid)){s+='<path d="M'+x(indices[i])+','+y(bands[0][i])+'L'+x(indices[i])+','+y(bands[1][i])+'L'+x(indices[i+1])+','+y(bands[1][i+1])+'L'+x(indices[i+1])+','+y(bands[0][i+1])+'Z" fill="'+color+'" fill-opacity=".15"/>';}}}
 if(maxline)s+='<path d="'+path(maxline,x,y,indices)+'" fill="none" stroke="'+color+'" stroke-opacity=".55" stroke-width="1" stroke-dasharray="4 3"/>';
 s+='<path d="'+path(values,x,y,indices)+'" fill="none" stroke="'+color+'" stroke-width="'+(kind==='hour'?2:1)+'"/>';
 const ticks=kind==='hour'?[0,3,6,9,12,15,18,21,23]:Array.from({length:7},(_,j)=>lo+(hi-lo)*j/6);
 for(let [j,t] of ticks.entries())s+='<text x="'+x(t)+'" y="'+(plotBottom+23)+'" text-anchor="'+(kind==='hour'?'middle':j===0?'start':j===ticks.length-1?'end':'middle')+'" font-size="13">'+(kind==='hour'?t:labelDate(t))+'</text>';
 return s;}
function draw(){if(!current)return;let g=gr.value,pr=current.profiles[g][$('season').value],showmax=$('showmax').checked;let pmax=$('same').checked?Math.max(...['observed','modelled'].flatMap(k=>(showmax?pr[k].max:pr[k].p90).filter(valid)))*1.08:null;
 $('profile').innerHTML=panel(pr.observed.mean,Array.from({length:24},(_,i)=>i),0,245,'Observado','#1b657e',0,23,pmax,[pr.observed.p10,pr.observed.p90],false,'hour',showmax?pr.observed.max:null)+panel(pr.modelled.mean,Array.from({length:24},(_,i)=>i),250,245,'Modelado · '+META.names[g],'#bd4e48',0,23,pmax,[pr.modelled.p10,pr.modelled.p90],false,'hour',showmax?pr.modelled.max:null);
 const daily=$('resolution').value==='daily',step=daily?24:1,source=daily?current.daily:current;
 const fullObs=source.observed,fullMod=source.groups[g],a=Math.max(0,(Date.parse($('from').value+'T00:00:00Z')-BASE)/HOUR),b=Math.min(META.hours-1,(Date.parse($('to').value+'T00:00:00Z')-BASE)/HOUR+23);
 if(b<=a){$('history').innerHTML='';return;}let first=Math.ceil(a/step),last=Math.floor(b/step),indices=Array.from({length:last-first+1},(_,i)=>(first+i)*step),obs=fullObs.slice(first,last+1),mod=fullMod.slice(first,last+1);
 let common=$('same').checked?Math.max(1,...obs.filter(valid),...mod.filter(valid))*1.08:null;
 $('history').innerHTML=panel(obs,indices,0,265,'Observado','#1b657e',a,b,common,null,true)+panel(mod,indices,275,265,'Modelado · '+META.names[g],'#bd4e48',a,b,common,null,true);historyState={a,b,step,obs:fullObs,model:fullMod};
 let m=current.stats[g];$('stats').textContent='Estatísticas das horas pareadas do triênio: N = '+m.paired_hours+'. Média observada '+fmt(m.observed_mean)+'; modelada '+fmt(m.modelled_mean)+'. Máximo observado '+fmt(m.observed_max)+'; modelado '+fmt(m.modelled_max)+' µg/m³. Correlação horária '+fmt(m.hourly_r)+'. O sombreado descreve sazonalidade, sem atribuir sozinho a causa dos picos.';
 let distance=META.distances?.find(r=>r.pollutant===pol.value&&r.station_id===st.value&&r.group_id===g),flags=META.flags?.find(r=>r.pollutant===pol.value&&r.group_id===g);
 if(distance)$('stats').textContent+=' Distância mínima às fontes '+fmt(distance.distance_min_geometry_km)+' km; distância ao centro ponderado por emissão '+fmt(distance.distance_emission_centroid_km)+' km. Distâncias são contexto geométrico, sem ponderação inversa automática.';
 if(flags)$('stats').textContent+=' Fontes já horárias no grupo: '+flags.hourly_sources+'.';
}
function rainfall(){let v=META.rain.observed,w=META.rain.model,idx=v.map((_,i)=>i*24);let top=30,bottom=240,left=100,right=1120,max=Math.max(...v.filter(valid),...w.filter(valid))*1.05,x=i=>left+i/(META.hours-1)*(right-left),y=a=>bottom-a/max*(bottom-top),s='';
for(let [a,b] of dryRanges())s+='<rect x="'+x(a)+'" width="'+(x(b)-x(a))+'" y="'+top+'" height="'+(bottom-top)+'" fill="#f3deb5" fill-opacity=".65"/>';
for(let j=0;j<=4;j++){let a=max*j/4;s+='<line x1="'+left+'" x2="'+right+'" y1="'+y(a)+'" y2="'+y(a)+'" stroke="#ddd"/><text x="88" y="'+(y(a)+5)+'" text-anchor="end" font-size="13">'+fmt(a)+'</text>';}
s+='<path d="'+path(v,x,y,idx)+'" fill="none" stroke="#1b657e" stroke-width="1"/><path d="'+path(w,x,y,idx)+'" fill="none" stroke="#bd4e48" stroke-opacity=".65" stroke-width="1"/><text x="100" y="18" fill="#1b657e" font-size="15">Mediana regional observada</text><text x="420" y="18" fill="#bd4e48" font-size="15">WRF/SFC</text><text transform="translate(27 140) rotate(-90)" text-anchor="middle" font-size="14">Precipitação (mm/dia)</text>';
for(let j=0;j<=6;j++){let i=(META.hours-1)*j/6;s+='<text x="'+x(i)+'" y="265" text-anchor="'+(j===0?'start':j===6?'end':'middle')+'" font-size="13">'+labelDate(i)+'</text>';}
$('rain').innerHTML=s;let table='<table><thead><tr><th>Referência</th><th>Ano</th><th>Início</th><th>Fim</th><th>Dias</th></tr></thead><tbody>';
for(let r of META.periods)table+='<tr><td>'+r.source+'</td><td>'+r.year+'</td><td>'+r.start.split('-').reverse().join('/')+'</td><td>'+r.end.split('-').reverse().join('/')+'</td><td>'+r.duration_days+'</td></tr>';
$('periods').innerHTML=table+'</tbody></table>';let links='';for(let p of ['PM10','PM25'])for(let s of META.stations[p])links+='<p>'+p+' · '+META.station_names[s]+': <a href="Concentracoes_'+p+'_'+s+'.svg">SVG</a> · <a href="Concentracoes_'+p+'_'+s+'.pdf">PDF</a> · <a href="Concentracoes_'+p+'_'+s+'.png">PNG</a></p>';$('static').innerHTML=links;}
$('history').addEventListener('mousemove',event=>{if(!historyState)return;let box=$('history').getBoundingClientRect(),px=(event.clientX-box.left)*1150/box.width;if(px<100||px>1120)return;let h=historyState.a+(px-100)/1020*(historyState.b-historyState.a),i=Math.max(0,Math.min(historyState.obs.length-1,Math.round(h/historyState.step)));let text=labelDate(i*historyState.step);if(historyState.step===1)text+=' '+String(i%24).padStart(2,'0')+':00';$('tip').textContent=text+' · Observado '+fmt(historyState.obs[i])+' · Modelado '+fmt(historyState.model[i])+' µg/m³';});
pol.onchange=stations;st.onchange=load;gr.onchange=draw;['same','season','showmax','resolution','from','to'].forEach(id=>$(id).onchange=draw);rainfall();stations();
</script></html>'''
    (Path(out)/'index.html').write_text(template,encoding='utf8')
