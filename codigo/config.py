# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entradas: argumentos do chamador e módulos locais relacionados no relatório.
# Campos/chaves em DIRS: emission, grade_generated, limite_cong, limite_emp, qar, uso_terra, vias, zoneamento.
# Saídas: retorno de funções, verificações ou arquivos definidos pelo chamador.
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

from pathlib import Path
import os

# Resolve project root
def _resolve_project_root() -> Path:
    """Resolve a raiz do projeto sem depender do diretório de execução.

    A pasta acima de codigo é a raiz, inclusive após migrações entre discos.
    EMI_PROJECT_ROOT permite uma substituição explícita para testes e executores.
    """
    return _cp_raiz()

BASE = _resolve_project_root()

DIRS = {
    "ref": BASE / "0_ref",
    "disp": BASE / "cen_dispersao",
    "limite_cong": BASE / "limite_cong",
    "limite_emp": BASE / "limite_emp",
    "qar": BASE / "qar",
    "qar_met": BASE / "qar_met",
    "uso_terra": BASE / "uso_terra",
    "vias": BASE / "vias",
    "zoneamento": BASE / "zoneamento",
    "emission": BASE / "emission",
    "post": BASE / "out-aermod",
    "aermod_logs": BASE / "adi_ado_sum",
    "grade": BASE / "grade",
    "grade_generated": BASE / "grade" / "gerada",
    "out": BASE / "output",
    "cache": BASE / "cache",
    "pos_cache": BASE / "cache" / "pos",
    "regional": BASE / "base_regional",
}

CRS_PROJECT = "EPSG:31983"
CRS_GEOGRAPHIC = "EPSG:4674"

ZERO_AS_MISSING = True
MIN_VALID_HOURS_DAY = 18
MIN_QUARTER_COMPLETENESS = 0.75
MONITOR_MIN_VALID_HOURS_DAY = 16
MONITOR_MIN_QUADRIMESTER_COMPLETENESS = 0.50
MONITOR_PERIOD_LABEL = "2023–2025"
N_YEARS_DESIGN = 3
MODEL_N_YEARS_DESIGN = 3
MODEL_PERIOD_LABEL = "2021–2023"
SHORT_TERM_PERCENTILE = 0.98

SHORT_TERM_METHOD = "P98_3YR"

INITIAL_REPRESENTATIVITY_CLASS = "Bairro"
REPRESENTATIVITY_RADIUS_M = 4000.0
STATION_COVERAGE_RADIUS_M = {}
MIN_ADT_MAIN_ROAD = 1000

ADT_FIELD_CANDIDATES = [
    "ADT", "AADT", "VMDA", "VMD", "trafego", "TRAFEGO",
    "veic_dia", "VEIC_DIA", "volume", "VOLUME"
]

USE_POS_CACHE = True
FORCE_REBUILD_POS_CACHE = False
POS_CACHE_VERSION = 1
POS_CACHE_SAMPLE_BYTES = 1024 * 1024

SHOW_POS_PROGRESS = True
POS_PROGRESS_MIN_SECONDS = 8.0
POS_PROGRESS_CHUNK_ROWS = 350_000

BACKGROUND_UGM3 = {
    "PM10": 0.0,
    "PM25": 0.0,
}

MODEL_BUFFER_M = 3500.0
GRID_NOMINAL_M = 500.0

RUN_RECEPTOR_GRID = True
GRID_REQUIRE_POPULATION_DATA = True
GRID_MODE = "population_communities_optimized_coverage"
GRID_COVERAGE_RADIUS_M = 500.0
GRID_INTERNAL_COVERAGE_METHOD = "coverage"
GRID_INTERNAL_SPACING_M = 500.0
GRID_INTERNAL_MIN_SPACING_M = 1.0
GRID_INTERNAL_GAP_FILL_STEP_M = 250.0
GRID_BOUNDARY_SPACING_M = 500.0

GRID_BOUNDARY_SIMPLIFY_M = 50.0
GRID_BOUNDARY_LINK_TOLERANCE_M = 2.0

GRID_INCLUDE_INTERNAL_BOUNDARIES = False
GRID_INCLUDE_INTERNAL_COVERAGE_POINTS = True
GRID_INCLUDE_STATION_RECEPTORS = True
GRID_REQUIRE_FULL_COVERAGE = True

GRID_COMMUNITY_LINK_DISTANCE_M = 1000.0
GRID_COMMUNITY_MIN_POPULATION = 0.0
GRID_ONE_REPRESENTATIVE_PER_ZONE = False
GRID_USE_LANDUSE_FOR_POP_ANCHOR = True
GRID_POPULATED_LANDUSE_CLASSES = [24]
GRID_COVERAGE_CHECK_STEP_M = 100.0

GRID_UNCOVERED_AREA_TOLERANCE_M2 = 200.0
GRID_UNCOVERED_AREA_REL_TOLERANCE_PCT = 0.001
GRID_POINT_DEDUPLICATION_M = 1.0
GRID_EXTERNAL_INNER_LIMIT_M = 500.0
GRID_EXTERNAL_INNER_SPACING_M = 500.0
GRID_EXTERNAL_OUTER_LIMIT_M = 3500.0
GRID_EXTERNAL_OUTER_SPACING_M = 1000.0
GRID_EXTERNAL_INTERNAL_DEDUPLICATION_M = 300.0

HIGH_LOW_METHOD = "q75"
HIGH_LOW_METHOD_EMISSION = "q75"
HIGH_LOW_METHOD_CONCENTRATION = "median"
EMISSION_HIGH_MIN_FRACTION_OF_MAX = 0.05
EMISSION_CLASS_METRIC = "EMIS_DENS_GS_KM2"

EMISSION_PRESSURE_QUANTILE = 0.75
EMISSION_FOCAL_THRESHOLD_RELATIVE_TOLERANCE = 0.01
EMISSION_INDUSTRIAL_HIGH_QUANTILE = 0.67
EMISSION_URBAN_HIGH_QUANTILE = 0.90
EMISSION_POINT_SUPPORT_RADIUS_M = 250.0
EMISSION_LINE_SUPPORT_HALF_WIDTH_M = 50.0
CONCENTRATION_CLASS_METRIC_24H = "P98_MODEL"
CONCENTRATION_CLASS_METRIC_ANNUAL = "ANNUAL_MODEL"
MIN_ZONE_MONITOR_COVERAGE_PCT = 50.0
MIN_BUFFER_ZONE_OVERLAP_PCT = 10.0

MAP_DPI = 600
MAP_LEVELS = 12
MAP_CMAP = "turbo"
SHOW_ZONE_OUTLINES_ON_SURFACE = True
WRF_SURFACE_BLACK_BACKGROUND = False
MAP_OUTSIDE_FACE = "#eff4f8"
MAP_BACKGROUND_FILL = "#f7fafc"
REGIONAL_BACKGROUND_BUFFER_M = 2500.0
REGIONAL_MUNICIPALITY_SEARCH_BUFFER_M = 15000.0

ROAD_FCLASS_FIELD = "fclass"
ROAD_SHOW_LEGEND = True

FILES = {
    "station_coords": DIRS["qar"] / "station_id.xlsx",
    "station_network": DIRS["qar"] / "est_cong.kmz",
    "municipality": DIRS["limite_cong"] / "congonhas.kml",
    "enterprises": DIRS["limite_emp"] / "limite_emp.kmz",
    "roads": DIRS["vias"] / "vias_cong.shp",
    "zoning": DIRS["zoneamento"] / "zon_cong.shp",
    "landuse_1985": DIRS["uso_terra"] / "mapbiomas-brazil-collection-101-congonhas-1985.tif",
    "landuse_2024": DIRS["uso_terra"] / "mapbiomas-brazil-collection-101-congonhas-2024.tif",
    "sources_PM10": DIRS["emission"] / "PM10_Sources.xlsx",
    "sources_PM25": DIRS["emission"] / "PM2-5_Sources.xlsx",

    "grid_500m": DIRS["grade_generated"] / "grade_receptores_adaptativa.csv",
    "regional_municipalities": None,
}

POST_OVERRIDE = {
    "PM10": {"24H": None, "ANNUAL": None},
    "PM25": {"24H": None, "ANNUAL": None},
}

QAR_EXCLUDE_XLSX = {"station_id.xlsx"}

RUN_LANDUSE = True
RUN_SOURCE_APPORTIONMENT = True
RUN_ENTERPRISE_ASSOCIATION = True

RUN_MODEL_SURFACE_MAPS = True

PREFERRED_LANDUSE_DIR_ALIASES = ["uso_terra", "uso terra"]

RUN_PLUME_GIF = True
PLUME_FRAME_DPI = 220
PLUME_GIF_FPS = 1
PLUME_MAX_HOURS = 24

STATION_DISPLAY_NAMES = {
    "motas": "Motas",
    "pires": "Pires",
    "n-plat": "Novo Plataforma",
    "matriz": "Matriz",
    "basilica": "Basílica",
    "j-prof": "Jardim Profeta",
    "lobo-leite": "Lobo Leite",
}

POLLUTANT_DISPLAY = {
    "PM10": "MP₁₀",
    "PM25": "MP₂,₅",
}

MONITOR_ZONE_CLASSIFICATION = "coverage"
MODEL_ZONE_STATUS_METHOD = "zone_mean"
MODEL_ZONE_EXCEEDANCE_FRACTION = 0.50

SOURCE_GEOMETRY_SEARCH_PATTERNS = [
    "*Area Source*.kml", "*Circular Area Source*.kml", "*Line Area Source*.kml",
    "*Line Source*.kml", "*Point Source*.kml", "*Polygon Area Source*.kml",
    "*Volume Source*.kml", "*Area Source*.kmz", "*Circular Area Source*.kmz",
    "*Line Area Source*.kmz", "*Line Source*.kmz", "*Point Source*.kmz",
    "*Polygon Area Source*.kmz", "*Volume Source*.kmz",
]

IBGE_MG_MUNICIPALITIES_URL = "https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2024/UFs/MG/MG_Municipios_2024.zip"
AUTO_DOWNLOAD_REGIONAL_MUNICIPALITIES = True

MAP_FOCUS_BUFFER_M = 2500.0
SATELLITE_BASEMAP_ALPHA = 0.28

USE_SATELLITE_BASEMAP = False

PLUME_ANIMATION_MODE = "both"
PLUME_GIF_FPS = 1
PLUME_MAX_FRAMES = 31

REGIONAL_FALLBACK_LABELS = [
    ("Ouro Preto", 0.58, 0.92),
    ("Conselheiro Lafaiete", 0.88, 0.50),
    ("Ouro Branco", 0.72, 0.16),
    ("Jeceaba", 0.28, 0.16),
    ("Belo Vale", 0.12, 0.50),
    ("São Brás do Suaçuí", 0.78, 0.80),
]

PLUME_MIN_PERCENTILE = 25.0
PLUME_MIN_FRACTION_OF_MAX = 0.05

PLUME_HOURLY_MAX_FRAMES = 24

PLUME_DAILY_MIN_PERCENTILE = 30.0

PLUME_DAILY_MIN_FRACTION_OF_MAX = 0.06

PLUME_HOURLY_MIN_PERCENTILE = 45.0

PLUME_HOURLY_MIN_FRACTION_OF_MAX = 0.10

RUN_HEALTH_IMPACT = True
HEALTH_COUNTERFACTUAL_UGM3 = 5.0
HEALTH_ENDPOINTS_TEMPLATE = BASE / "insumos_saude" / "saude_endpoints_template.csv"
HEALTH_POPULATION_TEMPLATE = BASE / "insumos_saude" / "saude_populacao_zonas_template.csv"
HEALTH_NOTES_TEMPLATE = BASE / "insumos_saude" / "LEIA-ME_impacto_saude.txt"
HEALTH_INPUT_DIRNAME = "05_impacto_saude"
REGIONAL_BOUNDARIES_CACHE = BASE / "base_regional" / "municipios_vizinhos_cache.geojson"

ABC_A_LIMIT_PCT = 80.0
ABC_B_LIMIT_PCT = 95.0
ABC_REDUCTION_SCENARIOS = [0.10, 0.20, 0.30, 0.50]

MANAGEMENT_WEIGHT_CONCENTRATION = 0.35
MANAGEMENT_WEIGHT_EMISSION = 0.25
MANAGEMENT_WEIGHT_STANDARD_STATUS = 0.25
MANAGEMENT_WEIGHT_MONITOR_GAP = 0.15

CENSO_DIR = BASE / "censo_ibge"
CENSO_AUTO_DOWNLOAD = True
CENSO_AUTO_DOWNLOAD_BASICO_FINAL = True
IBGE_DEMOGRAFIA_URL = "https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios/Agregados_por_Setor_csv/Agregados_por_setores_demografia_BR.zip"
IBGE_DICIONARIO_URL = "https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios/dicionario_de_dados_agregados_por_setores_censitarios_20260520.xlsx"
IBGE_BASICO_URL = "https://ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios/Agregados_por_Setor_csv/Agregados_por_setores_basico_BR_20260520.zip"
CENSO_POP_ALLOCATION_METHOD = "area_weighted"

ABC_TOP_N_DEFAULT = 9
ABC_DASHBOARD = True

MODEL_MAP_FOCUS_BUFFER_M = 3800.0

HEALTH_SCREENING_COUNTERFACTUAL_UGM3 = 5.0
HEALTH_SCREENING_PV_ANNUAL_UGM3 = 17.0
HEALTH_SCREENING_GENERATE_AF = True
ABC_EXPORT_ZONE_PRIORITY_MAPS = True
