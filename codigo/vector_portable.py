# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: {path} | gpd.read_file.
# Entrada: path.with_suffix('.cpg') | .read_text.
# Entrada: path.with_suffix('.prj') | .read_text.
# Campos/chaves em r.__geo_interface__: features.
# Saída: Path(path).with_suffix('.prj') | .write_text.
# Saída: Path(path).with_suffix('.cpg') | .write_text.
# Saída: Path(path).with_name(Path(path).stem + '_campos.csv') | .to_csv.
# CÓDIGO DO PROCESSAMENTO

"""I/O vetorial sem dependência de GDAL; preserva CRS e geometrias, sem alterar segurança."""
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
import sqlite3,struct,xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import shape,Polygon,mapping
from shapely import from_wkb,to_wkb
from shapely.geometry.polygon import orient
from shapely.ops import transform
from pyproj import CRS

# Read
def read(path):
    path=Path(path)
    if path.suffix.lower()=='.shp':
        try:
            import shapefile
        except ImportError:
            return gpd.read_file(path)
        enc=path.with_suffix('.cpg').read_text().strip() if path.with_suffix('.cpg').exists() else 'utf-8'
        with shapefile.Reader(str(path),encoding=enc) as r:
            features=list(r.__geo_interface__['features'])
        return gpd.GeoDataFrame.from_features(features,crs=CRS.from_wkt(path.with_suffix('.prj').read_text()))
    if path.suffix.lower()=='.kml':
        root=ET.parse(path).getroot();ns={'k':'http://www.opengis.net/kml/2.2'};geoms=[]
        def coords(node):return [tuple(map(float,t.split(',')[:2])) for t in node.text.split()]
        for p in root.findall('.//k:Polygon',ns):
            outer=p.find('k:outerBoundaryIs/k:LinearRing/k:coordinates',ns)
            inner=p.findall('k:innerBoundaryIs/k:LinearRing/k:coordinates',ns)
            geoms.append(Polygon(coords(outer),[coords(i) for i in inner]))
        if not geoms:raise ValueError(f'Nenhum polígono em {path}')
        return gpd.GeoDataFrame(geometry=geoms,crs=4326)
    if path.suffix.lower()=='.gpkg':
        with sqlite3.connect(f'file:{path.as_posix()}?mode=ro',uri=True) as c:
            table,col,srid=c.execute('select table_name,column_name,srs_id from gpkg_geometry_columns').fetchone()
            df=pd.read_sql_query(f'SELECT * FROM "{table}"',c)
            wkt=c.execute('select definition from gpkg_spatial_ref_sys where srs_id=?',(srid,)).fetchone()[0]
        c.close()
        def decode(blob):
            envelope=(blob[3]>>1)&7
            offset=8+{0:0,1:32,2:48,3:48,4:64}[envelope]
            return from_wkb(blob[offset:])
        geom=df.pop(col).map(decode)
        return gpd.GeoDataFrame(df,geometry=geom,crs=wkt)
    raise ValueError(f'Formato não suportado: {path}')

# Write gpkg
def write_gpkg(gdf,path,layer='zoneamento'):
    path=Path(path);tmp=path.with_name(path.stem+'.tmp.gpkg')
    if tmp.exists():raise FileExistsError(f'Arquivo temporário anterior: {tmp}')
    epsg=gdf.crs.to_epsg();cols=[x for x in gdf if x!=gdf.geometry.name and x.lower() not in ('fid','ogc_fid')]
    def q(s):return '"'+s.replace('"','""')+'"'
    def sqltype(s):return 'INTEGER' if pd.api.types.is_integer_dtype(s) or pd.api.types.is_bool_dtype(s) else 'REAL' if pd.api.types.is_numeric_dtype(s) else 'TEXT'
    with sqlite3.connect(tmp) as c:
        c.executescript('''PRAGMA application_id=1196444487; PRAGMA user_version=10300;
        CREATE TABLE gpkg_spatial_ref_sys(srs_name TEXT NOT NULL,srs_id INTEGER NOT NULL PRIMARY KEY,organization TEXT NOT NULL,organization_coordsys_id INTEGER NOT NULL,definition TEXT NOT NULL,description TEXT);
        CREATE TABLE gpkg_contents(table_name TEXT NOT NULL PRIMARY KEY,data_type TEXT NOT NULL,identifier TEXT UNIQUE,description TEXT DEFAULT '',last_change DATETIME NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),min_x DOUBLE,min_y DOUBLE,max_x DOUBLE,max_y DOUBLE,srs_id INTEGER);
        CREATE TABLE gpkg_geometry_columns(table_name TEXT NOT NULL,column_name TEXT NOT NULL,geometry_type_name TEXT NOT NULL,srs_id INTEGER NOT NULL,z TINYINT NOT NULL,m TINYINT NOT NULL,PRIMARY KEY(table_name,column_name));''')
        for srid,name,org,definition in [(-1,'Undefined Cartesian','NONE','undefined'),(0,'Undefined geographic','NONE','undefined'),(4326,'WGS 84','EPSG',CRS.from_epsg(4326).to_wkt()),(epsg,str(gdf.crs),'EPSG',gdf.crs.to_wkt())]:
            c.execute('INSERT OR IGNORE INTO gpkg_spatial_ref_sys VALUES(?,?,?,?,?,?)',(name,srid,org,srid,definition,''))
        c.execute(f'CREATE TABLE {q(layer)}(fid INTEGER PRIMARY KEY AUTOINCREMENT,geom BLOB,'+','.join(q(x)+' '+sqltype(gdf[x]) for x in cols)+')')
        c.execute('INSERT INTO gpkg_contents(table_name,data_type,identifier,min_x,min_y,max_x,max_y,srs_id) VALUES(?,?,?,?,?,?,?,?)',(layer,'features',layer,*map(float,gdf.total_bounds),epsg))
        c.execute('INSERT INTO gpkg_geometry_columns VALUES(?,?,?,?,?,?)',(layer,'geom','GEOMETRY',epsg,0,0))
        def native(x):
            if pd.isna(x):return None
            if isinstance(x,(np.integer,np.bool_,bool)):return int(x)
            if isinstance(x,np.floating):return float(x)
            return x if isinstance(x,(int,float,str)) else str(x)
        rows=[]
        for _,r in gdf.iterrows():rows.append((b'GP'+bytes([0,1])+struct.pack('<i',epsg)+to_wkb(r.geometry,output_dimension=2),*[native(r[x]) for x in cols]))
        c.executemany(f'INSERT INTO {q(layer)}(geom,'+','.join(map(q,cols))+') VALUES('+','.join('?' for _ in range(len(cols)+1))+')',rows)
    c.close()
    tmp.replace(path)

# Write shp
def write_shp(gdf,path):
    import shapefile
    from io_utils import _shp_safe_columns,_sanitize_vector_columns
    gdf,aliases=_shp_safe_columns(_sanitize_vector_columns(gdf));cols=[c for c in gdf if c!=gdf.geometry.name]
    with shapefile.Writer(str(path),shapeType=shapefile.POLYGON,encoding='utf-8') as w:
        for col in cols:
            s=gdf[col]
            if pd.api.types.is_bool_dtype(s):w.field(col,'L')
            elif pd.api.types.is_numeric_dtype(s):w.field(col,'N',size=24,decimal=8)
            else:w.field(col,'C',size=254)
        from shapely.geometry import MultiPolygon
        for _,r in gdf.iterrows():
            geom=r.geometry
            if geom.geom_type=='MultiPolygon':geom=MultiPolygon([orient(p,sign=-1) for p in geom.geoms])
            elif geom.geom_type=='Polygon':geom=orient(geom,sign=-1)
            else:raise ValueError(f'Shapefile requer polígonos: {geom.geom_type}')
            w.shape(mapping(geom));w.record(*[None if pd.isna(r[c]) else r[c].item() if isinstance(r[c],np.generic) else r[c] for c in cols])
    Path(path).with_suffix('.prj').write_text(gdf.crs.to_wkt(version='WKT1_ESRI'))
    Path(path).with_suffix('.cpg').write_text('UTF-8')
    pd.DataFrame([{'campo_original':a,'campo_shp':b} for a,b in aliases.items()]).to_csv(Path(path).with_name(Path(path).stem+'_campos.csv'),index=False,encoding='utf-8-sig')
