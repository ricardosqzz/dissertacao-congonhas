# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entradas: argumentos do chamador e módulos locais relacionados no relatório.
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

STANDARDS = {
    "PM10": {
        "PV": {"label": "PI-2", "24H": 100.0, "ANNUAL": 35.0},
        "PF": {"label": "PF",   "24H": 45.0,  "ANNUAL": 15.0},
    },
    "PM25": {
        "PV": {"label": "PI-2", "24H": 50.0, "ANNUAL": 17.0},
        "PF": {"label": "PF",   "24H": 15.0, "ANNUAL": 5.0},
    },
}

STAGE_ORDER = ('PF', 'PI4', 'PI3', 'PI2', 'PI1')
_STAGE_VALUES = {
    'PM10': ((45,15),(50,20),(75,30),(100,35),(120,40)),
    'PM25': ((15,5),(25,10),(37,15),(50,17),(60,20)),
}
for _pol, _values in _STAGE_VALUES.items():
    for _stage, (_daily, _annual) in zip(STAGE_ORDER, _values):
        STANDARDS[_pol][_stage] = {'label': _stage.replace('PI','PI-'),
                                  '24H': float(_daily), 'ANNUAL': float(_annual)}

POLLUTANT_ALIASES = {
    "PM10": ["PM10", "MP10", "PM10_UGM-3", "MP10_UGM-3"],
    "PM25": [
        "PM2-5", "PM2.5", "PM2,5", "PM25", "MP2-5", "MP2.5", "MP2,5", "MP25",
        "PM2-5_UGM-3", "PM2.5_UGM-3", "PM2,5_UGM-3", "MP2-5_UGM-3"
    ],
}

STATUS_ORDER = {
    "sem_dado": 0,
    "insuficiente": 1,
    "atendimento": 2,
    "nao_atendimento": 3,
}

# Nearest rank percentile
def nearest_rank_percentile(values, p=0.98):
    """Percentil por posto (nearest-rank), sem interpolação.

    Para n valores ordenados crescentemente, usa posição ceil(p*n), limitada a 1..n.
    Essa forma é mais próxima do procedimento de seleção por posto usado em métricas
    regulatórias do que a interpolação linear padrão de muitas bibliotecas.
    """
    import math
    import numpy as np
    arr = np.asarray(list(values), dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return np.nan
    arr.sort()
    rank = max(1, min(arr.size, int(math.ceil(float(p) * arr.size))))
    return float(arr[rank - 1])

# Annual p98
def annual_p98(values):
    """Tabela 1 do 40 CFR 50, Apêndice N, §4.5, para série diária contínua.

    Seleciona o ceil(n/50)-ésimo MAIOR dia válido, sem interpolação. Difere
    de ceil(0,98*n) quando n é múltiplo de 50. Todos os dias válidos desta
    série são creditáveis; não se aplica a calendário de amostragem distinto.
    A extensão ao MP10 é comparativa, não uma regra legal desse poluente.
    """
    import numpy as np
    arr=np.asarray(list(values),dtype=float)
    arr=np.sort(arr[np.isfinite(arr)])
    if not len(arr):return float('nan')
    rank=(len(arr)+49)//50
    return float(arr[-rank])
