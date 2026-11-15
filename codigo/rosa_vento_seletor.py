# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/projeto/output/16_revisao_pos_banca/vento/calendario_vento_horario.csv | pd.read_csv.
# Campos/chaves em c: direction_idx.
# Campos/chaves em ax.spines: polar.
# Saídas: retorno de funções, verificações ou arquivos definidos pelo chamador.
# CÓDIGO DO PROCESSAMENTO

"""Rosa meteorológica da entrada WRF/AERMET com seleção angular independente."""
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

from functools import lru_cache
import numpy as np
import pandas as pd
from matplotlib.patches import Patch
import config

DIRS=['N','NE','L','SE','S','SO','O','NO']
COLORS=['#BBDDE5','#77B8C3','#318EAA','#075A7A','#D59838','#B14739']
BREAKS=[0,.5,1,2,3,5,10]

@lru_cache(maxsize=1)
# Histogram
def histogram():
    p=config.BASE/'output/16_revisao_pos_banca/vento/calendario_vento_horario.csv'
    c=pd.read_csv(p);v=c[c.direction_idx.ge(0)]
    assert len(v)==24892 and v.wind_speed.between(0,10).all()

    directions=((v.wind_from_deg.to_numpy()+15)%360//30).astype(int)
    speed=np.searchsorted(BREAKS[1:],v.wind_speed.to_numpy(),side='left')
    h=np.zeros((12,6),dtype=int);np.add.at(h,(directions,speed),1)
    assert h.sum()==len(v)
    return h,100*h/len(v)

# Draw
def draw(ax,selected=None,fontsize=5.5):
    _,freq=histogram();ax.set_theta_zero_location('N');ax.set_theta_direction(-1)
    selected_idx=DIRS.index(selected) if selected in DIRS else None
    ax.set_facecolor('white');ax.set_ylim(0,np.ceil(freq.sum(axis=1).max()/5)*5)
    for i in range(12):
        lo=i*30-15;hi=i*30+15
        cuts=[lo,hi]
        if selected_idx is not None:
            for offset in [-360,0,360]:
                cuts.extend(x for x in [selected_idx*45-22.5+offset,selected_idx*45+22.5+offset] if lo<x<hi)
        cuts=sorted(set(cuts))
        for a,b in zip(cuts[:-1],cuts[1:]):
            active=selected_idx is None or abs((((a+b)/2-selected_idx*45+180)%360)-180)<=22.5
            bottom=0.
            for j,height in enumerate(freq[i]):
                ax.bar(np.deg2rad((a+b)/2),height,width=np.deg2rad(b-a)*.98,bottom=bottom,color=COLORS[j] if active else '#dce0df',edgecolor='white',linewidth=.18,zorder=3)
                bottom+=height
    ax.set_xticks(np.arange(8)*np.pi/4,DIRS,fontsize=fontsize)
    for i,t in enumerate(ax.get_xticklabels()):
        t.set_color('#075A7A' if selected_idx is None or selected_idx==i else '#a0a9a8')
        t.set_fontweight('bold' if selected_idx==i else 'normal')
    maximum=ax.get_ylim()[1];ticks=np.arange(5,maximum,5)
    ax.set_yticks(ticks,[f'{x:g}%' for x in ticks],fontsize=max(3.5,fontsize-1.4),color='#899594')
    ax.set_rlabel_position(275);ax.grid(color='#d6dedc',linewidth=.3)
    ax.spines['polar'].set_color('#c6cecb');ax.spines['polar'].set_linewidth(.35)
    ax.tick_params(axis='x',pad=0)
    return freq

# Add to figure
def add_to_figure(fig,selected,top=.10):
    ax=fig.add_axes([.405,top-.13,.11,.13],projection='polar',label='rosa_selecao_'+selected)
    ax.set_gid('rosa_vento_selecao_'+selected)
    draw(ax,selected,fontsize=4.8);ax.set_yticklabels([])
    labels=['0–0,5','0,5–1','1–2','2–3','3–5','5–10']
    legend=fig.legend([Patch(facecolor=v) for v in COLORS],labels,title='Velocidade (m/s)',ncol=2,loc='center left',bbox_to_anchor=(.55,top-.065),frameon=False,fontsize=4.5,title_fontsize=5,handlelength=1.2,columnspacing=.9,labelspacing=.4)
    legend.set_gid('legenda_velocidade_rosa')
    return ax
