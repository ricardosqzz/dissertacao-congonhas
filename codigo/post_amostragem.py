# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: self.path | self.path.open.
# Campos/chaves em self.info: n_receptors, period.
# Saídas: retorno de funções, verificações ou arquivos definidos pelo chamador.
# CÓDIGO DO PROCESSAMENTO

"""Acesso verificado a POST formatado, sem ler grupos inteiros para cada pico."""
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
import numpy as np
import pandas as pd
from out_aermod_reader import header

# Fixedpost
class FixedPost:
    def __init__(self,path):
        self.path=Path(path)
        self.info=header(self.path)
        self.nr=self.info['n_receptors']
        if not self.nr:
            raise ValueError('Cabeçalho sem número de receptores')
        with self.path.open('rb') as f:
            self.offset=0
            for line in f:
                if not line.startswith(b'*'):break
                self.offset+=len(line)
            self.record_size=len(line)
            f.seek(self.offset)
            first=f.read(self.record_size*self.nr)
        count,remainder=divmod(self.path.stat().st_size-self.offset,self.record_size)
        if remainder or count%self.nr:
            raise ValueError('Estrutura de comprimento fixo inconsistente: '+str(path))
        self.nt=count//self.nr
        self.coords=np.array([[float(r[:14]),float(r[14:28])] for r in first.splitlines()])
        self.mem=np.memmap(self.path,dtype='S'+str(self.record_size),mode='r',offset=self.offset,shape=(self.nt,self.nr))
        first_code=int(self.mem[0,0].item().split()[8]);last_code=int(self.mem[-1,0].item().split()[8])
        dates=pd.date_range(pd.to_datetime(str(first_code//100),format='%y%m%d')+pd.Timedelta(hours=first_code%100-1),
                            pd.to_datetime(str(last_code//100),format='%y%m%d')+pd.Timedelta(hours=last_code%100-1),
                            freq='h' if self.info['period']=='1H' else 'D')
        proposed=(((dates.year%100*100+dates.month)*100+dates.day)*100+dates.hour+1).to_numpy(dtype=np.int64)

        self.codes=proposed if len(proposed)==self.nt else np.array([int(r.split()[8]) for r in self.mem[:,0].copy()],dtype=np.int64)
        if len(np.unique(self.codes))!=self.nt:
            raise ValueError('Período duplicado no POST')
        self.lookup={int(v):i for i,v in enumerate(self.codes)}
        for t,j in [(0,0),(self.nt-1,self.nr-1),(self.nt//2,self.nr//2)]:
            row=self.mem[t,j].item().split()
            if int(row[8])!=self.codes[t] or not np.allclose(list(map(float,row[:2])),self.coords[j],rtol=0,atol=.001):
                raise ValueError('Ordenação de receptores ou períodos inesperada')
            if abs(float(self.mem[t,j].item()[28:42])-float(row[2]))>1e-10:
                raise ValueError('Campo de concentração incompatível')

    def receptor_indices(self,xy):
        mapping={tuple(v):j for j,v in enumerate(self.coords)}
        try:return np.array([mapping[tuple(v)] for v in np.asarray(xy)],int)
        except KeyError as e:raise ValueError('Receptor solicitado ausente do POST') from e

    def values(self,time_indices=None,receptor_indices=None):

        view=np.ndarray(shape=(self.nt,self.nr),dtype='S14',buffer=self.mem,offset=28,
                        strides=(self.record_size*self.nr,self.record_size))
        if time_indices is None and receptor_indices is None:
            result=view.astype(float)
        else:
            ti=np.arange(self.nt) if time_indices is None else np.asarray(time_indices)
            ri=np.arange(self.nr) if receptor_indices is None else np.asarray(receptor_indices)
            result=view[np.ix_(ti,ri)].astype(float)
        if not np.isfinite(result).all() or (result<0).any():
            raise ValueError('Concentração inválida no POST')
        return result

    def sample(self,codes,xy):
        codes=np.asarray(codes,dtype=np.int64)
        rows=np.array([self.lookup[int(v)] for v in codes])
        cols=self.receptor_indices(xy)
        records=np.empty(len(rows),dtype='S'+str(self.record_size))
        with self.path.open('rb') as f:
            for t in np.unique(rows):
                select=np.flatnonzero(rows==t)
                f.seek(self.offset+int(t)*self.nr*self.record_size)
                block=np.frombuffer(f.read(self.nr*self.record_size),dtype='S'+str(self.record_size))
                records[select]=block[cols[select]]
        values=np.array([float(v.item()[28:42]) for v in records])
        actual=np.array([int(v.item().split()[8]) for v in records])
        actual_xy=np.array([[float(v.item()[:14]),float(v.item()[14:28])] for v in records])
        if not np.array_equal(actual,codes) or not np.allclose(actual_xy,xy,rtol=0,atol=.001) or not np.isfinite(values).all() or (values<0).any():
            raise ValueError('Falha ao recuperar o evento selecionado')
        return values

    def close(self):
        self.mem._mmap.close()
