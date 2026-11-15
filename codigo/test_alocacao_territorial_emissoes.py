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
import pandas as pd
import geopandas as gpd
from shapely.geometry import box,Point,LineString
from alocacao_territorial_emissoes import partition,geometry_for_allocation,emission_class

# Rateiotests
class RateioTests(unittest.TestCase):
    def zones(self,geoms):return gpd.GeoDataFrame(geometry=geoms,crs=31983)
    def test_area_and_volume(self):
        z=self.zones([box(0,0,25,10),box(25,0,100,10)])
        p,o,a,total=partition(box(0,0,100,10),z,'área horizontal')
        self.assertEqual(sorted(f for _,f,_ in p),[.25,.75]);self.assertEqual(o+a,0)
    def test_line_with_external_fraction(self):
        z=self.zones([box(0,0,25,10),box(25,0,50,10)])
        p,o,a,t=partition(LineString([(0,5),(100,5)]),z,'comprimento')
        self.assertEqual(sorted(f for _,f,_ in p),[.25,.25]);self.assertEqual(o,.5)
    def test_overlap_not_duplicated(self):
        z=self.zones([box(0,0,60,10),box(40,0,100,10)])
        p,o,a,t=partition(box(0,0,100,10),z,'área')
        self.assertAlmostEqual(sum(f for _,f,_ in p),.8);self.assertAlmostEqual(a,.2)
    def test_point_boundary_pending(self):
        z=self.zones([box(0,0,50,10),box(50,0,100,10)])
        self.assertEqual(partition(Point(50,5),z,'ponto')[:3],([],0.,1.))
    def test_line_on_shared_boundary(self):
        z=self.zones([box(0,0,50,10),box(50,0,100,10)])
        p,o,a,t=partition(LineString([(50,0),(50,10)]),z,'comprimento')
        self.assertEqual(p,[]);self.assertAlmostEqual(a,1);self.assertEqual(o,0)
    def test_oblique_line_closure_large_coordinates(self):
        z=self.zones([box(600000,7730000,600032.323,7730100),box(600032.323,7730000,600076.789,7730100)])
        p,o,a,t=partition(LineString([(600000.123,7730001.111),(600099.987,7730087.678)]),z,'comprimento')
        self.assertAlmostEqual(sum(f for _,f,_ in p)+o+a,1,places=12)
    def test_point_visual_polygon_is_not_footprint(self):
        s=pd.Series({'source_type':'POINT','geometry':box(0,0,10,10)})
        geom,basis=geometry_for_allocation(s,{'Num_Coords':1,'X1':5,'Y1':5})
        self.assertEqual(geom,Point(5,5));self.assertEqual(basis,'ponto')
    def test_volume_without_footprint_stays_pending(self):
        s=pd.Series({'source_type':'VOLUME','geometry':Point(5,5)})
        self.assertIsNone(geometry_for_allocation(s,{'Num_Coords':1,'X1':5,'Y1':5})[0])
    def test_total_of_two_groups_is_high(self):
        self.assertEqual(emission_class(60+60,5),'Alta (>100 t/ano)')
        self.assertEqual(emission_class(100,5),'Intermediária')
        self.assertEqual(emission_class(5,5),'Baixa / minoritária')

if __name__=='__main__':unittest.main()
