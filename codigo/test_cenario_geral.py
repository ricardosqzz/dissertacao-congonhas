# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entradas: argumentos do chamador e módulos locais relacionados no relatório.
# Saídas: retorno de funções, verificações ou arquivos definidos pelo chamador.
# Uso: teste; entradas sintéticas ou produtos de referência indicados abaixo.
# Novas variáveis: config/analise_extensivel.json; definir origem, campo, agregação, transformação e peso.
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
from cenario_geral_pos_banca import peak_from_valid

# Generalscenariotests
class GeneralScenarioTests(unittest.TestCase):
    def test_peak_uses_full_valid_calendar_and_first_tie(self):
        values=np.array([[999,999],[5,8],[7,8],[6,20.]])
        c,t=peak_from_valid(values,[21010101,21010102,21010103,21010104],[False,True,True,True])
        np.testing.assert_array_equal(c,[7,20])
        np.testing.assert_array_equal(t,[21010103,21010104])
        c,t=peak_from_valid(values,[21010101,21010102,21010103,21010104],[False,True,True,False])
        np.testing.assert_array_equal(t,[21010103,21010102])

    def test_no_valid_period_is_not_a_zero_concentration(self):
        with self.assertRaises(ValueError):peak_from_valid(np.array([[10,20]]),[21010101],[False])

if __name__=='__main__':unittest.main()
