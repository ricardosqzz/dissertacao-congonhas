# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: {path} | pd.read_excel.
# Entrada: E:/projeto/config.DIRS['cache']/monitoramento_mma/assinatura.json | key.read_text.
# Entrada: E:/projeto/config.DIRS['cache']/monitoramento_mma/leitura.json | .read_text.
# Campos/chaves em out: DV, PM10, PM25, VV, datetime.
# Campos/chaves em cols: VV.
# Campos/chaves em config.DIRS: cache.
# Campos/chaves em a: station_id, year.
# Campos/chaves em x: path.
# Campos/chaves em old: DATA.
# Campos/chaves em f: datetime.
# Campos/chaves em df: datetime.
# Saída: E:/projeto/config.DIRS['cache']/monitoramento_mma/leitura.json | .write_text.
# Saída: E:/projeto/config.DIRS['cache']/monitoramento_mma/assinatura.json | key.write_text.
# Campos/chaves gerados em out: DV, station_id.
# Campos/chaves gerados em day: quadrimestre, valid_day, year.
# Campos/chaves gerados em r: n_valid_hourly, n_valid_hourly_historical.
# CÓDIGO DO PROCESSAMENTO

"""Leitura da rede regional e representatividade MMA 2020, Quadro 7.

Dias: pelo menos 16 horas únicas. Ano: pelo menos 50% dos dias em CADA
quadrimestre do calendário completo. Ausências não são convertidas em zero.
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
import calendar, re, unicodedata, json
import numpy as np
import pandas as pd
import config
from standards import STANDARDS, STAGE_ORDER, annual_p98

# Norm
def norm(value):
    return re.sub('[^a-z0-9]','',unicodedata.normalize('NFKD',str(value).replace('º','').replace('°','')).encode('ascii','ignore').decode().lower())

NAMES={'basilica':('basilica','Basílica'),'jardimprofeta':('j-prof','Jardim Profeta'),
 'loboleite':('lobo-leite','Lobo Leite'),'matriz':('matriz','Matriz'),
 'motas':('motas','Motas'),'novoplataforma':('n-plat','Nova Plataforma'),
 'pires':('pires','Pires'),'casadepedra':('casa-de-pedra','Casa de Pedra'),
 'minadaviga':('mina-da-viga','Mina da Viga'),'namisa':('namisa','Namisa'),
 'fabrica':('fabrica','Fábrica'),'miguelburnier':('miguel-burnier','Miguel Burnier'),
 'ferro':('ferro','Ferro+')}
TOKENS={'pm10':'PM10','mp10':'PM10','pm25':'PM25','mp25':'PM25',
 't':'T','temperatura':'T','dv':'DV','pp':'PP','pa':'PA','vv':'VV','rs':'RS','ur':'UR'}

# Read raw
def read_raw(path):
    raw=pd.read_excel(path,header=None)
    header=max(range(min(10,len(raw))),key=lambda i:sum(norm(v) in TOKENS for v in raw.iloc[i]))
    cols={TOKENS[norm(v)]:j for j,v in enumerate(raw.iloc[header]) if norm(v) in TOKENS}
    if not cols:raise ValueError(f'Cabeçalho não reconhecido: {path}')
    n=norm(re.split(r'20\d{2}',path.stem)[0]);matches=[key for key in NAMES if key in n]
    if len(matches)!=1:raise ValueError(f'Estação ambígua: {path}')
    sid,name=NAMES[matches[0]]
    body=raw.iloc[header+1:].copy()
    dt=pd.to_datetime(body.iloc[:,0],errors='coerce',dayfirst=True)

    numeric=body.iloc[:,0].map(lambda x:isinstance(x,(float,int)) and not isinstance(x,bool))
    if numeric.any():dt.loc[numeric]=pd.to_datetime(pd.to_numeric(body.loc[numeric,0]),unit='D',origin='1899-12-30',errors='coerce')
    out=pd.DataFrame({'datetime':dt})
    for target,j in cols.items():
        s=body.iloc[:,j]
        out[target]=pd.to_numeric(s.map(lambda v:v.replace(',','.') if isinstance(v,str) else v),errors='coerce').replace([np.inf,-np.inf],np.nan)
    year=int(re.search(r'(20\d{2})',path.name)[1]);other=int((out.datetime.notna()&out.datetime.dt.year.ne(year)).sum())
    out=out[out.datetime.dt.year.eq(year)].copy();out.datetime=out.datetime.dt.floor('h')
    for pol in ['PM10','PM25']:
        if pol not in out:out[pol]=np.nan
        out[pol]=out[pol].mask(out[pol].le(0) if config.ZERO_AS_MISSING else out[pol].lt(0))
    for c in ['VV','PP','RS']:
        if c in out:out[c]=out[c].mask(out[c]<0)
    if 'DV' in out:out['DV']=out.DV.where(out.DV.between(0,360))
    units=' | '.join(str(v) for v in raw.iloc[header+1].tolist())
    if 'VV' in cols and 'km/h' in str(raw.iloc[header+1,cols['VV']]).lower():out.VV=out.VV/3.6
    out['station_id']=sid
    audit={'file':str(path),'station_id':sid,'station_name':name,'year':year,'header_row':header+1,
      'rows':len(out),'out_of_filename_year':other,'duplicate_hours':int(out.datetime.duplicated().sum()),
      'columns':list(cols),'units':units,'PM10_hours':int(out.PM10.notna().sum()),'PM25_hours':int(out.PM25.notna().sum())}
    return out,audit

# Load network
def load_network(folder=None):
    folder=Path(folder or config.BASE/'qar_met');paths=sorted(folder.rglob('*.xlsx'))
    if not paths:raise FileNotFoundError(f'Sem arquivos em {folder}')
    cache=config.DIRS['cache']/'monitoramento_mma';cache.mkdir(parents=True,exist_ok=True)
    manifest=[{'path':str(p),'size':p.stat().st_size,'mtime_ns':p.stat().st_mtime_ns} for p in paths]
    legacy_paths=sorted((config.BASE/'qar').glob('*.xlsx'))
    legacy_paths=[p for p in legacy_paths if p.stem in {v[0] for v in NAMES.values()}]
    legacy_manifest=[{'path':str(p),'size':p.stat().st_size,'mtime_ns':p.stat().st_mtime_ns} for p in legacy_paths]
    signature={'version':3,'files':manifest,'legacy_files':legacy_manifest,'zero_as_missing':config.ZERO_AS_MISSING}
    key=cache/'assinatura.json'
    if key.exists() and json.loads(key.read_text(encoding='utf8'))==signature:
        d=pd.read_pickle(cache/'horas.pkl.gz');audit=json.loads((cache/'leitura.json').read_text(encoding='utf8'))
        return {sid:g.copy() for sid,g in d.groupby('station_id')},audit

    if key.exists():
        old=json.loads(key.read_text(encoding='utf8'))
        if old.get('files')==manifest and old.get('zero_as_missing')==config.ZERO_AS_MISSING:
            d=pd.read_pickle(cache/'horas.pkl.gz')
            audit=json.loads((cache/'leitura.json').read_text(encoding='utf8'))
            for a in [a for a in audit if a.get('source_kind')=='legacy_missing_year']:
                d=d[~(d.station_id.eq(a['station_id'])&d.datetime.dt.year.eq(a['year']))]
            audit=[a for a in audit if a.get('source_kind')!='legacy_missing_year']
            d,audit=add_missing_legacy_years(d,audit,legacy_paths)
            d.to_pickle(cache/'horas.pkl.gz')
            (cache/'leitura.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf8')
            key.write_text(json.dumps(signature,ensure_ascii=False),encoding='utf8')
            return {sid:g.copy() for sid,g in d.groupby('station_id')},audit

    if key.exists():
        old=json.loads(key.read_text(encoding='utf8'))
        now={x['path']:x for x in manifest};before={x['path']:x for x in old.get('files',[])}
        additions=[p for p in paths if str(p) not in before]
        if additions and old.get('version')==2 and old.get('zero_as_missing')==config.ZERO_AS_MISSING and all(now.get(k)==v for k,v in before.items()):
            previous=pd.read_pickle(cache/'horas.pkl.gz');audit=json.loads((cache/'leitura.json').read_text(encoding='utf8'));chunks=[previous]
            for p in additions:
                frame,a=read_raw(p);chunks.append(frame);audit.append(a)
            combined=pd.concat(chunks,ignore_index=True).groupby(['station_id','datetime'],as_index=False).mean(numeric_only=True)
            combined.to_pickle(cache/'horas.pkl.gz');(cache/'leitura.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf8');key.write_text(json.dumps(signature,ensure_ascii=False),encoding='utf8')
    if key.exists() and json.loads(key.read_text(encoding='utf8'))==signature:
        d=pd.read_pickle(cache/'horas.pkl.gz');audit=json.loads((cache/'leitura.json').read_text(encoding='utf8'))
    else:
        chunks=[];audit=[]
        for i,p in enumerate(paths):
            d,a=read_raw(p);chunks.append(d);audit.append(a)
            if (i+1)%20==0:print(f'Estações: {i+1}/{len(paths)} arquivos lidos',flush=True)
        d=pd.concat(chunks,ignore_index=True)

        d=d.groupby(['station_id','datetime'],as_index=False).mean(numeric_only=True)
        d,audit=add_missing_legacy_years(d,audit,legacy_paths)
        d.to_pickle(cache/'horas.pkl.gz')
        (cache/'leitura.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf8')
        key.write_text(json.dumps(signature,ensure_ascii=False),encoding='utf8')
    return {sid:g.copy() for sid,g in d.groupby('station_id')},audit

# Add missing legacy years
def add_missing_legacy_years(data,audit,paths):
    """Completar apenas anos sem arquivo anual; nunca preencher lacunas anuais."""
    present={(a['station_id'],a['year']) for a in audit if a.get('source_kind')!='legacy_missing_year'}
    chunks=[data]
    for path in paths:
        old=pd.read_excel(path)
        if 'DATA' not in old:continue
        dt=pd.to_datetime(old['DATA'],errors='coerce').dt.floor('h')
        f=pd.DataFrame({'datetime':dt,'station_id':path.stem})
        for pol,col in [('PM10','PM10_ugm-3'),('PM25','PM2-5_ugm-3')]:
            f[pol]=pd.to_numeric(old[col],errors='coerce') if col in old else np.nan
            f[pol]=f[pol].replace([np.inf,-np.inf],np.nan)
            f[pol]=f[pol].mask(f[pol].le(0) if config.ZERO_AS_MISSING else f[pol].lt(0))
        for year,sub in f.dropna(subset='datetime').groupby(f.datetime.dt.year):
            if (path.stem,int(year)) in present:continue
            audit.append(dict(file=str(path),station_id=path.stem,year=int(year),source_kind='legacy_missing_year',
                rows=len(sub),duplicate_hours=int(sub.datetime.duplicated().sum()),
                PM10_hours=int(sub.PM10.count()),PM25_hours=int(sub.PM25.count())))
            chunks.append(sub)
    combined=pd.concat(chunks,ignore_index=True)
    return combined.groupby(['station_id','datetime'],as_index=False).mean(numeric_only=True),audit

# Daily and yearly
def daily_and_yearly(df,pol,first=2017,last=2025):
    if 'station_id' not in df:df=df.assign(station_id='serie')
    h=df[['datetime',pol]].assign(datetime=df.datetime.dt.floor('h')).groupby('datetime')[pol].mean()
    day=h.resample('D').agg(['mean','count']).reindex(pd.date_range(f'{first}-01-01',f'{last}-12-31',freq='D',name='date'))
    day.columns=['value','n_hours'];day.n_hours=day.n_hours.fillna(0).astype(int)
    day['valid_day']=day.n_hours.ge(config.MONITOR_MIN_VALID_HOURS_DAY);day.loc[~day.valid_day,'value']=np.nan
    day['year']=day.index.year;day['quadrimestre']=(day.index.month-1)//4+1
    yearly=[];periods=[]
    for year,sub in day.groupby('year'):
        q=[];vals=sub.value.dropna()
        for num,v in sub.groupby('quadrimestre'):
            valid=int(v.valid_day.sum());fraction=valid/len(v);q.append(fraction)
            periods.append(dict(station_id=df.station_id.iloc[0],pollutant=pol,year=int(year),quadrimestre=int(num),expected_days=len(v),valid_days=valid,completeness=fraction,representative=fraction>=config.MONITOR_MIN_QUADRIMESTER_COMPLETENESS))
        yearly.append(dict(station_id=df.station_id.iloc[0],pollutant=pol,year=int(year),valid_year=min(q)>=config.MONITOR_MIN_QUADRIMESTER_COMPLETENESS,
          n_valid_days=len(vals),expected_days=len(sub),valid_days_pct=100*len(vals)/len(sub),
          annual_mean=float(vals.mean()) if len(vals) else np.nan,p98=annual_p98(vals) if len(vals) else np.nan,
          quadrim1=q[0],quadrim2=q[1],quadrim3=q[2],quadrimestre_min_completeness=min(q)))
    return day,pd.DataFrame(yearly),pd.DataFrame(periods)

# All tables
def all_tables(frames,first=2017,last=2025):
    ys=[];qs=[];daily={}
    for sid,frame in frames.items():
        for pol in ['PM10','PM25']:
            if frame[pol].notna().sum()==0:continue
            day,y,q=daily_and_yearly(frame,pol,first,last);daily[sid,pol]=day;ys.append(y);qs.append(q)
    return pd.concat(ys,ignore_index=True),pd.concat(qs,ignore_index=True),daily

# Selected metrics
def selected_metrics(yearly,rolling,frames,end=2025):
    rows=[]
    for (sid,pol),g in yearly.groupby(['station_id','pollutant']):
        r=rolling[(rolling.station_id==sid)&(rolling.pollutant==pol)&(rolling.end_year==end)].iloc[0].to_dict()
        f=frames[sid]
        r['n_valid_hourly']=int(f.loc[f.datetime.dt.year.between(end-2,end),pol].notna().sum())
        r['n_valid_hourly_historical']=int(f[pol].notna().sum())
        rows.append(r)
    return pd.DataFrame(rows)
