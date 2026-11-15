# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: {path} | pd.read_excel.
# Campos/chaves em df: Emission_Rate, Type.
# Campos/chaves em row: Emission_Rate, Type.
# Campos/chaves em config.DIRS: emission.
# Campos/chaves em cand.loc: _empname.
# Campos/chaves em emp.loc: _empname.
# Campos/chaves em out.at: urban_subgroup.
# Campos/chaves em src: emission_rate_native, source_id.
# Campos/chaves em z: AREA_KM2, EMIS_ALTA_INDUSTRIAL, EMIS_ALTA_URBANA, EMIS_DENS_GS_KM2, EMIS_FORA_MUN_GS, EMIS_HOTSPOT_P95, EMIS_INDUSTRIAL_GS, EMIS_PRESSAO_TIPO, EMIS_TOTAL_GS, EMIS_URBANA_GS, GRUPO_EMISSOR_LOCAL_ID.
# Campos/chaves em a: emission_gs, group_id.
# Campos/chaves em local: rank.
# Campos/chaves em dominant: group_id.
# Campos/chaves em sources: AEX, group_id.
# Campos/chaves em aa: emission_gs, group_id.
# Campos/chaves em z.loc: EMIS_URBANA_GS.
# Campos/chaves em s: allocated_gs, emission_total_gs.
# Campos/chaves em meta: expected, name.
# Saídas: retorno de funções, verificações ou arquivos definidos pelo chamador.
# Campos/chaves gerados em df: Emission_Rate, Type.
# Campos/chaves gerados em out: enterprise.
# Campos/chaves gerados em emp: _empname, geometry.
# Campos/chaves gerados em z: AREA_KM2, CONTR_EXTERNA_PCT, EMIS_ALTA_FOCAL, EMIS_ALTA_INDUSTRIAL, EMIS_ALTA_TOTAL, EMIS_ALTA_URBANA, EMIS_CRITERIO, EMIS_DENS_CLASS, EMIS_DENS_GS_KM2, EMIS_DENS_Q33, EMIS_DENS_Q67, EMIS_DENTRO_MUN_GS, EMIS_FORA_MUN_GS, EMIS_HOTSPOT_P95, EMIS_INDUSTRIAL_GS, EMIS_PRESSAO_ALTA, EMIS_PRESSAO_SCORE, EMIS_PRESSAO_TIPO, EMIS_THR_HOTSPOT_P95, EMIS_THR_INDUSTRIAL_GS, EMIS_THR_TOTAL_GS, EMIS_THR_URBANA_GS, EMIS_TOTAL_GS, EMIS_URBANA_GS, GRUPO_EMISSOR_LOCAL, GRUPO_EMISSOR_LOCAL_ID.
# Campos/chaves gerados em local: rank.
# Campos/chaves gerados em aa: _urban_road, emission_gs.
# Campos/chaves gerados em s: allocated_gs, allocated_pct, unallocated_gs.
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
import math
import re

import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon, LineString, box
from shapely import affinity
from shapely.validation import make_valid

import config
from io_utils import read_vector, normalize_name
from groups import infer_primary_group_from_source, urban_subgroup_from_source, is_exposed_area, canonical_group, GROUPS

VALID_TYPES = {"POINT", "AREA", "AREA_CIRC", "AREA_POLY", "VOLUME", "OPEN_PIT", "LINE", "LINE_VOLUME", "LINE_AREA", "RLINE", "RLINEXT"}
AREA_RATE_TYPES = {"AREA", "AREA_CIRC", "AREA_POLY", "OPEN_PIT", "LINE_AREA", "LINE", "RLINE"}
TOTAL_RATE_TYPES = {"POINT", "VOLUME", "LINE_VOLUME"}
LENGTH_RATE_TYPES = {"RLINEXT"}

# Kml name column
def _kml_name_column(gdf):
    preferred = ["name", "nome", "source_id", "id", "description"]
    columns = {str(c).lower(): c for c in gdf.columns}
    for key in preferred:
        c = columns.get(key)
        if c is None:
            continue
        values = gdf[c].dropna().astype(str).str.strip()
        if not values.empty and values.ne("").any():
            return c
    return None

# Clean geometry
def _clean_geometry(geom):
    if geom is None or geom.is_empty:
        return geom
    try:
        from shapely import force_2d

        geom = force_2d(geom)
    except Exception:
        pass
    try:
        if not geom.is_valid:
            geom = make_valid(geom)
    except Exception:
        try:
            geom = geom.buffer(0)
        except Exception:
            pass

    if geom.geom_type == 'GeometryCollection':
        from shapely.ops import unary_union
        parts=[]
        def collect(g):
            if g.geom_type in ('GeometryCollection','MultiPolygon','MultiLineString','MultiPoint'):
                for p in g.geoms:collect(p)
            elif not g.is_empty:parts.append(g)
        collect(geom)
        for types in ({'Polygon'},{'LineString','LinearRing'},{'Point'}):
            selected=[p for p in parts if p.geom_type in types]
            if selected:
                geom=unary_union(selected)
                break
    return geom

# Geometry lookup keys
def _geometry_lookup_keys(value):
    key = normalize_name(value)
    if not key:
        return []
    keys = [key]
    for suffix in ("-base", "-poly", "-polygon", "-line", "-point"):
        if key.endswith(suffix):
            keys.append(key[: -len(suffix)])
    return list(dict.fromkeys(k for k in keys if k))

# Load source geometries from files
def load_source_geometries_from_files(base_dir: Path):
    lookup = {}
    patterns = getattr(config, "SOURCE_GEOMETRY_SEARCH_PATTERNS", [])
    files = []
    for pattern in patterns:
        files.extend(sorted(base_dir.glob(pattern)))
        files.extend(sorted(base_dir.rglob(pattern)))
    seen = set()
    dedup = []
    for f in files:
        if f not in seen and f.exists():
            dedup.append(f); seen.add(f)
    for f in dedup:
        try:
            gdf = read_vector(f)
            if gdf.empty:
                continue
            name_col = _kml_name_column(gdf)
            if name_col is None:
                continue
            for r in gdf.itertuples():
                geom = getattr(r, 'geometry')
                if geom is None or geom.is_empty:
                    continue
                geom = _clean_geometry(geom)
                for key in _geometry_lookup_keys(getattr(r, name_col)):
                    if key not in lookup:
                        lookup[key] = geom
        except Exception:
            continue
    return lookup

# Detect lakes header
def detect_lakes_header(path: Path):
    head = pd.read_excel(path, header=None, nrows=80)
    for idx, row in head.iterrows():
        a = str(row.iloc[0]).strip() if len(row) > 0 else ""
        b = str(row.iloc[1]).strip() if len(row) > 1 else ""
        if a == "Type" and b == "ID":
            return int(idx)
    raise ValueError(f"Cabeçalho Type/ID não encontrado em {path}")

# Read lakes sources
def read_lakes_sources(path: Path):
    header_idx = detect_lakes_header(path)
    df = pd.read_excel(path, header=header_idx)
    df.columns = [str(c).strip() for c in df.columns]
    if "Type" not in df or "ID" not in df or "Emission_Rate" not in df:
        raise ValueError("Arquivo Lakes sem Type/ID/Emission_Rate")

    df["Type"] = df["Type"].astype(str).str.strip().str.upper()
    df["Emission_Rate"] = pd.to_numeric(df["Emission_Rate"], errors="coerce")

    df = df[df["Type"].isin(VALID_TYPES) & df["Emission_Rate"].notna()].copy()
    df = df.drop_duplicates(subset=["ID"], keep="first")
    return df

# Coord pairs
def _coord_pairs(row):
    try:
        n = int(float(row.get("Num_Coords", 1)))
    except Exception:
        n = 1
    coords = []
    for i in range(1, n + 1):
        try:
            x=float(row.get(f"X{i}"));y=float(row.get(f"Y{i}"))
        except (TypeError,ValueError):
            continue
        if math.isfinite(x) and math.isfinite(y):coords.append((x,y))
    return coords

# Source geometry
def source_geometry(row):
    typ = row["Type"]
    coords = _coord_pairs(row)
    if not coords:
        return None

    if typ in {"POINT", "VOLUME"}:
        return Point(coords[0])

    if typ == "AREA_CIRC":
        radius = pd.to_numeric(pd.Series([row.get("Radius")]), errors="coerce").iloc[0]
        diam = pd.to_numeric(pd.Series([row.get("Diam")]), errors="coerce").iloc[0]
        if pd.notna(radius) and radius > 0:
            r = float(radius)
        elif pd.notna(diam) and diam > 0:

            r = float(diam) / 2.0
        else:
            return Point(coords[0])
        return Point(coords[0]).buffer(r, resolution=32)

    if typ == "AREA":
        lx = pd.to_numeric(pd.Series([row.get("Length_X")]), errors="coerce").iloc[0]
        ly = pd.to_numeric(pd.Series([row.get("Length_Y")]), errors="coerce").iloc[0]
        ang = pd.to_numeric(pd.Series([row.get("Rotation_Angle")]), errors="coerce").iloc[0]
        if pd.isna(lx) or pd.isna(ly):
            return Point(coords[0])
        x, y = coords[0]
        geom = box(x, y, x + float(lx), y + float(ly))
        if pd.notna(ang) and float(ang) != 0:
            geom = affinity.rotate(geom, float(ang), origin=(x, y), use_radians=False)
        return geom

    if typ == "AREA_POLY" and len(coords) >= 3:
        try:
            return make_valid(Polygon(coords))
        except Exception:
            return LineString(coords)

    if typ in {"LINE_AREA", "LINE", "RLINE", "RLINEXT"} and len(coords) >= 2:
        line = LineString(coords)
        width = np.nan
        for key in ("Width", "Width_m", "Source_Width", "Road_Width", "Length_X"):
            v = pd.to_numeric(pd.Series([row.get(key)]), errors="coerce").iloc[0]
            if pd.notna(v) and float(v) > 0:
                width = float(v); break

        if pd.notna(width) and typ != "RLINEXT":
            return make_valid(line.buffer(width / 2.0, cap_style=2, join_style=2))
        if len(coords) >= 3 and typ != "RLINEXT":
            try:
                return make_valid(Polygon(coords))
            except Exception:
                pass
        return line

    if typ == "LINE_VOLUME" and len(coords) >= 2:
        return LineString(coords)

    if len(coords) >= 3:
        try:
            return make_valid(Polygon(coords))
        except Exception:
            pass
    if len(coords) >= 2:
        return LineString(coords)
    return Point(coords[0])

# Row width m
def _row_width_m(row):
    for key in ("Width", "Width_m", "Source_Width", "Road_Width", "Length_X"):
        v = pd.to_numeric(pd.Series([row.get(key)]), errors="coerce").iloc[0]
        if pd.notna(v) and float(v) > 0:
            return float(v)
    return np.nan

# Source measure
def _source_measure(row, geom):
    """Retorna área [m²] e comprimento [m] coerentes com o tipo da fonte."""
    if geom is None or geom.is_empty:
        return np.nan, np.nan
    area = float(geom.area) if geom.geom_type in {"Polygon", "MultiPolygon"} else np.nan
    length = float(geom.length) if geom.geom_type in {"LineString", "MultiLineString"} else np.nan
    typ = str(row.get("Type", "")).upper()
    if typ in AREA_RATE_TYPES and not np.isfinite(area):
        width = _row_width_m(row)
        if np.isfinite(length) and np.isfinite(width):
            area = length * width
    return area, length

# Total emission gs
def total_emission_gs(row, geom):
    """Converte a taxa nativa do AERMOD para emissão total em g/s sem misturar unidades.

    AREA/AREACIRC/AREAPOLY/OPEN_PIT/LINE/LINE_AREA/RLINE: g/s/m² × área efetiva.
    POINT/VOLUME/LINE_VOLUME: taxa já é total em g/s.
    RLINEXT: g/s/m × comprimento, quando usado no formato nativo do AERMOD.
    """
    rate = float(row["Emission_Rate"])
    typ = str(row["Type"]).upper()
    area_m2, length_m = _source_measure(row, geom)
    if typ in AREA_RATE_TYPES:
        if np.isfinite(area_m2) and area_m2 > 0:
            return rate * area_m2, "g/s/m2 × área da fonte", "g/s/m2", area_m2, length_m
        return np.nan, "área geométrica ausente - total não calculado", "g/s/m2", area_m2, length_m
    if typ in TOTAL_RATE_TYPES:
        return rate, "g/s total", "g/s", area_m2, length_m
    if typ in LENGTH_RATE_TYPES:
        if np.isfinite(length_m) and length_m > 0:
            return rate * length_m, "g/s/m × comprimento", "g/s/m", area_m2, length_m
        return np.nan, "comprimento ausente - total não calculado", "g/s/m", area_m2, length_m
    return rate, "taxa nativa - revisar", "desconhecida", area_m2, length_m

# Build source gdf
def build_source_gdf(path: Path, pollutant: str):
    df = read_lakes_sources(path)
    geom_lookup = load_source_geometries_from_files(config.DIRS["emission"])
    records = []
    for _, row in df.iterrows():
        sid = str(row.get("ID"))
        key = normalize_name(sid)
        geom = geom_lookup.get(key)
        if geom is None:
            geom = source_geometry(row)
        if geom is None or geom.is_empty:
            continue
        geom = _clean_geometry(geom)
        typ = str(row["Type"]).upper()

        if typ in AREA_RATE_TYPES and geom.geom_type in {"LineString", "MultiLineString"}:
            width = _row_width_m(row)
            if np.isfinite(width) and width > 0:
                geom = _clean_geometry(geom.buffer(width / 2.0, cap_style=2, join_style=2))
        total, assumption, native_unit, area_m2, length_m = total_emission_gs(row, geom)
        rate = float(row["Emission_Rate"])
        surface_rate = rate if typ in AREA_RATE_TYPES else np.nan
        line_rate = rate if typ in LENGTH_RATE_TYPES else np.nan
        if typ == "LINE_VOLUME" and np.isfinite(length_m) and length_m > 0:
            line_rate_equiv = float(total) / length_m if np.isfinite(total) else np.nan
        else:
            line_rate_equiv = line_rate
        records.append({
            "pollutant": pollutant,
            "source_id": sid,
            "desc": str(row.get("Desc")) if pd.notna(row.get("Desc")) else "",
            "source_type": typ,
            "emission_rate_native": rate,
            "native_unit": native_unit,
            "source_area_m2": area_m2,
            "source_length_m": length_m,
            "surface_rate_gs_m2": surface_rate,
            "line_rate_gs_m": line_rate_equiv,
            "emission_total_gs": float(total) if np.isfinite(total) else np.nan,
            "unit_assumption": assumption,
            "geometry_source": "kml/kmz" if key in geom_lookup else "planilha",
            "group_id": infer_primary_group_from_source(row.get("ID"), row.get("Desc")),
            "urban_subgroup": urban_subgroup_from_source(row.get("ID")),
            "AEX": bool(is_exposed_area(row.get("ID"))),
            "geometry": geom,
        })
    return gpd.GeoDataFrame(records, geometry="geometry", crs=config.CRS_PROJECT)

# Enterprise name col
def _enterprise_name_col(emp):
    candidates = ["nome", "name", "empresa", "empreendimento", "razao", "razão", "descricao", "descrição"]
    lower = {str(c).lower(): c for c in emp.columns}
    for c in candidates:
        if c in lower:
            return lower[c]
    return None

# Associate enterprises
def associate_enterprises(sources, enterprises, nearest_tolerance_m=250.0):
    out = sources.copy()
    out["enterprise"] = None
    if enterprises is None or enterprises.empty:
        return out
    emp = enterprises.to_crs(out.crs).copy()
    emp["geometry"] = emp.geometry.map(_clean_geometry)
    name_col = _enterprise_name_col(emp)
    if name_col is None:
        emp["_empname"] = [f"EMP_{i}" for i in emp.index]
    else:
        emp["_empname"] = emp[name_col].astype(str)

    for idx, src in out.iterrows():
        geom = src.geometry
        geom = _clean_geometry(geom)
        cand = emp[emp.intersects(geom)]
        chosen = None
        if not cand.empty:
            if geom.geom_type in {"Polygon", "MultiPolygon"}:
                scores = cand.geometry.intersection(geom).area
                chosen = cand.loc[scores.idxmax(), "_empname"]
            elif geom.geom_type in {"LineString", "MultiLineString"}:
                scores = cand.geometry.intersection(geom).length
                chosen = cand.loc[scores.idxmax(), "_empname"]
            else:
                chosen = cand.iloc[0]["_empname"]
        else:
            d = emp.geometry.distance(geom)
            if len(d) and float(d.min()) <= nearest_tolerance_m:
                chosen = emp.loc[d.idxmin(), "_empname"]
        out.at[idx, "enterprise"] = chosen

        subgroup = out.at[idx, "urban_subgroup"]
        has_urban_subgroup = pd.notna(subgroup) and str(subgroup).strip() != ""
        if has_urban_subgroup:
            out.at[idx, "group_id"] = "URB"
        elif chosen:
            g = canonical_group(chosen)
            if g and g not in {"AEX", "URB-FER", "URB-NUC", "URB-VIA"}:
                out.at[idx, "group_id"] = g
    return out

# Allocate emissions to zones
def allocate_emissions_to_zones(sources, zones):
    """Aloca emissões às zonas preservando massa e as unidades nativas da fonte.

    Diferentemente da normalização pela soma das interseções, fontes parcialmente fora do
    zoneamento não têm sua emissão externa redistribuída artificialmente para as zonas internas.
    """
    z = zones.copy()
    z["EMIS_TOTAL_GS"] = 0.0
    z["AREA_KM2"] = z.geometry.area / 1e6

    allocations = []
    point_radius = float(getattr(config, "EMISSION_POINT_SUPPORT_RADIUS_M", 250.0))
    line_half_width = float(getattr(config, "EMISSION_LINE_SUPPORT_HALF_WIDTH_M", 50.0))
    for _, src in sources.iterrows():
        geom = src.geometry
        if geom is None or geom.is_empty:
            continue
        typ = str(src.get("source_type", "")).upper()
        total = pd.to_numeric(pd.Series([src.get("emission_total_gs")]), errors="coerce").iloc[0]
        rate_area = pd.to_numeric(pd.Series([src.get("surface_rate_gs_m2")]), errors="coerce").iloc[0]
        rate_line = pd.to_numeric(pd.Series([src.get("line_rate_gs_m")]), errors="coerce").iloc[0]
        area_total = pd.to_numeric(pd.Series([src.get("source_area_m2")]), errors="coerce").iloc[0]
        length_total = pd.to_numeric(pd.Series([src.get("source_length_m")]), errors="coerce").iloc[0]

        cand = z[z.intersects(geom)].copy()
        if cand.empty:
            continue

        if geom.geom_type in {"Point", "MultiPoint"}:

            n = len(cand)
            for zid in cand.index:
                value = float(total) / n if np.isfinite(total) and n else 0.0
                z.at[zid, "EMIS_TOTAL_GS"] += value
                allocations.append({
                    "zone_index": zid, "source_id": src["source_id"], "source_type": typ,
                    "group_id": src.get("group_id"), "enterprise": src.get("enterprise"),
                    "emission_gs": value, "source_total_gs": total, "allocated_fraction": 1.0 / n if n else np.nan,
                    "intersection_measure": np.nan, "source_measure": np.nan, "allocation_basis": "emissão total g/s",
                    "source_intensity_gs_km2": value / (np.pi * point_radius**2 / 1e6) if point_radius > 0 else np.nan,
                })
            continue

        if geom.geom_type in {"Polygon", "MultiPolygon"}:
            inter = cand.geometry.intersection(geom).area
            for zid, inter_area in inter.items():
                if inter_area <= 0:
                    continue
                if np.isfinite(rate_area):
                    value = float(rate_area) * float(inter_area)
                    frac = float(inter_area) / float(area_total) if np.isfinite(area_total) and area_total > 0 else np.nan
                    basis = "g/s/m2 × área de interseção"
                elif np.isfinite(total) and np.isfinite(area_total) and area_total > 0:
                    frac = float(inter_area) / float(area_total)
                    value = float(total) * frac
                    basis = "g/s total × fração de área"
                else:
                    continue
                z.at[zid, "EMIS_TOTAL_GS"] += value
                allocations.append({
                    "zone_index": zid, "source_id": src["source_id"], "source_type": typ,
                    "group_id": src.get("group_id"), "enterprise": src.get("enterprise"),
                    "emission_gs": value, "source_total_gs": total, "allocated_fraction": frac,
                    "intersection_measure": float(inter_area), "source_measure": area_total, "allocation_basis": basis,
                    "source_intensity_gs_km2": value / (float(inter_area) / 1e6) if inter_area > 0 else np.nan,
                })
            continue

        if geom.geom_type in {"LineString", "MultiLineString"}:
            inter = cand.geometry.intersection(geom).length
            for zid, inter_len in inter.items():
                if inter_len <= 0:
                    continue
                if typ == "RLINEXT" and np.isfinite(src.get("emission_rate_native", np.nan)):
                    value = float(src["emission_rate_native"]) * float(inter_len)
                    frac = float(inter_len) / float(length_total) if np.isfinite(length_total) and length_total > 0 else np.nan
                    basis = "g/s/m × comprimento de interseção"
                elif typ == "LINE_VOLUME" and np.isfinite(total) and np.isfinite(length_total) and length_total > 0:
                    frac = float(inter_len) / float(length_total)
                    value = float(total) * frac
                    basis = "g/s total × fração de comprimento"
                elif np.isfinite(rate_line):
                    value = float(rate_line) * float(inter_len)
                    frac = float(inter_len) / float(length_total) if np.isfinite(length_total) and length_total > 0 else np.nan
                    basis = "g/s/m × comprimento de interseção"
                else:
                    continue
                z.at[zid, "EMIS_TOTAL_GS"] += value
                allocations.append({
                    "zone_index": zid, "source_id": src["source_id"], "source_type": typ,
                    "group_id": src.get("group_id"), "enterprise": src.get("enterprise"),
                    "emission_gs": value, "source_total_gs": total, "allocated_fraction": frac,
                    "intersection_measure": float(inter_len), "source_measure": length_total, "allocation_basis": basis,
                    "source_intensity_gs_km2": value / (float(inter_len) * 2 * line_half_width / 1e6) if inter_len > 0 and line_half_width > 0 else np.nan,
                })

    z["EMIS_DENS_GS_KM2"] = z["EMIS_TOTAL_GS"] / z["AREA_KM2"].replace(0, np.nan)
    dens = pd.to_numeric(z["EMIS_DENS_GS_KM2"], errors="coerce")
    pos = dens[dens > 0]
    q33 = float(pos.quantile(1/3)) if not pos.empty else np.nan
    q67 = float(pos.quantile(2/3)) if not pos.empty else np.nan
    def _dens_class(v):
        if pd.isna(v) or v <= 0:
            return "sem_emissao"
        if pd.notna(q33) and v <= q33:
            return "baixa"
        if pd.notna(q67) and v <= q67:
            return "moderada"
        return "alta"
    z["EMIS_DENS_CLASS"] = dens.map(_dens_class)
    z["EMIS_DENS_Q33"] = q33
    z["EMIS_DENS_Q67"] = q67

    a = pd.DataFrame(allocations)
    if not a.empty:
        focal = a.groupby("zone_index")["source_intensity_gs_km2"].quantile(0.95)
        z["EMIS_HOTSPOT_P95"] = focal.reindex(z.index).fillna(0.0)

        local = a[pd.to_numeric(a["emission_gs"], errors="coerce") > 0].groupby(
            ["zone_index", "group_id"], dropna=False
        )["emission_gs"].sum().reset_index()
        local["rank"] = local.groupby("zone_index")["emission_gs"].rank(method="first", ascending=False)
        dominant = local[local["rank"] == 1].set_index("zone_index")
        z["GRUPO_EMISSOR_LOCAL_ID"] = dominant["group_id"].reindex(z.index)
        z["GRUPO_EMISSOR_LOCAL"] = z["GRUPO_EMISSOR_LOCAL_ID"].map(
            lambda g: GROUPS.get(g, {}).get("name", g) if pd.notna(g) else None
        )

        src_totals = sources.assign(
            group_id=sources["group_id"].fillna("NAO_IDENTIFICADO")
        ).groupby("group_id")["emission_total_gs"].sum()
        alloc_totals = a.assign(
            group_id=a["group_id"].fillna("NAO_IDENTIFICADO")
        ).groupby("group_id")["emission_gs"].sum()
        group_outside = (src_totals - alloc_totals.reindex(src_totals.index).fillna(0.0)).clip(lower=0.0)
        z["EMIS_DENTRO_MUN_GS"] = z["EMIS_TOTAL_GS"]
        z["EMIS_FORA_MUN_GS"] = z["GRUPO_EMISSOR_LOCAL_ID"].map(group_outside).fillna(0.0)
        group_total = z["GRUPO_EMISSOR_LOCAL_ID"].map(src_totals)
        z["CONTR_EXTERNA_PCT"] = 100 * z["EMIS_FORA_MUN_GS"] / group_total.replace(0, np.nan)
    else:
        z["EMIS_HOTSPOT_P95"] = 0.0
        z["GRUPO_EMISSOR_LOCAL_ID"] = None
        z["GRUPO_EMISSOR_LOCAL"] = None
        z["EMIS_DENTRO_MUN_GS"] = z["EMIS_TOTAL_GS"]
        z["EMIS_FORA_MUN_GS"] = 0.0
        z["CONTR_EXTERNA_PCT"] = np.nan

    q = float(getattr(config, "EMISSION_PRESSURE_QUANTILE", 0.75))
    total_pos = pd.to_numeric(z["EMIS_TOTAL_GS"], errors="coerce")
    total_pos = total_pos[total_pos > 0]
    focal_pos = pd.to_numeric(z["EMIS_HOTSPOT_P95"], errors="coerce")
    focal_pos = focal_pos[focal_pos > 0]
    thr_total = float(total_pos.quantile(q)) if not total_pos.empty else np.nan
    thr_focal = float(focal_pos.quantile(q)) if not focal_pos.empty else np.nan
    z["EMIS_THR_TOTAL_GS"] = thr_total
    focal_tolerance = float(getattr(config, "EMISSION_FOCAL_THRESHOLD_RELATIVE_TOLERANCE", 0.01))
    effective_thr_focal = thr_focal * (1.0 + focal_tolerance) if pd.notna(thr_focal) else np.nan
    z["EMIS_THR_HOTSPOT_P95"] = effective_thr_focal

    z["EMIS_ALTA_TOTAL"] = pd.to_numeric(z["EMIS_TOTAL_GS"], errors="coerce").gt(thr_total) if pd.notna(thr_total) else False
    z["EMIS_ALTA_FOCAL"] = pd.to_numeric(z["EMIS_HOTSPOT_P95"], errors="coerce").gt(effective_thr_focal) if pd.notna(effective_thr_focal) else False

    if not a.empty:
        aa = a.copy()
        aa["emission_gs"] = pd.to_numeric(aa["emission_gs"], errors="coerce").fillna(0.0)
        aa["_urban_road"] = aa["group_id"].eq("URB")
        split = aa.groupby(["zone_index", "_urban_road"])["emission_gs"].sum().unstack(fill_value=0.0)
        z["EMIS_URBANA_GS"] = split.get(True, pd.Series(dtype=float)).reindex(z.index).fillna(0.0)
        z["EMIS_INDUSTRIAL_GS"] = split.get(False, pd.Series(dtype=float)).reindex(z.index).fillna(0.0)
    else:
        z["EMIS_URBANA_GS"] = 0.0
        z["EMIS_INDUSTRIAL_GS"] = 0.0

    q_ind = float(getattr(config, "EMISSION_INDUSTRIAL_HIGH_QUANTILE", 0.67))
    q_urb = float(getattr(config, "EMISSION_URBAN_HIGH_QUANTILE", 0.90))
    ind_pos = pd.to_numeric(z["EMIS_INDUSTRIAL_GS"], errors="coerce")
    ind_pos = ind_pos[ind_pos > 0]
    urban_zone = z.get("macrozona", pd.Series("", index=z.index)).astype(str).str.contains("Urbana", case=False, na=False)
    urb_pos = pd.to_numeric(z.loc[urban_zone, "EMIS_URBANA_GS"], errors="coerce")
    urb_pos = urb_pos[urb_pos > 0]
    thr_ind = float(ind_pos.quantile(q_ind)) if not ind_pos.empty else np.nan
    thr_urb = float(urb_pos.quantile(q_urb)) if not urb_pos.empty else np.nan
    z["EMIS_THR_INDUSTRIAL_GS"] = thr_ind
    z["EMIS_THR_URBANA_GS"] = thr_urb
    z["EMIS_ALTA_INDUSTRIAL"] = pd.to_numeric(z["EMIS_INDUSTRIAL_GS"], errors="coerce").gt(thr_ind) if pd.notna(thr_ind) else False
    z["EMIS_ALTA_URBANA"] = urban_zone & (pd.to_numeric(z["EMIS_URBANA_GS"], errors="coerce").gt(thr_urb) if pd.notna(thr_urb) else False)
    z["EMIS_PRESSAO_ALTA"] = z["EMIS_ALTA_INDUSTRIAL"] | z["EMIS_ALTA_URBANA"]
    z["EMIS_PRESSAO_TIPO"] = np.select(
        [z["EMIS_ALTA_INDUSTRIAL"] & z["EMIS_ALTA_URBANA"], z["EMIS_ALTA_INDUSTRIAL"], z["EMIS_ALTA_URBANA"]],
        ["industrial_e_urbana", "industrial_mineral", "ressuspensao_viaria_urbana"],
        default="baixa_em_ambas",
    )
    z["EMIS_CRITERIO"] = z["EMIS_PRESSAO_TIPO"]
    ind_rank = pd.to_numeric(z["EMIS_INDUSTRIAL_GS"], errors="coerce").rank(pct=True).fillna(0.0)
    urb_rank = pd.to_numeric(z["EMIS_URBANA_GS"], errors="coerce").where(urban_zone, 0.0).rank(pct=True).fillna(0.0)
    z["EMIS_PRESSAO_SCORE"] = pd.concat([ind_rank, urb_rank], axis=1).max(axis=1)
    return z, a

# Emission mass balance audit
def emission_mass_balance_audit(sources, allocations):
    """Auditoria de conservação de massa entre fontes e zoneamento."""
    s = sources[[c for c in ["source_id","source_type","group_id","enterprise","native_unit","emission_rate_native","source_area_m2","source_length_m","emission_total_gs","geometry_source"] if c in sources.columns]].copy()
    if allocations is None or allocations.empty:
        s["allocated_gs"] = 0.0
    else:
        a = allocations.groupby("source_id", as_index=False)["emission_gs"].sum().rename(columns={"emission_gs":"allocated_gs"})
        s = s.merge(a, on="source_id", how="left")
        s["allocated_gs"] = s["allocated_gs"].fillna(0.0)
    s["unallocated_gs"] = pd.to_numeric(s["emission_total_gs"], errors="coerce") - pd.to_numeric(s["allocated_gs"], errors="coerce")
    s["allocated_pct"] = 100 * pd.to_numeric(s["allocated_gs"], errors="coerce") / pd.to_numeric(s["emission_total_gs"], errors="coerce").replace(0, np.nan)
    return s

# Group count audit
def group_count_audit(sources):
    rows = []
    for group, meta in GROUPS.items():
        if group == "AEX":
            detected = int(sources["AEX"].fillna(False).sum()) if "AEX" in sources else 0
        elif group in {"URB-FER", "URB-NUC", "URB-VIA"}:
            detected = int((sources.get("urban_subgroup") == group).sum())
        else:
            detected = int((sources.get("group_id") == group).sum())
        expected = int(meta["expected"])
        rows.append({
            "group_id": group,
            "name": meta["name"],
            "kind": meta.get("kind"),
            "expected": expected,
            "detected": detected,
            "difference": detected - expected,
        })
    return pd.DataFrame(rows)
