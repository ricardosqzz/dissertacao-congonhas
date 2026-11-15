# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entradas: argumentos do chamador e módulos locais relacionados no relatório.
# Saídas: retorno de funções, verificações ou arquivos definidos pelo chamador.
# Uso: teste; entradas sintéticas ou produtos de referência indicados abaixo.
# CÓDIGO DO PROCESSAMENTO

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

import unittest
import numpy as np
from medias_horarias_verificadas import model_daily_mean

# Dailymeans
class DailyMeans(unittest.TestCase):
 def test_calm_hours_do_not_become_valid_zeros(self):
  self.assertAlmostEqual(float(model_daily_mean(120,20)),6)
  self.assertAlmostEqual(float(model_daily_mean(120,12)),120/18)
  self.assertAlmostEqual(float(model_daily_mean(120,24)),5)
 def test_zero_total_keeps_valid_calendar(self):
  np.testing.assert_array_equal(model_daily_mean([0,180,190],[24,18,19]),[0,10,10])
 def test_impossible_calendar_rejected(self):
  for n in [-1,25]:
   with self.assertRaises(ValueError):model_daily_mean(100,n)

if __name__=='__main__':unittest.main()
