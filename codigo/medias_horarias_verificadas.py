# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: E:/projeto/houremiss/AERMET-3Y.SFC | pd.read_csv.
# Entrada: E:/projeto/houremiss/AERMET-3Y.PFL | pd.read_csv.
# Entrada: E:/projeto/houremiss/AERMET-3Y.SFC | s.read_bytes.
# Entrada: E:/projeto/houremiss/AERMET-3Y.PFL | p.read_bytes.
# Entrada: E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_medias_diarias_1h_manifesto.json | meta.read_text.
# Entrada: E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_medias_diarias_1h.csv.gz | pd.read_csv.
# Entrada: selected['ALL', '24H'] | read_table.
# Entrada: selected['ALL', '1H'] | pd.read_csv.
# Campos/chaves em config.DIRS: out, post.
# Campos/chaves em cal: CODE, year.
# Campos/chaves em m: comparison_passed, daily_post, meteorology.
# Campos/chaves em d: date, day.
# Campos/chaves em selected: 1H, 24H, ALL, ANNUAL.
# Campos/chaves em raw24: CODE, X, Y, day.
# Campos/chaves em chunk: CONC, X, Y.
# Campos/chaves em sums: count, sum.
# Campos/chaves em a: sum.
# Saída: E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_medias_diarias_1h.csv.gz | check.to_csv.
# Saída: E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_denominadores_diarios.csv | daytable.to_csv.
# Saída: E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_auditoria_media_anual_horaria.csv | a.to_csv.
# Saída: E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_medias_diarias_1h_manifesto.json | .write_text.
# Saída: E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/auditoria_medias_horarias.json | .write_text.
# Campos/chaves gerados em cal: day, year.
# Campos/chaves gerados em d: date, year.
# Campos/chaves gerados em raw24: day.
# Campos/chaves gerados em chunk: day.
# Campos/chaves gerados em sums: daily_from_1h, denominator, mean_div24, valid_hours.
# Campos/chaves gerados em check: difference.
# Campos/chaves gerados em a: annual_reconstructed, denominator.
# X: coordenada leste em metros.
# Y: coordenada norte em metros.
# CÓDIGO DO PROCESSAMENTO

"""Reconstrói 24 h dos POST de 1 h com calendário meteorológico independente."""
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

OUT=config.DIRS['out']/'11_integracao/nova_modelagem'

# Model daily mean
def model_daily_mean(hourly_sum,valid_hours):
 """Política de calmarias para 24 h: denominador válido, mínimo de 18."""
 if np.any(np.asarray(valid_hours)<0) or np.any(np.asarray(valid_hours)>24):raise ValueError('Contagem diária fora de 0–24 h')
 return np.asarray(hourly_sum)/np.maximum(valid_hours,18)

# Identity
def identity(p):
 p=Path(p);return {'path':str(p.resolve()),'bytes':p.stat().st_size,'mtime_ns':p.stat().st_mtime_ns}

# Met calendar
def met_calendar():
 s=config.BASE/'houremiss/AERMET-3Y.SFC';p=config.BASE/'houremiss/AERMET-3Y.PFL'
 f=pd.read_csv(s,sep=r'\s+',skiprows=1,header=None)
 code=((f[0]*100+f[1])*100+f[2])*100+f[4]
 valid=f[15].gt(0)&f[6].gt(0)&f[18].gt(0)&f[11].ne(0)&f[11].gt(-99990)

 valid &= np.where(f[5].gt(0),f[7].gt(0)&f[9].gt(0),f[10].gt(0))
 profile=pd.read_csv(p,sep=r'\s+',header=None)
 pc=((profile[0]*100+profile[1])*100+profile[2])*100+profile[3]
 profile_ok=profile[7].ge(0)&profile[7].lt(90)&profile[8].gt(-90)&profile[8].lt(90)
 profile_ok=pd.Series(profile_ok.to_numpy(),index=pc).groupby(level=0).any()
 valid &= code.map(profile_ok).fillna(False)
 cal=pd.DataFrame({'CODE':code.astype('int64'),'valid':valid.astype(bool)})
 assert not cal.CODE.duplicated().any()
 cal['day']=cal.CODE//100;cal['year']=2000+cal.CODE//1_000_000
 cal=cal[cal.year.between(2021,2023)]
 assert len(cal)==3*8760
 return cal,{'sfc':identity(s),'pfl':identity(p),'sfc_sha256':hashlib.sha256(s.read_bytes()).hexdigest(),'pfl_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}

# Cached daily
def cached_daily(path24):
 """Retorna somente cache verificado contra os arquivos ainda presentes."""
 path24=Path(path24);pol='PM10' if path24.parent.name.upper()=='PM10' else 'PM25'
 meta=OUT/f'{pol}_medias_diarias_1h_manifesto.json';data=OUT/f'{pol}_medias_diarias_1h.csv.gz'
 if not meta.exists() or not data.exists():raise ValueError('Execute auditar_medias_horarias.py antes de calcular os indicadores diários.')
 m=json.loads(meta.read_text(encoding='utf8'))
 for key in ['hourly_post','daily_post']:
  if identity(m[key]['path'])!=m[key]:raise ValueError('POST alterado após a conferência horária; refazer auditar_medias_horarias.py.')
 if identity(path24)!=m['daily_post']:raise ValueError('Cache não corresponde ao POST de 24 h solicitado.')
 for key in ['sfc','pfl']:
  if identity(m['meteorology'][key]['path'])!=m['meteorology'][key]:raise ValueError('Meteorologia alterada após a conferência horária.')
 if not m['comparison_passed']:raise ValueError('Comparação horária não aprovada.')
 d=pd.read_csv(data,usecols=['X','Y','day','daily_from_1h'])
 d['date']=pd.to_datetime(d.day.astype(str),format='%y%m%d');d['year']=d.date.dt.year
 return d.rename(columns={'daily_from_1h':'CONC'})[['X','Y','date','year','CONC']]

# Run
def run():
 from out_aermod_reader import discover,read_table,annual
 OUT.mkdir(exist_ok=True,parents=True);cal,met=met_calendar();valid=cal.set_index('CODE').valid
 days=cal.groupby('day').valid.sum().rename('valid_hours');report={}
 for pol,folder in [('PM10','PM10'),('PM25','PM2-5')]:
  selected,_=discover(config.DIRS['post']/folder);path=selected['ALL','1H'];parts=[];nrows=0;invalid_nonzero=0
  print(pol,'lendo integralmente POST de 1 h',flush=True)
  raw24=read_table(selected['ALL','24H']);raw24['day']=raw24.CODE//100
  raw24=raw24[raw24.day.between(210101,231231)][['X','Y','day','CONC']]
  nr=raw24[['X','Y']].drop_duplicates().shape[0]
  for chunk in pd.read_csv(path,sep=r'\s+',comment='*',header=None,usecols=[0,1,2,6,7,8],names=['X','Y','CONC','AVE','GRP','CODE'],chunksize=nr*24*14):
   nrows+=len(chunk);assert set(chunk.AVE)=={'1-HR'} and set(chunk.GRP)=={'ALL'}
   assert np.isfinite(chunk[['X','Y','CONC']]).all().all() and chunk.CONC.ge(0).all()
   assert chunk.groupby('CODE').size().eq(nr).all() and not chunk.duplicated(['X','Y','CODE']).any()
   chunk['day']=chunk.CODE//100;chunk=chunk[chunk.day.between(210101,231231)].copy()
   if chunk.empty:continue
   ok=chunk.CODE.map(valid);assert ok.notna().all()
   invalid_nonzero+=int((~ok&chunk.CONC.ne(0)).sum())
   parts.append(chunk.groupby(['X','Y','day'],as_index=False).CONC.agg(['sum','count']).reset_index())
  assert invalid_nonzero==0,'Concentração não nula em hora meteorológica inválida; revisar calendário.'
  sums=pd.concat(parts).groupby(['X','Y','day'],as_index=False)[['sum','count']].sum()
  assert sums['count'].eq(24).all() and len(sums)==nr*1095
  sums['valid_hours']=sums.day.map(days);sums['denominator']=np.maximum(sums.valid_hours,18)
  sums['mean_div24']=sums['sum']/24;sums['daily_from_1h']=model_daily_mean(sums['sum'],sums.valid_hours)
  check=sums.merge(raw24.rename(columns={'CONC':'native_24h'}),on=['X','Y','day'],validate='one_to_one')
  assert len(check)==len(raw24)==len(sums)
  check['difference']=check.daily_from_1h-check.native_24h
  passed=np.isclose(check.daily_from_1h,check.native_24h,rtol=2e-7,atol=1e-5)
  assert passed.all(),f'{pol}: divergências além do arredondamento; não publicar o cache.'
  data=OUT/f'{pol}_medias_diarias_1h.csv.gz';check.to_csv(data,index=False,compression='gzip')
  daytable=check.groupby('day').agg(valid_hours=('valid_hours','first'),denominator=('denominator','first'),max_abs_difference=('difference',lambda x:x.abs().max())).reset_index()
  daytable.to_csv(OUT/f'{pol}_denominadores_diarios.csv',index=False)
  byyear=cal.groupby('year').valid.sum();a=annual(selected['ALL','ANNUAL'])
  annualsum=sums.assign(year=2000+sums.day//10000).groupby(['X','Y','year'],as_index=False)['sum'].sum()
  a=a.merge(annualsum,on=['X','Y','year'],validate='one_to_one');a['denominator']=a.year.map(byyear);a['annual_reconstructed']=a['sum']/a.denominator
  assert np.isclose(a.annual_reconstructed,a.CONC,rtol=2e-7,atol=1e-5).all()
  a.to_csv(OUT/f'{pol}_auditoria_media_anual_horaria.csv',index=False)
  m={'hourly_post':identity(path),'daily_post':identity(selected['ALL','24H']),'meteorology':met,'comparison_passed':bool(passed.all()),'denominators_inferred_from_24h':False,'rows_checked':len(check),'hourly_rows':nrows,'cache':str(data)}
  (OUT/f'{pol}_medias_diarias_1h_manifesto.json').write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding='utf8')
  report[pol]={'max_daily_difference':float(check.difference.abs().max()),'max_annual_difference':float((a.annual_reconstructed-a.CONC).abs().max()),'max_difference_mean_div24':float((check.mean_div24-check.native_24h).abs().max()),'annual_hours':{int(y):int(n) for y,n in byyear.items()},'daily_min_effective_hours':int(days.min()),'daily_max_effective_hours':int(days.max()),'days_with_minimum_denominator_18':int(days.lt(18).sum()),'daily_comparisons':len(check),'hourly_rows_checked':nrows,'invalid_hours_with_nonzero_concentration':invalid_nonzero,'denominators_inferred':False,'interpretation':'Médias reconstruídas dos POST horários; calendário independente SFC/PFL e mínimo de 18 h conforme política de calmarias; comparação com 24 h e anual nativos.'}
  print(pol,json.dumps(report[pol],ensure_ascii=False),flush=True)
 (OUT/'auditoria_medias_horarias.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
 return report

if __name__=='__main__':run()
