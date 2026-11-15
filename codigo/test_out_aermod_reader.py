# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entradas: argumentos do chamador e módulos locais relacionados no relatório.
# Campos/chaves em audit: zones_original_precision, zones_strict_export.
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
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point,box
from groups import canonical_post_group
from out_aermod_reader import link_receptors,saturation_class,filename_identity,PLT_GROUPS

# Tests
class Tests(unittest.TestCase):
    def test_numeric_plt_mapping(self):
        self.assertEqual(len(PLT_GROUPS),29)
        self.assertEqual(filename_identity('24H1G028.PLT'),('SCOF','24H'))
        self.assertEqual(filename_identity('AN00G025.PLT'),('VALE_FAB','ANNUAL'))
        self.assertEqual(filename_identity('01HGALL.PLT'),('ALL','1H'))
        self.assertEqual(filename_identity('01_GURB-VIA.POS'),('URB-VIA','1H'))
    def test_exact_groups(self):
        for gid in ['URB','URB-FER','URB-NUC','URB-VIA','SCOF','COOPERA','VALE_FAB']:
            self.assertEqual(canonical_post_group('24_G'+gid),gid)
    def test_boundaries(self):
        self.assertEqual(saturation_class(90),'Abaixo da faixa preventiva')
        self.assertEqual(saturation_class(100),'Próxima do padrão')
        self.assertEqual(saturation_class(100.001),'Acima do padrão')
        self.assertEqual(saturation_class(float('nan')),'Informação insuficiente')
    def test_recover_only_documented_rounding(self):
        z=gpd.GeoDataFrame({'zone_index':[0]},geometry=[box(0,0,1,1)],crs=31983)
        grid=gpd.GeoDataFrame(geometry=[Point(.004,.5)],crs=31983)
        coords=pd.DataFrame({'X':[0.,1.01],'Y':[.5,.5]})
        links,audit=link_receptors(coords,z,grid)
        self.assertEqual(len(links),1)
        self.assertEqual(audit['zones_strict_export'],0)
        self.assertEqual(audit['zones_original_precision'],1)

if __name__=='__main__':unittest.main()
