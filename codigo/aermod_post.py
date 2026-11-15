# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entrada: {path} | path.open.
# Entrada: {meta_path} | meta_path.read_text.
# Campos/chaves em ch: AVE, CONC, DATECODE, GRP, X, Y, _kind, date, hour, year.
# Campos/chaves em agg: COMPLETENESS, N_DAYS.
# Campos/chaves em sub: CONC, DATECODE, VALID_YEAR, X, Y, year.
# Campos/chaves em sub.loc: year.
# Campos/chaves em valid: ANNUAL_MEAN, P98, year.
# Campos/chaves em row: ANNUAL_MODEL, P98_MODEL, n_model_years, years_model.
# Campos/chaves em out: ANNUAL_MODEL, P98_MODEL, X, Y, n_model_years.
# Campos/chaves em info: ave.
# Campos/chaves em h: CONC, GRP, N_HOURS, SUM_CONC, X, Y, date.
# Campos/chaves em daily: date.
# Campos/chaves em paths: daily, meta.
# Saída: paths['meta'].tmp | tmp_meta.write_text.
# Campos/chaves gerados em info: ave, cache_file, cache_load_seconds, cache_used, daily_source, detected_averaging, group, n_receptors, raw_processing_seconds.
# Campos/chaves gerados em ch: CONC, DATECODE, _kind, date, hour, year.
# Campos/chaves gerados em agg: COMPLETENESS, EXPECTED_DAYS, VALID_YEAR, year.
# Campos/chaves gerados em row: ANNUAL_3YR, ANNUAL_MODEL, P98_3YR, P98_MODEL, n_design_years, years_valid.
# Campos/chaves gerados em a: N_HOURS.
# Campos/chaves gerados em h: CONC.
# Campos/chaves gerados em daily: SOURCE_AVERAGING, year.
# X: coordenada leste em metros.
# Y: coordenada norte em metros.
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
import re
import warnings
import json
import hashlib
import time
import os

import numpy as np
import pandas as pd
import geopandas as gpd

import config
from standards import STANDARDS, nearest_rank_percentile

DATA_RE = re.compile(r"^\s*[-+]?\d")

# Unique paths
def _unique_paths(paths):
    """Remove duplicações de caminhos, inclusive em sistemas case-insensitive."""
    seen = set()
    out = []
    for p in paths:
        pp = Path(p)
        try:
            key = str(pp.resolve()).casefold()
        except Exception:
            key = str(pp.absolute()).casefold()
        if key in seen:
            continue
        seen.add(key)
        out.append(pp)
    return out

# Inspect pos header
def inspect_pos_header(path: Path):
    info = {"file": str(path), "ave": None, "group": None, "n_receptors": None}
    with path.open("r", encoding="latin1", errors="replace") as f:
        for _ in range(30):
            line = f.readline()
            if not line:
                break
            up = line.upper()
            m = re.search(r"CONCURRENT\s+(.+?)\s+VALUES\s+FOR SOURCE GROUP:\s*(\S+)", up)
            if m:
                info["ave"] = m.group(1).strip()
                info["group"] = m.group(2).strip()
            m = re.search(r"TOTAL OF\s+(\d+)\s+RECEPTORS", up)
            if m:
                info["n_receptors"] = int(m.group(1))
    return info

# Fmt elapsed
def _fmt_elapsed(seconds):
    seconds = max(0, int(seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"

# Fmt size
def _fmt_size(num_bytes):
    n = float(num_bytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024.0 or unit == "TB":
            return f"{n:.1f} {unit}"
        n /= 1024.0

# Iter pos chunks
def iter_pos_chunks(path: Path, chunk_rows=350_000, progress=False, progress_label=None):
    """Itera pelas linhas de dados do POST em blocos.

    Quando ``progress=True``, imprime progresso aproximado por tamanho lido,
    número de registros válidos e tempo decorrido. O objetivo é deixar claro
    que arquivos .POS gigantes continuam sendo processados.
    """
    path = Path(path)
    rows = []
    data_rows = 0
    raw_lines = 0
    bytes_seen = 0
    file_size = path.stat().st_size if path.exists() else 0
    t0 = time.perf_counter()
    last_report = t0
    min_seconds = float(getattr(config, "POS_PROGRESS_MIN_SECONDS", 8.0))
    label = progress_label or path.name

    with path.open("r", encoding="latin1", errors="replace", newline="") as f:
        for line in f:
            raw_lines += 1

            bytes_seen += len(line)
            if not DATA_RE.match(line):
                continue
            p = line.split()

            if len(p) < 9:
                continue
            try:
                rows.append((
                    float(p[0]), float(p[1]), float(p[2]),
                    p[6], p[7], str(p[8]).zfill(8)
                ))
                data_rows += 1
            except Exception:
                continue
            if len(rows) >= chunk_rows:
                now = time.perf_counter()
                if progress and (now - last_report >= min_seconds):
                    pct = min(100.0, 100.0 * bytes_seen / file_size) if file_size else 0.0
                    print(
                        f"      [PROGRESSO] {label}: {pct:5.1f}% | "
                        f"{data_rows:,} registros | {_fmt_size(bytes_seen)} de {_fmt_size(file_size)} | "
                        f"tempo {_fmt_elapsed(now-t0)}",
                        flush=True,
                    )
                    last_report = now
                yield pd.DataFrame(rows, columns=["X", "Y", "CONC", "AVE", "GRP", "DATECODE"])
                rows = []
    if rows:
        yield pd.DataFrame(rows, columns=["X", "Y", "CONC", "AVE", "GRP", "DATECODE"])
    if progress:
        elapsed = time.perf_counter() - t0
        print(
            f"      [PROGRESSO] {label}: 100.0% | {data_rows:,} registros válidos lidos | "
            f"{_fmt_size(file_size)} | tempo {_fmt_elapsed(elapsed)}",
            flush=True,
        )

# Parse datecode
def parse_datecode(series: pd.Series):
    s = series.astype(str).str.replace(r"\.0$", "", regex=True).str.zfill(8)
    yy = pd.to_numeric(s.str.slice(0, 2), errors="coerce")
    mm = pd.to_numeric(s.str.slice(2, 4), errors="coerce")
    dd = pd.to_numeric(s.str.slice(4, 6), errors="coerce")
    hh = pd.to_numeric(s.str.slice(6, 8), errors="coerce")
    year = 2000 + yy

    dt = pd.to_datetime(dict(year=year, month=mm, day=dd), errors="coerce")
    return dt, hh

# Read post 24h
def read_post_24h(path: Path, background=0.0):
    info = inspect_pos_header(path)
    chunks = []
    for ch in iter_pos_chunks(path):

        mask = ch["AVE"].str.upper().isin({"24-HR", "24HR", "24"})
        ch = ch[mask].copy()
        if ch.empty:
            continue
        dt, hh = parse_datecode(ch["DATECODE"])
        ch["date"] = dt
        ch["year"] = dt.dt.year
        ch["hour"] = hh
        ch["CONC"] = ch["CONC"] + float(background)
        chunks.append(ch[["X", "Y", "CONC", "date", "year", "GRP"]])
    if not chunks:
        raise ValueError(f"Nenhum registro 24-HR encontrado em {path}")
    df = pd.concat(chunks, ignore_index=True)
    return df, info

# Summarize post 24h
def summarize_post_24h(path: Path, pollutant: str, background=0.0):
    """Resume um POSTFILE de 24 h por receptor.

    O monitoramento pode continuar usando 3 anos, mas a modelagem AERMOD
    aceita provisoriamente o número de anos definido em
    ``config.MODEL_N_YEARS_DESIGN``. Nesta versão o padrão é 1 ano, pois o
    POST disponível contém somente 2023. Quando os três anos estiverem
    disponíveis, basta alterar MODEL_N_YEARS_DESIGN para 3 no config.py.
    """
    info = inspect_pos_header(path)
    yearly_parts = []
    current_year = None
    current_parts = []

    def finalize_year(year, parts):
        if year is None or not parts:
            return None
        d = pd.concat(parts, ignore_index=True)
        d = d.drop_duplicates(subset=["X", "Y", "DATECODE"], keep="last")
        agg = d.groupby(["X", "Y"], observed=True).agg(
            ANNUAL_MEAN=("CONC", "mean"),
            N_DAYS=("CONC", "count"),
            P98=("CONC", lambda x: nearest_rank_percentile(x, config.SHORT_TERM_PERCENTILE)),
        ).reset_index()
        agg["year"] = int(year)
        expected = 366 if pd.Timestamp(int(year), 12, 31).is_leap_year else 365
        agg["EXPECTED_DAYS"] = expected
        agg["COMPLETENESS"] = agg["N_DAYS"] / expected
        agg["VALID_YEAR"] = agg["COMPLETENESS"] >= config.MIN_QUARTER_COMPLETENESS
        return agg

    for ch in iter_pos_chunks(path):
        mask = ch["AVE"].str.upper().isin({"24-HR", "24HR", "24"})
        ch = ch[mask].copy()
        if ch.empty:
            continue
        code = ch["DATECODE"].astype(str).str.replace(r"\.0$", "", regex=True).str.zfill(8)
        ch["year"] = 2000 + pd.to_numeric(code.str.slice(0, 2), errors="coerce")
        ch["CONC"] = ch["CONC"] + float(background)
        ch["DATECODE"] = code
        ch = ch.dropna(subset=["year", "X", "Y", "CONC"])
        for year, sub in ch.groupby("year", sort=True):
            year = int(year)
            if current_year is None:
                current_year = year
            if year != current_year:
                done = finalize_year(current_year, current_parts)
                if done is not None:
                    yearly_parts.append(done)
                current_parts = []
                current_year = year
            current_parts.append(sub[["X", "Y", "CONC", "DATECODE"]].copy())

    done = finalize_year(current_year, current_parts)
    if done is not None:
        yearly_parts.append(done)
    if not yearly_parts:
        raise ValueError(f"Nenhum registro 24-HR encontrado em {path}")

    yearly = pd.concat(yearly_parts, ignore_index=True)
    n_required = int(config.MODEL_N_YEARS_DESIGN)

    summaries = []
    for (x, y), sub in yearly.groupby(["X", "Y"], sort=False):
        valid_years = sorted(sub.loc[sub["VALID_YEAR"], "year"].astype(int).tolist())
        valid = pd.DataFrame(columns=sub.columns)
        for end_year in sorted(valid_years, reverse=True):
            wanted = list(range(end_year - n_required + 1, end_year + 1))
            if all(yv in valid_years for yv in wanted):
                valid = sub[sub["year"].isin(wanted)].sort_values("year")
                break

        row = {
            "X": x,
            "Y": y,
            "n_model_years": int(len(valid)),
            "years_model": ",".join(map(str, valid["year"].astype(int).tolist())) if len(valid) else "",
        }
        if len(valid) == n_required:
            row["P98_MODEL"] = valid["P98"].mean()
            row["ANNUAL_MODEL"] = valid["ANNUAL_MEAN"].mean()
        else:
            row["P98_MODEL"] = np.nan
            row["ANNUAL_MODEL"] = np.nan

        row["n_design_years"] = row["n_model_years"]
        row["years_valid"] = row["years_model"]
        row["P98_3YR"] = row["P98_MODEL"]
        row["ANNUAL_3YR"] = row["ANNUAL_MODEL"]
        summaries.append(row)

    out = pd.DataFrame(summaries)
    for scenario in ("PV", "PF"):
        lim24 = STANDARDS[pollutant][scenario]["24H"]
        limann = STANDARDS[pollutant][scenario]["ANNUAL"]
        out[f"ratio24_{scenario}"] = out["P98_MODEL"] / lim24
        out[f"ratioann_{scenario}"] = out["ANNUAL_MODEL"] / limann
        out[f"status_{scenario}"] = np.select(
            [
                out["n_model_years"] < n_required,
                (out["P98_MODEL"] <= lim24) & (out["ANNUAL_MODEL"] <= limann),
            ],
            ["insuficiente", "atendimento"],
            default="nao_atendimento",
        )

    gdf = gpd.GeoDataFrame(
        out,
        geometry=gpd.points_from_xy(out["X"], out["Y"]),
        crs=config.CRS_PROJECT,
    )
    return gdf, yearly, info

# Infer pollutant
def _infer_pollutant(path: Path):
    t = re.sub(r"[^A-Z0-9]+", "", str(path).upper())
    if "PM10" in t or "MP10" in t:
        return "PM10"
    if any(x in t for x in ["PM25", "PM2_5", "PM2-5", "MP25", "MP2-5"]):
        return "PM25"

    if "PM25" in t or "MP25" in t:
        return "PM25"
    return None

# Discover post 24h
def discover_post_24h(post_dir: Path, pollutant: str):
    override = config.POST_OVERRIDE[pollutant].get("24H")
    if override:
        p = Path(override)
        if p.exists():
            return p

    candidates = []
    for p in post_dir.rglob("*.POS"):
        pol = _infer_pollutant(p)
        info = inspect_pos_header(p)
        if pol == pollutant and info.get("ave") and "24" in str(info["ave"]):
            candidates.append(p)
    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:

        allc = [p for p in candidates if "GALL" in p.name.upper() or "ALL" in p.name.upper()]
        return sorted(allc or candidates)[0]
    return None

# Discover group posts
def discover_group_posts(post_dir: Path, pollutant: str):
    files = []
    for p in post_dir.rglob("*.POS"):
        if _infer_pollutant(p) not in {None, pollutant}:
            continue
        info = inspect_pos_header(p)
        if info.get("ave") and "24" in str(info["ave"]):
            files.append((p, info))
    return files

# Discover post hourly
def discover_post_hourly(post_dir: Path, pollutant: str):
    """Localiza preferencialmente um POSTFILE 1-HR do grupo ALL/GALL."""
    candidates = []
    for p in post_dir.rglob("*.POS"):
        pol = _infer_pollutant(p)
        if pol != pollutant:
            continue
        info = inspect_pos_header(p)
        if _ave_kind(info.get("ave")) == "1H":
            candidates.append(p)
    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        allc = [p for p in candidates if "GALL" in p.name.upper() or "ALL" in p.name.upper()]
        return sorted(allc or candidates)[0]
    return None

# Read post hourly for day
def read_post_hourly_for_day(path: Path, target_date, background=0.0, chunk_rows=350_000, progress=False):
    """Extrai a série horária de um único dia a partir de POST 1-HR."""
    target = pd.Timestamp(target_date).normalize()
    parts = []
    for ch in iter_pos_chunks(path, chunk_rows=chunk_rows, progress=progress, progress_label=path.name):
        if ch.empty:
            continue
        ch["_kind"] = ch["AVE"].map(_ave_kind)
        ch = ch[ch["_kind"] == "1H"].copy()
        if ch.empty:
            continue
        dt, hh = parse_datecode(ch["DATECODE"])
        ch["date"] = dt
        ch["hour"] = pd.to_numeric(hh, errors="coerce")
        ch["CONC"] = pd.to_numeric(ch["CONC"], errors="coerce") + float(background)
        ch = ch.dropna(subset=["X", "Y", "CONC", "date", "hour"])
        ch = ch[ch["date"] == target]
        if ch.empty:
            continue
        ch = ch[["X", "Y", "CONC", "date", "hour", "GRP"]].copy()
        parts.append(ch)
    if not parts:
        return pd.DataFrame(columns=["X","Y","CONC","date","hour","GRP"])
    out = pd.concat(parts, ignore_index=True)
    out = out.groupby(["X","Y","date","hour","GRP"], observed=True, as_index=False)["CONC"].mean()
    return out

# Ave kind
def _ave_kind(value):
    t = re.sub(r"[^A-Z0-9]+", "", str(value or "").upper())
    if t in {"24", "24HR", "24H"} or t.startswith("24HR"):
        return "24H"
    if t in {"1", "01", "1HR", "01HR", "1H"} or t.startswith("1HR"):
        return "1H"
    return None

# Read post daily
def read_post_daily(path: Path, background=0.0, chunk_rows=350_000, progress=False, progress_label=None):
    """Retorna uma série diária por receptor a partir de POST 24-HR ou 1-HR.

    Colunas: X, Y, CONC, date, year, GRP, N_HOURS, SOURCE_AVERAGING.
    Para POST 1-HR, um dia é mantido apenas quando possui pelo menos
    ``config.MIN_VALID_HOURS_DAY`` horas. Para POST 24-HR, o valor é usado
    diretamente como média de 24 h.
    """
    info = inspect_pos_header(path)
    direct_parts = []
    hourly_parts = []
    detected = set()

    for ch in iter_pos_chunks(path, chunk_rows=chunk_rows, progress=progress, progress_label=progress_label):
        if ch.empty:
            continue
        ch["_kind"] = ch["AVE"].map(_ave_kind)
        detected.update(ch["_kind"].dropna().unique().tolist())
        ch = ch[ch["_kind"].isin(["1H", "24H"])].copy()
        if ch.empty:
            continue
        code = ch["DATECODE"].astype(str).str.replace(r"\.0$", "", regex=True).str.zfill(8)
        yy = pd.to_numeric(code.str.slice(0, 2), errors="coerce")
        mm = pd.to_numeric(code.str.slice(2, 4), errors="coerce")
        dd = pd.to_numeric(code.str.slice(4, 6), errors="coerce")
        ch["date"] = pd.to_datetime(dict(year=2000 + yy, month=mm, day=dd), errors="coerce")
        ch["CONC"] = pd.to_numeric(ch["CONC"], errors="coerce") + float(background)
        ch = ch.dropna(subset=["X", "Y", "CONC", "date"])

        d24 = ch[ch["_kind"] == "24H"]
        if not d24.empty:

            a = d24.groupby(["X", "Y", "date", "GRP"], observed=True, as_index=False).agg(CONC=("CONC", "mean"))
            a["N_HOURS"] = 24
            direct_parts.append(a)

        d1 = ch[ch["_kind"] == "1H"]
        if not d1.empty:

            a = d1.groupby(["X", "Y", "date", "GRP"], observed=True, as_index=False).agg(
                SUM_CONC=("CONC", "sum"), N_HOURS=("CONC", "count")
            )
            hourly_parts.append(a)

    if direct_parts:
        daily = pd.concat(direct_parts, ignore_index=True)
        daily = daily.groupby(["X", "Y", "date", "GRP"], observed=True, as_index=False).agg(
            CONC=("CONC", "mean"), N_HOURS=("N_HOURS", "max")
        )
        source_ave = "24H"
    elif hourly_parts:
        h = pd.concat(hourly_parts, ignore_index=True)
        h = h.groupby(["X", "Y", "date", "GRP"], observed=True, as_index=False).agg(
            SUM_CONC=("SUM_CONC", "sum"), N_HOURS=("N_HOURS", "sum")
        )
        h = h[h["N_HOURS"] >= int(config.MIN_VALID_HOURS_DAY)].copy()
        h["CONC"] = h["SUM_CONC"] / h["N_HOURS"]
        daily = h[["X", "Y", "date", "GRP", "CONC", "N_HOURS"]]
        source_ave = "1H→24H"
    else:
        raise ValueError(f"Nenhum registro 1-HR ou 24-HR encontrado em {path}")

    daily["year"] = daily["date"].dt.year.astype("Int64")
    daily["SOURCE_AVERAGING"] = source_ave
    info = dict(info)
    info["daily_source"] = source_ave
    info["detected_averaging"] = ",".join(sorted(detected))
    return daily, info

# Safe pollutant name
def _safe_pollutant_name(pollutant, path):
    if pollutant:
        return str(pollutant).replace("/", "_")
    inferred = _infer_pollutant(path)
    return inferred or "GEN"

# Pos fingerprint
def _pos_fingerprint(path: Path):
    path = Path(path)
    st = path.stat()
    n = int(getattr(config, "POS_CACHE_SAMPLE_BYTES", 1024 * 1024))
    h = hashlib.sha256()
    with path.open("rb") as f:
        head = f.read(n)
        h.update(head)
        if st.st_size > n:
            f.seek(max(0, st.st_size - n))
            h.update(f.read(n))
    return {
        "size": int(st.st_size),
        "mtime_ns": int(st.st_mtime_ns),
        "sample_sha256": h.hexdigest(),
    }

# Pos cache paths
def _pos_cache_paths(path: Path, pollutant=None):
    cache_root = Path(getattr(config, "DIRS", {}).get("pos_cache", Path(config.BASE) / "cache" / "pos"))
    pol = _safe_pollutant_name(pollutant, path)
    folder = cache_root / pol
    folder.mkdir(parents=True, exist_ok=True)
    resolved = Path(path).resolve()
    try:
        identity = resolved.relative_to(Path(config.BASE).resolve()).as_posix().lower()
    except ValueError:
        identity = str(resolved).lower()
    key = hashlib.sha1(identity.encode("utf-8", errors="ignore")).hexdigest()[:10]
    stem = re.sub(r"[^A-Za-z0-9_.-]+", "_", Path(path).stem)
    base = folder / f"{stem}_{key}"
    return {
        "daily": Path(str(base) + "_daily.pkl.gz"),
        "meta": Path(str(base) + "_meta.json"),
    }

# Cache signature
def _cache_signature(background):
    return {
        "cache_version": int(getattr(config, "POS_CACHE_VERSION", 1)),
        "min_valid_hours_day": int(config.MIN_VALID_HOURS_DAY),
        "background": float(background),
    }

# Cache is valid
def _cache_is_valid(path: Path, meta_path: Path, background):
    if not meta_path.exists():
        return False, None
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except Exception:
        return False, None
    if meta.get("signature") != _cache_signature(background):
        return False, meta
    try:
        fp = _pos_fingerprint(path)
    except Exception:
        return False, meta
    return meta.get("source_fingerprint") == fp, meta

# Read post daily cached
def read_post_daily_cached(path: Path, background=0.0, pollutant=None, chunk_rows=350_000):
    """Lê o POST e mantém cache persistente da série diária tratada.

    O cache é invalidado automaticamente quando o .POS muda em tamanho, data
    de modificação ou amostra binária do início/fim.
    """
    path = Path(path)
    use_cache = bool(getattr(config, "USE_POS_CACHE", True))
    force = bool(getattr(config, "FORCE_REBUILD_POS_CACHE", False))
    paths = _pos_cache_paths(path, pollutant)

    if use_cache and not force and paths["daily"].exists():
        valid, meta = _cache_is_valid(path, paths["meta"], background)
        if valid:
            t0 = time.perf_counter()
            print(f"    [CACHE HIT] {path.name} -> usando série diária tratada", flush=True)
            daily = pd.read_pickle(paths["daily"], compression="gzip")
            load_elapsed = time.perf_counter() - t0
            print(
                f"    [CACHE OK] {path.name}: {len(daily):,} registros diários carregados em "
                f"{_fmt_elapsed(load_elapsed)}", flush=True
            )
            info = dict((meta or {}).get("info") or {})
            info["cache_used"] = True
            info["cache_file"] = str(paths["daily"])
            info["cache_load_seconds"] = round(time.perf_counter() - t0, 3)
            return daily, info

    reason = "forçado" if force else "primeira leitura ou .POS alterado"
    print(f"    [CACHE MISS] {path.name} -> {reason}; processando arquivo bruto...", flush=True)
    t0 = time.perf_counter()
    progress_enabled = bool(getattr(config, "SHOW_POS_PROGRESS", True))
    chunk_rows = int(getattr(config, "POS_PROGRESS_CHUNK_ROWS", chunk_rows))
    daily, info = read_post_daily(
        path, background=background, chunk_rows=chunk_rows,
        progress=progress_enabled, progress_label=path.name,
    )
    elapsed = time.perf_counter() - t0

    if use_cache:
        t1 = time.perf_counter()

        tmp_daily = Path(str(paths["daily"]) + ".tmp")
        tmp_meta = Path(str(paths["meta"]) + ".tmp")
        for tmp in (tmp_daily, tmp_meta):
            if tmp.exists():
                try:
                    tmp.unlink()
                except OSError:
                    pass
        daily.to_pickle(tmp_daily, compression="gzip")
        meta = {
            "source_file": str(path.resolve()),
            "source_fingerprint": _pos_fingerprint(path),
            "signature": _cache_signature(background),
            "info": dict(info),
            "rows_daily": int(len(daily)),
            "created_epoch": time.time(),
            "raw_processing_seconds": round(elapsed, 3),
        }
        tmp_meta.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
        os.replace(tmp_daily, paths["daily"])
        os.replace(tmp_meta, paths["meta"])
        print(
            f"    [CACHE SAVE] {path.name}: {len(daily):,} registros diários tratados "
            f"salvos em {paths['daily'].name} ({time.perf_counter()-t1:.1f}s)",
            flush=True,
        )
    info = dict(info)
    info["cache_used"] = False
    info["cache_file"] = str(paths["daily"]) if use_cache else ""
    info["raw_processing_seconds"] = round(elapsed, 3)
    return daily, info

# Summarize post for pm
def summarize_post_for_pm(path: Path, pollutant: str, background=0.0):
    """Calcula P98 diário e média anual por receptor usando POST 24h ou horário."""
    daily, info = read_post_daily_cached(path, background=background, pollutant=pollutant)
    yearly_parts = []
    for year, dyear in daily.groupby("year", observed=True):
        agg = dyear.groupby(["X", "Y"], observed=True).agg(
            ANNUAL_MEAN=("CONC", "mean"),
            N_DAYS=("CONC", "count"),
            P98=("CONC", lambda x: nearest_rank_percentile(x, config.SHORT_TERM_PERCENTILE)),
        ).reset_index()
        year = int(year)
        expected = 366 if pd.Timestamp(year, 12, 31).is_leap_year else 365
        agg["year"] = year
        agg["EXPECTED_DAYS"] = expected
        agg["COMPLETENESS"] = agg["N_DAYS"] / expected
        agg["VALID_YEAR"] = agg["COMPLETENESS"] >= config.MIN_QUARTER_COMPLETENESS
        yearly_parts.append(agg)

    if not yearly_parts:
        raise ValueError(f"Sem médias diárias válidas em {path}")
    yearly = pd.concat(yearly_parts, ignore_index=True)
    n_required = int(config.MODEL_N_YEARS_DESIGN)

    summaries = []
    for (x, y), sub in yearly.groupby(["X", "Y"], sort=False):
        valid_years = sorted(sub.loc[sub["VALID_YEAR"], "year"].astype(int).tolist())
        valid = pd.DataFrame(columns=sub.columns)
        for end_year in sorted(valid_years, reverse=True):
            wanted = list(range(end_year - n_required + 1, end_year + 1))
            if all(yv in valid_years for yv in wanted):
                valid = sub[sub["year"].isin(wanted)].sort_values("year")
                break
        row = {
            "X": float(x), "Y": float(y),
            "n_model_years": int(len(valid)),
            "years_model": ",".join(map(str, valid["year"].astype(int).tolist())) if len(valid) else "",
            "SOURCE_AVERAGING": info.get("daily_source", ""),
        }
        if len(valid) == n_required:
            row["P98_MODEL"] = float(valid["P98"].mean())
            row["ANNUAL_MODEL"] = float(valid["ANNUAL_MEAN"].mean())
        else:
            row["P98_MODEL"] = np.nan
            row["ANNUAL_MODEL"] = np.nan
        row["n_design_years"] = row["n_model_years"]
        row["years_valid"] = row["years_model"]
        row["P98_3YR"] = row["P98_MODEL"]
        row["ANNUAL_3YR"] = row["ANNUAL_MODEL"]
        summaries.append(row)

    out = pd.DataFrame(summaries)
    for scenario in ("PV", "PF"):
        lim24 = STANDARDS[pollutant][scenario]["24H"]
        limann = STANDARDS[pollutant][scenario]["ANNUAL"]
        out[f"ratio24_{scenario}"] = out["P98_MODEL"] / lim24
        out[f"ratioann_{scenario}"] = out["ANNUAL_MODEL"] / limann
        out[f"status_{scenario}"] = np.select(
            [
                out["n_model_years"] < n_required,
                (out["P98_MODEL"] <= lim24) & (out["ANNUAL_MODEL"] <= limann),
            ],
            ["insuficiente", "atendimento"],
            default="nao_atendimento",
        )

    gdf = gpd.GeoDataFrame(out, geometry=gpd.points_from_xy(out["X"], out["Y"]), crs=config.CRS_PROJECT)
    return gdf, yearly, info

# Pollutant folder
def _pollutant_folder(post_dir: Path, pollutant: str):
    names = ["PM10"] if pollutant == "PM10" else ["PM2-5", "PM25", "PM2_5"]
    for name in names:
        p = post_dir / name
        if p.exists() and p.is_dir():
            return p
    return post_dir

# Discover post main
def discover_post_main(post_dir: Path, pollutant: str):
    """Localiza o cenário ALL do poluente.

    Prioriza arquivos do grupo ALL dentro da pasta do poluente e aceita tanto
    POST 24-HR quanto POST 1-HR. O período é verificado pelo cabeçalho.
    """
    override = config.POST_OVERRIDE[pollutant].get("24H")
    if override:
        p = Path(override)
        if p.exists():
            return p
    folder = _pollutant_folder(post_dir, pollutant)
    files = _unique_paths(sorted(folder.glob("*.POS")) + sorted(folder.glob("*.pos")))
    if not files and folder == post_dir:
        files = _unique_paths(sorted(post_dir.rglob("*.POS")) + sorted(post_dir.rglob("*.pos")))

    compatible = []
    for p in files:
        pol = _infer_pollutant(p)
        if pol not in {None, pollutant}:
            continue
        info = inspect_pos_header(p)
        kind = _ave_kind(info.get("ave"))
        if kind not in {"1H", "24H"}:
            continue
        text = re.sub(r"[^A-Z0-9]+", "", p.stem.upper())
        is_all = "GALL" in text or text.endswith("ALL") or str(info.get("group", "")).upper() == "ALL"
        compatible.append((p, kind, is_all))

    all_files = [x for x in compatible if x[2]]
    pool = all_files or compatible
    if not pool:
        return None

    pool.sort(key=lambda x: (0 if x[1] == "24H" else 1, x[0].name))
    return pool[0][0]

# Discover group posts any
def discover_group_posts_any(post_dir: Path, pollutant: str):
    """Lista POSTFILEs 1-HR/24-HR na pasta específica do poluente."""
    folder = _pollutant_folder(post_dir, pollutant)
    files = _unique_paths(sorted(folder.glob("*.POS")) + sorted(folder.glob("*.pos")))
    if not files and folder == post_dir:
        files = _unique_paths(sorted(post_dir.rglob("*.POS")) + sorted(post_dir.rglob("*.pos")))
    out = []
    for p in files:
        pol = _infer_pollutant(p)
        if pol not in {None, pollutant}:
            continue
        info = inspect_pos_header(p)
        if _ave_kind(info.get("ave")) in {"1H", "24H"}:
            out.append((p, info))
    return out
