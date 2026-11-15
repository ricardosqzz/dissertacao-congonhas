# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: {path} | gpd.read_file.
# Entrada: {path} | path.read_bytes.
# Entrada: tmp.name | gpd.read_file.
# Entrada: {path} | zipfile.ZipFile.
# Saída: {path} | out.to_file.
# Saída: path.with_name(path.stem + '_campos.csv') | .to_csv.
# CÓDIGO DO PROCESSAMENTO

from __future__ import annotations
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
import shutil
import tempfile
import zipfile
import re

import geopandas as gpd
import pandas as pd

from config import CRS_PROJECT

# Ensure dirs
def ensure_dirs(*paths: Path):
    for p in paths:
        p.mkdir(parents=True, exist_ok=True)

# First existing
def first_existing(preferred: Path | None, folder: Path, patterns):
    if preferred is not None and preferred.exists():
        return preferred
    for pattern in patterns:
        found = sorted(folder.glob(pattern)) + sorted(folder.rglob(pattern))
        if found:
            return found[0]
    return None

# Read kml with encoding fallback
def _read_kml_with_encoding_fallback(path: Path):
    try:
        return gpd.read_file(path)
    except Exception as first_error:
        raw = path.read_bytes()
        last_error = first_error
        for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
            try:
                text = raw.decode(encoding)
                with tempfile.NamedTemporaryFile("w", suffix=".kml", delete=False, encoding="utf-8") as tmp:
                    tmp.write(text)
                    tmp_path = Path(tmp.name)
                try:
                    return gpd.read_file(tmp_path)
                finally:
                    tmp_path.unlink(missing_ok=True)
            except Exception as exc:
                last_error = exc
        raise last_error

# Read vector
def read_vector(path: Path, target_crs=CRS_PROJECT):
    """Lê KML/KMZ/SHP/GPKG/GeoJSON e reprojeta."""
    if path is None or not path.exists():
        raise FileNotFoundError(path)

    suffix = path.suffix.lower()
    temp = None
    try:
        if suffix == ".kmz":
            temp = Path(tempfile.mkdtemp(prefix="kmz_"))
            with zipfile.ZipFile(path, "r") as zf:
                zf.extractall(temp)
            kmls = list(temp.rglob("*.kml"))
            if not kmls:
                raise ValueError(f"KMZ sem KML: {path}")
            gdf = _read_kml_with_encoding_fallback(kmls[0])
        elif suffix == ".kml":
            gdf = _read_kml_with_encoding_fallback(path)
        else:
            gdf = gpd.read_file(path)

        if gdf.empty:
            return gdf
        if gdf.crs is None:

            if suffix in {".kml", ".kmz"}:
                gdf = gdf.set_crs("EPSG:4326")
            else:
                raise ValueError(f"Arquivo sem CRS declarado: {path}")
        return gdf.to_crs(target_crs)
    finally:
        if temp is not None:
            shutil.rmtree(temp, ignore_errors=True)

# Normalize name
def normalize_name(s):
    s = str(s or "").strip().lower()
    s = s.replace("ç", "c").replace("ã", "a").replace("á", "a").replace("à", "a")
    s = s.replace("é", "e").replace("ê", "e").replace("í", "i").replace("ó", "o")
    s = s.replace("ô", "o").replace("õ", "o").replace("ú", "u")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

# Excel serial to datetime
def excel_serial_to_datetime(series: pd.Series):
    """Converte datas robustamente, inclusive serial Excel."""
    s = series.copy()
    numeric = pd.to_numeric(s, errors="coerce")
    numeric_share = numeric.notna().mean() if len(s) else 0
    if numeric_share > 0.8 and numeric.dropna().between(20000, 80000).mean() > 0.8:
        return pd.to_datetime(numeric, unit="D", origin="1899-12-30", errors="coerce")
    return pd.to_datetime(s, dayfirst=True, errors="coerce")

# Sanitize vector columns
def _sanitize_vector_columns(gdf):
    out = gdf.copy()
    rename = {}
    drop_cols = []
    for c in out.columns:
        if c == out.geometry.name:
            continue
        lc = str(c).strip().lower()
        if lc in {"fid", "ogc_fid"}:
            rename[c] = f"src_{lc}"
        elif lc in {"geometry"}:
            drop_cols.append(c)
    if drop_cols:
        out = out.drop(columns=drop_cols, errors="ignore")
    if rename:
        out = out.rename(columns=rename)
    return out

# Save gpkg
def save_gpkg(gdf, path: Path, layer: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    out = _sanitize_vector_columns(gdf)
    out.to_file(path, layer=layer, driver="GPKG", index=False)

# Shp safe columns
def _shp_safe_columns(gdf):
    """Renomeia atributos para <=10 caracteres e evita colisões do Shapefile."""
    out = gdf.copy()
    geom = out.geometry.name
    used = set()
    mapping = {}
    rename = {}
    for c in out.columns:
        if c == geom:
            continue
        raw = str(c)
        base = re.sub(r"[^A-Za-z0-9_]", "_", raw).upper().strip("_") or "FIELD"
        candidate = base[:10]
        if candidate in used:
            prefix = base[:7]
            i = 1
            while True:
                candidate = f"{prefix}{i:03d}"[:10]
                if candidate not in used:
                    break
                i += 1
        used.add(candidate)
        rename[c] = candidate
        mapping[raw] = candidate
    return out.rename(columns=rename), mapping

# Save shp
def save_shp(gdf, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    out = _sanitize_vector_columns(gdf)
    out, mapping = _shp_safe_columns(out)
    out.to_file(path, driver="ESRI Shapefile", index=False)

    map_path = path.with_name(path.stem + "_campos.csv")
    pd.DataFrame([{"campo_original": k, "campo_shp": v} for k, v in mapping.items()]).to_csv(
        map_path, index=False, encoding="utf-8-sig"
    )
