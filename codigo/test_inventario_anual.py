# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entradas: argumentos do chamador e módulos locais relacionados no relatório.
# Campos/chaves em m.loc: emission_class, emission_high, emission_total_tpy.
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
from shapely.geometry import Polygon,LineString,GeometryCollection
from aermod_sources import _clean_geometry
from groups import infer_primary_group_from_source,canonical_group
from methodology_rules import group_mass_classes

# Inventorytests
class InventoryTests(unittest.TestCase):
    def test_mixed_geometry_preserves_area(self):
        poly=Polygon([(0,0),(2,0),(2,2),(0,2)])
        g=_clean_geometry(GeometryCollection([poly,LineString([(2,2),(3,3)])]))
        self.assertEqual(g.geom_type,'Polygon');self.assertEqual(g.area,4)

    def test_ids(self):
        for source,group in [('AEX01BCCA','CSN-CDP'),('VIA02CPI','CSN-PIR'),('CH01GER','GERDAU'),('VIA01VMF','VALE_FAB'),('VIA01VMV','VALE_VIG'),('AEX01FEP','FERRO'),('WG01','WGM')]:
            self.assertEqual(infer_primary_group_from_source(source),group)
        self.assertEqual(canonical_group('VALE S.A. - Mina de Fábrica'),'VALE_FAB')
        self.assertEqual(infer_primary_group_from_source('SCOF11','ÁREA CARREGAMENTO FERROVIÁRIO'),'SCOF')

    def test_annual_mass_not_annualized_twice(self):
        a=pd.DataFrame({'zone_index':[1,1,2,2,3], 'group_id':['a','a','a','b','a'],
            'emission_gs':[1.]*5,'emission_tpy':[60.,41.,60.,60.,100.]})
        m,g=group_mass_classes(a,[1,2,3],'PM10',annualization_basis='inventario_conciliado')
        self.assertTrue(m.loc[1,'emission_high']);self.assertTrue(m.loc[2,'emission_high'])
        self.assertFalse(m.loc[3,'emission_high']);self.assertEqual(m.loc[2,'emission_total_tpy'],120)

    def test_known_high_not_masked_by_unknown(self):
        a=pd.DataFrame({'zone_index':[1,1],'group_id':['a',None],
            'emission_gs':[1.,1.],'emission_tpy':[101.,10.]})
        m,g=group_mass_classes(a,[1],'PM10',annualization_basis='inventario_conciliado')
        self.assertTrue(m.loc[1,'emission_high']);self.assertEqual(m.loc[1,'emission_class'],'Majoritária')

if __name__=='__main__':unittest.main()
