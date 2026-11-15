# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: met['sfc']['path'] | pd.read_csv.
# Entrada: E:/projeto/wrf/AERMET-3Y.{ext} | p.read_bytes.
# Entrada: met[ext.lower()]['path'] | q.read_bytes.
# Entrada: E:/projeto/output/16_revisao_pos_banca/vento/{pol}_manifesto.json | stamp.read_text.
# Entrada: E:/projeto/out-aermod/{folder}/01_GALL.POS | pd.read_csv.
# Entrada: E:/projeto/output/11_integracao/nova_modelagem/{pol}_medias_diarias_1h.csv.gz | pd.read_csv.
# Campos/chaves em met: sfc.
# Campos/chaves em sfc: CODE.
# Campos/chaves em chunk: X, Y.
# Campos/chaves em metidx.loc: direction_idx.
# Campos/chaves em daily: day, direction_idx, eligible.
# Campos/chaves em summary: hours_by_direction.
# Saída: E:/projeto/output/16_revisao_pos_banca/vento/calendario_vento_horario.csv | cal.to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/vento/dias_direcao_persistente.csv | daily.to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/vento/frequencia_vento.csv | freq.to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/vento/{pol}_envelopes_horarios.csv | result.to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/vento/{pol}_envelopes_diarios_persistentes.csv | selected.to_csv.
# Saída: E:/projeto/output/16_revisao_pos_banca/vento/{pol}_manifesto.json | stamp.write_text.
# Campos/chaves gerados em sfc: CODE.
# Campos/chaves gerados em cal: direction, direction_idx.
# Campos/chaves gerados em freq: percent_total.
# Campos/chaves gerados em selected: direction.
# X: coordenada leste em metros.
# Y: coordenada norte em metros.
# CÓDIGO DO PROCESSAMENTO

"""Envelopes condicionados ao vento real da SFC, sem nova simulação AERMOD."""
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
import json,hashlib
import numpy as np
import pandas as pd
import config
from medias_horarias_verificadas import met_calendar,identity

ROOT=config.BASE/'output/16_revisao_pos_banca'
DIRS=np.array(['N','NE','L','SE','S','SO','O','NO'])

# Sector8
def sector8(degrees):
    a=np.asarray(degrees,float);valid=np.isfinite(a)&(a>=0)&(a<=360)
    out=np.full(a.shape,-1,dtype=int);out[valid]=np.floor(((a[valid]%360+22.5)%360)/45).astype(int);return out

# Run
def run():
    out=ROOT/'vento';out.mkdir(exist_ok=True,parents=True)
    cal,met=met_calendar();sfc=pd.read_csv(met['sfc']['path'],sep=r'\s+',skiprows=1,header=None)
    sfc['CODE']=(((sfc[0]*100+sfc[1])*100+sfc[2])*100+sfc[4]).astype('int64')
    cal=cal.merge(sfc[['CODE',15,16]].rename(columns={15:'wind_speed',16:'wind_from_deg'}),on='CODE',validate='one_to_one')

    copies={}
    for ext in ['SFC','PFL']:
        p=config.BASE/f'wrf/AERMET-3Y.{ext}';q=Path(met[ext.lower()]['path'])
        copies[ext]={'wrf_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'linked_sha256':hashlib.sha256(q.read_bytes()).hexdigest()}
        if copies[ext]['wrf_sha256']!=copies[ext]['linked_sha256']:raise ValueError('Meteorologia WRF difere da vinculada; confirmar cenário antes de filtrar.')
    cal['direction_idx']=sector8(cal.wind_from_deg);cal.loc[~cal.valid|cal.wind_speed.le(0),'direction_idx']=-1
    cal['direction']=cal.direction_idx.map(dict(enumerate(DIRS))).fillna('Inválida ou calmaria')
    cal.to_csv(out/'calendario_vento_horario.csv',index=False)
    dayrows=[]
    for day,g in cal.groupby('day'):
        v=g[g.direction_idx.ge(0)];n=len(v)
        if n:
            theta=np.deg2rad(v.wind_from_deg);u=np.mean(np.sin(theta));w=np.mean(np.cos(theta));r=float(np.hypot(u,w));deg=float(np.rad2deg(np.arctan2(u,w))%360);idx=int(sector8([deg])[0]);fraction=float(v.direction_idx.eq(idx).mean())
        else:r=0;deg=np.nan;idx=-1;fraction=0
        eligible=n>=18 and r>=.5 and fraction>=.5
        dayrows.append({'day':day,'valid_hours':n,'resultant':r,'mean_from_deg':deg,'direction_idx':idx if eligible else -1,'dominant_fraction':fraction,'eligible':eligible})
    daily=pd.DataFrame(dayrows);daily.to_csv(out/'dias_direcao_persistente.csv',index=False)
    freq=cal.groupby('direction',sort=False).agg(hours=('CODE','size'),mean_speed=('wind_speed','mean')).reset_index();freq['percent_total']=100*freq.hours/len(cal);freq.to_csv(out/'frequencia_vento.csv',index=False)
    summaries={}
    for pol,folder in [('PM10','PM10'),('PM25','PM2-5')]:
        path=config.BASE/f'out-aermod/{folder}/01_GALL.POS';stamp=out/f'{pol}_manifesto.json';target=out/f'{pol}_envelopes_horarios.csv'
        signature={'hourly_post':identity(path),'meteorology':met,'direction_method':'8 sectors from SFC, meteorological from; valid noncalm hours; 2021-2023'}
        if stamp.exists() and target.exists() and json.loads(stamp.read_text(encoding='utf8')).get('inputs')==signature:
            print(pol,'cache direcional íntegro',flush=True);continue
        from out_aermod_reader import header
        nr=header(path)['n_receptors'];assert nr and nr>0
        coords=None;maximum=np.full((8,nr),-np.inf);codes=np.zeros((8,nr),dtype='int64');sums=np.zeros((8,nr));counts=np.zeros(8,dtype=int);allmax=np.full(nr,-np.inf);rows=0
        metidx=cal.set_index('CODE');chunks=pd.read_csv(path,sep=r'\s+',comment='*',header=None,usecols=[0,1,2,8],names=['X','Y','C','CODE'],chunksize=nr*24*14)
        for chunk in chunks:
            if len(chunk)%nr:raise ValueError('Bloco incompleto de receptores')
            xy=chunk[['X','Y']].to_numpy().reshape(-1,nr,2);c=chunk.C.to_numpy().reshape(-1,nr);code=chunk.CODE.to_numpy().reshape(-1,nr)
            if coords is None:coords=xy[0].copy()
            assert np.all(xy==coords) and np.all(code==code[:,:1]) and np.isfinite(c).all() and (c>=0).all()
            t=code[:,0];keep=(t>=21010101)&(t<=23123124);c=c[keep];t=t[keep]
            if not len(t):continue
            sectors=metidx.loc[t,'direction_idx'].to_numpy();rows+=len(t)*nr
            for d in range(8):
                mask=sectors==d;v=c[mask]
                if not len(v):continue
                arg=v.argmax(axis=0);m=v[arg,np.arange(nr)];update=m>maximum[d];maximum[d,update]=m[update];codes[d,update]=t[mask][arg[update]];sums[d]+=v.sum(axis=0);counts[d]+=len(v)
            valid=sectors>=0
            if valid.any():allmax=np.maximum(allmax,c[valid].max(axis=0))
        assert rows==nr*26280 and np.all(counts>0)
        records=[]
        for d,name in enumerate(DIRS):
            records.append(pd.DataFrame({'X':coords[:,0],'Y':coords[:,1],'direction':name,'direction_from_center_deg':d*45,'max_1h':maximum[d],'max_code':codes[d],'conditional_mean_1h':sums[d]/counts[d],'hours':counts[d]}))
        result=pd.concat(records,ignore_index=True);result.to_csv(target,index=False)
        assert np.allclose(maximum.max(axis=0),allmax)

        cache=config.BASE/f'output/11_integracao/nova_modelagem/{pol}_medias_diarias_1h.csv.gz'
        ds=pd.read_csv(cache,usecols=['X','Y','day','daily_from_1h']).merge(daily[['day','direction_idx']],on='day',validate='many_to_one');ds=ds[ds.direction_idx.ge(0)]
        selected=ds.loc[ds.groupby(['X','Y','direction_idx']).daily_from_1h.idxmax()].copy();selected['direction']=selected.direction_idx.map(dict(enumerate(DIRS)));selected.to_csv(out/f'{pol}_envelopes_diarios_persistentes.csv',index=False)
        summary={'inputs':signature,'met_copies':copies,'hours_checked':rows,'hours_by_direction':dict(zip(DIRS,counts.tolist())),'valid_hours_total':int(counts.sum()),'excluded_calm_missing_hours':int(26280-counts.sum()),'daily_eligible':int(daily.eligible.sum()),'daily_rule':'minimum 18 valid hours, resultant >=0.5, at least 50% hours in mean wind sector','max_by_direction':result.groupby('direction').max_1h.max().to_dict(),'envelope_not_simultaneous':True,'wind_field_is_single_AERMET_profile':True}
        stamp.write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf8');summaries[pol]=summary
        print(pol,'envelopes concluídos',summary['hours_by_direction'],flush=True)
    return summaries

if __name__=='__main__':run()
