# CONFIGURAÇÃO DE ENTRADAS E SAÍDAS
# Configuração editável: codigo/caminhos_projeto.json
# Raiz dos dados: raiz_projeto; pastas e arquivos admitem caminhos próprios.
# Entradas: argumentos do chamador e módulos locais relacionados no relatório.
# Campos/chaves em value: name.
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

import re
import unicodedata

GROUPS = {
    "AEX":      {"name": "Áreas Expostas", "expected": 243, "kind": "overlap"},
    "BVC":      {"name": "BVC Transportes", "expected": 11, "kind": "primary"},
    "CDA":      {"name": "CDA Logística", "expected": 17, "kind": "primary"},
    "COC":      {"name": "Concrelagos Concreto", "expected": 16, "kind": "primary"},
    "COOPERA":  {"name": "Cooperauto", "expected": 5, "kind": "primary"},
    "CSN-CDP":  {"name": "CSN – Casa de Pedra", "expected": 146, "kind": "primary"},
    "CSN-PIR":  {"name": "CSN – Namisa/Pires", "expected": 37, "kind": "primary"},
    "ECOMIN":   {"name": "Ecomining América", "expected": 13, "kind": "primary"},
    "FERRO":    {"name": "Ferro+", "expected": 68, "kind": "primary"},
    "GERDAU":   {"name": "Gerdau Ouro Branco", "expected": 380, "kind": "primary"},
    "LGA":      {"name": "LGA Mineração", "expected": 53, "kind": "primary"},
    "LL-TRANS": {"name": "LL Transportes", "expected": 3, "kind": "primary"},
    "LM-MIN":   {"name": "LM Mining Company Eireli", "expected": 12, "kind": "primary"},
    "MONT-MIN": {"name": "Monteminas Minérios", "expected": 4, "kind": "primary"},
    "NOGD":     {"name": "Nogueira Duarte", "expected": 25, "kind": "primary"},
    "RODEIRO":  {"name": "Rodeiro", "expected": 2, "kind": "primary"},
    "SAPPORO":  {"name": "Sapporo Indústria e Comércio", "expected": 30, "kind": "primary"},
    "SILVANO":  {"name": "Silvano Transportes", "expected": 4, "kind": "primary"},
    "TERRA-MI": {"name": "Terra Minas", "expected": 1, "kind": "primary"},
    "TERRAMAR": {"name": "Terramares", "expected": 16, "kind": "primary"},
    "URB":      {"name": "Urbano Total", "expected": 103, "kind": "primary"},
    "URB-FER":  {"name": "Ferrovias Urbanas", "expected": 44, "kind": "subgroup"},
    "URB-NUC":  {"name": "Núcleo Urbano", "expected": 10, "kind": "subgroup"},
    "URB-VIA":  {"name": "Ressuspensão urbana", "expected": 49, "kind": "subgroup"},
    "VALE_FAB": {"name": "Vale – Fábrica", "expected": 144, "kind": "primary"},
    "VALE_VIG": {"name": "Vale – Viga", "expected": 117, "kind": "primary"},
    "WGM":      {"name": "WG Mineração", "expected": 8, "kind": "primary"},
    "SCOF":     {"name": "SCOF", "expected": 13, "kind": "primary"},
}

ALIASES = {
    "VALESAMINADEFABRICA": "VALE_FAB", "VALESAMINADEVIGA": "VALE_VIG",
    "CSNCDP": "CSN-CDP", "CSNCP": "CSN-CDP", "CASADEPEDRA": "CSN-CDP",
    "CSNPIR": "CSN-PIR", "PIRESCSN": "CSN-PIR", "CSNPIRES": "CSN-PIR",
    "CSNNAMISA": "CSN-PIR", "NAMISA": "CSN-PIR", "NAMISAPIRES": "CSN-PIR",
    "CONCRELAGOS": "COC", "COOPERauto": "COOPERA", "COOPERAUTO": "COOPERA",
    "LLTRANS": "LL-TRANS", "LMMIN": "LM-MIN", "MONTMIN": "MONT-MIN",
    "MONTEMINAS": "MONT-MIN", "MONTEMINASMINERIOS": "MONT-MIN", "MOM": "MONT-MIN",
    "TERRAMI": "TERRA-MI", "TERRAMINAS": "TERRA-MI",
    "VALEFAB": "VALE_FAB", "VALEFABRICA": "VALE_FAB", "VALEVIG": "VALE_VIG", "VALEVIGA": "VALE_VIG",
    "NOGD": "NOGD", "NOGDUAR": "NOGD", "NOGUEIRADUARTE": "NOGD",
    "ECOMINING": "ECOMIN", "GERDAU": "GERDAU", "FERRO": "FERRO",
    "SILVANO": "SILVANO", "RODEIRO": "RODEIRO", "SAPPORO": "SAPPORO",
    "TERRAMARES": "TERRAMAR", "WGM": "WGM", "WGMINERACAO": "WGM", "SCOF": "SCOF",
}

# Norm token
def norm_token(value):
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"[^A-Z0-9]+", "", text.upper())

# Canonical group
def canonical_group(value):
    t = norm_token(value)
    if not t:
        return None
    for key in GROUPS:
        if norm_token(key) == t:
            return key
    for alias, key in ALIASES.items():
        if norm_token(alias) in t:
            return key
    for key in GROUPS:
        if key in {"AEX", "URB-FER", "URB-NUC", "URB-VIA"}:
            continue
        kt = norm_token(key)
        if kt and kt in t:
            return key
    if t.startswith("AEX"):
        return "AEX"
    return None

# Urban subgroup from source
def urban_subgroup_from_source(source_id):
    raw = str(source_id or "").upper().replace("-", "_")
    token = norm_token(source_id)

    if raw.startswith("VIA_P") or token.startswith("VIAP"):
        return "URB-VIA"
    if token.startswith("URBU"):
        return "URB-NUC"
    if token.startswith("FER"):
        return "URB-FER"
    return None

# Is exposed area
def is_exposed_area(source_id):
    return norm_token(source_id).startswith("AEX")

# Infer primary group from source
def infer_primary_group_from_source(source_id, desc=None):

    suffixes={'CCA':'CSN-CDP','CPI':'CSN-PIR','GER':'GERDAU','VMF':'VALE_FAB',
              'VMV':'VALE_VIG','FEP':'FERRO','SAP':'SAPPORO','NOD':'NOGD',
              'TMA':'TERRAMAR','ECO':'ECOMIN','LLM':'LM-MIN','CPA':'COOPERA',
              'SSR':'SILVANO','LLT':'LL-TRANS','ROD':'RODEIRO','TMI':'TERRA-MI',
              'BVC':'BVC','CDA':'CDA','COC':'COC','LGA':'LGA','MOM':'MONT-MIN'}
    token=norm_token(source_id)
    if re.fullmatch(r'WG[0-9]+',token):
        return 'WGM'
    for suffix,group in suffixes.items():
        if re.match(r'^[A-Z]+[0-9]+[A-Z]*'+suffix+r'$',token):
            return group
    subgroup = urban_subgroup_from_source(source_id)
    if subgroup:
        return "URB"

    by_id=canonical_group(source_id)
    if by_id and by_id not in {'AEX','URB-FER','URB-NUC','URB-VIA'}:
        return by_id

    text = f"{source_id or ''} {desc or ''}"
    g = canonical_group(text)
    if g in {"AEX", "URB-FER", "URB-NUC", "URB-VIA"}:
        return None
    return g

POST_GROUP_NAMES = {
    "ALL": "Todas as fontes",
    "GERDAU": "Gerdau Ouro Branco",
    "CSN-CDP": "CSN – Casa de Pedra",
    "CSN-PIR": "CSN – Namisa/Pires",
    "FERRO": "Ferro+",
    "LGA": "LGA Mineração",
    "MINING": "Mineração - grupo agregado",
    "NOGD": "Nogueira Duarte",
    "URB": "Fontes urbanas",
    "VALE_FAB": "Vale – Fábrica",
    "VALE_VIG": "Vale – Viga",
}
POST_GROUP_NAMES.update({key: value['name'] for key, value in GROUPS.items()})

POST_FILE_ALIASES = {
    "GALL": "ALL",
    "ALL": "ALL",
    "GCSNCDP": "CSN-CDP",
    "GCSN_CDP": "CSN-CDP",
    "GCSNPIR": "CSN-PIR",
    "GCSN_PIR": "CSN-PIR",
    "GFERRO": "FERRO",
    "GGERDAU": "GERDAU",
    "GLGA": "LGA",
    "GMINING": "MINING",
    "GNOGDUAR": "NOGD",
    "GNOG_DUAR": "NOGD",
    "GURB": "URB",
    "GVALEFAB": "VALE_FAB",
    "GVALE_FAB": "VALE_FAB",
    "GVALEVIG": "VALE_VIG",
    "GVALE_VIG": "VALE_VIG",
}

# Canonical post group
def canonical_post_group(value):
    raw = str(value or "").upper().strip()
    token = norm_token(raw)
    if not token:
        return None

    stripped = re.sub(r"^[0-9]+", "", token)
    for key in ['ALL', *GROUPS]:
        if stripped in {norm_token(key), 'G'+norm_token(key)}:
            return key
    for alias, group in POST_FILE_ALIASES.items():
        if norm_token(alias) == token:
            return group

    token2 = re.sub(r"^[0-9]+", "", token)
    for alias, group in POST_FILE_ALIASES.items():
        if norm_token(alias) == token2 or norm_token(alias) in token2:
            return group
    g = canonical_group(value)
    return g
