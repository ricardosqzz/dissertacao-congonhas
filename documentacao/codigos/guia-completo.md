# Relatório dos códigos — Congonhas

Edição de 14 de novembro de 2026. Fontes locais e resultados atuais, sem reexecução dos modelos de dispersão.

## Como usar este relatório

Este documento reúne uma explicação metodológica e fichas dos códigos existentes na pasta de trabalho. Cada ficha informa finalidade, dependências, entradas, campos, produtos e trechos reais do arquivo. O índice HTML ao lado deste PDF permite buscar um nome e abrir a ficha completa, com o código integral numerado. O inventário CSV/JSON registra as assinaturas dos arquivos. Bibliotecas de terceiros distribuídas com Quarto, Node e outros programas não são códigos autorais e ficaram fora desse inventário.

As fichas distinguem cálculo atual, apoio, teste, geração editorial e rotina histórica. A presença de um arquivo na pasta não significa que seja necessário executá-lo para atualizar todos os resultados. As etapas antigas de migração e os geradores dos seminários entregues permanecem para rastreabilidade e não devem ser executados como um lote indiscriminado.

As entradas explicitadas foram levantadas na sintaxe dos programas e conferidas nos módulos principais. Expressões como `{path}`, argumentos do chamador e nomes compostos em tempo de execução são interfaces, não arquivos faltantes. Nos cabeçalhos, “campos/chaves” inclui atributos de camadas, colunas de tabelas e chaves de configuração. O dicionário de campos do TECO mantém a descrição específica por camada. O código integral resolve eventuais ambiguidades de uma expressão dinâmica.

## Caminhos, ambiente e reprodução em outro computador

O arquivo `codigo/caminhos_projeto.json` concentra a raiz, remapeamentos de pastas, exceções de arquivos e dependências externas. Com `raiz_projeto` vazio, a pasta que contém `codigo` é a raiz adotada. Ao copiar toda a árvore do projeto e mantê-la organizada, não é necessário conservar a letra E do disco. Para usar dados fora dessa árvore, preencher `raiz_projeto` ou o item correspondente em `pastas`/`arquivos`. Os programas consultam esse arquivo pelos módulos `caminhos_<projeto>` de cada linguagem.

Exemplo de configuração a adaptar, sem alterar os campos e as equações do processamento:

```json
{"raiz_projeto":"D:/Pesquisa/Meu projeto",
 "pastas":{"output":"D:/Pesquisa/Resultados"},
 "arquivos":{},"externos":{},"ambiente":{}}
```

A raiz pode ser sobrescrita pelas variáveis de ambiente CONGONHAS_PROJECT_ROOT, TECO_PROJECT_ROOT ou COPASA_PROJECT_ROOT. Congonhas também preserva EMI_PROJECT_ROOT. Cada projeto tem seu próprio arquivo de configuração e não consulta o de outro projeto. Os itens em `externos` identificam arquivos fora da árvore, fontes tipográficas, modelos e executáveis. Eles devem ser revistos na máquina de destino. O JSON armazena caminhos, não instala os programas.

As ferramentas administrativas que geram e conferem esta documentação dos três projetos utilizam também a tabela PROJETOS, no início de documentar_portabilidade.py, para localizar cada árvore. Ao transferir essas ferramentas, ajustar essa tabela ou usar --projeto/--raiz no inventariador. Elas não são necessárias para executar a análise configurável entregue à colaboradora. Os cabeçalhos dessas rotinas identificam essa configuração adicional.

O ambiente geográfico usa NumPy, pandas, GeoPandas, Shapely, Rasterio, PyProj/Pyogrio e SciPy. Os recursos PyQGIS/GRASS devem ser executados no Python instalado com o QGIS. Gerar Word/PDF ou pôster pode exigir outro ambiente com python-docx, ReportLab, pypdf, Pillow, lxml, Microsoft Word e as bibliotecas de autoria de apresentações. Os módulos JavaScript que importam `@oai/artifact-tool` dependem desse pacote, fornecido pelo ambiente de autoria utilizado aqui; não basta instalar Node. Essa dependência não é necessária para recalcular os indicadores geográficos.

Os programas anteriores à edição dos caminhos foram arquivados em `descontinuado/20261114_portabilidade_codigo`, preservando sua localização relativa. A edição dos códigos não executou novamente os modelos de dispersão nem substituiu os mapas publicados ou os textos acadêmicos já entregues.

## Conceitos numéricos que atravessam os códigos

Uma normalização coloca variáveis em escalas comparáveis, sem criar informação. Na transformação logarítmica usa-se t=ln(1+x). No min-max, n=(t−mínimo)/(máximo−mínimo). Na padronização z, z=(t−média)/desvio-padrão. Colunas constantes usam denominador 1, para evitar divisão por zero. Lacuna não é automaticamente zero. A máscara de registros completos define quais observações podem entrar em determinado ajuste.

O índice ponderado do TECO é I=100×Σ(wj×nj)/Σwj. Os pesos exprimem hipóteses de importância relativa, não coeficientes obtidos pela medição de genes. No k-means minimiza-se Σi Σj wj×(nij−centrogrupo,j)². Por isso o código multiplica a matriz normalizada por √peso antes do ajuste. Usar o peso diretamente nessa matriz elevaria a influência ao quadrado. A implementação utiliza scipy.cluster.vq.kmeans2, não uma chamada ao k-means do QGIS ou do scikit-learn. Inicializações repetidas e sementes explícitas reduzem a dependência de uma única solução inicial. [Documentação SciPy](https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.vq.kmeans2.html).

A silhouette de cada observação é s=(b−a)/máximo(a,b), em que a mede distância média ao próprio grupo e b à alternativa mais próxima. A média resume separação interna e pode comparar valores de k na mesma matriz. Não é um p-valor, nem porcentagem de acerto, nem comprovação de que o grupo corresponde a uma fonte real. Classes por quintis são cortes ordenados em uma variável. K-means é um agrupamento multivariado por semelhança. A estabilidade compara resultados depois de variar pesos, suporte ou amostras e não se confunde com nenhum dos dois. [Rousseeuw, 1987](https://doi.org/10.1016/0377-0427%2887%2990125-7).

Moran global relaciona os desvios padronizados de cada local aos de seus vizinhos. Com pesos de vizinhança padronizados por linha, o código usa I=(zᵀWz)/(zᵀz). O Moran local usa Ii=zi×(Wz)i. A significância é obtida por permutação, com p=(1+contagem de resultados tão extremos quanto o observado)/(1+número de permutações). O ajuste Benjamini-Hochberg controla a taxa de falsas descobertas da família declarada. HH e LL significam valor alto/baixo cercado de valores semelhantes; HL/LH são contrastes locais. NS indica ausência de evidência com o critério adotado, não ausência de pressão. ISO identifica isolamento topológico quando previsto. Associação espacial não demonstra uma rota hidrológica ou causal.

Uma junção por chave preserva identificadores e exige unicidade. Uma interseção espacial recorta as geometrias. Na média ponderada por área, x̄=Σ(xj×área de interseçãoj)/Σárea válida. Ratear população por área pressupõe distribuição uniforme dentro da parcela original quando não há uma base dasimétrica melhor. Uma reprojeção transforma coordenadas; atribuir um código EPSG sem transformar o dado não corrige uma coordenada errada. [GeoPandas overlay](https://geopandas.org/en/stable/docs/reference/api/geopandas.overlay.html).

## Ampliação controlada das variáveis

TECO e Congonhas receberam `config/analise_extensivel.json` e `codigo/reproduzir_analise_configuravel.py`. O cenário padrão reproduz a matriz publicada a partir dos produtos consolidados, com saída separada. Para acrescentar uma variável, declarar nome, origem, arquivo, camada/campo, unidade, transformação e agregação; depois informar o peso em cada cenário. A origem pode ser uma coluna da base, tabela, camada vetorial ou raster. Os métodos disponíveis são junção por chave, média ponderada pela área, soma de pontos e média dos pixels válidos. Outro tipo de dado requer acrescentar sua regra na função anexar_variavel. O programa interrompe a execução se houver campo ausente, chave duplicada ou agregação desconhecida.

Na expansão, justificar o sinal da variável e evitar contar duas vezes a mesma pressão. Revisar cobertura, ano, universo e lacunas. Transformações e pesos devem ser fixados antes de comparar cenários. No TECO, a agregação espacial usa os círculos de cálculo, enquanto a geometria final de apresentação continua sendo o suporte sem sobreposição. O exemplo de extensão demonstra uma interface técnica; escolher uma nova variável continua sendo uma decisão metodológica. Um peso não informado assume zero, portanto precisa ser conferido antes de interpretar o cenário.
## Fluxo específico de Congonhas

O processamento distingue inventário, entradas do AERMOD, saídas nativas, indicadores territoriais e apresentação. Há 1.497 receptores na modelagem regional, dos quais 1.008 no suporte municipal usado na análise espacial atual. As 311 zonas continuam como unidade de tradução para a gestão, sem substituir os receptores por médias arbitrárias na leitura dos arquivos. A metodologia de monitoramento elegível e a classificação relativa da modelagem têm finalidades diferentes.

O inventário anual concilia emissões estáticas e horárias. Para fonte área, o fluxo em g/s/m² multiplicado pela área resulta em g/s; a integração no tempo gera massa. Uma tonelada equivale a 10⁶ g. Não se deve multiplicar novamente pela área uma taxa que já é massa por segundo. A alocação territorial distribui a massa pela geometria e confere a soma antes e depois. Vias inventariadas são fontes de emissão, enquanto as vias apenas cartográficas são contexto. Grupos AEX e os subgrupos urbanos podem se sobrepor aos grupos primários e não devem ser somados novamente a ALL.

Os arquivos POST são lidos pelo período, grupo, coordenadas e código temporal. A comparação entre 1 h reconstruído e 24 h nativo é uma auditoria de agregação. A média diária não deve dividir simplesmente por 24 quando as regras de validade do modelo requerem outro denominador. Os módulos registram horas válidas, calmarias e dias marcados pelo modelo, preservando o dia técnico de 2024 fora dos indicadores de 2021-2023. O P98 anual é calculado em cada ano e depois se faz a média dos três P98, no indicador que utiliza essa regra. Máximo de 24 h, P98 e média anual não são sinônimos.

O cenário geral atual da análise conjunta usa seis colunas: máximo de 1 h, máximo de 24 h e média anual trienal para MP10 e MP2,5. Cada coluna passa por log1p e padronização z. Comparam-se Ward e k-means, de k=2 a 6. No k-means são dez inicializações por ajuste, semente 20261105+j e 100 iterações. A solução selecionada tem k=2 e silhouette 0,480665824, com 744 e 264 receptores. A reprodução configurável desta edição retornou os mesmos rótulos dos 1.008 receptores. O agrupamento inicial de quatro indicadores em revisao_espacial_pos_banca.py é histórico e não é a matriz atual de seis colunas.

As cinco faixas espaciais usam ≤P20, >P20 a P40, >P40 a P60, >P60 a P80 e >P80. Elas ordenam severidade relativa no domínio avaliado e não atestam atendimento ao padrão de qualidade do ar. Os quintis anuais de MP2,5 do pôster têm cortes 21,2; 29,4; 43,9 e 72,3 µg/m³. O perfil conjunto, por sua vez, reúne os dois poluentes e três períodos. Por isso não deve ser descrito como apenas um mapa anual de MP2,5.

Os limiares de emissão são associações empíricas. Para cada divisão da concentração, o código procura um corte da densidade de emissão que maximize acurácia balanceada, BA=0,5×(sensibilidade+especificidade), com observações mínimas nos dois lados. A estabilidade é avaliada em blocos espaciais de 2 e 4 km, cinco partições em cada escala. No pôster, o corte associado à faixa superior é 8,50 t/ano/km² e a BA média de teste é 0,767. Esses valores dependem do suporte e da amostra; não definem capacidade de suporte ambiental nem taxa causal que produziria exatamente uma concentração.

Moran identifica associação global/local; o correlograma resume associação por faixas de distância, sem ser necessariamente um mapa. As regiões de gestão combinam severidade relativa, configuração espacial, emissão e cobertura da rede. A região prioritária atual reúne 202 receptores em 14 componentes, totalizando 52,4 km² e intersectando 137 registros de zoneamento. O significado operacional é apoiar controle e investigação, sem equivaler a uma nova categoria legal de saturação.

Nos recortes por direção, os máximos em receptores diferentes podem ocorrer em horas ou dias diferentes. A atribuição recupera cada grupo no mesmo evento em que ALL atinge o máximo daquele receptor. Assim, não se somam máximos independentes de grupos como se fossem simultâneos. O cenário geral usa a meteorologia completa. Os recortes direcionais usam o calendário de horas/dias elegíveis, e a rosa destaca o setor selecionado. As concentrações são recebidas nos receptores e não devem ser confundidas com a emissão gerada dentro de uma zona.

As contribuições das regiões prioritárias são ponderadas pelo suporte definido, com grupos exclusivos. No pôster, Gerdau representa 74,7% e o urbano total 16,5% da contribuição recebida resumida. Isso não é participação na massa total municipal, nem fração de doenças, nem efeito evitável já demonstrado. O grupo urbano total agrega ressuspensão/combustão em vias, ferrovias e núcleos urbanos; seus subgrupos são diagnósticos, não parcelas adicionais.

O controle cartográfico mantém o encarte padronizado. A escala numérica deve ser recalculada ao mudar a dimensão física da figura no pôster; ampliar ou reduzir uma imagem muda a escala impressa. O código de cartografia e seus metadados distinguem escala no arquivo e escala no pôster. Os arquivos de seminários encerrados não foram reescritos nesta tarefa. Foram executados 28 testes de leitura, médias, inventário, alocação territorial, cenário geral e monitoramento, todos aprovados, além da reprodução numérica do agrupamento.

## Catálogo de rotinas

179 arquivos autorais foram documentados. O índice HTML apresenta a ficha integral e o código numerado de cada um. As fichas seguintes preservam os pontos de cálculo, os campos e os trechos citados.

## codigo/aermod_post.py

Aermod post. Aquisição/leitura. A organização passa por _unique_paths, inspect_pos_header, _fmt_elapsed, _fmt_size, iter_pos_chunks, parse_datecode, read_post_24h, summarize_post_24h, _infer_pollutant, discover_post_24h.

**Papel.** Aquisição/leitura. **Fonte inspecionada.** E:\projeto\codigo\aermod_post.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| __future__ | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| standards | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| time | Medição de duração e acompanhamento de tarefas. |
| warnings | Controle de avisos de bibliotecas sem alterar a definição do estimador. |


**Entradas.**

- {path} — chamada path.open, linha 503.
- {meta_path} — chamada meta_path.read_text, linha 547.

**Saídas.**

- paths['meta'].tmp — chamada tmp_meta.write_text, linha 619.

**Campos e chaves lidos.**

- ch: AVE, CONC, DATECODE, GRP, X, Y, _kind, date, hour, year.
- agg: COMPLETENESS, N_DAYS.
- sub: CONC, DATECODE, VALID_YEAR, X, Y, year.
- sub.loc: year.
- valid: ANNUAL_MEAN, P98, year.
- row: ANNUAL_MODEL, P98_MODEL, n_model_years, years_model.
- out: ANNUAL_MODEL, P98_MODEL, X, Y, n_model_years.
- info: ave.
- h: CONC, GRP, N_HOURS, SUM_CONC, X, Y, date.
- daily: date.
- paths: daily, meta.

**Campos e chaves gerados.**

- info: ave, cache_file, cache_load_seconds, cache_used, daily_source, detected_averaging, group, n_receptors, raw_processing_seconds.
- ch: CONC, DATECODE, _kind, date, hour, year.
- agg: COMPLETENESS, EXPECTED_DAYS, VALID_YEAR, year.
- row: ANNUAL_3YR, ANNUAL_MODEL, P98_3YR, P98_MODEL, n_design_years, years_valid.
- a: N_HOURS.
- h: CONC.
- daily: SOURCE_AVERAGING, year.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| _unique_paths(paths) | 61-75 | Chamadas efetivas: set, Path, seen.add, out.append, .casefold, str, pp.resolve, pp.absolute Retorno: out. |
| inspect_pos_header(path: Path) | 78-93 | Chamadas efetivas: str, path.open, range, f.readline, line.upper, re.search, .strip, int Retorno: info. |
| _fmt_elapsed(seconds) | 96-102 | Chamadas efetivas: max, divmod, int Retorno: f'{m:02d}:{s:02d}', f'{h:02d}:{m:02d}:{s:02d}'. |
| _fmt_size(num_bytes) | 105-110 | Chamadas efetivas: float Retorno: f'{n:.1f} {unit}'. |
| iter_pos_chunks(path: Path, chunk_rows=350000, progress=False, progress_label=None) | 113-171 | Chamadas efetivas: Path, time.perf_counter, float, path.exists, getattr, path.open, print, path.stat |
| parse_datecode(series: pd.Series) | 174-183 | Chamadas efetivas: .str.zfill, pd.to_numeric, pd.to_datetime, s.str.slice, dict, .str.replace, series.astype Retorno: (dt, hh). |
| read_post_24h(path: Path, background=0.0) | 186-204 | Chamadas efetivas: inspect_pos_header, iter_pos_chunks, pd.concat, .isin, .copy, parse_datecode, chunks.append, ValueError Retorno: (df, info). |
| summarize_post_24h(path: Path, pollutant: str, background=0.0) | 207-318 | Chamadas efetivas: inspect_pos_header, iter_pos_chunks, finalize_year, pd.concat, int, yearly.groupby, pd.DataFrame, gpd.GeoDataFrame Retorno: (gdf, yearly, info), agg. |
| _infer_pollutant(path: Path) | 321-330 | Chamadas efetivas: re.sub, any, .upper, str Retorno: None, 'PM10'. |
| discover_post_24h(post_dir: Path, pollutant: str) | 333-352 | Chamadas efetivas: .get, post_dir.rglob, Path, p.exists, _infer_pollutant, inspect_pos_header, len, info.get Retorno: None, candidates[0]. |
| discover_group_posts(post_dir: Path, pollutant: str) | 355-363 | Chamadas efetivas: post_dir.rglob, inspect_pos_header, _infer_pollutant, info.get, files.append, str Retorno: files. |
| discover_post_hourly(post_dir: Path, pollutant: str) | 366-381 | Chamadas efetivas: post_dir.rglob, _infer_pollutant, inspect_pos_header, len, _ave_kind, candidates.append, sorted, info.get Retorno: None, candidates[0]. |
| read_post_hourly_for_day(path: Path, target_date, background=0.0, chunk_rows=350000, progress=False) | 384-409 | Chamadas efetivas: .normalize, iter_pos_chunks, pd.concat, .mean, .map, .copy, parse_datecode, pd.to_numeric Retorno: out, pd.DataFrame(columns=['X', 'Y', 'CONC', 'date', 'hour', 'GRP']). |
| _ave_kind(value) | 412-418 | Chamadas efetivas: re.sub, .upper, t.startswith, str Retorno: None, '24H'. |
| read_post_daily(path: Path, background=0.0, chunk_rows=350000, progress=False, progress_label=None) | 421-488 | Chamadas efetivas: inspect_pos_header, set, iter_pos_chunks, .dt.year.astype, dict, .join, .map, detected.update Retorno: (daily, info). |
| _safe_pollutant_name(pollutant, path) | 491-495 | Chamadas efetivas: _infer_pollutant, .replace, str Retorno: inferred or 'GEN', str(pollutant).replace('/', '_'). |
| _pos_fingerprint(path: Path) | 498-513 | Chamadas efetivas: Path, path.stat, int, hashlib.sha256, getattr, path.open, f.read, h.update Retorno: {'size': int(st.st_size), 'mtime_ns': int(st.st_mtime_ns), 'sample_sha256': h.hexdigest()}. |
| _pos_cache_paths(path: Path, pollutant=None) | 516-532 | Chamadas efetivas: Path, _safe_pollutant_name, folder.mkdir, .resolve, re.sub, .get, .lower, .hexdigest Retorno: {'daily': Path(str(base) + '_daily.pkl.gz'), 'meta': Path(str(base) + '_meta.json')}. |
| _cache_signature(background) | 535-540 | Chamadas efetivas: int, float, getattr Retorno: {'cache_version': int(getattr(config, 'POS_CACHE_VERSION', 1)), 'min_valid_hours_day': int(config.MIN_VALID_HOURS_DAY), 'background': float(background)}. |
| _cache_is_valid(path: Path, meta_path: Path, background) | 543-556 | lê dados Retorno: (meta.get('source_fingerprint') == fp, meta), (False, None). |
| read_post_daily_cached(path: Path, background=0.0, pollutant=None, chunk_rows=350000) | 559-631 | grava produtos Retorno: (daily, info), (daily, info). |
| summarize_post_for_pm(path: Path, pollutant: str, background=0.0) | 634-700 | Chamadas efetivas: read_post_daily_cached, daily.groupby, pd.concat, int, yearly.groupby, pd.DataFrame, gpd.GeoDataFrame, .reset_index Retorno: (gdf, yearly, info). |
| _pollutant_folder(post_dir: Path, pollutant: str) | 703-709 | Chamadas efetivas: p.exists, p.is_dir Retorno: post_dir, p. |
| discover_post_main(post_dir: Path, pollutant: str) | 712-747 | Chamadas efetivas: .get, _pollutant_folder, _unique_paths, pool.sort, Path, p.exists, _infer_pollutant, inspect_pos_header Retorno: pool[0][0], None. |
| discover_group_posts_any(post_dir: Path, pollutant: str) | 750-764 | Chamadas efetivas: _pollutant_folder, _unique_paths, _infer_pollutant, inspect_pos_header, sorted, _ave_kind, out.append, folder.glob Retorno: out. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/aermod_post.py, linhas 285-291.

```python
        if len(valid) == n_required:
            row["P98_MODEL"] = valid["P98"].mean()
            row["ANNUAL_MODEL"] = valid["ANNUAL_MEAN"].mean()
        else:
            row["P98_MODEL"] = np.nan
            row["ANNUAL_MODEL"] = np.nan

```

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/aermod_sources.py

Reconstrói geometrias das fontes das planilhas/KML, interpreta o tipo de taxa, associa empreendimentos, aloca massa às zonas e confere conservação. Fluxos superficiais precisam da área emissora para resultar em g/s; fontes com taxa já integrada não recebem uma multiplicação adicional. O código distingue fontes de diferentes tipologias antes da distribuição territorial.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\aermod_sources.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| __future__ | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| io_utils | Módulo autoral local; sua ficha está neste relatório. |
| math | Funções matemáticas escalares. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| shapely | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shapely.ops | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shapely.validation | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- {path} — chamada pd.read_excel, linha 169.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- df: Emission_Rate, Type.
- row: Emission_Rate, Type.
- config.DIRS: emission.
- cand.loc: _empname.
- emp.loc: _empname.
- out.at: urban_subgroup.
- src: emission_rate_native, source_id.
- z: AREA_KM2, EMIS_ALTA_INDUSTRIAL, EMIS_ALTA_URBANA, EMIS_DENS_GS_KM2, EMIS_FORA_MUN_GS, EMIS_HOTSPOT_P95, EMIS_INDUSTRIAL_GS, EMIS_PRESSAO_TIPO, EMIS_TOTAL_GS, EMIS_URBANA_GS, GRUPO_EMISSOR_LOCAL_ID.
- a: emission_gs, group_id.
- local: rank.
- dominant: group_id.
- sources: AEX, group_id.
- aa: emission_gs, group_id.
- z.loc: EMIS_URBANA_GS.
- s: allocated_gs, emission_total_gs.
- meta: expected, name.

**Campos e chaves gerados.**

- df: Emission_Rate, Type.
- out: enterprise.
- emp: _empname, geometry.
- z: AREA_KM2, CONTR_EXTERNA_PCT, EMIS_ALTA_FOCAL, EMIS_ALTA_INDUSTRIAL, EMIS_ALTA_TOTAL, EMIS_ALTA_URBANA, EMIS_CRITERIO, EMIS_DENS_CLASS, EMIS_DENS_GS_KM2, EMIS_DENS_Q33, EMIS_DENS_Q67, EMIS_DENTRO_MUN_GS, EMIS_FORA_MUN_GS, EMIS_HOTSPOT_P95, EMIS_INDUSTRIAL_GS, EMIS_PRESSAO_ALTA, EMIS_PRESSAO_SCORE, EMIS_PRESSAO_TIPO, EMIS_THR_HOTSPOT_P95, EMIS_THR_INDUSTRIAL_GS, EMIS_THR_TOTAL_GS, EMIS_THR_URBANA_GS, EMIS_TOTAL_GS, EMIS_URBANA_GS, GRUPO_EMISSOR_LOCAL, GRUPO_EMISSOR_LOCAL_ID.
- local: rank.
- aa: _urban_road, emission_gs.
- s: allocated_gs, allocated_pct, unallocated_gs.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| _kml_name_column(gdf) | 66-76 | Chamadas efetivas: .lower, columns.get, .str.strip, .any, str, .astype, values.ne, .dropna Retorno: None, c. |
| _clean_geometry(geom) | 79-110 | Chamadas efetivas: force_2d, collect, make_valid, geom.buffer, unary_union, parts.append Retorno: geom, geom. |
| _geometry_lookup_keys(value) | 113-121 | Chamadas efetivas: normalize_name, list, key.endswith, dict.fromkeys, keys.append, len Retorno: list(dict.fromkeys((k for k in keys if k))), []. |
| load_source_geometries_from_files(base_dir: Path) | 124-154 | Chamadas efetivas: getattr, set, files.extend, sorted, f.exists, dedup.append, seen.add, read_vector Retorno: lookup. |
| detect_lakes_header(path: Path) | 157-164 | lê dados Retorno: int(idx). |
| read_lakes_sources(path: Path) | 167-179 | lê dados Retorno: df. |
| _coord_pairs(row) | 182-194 | Chamadas efetivas: range, int, float, math.isfinite, coords.append, row.get Retorno: coords. |
| source_geometry(row) | 197-263 | Chamadas efetivas: _coord_pairs, Point, .buffer, box, LineString, len, pd.notna, float Retorno: Point(coords[0]), None. |
| _row_width_m(row) | 266-271 | Chamadas efetivas: pd.notna, float, pd.to_numeric, pd.Series, row.get Retorno: np.nan, float(v). |
| _source_measure(row, geom) | 274-285 | Chamadas efetivas: .upper, float, _row_width_m, str, np.isfinite, row.get Retorno: (area, length), (np.nan, np.nan). |
| total_emission_gs(row, geom) | 288-308 | Chamadas efetivas: float, .upper, _source_measure, str, np.isfinite Retorno: (rate, 'taxa nativa - revisar', 'desconhecida', area_m2, length_m), (np.nan, 'área geométrica ausente - total não calculado', 'g/s/m2', area_m2, length_m). |
| build_source_gdf(path: Path, pollutant: str) | 311-357 | Chamadas efetivas: read_lakes_sources, load_source_geometries_from_files, df.iterrows, gpd.GeoDataFrame, str, normalize_name, geom_lookup.get, _clean_geometry Retorno: gpd.GeoDataFrame(records, geometry='geometry', crs=config.CRS_PROJECT). |
| _enterprise_name_col(emp) | 360-366 | Chamadas efetivas: .lower, str Retorno: None, lower[c]. |
| associate_enterprises(sources, enterprises, nearest_tolerance_m=250.0) | 369-410 | Chamadas efetivas: sources.copy, .copy, emp.geometry.map, _enterprise_name_col, out.iterrows, .astype, _clean_geometry, enterprises.to_crs Retorno: out, out. |
| allocate_emissions_to_zones(sources, zones) | 413-609 | Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. Retorno: (z, a), 'alta'. |
| emission_mass_balance_audit(sources, allocations) | 612-623 | Chamadas efetivas: .copy, .rename, s.merge, .fillna, pd.to_numeric, .replace, .sum, allocations.groupby Retorno: s. |
| group_count_audit(sources) | 626-644 | Chamadas efetivas: GROUPS.items, pd.DataFrame, int, rows.append, meta.get, .sum, .fillna, sources.get Retorno: pd.DataFrame(rows). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/aermod_sources.py, linhas 511-517.

```python
    pos = dens[dens > 0]
    q33 = float(pos.quantile(1/3)) if not pos.empty else np.nan
    q67 = float(pos.quantile(2/3)) if not pos.empty else np.nan
    def _dens_class(v):
        if pd.isna(v) or v <= 0:
            return "sem_emissao"
        if pd.notna(q33) and v <= q33:
```

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

**Cálculos a observar nesta rotina.**

- quantile: Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/ajustar_blocos_figuras_docx.py

Mantém legenda, imagem e fonte juntas e evita folhas vazias entre pranchas.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\ajustar_blocos_figuras_docx.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| docx | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

- E:/projeto/output/09_projeto_dissertacao/seminarios_02/Projeto_Ricardo-Queiroz_{version}.docx — chamada d.save, linha 56.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| layout(d) | 28-50 | Chamadas efetivas: list, enumerate, re.match, p._p.xpath, next, after.text.startswith, following.text.startswith, .remove Retorno: d. |
| run() | 53-56 | grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/ajustar_blocos_figuras_docx.py, linhas 28-36.

```python
def layout(d):
    ps=list(d.paragraphs)
    for i,p in enumerate(ps):
        if re.match(r'Figura [A-Z]\s*\d+\s*[–-]',p.text):
            p.paragraph_format.keep_with_next=True
            p.paragraph_format.keep_together=True
            for after in ps[i+1:]:
                if after.text.startswith('Fonte:'):
                    after.paragraph_format.keep_together=True
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/alocacao_territorial_emissoes.py

Distribui massas no suporte territorial e verifica a conservação. Diferencia fonte de emissão e concentração recebida, evitando dividir indevidamente fluxo por uma área adicional.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\alocacao_territorial_emissoes.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| aermod_sources | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| inventario_anual | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shapely.ops | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/config.DIRS['out']/14_auditoria_entradas/revalidacao_final/validacao_final.json — chamada validation.read_text, linha 66.
- E:/projeto/entrada_aermod/{name} — chamada path.read_bytes, linha 68.
- E:/projeto/config.DIRS['out']/13_rateio_emissoes/Resumo_zonas.csv — chamada pd.read_csv, linha 166.
- E:/projeto/config.DIRS['out']/11_integracao/zoneamento_integrado.gpkg — chamada gpd.read_file, linha 185.
- E:/projeto/config.DIRS['out']/14_auditoria_entradas/revalidacao_final/Massas_fontes_2021_2023.csv — chamada pd.read_csv, linha 195.
- E:/projeto/config.DIRS['out']/14_auditoria_entradas/revalidacao_final/fontes_correntes.json — chamada .read_text, linha 196.

**Saídas.**

- E:/projeto/config.DIRS['out']/13_rateio_emissoes/{name}.csv — chamada table.to_csv, linha 272.
- Argumento fornecido pelo chamador — chamada table.to_json, linha 274.
- E:/projeto/config.DIRS['out']/13_rateio_emissoes/tabelas_planilha.json — chamada .write_text, linha 275.
- E:/projeto/config.DIRS['out']/13_rateio_emissoes/auditoria_rateio.json — chamada .write_text, linha 283.

**Campos e chaves lidos.**

- config.DIRS: out.
- evidence: arquivos.
- source: source_type.
- table: poluente.
- r: id, poluente.
- masses: poluente.
- rec: inventario_ids, status.
- zones.loc: nome.
- a: zona.
- sub.loc: massa_zona_t_ano.
- tables: Balanco_fontes, Resumo_zonas.
- report: classes.

**Campos e chaves gerados.**

- report: classes.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| refined_sources(pol, name) | 62-72 | lê dados Retorno: (raw, sources). |
| geometry_for_allocation(source, raw) | 75-96 | Chamadas efetivas: _coord_pairs, _clean_geometry, unary_union, raw.get, len, LineString, pd.notna, source_geometry Retorno: (None, 'projeção horizontal ausente'), (Point(coords[0]), 'ponto') if coords else (None, 'ponto ausente'). |
| partition(geom, zones, basis) | 99-154 | Chamadas efetivas: zones.sindex.query, measure, enumerate, unary_union, GeometryCollection, abs, sum, list Retorno: (result, outside, ambiguous, total), (result, outside / total, ambiguous / total, total). |
| emission_class(value, minor) | 157-161 | Chamadas efetivas: np.isclose Retorno: 'Sem massa quantificada', 'Alta (>100 t/ano)'. |
| apply_territorial_totals(zones) | 164-180 | lê dados Retorno: z. |
| run() | 183-285 | lê dados; grava produtos Retorno: tables. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/alocacao_territorial_emissoes.py, linhas 130-136.

```python
        result=[(z,v/total,v) for z,v in allocated.items()]
        assert abs(sum(v for _,v,_ in result)+(outside+ambiguous)/total-1)<1e-6
        return result,outside/total,ambiguous/total,total
    positions=zones.sindex.query(geom,predicate='intersects')
    hits=[(zones.index[i],geom.intersection(zones.geometry.iloc[i])) for i in positions]
    if basis=='ponto':
        if len(hits)==1:return [(hits[0][0],1.,1.)],0.,0.,1.
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/alocacao_territorial_emissoes.py, linhas 152-158.

```python
    ambiguous=measure(conflict)/total
    assert abs(sum(f for _,f,_ in result)+outside+ambiguous-1)<1e-6, (basis,total,sum(f for _,f,_ in result),outside,ambiguous)
    return result,outside,ambiguous,total

# Emission class
def emission_class(value,minor):
    if value>100 and not np.isclose(value,100,atol=1e-10,rtol=0):return 'Alta (>100 t/ano)'
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/analisar_espacial_direcoes.py

Aplica os mesmos testes aos envelopes por direção e ao cenário geral, recupera contribuições no evento ALL de cada receptor, compara Ward/k-means, Moran, correlogramas, limiares e regiões de gestão.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\analisar_espacial_direcoes.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| complementar_quintis_gestao | Módulo autoral local; sua ficha está neste relatório. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| medias_horarias_verificadas | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| out_aermod_reader | Módulo autoral local; sua ficha está neste relatório. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| post_amostragem | Módulo autoral local; sua ficha está neste relatório. |
| revisao_espacial_pos_banca | Módulo autoral local; sua ficha está neste relatório. |
| scipy | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.cluster.hierarchy | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.cluster.vq | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.sparse.csgraph | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.spatial | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/eventos_{pol}_{period}_manifesto.json — chamada signature.read_text, linha 113.
- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/eventos_{pol}_{period}.npz — chamada np.load, linha 114.
- E:/projeto/output/16_revisao_pos_banca/vento/{pol}_envelopes_{'horarios' if period == '1h' else 'diarios_persistentes'}.csv — chamada pd.read_csv, linha 115.
- E:/projeto/output/16_revisao_pos_banca/vento/'calendario_vento_horario.csv' if period == '1h' else 'dias_direcao_persistente.csv' — chamada pd.read_csv, linha 136.
- E:/projeto/output/16_revisao_pos_banca/celulas_analise.gpkg — chamada gpd.read_file, linha 202.
- E:/projeto/output/16_revisao_pos_banca/zoneamento_pos_banca.gpkg — chamada gpd.read_file, linha 203.
- E:/projeto/output/16_revisao_pos_banca/vinculo_celula_zona.csv — chamada pd.read_csv, linha 203.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/perfis_normalizados_grupos_estacoes.csv — chamada pd.read_csv, linha 217.
- E:/projeto/output/15_auditoria_metodologica/revisao_cientifica/vinculos_estacoes_receptores.csv — chamada pd.read_csv, linha 218.
- E:/projeto/output/11_integracao/nova_modelagem/estacoes_trienio_comum.csv — chamada pd.read_csv, linha 219.
- {p} — chamada load, linha 226.

**Saídas.**

- {path} — chamada path.write_text, linha 100.
- Path(output) if output is not None else globals()['OUT']/comparacao_agrupamentos.csv — chamada .to_csv, linha 232.
- Path(output) if output is not None else globals()['OUT']/{pol}_{period}_receptores.csv — chamada table.to_csv, linha 327.
- Path(output) if output is not None else globals()['OUT']/correlogramas.csv — chamada .to_csv, linha 329.
- Path(output) if output is not None else globals()['OUT']/sensibilidade_espacial.csv — chamada .to_csv, linha 329.
- Path(output) if output is not None else globals()['OUT']/limiares_cinco_faixas.csv — chamada .to_csv, linha 330.
- Path(output) if output is not None else globals()['OUT']/limiares_regressao_complementar.csv — chamada .to_csv, linha 330.
- Path(output) if output is not None else globals()['OUT']/distribuicoes_emissao_por_faixa.csv — chamada .to_csv, linha 331.
- Path(output) if output is not None else globals()['OUT']/'regioes_gerais' if general else 'regioes_direcionais'.gpkg — chamada region_frame.to_file, linha 335.
- Path(output) if output is not None else globals()['OUT']/'regioes_gerais' if general else 'regioes_direcionais'.csv — chamada .to_csv, linha 335.
- Path(output) if output is not None else globals()['OUT']/ABC_contribuicoes_regioes.csv — chamada .to_csv, linha 336.
- Path(output) if output is not None else globals()['OUT']/regioes_zoneamento.csv — chamada .to_csv, linha 336.
- Mais 2 referências na ficha HTML e no inventário JSON.

**Campos e chaves lidos.**

- v: kind.
- cells: X, Y, geometry, receptor_id.
- raw: direction.
- paths: ALL.
- calendar: CODE, day.
- r: silhouette.
- best: k, method.
- labels: ward.
- eligible: n_design_years, pollutant.
- sg: station_id.
- d: codes, concentrations, counts, group_values, groups, yearly.
- sg.loc: station_id.
- z: zone_index.
- spatial: network_priority.

**Campos e chaves gerados.**

- calendar: native_code.
- f: best_cluster, dominant_group, emission_band, emission_band_basis, emission_density, five_emission_bands_identifiable, management, mass_tpy, matrix, network_priority, ward4.
- spatial: network_priority.
- summary: clustering_joint_1h_24h_anual.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| dump(path, obj) | 99-100 | grava produtos |
| peak_data(pol, period, cells) | 103-152 | lê dados; grava produtos Retorno: result, {k: f[k] for k in f.files}. |
| partition(frame, field) | 155-165 | Identifica componentes conectados de uma rede de vizinhança. Une regiões espacialmente conectadas; não estima transporte físico. |
| silhouette_fast(dm, labels) | 168-175 | Chamadas efetivas: np.unique, np.stack, np.array, np.searchsorted, means.min, np.maximum, np.divide, float Retorno: float(score.mean()). |
| clustering(features) | 178-190 | Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original.; Agrupamento hierárquico. Com method=ward, as fusões procuram o menor aumento da dispersão interna.; Ajusta centroides pelo k-means. A matriz de entrada, a inicialização ++, a semente e as repetições determinam a solução reproduzida. Retorno: (records, labels[best['method'], best['k']], labels['ward', 4], best). |
| run(*, directions=None, periods=None, output=None, loader=None) | 193-343 | lê dados; grava produtos; Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original.; Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/analisar_espacial_direcoes.py, linhas 162-168.

```python
        adjacency=sparse.coo_matrix((np.ones(e.shape[1]),e),shape=(len(sub),len(sub)))
        n,labels=connected_components(adjacency,directed=False)
        order=sorted(range(n),key=lambda k:(sub[labels==k].geometry.union_all().centroid.x,sub[labels==k].geometry.union_all().centroid.y))
        for j,k in enumerate(order,1):yield value,j,sub[labels==k]

# Silhouette fast
def silhouette_fast(dm,labels):
```

Identifica componentes conectados de uma rede de vizinhança. Une regiões espacialmente conectadas; não estima transporte físico.

Trecho de codigo/analisar_espacial_direcoes.py, linhas 178-184.

```python
def clustering(features):
    x=np.log1p(features);scale=x.std(0);x=(x-x.mean(0))/np.where(scale>0,scale,1);dm=distance.cdist(x,x);tree=linkage(x,method='ward');records=[];labels={}
    for method in ['ward','kmeans']:
        for k in range(2,7):
            if method=='ward':lab=fcluster(tree,k,criterion='maxclust')-1
            else:
                fits=[kmeans2(x,k,minit='++',iter=100,rng=np.random.default_rng(SEED+j)) for j in range(10)]
```

Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original.

Desvio-padrão. Na padronização z, coloca colunas em escala comparável; conferir ddof no trecho.

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

Matriz de distâncias entre observações. É usada no agrupamento, na silhouette ou na comparação entre centroides.

Agrupamento hierárquico. Com method=ward, as fusões procuram o menor aumento da dispersão interna.

Transforma a árvore hierárquica em rótulos de grupos segundo o critério fornecido.

Ajusta centroides pelo k-means. A matriz de entrada, a inicialização ++, a semente e as repetições determinam a solução reproduzida.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- connected_components: Identifica componentes conectados de uma rede de vizinhança. Une regiões espacialmente conectadas; não estima transporte físico.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- log1p: Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original.
- std: Desvio-padrão. Na padronização z, coloca colunas em escala comparável; conferir ddof no trecho.
- cdist: Matriz de distâncias entre observações. É usada no agrupamento, na silhouette ou na comparação entre centroides.
- linkage: Agrupamento hierárquico. Com method=ward, as fusões procuram o menor aumento da dispersão interna.
- fcluster: Transforma a árvore hierárquica em rótulos de grupos segundo o critério fornecido.
- kmeans2: Ajusta centroides pelo k-means. A matriz de entrada, a inicialização ++, a semente e as repetições determinam a solução reproduzida.
- quantile: Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.
- average: Média com ou sem pesos. As unidades do resultado são as da variável antes de eventual normalização.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/analises_direcionais_pos_banca.py

Envelopes condicionados ao vento real da SFC, sem nova simulação AERMOD.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\analises_direcionais_pos_banca.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| medias_horarias_verificadas | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| out_aermod_reader | Módulo autoral local; sua ficha está neste relatório. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- met['sfc']['path'] — chamada pd.read_csv, linha 61.
- E:/projeto/wrf/AERMET-3Y.{ext} — chamada p.read_bytes, linha 68.
- met[ext.lower()]['path'] — chamada q.read_bytes, linha 68.
- E:/projeto/output/16_revisao_pos_banca/vento/{pol}_manifesto.json — chamada stamp.read_text, linha 87.
- E:/projeto/out-aermod/{folder}/01_GALL.POS — chamada pd.read_csv, linha 92.
- E:/projeto/output/11_integracao/nova_modelagem/{pol}_medias_diarias_1h.csv.gz — chamada pd.read_csv, linha 115.

**Saídas.**

- E:/projeto/output/16_revisao_pos_banca/vento/calendario_vento_horario.csv — chamada cal.to_csv, linha 72.
- E:/projeto/output/16_revisao_pos_banca/vento/dias_direcao_persistente.csv — chamada daily.to_csv, linha 81.
- E:/projeto/output/16_revisao_pos_banca/vento/frequencia_vento.csv — chamada freq.to_csv, linha 82.
- E:/projeto/output/16_revisao_pos_banca/vento/{pol}_envelopes_horarios.csv — chamada result.to_csv, linha 111.
- E:/projeto/output/16_revisao_pos_banca/vento/{pol}_envelopes_diarios_persistentes.csv — chamada selected.to_csv, linha 116.
- E:/projeto/output/16_revisao_pos_banca/vento/{pol}_manifesto.json — chamada stamp.write_text, linha 118.

**Campos e chaves lidos.**

- met: sfc.
- sfc: CODE.
- chunk: X, Y.
- metidx.loc: direction_idx.
- daily: day, direction_idx, eligible.
- summary: hours_by_direction.

**Campos e chaves gerados.**

- sfc: CODE.
- cal: direction, direction_idx.
- freq: percent_total.
- selected: direction.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| sector8(degrees) | 54-56 | Chamadas efetivas: np.asarray, np.full, .astype, np.isfinite, np.floor Retorno: out. |
| run() | 59-120 | lê dados; grava produtos Retorno: summaries. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/analises_direcionais_pos_banca.py, linhas 76-82.

```python
        if n:
            theta=np.deg2rad(v.wind_from_deg);u=np.mean(np.sin(theta));w=np.mean(np.cos(theta));r=float(np.hypot(u,w));deg=float(np.rad2deg(np.arctan2(u,w))%360);idx=int(sector8([deg])[0]);fraction=float(v.direction_idx.eq(idx).mean())
        else:r=0;deg=np.nan;idx=-1;fraction=0
        eligible=n>=18 and r>=.5 and fraction>=.5
        dayrows.append({'day':day,'valid_hours':n,'resultant':r,'mean_from_deg':deg,'direction_idx':idx if eligible else -1,'dominant_fraction':fraction,'eligible':eligible})
    daily=pd.DataFrame(dayrows);daily.to_csv(out/'dias_direcao_persistente.csv',index=False)
    freq=cal.groupby('direction',sort=False).agg(hours=('CODE','size'),mean_speed=('wind_speed','mean')).reset_index();freq['percent_total']=100*freq.hours/len(cal);freq.to_csv(out/'frequencia_vento.csv',index=False)
```

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/atlas_cenarios.py

Entrada compatível para gerar cenários no encarte comum.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\atlas_cenarios.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| atlas_encarte_padrao | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/atlas_cenarios.py, linhas 8-16.

```python
"""Entrada compatível para gerar cenários no encarte comum."""
# INÍCIO DOS CAMINHOS PORTÁTEIS
import sys as _cp_sys
from pathlib import Path as _cp_Path
_cp_file = _cp_Path(globals().get('__file__', _cp_Path.cwd() / 'codigo' / 'script.py')).resolve()
for _cp_parent in [_cp_file.parent, *_cp_file.parents]:
    _cp_code = _cp_parent if (_cp_parent / 'caminhos_congonhas.py').is_file() else _cp_parent / 'codigo'
    if (_cp_code / 'caminhos_congonhas.py').is_file():
        if str(_cp_code) not in _cp_sys.path: _cp_sys.path.insert(0, str(_cp_code))
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/atlas_encarte_padrao.py

Cenários de dispersão no encarte comum dos apêndices.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\atlas_encarte_padrao.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| cartografia_apendices | Módulo autoral local; sua ficha está neste relatório. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| out_aermod_reader | Módulo autoral local; sua ficha está neste relatório. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| pyproj | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| standards | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/zoneamento_nova_modelagem.gpkg — chamada gpd.read_file, linha 59.
- E:/projeto/config.DIRS['out']/11_integracao/apendices/resumo_figuras.json — chamada .read_text, linha 62.
- {f} — chamada pd.read_csv, linha 70.

**Saídas.**

- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/manifesto_PLT.csv — chamada .to_csv, linha 119.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/atlas_manifest.json — chamada .write_text, linha 120.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/legendas_textuais_cenarios.json — chamada .write_text, linha 121.

**Campos e chaves lidos.**

- config.DIRS: out, post.
- h: group, has_data, period.
- a: CONC, X, Y.
- selected: ANNUAL.
- tables: ALL.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| color_scale(limits, maximum, display_cap=None) | 48-55 | Chamadas efetivas: max, float, np.array, FuncNorm, LinearSegmentedColormap.from_list, np.floor, breaks.tolist, np.log10 Retorno: (cmap, norm, breaks.tolist()). |
| run() | 58-121 | lê dados; grava produtos; Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/atlas_encarte_padrao.py, linhas 87-93.

```python
                actual_max=max(tables[g,period].CONC.max() for g in groups)
                cap=max(tables[g,period].CONC.quantile(.98) for g in groups)
                cmap,norm,ticks=color_scale(limits,actual_max,min(cap,actual_max*.9))
                surfaces=[]
                for group in groups:
                    a=tables[group,period];x,y=transformer.transform(a.X.to_numpy(),a.Y.to_numpy())
                    surfaces.append(dict(x=x,y=y,values=a.CONC.to_numpy(),limits=limits,colors=COLORS,cmap=cmap,norm=norm,ticks=ticks,actual_max=actual_max))
```

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

Trecho de codigo/atlas_encarte_padrao.py, linhas 111-117.

```python
            limits=[STANDARDS[pol][s]['24H' if period=='24H' else 'ANNUAL'] for s in ['PF','PI4','PI3','PI2']]
            cmap,norm,ticks=color_scale(limits,a.CONC.max(),min(a.CONC.quantile(.98),a.CONC.max()*.9))
            pair.append(dict(x=x,y=y,values=a.CONC.to_numpy(),limits=limits,colors=COLORS,cmap=cmap,norm=norm,ticks=ticks,actual_max=float(a.CONC.max())))
        name=pol+'_ALL_24h_anual';title='MP₁₀' if pol=='PM10' else 'MP₂,₅'
        cart.render(zones,municipality,['24H','ANNUAL'],'dispersao',[title+' · máxima de 24 horas',title+' · máxima anual'],'',extent,surfaces=pair,filename=name)
        products.append(dict(name=name,pol=pol,period='24H_ANNUAL',category='ALL'))
        captions.append(dict(arquivo=name,nota_para_legenda_textual='Envelopes dos maiores valores por receptor em 2021–2023: 24 horas e anual. Não correspondem necessariamente a um episódio simultâneo. Interpolação cartográfica suave, limitada ao domínio amostrado e aos valores extremos observados; não altera as concentrações nos receptores usadas na classificação. Barras individuais com escala não linear e patamares PF, PI-4, PI-3 e PI-2. Contribuição primária sem fundo.'))
```

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

**Cálculos a observar nesta rotina.**

- quantile: Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/atualizar_emissoes_integradas.py

Atualiza apenas as emissões, preservando monitoramento e modelagem existentes.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\atualizar_emissoes_integradas.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| aermod_sources | Módulo autoral local; sua ficha está neste relatório. |
| alocacao_territorial_emissoes | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| inventario_anual | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| publicar_rateio_refinado | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| validar_massas_entrada | Módulo autoral local; sua ficha está neste relatório. |
| vector_portable | Módulo autoral local; sua ficha está neste relatório. |


**Entradas.**

- {out}/resumo_execucao.json — chamada summary_path.read_text, linha 47.

**Saídas.**

- {out}/resumo_execucao.json — chamada summary_path.write_text, linha 57.
- {out}/CONFERENCIA_EMISSOES.md — chamada .write_text, linha 78.

**Campos e chaves lidos.**

- r: classes, high_groups, inventory_rows_pending, unidentified_groups.
- row: emission_tpy, group_id, zone_index.

**Campos e chaves gerados.**

- summary: annualization, emission_revision, emission_revision_note.
- previous: emission_classes, inventory_rows_pending, source_association_validated, sources_unidentified.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 33-41 | Chamadas efetivas: validate, allocate, publish Retorno: tables. |
| write_report(out, report) | 44-79 | lê dados; grava produtos Retorno: report. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/atualizar_emissoes_integradas.py, linhas 33-41.

```python
def run():

    from validar_massas_entrada import run as validate
    from alocacao_territorial_emissoes import run as allocate
    from publicar_rateio_refinado import run as publish
    validate()
    tables=allocate()
    publish()
    return tables
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/atualizar_figuras_seminario.py

Substitui as figuras correntes no DOCX preservando o texto revisado.

**Papel.** Histórico editorial: entrega de seminários encerrada. **Fonte inspecionada.** E:\projeto\codigo\atualizar_figuras_seminario.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| PIL | Inspeção, composição ou ajuste de imagens pela biblioteca Pillow. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| docx | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.shared | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/11_integracao/nova_modelagem/figuras_seminario_manifesto.json — chamada .read_text, linha 42.
- E:/projeto/output/11_integracao/nova_modelagem/legendas_textuais_cenarios.json — chamada .read_text, linha 43.
- E:/projeto/output/11_integracao/nova_modelagem/identificacao_estacoes_figura_B1.csv — chamada .read_text, linha 44.
- f['arquivo'] — chamada path.read_bytes, linha 81.
- f['arquivo'] — chamada Image.open, linha 82.

**Saídas.**

- E:/projeto/output/09_projeto_dissertacao/seminarios_02/Projeto_Ricardo-Queiroz_Entrega.docx — chamada d.save, linha 90.
- E:/projeto/output/09_projeto_dissertacao/seminarios_02/Lista_Figuras_Apendices.md — chamada .write_text, linha 96.
- E:/projeto/output/11_integracao/nova_modelagem/figuras_seminario_manifesto.json — chamada .write_text, linha 97.

**Campos e chaves lidos.**

- x: arquivo, codigo, descricao, nota_para_legenda_textual, titulo.
- f: arquivo, titulo.

**Campos e chaves gerados.**

- f: descricao.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 38-98 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/atualizar_figuras_seminario.py, linhas 38-46.

```python
def run():
    root=config.BASE;out=root/'output/11_integracao/nova_modelagem'
    target=root/'output/09_projeto_dissertacao/seminarios_02/Projeto_Ricardo-Queiroz_Entrega.docx'
    source=target if target.exists() else root/'descontinuado/2026-10-29_leitura_entrega/output/09_projeto_dissertacao/seminarios_02/Projeto_Ricardo-Queiroz.docx'
    d=Document(source);entries=json.loads((out/'figuras_seminario_manifesto.json').read_text(encoding='utf8'))
    info={x['codigo']:x for x in entries};notes={x['arquivo']:x['nota_para_legenda_textual'] for x in json.loads((out/'legendas_textuais_cenarios.json').read_text(encoding='utf8'))}
    station_rows=(out/'identificacao_estacoes_figura_B1.csv').read_text(encoding='utf8').splitlines()[1:]
    station_text='; '.join(line.split(',')[0]+' – '+line.split(',')[-1] for line in station_rows)
    changed=[];paras=list(d.paragraphs)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. Rotina histórica: conferir pré-condições e versão de dados antes de qualquer execução.

## codigo/atualizar_nova_modelagem_completa.py

Atualiza tabelas, cartografia e painel a partir das saídas em out-aermod.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\atualizar_nova_modelagem_completa.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| alocacao_territorial_emissoes | Módulo autoral local; sua ficha está neste relatório. |
| atlas_encarte_padrao | Módulo autoral local; sua ficha está neste relatório. |
| atualizar_resultados_aermod | Módulo autoral local; sua ficha está neste relatório. |
| auditar_emi_execucao_252 | Módulo autoral local; sua ficha está neste relatório. |
| auditar_series_e_gravidade | Módulo autoral local; sua ficha está neste relatório. |
| auditoria_exaustiva_estacoes | Módulo autoral local; sua ficha está neste relatório. |
| auditoria_metodologica_integrada | Módulo autoral local; sua ficha está neste relatório. |
| avaliar_robustez_cientifica | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| complementar_periodo_comum | Módulo autoral local; sua ficha está neste relatório. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| consolidar_atributos_evidencia | Módulo autoral local; sua ficha está neste relatório. |
| consolidar_populacao_atual | Módulo autoral local; sua ficha está neste relatório. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| densidade_hectare | Módulo autoral local; sua ficha está neste relatório. |
| gerar_complementos_revisao | Módulo autoral local; sua ficha está neste relatório. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| integrar_monitoramento_atual | Módulo autoral local; sua ficha está neste relatório. |
| integrar_periodo_comum | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| medias_horarias_verificadas | Módulo autoral local; sua ficha está neste relatório. |
| painel_nova_modelagem | Módulo autoral local; sua ficha está neste relatório. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| regenerar_mapas_atuais | Módulo autoral local; sua ficha está neste relatório. |
| revisao_trienal_grupos | Módulo autoral local; sua ficha está neste relatório. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sincronizar_rateio_corrente | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| validar_massas_entrada | Módulo autoral local; sua ficha está neste relatório. |


**Entradas.**

- E:/projeto/descontinuado/datetime.now().strftime('%Y-%m-%d_%H%M%S_regeneracao')/p.relative_to(config.BASE) — chamada q.read_bytes, linha 62.

**Saídas.**

- E:/projeto/descontinuado/datetime.now().strftime('%Y-%m-%d_%H%M%S_regeneracao')/manifesto.json — chamada .write_text, linha 64.

**Campos e chaves lidos.**

- config.DIRS: out.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| preservar_correntes() | 49-64 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/atualizar_nova_modelagem_completa.py, linhas 49-57.

```python
def preservar_correntes():
    """Preserva o conteúdo anterior dos resultados gerados que serão substituídos."""
    from datetime import datetime
    import hashlib,json,shutil
    import config
    folder=config.DIRS['out']/'11_integracao/nova_modelagem'
    archive=config.BASE/'descontinuado'/datetime.now().strftime('%Y-%m-%d_%H%M%S_regeneracao')
    records=[]
    for p in folder.iterdir():
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/atualizar_previas_paleta.py

Atualiza somente prévias de concentração, sem editar a interface ou o catálogo.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\atualizar_previas_paleta.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| PIL | Inspeção, composição ou ajuste de imagens pela biblioteca Pillow. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| empacotar_visualizador_privado | Módulo autoral local; sua ficha está neste relatório. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/dissertacao/visualizador/catalogo.json — chamada .read_text, linha 45.
- E:/projeto/output/16_revisao_pos_banca/cenario_geral/figuras/Geral_{item['period']}_Concentracoes.png — chamada Image.open, linha 52.
- source.with_suffix('.svg') — chamada .read_text, linha 55.
- E:/projeto/output/16_revisao_pos_banca/visualizador/item['src'] — chamada target.read_bytes, linha 58.
- E:/projeto/temp/paleta_concentracoes_auditoria_preliminar.json — chamada .read_text, linha 66.

**Saídas.**

- E:/projeto/output/16_revisao_pos_banca/visualizador/item['src'] — chamada im.save, linha 57.
- E:/projeto/descontinuado/datetime.datetime.now().strftime('%Y%m%d_%H%M%S')_previas_paleta/manifesto.json — chamada .write_text, linha 65.
- E:/projeto/output/16_revisao_pos_banca/Auditoria_paleta_concentracoes.json — chamada .write_text, linha 71.

**Campos e chaves lidos.**

- data: catalog.
- item: direction, mode, period, product, src.
- r: arquivo, dimensoes_iguais, encartes_e_barras_iguais, todas_geometrias_vetoriais_iguais.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 38-72 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/atualizar_previas_paleta.py, linhas 38-46.

```python
def run():
    Image.MAX_IMAGE_PIXELS=400_000_000
    archive=R/'descontinuado'/(datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+'_previas_paleta');rows=[]
    def preserve(p):
        if p.is_file():
            dest=archive/p.relative_to(R);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
            rows.append(dict(origem=str(p),destino=str(dest),motivo='Previa ou pacote substituido apos ajuste exclusivo da paleta'))
    data=json.loads((REPO/'catalogo.json').read_text(encoding='utf8'));updated=[]
    for item in data['catalog']:
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/atualizar_produtos_cartograficos.py

Entrada única; execução interrompida em erro, sem rodar AERMOD.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\atualizar_produtos_cartograficos.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| alocacao_territorial_emissoes | Módulo autoral local; sua ficha está neste relatório. |
| argparse | Parâmetros fornecidos ao iniciar o programa. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| mapas_apendices | Módulo autoral local; sua ficha está neste relatório. |
| mapas_complementares | Módulo autoral local; sua ficha está neste relatório. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| subprocess | Chamada de outros programas e verificação de seus resultados de execução. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves gerados.**

- os.environ: TEMP, TMP.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| main() | 31-45 | Chamadas efetivas: argparse.ArgumentParser, parser.add_argument, parser.parse_args, str, rateio, subprocess.run, complementos, Path.home |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/atualizar_produtos_cartograficos.py, linhas 9-17.

```python
"""Entrada única; execução interrompida em erro, sem rodar AERMOD.

Padrão: rateio + complementos + revisão de C1 usando indicadores existentes.
--completo: recalcula também os demais apêndices a partir das bases disponíveis.
"""
# INÍCIO DOS CAMINHOS PORTÁTEIS
import sys as _cp_sys
from pathlib import Path as _cp_Path
_cp_file = _cp_Path(globals().get('__file__', _cp_Path.cwd() / 'codigo' / 'script.py')).resolve()
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/atualizar_resultados_aermod.py

Atualiza diagnóstico da nova execução sem somar grupos sobrepostos.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\atualizar_resultados_aermod.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| io_utils | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| methodology_rules | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| out_aermod_reader | Módulo autoral local; sua ficha está neste relatório. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| standards | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| vector_portable | Módulo autoral local; sua ficha está neste relatório. |


**Entradas.**

- E:/projeto/config.DIRS['grade_generated']/grade_receptores_adaptativa.gpkg [camada 'receptores'] — chamada gpd.read_file, linha 95.

**Saídas.**

- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_fechamento_receptores.csv — chamada .to_csv, linha 83.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_receptores_anuais.csv — chamada metrics.to_csv, linha 92.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_vinculo_receptor_zona.csv — chamada links.to_csv, linha 99.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_ABC_sintese_criticos.png — chamada ax.figure.savefig, linha 131.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_ABC_sintese_criticos.svg — chamada ax.figure.savefig, linha 131.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/saturacao_por_zona_ano.csv — chamada .to_csv, linha 135.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/ABC_zonas_criticas.csv — chamada .to_csv, linha 136.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/manifesto_saidas.csv — chamada .to_csv, linha 137.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/zoneamento_nova_modelagem.csv — chamada .to_csv, linha 138.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/zoneamento_nova_modelagem.gpkg — chamada ledger.to_file, linha 139.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/resumo.json — chamada .write_text, linha 140.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/index.html — chamada .write_text, linha 145.

**Campos e chaves lidos.**

- config.DIRS: aermod_logs, grade_generated, out, post, zoneamento.
- config.FILES: zoning.
- selected: 24H, ALL, ANNUAL.
- annuals: ALL.
- lim: 24H, ANNUAL.
- r: pollutant.
- s: critical_preliminary, zones_with_internal_receptor.

**Campos e chaves gerados.**

- zones: zone_index.
- full: closure_ok, residual, sum_groups.
- metrics: ANNUAL_DAILY_MEAN, ANNUAL_MEAN.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 65-146 | lê dados; grava produtos Retorno: summaries. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/atualizar_resultados_aermod.py, linhas 80-86.

```python
            full[g]=s
        full['sum_groups']=full[ids].sum(axis=1);full['residual']=full.ALL-full.sum_groups
        full['closure_ok']=np.abs(full.residual)<=np.maximum(.001,.001*full.ALL)
        full.reset_index().to_csv(OUT/f'{pol}_fechamento_receptores.csv',index=False)
        if not full.closure_ok.all():raise ValueError(f'{pol}: falha de fechamento anual; consultar CSV')
        print(f'{pol}: 29 grupos, fechamento anual conferido; lendo série diária ALL...',flush=True)
        d,excluded=daily(selected['ALL','24H'],config.DIRS['aermod_logs']/('PM10.sum' if pol=='PM10' else 'PM25.sum'))
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/atualizar_resultados_aermod.py, linhas 112-118.

```python
        critical=set(worst.index[worst.critical]);ledger[f'{pol}_critico_preliminar']=ledger.index.isin(critical)
        means=full.reset_index().groupby(['X','Y'])[ids+['ALL']].mean().reset_index().merge(links,on=['X','Y'])
        byzone=means.groupby('zone_index')[ids+['ALL']].mean()
        dominant=byzone[ids].idxmax(axis=1);dominant[byzone[ids].sum(axis=1)<=0]='Sem contribuição positiva'
        ledger[f'{pol}_grupo_principal']=dominant.map(lambda g:POST_GROUP_NAMES.get(g,g)).reindex(zones.index).fillna('Informação insuficiente')
        for zid,row in byzone.iterrows():
            if zid not in critical:continue
```

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/auditar_adi_taxas.py

Compara taxas da planilha com as fontes realmente expandidas no ADI.

**Papel.** Auditoria/diagnóstico. **Fonte inspecionada.** E:\projeto\codigo\auditar_adi_taxas.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| collections | Estruturas de contagem, agrupamento e coleções auxiliares. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| validar_massas_entrada | Módulo autoral local; sua ficha está neste relatório. |


**Entradas.**

- E:/projeto/config.DIRS['out']/14_auditoria_entradas/entrada_BPIP_7caracteres/alteracoes.json — chamada .read_text, linha 37.
- out / 'PM25_Entrada_Revisada.ADI' if revised and pol == 'PM25' else config.DIRS['aermod_logs'] / f'{pol}.ADI' — chamada input_path.read_text, linha 42.

**Saídas.**

- E:/projeto/config.DIRS['out']/15_auditoria_metodologica/taxas_planilha_versus_ADI{suffix}.csv — chamada .to_csv, linha 76.
- E:/projeto/config.DIRS['out']/15_auditoria_metodologica/auditoria_taxas_ADI{suffix}.json — chamada .write_text, linha 77.

**Campos e chaves lidos.**

- config.DIRS: aermod_logs, out.
- source: taxa_total_g_s, tipo.
- x: poluente.
- sub: coerente_0_1pct, diferenca_relativa.
- v: failed_or_missing.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run(revised=False) | 35-79 | lê dados; grava produtos Retorno: summary. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/auditar_adi_taxas.py, linhas 58-64.

```python
                xy=np.asarray(verts[sid]);xy=xy-xy[0]
                area=abs(np.sum(xy[:,0]*np.roll(xy[:,1],-1)-np.roll(xy[:,0],-1)*xy[:,1]))/2
                mass=q*area
            elif typ=='AREACIRC':mass=q*math.pi*p[2]**2
            elif typ in ['POINT','VOLUME','POINTCAP','POINTHOR']:mass=q
            else:unsupported.append((sid,typ));continue
            par=parents[sid];totals[par]=totals.get(par,0.)+mass
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/auditar_adi_taxas.py, linhas 68-74.

```python
            rel=abs(delta)/abs(expected) if expected else 0 if actual==0 else np.nan
            rows.append({'poluente':pol,'id':sid,'id_adi':mapping.get(sid,sid),'tipo':source['tipo'],'taxa_total_planilha_g_s':expected,'taxa_total_adi_g_s':actual,'diferenca_g_s':delta,'diferenca_relativa':rel,'n_fontes_expandidas':sum(v==mapping.get(sid,sid) for v in parents.values()),'coerente_0_1pct':bool(np.isfinite(actual) and abs(delta)<=max(1e-9,abs(expected)*.001)) if expected is not None else False})
        sub=pd.DataFrame([x for x in rows if x['poluente']==pol])
        summary[pol]={'parent_sources':len(raw),'expanded_sources':len(loc),'unmatched_parent_keys':sorted(set(totals)-{mapping.get(s,s) for s in raw}),
            'failed_or_missing':int((~sub.coerente_0_1pct).sum()),'unsupported':unsupported,
            'expanded_types':dict(Counter(v[0] for v in loc.values())),'max_relative_difference':float(sub.diferenca_relativa.max())}
        print(pol,{k:v for k,v in summary[pol].items() if k!='unmatched_parent_keys'},flush=True)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/auditar_cenario_geral.py

Conferência do cenário geral e da escala física dos mapas vetoriais.

**Papel.** Auditoria/diagnóstico. **Fonte inspecionada.** E:\projeto\codigo\auditar_cenario_geral.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| cenario_geral_pos_banca | Módulo autoral local; sua ficha está neste relatório. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| medias_horarias_verificadas | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| pyproj | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| xml.etree.ElementTree | Leitura/edição de XML de projetos e documentos. |


**Entradas.**

- {path} — chamada path.read_text, linha 73.
- E:/projeto/output/16_revisao_pos_banca/cenario_geral/resumo.json — chamada .read_text, linha 78.
- E:/projeto/output/16_revisao_pos_banca/celulas_analise.gpkg — chamada gpd.read_file, linha 79.
- E:/projeto/output/16_revisao_pos_banca/cenario_geral/{pol}_{period}_receptores.csv — chamada pd.read_csv, linha 84.
- E:/projeto/output/16_revisao_pos_banca/cenario_geral/eventos_{pol}_{period}_manifesto.json — chamada .read_text, linha 88.
- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/{pol}_1h_receptores.csv — chamada pd.read_csv, linha 92.
- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/{pol}_24h_receptores.csv — chamada pd.read_csv, linha 99.
- E:/projeto/output/16_revisao_pos_banca/cenario_geral/periodos_{pol}_{period}.json — chamada .read_text, linha 106.
- E:/projeto/output/16_revisao_pos_banca/cenario_geral/zoneamento_geral.csv — chamada pd.read_csv, linha 109.
- E:/projeto/output/16_revisao_pos_banca/cenario_geral/regioes_gerais.csv — chamada pd.read_csv, linha 112.
- E:/projeto/output/16_revisao_pos_banca/cenario_geral/ABC_contribuicoes_regioes.csv — chamada pd.read_csv, linha 112.
- E:/projeto/output/11_integracao/apendices/resumo_figuras.json — chamada .read_text, linha 115.
- Mais 2 referências na ficha HTML e no inventário JSON.

**Saídas.**

- E:/projeto/output/16_revisao_pos_banca/cenario_geral/auditoria_campos.csv — chamada .to_csv, linha 135.
- E:/projeto/output/16_revisao_pos_banca/cenario_geral/auditoria_escala_cartografica.json — chamada .write_text, linha 136.
- E:/projeto/output/16_revisao_pos_banca/cenario_geral/auditoria_final.json — chamada .write_text, linha 138.

**Campos e chaves lidos.**

- r: height, map_panels, width.
- summary: cases.
- v: kind.
- cal.loc: CODE.
- f: concentration, event_code, quintile, receptor_id.
- manifest: files.
- stamp: path.
- m: eligible_periods_by_year, group_closure_max_abs.
- regions: eligible_monitored_area_pct.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| scale_receipt(path, extent) | 62-74 | lê dados Retorno: dict(path=str(path), map_panels=len(maps), nominal_scale=440000, min_measured_scale=min(scales), max_measured_scale=max(scales), geographic_extent=ex). |
| run() | 77-140 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/auditar_cenario_geral.py, linhas 79-85.

```python
    cells=gpd.read_file(ROOT/'celulas_analise.gpkg');primary=[g for g,v in GROUPS.items() if v['kind']=='primary']
    cal,_=met_calendar();valid=set(cal.loc[cal.valid,'CODE']);days=cal.groupby('day').valid.sum()
    audit=[]
    for period in ['1h','24h','anual']:
        for pol in ['PM10','PM25']:
            f=pd.read_csv(OUT/f'{pol}_{period}_receptores.csv')
            assert len(f)==1008 and f.receptor_id.nunique()==1008 and f.quintile.between(1,5).all()
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/auditar_cenario_geral.py, linhas 86-92.

```python
            assert np.isfinite(f.concentration).all() and f.concentration.ge(0).all()
            assert np.allclose(f[['C_'+g for g in primary]].sum(axis=1),f.concentration,rtol=3e-5,atol=2e-4)
            manifest=json.loads((OUT/f'eventos_{pol}_{period}_manifesto.json').read_text(encoding='utf8'))
            for stamp in manifest['files'].values():assert identity(stamp['path'])==stamp
            if period=='1h':
                assert f.event_code.isin(valid).all()
                d=pd.read_csv(ROOT/f'vento/analises_espaciais/{pol}_1h_receptores.csv').groupby('receptor_id').concentration.max()
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/auditar_direcoes_perfis.py

Conferência final da extensão direcional e das séries em concentração.

**Papel.** Auditoria/diagnóstico. **Fonte inspecionada.** E:\projeto\codigo\auditar_direcoes_perfis.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/resumo.json — chamada .read_text, linha 59.
- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/zoneamento_direcional.csv — chamada pd.read_csv, linha 60.
- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/regioes_direcionais.csv — chamada pd.read_csv, linha 63.
- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/ABC_contribuicoes_regioes.csv — chamada pd.read_csv, linha 63.
- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/correlogramas.csv — chamada pd.read_csv, linha 66.
- E:/projeto/output/16_revisao_pos_banca/vento/calendario_vento_horario.csv — chamada pd.read_csv, linha 67.
- E:/projeto/output/16_revisao_pos_banca/vento/dias_direcao_persistente.csv — chamada pd.read_csv, linha 68.
- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/{pol}_{period}_receptores.csv — chamada pd.read_csv, linha 72.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/precipitacao_referencia_diaria.csv — chamada pd.read_csv, linha 94.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/dados_series/metadados.js — chamada .read_text, linha 95.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/dados_series/{pol}_{sid}.js — chamada .read_text, linha 98.
- {entry} — chamada entry.read_text, linha 105.
- Mais 1 referências na ficha HTML e no inventário JSON.

**Saídas.**

- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/{pol}_{period}_receptores.csv — chamada table.to_csv, linha 78.
- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/auditoria_campos.csv — chamada .to_csv, linha 93.
- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/escalas_associacao_correlogramas.csv — chamada .to_csv, linha 93.
- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/auditoria_final.json — chamada .write_text, linha 121.

**Campos e chaves lidos.**

- summary: cases.
- regions: eligible_monitored_area_pct.
- v: kind.
- table: concentration, direction, five_emission_bands_identifiable, quintile.
- c: direction, five_emission_bands_identifiable, period, pollutant.
- correlo: direction, period, pollutant.
- rain: n_rain_stations.
- metadata: stations.
- data: groups, observed.
- check: pollutant, station_id.

**Campos e chaves gerados.**

- table: emission_band_basis, five_emission_bands_identifiable.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 58-122 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/auditar_direcoes_perfis.py, linhas 61-67.

```python
    assert zones.groupby(['pollutant','period','direction']).zone_index.nunique().eq(311).all()
    assert np.allclose(zones[[f'Q{i}_area_pct' for i in range(1,6)]].sum(axis=1),100)
    regions=pd.read_csv(OUT/'regioes_direcionais.csv');abc=pd.read_csv(OUT/'ABC_contribuicoes_regioes.csv')
    assert np.allclose(abc.groupby('region_id').share_pct.sum(),100,atol=.01)
    assert regions.eligible_monitored_area_pct.between(-1e-7,100+1e-7).all()
    primary=[g for g,v in GROUPS.items() if v['kind']=='primary'];records=[];correlo=pd.read_csv(OUT/'correlogramas.csv');scales=[]
    hourly=pd.read_csv(ROOT/'vento/calendario_vento_horario.csv').set_index('CODE').direction
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/auditar_emi_execucao_252.py

Confere o cenário de 252 fontes sem substituir a escolha do executante.

**Papel.** Auditoria/diagnóstico. **Fonte inspecionada.** E:\projeto\codigo\auditar_emi_execucao_252.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/12_houremiss/sensibilidade_WG_SCOF_1h/consolidado/validacao_consolidacao.json — chamada .read_text, linha 48.
- E:/projeto/output/14_auditoria_entradas/revalidacao_final/fontes_correntes.json — chamada .read_text, linha 49.
- E:/projeto/output/12_houremiss/sensibilidade_WG_SCOF_1h/Massas_anuais.csv — chamada pd.read_csv, linha 50.
- rec['arquivo'] — chamada p.open, linha 57.
- E:/projeto/output/13_rateio_emissoes/Fracoes_fontes.csv — chamada pd.read_csv, linha 79.
- E:/projeto/output/13_rateio_emissoes/Resumo_zonas.csv — chamada pd.read_csv, linha 80.

**Saídas.**

- E:/projeto/output/15_auditoria_metodologica/massas_9_fontes_cenario_252.csv — chamada d.to_csv, linha 78.
- E:/projeto/output/15_auditoria_metodologica/comparacao_rateio_cenario_252.csv — chamada .to_csv, linha 91.
- E:/projeto/output/15_auditoria_metodologica/auditoria_emi_252.json — chamada .write_text, linha 92.

**Campos e chaves lidos.**

- x: area_modelo_m2, arquivo, id, poluente, sha256.
- rec: arquivo, ordem_ids, origens, sha256.
- expected: ano, id, poluente.
- d: ano, poluente.
- fractions: id_fonte, poluente.
- zones: poluente.
- z: cenario_252_t_ano, classe_mudaria, delta_t_ano, nome_zona, poluente, total_quantificado_t_ano, zona.

**Campos e chaves gerados.**

- f: delta.
- z: cenario_252_t_ano, classe_mudaria, delta_t_ano.
- : classes_100t_alteradas, delta_massa_municipal_t_ano.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 45-93 | lê dados; grava produtos Retorno: summary. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/auditar_emi_execucao_252.py, linhas 85-91.

```python
        f['delta']=f.fracao*f.id_fonte.map(p.diferenca_t_ano)
        z=zones[zones.poluente==pol].copy();z['delta_t_ano']=z.zona.map(f.groupby('zona').delta.sum()).fillna(0)
        z['cenario_252_t_ano']=z.total_quantificado_t_ano+z.delta_t_ano
        z['classe_mudaria']=(z.total_quantificado_t_ano>100)!=(z.cenario_252_t_ano>100)
        comparison.append(z[['poluente','zona','nome_zona','total_quantificado_t_ano','cenario_252_t_ano','delta_t_ano','classe_mudaria']])
        summary[pol]['delta_massa_municipal_t_ano']=float(z.delta_t_ano.sum());summary[pol]['classes_100t_alteradas']=int(z.classe_mudaria.sum())
    pd.concat(comparison).to_csv(o/'comparacao_rateio_cenario_252.csv',index=False)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/auditar_escalas_poster.py

Mede a escala no tamanho físico das imagens incorporadas ao PPTX.

**Papel.** Auditoria/diagnóstico. **Fonte inspecionada.** E:\projeto\codigo\auditar_escalas_poster.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| posixpath | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| pyproj | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| xml.etree.ElementTree | Leitura/edição de XML de projetos e documentos. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- E:/projeto/output/11_integracao/apendices/resumo_figuras.json — chamada .read_text, linha 33.
- {pptx} — chamada zipfile.ZipFile, linha 36.

**Saídas.**

- {output} — chamada output.write_text, linha 62.

**Campos e chaves lidos.**

- N: r.
- x: role.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run(pptx, output) | 32-62 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/auditar_escalas_poster.py, linhas 55-61.

```python
            maps.append(dict(role=role,media=target,ground_width_m=distance,map_width_cm=100*map_width_m,scale_measured=scale,scale_label=expected))
        assert len(maps)==10 and sum(x['role']=='metodologia' for x in maps)==4
        text=' '.join(t.text or '' for t in root.findall('.//a:t',N))
        assert '27192*83' in text and 'Mover Program' in text
        assert 'Finance Code 001' in text
        assert 'Health assessment' not in text and 'Population' not in text
    result=dict(passed=True,pptx=str(pptx),native_poster_cm=[120,90],methods_scale=440000,main_maps_scale=220000,maps=maps,mover_acknowledgement=True,capes_finance_code_001=True,health_results_in_poster=False)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/auditar_ids_bpip_final.py

Auditar ids bpip final. Auditoria/diagnóstico. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Auditoria/diagnóstico. **Fonte inspecionada.** E:\projeto\codigo\auditar_ids_bpip_final.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| collections | Estruturas de contagem, agrupamento e coleções auxiliares. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| openpyxl | Leitura/escrita de planilhas XLSX; não é o mecanismo do Excel aberto. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- externos.1h_adi_7e2357f — chamada .read_text, linha 26.
- externos.1h_ado_b8fbad1 — chamada .read_text, linha 39.

**Saídas.**

- E:/projeto/output/14_auditoria_entradas/entrada_BPIP_7caracteres/auditoria_base.json — chamada .write_text, linha 56.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/auditar_ids_bpip_final.py, linhas 25-33.

```python
out.mkdir(parents=True,exist_ok=True)
ls=Path(_cp_externo('1h_adi_7e2357f')).read_text(encoding='cp1252').splitlines()
loc={};par={};hour=set();groups=defaultdict(set);desc={};last=None
for l in ls:
 p=l.split()
 if not p:continue
 if p[0]=='LOCATION':loc[p[1]]=p[2:];last=p[1]
 if p[:2]==['**','DESCRSRC'] and last:desc[last]=' '.join(p[2:])
 if p[0]=='SRCPARAM':par[p[1]]=p[2:]
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/auditar_medias_horarias.py

Conferência integral dos POST horários com calendário meteorológico independente.

**Papel.** Auditoria/diagnóstico. **Fonte inspecionada.** E:\projeto\codigo\auditar_medias_horarias.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| medias_horarias_verificadas | Módulo autoral local; sua ficha está neste relatório. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/auditar_medias_horarias.py, linhas 8-16.

```python
"""Conferência integral dos POST horários com calendário meteorológico independente."""
# INÍCIO DOS CAMINHOS PORTÁTEIS
import sys as _cp_sys
from pathlib import Path as _cp_Path
_cp_file = _cp_Path(globals().get('__file__', _cp_Path.cwd() / 'codigo' / 'script.py')).resolve()
for _cp_parent in [_cp_file.parent, *_cp_file.parents]:
    _cp_code = _cp_parent if (_cp_parent / 'caminhos_congonhas.py').is_file() else _cp_parent / 'codigo'
    if (_cp_code / 'caminhos_congonhas.py').is_file():
        if str(_cp_code) not in _cp_sys.path: _cp_sys.path.insert(0, str(_cp_code))
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/auditar_pares_vento.py

Confere figuras pareadas, escala física e totais do calendário.

**Papel.** Auditoria/diagnóstico. **Fonte inspecionada.** E:\projeto\codigo\auditar_pares_vento.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| auditar_cenario_geral | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/11_integracao/apendices/resumo_figuras.json — chamada .read_text, linha 35.
- {p} — chamada p.read_text, linha 40.
- E:/projeto/output/16_revisao_pos_banca/vento/calendario_vento_horario.csv — chamada pd.read_csv, linha 45.
- E:/projeto/output/16_revisao_pos_banca/vento/horas_por_direcao.csv — chamada pd.read_csv, linha 45.
- {entry} — chamada entry.read_text, linha 50.

**Saídas.**

- os.environ.get('CONGONHAS_PAIRED_OUTPUT', str(ROOT / 'vento/analises_espaciais/pares'))/auditoria_final.json — chamada .write_text, linha 56.

**Campos e chaves lidos.**

- receipt: map_panels.
- hours: 2021, 2022, 2023, persistent_days, total_hours.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run(check_links=True) | 34-56 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/auditar_pares_vento.py, linhas 45-51.

```python
    cal=pd.read_csv(ROOT/'vento/calendario_vento_horario.csv');hours=pd.read_csv(ROOT/'vento/horas_por_direcao.csv')
    assert len(cal)==26280 and hours.total_hours.sum()==24892 and hours.persistent_days.sum()==463
    assert hours[['2021','2022','2023']].sum(axis=1).eq(hours.total_hours).all()
    links=0
    for entry in ([OUT/'index.html',OUT.parent/'index.html'] if check_links else []):
        s=entry.read_text(encoding='utf8')
        for href in re.findall(r'(?:href|src)="([^"]+)"',s):
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/auditar_revisao_pos_banca.py

Verificações integradas da revisão, com rastreabilidade dos insumos.

**Papel.** Auditoria/diagnóstico. **Fonte inspecionada.** E:\projeto\codigo\auditar_revisao_pos_banca.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/16_revisao_pos_banca/zoneamento_pos_banca.gpkg — chamada gpd.read_file, linha 55.
- E:/projeto/output/16_revisao_pos_banca/celulas_analise.gpkg — chamada gpd.read_file, linha 55.
- E:/projeto/output/16_revisao_pos_banca/receptores.csv — chamada pd.read_csv, linha 55.
- E:/projeto/output/16_revisao_pos_banca/resumo.json — chamada .read_text, linha 55.
- E:/projeto/output/11_integracao/nova_modelagem/{pol}_fechamento_receptores.csv — chamada pd.read_csv, linha 60.
- E:/projeto/output/16_revisao_pos_banca/regioes_controle.csv — chamada pd.read_csv, linha 64.
- E:/projeto/output/16_revisao_pos_banca/ABC_regioes_contribuintes.csv — chamada pd.read_csv, linha 64.
- E:/projeto/output/16_revisao_pos_banca/preparacao_modelagem/Vinculo_grade_candidata_311_zonas.csv — chamada pd.read_csv, linha 67.
- E:/projeto/adi_ado_sum/{pol}.ADI — chamada .read_text, linha 71.
- {path} — chamada path.read_text, linha 78.
- p[1:] — chamada p.read_bytes, linha 90.

**Saídas.**

- E:/projeto/output/16_revisao_pos_banca/auditoria_integrada.json — chamada .write_text, linha 92.

**Campos e chaves lidos.**

- v: kind.
- z: zone_index.
- points: X, Y.
- summary: pols.
- abc.loc: ABC.
- abc: region_id.
- regions.loc: n_receptors.
- regions: pollutant, region_id.
- gridlinks: geometry_fragment, inside_zone_after_rounding, zone_index.
- gridlinks.loc: zone_index.
- checks: zones_unique.

**Campos e chaves gerados.**

- checks: candidate_grid, temporal_scenarios, zones_unique.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 54-92 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/auditar_revisao_pos_banca.py, linhas 57-63.

```python
 for pol in ['PM10','PM25']:
  q=z[[f'{pol}_Q{i}_area_pct' for i in range(1,6)]].sum(axis=1);assert np.allclose(q,100)
  groups=z[[pol+'_share_'+k for k in primary]].sum(axis=1);assert np.allclose(groups,100,atol=.001)
  g=pd.read_csv(R/f'output/11_integracao/nova_modelagem/{pol}_fechamento_receptores.csv').groupby(['X','Y']).ALL.mean().reset_index()
  comp=points[['X','Y',pol+'_annual']].merge(g,on=['X','Y'],validate='one_to_one')
  assert np.allclose(comp[pol+'_annual'],comp.ALL,atol=1e-4,rtol=2e-5)
  checks[pol]={'zone_Q_sum_max_error_pct':float((q-100).abs().max()),'zone_group_sum_max_error_pct':float((groups-100).abs().max()),'ALL_vs_annual_indicator_max_abs':float((comp[pol+'_annual']-comp.ALL).abs().max()),'source_mass_conservation_error_tpy':summary['pols'][pol]['mass_allocation']['absolute_error_tpy']}
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/auditar_series_e_gravidade.py

Auditoria das estações e graduação exploratória, sem mudar o índice vigente.

**Papel.** Auditoria/diagnóstico. **Fonte inspecionada.** E:\projeto\codigo\auditar_series_e_gravidade.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| cartografia_apendices | Módulo autoral local; sua ficha está neste relatório. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.dates | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| methodology_rules | Módulo autoral local; sua ficha está neste relatório. |
| monitoramento_mma | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| standards | Módulo autoral local; sua ficha está neste relatório. |
| stations | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/identificacao_estacoes_figura_B1.csv — chamada pd.read_csv, linha 62.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/zoneamento_avaliacao_atual.gpkg — chamada gpd.read_file, linha 94.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_indicadores_trienais_receptores.csv — chamada pd.read_csv, linha 96.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_vinculo_receptor_zona.csv — chamada pd.read_csv, linha 96.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_todos_grupos_por_zona.csv — chamada pd.read_csv, linha 102.

**Saídas.**

- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/Series_historicas_estacoes.{ext} — chamada fig.savefig, linha 77.
- E:/projeto/config.DIRS['out']/10_avaliacao_rede/series_diarias_estacoes.csv — chamada daily.to_csv, linha 79.
- E:/projeto/config.DIRS['out']/10_avaliacao_rede/sinalizacoes_PM25_maior_PM10_por_ano.csv — chamada .to_csv, linha 83.
- E:/projeto/config.DIRS['out']/10_avaliacao_rede/auditoria_estacoes_completa.csv — chamada .to_csv, linha 84.
- E:/projeto/config.DIRS['out']/10_avaliacao_rede/Serie_{row.station_id}.{ext} — chamada fig.savefig, linha 92.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{name}.gpkg — chamada z.to_file, linha 109.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{name}.csv — chamada .to_csv, linha 109.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/auditoria_recorte_ABC.csv — chamada .to_csv, linha 110.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/auditoria_series_gravidade.json — chamada .write_text, linha 113.

**Campos e chaves lidos.**

- config.DIRS: out.
- pv: 24H, ANNUAL.
- ax.spines: right, top.

**Campos e chaves gerados.**

- flagged: year.
- report: criterio, fontes_historicas_adicionadas.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| severity(annual, daily, pol) | 56-58 | Chamadas efetivas: np.select, annual.le, daily.le Retorno: np.select([annual.le(pv['ANNUAL']) & daily.le(pv['24H']), annual.le(pi1[0]) & daily.le(pi1[1]), annual.le(2 * pi1[0]) & daily.le(2 * pi1[1])], LEVELS[:3], default=LEVELS[3]). |
| run() | 61-114 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/auditar_series_e_gravidade.py, linhas 72-78.

```python
        ax.set_ylabel('µg/m³',fontsize=9);ax.grid(alpha=.17);ax.spines[['top','right']].set_visible(False)
        audit.append(dict(station_id=row.station_id,station_name=row.station_name,first_hour=str(f.datetime.min()),last_hour=str(f.datetime.max()),unique_hours=len(f),duplicate_hours=int(f.datetime.duplicated().sum()),PM10_valid_hours=int(f.PM10.count()),PM25_valid_hours=int(f.PM25.count()),paired_hours=int((f.PM10.notna()&f.PM25.notna()).sum()),PM25_above_PM10_hours=int((f.PM25>f.PM10).sum()),PM10_max=float(f.PM10.max()),PM25_max=float(f.PM25.max()) if f.PM25.notna().any() else None))
    axes[-1].xaxis.set_major_locator(mdates.YearLocator());axes[-1].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    fig.subplots_adjust(left=.10,right=.98,top=.98,bottom=.065,hspace=.50)
    fig.legend(*axes[0].get_legend_handles_labels(),loc='lower center',ncol=2,frameon=False,fontsize=10)
    for ext in ['png','svg','pdf']:fig.savefig(OUT/f'Series_historicas_estacoes.{ext}',dpi=800,bbox_inches='tight',pad_inches=.06)
    plt.close(fig)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/auditoria_exaustiva_estacoes.py

Confronta cada aba das bases originais com a série efetivamente utilizada.

**Papel.** Auditoria/diagnóstico. **Fonte inspecionada.** E:\projeto\codigo\auditoria_exaustiva_estacoes.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| itertools | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| monitoramento_mma | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| openpyxl | Leitura/escrita de planilhas XLSX; não é o mecanismo do Excel aberto. |
| openpyxl.utils.datetime | Leitura/escrita de planilhas XLSX; não é o mecanismo do Excel aberto. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

- E:/projeto/config.DIRS['out']/10_avaliacao_rede/auditoria_todas_bases_estacoes.csv — chamada summary.to_csv, linha 113.
- E:/projeto/config.DIRS['out']/10_avaliacao_rede/auditoria_abas_originais.csv — chamada .to_csv, linha 114.
- E:/projeto/config.DIRS['out']/10_avaliacao_rede/auditoria_divergencias_originais.csv — chamada .to_csv, linha 115.
- E:/projeto/config.DIRS['out']/10_avaliacao_rede/auditoria_todas_bases_resumo.json — chamada .write_text, linha 118.

**Campos e chaves lidos.**

- config.DIRS: out.
- a: file.
- raw: datetime.
- summary: source_kind.
- report: different_annual_values, missing_positive_hours_annual.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| column_pollutant(value) | 45-49 | Chamadas efetivas: norm, key.startswith Retorno: None, 'PM10'. |
| run() | 52-121 | grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/auditoria_exaustiva_estacoes.py, linhas 69-75.

```python
                except StopIteration:break
            scores=[sum(column_pollutant(v) is not None for v in row) for row in first]
            header=int(np.argmax(scores)) if scores else 0
            columns={pol:i for i,v in enumerate(first[header]) if (pol:=column_pollutant(v)) is not None} if first else {}
            sheets.append(dict(file=str(path),sheet=sheet.title,station_id=sid,rows_declared=sheet.max_row,columns_declared=sheet.max_column,header_row=header+1,pollutant_columns=';'.join(columns)))
            if not columns:continue
            data=[];bad_dates=0;dates_outside=0;nonpositive={pol:0 for pol in columns}
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/auditoria_exaustiva_estacoes.py, linhas 100-106.

```python
            if not data:continue
            raw=pd.DataFrame(data);duplicates=int(raw.datetime.duplicated().sum())
            raw=raw.groupby('datetime').mean(numeric_only=True)
            for year,sub in raw.groupby(raw.index.year):
                for pol in columns:
                    series=sub[pol].dropna();target=processed[pol].reindex(series.index)
                    missing=target.isna();different=target.notna()&~np.isclose(series,target,rtol=0,atol=1e-6,equal_nan=True)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/auditoria_metodologica_integrada.py

Auditoria reproduzível dos insumos e indicadores usados no seminário.

**Papel.** Auditoria/diagnóstico. **Fonte inspecionada.** E:\projeto\codigo\auditoria_metodologica_integrada.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| methodology_rules | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| out_aermod_reader | Módulo autoral local; sua ficha está neste relatório. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| standards | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/zoneamento_avaliacao_atual.gpkg — chamada gpd.read_file, linha 91.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_receptores_anuais.csv — chamada pd.read_csv, linha 113.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_indicadores_trienais_receptores.csv — chamada pd.read_csv, linha 118.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_vinculo_receptor_zona.csv — chamada pd.read_csv, linha 120.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_todos_grupos_por_zona.csv — chamada pd.read_csv, linha 134.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_perfis_311_zonas.csv — chamada pd.read_csv, linha 137.
- E:/projeto/config.DIRS['out']/13_rateio_emissoes/Resumo_zonas.csv — chamada pd.read_csv, linha 149.
- E:/projeto/config.DIRS['out']/13_rateio_emissoes/Balanco_fontes.csv — chamada pd.read_csv, linha 152.
- E:/projeto/config.DIRS['out']/13_rateio_emissoes/Fracoes_fontes.csv — chamada pd.read_csv, linha 154.
- E:/projeto/config.DIRS['aermod_logs']/'PM10.ADI' if pol == 'PM10' else 'PM25.ADI' — chamada adi.read_text, linha 160.
- p[1:] — chamada p.read_bytes, linha 178.
- E:/projeto/config.DIRS['out']/10_avaliacao_rede/quadrimestres_mma.csv — chamada pd.read_csv, linha 181.
- Mais 6 referências na ficha HTML e no inventário JSON.

**Saídas.**

- E:/projeto/config.DIRS['out']/15_auditoria_metodologica/qualidade_geometrica_zonas.csv — chamada .to_csv, linha 98.
- E:/projeto/config.DIRS['out']/15_auditoria_metodologica/{pol}_comparacao_p98_trienio.csv — chamada comparison.to_csv, linha 131.
- E:/projeto/config.DIRS['out']/15_auditoria_metodologica/correcao_posto_p98_estacoes.csv — chamada .to_csv, linha 191.
- E:/projeto/config.DIRS['out']/15_auditoria_metodologica/auditoria_integrada.json — chamada .write_text, linha 204.
- E:/projeto/config.DIRS['out']/15_auditoria_metodologica/manifesto_entradas_saida.csv — chamada .to_csv, linha 205.

**Campos e chaves lidos.**

- config.DIRS: aermod_logs, out, post.
- z: geometry, nome, zone_index.
- results: territorio.
- geom.loc: zone_index.
- selected: 24H, ALL, ANNUAL.
- a: ALL.
- v: kind.
- comp: ANNUAL_MEAN, N_DAYS, P98.
- current: ANNUAL_MEAN, N_DAYS, P98.
- links: spatial_support, zone_index.
- byzone: URB-FER, URB-NUC, URB-VIA.
- profiles: n_zonas.
- links.loc: zone_index.
- mass: poluente.
- b: fracao_ambigua, massa_alocada_t_ano, massa_ambigua_t_ano, massa_fonte_t_ano, massa_fora_zoneamento_t_ano, poluente.
- f: poluente.
- q: completeness, expected_days, representative.
- diff: n_valid_days, p98, p98_before, pollutant, station_id, year.
- z.loc: PM25_ANN_monitor, health_fraction_pct.

**Campos e chaves gerados.**

- results: health, inputs, p98_corrected_station_years, population, stations, territorio.
- geom: area_m2, area_residual, populacao_pendente.
- : emissions, execution, population_pending_zones, residual_area_zones.
- metrics: ANNUAL_DAILY_MEAN, ANNUAL_MEAN.
- comparison: difference.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| close(a, b, atol=1e-08) | 83-85 | Chamadas efetivas: np.allclose, ValueError, str, np.nanmax, np.abs, np.asarray |
| run() | 88-207 | lê dados; grava produtos Retorno: results. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/auditoria_metodologica_integrada.py, linhas 193-199.

```python
    eligible=z.PM25_PV_origem.eq('monitoramento')&z.pop_ge30_estimada.gt(0)&z.PM25_ANN_monitor.notna()
    expected=100*(-np.expm1(-np.log(1.08)/10*np.maximum(z.loc[eligible,'PM25_ANN_monitor']-5,0)))
    close(expected,z.loc[eligible,'health_fraction_pct'])
    assert z.loc[~eligible,'health_fraction_pct'].isna().all() and z.health_avoidable_deaths.isna().all()
    results['health']={'eligible_zones':int(eligible.sum()),'fraction_min_pct':float(expected.min()),'fraction_max_pct':float(expected.max()),'deaths_estimated':False,'RR10':1.08,'reference':5.}
    results['population']=json.loads((config.DIRS['out']/'06_censo_ibge/auditoria_populacao_consolidada.json').read_text(encoding='utf8'))
    results['inputs']=json.loads((config.DIRS['out']/'14_auditoria_entradas/revalidacao_final/validacao_final.json').read_text(encoding='utf8'))
```

Logaritmo natural. Na função de risco, β=ln(RR)/10 converte um risco relativo por 10 µg/m³ para a escala de 1 µg/m³.

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- log: Logaritmo natural. Na função de risco, β=ln(RR)/10 converte um risco relativo por 10 µg/m³ para a escala de 1 µg/m³.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/autoteste_metodologia.py

Autotestes sintéticos dos cálculos estruturais da v34.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\projeto\codigo\autoteste_metodologia.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| __future__ | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| aermod_sources | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| censo_ibge | Módulo autoral local; sua ficha está neste relatório. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| management | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| receptor_grid | Módulo autoral local; sua ficha está neste relatório. |
| risk | Módulo autoral local; sua ficha está neste relatório. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| source_apportionment | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| zone_analysis | Módulo autoral local; sua ficha está neste relatório. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- z: EMIS_TOTAL_GS.
- bal: unallocated_gs.
- abc: ABC_CLASS.
- abc2: ABC_CLASS, ABC_CUM_PCT.
- scen.loc: EST_REDUCTION_PCT_ALL.
- scen: reduction_fraction_A.
- aabc: zone_index.
- z0: ABC_SHARE_PCT.
- mg: N_GROUPS_A, zone_index.
- hs.loc: health_pop_above_pv.
- haf: mean_af_pct.
- r: kind, population, zone_primary.
- gdiag: coverage_ok.
- gze.loc: _grid_geometry_source.
- gze: zone_index.

**Campos e chaves gerados.**

- zm: zone_index.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| main() | 67-194 | Chamadas efetivas: gpd.GeoDataFrame, allocate_emissions_to_zones, np.allclose, emission_mass_balance_audit, pd.DataFrame, build_abc_analysis, build_abc_reduction_scenarios, float |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/autoteste_metodologia.py, linhas 121-127.

```python
    z0=aabc[aabc['zone_index']==0].sort_values('ABC_RANK')
    assert abs(float(z0['ABC_SHARE_PCT'].sum())-100.0)<1e-9
    assert 'ABC_EMIS_PRIORITY_GROUP' in asummary.columns

    zm=z.copy()
    zm['zone_index']=zm.index
    zm=zm.set_index('zone_index',drop=False)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/autoteste_metodologia.py, linhas 158-164.

```python
    assert len(zone1_communities)>=1
    assert abs(sum(float(r['population']) for r in zone1_communities)-300.0)<1e-9
    assert sum(r['kind']=='GEOCENTRO_SEM_POPULACAO' and r['zone_primary']=='2' for r in anchors)==1
    old_boundaries = getattr(config, "GRID_INCLUDE_INTERNAL_BOUNDARIES", True)
    config.GRID_INCLUDE_INTERNAL_BOUNDARIES = True
    borders,_,max_gap=_boundary_records(gzn,gmgeom)
    config.GRID_INCLUDE_INTERNAL_BOUNDARIES = old_boundaries
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/avaliar_robustez_cientifica.py

Comparações auditáveis para a revisão científica, sem recalibrar AERMOD.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\avaliar_robustez_cientifica.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| medias_horarias_verificadas | Módulo autoral local; sua ficha está neste relatório. |
| methodology_rules | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| scipy.spatial | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.stats | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| shapely | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| standards | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/10_avaliacao_rede/series_diarias_estacoes.csv — chamada pd.read_csv, linha 94.
- E:/projeto/output/11_integracao/nova_modelagem/{pol}_medias_diarias_1h_manifesto.json — chamada .read_text, linha 99.
- E:/projeto/output/11_integracao/nova_modelagem/{pol}_indicadores_trienais_receptores.csv — chamada pd.read_csv, linha 192.
- E:/projeto/output/11_integracao/nova_modelagem/{pol}_medias_diarias_1h.csv.gz — chamada pd.read_csv, linha 114.
- E:/projeto/output/10_avaliacao_rede/trienios_mma.csv — chamada pd.read_csv, linha 147.
- E:/projeto/output/11_integracao/nova_modelagem/{pol}_vinculo_receptor_zona.csv — chamada pd.read_csv, linha 193.
- E:/projeto/output/11_integracao/nova_modelagem/{pol}_todos_grupos_por_zona.csv — chamada pd.read_csv, linha 209.
- E:/projeto/output/11_integracao/nova_modelagem/zoneamento_avaliacao_atual.gpkg — chamada gpd.read_file, linha 249.
- E:/projeto/output/11_integracao/nova_modelagem/estacoes_rede_atual.gpkg — chamada gpd.read_file, linha 249.

**Saídas.**

- E:/projeto/output/15_auditoria_metodologica/revisao_cientifica/pares_diarios_estacoes_2021_2023.csv — chamada pairs.to_csv, linha 140.
- E:/projeto/output/15_auditoria_metodologica/revisao_cientifica/desempenho_por_estacao.csv — chamada summary.to_csv, linha 141.
- E:/projeto/output/15_auditoria_metodologica/revisao_cientifica/vinculos_estacoes_receptores.csv — chamada .to_csv, linha 142.
- E:/projeto/output/15_auditoria_metodologica/revisao_cientifica/cobertura_cenarios_por_zona.csv — chamada .to_csv, linha 171.
- E:/projeto/output/15_auditoria_metodologica/revisao_cientifica/prioridades_e_estabilidade_por_zona.csv — chamada .to_csv, linha 243.
- E:/projeto/output/15_auditoria_metodologica/revisao_cientifica/robustez_cientifica.json — chamada .write_text, linha 257.

**Campos e chaves lidos.**

- observations: pollutant, valid_day, year.
- manifest: comparison_passed, meteorology.
- roll: end_year, n_design_years, pollutant, start_year.
- threshold: 24H, ANNUAL.
- v: kind.
- t: 24H, ANNUAL.
- z.loc: pop_estimada.
- meanmax: zone_ids.
- z: zone_index.

**Campos e chaves gerados.**

- chunk: station_id.
- model: date.
- pairs: month, pollutant, year.
- records: coverage.
- report: input_identities.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| agreement(observed, modelled) | 71-79 | Chamadas efetivas: np.asarray, dict, np.isfinite, len, float, o.mean, m.mean, e.mean Retorno: dict(n=len(o), observed_mean=float(o.mean()), modelled_mean=float(m.mean()), bias=float(e.mean()), mae=float(np.abs(e).mean()), rmse=float(np.sqrt(np.mean(e ** 2))), correlation=float(np.corrcoef(o, m. |
| footprint(z, mask) | 82-90 | Chamadas efetivas: np.asarray, dict, union_all, len, int, float, mask.sum, .any Retorno: dict(zones=int(mask.sum()), zone_ids=[int(x) for x in sel.zone_index], area_km2=float(area / 1000000.0), area_pct=float(area / total_area * 100), allocated_population=float(sel.pop_estimada.sum(min_co. |
| station_pairs(stations) | 93-143 | lê dados; grava produtos Retorno: summary. |
| coverage_sensitivity(z, stations) | 146-172 | lê dados; grava produtos Retorno: results. |
| ranking_compare(a, b, ids) | 175-184 | Associação por postos. Mede ordenação conjunta, não igualdade de magnitude nem desempenho frente a observações ausentes. Retorno: dict(eligible=len(ids), reference_top_count=len(sa), alternative_top_count=len(sb), shared_top_count=len(sa & sb), jaccard=float(len(sa & sb) / len(sa  /  sb)), spearman=correlation, reference_top_ids=s. |
| zonal_sensitivity(z) | 187-244 | lê dados; grava produtos Retorno: result. |
| run() | 247-260 | lê dados; grava produtos Retorno: report. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/avaliar_robustez_cientifica.py, linhas 76-82.

```python
    return dict(n=len(o),observed_mean=float(o.mean()),modelled_mean=float(m.mean()),
        bias=float(e.mean()),mae=float(np.abs(e).mean()),rmse=float(np.sqrt(np.mean(e**2))),
        correlation=float(np.corrcoef(o,m)[0,1]) if len(o)>1 and np.std(o)>0 and np.std(m)>0 else None,
        model_observed_mean_ratio=float(m.mean()/o.mean()) if o.mean()>0 else None)

# Footprint
def footprint(z,mask):
```

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

Raiz quadrada. No ajuste ponderado do k-means, multiplicar a coluna por √peso faz o peso entrar uma única vez na distância ao quadrado.

Desvio-padrão. Na padronização z, coloca colunas em escala comparável; conferir ddof no trecho.

Trecho de codigo/avaliar_robustez_cientifica.py, linhas 180-186.

```python
    sa=set(aa[aa>=aa.nlargest(n).iloc[-1]].index);sb=set(bb[bb>=bb.nlargest(n).iloc[-1]].index)
    correlation=float(spearmanr(aa,bb).statistic) if aa.nunique()>1 and bb.nunique()>1 else None
    return dict(eligible=len(ids),reference_top_count=len(sa),alternative_top_count=len(sb),
        shared_top_count=len(sa&sb),jaccard=float(len(sa&sb)/len(sa|sb)),
        spearman=correlation,reference_top_ids=sorted(map(int,sa)),alternative_top_ids=sorted(map(int,sb)))

# Zonal sensitivity
```

Associação por postos. Mede ordenação conjunta, não igualdade de magnitude nem desempenho frente a observações ausentes.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- sqrt: Raiz quadrada. No ajuste ponderado do k-means, multiplicar a coluna por √peso faz o peso entrar uma única vez na distância ao quadrado.
- std: Desvio-padrão. Na padronização z, coloca colunas em escala comparável; conferir ddof no trecho.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- spearmanr: Associação por postos. Mede ordenação conjunta, não igualdade de magnitude nem desempenho frente a observações ausentes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/caminhos_congonhas.mjs

Caminhos congonhas. Configuração compartilhada. A organização passa por settings, raizProjeto, caminho, callback, externo, adaptarTexto, callback, adaptarRuntime.

**Papel.** Configuração compartilhada. **Fonte inspecionada.** E:\projeto\codigo\caminhos_congonhas.mjs.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| node:fs | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |
| node:path | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |
| node:url | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |


**Entradas.**

- process.env[envKey+'_CONFIG'] /  / path.join(code,'caminhos_projeto.json') — chamada fs.readFileSync, linha 14.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/caminhos_congonhas.mjs, linhas 14-22.

```javascript
const settings=()=>JSON.parse(fs.readFileSync(process.env[envKey+'_CONFIG']||path.join(code,'caminhos_projeto.json'),'utf8').replace(/^\uFEFF/,''));

// Configuração e raiz
export function raizProjeto(style='posix'){
 const c=settings();let r=process.env[envKey]||(project==='congonhas'?process.env.EMI_PROJECT_ROOT:'')||c.raiz_projeto||path.dirname(code);
 r=path.isAbsolute(r)?r:path.resolve(code,r);return style==='posix'?r.replaceAll('\\','/'):r;
}

// Pastas e arquivos
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/caminhos_congonhas.ps1

Caminhos congonhas. Configuração compartilhada. A organização passa por Get, Get, Get, Get, Convert.

**Papel.** Configuração compartilhada. **Fonte inspecionada.** E:\projeto\codigo\caminhos_congonhas.ps1.

**Bibliotecas e dependências.**

Não há importação Python/JavaScript declarada; conferir programas acionados e comandos do arquivo.

**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/caminhos_congonhas.ps1, linhas 12-20.

```text
function Get-PortableSettings { Get-Content -LiteralPath $script:PortableConfig -Raw -Encoding UTF8 | ConvertFrom-Json }
function Get-PortableRoot {
 $c=Get-PortableSettings
 $name="CONGONHAS_PROJECT_ROOT"
 $value=[Environment]::GetEnvironmentVariable($name)
 if(-not $value -and "congonhas" -eq 'congonhas'){$value=$env:EMI_PROJECT_ROOT}
 if(-not $value){$value=$c.raiz_projeto}
 if(-not $value){return (Split-Path $script:PortableCode -Parent)}
 if([System.IO.Path]::IsPathRooted($value)){return $value}
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/caminhos_congonhas.py

Caminhos congonhas. Configuração compartilhada. A organização passa por configuracao, raiz_projeto, caminho, texto_caminho, externo, adaptar_texto.

**Papel.** Configuração compartilhada. **Fonte inspecionada.** E:\projeto\codigo\caminhos_congonhas.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| json | Configurações, metadados e registros estruturados de auditoria. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- Path(override).expanduser() if override else CONFIG_FILE — chamada path.read_text, linha 24.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- entry: chave, original.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| configuracao() | 21-24 | lê dados Retorno: json.loads(path.read_text('utf-8-sig')) if path.exists() else {}. |
| raiz_projeto() | 26-35 | Chamadas efetivas: configuracao, cfg.get, .strip, .expanduser, p.is_absolute, .resolve, os.environ.get, Path Retorno: BASE_CODIGO.parent, p if p.is_absolute() else (BASE_CODIGO / p).resolve(). |
| caminho(relativo='') | 38-47 | Chamadas efetivas: configuracao, raiz_projeto, .strip, sorted, cfg.get, .replace, rel.startswith, .expanduser Retorno: root / rel if rel else root, base / suffix if suffix else base. |
| texto_caminho(relativo='', estilo='posix') | 49-51 | Chamadas efetivas: caminho, p.as_posix, str Retorno: p.as_posix() if estilo == 'posix' else str(p). |
| externo(chave) | 54-68 | Chamadas efetivas: configuracao, .get, .expanduser, KeyError, isinstance, entry.get, str, ValueError Retorno: p.as_posix() if '/' in text and '\\' not in text else str(p). |
| adaptar_texto(texto) | 71-89 | Chamadas efetivas: configuracao, cfg.get, .values, re.compile, pattern.sub, original.replace, texto_caminho, .join Retorno: pattern.sub(lambda m: pairs[m[0]], str(texto)), texto. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/caminhos_congonhas.py, linhas 26-34.

```python
def raiz_projeto():
    cfg=configuracao()
    explicit=os.environ.get(ENV_RAIZ,'').strip() or (os.environ.get('EMI_PROJECT_ROOT','').strip() if PROJETO=='congonhas' else '') or cfg.get('raiz_projeto','')
    if explicit:
        p=Path(explicit).expanduser()
        return p if p.is_absolute() else (BASE_CODIGO/p).resolve()
    if cfg.get('modo_entrega'):
        for p in BASE_CODIGO.parents:
            if (p/'01_entradas').is_dir() and (p/'02_saidas').is_dir():return p
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/cartografia_apendices.py

Cartografia em SIRGAS 2000 com escala geodésica e contexto municipal.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\cartografia_apendices.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| matplotlib.cm | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.font_manager | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.lines | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.patches | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.path | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.ticker | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.tri | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| pyproj | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| rosa_vento_seletor | Módulo autoral local; sua ficha está neste relatório. |
| scipy.interpolate | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shapely.ops | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| textwrap | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| vector_portable | Módulo autoral local; sua ficha está neste relatório. |


**Entradas.**

- E:/projeto/base_regional/municipios_vizinhos_cache.geojson — chamada gp.read_file, linha 97.
- E:/projeto/config.DIRS['out']/11_integracao/apendices/{stem}.svg — chamada svg_path.read_text, linha 359.

**Saídas.**

- E:/projeto/config.DIRS['out']/11_integracao/apendices/{stem}.{ext} — chamada fig.savefig, linha 357.
- E:/projeto/config.DIRS['out']/11_integracao/apendices/{stem}.svg — chamada svg_path.write_text, linha 360.

**Campos e chaves lidos.**

- config.DIRS: out.
- v: name.
- surface: cmap, limits, norm, values, x, y.
- opts: ticklabels.
- s: cmap, norm, ticks, values.

**Campos e chaves gerados.**

- surface: _bar_position.
- handles: missing, peak.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| rounded_scale_ticks(norm) | 64-73 | Chamadas efetivas: norm.inverse, np.unique, np.floor, np.ceil, np.linspace, ticks.append, np.log10, float Retorno: np.unique(ticks + [float(norm.vmax)]). |
| centered_legend(fig, handles, ncol=3, *, y=0.25, fontsize=9, row_step=0.045, full_width=False, center=0.535) | 76-91 | Chamadas efetivas: fig.canvas.get_renderer, FontProperties, enumerate, max, sum, range, len, fig.legend |
| render(z, muni, fields, code, titles, note, extent, *, stations=None, eligible=None, numeric=False, hatches=None, panel_layers=None, numeric_options=None, palette=None, surfaces=None, surface_legend=None, panel_shape=None, filename=None, figure_title=None, legend_categories=None, zone_layer=None, show_zones=True, station_overlay=None, atlas_scale=None, wind_directions=None, png_dpi=None) | 94-361 | lê dados; grava produtos; Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/cartografia_apendices.py, linhas 179-185.

```python
            xx,yy=np.meshgrid(gx,gy)
            values_grid=np.expm1(CloughTocher2DInterpolator(np.c_[surface['x'],surface['y']],np.log1p(values))(xx,yy))
            values_grid=np.ma.masked_invalid(np.clip(values_grid,0,float(values.max())))
            contours=ax.pcolormesh(xx,yy,values_grid,cmap=surface['cmap'],norm=surface['norm'],shading='gouraud',zorder=3,rasterized=True)
            vertices=[];commands=[]
            for polygon in getattr(municipality_union,'geoms',[municipality_union]):
                for ring in [polygon.exterior,*polygon.interiors]:
```

Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- log1p: Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/cenario_geral_pos_banca.py

Organiza a meteorologia completa e a matriz conjunta de máximos de 1 h, máximos de 24 h e média anual trienal dos dois poluentes, sem restringir a uma direção do vento.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\cenario_geral_pos_banca.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| analisar_espacial_direcoes | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| medias_horarias_verificadas | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| out_aermod_reader | Módulo autoral local; sua ficha está neste relatório. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| post_amostragem | Módulo autoral local; sua ficha está neste relatório. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/adi_ado_sum/'PM10.ADO' if pol == 'PM10' else 'PM25.ADO' — chamada p.read_text, linha 55.
- cache.with_name(cache.stem + '_manifesto.json') — chamada manifest.read_text, linha 79.
- E:/projeto/output/16_revisao_pos_banca/cenario_geral/eventos_{pol}_{period}.npz — chamada np.load, linha 80.

**Saídas.**

- E:/projeto/output/16_revisao_pos_banca/cenario_geral/envelope_{pol}_{period}.csv — chamada envelope.to_csv, linha 130.

**Campos e chaves lidos.**

- cells: X, Y.
- paths: ALL.
- check: concentration, from_1h.

**Campos e chaves gerados.**

- daily: day.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| excluded_days(pol) | 52-59 | lê dados Retorno: (result, p). |
| peak_from_valid(values, codes, valid) | 62-67 | Chamadas efetivas: v.argmax, np.asarray, len, ValueError, np.arange Retorno: (v[arg, np.arange(v.shape[1])], t[arg]). |
| load_general(pol, period, cells) | 70-141 | lê dados; grava produtos Retorno: result, {k: f[k] for k in f.files}. |
| run() | 144-146 | Chamadas efetivas: OUT.mkdir, spatial_run |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/cenario_geral_pos_banca.py, linhas 88-94.

```python
            if group=='ALL':yearly_full=pivot[[2021,2022,2023]].to_numpy().T
            selected=pd.DataFrame(xy,columns=['X','Y']).merge(pivot.mean(axis=1).rename('value').reset_index(),on=['X','Y'],validate='one_to_one')
            group_values.append(selected.value.to_numpy())
        index=pd.MultiIndex.from_arrays(coords.T).get_indexer(pd.MultiIndex.from_arrays(xy.T))
        if (index<0).any():raise ValueError('Receptor anual ausente')
        maximum=yearly_full.mean(axis=0);codes=np.zeros(len(coords),dtype=np.int64)
        yearly=yearly_full[:,index][:,None,:];counts=cal.groupby('year').valid.sum().to_numpy()[:,None]
```

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/censo_ibge.py

Censo ibge. Processamento ou módulo de apoio. A organização passa por _digits15, _first_existing, _download, ensure_official_inputs, load_sector_geometry, load_sector_attributes_xlsx, _read_preliminary_population, load_preliminary_population, _filter_census_chunks, _read_csv_file_filtered.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\censo_ibge.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| __future__ | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| alocacao_territorial_emissoes | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| io | Fluxos em memória para imagens, tabelas e documentos. |
| io_utils | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| shapely.ops | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| urllib.request | Requisições e manipulação de endereços de serviços públicos. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- _first_existing(censo_dir, ['setor_cong.shp', 'setor_cong.gpkg', 'setor_cong.geojson', '*setor*cong*.shp', '*setor*cong*.gpkg']) — chamada gpd.read_file, linha 144.
- _first_existing(Path(censo_dir), ['dicionario_de_dados_agregados_por_setores_censitarios*.xlsx', '*dicionario*dados*setores*censitarios*.xlsx']) — chamada pd.read_excel, linha 368.
- _first_existing(censo_dir, ['setor_cong.shp', 'setor_cong.gpkg', 'setor_cong.geojson', '*setor*cong*.shp', '*setor*cong*.gpkg']) — chamada pd.read_excel, linha 178.
- {fh} — chamada pd.read_csv, linha 214.
- _first_existing(censo_dir, ['setor_cong.shp', 'setor_cong.gpkg', 'setor_cong.geojson', '*setor*cong*.shp', '*setor*cong*.gpkg']) — chamada open, linha 237.
- {censo_dir}/demografia_congonhas_setores.csv — chamada pd.read_csv, linha 328.
- _first_existing(censo_dir, ['Agregados_por_setores_demografia_BR*.xlsx', '*setores*demografia*BR*.xlsx']) — chamada pd.read_excel, linha 345.
- _first_existing(censo_dir, ['Agregados_por_setores_basico_BR*.zip', '*setores*basico*BR*.zip']) — chamada zipfile.ZipFile, linha 306.
- zipfile.ZipFile(zip_path) — chamada zf.open, linha 307.

**Saídas.**

- dest.with_suffix(dest.suffix + '.part') — chamada open, linha 89.
- {censo_dir}/demografia_congonhas_setores.csv — chamada df.to_csv, linha 357.
- {out_root}/06_censo_ibge/LEIA-ME_censo_ibge.txt — chamada .write_text, linha 571.
- {out_root}/06_censo_ibge/censo_setores_congonhas.csv — chamada .to_csv, linha 623.
- {out_root}/06_censo_ibge/censo_populacao_por_zoneamento.csv — chamada zone_pop.to_csv, linha 624.
- {out_root}/06_censo_ibge/censo_alocacao_populacao_auditoria.csv — chamada pop_audit.to_csv, linha 625.
- {out_root}/06_censo_ibge/censo_variaveis_idade_identificadas.csv — chamada age_map.to_csv, linha 627.
- {out_root}/06_censo_ibge/censo_faixas_etarias_qc.csv — chamada .to_csv, linha 630.
- {out_root}/06_censo_ibge/censo_setores_congonhas.gpkg [camada 'setores'] — chamada sectors.to_file, linha 632.
- {out_root}/06_censo_ibge/LEIA-ME_dados_IBGE_idade.txt — chamada .write_text, linha 636.
- {out_root}/06_censo_ibge/censo_diagnostico.csv — chamada .to_csv, linha 670.

**Campos e chaves lidos.**

- g: CD_SETOR_NORM.
- df: CD_SETOR, CD_SETOR_NORM, V0001, V0007.
- dic: variable.
- x: variable.
- d: CD_SETOR_NORM, V01006, V01031, V01032, V01033, V01034, V01035, V01036, V01037, V01038, V01039, V01040, V01041.
- out: pop_0_4, pop_10_14, pop_5_9, pop_ge30.
- z.loc: zone_index.
- z: zone_index.
- sectors: POP_TOTAL, SETOR_AREA_KM2, pop_total_demografia.

**Campos e chaves gerados.**

- g: CD_SETOR_NORM, SETOR_AREA_KM2.
- df: CD_SETOR_NORM, DOM_PART_OCUP, POP_TOTAL.
- d: CD_SETOR_NORM.
- out: age_qc_1_10, age_qc_25_74, age_qc_30_99, age_qc_ge25, age_qc_ge30, age_qc_gt1, pop_0_4, pop_10_14, pop_15_19, pop_1_10, pop_20_24, pop_25_29, pop_25_74, pop_30_39, pop_30_99, pop_40_49, pop_50_59, pop_5_9, pop_60_69, pop_70mais, pop_ge25, pop_ge30, pop_gt1, pop_total_demografia.
- z: zone_index.
- agg: population_allocation_status.
- sectors: POP_DENS_KM2, POP_TOTAL.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| _digits15(value) | 72-74 | Chamadas efetivas: re.sub, str, .zfill Retorno: s[:15].zfill(15) if s else ''. |
| _first_existing(folder: Path, patterns) | 77-82 | Chamadas efetivas: sorted, folder.glob Retorno: None, hits[0]. |
| _download(url: str, dest: Path, timeout=60) | 85-96 | Chamadas efetivas: dest.parent.mkdir, dest.with_suffix, urllib.request.Request, tmp.replace, urllib.request.urlopen, open, resp.read, f.write Retorno: dest. |
| ensure_official_inputs(censo_dir: Path) | 99-136 | Chamadas efetivas: Path, ensure_dirs, getattr, targets.append, dest.exists, _download, downloads.append, str Retorno: downloads, downloads. |
| load_sector_geometry(censo_dir: Path) | 139-163 | lê dados Retorno: (g, path), (None, None). |
| load_sector_attributes_xlsx(censo_dir: Path) | 166-173 | lê dados Retorno: (df, p), (pd.DataFrame(), None). |
| _read_preliminary_population(path: Path) | 176-186 | lê dados Retorno: df. |
| load_preliminary_population(censo_dir: Path) | 189-197 | Chamadas efetivas: Path, _first_existing, _read_preliminary_population, pd.DataFrame Retorno: (_read_preliminary_population(p), p), (pd.DataFrame(), None). |
| _filter_census_chunks(reader_factory, sector_prefix=MUN_CODE) | 202-232 | lê dados Retorno: (pd.DataFrame(), None), (pd.concat(chunks, ignore_index=True) if chunks else pd.DataFrame(), encoding). |
| _read_csv_file_filtered(path: Path, sector_prefix=MUN_CODE) | 235-237 | Chamadas efetivas: Path, _filter_census_chunks, open Retorno: _filter_census_chunks(lambda: open(path, 'rb'), sector_prefix=sector_prefix)[0]. |
| load_final_basic(censo_dir: Path) | 240-294 | lê dados; grava produtos Retorno: (df, src), (df, cache). |
| _read_zip_csv_filtered(zip_path: Path, sector_prefix=MUN_CODE) | 297-320 | Chamadas efetivas: Path, _filter_census_chunks, zipfile.ZipFile, zf.open, _ZipMember, pd.DataFrame, zf.namelist, .endswith Retorno: df, _ZipMember(). |
| load_demography(censo_dir: Path) | 323-360 | lê dados; grava produtos Retorno: (df, src), (df, cache). |
| _dictionary_rows(censo_dir: Path) | 363-383 | lê dados Retorno: (pd.DataFrame(rows).drop_duplicates(['variable', 'description']), p), (pd.DataFrame(), None). |
| _age_from_description(desc: str) | 386-404 | Chamadas efetivas: .replace, re.search, int, m.group, .lower, str Retorno: None, None. |
| infer_age_variables(censo_dir: Path, demography_cols) | 407-445 | Chamadas efetivas: _dictionary_rows, .upper, .copy, dic.itertuples, .lower, re.search, _age_from_description, .drop_duplicates Retorno: (pd.DataFrame(rows).drop_duplicates('variable') if rows else pd.DataFrame(), path). |
| build_age_groups(demography: pd.DataFrame, age_map: pd.DataFrame) | 448-503 | Chamadas efetivas: demography.copy, pd.DataFrame, sumcols, next, .map, .startswith, .upper, str Retorno: out, pd.DataFrame(). |
| allocate_population_to_zones(sectors: gpd.GeoDataFrame, zones: gpd.GeoDataFrame, pop_cols) | 506-560 | Chamadas efetivas: .copy, zones.copy, s.itertuples, pd.DataFrame, .sum, all_zones.merge, set, z.iterrows Retorno: (agg, aud), (pd.DataFrame(), pd.DataFrame()). |
| run_census_module(zones, municipality, out_root: Path) | 563-671 | grava produtos Retorno: {'status': 'ok', 'zone_population': zone_pop, 'sectors': sectors, 'diagnostic': diag}, {'status': 'no_shape', 'zone_population': pd.DataFrame(), 'sectors': None}. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/censo_ibge.py, linhas 471-477.

```python
        cols = [c for c in cols if c in d.columns]
        return d[cols].sum(axis=1, min_count=1) if cols else pd.Series(np.nan, index=d.index)

    out["pop_total_demografia"] = d["V01006"] if "V01006" in d.columns else sumcols(age_vars)
    out["pop_0_4"] = d["V01031"] if "V01031" in d.columns else np.nan
    out["pop_5_9"] = d["V01032"] if "V01032" in d.columns else np.nan
    out["pop_10_14"] = d["V01033"] if "V01033" in d.columns else np.nan
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/censo_ibge.py, linhas 526-532.

```python
        pieces,outside,ambiguous,total = partition(geom,z,'área')
        allocated_fraction = sum(f for _,f,_ in pieces)
        for zid,frac,area in pieces:
            rec = {"CD_SETOR_NORM": sec_code, "zone_index": z.loc[zid,'zone_index'], "area_fraction": frac, "intersection_area_m2": area}
            for c in pop_cols:
                val = pd.to_numeric(pd.Series([getattr(sr, c, np.nan)]), errors="coerce").iloc[0]
                rec[c] = float(val) * frac if pd.notna(val) else np.nan
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/comparar_bpip_gerdau.py

Comparar bpip gerdau. Processamento ou módulo de apoio. A organização passa por bpi, params.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\comparar_bpip_gerdau.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| collections | Estruturas de contagem, agrupamento e coleções auxiliares. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- externos.downloads_f68ae09/{name} — chamada .read_text, linha 29.
- {path} — chamada path.read_text, linha 38.

**Saídas.**

- E:\projeto/output/14_auditoria_entradas/correcao_BPIP_FUNIT/comparacao_GERDAU.json — chamada out.write_text, linha 56.

**Campos e chaves lidos.**

- report: edificacoes_identicas.
- x: diferenca_maxima.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| bpi(name) | 28-34 | lê dados Retorno: (ls, stacks). |
| params(path) | 36-42 | lê dados Retorno: data. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/comparar_bpip_gerdau.py, linhas 58-62.

```python
print('Fontes correspondentes:',len(matches),'Sem correspondencia:',len(unmatched))
print('Fontes com parametros numericamente diferentes:',sum(any(x['diferenca_maxima'].values()) for x in matches))
for _,sid,v in sa:
    if sid.startswith('FLARE'):
        print(sid,v,[(t,w) for _,t,w in sb if w[2:]==v[2:]])
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/complementar_periodo_comum.py

Complementar periodo comum. Processamento ou módulo de apoio. A organização passa por run.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\complementar_periodo_comum.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| cartografia_apendices | Módulo autoral local; sua ficha está neste relatório. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| integrar_periodo_comum | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- {OUT}/zoneamento_periodo_comum.gpkg — chamada gpd.read_file, linha 40.
- E:/projeto/config.DIRS['out']/13_rateio_emissoes/Resumo_zonas.csv — chamada pd.read_csv, linha 41.
- E:/projeto/config.DIRS['out']/06_censo_ibge/censo_populacao_por_zoneamento.csv — chamada pd.read_csv, linha 50.
- E:/projeto/config.DIRS['out']/11_integracao/apendices/resumo_figuras.json — chamada .read_text, linha 60.

**Saídas.**

- {OUT}/zoneamento_periodo_comum.gpkg — chamada .to_file, linha 64.
- {OUT}/zoneamento_periodo_comum.csv — chamada .to_csv, linha 65.
- {OUT}/resumo_complementar_comum.json — chamada .write_text, linha 67.

**Campos e chaves lidos.**

- config.DIRS: out.
- mass: poluente.
- z: PM25_ANN_monitor, PM25_PV_origem, health_fraction_pct, pop_estimada, pop_ge30_estimada.
- z.loc: PM25_ANN_monitor.

**Campos e chaves gerados.**

- z: health_avoidable_deaths, health_period, pop_alocacao_status, pop_estimada, pop_ge30_estimada, pop_metodo_figura.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 39-67 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/complementar_periodo_comum.py, linhas 56-62.

```python
    for rr,col in [(1.08,'health_fraction_pct'),(1.06,'health_fraction_low_pct'),(1.11,'health_fraction_high_pct')]:
        z[col]=np.nan;z.loc[good,col]=100*(1-np.exp(-np.log(rr)/10*np.maximum(z.loc[good,'PM25_ANN_monitor']-5,0)))
    z['health_period']='2021-2023';z['health_avoidable_deaths']=np.nan
    cart.OUT=OUT
    extent=json.loads((config.DIRS['out']/'11_integracao/apendices/resumo_figuras.json').read_text(encoding='utf8'))['bounds_degrees']
    mun=gpd.GeoDataFrame(geometry=[z.geometry.union_all()],crs=z.crs)
    cart.render(z,mun,['PM10_quadrante_comum','PM25_quadrante_comum'],'C1',['MP₁₀ · emissão e concentração','MP₂,₅ · emissão e concentração'],'Emissão: massa total territorial, referência 2023. Concentração: integração 2021–2023, PI-2, critérios do estudo.',extent)
```

Função exponencial. No módulo sanitário, a fração potencialmente evitável é 1−exp(−β×ΔC), condicionada à função concentração-resposta e ao contrafactual.

Logaritmo natural. Na função de risco, β=ln(RR)/10 converte um risco relativo por 10 µg/m³ para a escala de 1 µg/m³.

**Cálculos a observar nesta rotina.**

- exp: Função exponencial. No módulo sanitário, a fração potencialmente evitável é 1−exp(−β×ΔC), condicionada à função concentração-resposta e ao contrafactual.
- log: Logaritmo natural. Na função de risco, β=ln(RR)/10 converte um risco relativo por 10 µg/m³ para a escala de 1 µg/m³.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/complementar_quintis_gestao.py

Calcula quintis, procura cortes de emissão associados a faixas de concentração e testa estabilidade em blocos espaciais. A associação não estabelece um limite causal ou legal de emissão.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\complementar_quintis_gestao.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| revisao_espacial_pos_banca | Módulo autoral local; sua ficha está neste relatório. |
| scipy | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.sparse.csgraph | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/16_revisao_pos_banca/celulas_analise.gpkg — chamada gpd.read_file, linha 79.
- E:/projeto/output/16_revisao_pos_banca/zoneamento_pos_banca.gpkg — chamada gpd.read_file, linha 79.
- E:/projeto/output/16_revisao_pos_banca/vinculo_celula_zona.csv — chamada pd.read_csv, linha 79.

**Saídas.**

- E:/projeto/output/16_revisao_pos_banca/{name}.gpkg — chamada frame.to_file, linha 123.
- E:/projeto/output/16_revisao_pos_banca/{name}.csv — chamada .to_csv, linha 123.
- E:/projeto/output/16_revisao_pos_banca/limiares_cinco_faixas_validacao.csv — chamada .to_csv, linha 124.
- E:/projeto/output/16_revisao_pos_banca/emissoes_por_faixa_concentracao.csv — chamada .to_csv, linha 124.
- E:/projeto/output/16_revisao_pos_banca/ABC_regioes_gestao.csv — chamada .to_csv, linha 124.
- E:/projeto/output/16_revisao_pos_banca/regioes_gestao_zoneamento.csv — chamada .to_csv, linha 124.
- E:/projeto/output/16_revisao_pos_banca/resumo_quintis_gestao.json — chamada .write_text, linha 125.

**Campos e chaves lidos.**

- cells: X, Y, receptor_id.
- v: kind.
- folds_here: basis, pollutant.
- links: receptor_id, zone_area_fraction, zone_index.
- z: zone_index.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| binary_cut(x, y) | 49-57 | Chamadas efetivas: np.asarray, np.argsort, sy.sum, np.arange, int, float, len, sy.cumsum Retorno: float((sx[idx] + sx[idx + 1]) / 2), np.nan. |
| balanced_accuracy(y, pred) | 60-62 | Chamadas efetivas: np.asarray, float, y.any, .any, .mean Retorno: float(0.5 * (pred[y].mean() + (~pred[~y]).mean())) if y.any() and (~y).any() else np.nan. |
| estimate_cuts(x, c, xy, pol, basis) | 65-75 | Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. Retorno: rows. |
| run() | 78-125 | lê dados; grava produtos; Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.; Identifica componentes conectados de uma rede de vizinhança. Une regiões espacialmente conectadas; não estima transporte físico. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/complementar_quintis_gestao.py, linhas 65-71.

```python
def estimate_cuts(x,c,xy,pol,basis):
    concentration_cuts=np.quantile(c,[.2,.4,.6,.8]);rows=[];folds=[]
    for size in [2000,4000]:
        b=np.floor((xy-xy.min(0))/size).astype(int);keys=list(map(tuple,b));unique=sorted(set(keys));np.random.default_rng(SEED).shuffle(unique);lookup={key:i%5 for i,key in enumerate(unique)};folds.append((size,np.array([lookup[v] for v in keys])))
    for percentile,ccut in zip([20,40,60,80],concentration_cuts):
        y=c>ccut;cut=binary_cut(x,y)
        for size,f in folds:
```

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

Trecho de codigo/complementar_quintis_gestao.py, linhas 85-91.

```python
            for i in range(1,6):
                vals=x[q==i];conditional.append({'pollutant':pol,'basis':basis,'concentration_band':i,'n':len(vals),'emission_min':vals.min(),'emission_p20':np.quantile(vals,.2),'emission_median':np.median(vals),'emission_p80':np.quantile(vals,.8),'emission_max':vals.max(),'concentration_low':float(c[q==i].min()),'concentration_high':float(c[q==i].max())})
        e=cells[pol+'_density_tpy_km2'].to_numpy();cuts=np.array([binary_cut(e,c>v) for v in ccuts]);ordered=bool(np.isfinite(cuts).all() and np.all(np.diff(cuts)>0))
        cells[pol+'_emission_associated_band']=np.searchsorted(cuts,e,side='left')+1 if ordered else np.nan
        eq_rank,ecuts=relative_quintile(e);eq=(cells[pol+'_emission_associated_band'].to_numpy().astype(int) if ordered else eq_rank);cells[pol+'_emission_rank_quintile']=eq_rank;cells[pol+'_emission_q']=eq

        e80=cuts[-1];cells[pol+'_matrix_associative']=np.where(q==5,'Alta C','Demais C')+' / '+np.where(e>e80,'Alta E','Demais E')
```

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- quantile: Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.
- connected_components: Identifica componentes conectados de uma rede de vizinhança. Une regiões espacialmente conectadas; não estima transporte físico.
- average: Média com ou sem pesos. As unidades do resultado são as da variável antes de eventual normalização.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/completar_emi_dia_tecnico.py

Acrescenta somente o dia meteorologico invalido, preservando bytes anteriores.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\completar_emi_dia_tecnico.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- {path} — chamada path.open, linha 79.
- E:/projeto/houremiss/AERMET-3Y.SFC — chamada .read_text, linha 47.
- E:/projeto/output/12_houremiss/Pacote_AERMOD_2021_2023.zip — chamada zipfile.ZipFile, linha 102.
- {src} — chamada src.open, linha 100.
- {dst} — chamada dst.open, linha 100.
- {z} — chamada z.open, linha 106.

**Saídas.**

- {path} — chamada path.open, linha 70.
- E:/projeto/output/12_houremiss/Pacote_AERMOD_2021_2023.atualizando.zip — chamada zipfile.ZipFile, linha 95.
- E:/projeto/output/12_houremiss/complemento_dia_tecnico_20240101.json — chamada .write_text, linha 109.

**Campos e chaves lidos.**

- r: arquivo.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| digest(path, limit=None) | 37-45 | Chamadas efetivas: hashlib.sha256, h.hexdigest, path.open, f.read, h.update, len, min Retorno: h.hexdigest(). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/completar_emi_dia_tecnico.py, linhas 37-45.

```python
def digest(path,limit=None):
    h=hashlib.sha256()
    with path.open('rb') as f:
        while limit is None or limit>0:
            b=f.read(1024*1024 if limit is None else min(limit,1024*1024))
            if not b:break
            h.update(b)
            if limit is not None:limit-=len(b)
    return h.hexdigest()
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/conciliar_nucleos_urbanos.py

Concilia totais municipais sem atribuir todo Congonhas apenas a Pires.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\conciliar_nucleos_urbanos.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| collections | Estruturas de contagem, agrupamento e coleções auxiliares. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/inventario/Resumo_Inventario_Congonhas_2023-R1.xlsx — chamada pd.read_excel, linha 49.
- E:/projeto/inventario/Resumo_Inventario_Congonhas_2023-R1.xlsx — chamada path.read_bytes, linha 71.
- E:/projeto/config.DIRS['out']/14_auditoria_entradas/revalidacao_final/fontes_correntes.json — chamada .read_text, linha 83.
- E:/projeto/config.DIRS['out']/14_auditoria_entradas/revalidacao_final/Massas_fontes_2021_2023.csv — chamada pd.read_csv, linha 84.
- E:/projeto/config.DIRS['out']/14_auditoria_entradas/revalidacao_final/validacao_final.json — chamada .read_text, linha 85.

**Saídas.**

- E:/projeto/config.DIRS['out']/15_auditoria_metodologica/conciliacao_nucleos_urbanos.csv — chamada .to_csv, linha 77.
- E:/projeto/config.DIRS['out']/14_auditoria_entradas/revalidacao_final/fontes_correntes.json — chamada .write_text, linha 87.
- E:/projeto/config.DIRS['out']/14_auditoria_entradas/revalidacao_final/Massas_fontes_2021_2023.csv — chamada .to_csv, linha 88.
- E:/projeto/config.DIRS['out']/14_auditoria_entradas/revalidacao_final/validacao_final.json — chamada .write_text, linha 89.

**Campos e chaves lidos.**

- x: diferenca_t_ano, id, massa_continua_t_ano, massa_inventario_t_ano, poluente, status.
- report: arquivos.
- config.DIRS: out.

**Campos e chaves gerados.**

- x: conciliação_nivel, inventario_ids, massa_alvo_t_ano, massa_inventario_conjunto_t_ano, massa_inventario_t_ano, memorial_corrigido, origem, status.
- report: conciliacao_nucleos_urbanos.
- : status.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| reconcile(records, annual, report) | 47-78 | lê dados; grava produtos Retorno: (records, annual, report). |
| run() | 81-90 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/conciliar_nucleos_urbanos.py, linhas 54-60.

```python
            assert len(sources)==len(ids)
            actual=sum(x['massa_continua_t_ano'] for x in sources)
            expected=float(inv.loc[road,col])+float(inv.loc[residential,col])
            assert np.isclose(actual,expected,rtol=1e-6,atol=1e-6),(pol,name,actual,expected)
            for x in sources:
                x['status']='conciliada';x['massa_inventario_t_ano']=None
                x['massa_inventario_conjunto_t_ano']=expected
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/config.py

Config. Processamento ou módulo de apoio. A organização passa por _resolve_project_root.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\config.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- DIRS: emission, grade_generated, limite_cong, limite_emp, qar, uso_terra, vias, zoneamento.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| _resolve_project_root() | 25-31 | Chamadas efetivas: _cp_raiz Retorno: _cp_raiz(). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/config.py, linhas 25-33.

```python
def _resolve_project_root() -> Path:
    """Resolve a raiz do projeto sem depender do diretório de execução.

    A pasta acima de codigo é a raiz, inclusive após migrações entre discos.
    EMI_PROJECT_ROOT permite uma substituição explícita para testes e executores.
    """
    return _cp_raiz()

BASE = _resolve_project_root()
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/consolidar_atributos_evidencia.py

Completa resumos dos receptores e explicita alcance da evidência por zona.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\consolidar_atributos_evidencia.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_indicadores_trienais_receptores.csv — chamada pd.read_csv, linha 41.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_vinculo_receptor_zona.csv — chamada pd.read_csv, linha 42.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{name}.gpkg — chamada gpd.read_file, linha 56.
- E:/projeto/descontinuado/datetime.now().strftime('%Y-%m-%d_%H%M%S_atributos_evidencia')/p.relative_to(config.BASE) — chamada dest.read_bytes, linha 77.

**Saídas.**

- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{name}.gpkg — chamada z.to_file, linha 78.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{name}.csv — chamada .to_csv, linha 78.
- E:/projeto/descontinuado/datetime.now().strftime('%Y-%m-%d_%H%M%S_atributos_evidencia')/manifesto.json — chamada .write_text, linha 81.
- E:/projeto/config.DIRS['out']/15_auditoria_metodologica/revisao_cientifica/consolidacao_atributos.json — chamada target.write_text, linha 83.

**Campos e chaves lidos.**

- config.DIRS: out.
- z: zone_index.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| summaries(pol) | 40-47 | lê dados Retorno: result. |
| run() | 50-84 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/consolidar_atributos_evidencia.py, linhas 59-65.

```python
                target=pol+'_'+col
                filled[target]=int(z[target].isna().sum()) if target in z else len(z)
                z[target]=z.zone_index.map(table[col])
            for scenario in ['PV','PF']:
                model_origin=z[f'{pol}_{scenario}_origem'].eq('modelagem')
                bad=z[f'{pol}_{scenario}_integrado'].eq('nao_atendimento')
                z[f'{pol}_{scenario}_alcance']=np.where(model_origin,
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/consolidar_emi_wg_scof.py

Intercala conjuntos HOUREMIS por hora sem modificar taxas ou IDs.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\consolidar_emi_wg_scof.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| contextlib | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- {path} — chamada path.open, linha 37.
- line.split() — chamada p.open, linha 58.
- final.with_suffix('.temporario') — chamada pending.open, linha 79.

**Saídas.**

- final.with_suffix('.temporario') — chamada pending.open, linha 59.
- E:/projeto/output/12_houremiss/sensibilidade_WG_SCOF_1h/consolidado/validacao_consolidacao.json — chamada .write_text, linha 92.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| first_ids(path) | 35-43 | Chamadas efetivas: path.open, len, line.split, ids.append, set, tuple, .decode, map Retorno: ids. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/consolidar_emi_wg_scof.py, linhas 35-43.

```python
def first_ids(path):
    ids=[]
    with path.open('rb') as f:
        for line in f:
            p=line.split()
            if tuple(map(int,p[2:6]))!=(2021,1,1,1):break
            ids.append(p[6].decode('ascii'))
    assert len(set(ids))==len(ids)
    return ids
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/consolidar_populacao_atual.py

Recalcula o suporte censitário sem dupla contagem em zonas sobrepostas.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\consolidar_populacao_atual.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| censo_ibge | Módulo autoral local; sua ficha está neste relatório. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/zoneamento_avaliacao_atual.gpkg — chamada gpd.read_file, linha 45.
- E:/projeto/config.DIRS['out']/06_censo_ibge/censo_setores_congonhas.gpkg — chamada gpd.read_file, linha 46.
- E:/projeto/config.DIRS['out']/06_censo_ibge/censo_populacao_por_zoneamento.csv — chamada pd.read_csv, linha 47.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{name}.gpkg — chamada gpd.read_file, linha 55.
- p.parent/'resumo_periodo_comum.json' if name == 'zoneamento_periodo_comum' else 'resumo_avaliacao_atual.json' — chamada summary_path.read_text, linha 67.

**Saídas.**

- E:/projeto/config.DIRS['out']/06_censo_ibge/censo_populacao_por_zoneamento.csv — chamada population.to_csv, linha 51.
- E:/projeto/config.DIRS['out']/06_censo_ibge/censo_alocacao_populacao_auditoria.csv — chamada audit.to_csv, linha 52.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{name}.gpkg — chamada z.to_file, linha 63.
- p.with_suffix('.csv') — chamada .to_csv, linha 63.
- p.parent/'resumo_periodo_comum.json' if name == 'zoneamento_periodo_comum' else 'resumo_avaliacao_atual.json' — chamada summary_path.write_text, linha 70.
- E:/projeto/config.DIRS['out']/06_censo_ibge/auditoria_populacao_consolidada.json — chamada .write_text, linha 83.

**Campos e chaves lidos.**

- config.DIRS: out.
- z: PM25_ANN_monitor, PM25_PV_origem, health_fraction_pct, pop_estimada, pop_ge30_estimada, zone_index.
- z.loc: PM25_ANN_monitor, zone_index.
- population.loc: zone_index.
- result: population_allocated, population_ambiguous, population_outside, population_source.

**Campos e chaves gerados.**

- z: pop_alocacao_status, pop_estimada, pop_ge30_estimada, pop_metodo_figura.
- summary: health, population.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 43-85 | lê dados; grava produtos Retorno: result. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/consolidar_populacao_atual.py, linhas 61-67.

```python
        for rr,col in [(1.08,'health_fraction_pct'),(1.06,'health_fraction_low_pct'),(1.11,'health_fraction_high_pct')]:
            z[col]=np.nan;z.loc[good,col]=100*(-np.expm1(-np.log(rr)/10*np.maximum(z.loc[good,'PM25_ANN_monitor']-5,0)))
        z.to_file(p,driver='GPKG');z.drop(columns='geometry').to_csv(p.with_suffix('.csv'),index=False)
        name_summary='resumo_periodo_comum.json' if name=='zoneamento_periodo_comum' else 'resumo_avaliacao_atual.json'
        summary_path=p.parent/name_summary
        if summary_path.exists():
            summary=json.loads(summary_path.read_text(encoding='utf8'))
```

Logaritmo natural. Na função de risco, β=ln(RR)/10 converte um risco relativo por 10 µg/m³ para a escala de 1 µg/m³.

**Cálculos a observar nesta rotina.**

- log: Logaritmo natural. Na função de risco, β=ln(RR)/10 converte um risco relativo por 10 µg/m³ para a escala de 1 µg/m³.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/consolidar_regioes_pos_banca.py

Regiões contíguas e ABC dos grupos em receptores HH, sem substituir o legado.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\consolidar_regioes_pos_banca.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| scipy | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.sparse.csgraph | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/16_revisao_pos_banca/celulas_analise.gpkg — chamada gpd.read_file, linha 39.
- E:/projeto/output/16_revisao_pos_banca/zoneamento_pos_banca.gpkg — chamada gpd.read_file, linha 39.

**Saídas.**

- E:/projeto/output/16_revisao_pos_banca/regioes_controle.gpkg — chamada regions.to_file, linha 65.
- E:/projeto/output/16_revisao_pos_banca/regioes_controle.csv — chamada .to_csv, linha 65.
- E:/projeto/output/16_revisao_pos_banca/ABC_regioes_contribuintes.csv — chamada .to_csv, linha 65.
- E:/projeto/output/16_revisao_pos_banca/regioes_zoneamento.csv — chamada .to_csv, linha 65.
- E:/projeto/output/16_revisao_pos_banca/resumo_regioes.json — chamada .write_text, linha 66.

**Campos e chaves lidos.**

- v: kind.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 38-66 | lê dados; grava produtos; Identifica componentes conectados de uma rede de vizinhança. Une regiões espacialmente conectadas; não estima transporte físico. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/consolidar_regioes_pos_banca.py, linhas 45-51.

```python
   pairs=sub.sindex.query(sub.geometry,predicate='touches');adj=sparse.coo_matrix((np.ones(pairs.shape[1]),pairs),shape=(len(sub),len(sub)))
   n,lab=connected_components(adj,directed=False)

   centres=sub.assign(component=lab).dissolve('component').centroid;order=sorted(range(n),key=lambda c:(centres.iloc[c].x,centres.iloc[c].y))
   for idx,component in enumerate(order,1):
    g=sub[lab==component];geom=g.geometry.union_all();rid=f'{pol}_{code}_{idx:02d}';area=g.area.to_numpy();total=float(np.average(g[pol+'_annual'],weights=area))
    records.append({'region_id':rid,'pollutant':pol,'classification':label,'n_receptors':len(g),'area_km2':geom.area/1e6,'annual_area_mean':total,'population_status':'Refinamento residencial pendente','geometry':geom})
```

Identifica componentes conectados de uma rede de vizinhança. Une regiões espacialmente conectadas; não estima transporte físico.

Média com ou sem pesos. As unidades do resultado são as da variável antes de eventual normalização.

**Cálculos a observar nesta rotina.**

- connected_components: Identifica componentes conectados de uma rede de vizinhança. Une regiões espacialmente conectadas; não estima transporte físico.
- average: Média com ou sem pesos. As unidades do resultado são as da variável antes de eventual normalização.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/consolidar_texto_auditoria_seminario.py

Revisão localizada e tabelas históricas compactas; preserva estilos do autor.

**Papel.** Histórico editorial: entrega de seminários encerrada. **Fonte inspecionada.** E:\projeto\codigo\consolidar_texto_auditoria_seminario.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| docx | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.enum.table | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.enum.text | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.oxml | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.oxml.ns | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.shared | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/10_avaliacao_rede/anuais_mma.csv — chamada pd.read_csv, linha 77.
- E:/projeto/output/10_avaliacao_rede/trienios_mma.csv — chamada pd.read_csv, linha 77.
- E:/projeto/output/11_integracao/nova_modelagem/estacoes_trienio_atual.csv — chamada pd.read_csv, linha 110.
- E:/projeto/output/15_auditoria_metodologica/auditoria_integrada.json — chamada .read_text, linha 160.

**Saídas.**

- E:/projeto/output/10_avaliacao_rede/tabela_resumida_{kind}.csv — chamada .to_csv, linha 102.
- (p := (FOLDER / 'Projeto_Ricardo-Queiroz_Entrega.docx')) — chamada d.save, linha 168.

**Campos e chaves lidos.**

- y: pollutant, station_id.
- current: pollutant, station_id.
- audit: health.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| replace(p, text) | 43-47 | Chamadas efetivas: p.add_run |
| table_style(t, widths, valid=None) | 50-73 | Chamadas efetivas: zip, enumerate, Inches, row._tr.get_or_add_trPr, pr.append, OxmlElement, c._tc.get_or_add_tcPr, cp.append |
| compact_tables(d) | 76-123 | lê dados; grava produtos Retorno: len(keys). |
| run() | 126-169 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/consolidar_texto_auditoria_seminario.py, linhas 43-51.

```python
def replace(p,text):
    if p.runs:
        p.runs[0].text=text
        for r in p.runs[1:]:r.text=''
    else:p.add_run(text)

# Table style
def table_style(t,widths,valid=None):
    t.autofit=False
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. Rotina histórica: conferir pré-condições e versão de dados antes de qualquer execução.

## codigo/corrigir_entrada_bpip_funit.py

Recupera resultados oficiais BPIP sem alterar emissoes ou dados fisicos.

**Papel.** Consolidação/migração: conferir pré-condições. **Fonte inspecionada.** E:\projeto\codigo\corrigir_entrada_bpip_funit.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| collections | Estruturas de contagem, agrupamento e coleções auxiliares. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- externos.pm10_adi_e342565 — chamada adi.read_bytes, linha 35.
- E:/projeto/temp/bpip_diagnostico/PM10.pro — chamada pro.read_text, linha 37.
- E:/projeto/output/14_auditoria_entradas/correcao_BPIP_FUNIT/PM10_BPIP_FUNIT_corrigido.ADI — chamada target.read_bytes, linha 86.

**Saídas.**

- E:/projeto/output/14_auditoria_entradas/correcao_BPIP_FUNIT/PM10_BPIP_FUNIT_corrigido.ADI — chamada target.write_bytes, linha 82.
- E:/projeto/output/14_auditoria_entradas/correcao_BPIP_FUNIT/BPIP_parametros_separados.INP — chamada .write_text, linha 83.
- E:/projeto/output/14_auditoria_entradas/correcao_BPIP_FUNIT/verificacao.json — chamada .write_text, linha 86.

**Campos e chaves lidos.**

- current: FPO48GER, XBADJ, YBADJ.
- official: FPO48GER, XBADJ, YBADJ.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| unaffected(ls) | 78-79 | Chamadas efetivas: l.split Retorno: [l for l in ls if not (l.split() and (l.split()[0] in ('POSTFILE', 'PLOTFILE') or (l.split()[0] in ('XBADJ', 'YBADJ') and l.split()[1] == 'FPO48GER')))]. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/corrigir_entrada_bpip_funit.py, linhas 78-86.

```python
def unaffected(ls):
    return [l for l in ls if not (l.split() and (l.split()[0] in ('POSTFILE','PLOTFILE') or (l.split()[0] in ('XBADJ','YBADJ') and l.split()[1]=='FPO48GER')))]
assert unaffected(lines)==unaffected(new)
target=out/'PM10_BPIP_FUNIT_corrigido.ADI'
target.write_bytes(('\r\n'.join(new)+'\r\n').encode('cp1252'))
(out/'BPIP_parametros_separados.INP').write_text('\n'.join(clean)+'\n',encoding='ascii')
shutil.copy2(pro,out/'PM10_BPIP_EPA.pro')
shutil.copy2(root/'temp/bpip_diagnostico/PM10.sup',out/'PM10_BPIP_EPA.sup')
(out/'verificacao.json').write_text(json.dumps(dict(entrada_original=str(adi),sha256_original=hashlib.sha256(original).hexdigest(),sha256_corrigido=hashlib.sha256(target.read_bytes()).hexdigest(),bpip_versao='04274 oficial EPA',x_faltantes=official['XBADJ','FPO48GER'][24:30],parametros_oficiais=official['YBADJ','FPO48GER'],unidades_removidas=unit_edits,emissoes_alteradas=False,simulacao_aermod_executada=False),indent=2),encoding='utf8')
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. Rotina histórica: conferir pré-condições e versão de dados antes de qualquer execução.

## codigo/criar_versoes_seminario.py

A leitura contém integralmente o texto da entrega; só muda a posição das figuras.

**Papel.** Histórico editorial: entrega de seminários encerrada. **Fonte inspecionada.** E:\projeto\codigo\criar_versoes_seminario.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| ajustar_blocos_figuras_docx | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| docx | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

- E:/projeto/output/09_projeto_dissertacao/seminarios_02/Projeto_Ricardo-Queiroz_Leitura.docx — chamada read.save, linha 108.
- E:/projeto/temp/qa_seminarios/integridade_texto_versoes.json — chamada .write_text, linha 109.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| normalize_reference(text) | 30-31 | Chamadas efetivas: re.sub Retorno: re.sub('\\b([A-I])\\s+(\\d+)\\b', '\\1\\2', text). |
| main_text(document) | 34-38 | Chamadas efetivas: list, next, enumerate, re.match, p.text.startswith, normalize_reference Retorno: [p.text for p in paras[start:end] if p.text and (not re.match('Figura [A-Z]\\d+\\s*[–-]', normalize_reference(p.text))) and (not p.text.startswith('Fonte:'))]. |
| run() | 41-110 | grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/criar_versoes_seminario.py, linhas 30-38.

```python
def normalize_reference(text):
    return re.sub(r'\b([A-I])\s+(\d+)\b',r'\1\2',text)

# Main text
def main_text(document):
    paras=list(document.paragraphs)
    start=next(i for i,p in enumerate(paras) if p.text=='INTRODUÇÃO/REVISÃO DA LITERATURA')
    end=next(i for i,p in enumerate(paras) if p.text=='CRONOGRAMA')
    return [p.text for p in paras[start:end] if p.text and not re.match(r'Figura [A-Z]\d+\s*[–-]',normalize_reference(p.text)) and not p.text.startswith('Fonte:')]
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. Rotina histórica: conferir pré-condições e versão de dados antes de qualquer execução.

## codigo/densidade_hectare.py

Suporte comum de 1 ha para áreas/volumes, com conservação da massa.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\densidade_hectare.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shapely | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/zoneamento_periodo_comum.gpkg — chamada gpd.read_file, linha 45.
- E:/projeto/config.DIRS['out']/13_rateio_emissoes/fontes_rateio_{pol}.gpkg — chamada gpd.read_file, linha 53.

**Saídas.**

- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_densidade_1ha.gpkg — chamada result.to_file, linha 66.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_maiores_densidades_1ha.csv — chamada .to_csv, linha 68.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_fontes_celula_maxima.csv — chamada contributors.to_csv, linha 71.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/auditoria_densidade_1ha.json — chamada .write_text, linha 73.

**Campos e chaves lidos.**

- config.DIRS: out.
- s: geometry, mass_inside, massa, source_area_m2, source_id, source_type.
- cells: cell_id, geometry.
- result: mass_allocated.

**Campos e chaves gerados.**

- s: mass_inside, source_area_m2.
- parts: mass_allocated.
- result: density_t_ha.
- top: x, y.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 44-73 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/densidade_hectare.py, linhas 60-66.

```python
        parts['mass_allocated']=parts.massa*parts.geometry.area/parts.source_area_m2
        mass=parts.groupby('cell_id').mass_allocated.sum()
        result=cells.merge(mass,on='cell_id',how='inner')
        result['density_t_ha']=result.mass_allocated
        result.geometry=result.geometry.intersection(mun)
        if not np.isclose(result.mass_allocated.sum(),s.mass_inside.sum(),rtol=1e-8,atol=1e-6):raise ValueError('Balanço da grade de 1 ha falhou')
        result.to_file(OUT/f'{pol}_densidade_1ha.gpkg',driver='GPKG')
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/diagnosticar_perfis_grupos.py

Extrai somente receptores das estações dos POST fixos e documenta identificabilidade.

**Papel.** Auditoria/diagnóstico. **Fonte inspecionada.** E:\projeto\codigo\diagnosticar_perfis_grupos.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| io | Fluxos em memória para imagens, tabelas e documentos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| medias_horarias_verificadas | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| out_aermod_reader | Módulo autoral local; sua ficha está neste relatório. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- {path} — chamada path.open, linha 59.
- io.BytesIO(subset.tobytes()) — chamada pd.read_csv, linha 71.
- E:/projeto/output/15_auditoria_metodologica/revisao_cientifica/vinculos_estacoes_receptores.csv — chamada pd.read_csv, linha 76.
- E:/projeto/adi_ado_sum/'PM10.ADI' if pol == 'PM10' else 'PM25.ADI' — chamada adi.read_text, linha 80.
- E:/projeto/output/13_rateio_emissoes/fontes_rateio_{pol}.gpkg — chamada gpd.read_file, linha 96.
- E:/projeto/output/09_projeto_dissertacao/seminarios_02/apresentacao/apoio_meteorologia_perfis/pares_horarios_{pol}.csv — chamada pd.read_csv, linha 102.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/{pol}_{group}_cache.json — chamada meta.read_text, linha 106.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/{pol}_{group}_estacoes.csv.gz — chamada pd.read_csv, linha 106.

**Saídas.**

- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/{pol}_grupos_estaticos_auxiliares.INC — chamada .write_text, linha 95.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/{pol}_grupos_estaticos_auxiliares.csv — chamada .to_csv, linha 95.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/{pol}_{group}_estacoes.csv.gz — chamada d.to_csv, linha 108.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/{pol}_{group}_cache.json — chamada meta.write_text, linha 108.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/perfis_normalizados_grupos_estacoes.csv — chamada .to_csv, linha 113.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/diagnostico_concordancia_grupos.csv — chamada .to_csv, linha 113.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/distancias_grupos_estacoes.csv — chamada .to_csv, linha 113.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/grupos_fontes_horarias_e_estaticas.csv — chamada .to_csv, linha 113.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/manifesto.json — chamada .write_text, linha 114.

**Campos e chaves lidos.**

- cal.loc: CODE.
- stations: pollutant.
- observed: CODE.
- d: CODE.

**Campos e chaves gerados.**

- groups: ALL.
- d: hour.
- p: group_id, group_norm, observed_norm, pollutant, station_id.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| station_records(path, stations) | 56-71 | lê dados Retorno: d.merge(stations, on=['X', 'Y'], validate='many_to_one'). |
| run() | 74-114 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/diagnosticar_perfis_grupos.py, linhas 98-104.

```python
            geom=g.geometry.union_all();weight=np.maximum(g.massa.to_numpy(),0);centers=g.geometry.centroid
            if weight.sum():cx=np.average(centers.x,weights=weight);cy=np.average(centers.y,weights=weight)
            else:cx=geom.centroid.x;cy=geom.centroid.y
            for r in st.itertuples():distances.append({'pollutant':pol,'group_id':group,'station_id':r.station_id,'distance_min_geometry_km':geom.distance(Point(r.X,r.Y))/1000,'distance_emission_centroid_km':np.hypot(cx-r.X,cy-r.Y)/1000,'bearing_station_to_emission_centroid':np.rad2deg(np.arctan2(cx-r.X,cy-r.Y))%360})
        observed=pd.read_csv(config.BASE/f'output/09_projeto_dissertacao/seminarios_02/apresentacao/apoio_meteorologia_perfis/pares_horarios_{pol}.csv',usecols=['station_id','CODE','observed']);observed=observed[observed.CODE.isin(good)]
        for (group,period),path in selected.items():
            if period!='1H':continue
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Média com ou sem pesos. As unidades do resultado são as da variável antes de eventual normalização.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- average: Média com ou sem pesos. As unidades do resultado são as da variável antes de eventual normalização.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/diagnostico_grupos_periodo.py

Comparação descritiva de grupos nas mesmas datas, sem chamá-la anual.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\diagnostico_grupos_periodo.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| integracao_metodologica | Módulo autoral local; sua ficha está neste relatório. |
| methodology_rules | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| common_period(zones, pol) | 28-55 | Chamadas efetivas: load_groups, sorted, max, min, .size, .reset_index, .merge, point_gdf Retorno: (pd.Series(dominant), pd.DataFrame(rows), dict(start=str(start), end=str(end), expected_days=expected, n_zones=len(dominant), n_groups=len(ids), closure_min=float(np.nanmin(closure)), closure_max=floa. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/diagnostico_grupos_periodo.py, linhas 43-49.

```python
    valid=count[count.ge(.75*expected)].rename('n_days').reset_index()
    means=joined.groupby(['X','Y'])[cols].mean().reset_index().merge(valid,on=['X','Y'])
    pts=point_gdf(means);rows=[];dominant={};closure=[]
    for zid,zone in zones.iterrows():
        p=pts[pts.geometry.covered_by(zone.geometry)]
        if p.empty:continue
        v=p[ids].mean().sort_values(ascending=False);total=v.sum()
```

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/diagnostics.py

Diagnostics. Auditoria/diagnóstico. A organização passa por project_file_diagnostics, write_method_notes, write_epa_validation_notes, epa_calculation_checklist.

**Papel.** Auditoria/diagnóstico. **Fonte inspecionada.** E:\projeto\codigo\diagnostics.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| __future__ | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| aermod_post | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| io_utils | Módulo autoral local; sua ficha está neste relatório. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

- {path} — chamada path.write_text, linha 103.

**Campos e chaves lidos.**

- config.FILES: enterprises, landuse_1985, landuse_2024, municipality, roads, sources_PM10, sources_PM25, station_coords, zoning.
- config.DIRS: emission, limite_cong, limite_emp, post, qar, uso_terra, vias, zoneamento.
- station_metrics.loc: station_id.
- station_metrics: pollutant.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| project_file_diagnostics(station_metrics=None) | 34-66 | Chamadas efetivas: pd.DataFrame, first_existing, rows.append, discover_post_main, discover_group_posts_any, .nunique, inspect_pos_header, str Retorno: pd.DataFrame(rows). |
| write_method_notes(path: Path) | 69-88 | grava produtos |
| write_epa_validation_notes(path: Path) | 91-103 | grava produtos |
| epa_calculation_checklist() | 106-125 | Chamadas efetivas: pd.DataFrame Retorno: pd.DataFrame([{'tema': 'PM2,5 - média diária', 'implementacao': 'dia válido com >=16 h válidas', 'referencia': '2/3 das médias horárias válidas no dia — MMA 2020', 'status': 'alinhado'}, {'tema': 'PM2. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/diagnostics.py, linhas 34-42.

```python
def project_file_diagnostics(station_metrics=None):
    rows = []

    checks = [
        ("limite_cong", config.FILES["municipality"], config.DIRS["limite_cong"], ["*.kml", "*.kmz", "*.shp"]),
        ("limite_emp", config.FILES["enterprises"], config.DIRS["limite_emp"], ["*.kmz", "*.kml", "*.shp"]),
        ("vias", config.FILES["roads"], config.DIRS["vias"], ["*.shp", "*.gpkg"]),
        ("zoneamento", config.FILES["zoning"], config.DIRS["zoneamento"], ["*.shp", "*.gpkg"]),
        ("station_id", config.FILES["station_coords"], config.DIRS["qar"], ["*station*id*.xlsx"]),
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/dispersion_contours.py

Dispersion contours. Processamento ou módulo de apoio. A organização passa por _folders_for_pol, _period_patterns, discover_contours, load_contours.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\dispersion_contours.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| __future__ | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| io_utils | Módulo autoral local; sua ficha está neste relatório. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| _folders_for_pol(pol: str) | 30-33 | Organiza parâmetros, expressões ou retorno sem chamada externa. Retorno: ['PM2-5', 'PM25', 'PM2_5'], ['PM10']. |
| _period_patterns(period: str) | 36-39 | Chamadas efetivas: .startswith, period.upper Retorno: ['Anual', 'ANUAL', 'Annual', 'annual'], ['24H', '24h', '24_H', '24-H']. |
| discover_contours(base_dir: Path, pol: str, period: str) | 42-64 | Chamadas efetivas: _folders_for_pol, _period_patterns, base_dir.rglob, .replace, candidates.append, any, sorted, .lower Retorno: sorted(candidates)[0] if candidates else None. |
| load_contours(base_dir: Path, pol: str, period: str) | 67-75 | Chamadas efetivas: discover_contours, read_vector, .copy, gdf.geometry.notna Retorno: (gdf, p), (None, None). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/dispersion_contours.py, linhas 30-38.

```python
def _folders_for_pol(pol: str):
    if pol == 'PM10':
        return ['PM10']
    return ['PM2-5', 'PM25', 'PM2_5']

# Period patterns
def _period_patterns(period: str):
    if period.upper().startswith('24'):
        return ['24H', '24h', '24_H', '24-H']
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/documentar_outros_codigos.py

Documentar outros codigos. Documentação/apoio. A organização passa por rec_for, main.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\projeto\codigo\documentar_outros_codigos.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| documentar_portabilidade | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| subprocess | Chamada de outros programas e verificação de seus resultados de execução. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- info['raiz']/temp/preparacao_20261114/inventario_antes.json — chamada .read_text, linha 58.
- {p} — chamada p.open, linha 80.

**Saídas.**

- {p} — chamada p.write_text, linha 111.
- info['raiz']/codigo/caminhos_projeto.json — chamada .write_text, linha 123.
- info['raiz']/temp/preparacao_20261114/portabilidade_outros.json — chamada .write_text, linha 124.

**Campos e chaves lidos.**

- parsed: calls, comments, errors, functions, imports, paramEnd, source, strings.
- x: args, end, endline, expandable, kind, line, name, start, value.
- info: raiz.
- cfg: externos.
- c: end, start.
- f: name, start.
- e: caminho.
- r: projeto.

**Campos e chaves gerados.**

- rec: chamadas, funcoes, imports.
- e: caminho.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| rec_for(p, root, parsed) | 42-52 | Chamadas efetivas: d.inspecionar_outro, .split, .append Retorno: rec. |
| main() | 55-125 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/documentar_outros_codigos.py, linhas 42-50.

```python
def rec_for(p,root,parsed):
    rec=d.inspecionar_outro(p,root)
    if p.suffix=='.mjs':
        rec['imports']=parsed['imports']
        rec['funcoes']=[{'nome':x['name'],'linha':x['line'],'fim':x['endline'],'argumentos':'','doc':''} for x in parsed['functions']]
        rec['chamadas']=[{'chamada':x['name'],'linha':x['line']} for x in parsed['calls']]
        for x in parsed['calls']:
            name=x['name'].split('.')[-1]
            mode='entradas' if name in ['readFileSync','readFile','load','importPptx'] else 'saidas' if name in ['writeFile','writeFileSync','save','exportPptx','export','finalizePresentation'] else None
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/documentar_portabilidade.py

Documentar portabilidade. Documentação/apoio. A organização passa por sha, fontes, ler, nome_chave, nome_expr, strnode, inspecionar_python, inspecionar_outro, preparar_config, interno.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\projeto\codigo\documentar_portabilidade.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| argparse | Parâmetros fornecidos ao iniciar o programa. |
| ast | Inspeção/transformação da sintaxe Python sem executar o processamento científico. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| io | Fluxos em memória para imagens, tabelas e documentos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| subprocess | Chamada de outros programas e verificação de seus resultados de execução. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| tokenize | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |


**Entradas.**

- {path} — chamada path.read_bytes, linha 51.
- {path} — chamada path.read_text, linha 68.
- {root}/codigo/caminhos_projeto.json — chamada file.read_text, linha 365.

**Saídas.**

- {root}/codigo/caminhos_projeto.json — chamada file.write_text, linha 377.
- {root}/codigo/caminhos_{key}{suffix} — chamada path.write_text, linha 382.
- args.raiz if args.raiz and len(chosen) == 1 else info['raiz']/temp/preparacao_20261114/inventario_antes.json — chamada .write_text, linha 520.
- args.raiz if args.raiz and len(chosen) == 1 else info['raiz']/rec['arquivo'] — chamada p.write_text, linha 533.
- args.raiz if args.raiz and len(chosen) == 1 else info['raiz']/temp/preparacao_20261114/portabilidade_python.json — chamada .write_text, linha 535.

**Campos e chaves lidos.**

- info: fontes, raiz.
- r: caminho, chamada, expressao, parametros, valor.
- rec: arquivo, caminhos_absolutos, campos_gerados, campos_lidos, entradas, linguagem, saidas.
- item: valor.
- cfg: ambiente, externos.
- x: caminhos_ajustados.

**Campos e chaves gerados.**

- item: caminho, expressao.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| sha(path) | 51-51 | lê dados Retorno: hashlib.sha256(path.read_bytes()).hexdigest(). |
| fontes(root, info) | 53-64 | Chamadas efetivas: set, found.update, sorted, os.walk, p.exists, root.iterdir, .lower, Path Retorno: sorted(found, key=lambda p: p.relative_to(root).as_posix().lower()). |
| ler(path) | 66-68 | lê dados Retorno: path.read_text('utf-8-sig'), path.read_text('cp1252'). |
| nome_chave(s) | 70-72 | Chamadas efetivas: Path, s.replace, .hexdigest, .lower, hashlib.sha1, .strip, s.encode, re.sub Retorno: re.sub('[^a-zA-Z0-9]+', '_', stem).strip('_').lower()[:45] + '_' + hashlib.sha1(s.encode()).hexdigest()[:7]. |
| nome_expr(node) | 74-77 | Chamadas efetivas: isinstance, nome_expr Retorno: '', node.id. |
| strnode(node) | 79-81 | Chamadas efetivas: ast.unparse Retorno: ast.unparse(node), '?'. |
| inspecionar_python(path, root, source=None) | 84-171 | Chamadas efetivas: ast.parse, set, ast.walk, sorted, ler, str, id, isinstance Retorno: {'arquivo': path.relative_to(root).as_posix(), 'linguagem': 'Python', 'sha256': sha(path), 'linhas': len(source.splitlines()), 'doc': ast.get_docstring(tree) or '', 'imports': sorted(set(imports)), 'f. |
| inspecionar_outro(path, root) | 173-175 | Chamadas efetivas: ler, re.findall, .as_posix, .get, sha, len, s.splitlines, path.relative_to Retorno: {'arquivo': path.relative_to(root).as_posix(), 'linguagem': {'.mjs': 'JavaScript', '.ps1': 'PowerShell', '.bat': 'Batch'}.get(path.suffix, path.suffix), 'sha256': sha(path), 'linhas': len(s.splitlines. |
| preparar_config(root, key, info, records) | 363-383 | lê dados; grava produtos Retorno: cfg. |
| interno(value, root) | 385-389 | Chamadas efetivas: value.replace, root.as_posix, .startswith, normalized.lower, prefix.lower, len Retorno: None, ''. |
| offsets(source) | 391-395 | Chamadas efetivas: source.splitlines, starts.append, len, .decode, .encode Retorno: at, starts[line - 1] + len(lines[line - 1].encode('utf8')[:col].decode('utf8')). |
| strip_comments(source) | 397-404 | Chamadas efetivas: source.splitlines, list, reversed, starts.append, .strip, tokenize.generate_tokens, len, re.sub Retorno: re.sub('\\n{3,}', '\n\n', '\n'.join((x.rstrip() for x in ''.join(chars).splitlines()))).strip() + '\n'. |
| cabecalho(rec, key) | 407-433 | Chamadas efetivas: .items, .union, meanings.items, lines.append, .startswith, .name.startswith, any, .join Retorno: '\n'.join((prefix + line for line in lines)) + '\n'. |
| bootstrap_py(key) | 435-447 | Organiza parâmetros, expressões ou retorno sem chamada externa. Retorno: f"# INÍCIO DOS CAMINHOS PORTÁTEIS\nimport sys as _cp_sys\nfrom pathlib import Path as _cp_Path\n_cp_file = _cp_Path(globals().get('__file__', _cp_Path.cwd() / 'codigo' / 'script.py')).resolve()\nfor _. |
| adaptar_python(path, root, key, rec) | 449-503 | grava produtos Retorno: (result, entries), None. |
| inspecionar_projeto(root, info) | 505-511 | Chamadas efetivas: fontes, p.name.startswith, records.append, inspecionar_python, inspecionar_outro, .as_posix, str, p.relative_to Retorno: records. |
| main() | 514-536 | grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/documentar_portabilidade.py, linhas 535-538.

```python
        (work/'portabilidade_python.json').write_text(json.dumps(planned,ensure_ascii=False,indent=2),encoding='utf8')
        print(json.dumps({'projeto':key,'scripts':len(records),'python':len(planned),'substituicoes':sum(x['caminhos_ajustados'] for x in planned),'aplicado':args.aplicar,'externos':len(cfg['externos'])},ensure_ascii=True),flush=True)

if __name__=='__main__':main()
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/empacotar_visualizador_privado.py

Armazena as prévias em volumes pequenos e oferece um ZIP pronto de leitura.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\empacotar_visualizador_privado.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- E:/projeto/dissertacao/visualizador/catalogo.json — chamada .read_text, linha 28.

**Saídas.**

- E:/projeto/output/16_revisao_pos_banca/visualizador/Visualizador_Congonhas.zip — chamada zipfile.ZipFile, linha 43.

**Campos e chaves lidos.**

- data: catalog.
- item: src.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| package() | 27-47 | lê dados; grava produtos Retorno: (target, names). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/empacotar_visualizador_privado.py, linhas 27-35.

```python
def package():
    data=json.loads((REPO/'catalogo.json').read_text(encoding='utf8'));parts=REPO/'partes';parts.mkdir(exist_ok=True)
    batches=[];batch=[];size=0
    for item in data['catalog']:
        p=OUT/item['src'];n=p.stat().st_size
        if batch and size+n>1_750_000:batches.append(batch);batch=[];size=0
        batch.append((p,item['src']));size+=n
    if batch:batches.append(batch)
    names=[]
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/Executar_Autoteste.bat

Executar Autoteste. Processamento ou módulo de apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\Executar_Autoteste.bat.

**Bibliotecas e dependências.**

Não há importação Python/JavaScript declarada; conferir programas acionados e comandos do arquivo.

**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/Executar_Autoteste.bat, linhas 9-17.

```text
@echo off
set "CODE_DIR=%~dp0"
REM Raiz e caminhos definidos em caminhos_projeto.json
cd /d "%CODE_DIR%"
if exist .venv\Scripts\python.exe (
  .venv\Scripts\python.exe autoteste_metodologia.py
) else (
  python autoteste_metodologia.py
)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/Executar_Avaliacao_Rede.bat

Executar Avaliacao Rede. Processamento ou módulo de apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\Executar_Avaliacao_Rede.bat.

**Bibliotecas e dependências.**

Não há importação Python/JavaScript declarada; conferir programas acionados e comandos do arquivo.

**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/Executar_Avaliacao_Rede.bat, linhas 9-17.

```text
@echo off
chcp 65001 >nul
set "CODE_DIR=%~dp0"
REM Raiz e caminhos definidos em caminhos_projeto.json
cd /d "%CODE_DIR%"
if not exist .venv\Scripts\python.exe (
  echo Ambiente ausente. Execute Executar_Projeto.bat para preparar dependencias.
  pause
  exit /b 1
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/Executar_Mapas_Apendices.bat

Executar Mapas Apendices. Cartografia/apresentação. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\Executar_Mapas_Apendices.bat.

**Bibliotecas e dependências.**

Não há importação Python/JavaScript declarada; conferir programas acionados e comandos do arquivo.

**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/Executar_Mapas_Apendices.bat, linhas 9-17.

```text
@echo off
cd /d "%~dp0"
"%~dp0.venv\Scripts\python.exe" "%~dp0mapas_apendices.py"
if errorlevel 1 (
  echo Erro na geracao. Consulte a mensagem acima.
  pause
  exit /b 1
)
echo Figuras salvas em E:\projeto\output\11_integracao\apendices
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/Executar_Projeto.bat

Executar Projeto. Processamento ou módulo de apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\Executar_Projeto.bat.

**Bibliotecas e dependências.**

Não há importação Python/JavaScript declarada; conferir programas acionados e comandos do arquivo.

**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/Executar_Projeto.bat, linhas 9-17.

```text
@echo off
chcp 65001 >nul
set "CODE_DIR=%~dp0"
REM Raiz e caminhos definidos em caminhos_projeto.json
cd /d "%CODE_DIR%"
if not exist .venv\Scripts\python.exe (
    echo Criando ambiente virtual...
    py -m venv .venv
    if errorlevel 1 (
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/Executar_Revisao_Pos_Banca.bat

Executar Revisao Pos Banca. Processamento ou módulo de apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\Executar_Revisao_Pos_Banca.bat.

**Bibliotecas e dependências.**

Não há importação Python/JavaScript declarada; conferir programas acionados e comandos do arquivo.

**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/Executar_Revisao_Pos_Banca.bat, linhas 9-17.

```text
@echo off
cd /d "%~dp0"
py -3.14 revisao_espacial_pos_banca.py
if errorlevel 1 exit /b 1
py -3.14 preparar_continuidade_pos_banca.py
if errorlevel 1 exit /b 1
py -3.14 consolidar_regioes_pos_banca.py
if errorlevel 1 exit /b 1
py -3.14 figuras_pos_banca.py
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/Executar_Webservice.bat

Executar Webservice. Processamento ou módulo de apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\Executar_Webservice.bat.

**Bibliotecas e dependências.**

Não há importação Python/JavaScript declarada; conferir programas acionados e comandos do arquivo.

**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/Executar_Webservice.bat, linhas 9-17.

```text
@echo off
set "CODE_DIR=%~dp0"
REM Raiz e caminhos definidos em caminhos_projeto.json
cd /d "%CODE_DIR%"
if not exist .venv (
  echo Ambiente virtual nao encontrado. Rode primeiro Executar_Projeto.bat.
  pause
  exit /b 1
)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/exportar_docx_preparacao.ps1

Exportar docx preparacao. Documentação/apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\projeto\codigo\exportar_docx_preparacao.ps1.

**Bibliotecas e dependências.**

Não há importação Python/JavaScript declarada; conferir programas acionados e comandos do arquivo.

**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/exportar_docx_preparacao.ps1, linhas 9-17.

```text
param([Parameter(Mandatory=$true)][string]$ListaArquivos)
. (Join-Path $PSScriptRoot 'caminhos_congonhas.ps1')

$ErrorActionPreference='Stop'


$items=Get-Content -LiteralPath $ListaArquivos -Raw -Encoding UTF8 | ConvertFrom-Json
$word=New-Object -ComObject Word.Application
$word.Visible=$false
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/exportar_grade_aermod_atual.py

Reexporta a grade consolidada, sem alterar as coordenadas ou gerar novos pontos.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\exportar_grade_aermod_atual.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- Path(__file__).resolve().parents[1]/output/07_grade_receptores/grade_receptores_adaptativa.csv — chamada .open, linha 34.
- Path(__file__).resolve().parents[1]/output/07_grade_receptores/grade_diagnostico_por_setor.csv — chamada .open, linha 35.
- Path(__file__).resolve().parents[1]/output/07_grade_receptores/grade_manifesto.json — chamada .read_text, linha 53.

**Saídas.**

- {target}/{name} — chamada .write_text, linha 46.
- {target}/grade_manifesto.json — chamada .write_text, linha 59.
- Path(__file__).resolve().parents[1]/output/07_grade_receptores/ULTIMA_GRADE_GERADA.json — chamada .write_text, linha 60.
- Path(__file__).resolve().parents[1]/grade/gerada/LEIA-ME_ENTRADA_AERMOD.md — chamada .write_text, linha 75.

**Campos e chaves lidos.**

- r: n_receptors_linked, receptor_id, utm_x, utm_y.

**Campos e chaves gerados.**

- manifest: reexport_note, reexported_at, standard_inputs, terrain_processed.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| migrate(value) | 48-52 | Chamadas efetivas: isinstance, value.replace, _cp_externo, str, migrate, value.items Retorno: value, value.replace(_cp_externo('projeto_fa81bd8'), str(BASE)). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/exportar_grade_aermod_atual.py, linhas 48-56.

```python
def migrate(value):
 if isinstance(value,str):return value.replace(_cp_externo('projeto_fa81bd8'),str(BASE))
 if isinstance(value,dict):return {k:migrate(v) for k,v in value.items()}
 if isinstance(value,list):return [migrate(v) for v in value]
 return value
manifest=migrate(json.loads((folder/'grade_manifesto.json').read_text(encoding='utf-8')))
manifest['reexported_at']=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3))).isoformat()
manifest['reexport_note']='Coordenadas originais preservadas; exportação padrão RE e atualização dos caminhos. Não representa nova otimização espacial nem processamento AERMAP.'
manifest['terrain_processed']=False
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/exportar_perfis_estaticos.py

Exporta fatores completos fornecidos no CSV, sem modificar o cenário ativo.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\exportar_perfis_estaticos.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| argparse | Parâmetros fornecidos ao iniciar o programa. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- {csv} — chamada pd.read_csv, linha 34.
- E:/projeto/adi_ado_sum/{pol}.ADI — chamada .read_text, linha 48.

**Saídas.**

- {out}/{pol}_perfis_estaticos_EMISFACT.INC — chamada .write_text, linha 65.

**Campos e chaves lidos.**

- d: factor, pollutant.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run(csv, out) | 31-66 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/exportar_perfis_estaticos.py, linhas 40-46.

```python
        values=g.sort_values('hour_start').factor.to_numpy()
        if (values<0).any() or not np.isclose(values.mean(),1,atol=1e-8):raise ValueError('Fatores precisam ser não negativos e ter média diária 1')
        vectors[pol,group]=values
    for pol,group in vectors:
        other='PM25' if pol=='PM10' else 'PM10'
        if (other,group) in vectors and not np.allclose(vectors[pol,group],vectors[other,group],atol=1e-8):raise ValueError('Mesmo grupo tem perfis diferentes entre poluentes; desagregar processos antes da exportação')
    out.mkdir(exist_ok=True,parents=True)
```

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/exportar_textos.ps1

Exportar textos. Processamento ou módulo de apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\exportar_textos.ps1.

**Bibliotecas e dependências.**

Não há importação Python/JavaScript declarada; conferir programas acionados e comandos do arquivo.

**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/exportar_textos.ps1, linhas 10-15.

```text
. (Join-Path $PSScriptRoot 'caminhos_congonhas.ps1')
$ErrorActionPreference='Stop'
$taskPython=Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
if(-not(Test-Path -LiteralPath $taskPython)){throw 'Python editorial indisponível. Use Python com lxml e Quarto instalados.'}
& $taskPython (Get-PortablePath 'dissertacao/ferramentas/gerar.py')
if($LASTEXITCODE -ne 0){throw 'A geração não foi concluída; consulte a mensagem acima.'}
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/figuras_analises_direcionais.py

Pranchas das análises de cada direção no encarte cartográfico consolidado.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\figuras_analises_direcionais.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| argparse | Parâmetros fornecidos ao iniciar o programa. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| cartografia_apendices | Módulo autoral local; sua ficha está neste relatório. |
| concurrent.futures | Execução concorrente quando prevista pela rotina; não equivale a um novo método de cálculo. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| paleta_concentracoes | Módulo autoral local; sua ficha está neste relatório. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| subprocess | Chamada de outros programas e verificação de seus resultados de execução. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/16_revisao_pos_banca/vento/{pol}_envelopes_{'horarios' if period == '1h' else 'diarios_persistentes'}.csv — chamada pd.read_csv, linha 103.
- E:/projeto/output/16_revisao_pos_banca/zoneamento_pos_banca.gpkg — chamada gpd.read_file, linha 246.
- E:/projeto/output/16_revisao_pos_banca/celulas_analise.gpkg — chamada gpd.read_file, linha 119.
- E:/projeto/output/11_integracao/apendices/resumo_figuras.json — chamada .read_text, linha 247.
- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/resumo.json — chamada .read_text, linha 122.
- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/comparacao_agrupamentos.csv — chamada pd.read_csv, linha 124.
- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/correlogramas.csv — chamada pd.read_csv, linha 124.
- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/limiares_cinco_faixas.csv — chamada pd.read_csv, linha 124.
- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/regioes_direcionais.csv — chamada pd.read_csv, linha 125.
- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/ABC_contribuicoes_regioes.csv — chamada pd.read_csv, linha 125.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/perfis_normalizados_grupos_estacoes.csv — chamada pd.read_csv, linha 126.
- E:/projeto/output/15_auditoria_metodologica/revisao_cientifica/vinculos_estacoes_receptores.csv — chamada pd.read_csv, linha 127.
- Mais 5 referências na ficha HTML e no inventário JSON.

**Saídas.**

- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/figuras/{name}.{ext} — chamada fig.savefig, linha 96.
- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/{pol}_{period}_cortes_comuns.csv — chamada .to_csv, linha 135.
- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/{pol}_{period}_referencia_comum.json — chamada .write_text, linha 136.
- {fig} — chamada save, linha 228.
- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/figuras/catalogo_{polls[0]}_{periods[0]}.json — chamada .write_text, linha 196.
- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/figuras/legendas.json — chamada .write_text, linha 229.
- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/index.html — chamada .write_text, linha 238.
- E:/projeto/output/16_revisao_pos_banca/figuras/index.html — chamada main.write_text, linha 241.

**Campos e chaves lidos.**

- table.loc: concentration.
- raw: direction.
- table: concentration, direction, dominant_group, period, pollutant, quintile, quintile_reference_union, receptor_id.
- cells: geometry, receptor_id.
- v: name.
- eligible: n_design_years, pollutant.
- limits: basis, direction, period, pollutant.
- abc: label, period, pollutant, region_type.
- regions: area_km2, concentration_area_mean, region_id.
- joint_table: direction.
- corr: direction, period, pollutant.
- cluster: direction, method.
- r: direction, five_emission_bands_identifiable, lisa_counts, management_counts, period, pollutant.
- summary: cases.
- counts: five_emission_bands, pollutant.

**Campos e chaves gerados.**

- table: quintile_reference_union.
- f: Q, Q_common, best_cluster_label, dominant_name, label, ward4_label.
- opts: station_overlay.
- joined: weighted_C.
- plot: Demais grupos.
- counts: five_emission_bands, pollutant.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| save(fig, name, caption, catalog) | 95-97 | grava produtos |
| concentration_maps(pol, period, z, muni, extent, table) | 100-114 | lê dados; Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. |
| run(polls=None, periods=None, worker=False, finalize_only=False) | 117-241 | lê dados; grava produtos; Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/figuras_analises_direcionais.py, linhas 105-111.

```python
    positive=table.loc[table.concentration>0,'concentration']
    low=max(10.**np.floor(np.log10(positive.quantile(.02))),.01);cap=float(positive.quantile(.99));unit=10.**np.floor(np.log10(cap));cap=max(10*low,np.floor(cap/unit)*unit);norm=LogNorm(low,cap)
    ticks=np.unique(np.r_[low,np.power(10.,np.arange(np.ceil(np.log10(low)),np.floor(np.log10(cap))+1)),cap])
    surfaces=[]
    for direction in DIRS:
        f=raw[raw.direction.eq(direction)].copy()
        geo=gpd.GeoSeries(gpd.points_from_xy(f.X,f.Y),crs=z.crs).to_crs(4674)
```

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

**Cálculos a observar nesta rotina.**

- quantile: Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/figuras_cenario_geral.py

Mapas pareados do cenário sem condicionamento pelo vento.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\figuras_cenario_geral.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| cartografia_apendices | Módulo autoral local; sua ficha está neste relatório. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| figuras_analises_direcionais | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| paleta_concentracoes | Módulo autoral local; sua ficha está neste relatório. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| visualizar_abc_direcional | Módulo autoral local; sua ficha está neste relatório. |


**Entradas.**

- E:/projeto/output/16_revisao_pos_banca/zoneamento_pos_banca.gpkg — chamada gpd.read_file, linha 77.
- E:/projeto/output/16_revisao_pos_banca/celulas_analise.gpkg — chamada gpd.read_file, linha 77.
- E:/projeto/output/11_integracao/apendices/resumo_figuras.json — chamada .read_text, linha 79.
- E:/projeto/output/16_revisao_pos_banca/cenario_geral/{pol}_{period}_receptores.csv — chamada pd.read_csv, linha 83.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/perfis_normalizados_grupos_estacoes.csv — chamada pd.read_csv, linha 88.
- E:/projeto/output/15_auditoria_metodologica/revisao_cientifica/vinculos_estacoes_receptores.csv — chamada pd.read_csv, linha 89.
- E:/projeto/output/11_integracao/nova_modelagem/estacoes_trienio_comum.csv — chamada pd.read_csv, linha 90.
- E:/projeto/output/16_revisao_pos_banca/cenario_geral/envelope_{pol}_{period}.csv — chamada pd.read_csv, linha 111.
- E:/projeto/output/16_revisao_pos_banca/cenario_geral/correlogramas.csv — chamada pd.read_csv, linha 124.
- E:/projeto/output/16_revisao_pos_banca/cenario_geral/limiares_cinco_faixas.csv — chamada pd.read_csv, linha 124.
- E:/projeto/output/16_revisao_pos_banca/cenario_geral/comparacao_agrupamentos.csv — chamada pd.read_csv, linha 124.
- E:/projeto/output/16_revisao_pos_banca/cenario_geral/resumo.json — chamada .read_text, linha 156.
- Mais 1 referências na ficha HTML e no inventário JSON.

**Saídas.**

- E:/projeto/output/16_revisao_pos_banca/cenario_geral/figuras/{stem}.{ext} — chamada fig.savefig, linha 126.
- {fig} — chamada save, linha 155.
- E:/projeto/output/16_revisao_pos_banca/cenario_geral/index.html — chamada .write_text, linha 163.
- E:/projeto/output/16_revisao_pos_banca/cenario_geral/figuras/legendas.json — chamada .write_text, linha 164.
- {p} — chamada p.write_text, linha 168.

**Campos e chaves lidos.**

- cells: geometry, receptor_id.
- v: name.
- eligible: n_design_years, pollutant.
- f: X, Y, concentration, emission_density, quintile.
- layers: 1h, PM10.
- corr: period, pollutant.
- comparison: method.
- limits: basis, period, pollutant.
- r: five_emission_bands_identifiable, global_moran, lisa_counts, management_counts, n_receptors, period, pollutant.
- summary: cases.

**Campos e chaves gerados.**

- g: Q, best_cluster_label, dominant_name, ward4_label.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run(concentrations_only=False) | 75-171 | lê dados; grava produtos; Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/figuras_cenario_geral.py, linhas 111-117.

```python
            f=pd.read_csv(DATA/f'envelope_{pol}_{period}.csv');v=table[pol,period].concentration;positive=v[v>0]
            low=max(10.**np.floor(np.log10(positive.quantile(.02))),.01);cap=float(positive.quantile(.99));unit=10.**np.floor(np.log10(cap));cap=max(10*low,np.floor(cap/unit)*unit)
            ticks=np.unique(np.r_[low,10.**np.arange(np.ceil(np.log10(low)),np.floor(np.log10(cap))+1),cap])
            geo=gpd.GeoSeries(gpd.points_from_xy(f.X,f.Y),crs=z.crs).to_crs(4674)
            surfaces.append(dict(x=geo.x.to_numpy(),y=geo.y.to_numpy(),values=f.concentration.to_numpy(),limits=[low,cap],norm=LogNorm(low,cap),cmap=concentration_cmap(),ticks=ticks,actual_max=float(v.max()),max_in_label=True))
        stem=f'Geral_{period}_Concentracoes'
        cart.render(z,muni,['concentration']*2,stem,[PN[p] for p in POLLS],'',extent,surfaces=surfaces,zone_layer=z,filename=stem,figure_title=LABEL[period]+' · meteorologia completa')
```

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

**Cálculos a observar nesta rotina.**

- quantile: Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/figuras_complementares_20261106.py

Mapas e gráficos das cinco faixas, gestão e envelopes direcionais.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\figuras_complementares_20261106.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| cartografia_apendices | Módulo autoral local; sua ficha está neste relatório. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| figuras_pos_banca | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/16_revisao_pos_banca/celulas_analise.gpkg — chamada gpd.read_file, linha 57.
- E:/projeto/output/16_revisao_pos_banca/zoneamento_pos_banca.gpkg — chamada gpd.read_file, linha 57.
- E:/projeto/output/11_integracao/apendices/resumo_figuras.json — chamada .read_text, linha 58.
- E:/projeto/output/16_revisao_pos_banca/figuras/legendas.json — chamada .read_text, linha 58.
- E:/projeto/output/16_revisao_pos_banca/limiares_cinco_faixas_validacao.csv — chamada pd.read_csv, linha 66.
- E:/projeto/output/16_revisao_pos_banca/resumo_quintis_gestao.json — chamada .read_text, linha 66.
- E:/projeto/output/16_revisao_pos_banca/ABC_regioes_gestao.csv — chamada pd.read_csv, linha 81.
- E:/projeto/output/16_revisao_pos_banca/regioes_gestao.csv — chamada pd.read_csv, linha 81.
- E:/projeto/output/16_revisao_pos_banca/vento/{file} — chamada pd.read_csv, linha 91.
- E:/projeto/output/16_revisao_pos_banca/vento/frequencia_vento.csv — chamada pd.read_csv, linha 102.

**Saídas.**

- {fig} — chamada save, linha 105.
- E:/projeto/output/16_revisao_pos_banca/figuras/legendas.json — chamada .write_text, linha 106.
- E:/projeto/output/16_revisao_pos_banca/figuras/index.html — chamada .write_text, linha 108.

**Campos e chaves lidos.**

- lim: basis, pollutant.
- bp: boxes.
- contribution: management_class, pollutant.
- regions: management_class, pollutant.
- cells: X, Y, geometry.
- d: direction.

**Campos e chaves gerados.**

- captions: Figura_PB10, Figura_PB11, PB12_cinco_faixas_emissao, PB13_estabilidade_limiares, PB16_frequencia_direcional.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 55-109 | lê dados; grava produtos; Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/figuras_complementares_20261106.py, linhas 94-100.

```python
            municipal_values=pd.concat([layer[col] for layer in layers]);positive=municipal_values[municipal_values>0]
            low=max(10.**np.floor(np.log10(float(positive.quantile(.02)))),.01);cap=float(positive.quantile(.99));unit=10.**np.floor(np.log10(cap));cap=max(10*low,np.floor(cap/unit)*unit);norm=LogNorm(low,cap)
            ticks=np.unique(np.r_[norm.vmin,np.power(10.,np.arange(np.ceil(np.log10(norm.vmin)),np.floor(np.log10(norm.vmax))+1)),norm.vmax])
            opts=[{'label':f'Concentração {period} (µg/m³)','norm':norm,'ticks':ticks,'cmap':'YlGnBu','show_missing':False}]*8
            geographic=gpd.GeoSeries(gpd.points_from_xy(cells.X,cells.Y),crs=cells.crs).to_crs(4674);surfaces=[{'x':geographic.x.to_numpy(),'y':geographic.y.to_numpy(),'values':layer[col].to_numpy(),'limits':[norm.vmin,norm.vmax],'cmap':'YlGnBu','norm':norm,'ticks':ticks,'actual_max':float(municipal_values.max())} for layer in layers]
            code=f'PB15_{pol}_{period}';cart.render(z,muni,[col]*8,code,[f'Vento de {v}' for v in directions],'',extent,surfaces=surfaces,panel_shape=(4,2),zone_layer=z)
            captions[f'Figura_{code}']=('Envelope dos máximos horários por receptor nas horas válidas em cada direção meteorológica de origem. ' if period=='1h' else 'Envelope das médias diárias completas em dias persistentes na direção indicada, com ao menos 18 h válidas, resultante circular ≥ 0,5 e frequência direcional ≥ 50%. ')+ 'O máximo de cada receptor pode ocorrer em momento diferente. Diagnóstico do cenário 2021-2023, não previsão simultânea de nuvem de poeira e sem comparação normativa. Barra logarítmica comum aos oito painéis, com ponta para valores acima do corte cartográfico próximo ao P99 e máximo municipal preservado. Interpolação apenas visual; tabelas mantêm os valores originais.'
```

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- quantile: Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/figuras_pos_banca.py

Figuras pós-banca no encarte aprovado, sem reescrever seminários.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\figuras_pos_banca.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| cartografia_apendices | Módulo autoral local; sua ficha está neste relatório. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/16_revisao_pos_banca/zoneamento_pos_banca.gpkg — chamada gpd.read_file, linha 61.
- E:/projeto/output/16_revisao_pos_banca/celulas_analise.gpkg — chamada gpd.read_file, linha 61.
- E:/projeto/output/11_integracao/apendices/resumo_figuras.json — chamada .read_text, linha 62.
- E:/projeto/output/16_revisao_pos_banca/correlogramas.csv — chamada pd.read_csv, linha 75.
- E:/projeto/output/16_revisao_pos_banca/comparacao_agrupamentos.csv — chamada pd.read_csv, linha 79.
- E:/projeto/output/16_revisao_pos_banca/limiares_associativos_validacao_espacial.csv — chamada pd.read_csv, linha 83.
- E:/projeto/output/16_revisao_pos_banca/contribuicoes_regioes.csv — chamada pd.read_csv, linha 88.

**Saídas.**

- E:/projeto/output/16_revisao_pos_banca/figuras/{name}.{ext} — chamada fig.savefig, linha 55.
- {fig} — chamada save, linha 91.
- E:/projeto/output/16_revisao_pos_banca/figuras/legendas.json — chamada .write_text, linha 103.
- E:/projeto/output/16_revisao_pos_banca/figuras/index.html — chamada .write_text, linha 105.

**Campos e chaves lidos.**

- cells: ward_k2, ward_k4.
- d: pollutant.
- c: method.
- t: emission_basis, pollutant.
- g: pollutant, region.

**Campos e chaves gerados.**

- cells: ward2, ward4.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| save(fig, name) | 54-56 | grava produtos |
| run() | 59-106 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/figuras_pos_banca.py, linhas 54-62.

```python
def save(fig,name):
 for ext in ['svg','pdf','png']:fig.savefig(OUT/f'{name}.{ext}',dpi=450,bbox_inches='tight',facecolor='white')
 plt.close(fig)

# Run
def run():
 OUT.mkdir(exist_ok=True,parents=True);cart.OUT=OUT
 z=gpd.read_file(ROOT/'zoneamento_pos_banca.gpkg');cells=gpd.read_file(ROOT/'celulas_analise.gpkg');muni=gpd.GeoDataFrame(geometry=[z.geometry.union_all()],crs=z.crs)
 extent=json.loads((config.BASE/'output/11_integracao/apendices/resumo_figuras.json').read_text(encoding='utf8'))['bounds_degrees']
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/figuras_poster_pos_banca.py

Mapas individuais e gráficos do pôster; mantém o encarte operacional.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\figuras_poster_pos_banca.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| cartografia_apendices | Módulo autoral local; sua ficha está neste relatório. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| copy | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| figuras_pos_banca | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.colorbar | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| svg_compativel_word | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| xml.etree.ElementTree | Leitura/edição de XML de projetos e documentos. |


**Entradas.**

- E:/projeto/output/16_revisao_pos_banca/zoneamento_pos_banca.gpkg — chamada gpd.read_file, linha 72.
- E:/projeto/output/16_revisao_pos_banca/celulas_analise.gpkg — chamada gpd.read_file, linha 72.
- E:/projeto/output/11_integracao/apendices/resumo_figuras.json — chamada .read_text, linha 73.
- E:/projeto/output/16_revisao_pos_banca/correlogramas.csv — chamada pd.read_csv, linha 96.

**Saídas.**

- E:/projeto/temp/pos_banca_2026_11_05/assets/poster_correlograma.svg — chamada fig.savefig, linha 99.
- E:/projeto/temp/pos_banca_2026_11_05/assets/poster_HH_bar.svg — chamada fig.savefig, linha 101.

**Campos e chaves lidos.**

- patch.attrib: d.
- cells: PM25_lisa, PM25_quintile.
- d: I, max_distance_m, min_distance_m, pollutant.

**Campos e chaves gerados.**

- cells: contributor.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| crop_map(source, target) | 46-67 | Chamadas efetivas: ET.parse, tree.getroot, root.find, ax.find, list, title.findall, ax.remove, max |
| run() | 70-102 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/figuras_poster_pos_banca.py, linhas 46-54.

```python
def crop_map(source,target):

 tree=ET.parse(source);root=tree.getroot();ns={'s':'http://www.w3.org/2000/svg'}
 ax=root.find('.//s:g[@id="axes_1"]',ns)
 patch=ax.find('s:g/s:path',ns);coords=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',patch.attrib['d'])))
 xs=coords[::2];ys=coords[1::2];bottom=max(ys)+14

 title=ax.find('s:g[@id="text_17"]',ns)
 if title is None:raise ValueError('Título do encarte não identificado')
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/finalizar_adi_ids7.py

Finalizar adi ids7. Consolidação/migração: conferir pré-condições. A organização passa por groups, params.

**Papel.** Consolidação/migração: conferir pré-condições. **Fonte inspecionada.** E:\projeto\codigo\finalizar_adi_ids7.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| collections | Estruturas de contagem, agrupamento e coleções auxiliares. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/14_auditoria_entradas/entrada_BPIP_7caracteres/alteracoes.json — chamada .read_text, linha 32.
- externos.1h_adi_7e2357f — chamada src.read_text, linha 33.
- E:/projeto/output/14_auditoria_entradas/entrada_BPIP_7caracteres/PM10_IDS7.pro — chamada .read_text, linha 35.
- E:/projeto/output/14_auditoria_entradas/entrada_BPIP_7caracteres/auditoria_base.json — chamada .read_text, linha 79.
- externos.1h_adi_7e2357f — chamada src.read_bytes, linha 81.

**Saídas.**

- E:/projeto/output/14_auditoria_entradas/entrada_BPIP_7caracteres/PM10_IDS7_BPIP_FUNIT.ADI — chamada target.write_bytes, linha 77.
- E:/projeto/output/14_auditoria_entradas/entrada_BPIP_7caracteres/grupos_fontes_IDS7.INP — chamada .write_bytes, linha 78.
- E:/projeto/output/14_auditoria_entradas/entrada_BPIP_7caracteres/validacao_ADI.json — chamada .write_text, linha 82.

**Campos e chaves lidos.**

- p: heights, mapping.
- audit: hour, warnings.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| groups(ls) | 57-62 | Chamadas efetivas: defaultdict, dict, l.split, .update Retorno: dict(g). |
| params(ls) | 66-67 | Chamadas efetivas: l.split Retorno: {s[1]: s[2:] for l in ls if (s := l.split()) and s[0] == 'SRCPARAM'}. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/finalizar_adi_ids7.py, linhas 57-65.

```python
def groups(ls):
 g=defaultdict(set)
 for l in ls:
  t=l.split()
  if t and t[0]=='SRCGROUP':g[t[1]].update(t[2:])
 return dict(g)
oldg=groups(lines);newg=groups(new)
assert {k:{mapping.get(s,s) for s in v} for k,v in oldg.items()}==newg
# Params
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. Rotina histórica: conferir pré-condições e versão de dados antes de qualquer execução.

## codigo/finalizar_documentacao_codigos.py

Finalizar documentacao codigos. Documentação/apoio. A organização passa por cabecalhos, entrega_teco, replacements.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\projeto\codigo\finalizar_documentacao_codigos.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| ast | Inspeção/transformação da sintaxe Python sem executar o processamento científico. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| documentar_campos_scripts_teco | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| documentar_portabilidade | Módulo autoral local; sua ficha está neste relatório. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| importlib.metadata | Importação e identificação de versões das bibliotecas. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- info['raiz']/AGENTS.md — chamada agents.read_text, linha 71.
- E:/teco/codigo/caminhos_projeto.json — chamada .read_text, linha 89.
- E:/teco/config/analise_extensivel.json — chamada .read_text, linha 95.
- E:/teco/entrega_final/00_documentacao/manifesto.json — chamada .read_text, linha 100.
- E:/teco/entrega_final/00_documentacao/Dicionario_dos_campos.html — chamada p.read_text, linha 102.
- E:/teco/entrega_final/00_documentacao/Dicionario_dos_campos.html — chamada p.read_bytes, linha 126.

**Saídas.**

- E:/teco/entrega_final/00_documentacao/Dicionario_dos_campos.html — chamada p.write_text, linha 102.
- info['raiz']/codigo/requirements-calculo.txt — chamada .write_text, linha 68.
- info['raiz']/codigo/LEIA_CAMINHOS.md — chamada doc.write_text, linha 70.
- info['raiz']/AGENTS.md — chamada agents.write_text, linha 75.
- E:/projeto/temp/preparacao_20261114/cabecalhos_conferidos.json — chamada .write_text, linha 76.
- E:/teco/entrega_final/05_scripts/python/caminhos_projeto.json — chamada .write_text, linha 90.
- E:/teco/entrega_final/05_scripts/{sub}/caminhos_projeto.json — chamada .write_text, linha 92.
- E:/teco/entrega_final/05_scripts/caminhos_projeto.json — chamada .write_text, linha 94.
- E:/teco/entrega_final/05_scripts/parametros/analise_extensivel.json — chamada .write_text, linha 98.
- E:/teco/entrega_final/05_scripts/LEIA_PRIMEIRO.md — chamada .write_text, linha 123.
- E:/teco/entrega_final/05_scripts/Inventario_scripts_atual.json — chamada .write_text, linha 127.

**Campos e chaves lidos.**

- info: raiz, saida.
- d.PROJETOS: teco.
- cfg: pastas.
- config: base, suporte_calculo.
- spec: arquivo.

**Campos e chaves gerados.**

- cfg: modo_entrega, raiz_projeto.
- : entrega_final.
- c: raiz_projeto.
- spec: arquivo.
- config: saida.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| cabecalhos() | 46-76 | lê dados; grava produtos |
| entrega_teco() | 79-128 | lê dados; grava produtos |
| replacements(s) | 130-130 | Chamadas efetivas: s.replace Retorno: s.replace('629 campos em 50 camadas vetoriais', '704 campos em 53 camadas vetoriais'). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/finalizar_documentacao_codigos.py, linhas 46-54.

```python
def cabecalhos():
    results=[]
    for key,info in d.PROJETOS.items():
        root=Path(info['raiz']);files=d.fontes(root,info)
        for p in files:
            s=d.ler(p)
            if p.suffix=='.py':
                rec=d.inspecionar_python(p,root)
                start=s.find('# CÓDIGO DO PROCESSAMENTO')
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/gerar_complementos_revisao.py

Legenda ampla dos perfis e uso do solo para a caracterização municipal.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\gerar_complementos_revisao.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| cartografia_apendices | Módulo autoral local; sua ficha está neste relatório. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| landuse | Módulo autoral local; sua ficha está neste relatório. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| rasterio | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| rasterio.features | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/zoneamento_avaliacao_atual.gpkg — chamada gpd.read_file, linha 52.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_todos_grupos_por_zona.csv — chamada pd.read_csv, linha 55.
- config.FILES['landuse_2024'] — chamada rasterio.open, linha 79.
- E:/projeto/config.DIRS['out']/11_integracao/apendices/resumo_figuras.json — chamada .read_text, linha 84.
- E:/projeto/config.DIRS['vias']/vias_cong.shp — chamada gpd.read_file, linha 87.
- E:/projeto/config.DIRS['grade_generated']/grade_receptores_adaptativa.csv — chamada pd.read_csv, linha 90.

**Saídas.**

- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_perfis_311_zonas.csv — chamada .to_csv, linha 65.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_ABC_sintese_criticos.{ext} — chamada fig.savefig, linha 76.

**Campos e chaves lidos.**

- config.DIRS: grade_generated, out, vias.
- config.FILES: landuse_2024.
- roads: fclass.
- grid: utm_x, utm_y.

**Campos e chaves gerados.**

- profiles.loc: DEMAIS.
- totals: DEMAIS.
- roads: classe.
- grid: localizacao.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 51-94 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/gerar_complementos_revisao.py, linhas 56-62.

```python
        dominant=d[primary].idxmax(axis=1);critical=z[f'{pol}_critico_preliminar'].reindex(d.index)
        shares=d.loc[critical,primary].div(d.loc[critical,primary].sum(axis=1),axis=0)*100
        profiles=shares.groupby(dominant.reindex(shares.index)).mean();counts=dominant.reindex(shares.index).value_counts()
        remaining=d.loc[~critical,primary].div(d.loc[~critical,primary].sum(axis=1),axis=0)*100
        labels=[f'{POST_GROUP_NAMES.get(g,g)} (n={counts[g]})' for g in profiles.index]
        totals=counts.to_dict()
        if len(remaining):
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/gerar_documentos_academicos_v36.py

Gerar documentos academicos v36. Histórico editorial: entrega de seminários encerrada. A organização passa por read_csv, fmt_num, fmt_int, fmt_int_en, pct, clean_label, clear_document, document_from_template, set_run_font, setup_styles.

**Papel.** Histórico editorial: entrega de seminários encerrada. **Fonte inspecionada.** E:\projeto\codigo\gerar_documentos_academicos_v36.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| __future__ | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| docx | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.enum.section | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.enum.table | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.enum.text | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.oxml | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.oxml.ns | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.shared | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| revisao_bibliografica_v38 | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- {path} — chamada pd.read_csv, linha 98.
- E:/projeto/output/08_documentos/figuras/metricas_documentos_v36.json — chamada .read_text, linha 404.
- E:/projeto/output/07_grade_receptores/grade_manifesto.json — chamada .read_text, linha 405.
- E:/projeto/output/07_grade_receptores/grade_diagnostico_por_setor.csv — chamada read_csv, linha 406.
- E:/projeto/output/{folder}/comum/zoneamento_{pol}_resultados.csv — chamada read_csv, linha 410.
- E:/projeto/output/{folder}/comum/modelagem_{pol}_periodo.csv — chamada read_csv, linha 411.
- E:/projeto/output/{folder}/emissoes_{pol}_ABC_resumo_setores.csv — chamada read_csv, linha 412.
- E:/projeto/output/{folder}/source_apportionment_{pol}_ABC_resumo_zonas.csv — chamada read_csv, linha 413.
- E:/projeto/output/{folder}/source_apportionment_{pol}_ABC_anual_resumo_zonas.csv — chamada read_csv, linha 414.
- E:/projeto/output/{folder}/fontes_{pol}_balanco_massa_por_grupo.csv — chamada read_csv, linha 415.
- E:/projeto/output/05_impacto_saude/impacto_saude_indicadores_exposicao_zona.csv — chamada read_csv, linha 417.

**Saídas.**

- E:/projeto/0_ref/seminario_qualificacao_congonhas_atual.docx — chamada doc.save, linha 744.
- E:/projeto/0_ref/dissertacao_congonhas_atual.docx — chamada doc.save, linha 877.
- E:/projeto/0_ref/resumo_expandido_congonhas_atual.docx — chamada doc.save, linha 944.

**Campos e chaves lidos.**

- styles: Normal.
- ctx: metrics.
- m: PM10, PM25, grid_total, health.
- df: ABC_EMIS_PRIORITY_GROUP.
- crit: GROUP_SUM_TO_ALL_PCT, TOP1_SHARE_PCT, TOP3_SHARE_PCT.
- ann: GROUP_SUM_TO_ALL_PCT, TOP1_SHARE_PCT.

**Campos e chaves gerados.**

- ctx: health.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| read_csv(path: Path) | 97-98 | lê dados Retorno: pd.read_csv(path, encoding='utf-8-sig'). |
| fmt_num(value, digits=1) | 101-113 | Chamadas efetivas: .replace, pd.isna, float, re.sub, str Retorno: txt, '-'. |
| fmt_int(value) | 116-124 | Chamadas efetivas: pd.isna, .replace, str, int, round, float Retorno: '-', f'{int(round(float(value))):,}'.replace(',', '.'). |
| fmt_int_en(value) | 127-135 | Chamadas efetivas: pd.isna, str, int, round, float Retorno: '-', f'{int(round(float(value))):,}'. |
| pct(value, digits=1) | 138-139 | Chamadas efetivas: fmt_num Retorno: f'{fmt_num(value, digits)}%'. |
| clean_label(text) | 142-149 | Chamadas efetivas: .replace, str, text.replace Retorno: text.replace('_', ' ').replace('PM25', 'PM2,5').replace('nao atendimento', 'não atendimento').replace('nao_atendimento', 'não atendimento'). |
| clear_document(doc: Document) | 152-157 | Chamadas efetivas: list, body.remove, qn |
| document_from_template(path: Path) | 160-163 | Chamadas efetivas: clear_document, path.exists, Document, str Retorno: doc. |
| set_run_font(run, font='Arial', size=11, bold=None, italic=None, color=DARK) | 166-177 | Chamadas efetivas: run._element.rPr.rFonts.set, qn, Pt |
| setup_styles(doc: Document, font='Arial', body_size=11, line_spacing=1.5, paragraph_after=6) | 180-196 | Chamadas efetivas: ._element.rPr.rFonts.set, Pt, qn, st._element.rPr.rFonts.set |
| set_a4(section, left=3.0, right=2.0, top=3.0, bottom=2.0) | 199-207 | Chamadas efetivas: Cm |
| set_cell_shading(cell, fill) | 210-216 | Chamadas efetivas: cell._tc.get_or_add_tcPr, tc_pr.find, shd.set, qn, OxmlElement, tc_pr.append |
| set_cell_margins(cell, top=90, start=120, bottom=90, end=120) | 219-232 | Chamadas efetivas: tc.get_or_add_tcPr, tc_pr.first_child_found_in, .items, OxmlElement, tc_pr.append, tc_mar.find, node.set, qn |
| set_table_width(table, widths) | 235-243 | Chamadas efetivas: enumerate, set_cell_margins, len, Inches |
| add_para(doc, text='', font='Arial', size=11, bold=False, italic=False, align=None, after=6, before=0, line_spacing=1.35) | 246-256 | Chamadas efetivas: doc.add_paragraph, Pt, p.add_run, set_run_font Retorno: p. |
| add_heading(doc, text, level=1, font='Arial') | 259-266 | Chamadas efetivas: doc.add_paragraph, Pt, p.add_run, set_run_font, text.upper Retorno: p. |
| ensure_bullet_numbering(doc) | 269-322 | Chamadas efetivas: getattr, numbering.findall, OxmlElement, abstract.set, multi.set, abstract.append, lvl.set, start.set Retorno: num_id, existing. |
| apply_num(paragraph, num_id, level=0) | 325-334 | Chamadas efetivas: paragraph._p.get_or_add_pPr, OxmlElement, ilvl.set, num_id_el.set, num_pr.append, p_pr.append, qn, str |
| add_bullet(doc, text, font='Arial', size=10.5) | 337-344 | Chamadas efetivas: doc.add_paragraph, apply_num, Pt, p.add_run, set_run_font, ensure_bullet_numbering Retorno: p. |
| add_table(doc, headers, rows, widths=None, font='Arial', size=9.2, header_fill=LIGHT) | 347-369 | Chamadas efetivas: doc.add_table, enumerate, str, set_cell_shading, set_table_width, len, table.add_row, set_run_font Retorno: table. |
| add_caption(doc, text, font='Arial', size=9, above=False) | 372-374 | Chamadas efetivas: add_para Retorno: p. |
| add_image(doc, path: Path, caption: str, width=6.0, font='Arial') | 377-386 | Chamadas efetivas: doc.add_paragraph, p.add_run, run.add_picture, add_caption, path.exists, add_para, str, Inches |
| add_reference_list(doc, refs, font='Arial', size=9.2) | 389-396 | Chamadas efetivas: doc.add_paragraph, Pt, Cm, p.add_run, set_run_font |
| add_page_break(doc) | 399-400 | Chamadas efetivas: doc.add_page_break |
| collect_context() | 403-418 | lê dados Retorno: ctx. |
| objective_rows() | 421-427 | Organiza parâmetros, expressões ou retorno sem chamada externa. Retorno: [['1', 'Classificar áreas do zoneamento urbano municipal (plano diretor).', 'Atendimento x não atendimento por dados de monitoramento e modelagem; áreas não cobertas pela rede são preenchidas pela mod. |
| results_rows(ctx) | 470-478 | Chamadas efetivas: fmt_int, m.get Retorno: [['Grade v37', fmt_int(m['grid_total']), f"Malha setorial interna de 500 m; {fmt_int(m.get('grid_representative_ok'))}/{fmt_int(m.get('grid_diag_n'))} setores válidos com receptor representativo."], [. |
| cmas_result_table_rows(ctx) | 481-507 | Chamadas efetivas: fmt_int_en, pm25_quads.get, m.get Retorno: [['Grid audit', f"{fmt_int_en(m['grid_total'])} receptors", f"All {fmt_int_en(m.get('grid_diag_n'))} valid zones received representative and 500 m internal coverage points; shared-border receptor line. |
| quadrant_table(ctx, pol) | 510-518 | Chamadas efetivas: fmt_int, counts.get Retorno: [[label, fmt_int(counts.get(key, 0))] for label, key in order]. |
| abc_rows(ctx, pol) | 521-524 | Chamadas efetivas: .head, .value_counts, str, fmt_int, vc.items, .fillna Retorno: [[str(k), fmt_int(v)] for k, v in vc.items()]. |
| source_apportionment_summary(ctx, pol) | 527-536 | Chamadas efetivas: pct, .mean, .median Retorno: [['Top-1 crítico médio', pct(crit['TOP1_SHARE_PCT'].mean(), 1)], ['Top-3 crítico médio', pct(crit['TOP3_SHARE_PCT'].mean(), 1)], ['Fechamento crítico mediano', pct(crit['GROUP_SUM_TO_ALL_PCT'].median(. |
| methodology_pipeline_rows() | 539-581 | Organiza parâmetros, expressões ou retorno sem chamada externa. Retorno: [['1. Bases territoriais', 'Limite municipal, zoneamento do plano diretor, setores censitários, vias, empreendimentos, fontes AERMOD, rede de monitoramento e POSTFILEs.', 'Todos os dados são reprojeta. |
| equation_rows() | 584-608 | Organiza parâmetros, expressões ou retorno sem chamada externa. Retorno: [['Média diária', 'C_d = (1/n_d) * soma(C_h), com n_d >= 18', 'Frondizi (2007); 40 CFR Part 50, Appendix N, por analogia de completude.'], ['Completude trimestral', 'Comp_q = N_dias_validos,q / N_dias. |
| sip_alignment_rows() | 611-620 | Organiza parâmetros, expressões ou retorno sem chamada externa. Retorno: [['Padrão e forma do indicador', 'CONAMA 506/2024, WHO 2021 e analogia com NAAQS/Appendix N', 'Define limites, períodos de referência, P98, média anual e completude.'], ['Rede de monitoramento', 'Esta. |
| title_page_seminar(doc) | 623-644 | Chamadas efetivas: add_page_break, add_para |
| build_seminar(ctx) | 647-744 | grava produtos |
| title_page_diss(doc) | 747-773 | Chamadas efetivas: add_para, add_page_break, len |
| build_dissertation(ctx) | 776-877 | grava produtos |
| setup_cmas(doc) | 880-890 | Chamadas efetivas: setup_styles, set_a4, list, OxmlElement, cols.set, sect_pr.append, sect_pr.findall, sect_pr.remove |
| add_cmas_heading(doc, text) | 893-900 | Chamadas efetivas: doc.add_paragraph, Pt, p.add_run, set_run_font, text.upper Retorno: p. |
| add_cmas_para(doc, text) | 903-904 | Chamadas efetivas: add_para Retorno: add_para(doc, text, font='Trebuchet MS', size=9, align=WD_ALIGN_PARAGRAPH.JUSTIFY, after=3, line_spacing=1.0). |
| build_cmas(ctx) | 907-944 | grava produtos |
| main() | 947-954 | Chamadas efetivas: REF.mkdir, collect_context, build_seminar, build_dissertation, build_cmas, print |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/gerar_documentos_academicos_v36.py, linhas 530-536.

```python
    return [
        ["Top-1 crítico médio", pct(crit["TOP1_SHARE_PCT"].mean(), 1)],
        ["Top-3 crítico médio", pct(crit["TOP3_SHARE_PCT"].mean(), 1)],
        ["Fechamento crítico mediano", pct(crit["GROUP_SUM_TO_ALL_PCT"].median(), 1)],
        ["Top-1 anual médio", pct(ann["TOP1_SHARE_PCT"].mean(), 1)],
        ["Fechamento anual mediano", pct(ann["GROUP_SUM_TO_ALL_PCT"].median(), 1)],
    ]
```

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. Rotina histórica: conferir pré-condições e versão de dados antes de qualquer execução.

## codigo/gerar_documentos_preparacao.py

Gerar documentos preparacao. Documentação/apoio. A organização passa por registrar_fontes, blocos, texto_simples, inline_pdf, criar_docx, criar_pdf, main, afterFlowable, footer.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\projeto\codigo\gerar_documentos_preparacao.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| argparse | Parâmetros fornecidos ao iniciar o programa. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| docx | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.enum.table | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.enum.text | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.opc.constants | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.oxml | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.oxml.ns | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.shared | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| reportlab.lib | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.enums | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.pagesizes | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.styles | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.pdfbase | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.pdfbase.ttfonts | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.pdfgen | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.platypus | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| textwrap | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |


**Entradas.**

- {name} — chamada src.read_text, linha 200.

**Saídas.**

- {path} — chamada doc.save, linha 150.

**Campos e chaves lidos.**

- doc.styles: Normal, Title.
- styles: body, code, table, title.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| registrar_fontes() | 45-52 | Chamadas efetivas: Path, FileNotFoundError, os.environ.get, tuple, all, _cp_externo, pdfmetrics.registerFontFamily, p.exists |
| blocos(text) | 55-78 | Chamadas efetivas: text.splitlines, len, line.startswith, line.strip, .strip, buf.append, code.append, .startswith |
| texto_simples(s) | 81-83 | Chamadas efetivas: re.sub, .replace, s.replace Retorno: s.replace('**', '').replace('`', ''). |
| inline_pdf(s) | 86-91 | Chamadas efetivas: html.escape, re.sub Retorno: s. |
| criar_docx(path, content) | 94-150 | grava produtos |
| PDFComMarcadores() | 153-156 | Chamadas efetivas: isinstance, self.canv.bookmarkPage, self.canv.addOutlineEntry, getattr, str, flow.getPlainText, self.seq.nextf |
| criar_pdf(path, content) | 159-194 | Chamadas efetivas: registrar_fontes, PDFComMarcadores, pdf.build, ParagraphStyle, kind.startswith, canv.setFont, canv.setFillColor, canv.drawRightString |
| main() | 197-203 | lê dados |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/gerar_documentos_preparacao.py, linhas 45-53.

```python
def registrar_fontes():
    folder=Path(os.environ.get('DOCUMENT_FONT_DIR',_cp_externo('fonts_2a6cc8f')))
    candidates=[(folder/'arial.ttf',folder/'arialbd.ttf',folder/'ariali.ttf',folder/'consola.ttf'),tuple(Path('/usr/share/fonts/truetype/dejavu')/n for n in ['DejaVuSans.ttf','DejaVuSans-Bold.ttf','DejaVuSans-Oblique.ttf','DejaVuSansMono.ttf'])]
    for normal,bold,italic,code in candidates:
        if all(p.exists() for p in [normal,bold,italic,code]):
            for name,path in [('Body',normal),('BodyBold',bold),('BodyItalic',italic),('Code',code)]:pdfmetrics.registerFont(TTFont(name,str(path)))
            pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='BodyItalic',boldItalic='BodyBold');return
    raise FileNotFoundError('Informe DOCUMENT_FONT_DIR com Arial e Consolas ou instale DejaVu Sans e DejaVu Sans Mono.')

```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/gerar_documentos_resultados.py

Gerar documentos resultados. Documentação/apoio. A organização passa por read_csv, clean_text, fmt_number, fmt_int, pct, set_cell_shading, set_cell_margins, set_table_width, set_run_font, add_paragraph.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\projeto\codigo\gerar_documentos_resultados.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| __future__ | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| docx | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.enum.section | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.enum.table | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.enum.text | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.oxml | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.oxml.ns | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.shared | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- {path} — chamada pd.read_csv, linha 88.
- E:/projeto/output/00_diagnostico/resumo_execucao.csv — chamada read_csv, linha 305.
- E:/projeto/output/00_diagnostico/diagnostico_geometria_zoneamento.csv — chamada read_csv, linha 306.
- E:/projeto/output/07_grade_receptores/grade_manifesto.json — chamada .read_text, linha 307.
- E:/projeto/output/07_grade_receptores/grade_diagnostico_por_setor.csv — chamada read_csv, linha 308.
- E:/projeto/output/06_censo_ibge/censo_diagnostico.csv — chamada read_csv, linha 309.
- E:/projeto/output/06_censo_ibge/censo_populacao_por_zoneamento.csv — chamada read_csv, linha 310.
- E:/projeto/output/05_impacto_saude/impacto_saude_indicadores_exposicao_zona.csv — chamada read_csv, linha 311.
- E:/projeto/output/05_impacto_saude/impacto_saude_fracao_atribuivel_cronica_zona_endpoint.csv — chamada read_csv, linha 312.
- E:/projeto/output/05_impacto_saude/impacto_saude_fracao_atribuivel_aguda_zona_endpoint.csv — chamada read_csv, linha 313.
- E:/projeto/output/{folder}/comum/modelagem_{pol}_periodo.csv — chamada read_csv, linha 317.
- E:/projeto/output/{folder}/comum/zoneamento_{pol}_resultados.csv — chamada read_csv, linha 318.
- Mais 6 referências na ficha HTML e no inventário JSON.

**Saídas.**

- E:/projeto/0_ref/relatorio_tecnico_congonhas_atual.docx — chamada doc.save, linha 733.
- E:/projeto/0_ref/resumo_expandido_congonhas_atual.docx — chamada doc.save, linha 862.

**Campos e chaves lidos.**

- styles: Normal.
- ctx: af_cr, censo_diag, geom, grid_diag, grid_manifest, health, model.
- df: ANNUAL_MODEL, P98_MODEL.
- r: allocated_pct, emission_allocated_gs, emission_total_gs, endpoint, group_id, max, mean, min, n_sources.
- abc: ABC_EMIS_PRIORITY_GROUP, GROUP_SUM_TO_ALL_PCT, N_GROUPS_A, TOP1_SHARE_PCT.
- annual: GROUP_SUM_TO_ALL_PCT, N_GROUPS_A, TOP1_SHARE_PCT.
- h: health_person_ugm3_excess_cf, health_pop_above_cf, health_pop_above_pv, health_population_exposed.
- gd: coverage_ok, coverage_pct, representative_ok.
- gm: counts_by_kind, total_receptors.
- geom: area_municipio_km2, area_sem_zoneamento_km2, n_geometrias_invalidas, n_zonas, percentual_municipio_sem_zoneamento.
- censo: n_setores_com_populacao, n_setores_shape.
- pm10_df: status_PF, status_PV.
- pm25_df: status_PF, status_PV.
- pm10_z: PM10_PF_status, PM10_PV_status.
- pm25_z: PM25_PF_status, PM25_PV_status.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| read_csv(path: Path) | 87-88 | lê dados Retorno: pd.read_csv(path, encoding='utf-8-sig'). |
| clean_text(value) | 91-101 | Chamadas efetivas: str, .replace, text.replace Retorno: text.replace('�', 'ã').replace('PM25', 'PM2,5').replace('PM10', 'PM10').replace('nao_', 'não_').replace('_', ' '), ''. |
| fmt_number(value, digits=1) | 104-120 | Chamadas efetivas: .replace, pd.isna, float, abs, re.sub, str, txt.replace Retorno: txt, '-'. |
| fmt_int(value) | 123-129 | Chamadas efetivas: pd.isna, .replace, str, int, round, float Retorno: f'{int(round(float(value))):,}'.replace(',', '.'), '-'. |
| pct(value, digits=1) | 132-133 | Chamadas efetivas: fmt_number Retorno: f'{fmt_number(value, digits)}%'. |
| set_cell_shading(cell, fill: str) | 136-142 | Chamadas efetivas: cell._tc.get_or_add_tcPr, tc_pr.find, shd.set, qn, OxmlElement, tc_pr.append |
| set_cell_margins(cell, top=80, start=120, bottom=80, end=120) | 145-158 | Chamadas efetivas: tc.get_or_add_tcPr, tc_pr.first_child_found_in, .items, OxmlElement, tc_pr.append, tc_mar.find, node.set, qn |
| set_table_width(table, widths_inches) | 161-169 | Chamadas efetivas: enumerate, set_cell_margins, len, Inches |
| set_run_font(run, size=None, bold=None, italic=None, color=None) | 172-183 | Chamadas efetivas: run._element.rPr.rFonts.set, qn, Pt |
| add_paragraph(doc, text='', style=None, bold=False, italic=False, size=11, color=INK, align=None, after=6, before=0) | 186-196 | Chamadas efetivas: doc.add_paragraph, Pt, p.add_run, set_run_font Retorno: p. |
| add_heading(doc, text, level=1) | 199-210 | Chamadas efetivas: doc.add_paragraph, Pt, p.add_run, set_run_font Retorno: p. |
| add_bullet(doc, text) | 213-219 | Chamadas efetivas: doc.add_paragraph, Pt, p.add_run, set_run_font Retorno: p. |
| add_numbered(doc, text) | 222-228 | Chamadas efetivas: doc.add_paragraph, Pt, p.add_run, set_run_font Retorno: p. |
| add_caption(doc, text) | 231-232 | Chamadas efetivas: add_paragraph Retorno: add_paragraph(doc, text, italic=True, size=9.5, color=MUTED, align=WD_ALIGN_PARAGRAPH.CENTER, after=8, before=2). |
| add_table(doc, headers, rows, widths=None, font_size=9.2) | 235-259 | Chamadas efetivas: doc.add_table, enumerate, str, set_cell_shading, set_table_width, len, table.add_row, set_run_font Retorno: table. |
| add_key_value_table(doc, rows) | 262-263 | Chamadas efetivas: add_table Retorno: add_table(doc, ['Item', 'Síntese'], rows, widths=[2.0, 4.5], font_size=9.5). |
| add_image(doc, path: Path, caption: str, width_in=6.25) | 266-274 | Chamadas efetivas: path.exists, doc.add_paragraph, p.add_run, run.add_picture, add_caption, add_paragraph, str, Inches |
| setup_doc(doc: Document, title_header: str) | 277-301 | Chamadas efetivas: Inches, _cp_adaptar, ._element.rPr.rFonts.set, Pt, set_run_font, qn |
| collect_context() | 304-347 | lê dados Retorno: {'resumo': resumo, 'geom': geom, 'grid_manifest': grid_manifest, 'grid_diag': grid_diag, 'censo_diag': censo_diag, 'censo_pop': censo_pop, 'health': health, 'af_cr': af_cr, 'af_ag': af_ag, 'model': mo. |
| model_stats_rows(ctx) | 350-372 | Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. Retorno: rows. |
| emission_rows(ctx, pol, n=10) | 375-388 | Chamadas efetivas: .head, mass.iterrows, rows.append, .sort_values, clean_text, fmt_int, fmt_number, pct Retorno: rows. |
| abc_dominance_rows(ctx) | 391-403 | Chamadas efetivas: .head, rows.append, .value_counts, pol.replace, fmt_int, .join, len, counts.items Retorno: rows. |
| source_apportionment_rows(ctx) | 406-422 | Chamadas efetivas: rows.append, pol.replace, fmt_number, .mean Retorno: rows. |
| health_rows(ctx) | 425-444 | Chamadas efetivas: .reset_index, af.iterrows, rows.append, .agg, fmt_int, fmt_number, len, .sum Retorno: rows. |
| add_title_page(doc, title, subtitle, meta_rows) | 447-471 | Chamadas efetivas: add_paragraph, doc.add_table, set_table_width, enumerate, doc.add_page_break, set_cell_shading, table.row_cells, len |
| build_report(ctx) | 474-733 | grava produtos |
| setup_abstract_doc(doc) | 736-742 | Chamadas efetivas: setup_doc, Cm |
| build_abstract(ctx) | 745-862 | grava produtos |
| main() | 865-871 | Chamadas efetivas: REF.mkdir, collect_context, build_report, build_abstract, print |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/gerar_documentos_resultados.py, linhas 362-368.

```python
                fmt_number(df["P98_MODEL"].median(), 1),
                fmt_number(df["P98_MODEL"].quantile(0.95), 1),
                fmt_number(df["P98_MODEL"].max(), 1),
                fmt_number(df["ANNUAL_MODEL"].median(), 1),
                fmt_number(df["ANNUAL_MODEL"].quantile(0.95), 1),
                fmt_number(df["ANNUAL_MODEL"].max(), 1),
                f"{z[pv_col].value_counts().get('nao_atendimento', 0)} / {len(z)}",
```

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

**Cálculos a observar nesta rotina.**

- quantile: Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/gerar_figuras_documentos.py

Gerar figuras documentos. Cartografia/apresentação. A organização passa por _read_csv, _fmt_int, _fmt_int_en, _safe_font, _read_gdf, _clean_label, _geo_extent, _title, _plot_numeric_zone, _plot_category_zone.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\gerar_figuras_documentos.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| PIL | Inspeção, composição ou ajuste de imagens pela biblioteca Pillow. |
| __future__ | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib.cm | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.patches | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| textwrap | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |


**Entradas.**

- {path} — chamada pd.read_csv, linha 60.
- {path} — chamada gpd.read_file, linha 88.
- E:/projeto/output/07_grade_receptores/grade_manifesto.json — chamada .read_text, linha 211.
- {image_path} — chamada Image.open, linha 336.

**Saídas.**

- {path} — chamada fig.savefig, linha 713.
- {path} — chamada canvas.save, linha 366.
- {path} — chamada .to_csv, linha 752.
- E:/projeto/output/08_documentos/figuras/metricas_documentos_v36.json — chamada .write_text, linha 765.

**Campos e chaves lidos.**

- z: _plot_value.
- manifest: counts_by_kind, total_receptors.
- grid_diag: coverage_ok, coverage_pct, max_distance_sampled_m, representative_ok.
- receptors: kind, roles.
- community: landuse_preferred.
- m: status_PF, status_PV.
- health: health_person_ugm3_excess_cf, health_pop_above_cf, health_pop_above_pv, pop_total.
- metrics: PM10, PM25, grid_total, health.
- top: ABC_CLASS, ABC_SHARE_PCT, label.
- ax4.spines: bottom.

**Campos e chaves gerados.**

- z: _plot_value.
- metrics: grid_community_landuse_preferred, grid_community_total, grid_gap_fill_points, health.
- top: ABC_SHARE_PCT, label.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| _read_csv(path: Path) | 59-60 | lê dados Retorno: pd.read_csv(path, encoding='utf-8-sig'). |
| _fmt_int(value) | 63-64 | Chamadas efetivas: .replace, int, round, float Retorno: f'{int(round(float(value))):,}'.replace(',', '.'). |
| _fmt_int_en(value) | 67-68 | Chamadas efetivas: int, round, float Retorno: f'{int(round(float(value))):,}'. |
| _safe_font(size: int, bold: bool=False) | 71-80 | Chamadas efetivas: ImageFont.load_default, Path, p.exists, _cp_externo, ImageFont.truetype, str Retorno: ImageFont.load_default(), ImageFont.truetype(str(p), size=size). |
| _read_gdf(path: Path, layer: str  /  None=None) | 83-88 | lê dados Retorno: gpd.read_file(path), gpd.read_file(path, layer=layer). |
| _clean_label(value: str) | 91-98 | Chamadas efetivas: str, .strip, .replace, text.replace Retorno: text.replace('_', ' ').replace('PM25', 'PM2.5').replace('PM10', 'PM10').strip(). |
| _geo_extent(ax, zones, pad=0.045) | 101-108 | Chamadas efetivas: max, ax.set_xlim, ax.set_ylim, ax.set_aspect, ax.set_axis_off |
| _title(ax, text: str) | 111-112 | Chamadas efetivas: ax.set_title |
| _plot_numeric_zone(ax, fig, zones, column: str, title: str, label: str, cmap='viridis', vmin=None, vmax=None) | 115-144 | Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. |
| _plot_category_zone(ax, zones, column: str, title: str, palette: dict, labels: dict, legend_title: str) | 147-175 | Chamadas efetivas: zones.copy, z.plot, palette.items, z.boundary.plot, _geo_extent, _title, sub.plot, handles.append |
| _metric_card(fig, x, y, w, h, value: str, label: str, color='#1f4e79') | 178-191 | Chamadas efetivas: FancyBboxPatch, fig.add_artist, fig.text |
| _group_label(group_id, group_name='') | 194-207 | Chamadas efetivas: labels.get, str Retorno: labels.get(str(group_id), str(group_name or group_id)). |
| collect_metrics() | 210-257 | lê dados Retorno: metrics. |
| draw_flowchart(path: Path) | 260-327 | grava produtos |
| _paste_fit(canvas: Image.Image, image_path: Path, box, title: str) | 330-344 | Chamadas efetivas: ImageDraw.Draw, _safe_font, draw.text, .convert, img.thumbnail, canvas.paste, draw.rectangle, Image.open |
| draw_map_panel(path: Path) | 347-366 | grava produtos |
| draw_summary_chart(path: Path, metrics: dict) | 369-437 | grava produtos |
| draw_cmas_method_compact(path: Path, metrics: dict) | 440-520 | grava produtos |
| draw_cmas_integrated_results(path: Path, metrics: dict) | 523-610 | grava produtos |
| draw_cmas_quantitative_snapshot(path: Path, metrics: dict) | 613-714 | grava produtos |
| write_cmas_figure_manifest(path: Path) | 717-752 | grava produtos |
| main() | 755-770 | grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/gerar_figuras_documentos.py, linhas 118-124.

```python
    if vmin is None:
        vmin = float(values.quantile(0.02)) if values.notna().any() else 0.0
    if vmax is None:
        vmax = float(values.quantile(0.98)) if values.notna().any() else 1.0
    if not np.isfinite(vmin):
        vmin = 0.0
    if not np.isfinite(vmax) or vmax <= vmin:
```

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

**Cálculos a observar nesta rotina.**

- quantile: Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/Gerar_Grade_AERMOD.bat

Gerar Grade AERMOD. Processamento ou módulo de apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\Gerar_Grade_AERMOD.bat.

**Bibliotecas e dependências.**

Não há importação Python/JavaScript declarada; conferir programas acionados e comandos do arquivo.

**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/Gerar_Grade_AERMOD.bat, linhas 9-17.

```text
@echo off
chcp 65001 >nul
set "CODE_DIR=%~dp0"
REM Raiz e caminhos definidos em caminhos_projeto.json
cd /d "%CODE_DIR%"

if not exist .venv\Scripts\python.exe (
    echo Criando ambiente virtual...
    py -m venv .venv
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/gerar_grade_receptores.py

Gerar grade receptores. Processamento ou módulo de apoio. A organização passa por main.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\gerar_grade_receptores.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| __future__ | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| censo_ibge | Módulo autoral local; sua ficha está neste relatório. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| io_utils | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| main | Módulo autoral local; sua ficha está neste relatório. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| receptor_grid | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| traceback | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

- E:/projeto/config.DIRS['out']/07_grade_receptores/ULTIMA_GRADE_GERADA.json — chamada .write_text, linha 84.

**Campos e chaves lidos.**

- config.DIRS: grade_generated, out.
- config.FILES: municipality, zoning.
- result: manifest, operational_dir, output_dir, total_receptors.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| main() | 35-88 | grava produtos Retorno: result. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/gerar_grade_receptores.py, linhas 15-23.

```python
_cp_file = _cp_Path(globals().get('__file__', _cp_Path.cwd() / 'codigo' / 'script.py')).resolve()
for _cp_parent in [_cp_file.parent, *_cp_file.parents]:
    _cp_code = _cp_parent if (_cp_parent / 'caminhos_congonhas.py').is_file() else _cp_parent / 'codigo'
    if (_cp_code / 'caminhos_congonhas.py').is_file():
        if str(_cp_code) not in _cp_sys.path: _cp_sys.path.insert(0, str(_cp_code))
        break
from caminhos_congonhas import raiz_projeto as _cp_raiz, texto_caminho as _cp_texto, externo as _cp_externo, adaptar_texto as _cp_adaptar
# FIM DOS CAMINHOS PORTÁTEIS

```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/gerar_guias_poster_metodologia.py

Documentos de leitura derivados dos textos editáveis do repositório.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\gerar_guias_poster_metodologia.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| docx | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.enum.text | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.oxml | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.oxml.ns | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.shared | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- {source} — chamada source.read_text, linha 59.

**Saídas.**

- {target} — chamada doc.save, linha 62.

**Campos e chaves lidos.**

- doc.styles: Normal.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| runs(p, text) | 31-36 | Chamadas efetivas: re.split, re.fullmatch, p.add_run, m.group |
| build(source, target, english=False) | 38-62 | lê dados; grava produtos |
| run() | 64-66 | Chamadas efetivas: build |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/gerar_guias_poster_metodologia.py, linhas 31-39.

```python
def runs(p,text):
    for token in re.split(r'((?:MP|PM)(?:10|2[,\.]5)|O3)',text):
        m=re.fullmatch(r'(MP|PM)(10|2[,\.]5)|(O)(3)',token)
        if m:
            p.add_run(m.group(1) or m.group(3));r=p.add_run(m.group(2) or m.group(4));r.font.subscript=True
        else:p.add_run(token)
# Build
def build(source,target,english=False):
    doc=Document();sec=doc.sections[0];sec.page_width=Cm(21);sec.page_height=Cm(29.7)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/gerar_material_estudo_poster_teco.py

Guias independentes para leitura, apresentação e planejamento inicial.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\gerar_material_estudo_poster_teco.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| docx | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.enum.text | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.opc.constants | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.oxml | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.oxml.ns | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.shared | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/descontinuado/2026_11_08_poster_detalhado/manifesto.json — chamada f.read_text, linha 52.
- {p} — chamada p.read_bytes, linha 53.
- {md} — chamada md.read_text, linha 84.
- E:/projeto/dissertacao/metodologia/guia-metodologia-completa.md — chamada .read_text, linha 116.
- E:/projeto/temp/revisao_poster_teco_20261108/complemento_guia_poster.md — chamada .read_text, linha 118.
- E:/projeto/output/16_revisao_pos_banca/contribuicoes_prioridades_pooled_PM25.csv — chamada .open, linha 120.
- E:/projeto/temp/revisao_poster_teco_20261108/roteiro_en.md — chamada .read_text, linha 133.
- E:/projeto/temp/revisao_poster_teco_20261108/texto_teco.md — chamada .read_text, linha 134.
- E:/projeto/dissertacao/poster/README.md — chamada .read_text, linha 138.

**Saídas.**

- E:/projeto/descontinuado/2026_11_08_poster_detalhado/manifesto.json — chamada f.write_text, linha 53.
- {p} — chamada p.write_text, linha 57.
- {dest} — chamada doc.save, linha 112.

**Campos e chaves lidos.**

- doc.styles: Normal.
- r: share_pct.
- row: group_id, share_pct.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| archive(p) | 47-53 | lê dados; grava produtos |
| write(p, s) | 56-57 | grava produtos |
| runs(p, text) | 60-71 | Chamadas efetivas: re.split, re.fullmatch, p.add_run, part.startswith, m.group, part.rstrip, OxmlElement, link.set |
| build(md, dest, header) | 74-112 | lê dados; grava produtos |
| main() | 115-149 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/gerar_material_estudo_poster_teco.py, linhas 47-55.

```python
def archive(p):
    if not p.exists():return
    q=B/p.relative_to(R)
    if q.exists():return
    q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
    f=B/'manifesto.json';a=json.loads(f.read_text(encoding='utf8')) if f.exists() else []
    a.append({'origem':str(p),'arquivo_preservado':str(q),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'motivo':'Material gerado substituído pela revisão de estudo do pôster.'});f.write_text(json.dumps(a,ensure_ascii=False,indent=2),encoding='utf8')

# Write
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/gerar_metodologia_texto_abnt_v36.py

Gerar metodologia texto abnt v36. Histórico editorial: entrega de seminários encerrada. A organização passa por _metrics, add_equation, add_method_paras, title_page, build_document.

**Papel.** Histórico editorial: entrega de seminários encerrada. **Fonte inspecionada.** E:\projeto\codigo\gerar_metodologia_texto_abnt_v36.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| __future__ | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| docx | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.enum.text | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.shared | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| gerar_documentos_academicos_v36 | Módulo autoral local; sua ficha está neste relatório. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

- g.REF/metodologia_congonhas_atual.docx — chamada doc.save, linha 412.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| _metrics() | 33-37 | Chamadas efetivas: g.collect_context Retorno: g.collect_context()['metrics'], {}. |
| add_equation(doc: Document, text: str) | 40-46 | Chamadas efetivas: doc.add_paragraph, Pt, p.add_run, g.set_run_font, RGBColor |
| add_method_paras(doc: Document, paragraphs) | 49-58 | Chamadas efetivas: g.add_para |
| title_page(doc: Document) | 61-85 | Chamadas efetivas: g.add_para, g.add_page_break |
| build_document() | 88-413 | grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/gerar_metodologia_texto_abnt_v36.py, linhas 33-41.

```python
def _metrics():
    try:
        return g.collect_context()["metrics"]
    except Exception:
        return {}

# Add equation
def add_equation(doc: Document, text: str):
    p = doc.add_paragraph()
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. Rotina histórica: conferir pré-condições e versão de dados antes de qualquer execução.

## codigo/gerar_poster_cmas.mjs

Monta o pôster Congonhas no modelo oficial, verifica assinaturas das fontes quantitativas e insere mapas, gráficos, texto e agradecimentos.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\gerar_poster_cmas.mjs.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| ./caminhos_congonhas.mjs | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| node:fs/promises | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |
| node:fs | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |
| node:crypto | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |
| node:url | Biblioteca padrão Node.js para arquivos, caminhos, importação ou assinaturas. |
| @oai/artifact-tool | Biblioteca de autoria do ambiente de apresentações/planilhas; precisa ser disponibilizada na máquina de autoria. |


**Entradas.**

- R+'/codigo/recursos_poster/fontes_resultados.json' — chamada readFileSync, linha 47.
- item.path — chamada readFileSync, linha 49.
- await FileBlob.load(SOURCE) — chamada PresentationFile.importPptx, linha 55.
- SOURCE — chamada FileBlob.load, linha 55.
- file — chamada readFileSync, linha 84.
- A+'/dados_poster_20261109.json' — chamada readFileSync, linha 133.
- file — chamada readFileSync, linha 138.
- A+'/poster_'+k+'_MAIN.svg' — chamada readFileSync, linha 199.
- A+'/'+file — chamada readFileSync, linha 291.
- SOURCE — chamada readFileSync, linha 313.

**Saídas.**

- T+'/poster_after_inspect.ndjson' — chamada fs.writeFile, linha 303.
- T+'/poster_after.png' — chamada fs.writeFile, linha 305.
- {slide:s,format:'png',scale:.4} — chamada p.export, linha 305.
- T+'/layout_pairs.json' — chamada fs.writeFile, linha 307.
- candidate — chamada (await PresentationFile.exportPptx(p)).save, linha 309.
- p — chamada PresentationFile.exportPptx, linha 309.
- {workspaceDir:T,candidatePath:candidate,finalPath:T+'/poster_validado_revisao/Poster_CMAS_Session12_Congonhas_final.pptx',pythonExecutable:PY,integrityValidatorPath:SKILL+'/container_tools/inspect_pre — chamada finalizePresentation, linha 313.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/gerar_poster_cmas.mjs, linhas 62-70.

```javascript
function edit(id,text,size,position,align='left',color=C.ink,bold=false){

 const x=p.resolve(id);x.text=text;

 x.text.style={typeface:'Arial',fontSize:size,color,bold,alignment:align,verticalAlignment:'top',autoFit:'none',insets:0,wrap:'square'};

 if(position)x.position=position;return x;

}
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/gerar_relatorio_auditoria_integrada.py

Relatório legível da auditoria, com resultados vinculados às evidências.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\projeto\codigo\gerar_relatorio_auditoria_integrada.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| reportlab.lib | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.pagesizes | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.styles | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.pdfbase | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.pdfbase.ttfonts | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.platypus | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/15_auditoria_metodologica/auditoria_integrada.json — chamada .read_text, linha 42.

**Saídas.**

- E:/projeto/output/15_auditoria_metodologica/Relatorio_Auditoria_Metodologica_Integrada.md — chamada .write_text, linha 269.

**Campos e chaves lidos.**

- a: PM10, PM25, health, p98_corrected_station_years, population, territorio.
- v: n_valid_days, p98, p98_before, pollutant, station_id, year.
- p: population_allocated, population_ambiguous, population_outside.
- h: eligible_zones, fraction_max_pct, fraction_min_pct.
- styles: BodyAudit, Heading1, Heading2, Title.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| number(x, digits=2) | 38-38 | Chamadas efetivas: .replace Retorno: f'{x:,.{digits}f}'.replace(',', 'X').replace('.', ',').replace('X', '.'). |
| content() | 41-228 | lê dados Retorno: f"# Auditoria metodológica do Projeto Congonhas\n\nRevisão consolidada em 29 de outubro de 2026\n\nO relatório explica como os arquivos de entrada se transformam nos indicadores territoriais dos quatr. |
| render_pdf(markdown, dest) | 231-266 | Chamadas efetivas: Path, pdfmetrics.registerFontFamily, getSampleStyleSheet, styles.add, ParagraphStyle, markdown.splitlines, .build, _cp_externo Retorno: s. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/gerar_relatorio_auditoria_integrada.py, linhas 38-46.

```python
def number(x,digits=2):return f'{x:,.{digits}f}'.replace(',','X').replace('.',',').replace('X','.')

# Content
def content():
    a=json.loads((OUT/'auditoria_integrada.json').read_text(encoding='utf8'));p=a['population'];h=a['health']
    rows='\n'.join(f"| {v['station_id']} | {'MP10' if v['pollutant']=='PM10' else 'MP2,5'} | {v['year']} | {v['n_valid_days']} | {number(v['p98_before'])} | {number(v['p98'])} |" for v in a['p98_corrected_station_years'])
    return f'''# Auditoria metodológica do Projeto Congonhas

Revisão consolidada em 29 de outubro de 2026
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/gerar_relatorios_codigos.py

Gerar relatorios codigos. Documentação/apoio. A organização passa por papel, purpose, limpar_item, tabela, recorte, detalhes_funcoes, ficha, md_html, main, inline.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\projeto\codigo\gerar_relatorios_codigos.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| ast | Inspeção/transformação da sintaxe Python sem executar o processamento científico. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| documentar_outros_codigos | Módulo autoral local; sua ficha está neste relatório. |
| documentar_portabilidade | Módulo autoral local; sua ficha está neste relatório. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| subprocess | Chamada de outros programas e verificação de seus resultados de execução. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| textwrap | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |


**Entradas.**

- Path(__file__).with_name('gerar_documentos_preparacao.py') — chamada .read_text, linha 416.
- info['raiz']/info['saida']/index.html — chamada page.read_text, linha 454.

**Saídas.**

- info['raiz']/info['saida']/Inventario_codigos.json — chamada .write_text, linha 441.
- info['raiz']/info['saida']/Inventario_codigos.csv — chamada .open, linha 442.
- info['raiz']/info['saida']/fichas/{i}_Path(rec['arquivo']).stem.md — chamada .write_text, linha 447.
- info['raiz']/info['saida']/fichas/{i}_Path(rec['arquivo']).stem.html — chamada .write_text, linha 448.
- stem.with_suffix('.md') — chamada .write_text, linha 452.
- info['raiz']/info['saida']/index.html — chamada .write_text, linha 453.
- info['raiz']/info['saida']/index.html — chamada page.write_text, linha 454.

**Campos e chaves lidos.**

- rec: arquivo, doc, entradas, finalidade, linguagem, papel.
- x: nome.
- o: linha, operacao.
- op: linha.
- f: nome.
- item: chamada, linha.
- namespace: blocos.
- info: nome, raiz, saida.

**Campos e chaves gerados.**

- rec: finalidade, papel.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| papel(name, key) | 281-292 | Chamadas efetivas: name.lower, n.startswith, any Retorno: 'Processamento ou módulo de apoio', 'Configuração compartilhada'. |
| purpose(rec, key) | 295-304 | Chamadas efetivas: rec.get, papel, .stem.replace, Path, .replace, len, .startswith, .split Retorno: stems[:1].upper() + stems[1:] + '. ' + role + '. ' + ('A organização passa por ' + ', '.join(funcs[:10]) + '.' if funcs else 'As instruções são executadas no corpo principal, na ordem do arquivo.'), C. |
| limpar_item(text) | 307-308 | Chamadas efetivas: .strip, .replace, str Retorno: str(text).replace(' / ', ' / ').replace('\n', ' ').replace('\r', ' ').strip(). |
| tabela(headers, rows) | 311-312 | Chamadas efetivas: .join, len, limpar_item Retorno: '\n'.join([' /  ' + '  /  '.join(headers) + '  / ', ' /  ' + '  /  '.join(['---'] * len(headers)) + '  / '] + [' /  ' + '  /  '.join((limpar_item(v) for v in row)) + '  / ' for row in rows]) + '\n\n'. |
| recorte(source, rec) | 315-332 | Chamadas efetivas: source.splitlines, rec.get, set, max, chosen.append, any, seen.update, out.append Retorno: out. |
| detalhes_funcoes(source, rec) | 335-356 | Chamadas efetivas: ast.parse, ast.walk, any, dict.fromkeys, result.append, isinstance, verbs.append, .join Retorno: result, result. |
| ficha(rec, root, key, full=False) | 359-410 | Chamadas efetivas: d.ler, rec.get, detalhes_funcoes, recorte, list, .join, purpose, first.startswith Retorno: '\n'.join(parts). |
| md_html(md) | 415-426 | lê dados Retorno: '\n'.join(out), re.sub('\\[([^\\]]+)\\]\\(([^)]+)\\)', '<a href="\\2">\\1</a>', s). |
| main() | 429-455 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/gerar_relatorios_codigos.py, linhas 281-289.

```python
def papel(name,key):
    n=name.lower()
    if n.startswith('caminhos_'):return 'Configuração compartilhada'
    if n.startswith('test_') or n.startswith(('validar','verificar','conferir','testar','autoteste')):return 'Conferência/teste'
    if n.startswith(('auditar','auditoria','diagnosticar','diagnostics')):return 'Auditoria/diagnóstico'
    if key=='congonhas' and any(x in n for x in ['seminario','orientadora','documentos_academicos_v36','metodologia_texto_abnt_v36','revisao_bibliografica_v38']):return 'Histórico editorial: entrega de seminários encerrada'
    if n.startswith('map_copasa'):return 'Histórico: etapa anterior à rodada CMAS atual'
    if any(x in n for x in ['figura','mapa','cartograf','poster','rosa_vento','svg','paleta','estilo','qgis','encarte']):return 'Cartografia/apresentação'
    if any(x in n for x in ['relatorio','document','dicionario','guia','preparacao']):return 'Documentação/apoio'
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/gerar_visualizador_privado.py

Empacota prévias leves, sem dados horários ou serviços externos.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\gerar_visualizador_privado.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| PIL | Inspeção, composição ou ajuste de imagens pela biblioteca Pillow. |
| argparse | Parâmetros fornecidos ao iniciar o programa. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| empacotar_visualizador_privado | Módulo autoral local; sua ficha está neste relatório. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| rosa_vento_seletor | Módulo autoral local; sua ficha está neste relatório. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- {p} — chamada Image.open, linha 58.
- p.with_suffix('.svg') — chamada .read_text, linha 62.
- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/pares/p.with_suffix('.svg').name — chamada original.read_text, linha 65.
- E:/projeto/output/16_revisao_pos_banca/visualizador/imagens/{mode}_p.stem.webp — chamada target.read_bytes, linha 74.
- E:/projeto/output/16_revisao_pos_banca/vento/horas_por_direcao.csv — chamada pd.read_csv, linha 88.

**Saídas.**

- p.with_suffix('.svg') — chamada .write_text, linha 66.
- E:/projeto/output/16_revisao_pos_banca/visualizador/imagens/{mode}_p.stem.webp — chamada image.save, linha 71.
- {folder}/dados.js — chamada .write_text, linha 95.
- {folder}/catalogo.json — chamada .write_text, linha 96.
- E:/projeto/output/16_revisao_pos_banca/visualizador/auditoria_visualizador.json — chamada .write_text, linha 100.

**Campos e chaves lidos.**

- c: mode.

**Campos e chaves gerados.**

- row: direction.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run(pairs) | 52-101 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/gerar_visualizador_privado.py, linhas 52-60.

```python
def run(pairs):
    Image.MAX_IMAGE_PIXELS=400_000_000
    (OUT/'imagens').mkdir(parents=True,exist_ok=True);REPO.mkdir(parents=True,exist_ok=True)
    catalog=[];sources=[]
    def add(p,mode,period,product,direction=None):
        name=mode+'_'+p.stem+'.webp';target=OUT/'imagens'/name
        with Image.open(p) as image:
            image=image.convert('RGB')

```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/groups.py

Define os grupos de fontes e distingue os grupos primários exclusivos dos agrupamentos diagnósticos sobrepostos.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\groups.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| unicodedata | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- value: name.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| norm_token(value) | 72-75 | Chamadas efetivas: unicodedata.normalize, .join, re.sub, str, text.upper, unicodedata.combining Retorno: re.sub('[^A-Z0-9]+', '', text.upper()). |
| canonical_group(value) | 78-96 | Chamadas efetivas: norm_token, ALIASES.items, t.startswith Retorno: None, None. |
| urban_subgroup_from_source(source_id) | 99-109 | Chamadas efetivas: .replace, norm_token, token.startswith, raw.startswith, .upper, str Retorno: None, 'URB-VIA'. |
| is_exposed_area(source_id) | 112-113 | Chamadas efetivas: .startswith, norm_token Retorno: norm_token(source_id).startswith('AEX'). |
| infer_primary_group_from_source(source_id, desc=None) | 116-141 | Chamadas efetivas: norm_token, re.fullmatch, suffixes.items, urban_subgroup_from_source, canonical_group, re.match Retorno: g, 'WGM'. |
| canonical_post_group(value) | 179-198 | Chamadas efetivas: .strip, norm_token, re.sub, POST_FILE_ALIASES.items, canonical_group, .upper, str Retorno: g, None. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/groups.py, linhas 72-80.

```python
def norm_token(value):
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"[^A-Z0-9]+", "", text.upper())

# Canonical group
def canonical_group(value):
    t = norm_token(value)
    if not t:
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/integracao_metodologica.py

Produtos territoriais harmonizados, sem executar novas simulações AERMOD.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\integracao_metodologica.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| aermod_post | Módulo autoral local; sua ficha está neste relatório. |
| aermod_sources | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| inventario_anual | Módulo autoral local; sua ficha está neste relatório. |
| io_utils | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.patches | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.ticker | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| methodology_rules | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| out_aermod_reader | Módulo autoral local; sua ficha está neste relatório. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| source_apportionment | Módulo autoral local; sua ficha está neste relatório. |
| standards | Módulo autoral local; sua ficha está neste relatório. |
| stations | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| vector_portable | Módulo autoral local; sua ficha está neste relatório. |
| zone_analysis | Módulo autoral local; sua ficha está neste relatório. |


**Entradas.**

- E:/projeto/config.DIRS['out']/07_grade_receptores/grade_diagnostico_por_setor.csv — chamada pd.read_csv, linha 290.

**Saídas.**

- E:/projeto/config.DIRS['out']/11_integracao/{name} — chamada df.to_csv, linha 77.
- path.with_suffix('.' + ext) — chamada fig.savefig, linha 124.
- E:/projeto/config.DIRS['out']/11_integracao/resumo_execucao.json — chamada .write_text, linha 302.
- E:/projeto/config.DIRS['out']/11_integracao/index.html — chamada .write_text, linha 306.

**Campos e chaves lidos.**

- config.DIRS: aermod_logs, emission, limite_cong, out, post, qar, zoneamento.
- stations: geometry, station_id.
- groups: ALL.
- config.FILES: municipality, zoning.
- summary: pollutants.
- daily: ALL.
- sub.loc: group_id, group_name.
- pst: source_period.

**Campos e chaves gerados.**

- base: year.
- zones: zone_index.
- ledger: grid_n_internal, health_avoidable_deaths, health_status, population_estimated, population_source.
- summary: grid_points, grid_zones_with_point, health_status, population_estimated_sum.
- tab: period, pollutant.
- pst: closure_max_pct, closure_min_pct, concentration_priorities, dominant_groups, emission_classes, emission_threshold_tpy, integrated_classes, inventory_unmatched_sources, latest_classes, latest_period, latest_valid_stations, model_preview_classes, model_preview_year, model_preview_zones_with_receptors, model_years, source_association_validated, source_groups, source_period, source_zones, sources_unidentified.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| csv(df, name) | 75-77 | grava produtos |
| buffers(stations, metrics, pol, start, end) | 80-85 | Chamadas efetivas: .merge, gpd.GeoDataFrame, b.geometry.buffer, metrics.n_design_years.eq, .drop_duplicates Retorno: b. |
| point_gdf(table) | 88-89 | Chamadas efetivas: gpd.GeoDataFrame, gpd.points_from_xy Retorno: gpd.GeoDataFrame(table, geometry=gpd.points_from_xy(table.X, table.Y), crs=config.CRS_PROJECT). |
| station_links(zones, b, pol, period) | 92-100 | Chamadas efetivas: zones.iterrows, pd.DataFrame, b.itertuples, z.geometry.intersection, rows.append Retorno: pd.DataFrame(rows). |
| map_panel(zones, municipality, columns, path, labels) | 103-125 | grava produtos |
| load_groups(pol) | 128-146 | Chamadas efetivas: next, discover, selected.items, result.items, read_daily_native, .append, provenance.append, pd.concat Retorno: (result, provenance), (result, provenance). |
| annual_contributions(groups, zones, pol, years) | 149-176 | Chamadas efetivas: sorted, .rename, model_period_metrics, base.merge, .reset_index, point_gdf, zones.iterrows, model_annual_metrics Retorno: (pd.DataFrame(rows), pd.DataFrame(audit)), (pd.DataFrame(), pd.DataFrame()). |
| run() | 179-308 | lê dados; grava produtos Retorno: summary. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/integracao_metodologica.py, linhas 163-169.

```python
    if base.empty:return pd.DataFrame(),pd.DataFrame()
    means=base.groupby(['X','Y','year'])[['ALL']+group_ids].mean().groupby(['X','Y']).mean().reset_index()
    pts=point_gdf(means);rows=[];audit=[]
    for zid,z in zones.iterrows():
        sub=pts[pts.geometry.covered_by(z.geometry)]
        if sub.empty:continue
        values=sub[group_ids].mean().sort_values(ascending=False);total=values.sum();allmean=sub.ALL.mean()
```

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/integrar_monitoramento_atual.py

Diagnóstico territorial atualizado: monitoramento 2023–25 e modelo 2021–23.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\integrar_monitoramento_atual.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| integracao_metodologica | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| methodology_rules | Módulo autoral local; sua ficha está neste relatório. |
| monitoramento_mma | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| stations | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| zone_analysis | Módulo autoral local; sua ficha está neste relatório. |


**Entradas.**

- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_receptores_anuais.csv — chamada pd.read_csv, linha 69.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_vinculo_receptor_zona.csv — chamada pd.read_csv, linha 70.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/zoneamento_nova_modelagem.gpkg — chamada gpd.read_file, linha 126.

**Saídas.**

- E:/projeto/config.DIRS['out']/10_avaliacao_rede/{name}.csv — chamada df.to_csv, linha 115.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/estacoes_rede_atual.gpkg — chamada stations.to_file, linha 120.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/identificacao_estacoes_figura_B1.csv — chamada .to_csv, linha 121.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/estacoes_metricas_anuais.csv — chamada yearly.to_csv, linha 122.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/estacoes_trienio_atual.csv — chamada selected.to_csv, linha 123.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/estacoes_trienios_mma.csv — chamada roll.to_csv, linha 124.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/estacoes_trienio_comum.csv — chamada .to_csv, linha 125.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/zoneamento_{name}.gpkg — chamada z.to_file, linha 129.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/zoneamento_{name}.csv — chamada .to_csv, linha 129.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/integracao_{name}.csv — chamada records.to_csv, linha 130.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/resumo_{name}.json — chamada .write_text, linha 131.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/zoneamento_nova_modelagem.gpkg — chamada z.to_file, linha 133.
- Mais 4 referências na ficha HTML e no inventário JSON.

**Campos e chaves lidos.**

- config.DIRS: out, qar.
- z.loc: PM25_ANN_monitor.
- stations: number, station_id, station_name.
- sub: T.
- v.loc: DV.
- v: T.

**Campos e chaves gerados.**

- z: health_avoidable_deaths, health_period.
- summary: health, quadrants.
- stations: number.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| integrate(z, stations, roll, years) | 65-109 | lê dados Retorno: (z, pd.DataFrame(records), summary). |
| run() | 112-145 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/integrar_monitoramento_atual.py, linhas 104-110.

```python
    for rr,c in [(1.08,'health_fraction_pct'),(1.06,'health_fraction_low_pct'),(1.11,'health_fraction_high_pct')]:
        z[c]=np.nan;z.loc[good,c]=100*(1-np.exp(-np.log(rr)/10*np.maximum(z.loc[good,'PM25_ANN_monitor']-5,0)))
    z['health_period']=f'{years[0]}-{years[1]}';z['health_avoidable_deaths']=np.nan
    summary['health']={'eligible_zones':int(good.sum()),'min':float(z.health_fraction_pct.min()),'max':float(z.health_fraction_pct.max())}
    summary['quadrants']={p:z[f'{p}_quadrante_comum'].value_counts().to_dict() for p in ['PM10','PM25']}
    return z,pd.DataFrame(records),summary

```

Função exponencial. No módulo sanitário, a fração potencialmente evitável é 1−exp(−β×ΔC), condicionada à função concentração-resposta e ao contrafactual.

Logaritmo natural. Na função de risco, β=ln(RR)/10 converte um risco relativo por 10 µg/m³ para a escala de 1 µg/m³.

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- exp: Função exponencial. No módulo sanitário, a fração potencialmente evitável é 1−exp(−β×ΔC), condicionada à função concentração-resposta e ao contrafactual.
- log: Logaritmo natural. Na função de risco, β=ln(RR)/10 converte um risco relativo por 10 µg/m³ para a escala de 1 µg/m³.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/integrar_periodo_comum.py

Integra observações e simulações de 2021–2023 sem substituir anos ausentes.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\integrar_periodo_comum.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| cartografia_apendices | Módulo autoral local; sua ficha está neste relatório. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| integracao_metodologica | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| methodology_rules | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| stations | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| zone_analysis | Módulo autoral local; sua ficha está neste relatório. |


**Entradas.**

- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/zoneamento_nova_modelagem.gpkg — chamada gpd.read_file, linha 50.
- E:/projeto/config.DIRS['out']/11_integracao/apendices/resumo_figuras.json — chamada .read_text, linha 61.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_receptores_anuais.csv — chamada pd.read_csv, linha 71.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_vinculo_receptor_zona.csv — chamada pd.read_csv, linha 73.

**Saídas.**

- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/estacoes_metricas_anuais.csv — chamada yearly.to_csv, linha 57.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/estacoes_trienio_comum.csv — chamada common.to_csv, linha 59.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/integracao_periodo_comum.csv — chamada .to_csv, linha 100.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/zoneamento_periodo_comum.gpkg — chamada z.to_file, linha 101.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/zoneamento_periodo_comum.csv — chamada .to_csv, linha 102.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/resumo_periodo_comum.json — chamada .write_text, linha 103.

**Campos e chaves lidos.**

- config.DIRS: out, qar.
- metrics.loc: station_id.
- yearly.loc: station_id.
- z: zone_index.
- linked: zone_index.

**Campos e chaves gerados.**

- st: number.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 49-104 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/integrar_periodo_comum.py, linhas 49-57.

```python
def run():
    z=gpd.read_file(OUT/'zoneamento_nova_modelagem.gpkg')
    print('Validando séries originais das estações...',flush=True)
    metrics,frames=load_all_station_metrics(config.DIRS['qar'])
    if metrics.pollutant.eq('ERRO').any():raise ValueError(metrics[metrics.pollutant.eq('ERRO')].to_dict('records'))
    yearly=station_yearly_metrics(frames);roll=rolling_station_metrics(yearly,2018)
    stations,missing=build_station_gdf(metrics,config.DIRS['qar']/'station_id.xlsx',config.DIRS['qar']/'est_cong.kmz')
    if missing:raise ValueError(missing)
    yearly.to_csv(OUT/'estacoes_metricas_anuais.csv',index=False)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/inventario_anual.py

Concilia a massa anual estática e horária, a geometria das fontes e as unidades de emissão antes da agregação territorial.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\inventario_anual.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| aermod_sources | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| methodology_rules | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shapely.ops | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/0_ref/seminarios_02/Resumo_Inventario_Congonhas_2023-R1.xlsx — chamada pd.read_excel, linha 45.

**Saídas.**

- {output}/{pol}_{name}.csv — chamada table.to_csv, linha 147.

**Campos e chaves lidos.**

- inv: key, matched_geometry, row, tpy.
- ids.loc: group.
- inv.loc: tpy.
- out.loc: emission_total_gs, inventory_match, inventory_row, line_rate_gs_m, source_area_m2, source_length_m.

**Campos e chaves gerados.**

- inv: description, group, key, matched_geometry, row, tpy.
- out: emission_annual_tpy, emission_basis, emission_total_gs, inventory_coordinate_distance_m, inventory_match, inventory_row, inventory_source_id, model_emission_total_gs.
- audit: inventory_file, inventory_year.
- alloc: emission_tpy.
- mass: emission_audit_status, emission_fallback_tpy, emission_inventory_pending_sources, emission_inventory_tpy.
- balance: allocated_tpy, overlap_warning, rate_basis, source_total_tpy, unallocated_tpy.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| apply_inventory(sources, pol) | 44-120 | lê dados Retorno: (out, audit, missing). |
| calculate_zone_emissions(sources, zones, pol, output) | 123-148 | grava produtos Retorno: (mass, groups, alloc, audit, missing). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/inventario_anual.py, linhas 77-83.

```python
        weights=sub.model_emission_total_gs.clip(lower=0)
        if len(sub)>1 and (not np.isfinite(weights).all() or weights.sum()<=0):

            if sub.geometry.geom_type.isin(['Polygon','MultiPolygon']).all():
                weights=sub.geometry.area
            elif sub.geometry.geom_type.isin(['LineString','MultiLineString']).all():
                weights=sub.geometry.length
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/inventario_anual.py, linhas 86-92.

```python
                continue
            if not np.isfinite(weights).all() or weights.sum()<=0:
                out.loc[sub.index,'inventory_match']='partição sem medida geométrica válida'
                continue
            out.loc[sub.index,'inventory_match']=out.loc[sub.index,'inventory_match']+'; partição por medida geométrica'
        weights=weights/weights.sum() if len(sub)>1 else pd.Series(1.,index=sub.index)

```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/io_utils.py

Io utils. Processamento ou módulo de apoio. A organização passa por ensure_dirs, first_existing, _read_kml_with_encoding_fallback, read_vector, normalize_name, excel_serial_to_datetime, _sanitize_vector_columns, save_gpkg, _shp_safe_columns, save_shp.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\io_utils.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| __future__ | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| tempfile | Arquivos temporários definidos pelo processamento. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- {path} — chamada gpd.read_file, linha 93.
- {path} — chamada path.read_bytes, linha 57.
- tmp.name — chamada gpd.read_file, linha 66.
- {path} — chamada zipfile.ZipFile, linha 84.

**Saídas.**

- {path} — chamada out.to_file, linha 183.
- path.with_name(path.stem + '_campos.csv') — chamada .to_csv, linha 186.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| ensure_dirs(*paths: Path) | 38-40 | Chamadas efetivas: p.mkdir |
| first_existing(preferred: Path  /  None, folder: Path, patterns) | 43-50 | Chamadas efetivas: preferred.exists, sorted, folder.glob, folder.rglob Retorno: None, preferred. |
| _read_kml_with_encoding_fallback(path: Path) | 53-71 | lê dados Retorno: gpd.read_file(path), gpd.read_file(tmp_path). |
| read_vector(path: Path, target_crs=CRS_PROJECT) | 74-106 | lê dados Retorno: gdf.to_crs(target_crs), gdf. |
| normalize_name(s) | 109-114 | Chamadas efetivas: .lower, .replace, .strip, re.sub, str, s.replace Retorno: re.sub('[^a-z0-9]+', '-', s).strip('-'). |
| excel_serial_to_datetime(series: pd.Series) | 117-124 | Chamadas efetivas: series.copy, pd.to_numeric, pd.to_datetime, len, .mean, numeric.notna, .between, numeric.dropna Retorno: pd.to_datetime(s, dayfirst=True, errors='coerce'), pd.to_datetime(numeric, unit='D', origin='1899-12-30', errors='coerce'). |
| _sanitize_vector_columns(gdf) | 127-143 | Chamadas efetivas: gdf.copy, .lower, out.drop, out.rename, .strip, drop_cols.append, str Retorno: out. |
| save_gpkg(gdf, path: Path, layer: str) | 146-149 | grava produtos |
| _shp_safe_columns(gdf) | 152-176 | Chamadas efetivas: gdf.copy, set, str, used.add, out.rename, .strip, .upper, re.sub Retorno: (out.rename(columns=rename), mapping). |
| save_shp(gdf, path: Path) | 179-188 | grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/io_utils.py, linhas 120-126.

```python
    numeric = pd.to_numeric(s, errors="coerce")
    numeric_share = numeric.notna().mean() if len(s) else 0
    if numeric_share > 0.8 and numeric.dropna().between(20000, 80000).mean() > 0.8:
        return pd.to_datetime(numeric, unit="D", origin="1899-12-30", errors="coerce")
    return pd.to_datetime(s, dayfirst=True, errors="coerce")

# Sanitize vector columns
```

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/landuse.py

Landuse. Processamento ou módulo de apoio. A organização passa por read_landuse, zonal_landuse_composition, dominant_landuse, read_landuse_clipped.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\landuse.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| __future__ | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| rasterio | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| rasterio.mask | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| rasterio.transform | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| rasterio.warp | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- {path} — chamada rasterio.open, linha 134.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| read_landuse(path: Path) | 78-84 | Chamadas efetivas: rasterio.open, .astype, src.read Retorno: (arr, src.transform, src.crs). |
| zonal_landuse_composition(path: Path, zones: gpd.GeoDataFrame, year: int) | 87-115 | Chamadas efetivas: pd.DataFrame, rasterio.open, zones.to_crs, z.iterrows, vals.astype, np.unique, counts.sum, zip Retorno: pd.DataFrame(rows). |
| dominant_landuse(composition: pd.DataFrame) | 118-124 | Chamadas efetivas: .idxmax, .copy, pd.DataFrame, composition.groupby Retorno: out, pd.DataFrame(columns=['zone_index', 'year', 'landuse_code', 'landuse_name', 'landuse_pct']). |
| read_landuse_clipped(path: Path, boundary: gpd.GeoDataFrame, buffer_m: float=3000.0, target_crs=None) | 127-174 | Chamadas efetivas: getattr, rasterio.open, boundary.to_crs, .buffer, mask, np.ma.isMaskedArray, np.float32, array_bounds Retorno: (dst, dst_transform, target_crs), (arr.astype(float), src_transform, src.crs or target_crs). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/landuse.py, linhas 104-110.

```python
            codes, counts = np.unique(vals, return_counts=True)
            total = counts.sum()
            for code, n in zip(codes, counts):
                rows.append({
                    "zone_index": zid,
                    "year": int(year),
                    "code": int(code),
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/main.py

Main. Processamento ou módulo de apoio. A organização passa por say, pol_label, _slugify_name, _valid_geometry_mask, complete_emission_abc_summary, resolve_vectors, station_workflow, load_source_workflow, model_workflow, plume_gif_workflow.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\main.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| PIL | Inspeção, composição ou ajuste de imagens pela biblioteca Pillow. |
| __future__ | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| aermod_post | Módulo autoral local; sua ficha está neste relatório. |
| aermod_sources | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| censo_ibge | Módulo autoral local; sua ficha está neste relatório. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| diagnostics | Módulo autoral local; sua ficha está neste relatório. |
| dispersion_contours | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| gerar_figuras_documentos | Módulo autoral local; sua ficha está neste relatório. |
| integracao_metodologica | Módulo autoral local; sua ficha está neste relatório. |
| io_utils | Módulo autoral local; sua ficha está neste relatório. |
| landuse | Módulo autoral local; sua ficha está neste relatório. |
| management | Módulo autoral local; sua ficha está neste relatório. |
| maps | Módulo autoral local; sua ficha está neste relatório. |
| methodology_rules | Módulo autoral local; sua ficha está neste relatório. |
| network_history | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| receptor_grid | Módulo autoral local; sua ficha está neste relatório. |
| representativity | Módulo autoral local; sua ficha está neste relatório. |
| risk | Módulo autoral local; sua ficha está neste relatório. |
| source_apportionment | Módulo autoral local; sua ficha está neste relatório. |
| standards | Módulo autoral local; sua ficha está neste relatório. |
| stations | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| traceback | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| unicodedata | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| zone_analysis | Módulo autoral local; sua ficha está neste relatório. |


**Entradas.**

- {fp} — chamada Image.open, linha 626.
- health_result.get('screening_zone') — chamada pd.read_csv, linha 981.
- health_result.get('screening_chronic_af') — chamada pd.read_csv, linha 1001.
- health_result.get('screening_acute_af') — chamada pd.read_csv, linha 1010.
- health_result.get('zone_summary') — chamada pd.read_csv, linha 1020.

**Saídas.**

- {out_root}/00_diagnostico/estacoes_metricas_3anos.csv — chamada metrics.to_csv, linha 279.
- {out_root}/00_diagnostico/estacoes_metricas_anuais.csv — chamada yearly.to_csv, linha 282.
- {out_root}/00_diagnostico/estacoes_metricas_trienios_moveis.csv — chamada .to_csv, linha 283.
- {out_root}/01_representatividade/estacoes_diagnostico_espacial.csv — chamada .to_csv, linha 302.
- {out_root}/00_diagnostico/ATENCAO_estacoes_sem_coordenada.txt — chamada .write_text, linha 305.
- {out_pol}/fontes_{pol}_auditoria.csv — chamada .to_csv, linha 353.
- {out_pol}/fontes_{pol}_alocacao_zoneamento.csv — chamada allocations.to_csv, linha 354.
- {out_pol}/fontes_{pol}_balanco_massa.csv — chamada mass_audit.to_csv, linha 356.
- {out_pol}/fontes_{pol}_balanco_massa_por_tipo.csv — chamada by_type.to_csv, linha 365.
- {out_pol}/fontes_{pol}_balanco_massa_por_grupo.csv — chamada by_group.to_csv, linha 374.
- {out_pol}/fontes_{pol}_grupos_por_zoneamento.csv — chamada gr.to_csv, linha 382.
- {out_pol}/emissoes_{pol}_ABC_por_setor_zoneamento.csv — chamada abc_emis.to_csv, linha 386.
- Mais 42 referências na ficha HTML e no inventário JSON.

**Campos e chaves lidos.**

- z: EMIS_PRESSAO_SCORE, zone_index.
- config.FILES: enterprises, municipality, roads, station_coords, station_network, zoning.
- config.DIRS: disp, emission, grade_generated, limite_cong, limite_emp, out, post, qar, uso_terra, vias, zoneamento.
- by_type: emission_allocated_gs, emission_total_gs.
- mass_audit: group_id.
- by_group: emission_allocated_gs, emission_total_gs.
- gr: emission_gs, group_id.
- zones_emit: GRUPO_EMISSOR_LOCAL_ID.
- sources: group_id.
- dd: date.
- daily_mean: date, ym.
- sub: X, Y, n_design_years, n_valid_hourly.
- hh: CONC, date, hour.
- land_diag: code, pixel_count.
- ca: ALL_ANNUAL_MEAN, GROUP_ANNUAL_MEAN.
- abc_scen: reduction_fraction_A.
- s30: EST_REDUCTION_PCT_ALL.
- abc_summary: ABC_PRIORITY_GROUP, zone_index.
- grid_result: output_dir, total_receptors.
- zpop: pop_1_10, pop_ge25, pop_ge30, pop_gt1.
- station_by_pol: PM25.
- hm: health_person_ugm3_excess_cf, health_pop_above_cf, health_pop_above_pv, health_population_exposed.
- haf: endpoint.
- hz: endpoint.
- metrics: pollutant.

**Campos e chaves gerados.**

- z: ABC_A_RED30_EST_PCT_ALL, dominant_group, dominant_group_pct, zone_index.
- municipality: geometry.
- zones: _zone_id, geometry.
- municipality.attrs: source_path.
- zones.attrs: source_path.
- enterprises.attrs: source_path.
- roads.attrs: source_path.
- by_type: allocated_pct.
- by_group: allocated_pct.
- gr: emission_pct_zone, group_id, rank_zone.
- zones_emit: AUDIT_FONTE_COMPLETA, zone_index.
- dd: date.
- daily_mean: ym.
- hh: date.
- land_diag: class_name, percent, plot_crs, recognized_mapbiomas, source_file.
- ca: ALL_CRIT_MEAN, GROUP_CRIT_MEAN.
- abc_summary: GRUPO_CONTR_ANUAL, GRUPO_CONTR_P98.
- zpop: zone_index.
- base_health: zone_index.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| say(msg) | 181-182 | Chamadas efetivas: print |
| pol_label(pol: str) | 185-187 | Chamadas efetivas: .get, getattr Retorno: getattr(config, 'POLLUTANT_DISPLAY', {}).get(pol, pol). |
| _slugify_name(value: str) | 190-193 | Chamadas efetivas: .decode, .lower, .encode, .strip, unicodedata.normalize, re.sub, str Retorno: txt or 'mapa'. |
| _valid_geometry_mask(gdf) | 196-197 | Chamadas efetivas: gdf.geometry.map Retorno: gdf.geometry.map(lambda geom: geom is not None and (not geom.is_empty)). |
| complete_emission_abc_summary(zones, summary) | 200-233 | Chamadas efetivas: zones.copy, pd.DataFrame, base.merge, text_defaults.items, numeric_defaults.items, summary.copy, .fillna, .isin Retorno: out. |
| resolve_vectors() | 236-273 | Chamadas efetivas: first_existing, read_vector, .copy, zones.index.astype, str, FileNotFoundError, municipality.geometry.make_valid, zones.geometry.make_valid Retorno: (municipality, zones, enterprises, roads). |
| station_workflow(municipality, zones, enterprises, roads, out_root) | 276-335 | grava produtos Retorno: (metrics, yearly, stations, by_pol). |
| load_source_workflow(pol, zones, enterprises, out_pol, municipality=None) | 338-418 | grava produtos Retorno: (zones_emit, sources, allocations), (zones.copy(), None, pd.DataFrame()). |
| model_workflow(pol, zones_emit, municipality, station_buffers_valid, out_pol, roads=None) | 421-526 | grava produtos; Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. Retorno: (model, yearly, post_path, z), (None, None, None, zones_emit). |
| plume_gif_workflow(pol, municipality, zones, out_pol, roads=None) | 529-639 | grava produtos |
| landuse_workflow(municipality, zones, roads, enterprises, stations, out_root) | 642-699 | grava produtos |
| source_apportionment_optional(pol, post_path, zones_result, model, out_pol, municipality=None) | 702-803 | grava produtos Retorno: abc_summary, pd.DataFrame(). |
| main() | 806-1086 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/main.py, linhas 514-520.

```python
                "concentration_threshold_high": pd.to_numeric(z[f"{pol}_QUAD_ANUAL_thr_conc"], errors="coerce").dropna().iloc[0] if pd.to_numeric(z[f"{pol}_QUAD_ANUAL_thr_conc"], errors="coerce").notna().any() else np.nan,
                "emission_min": emis_s.min(), "emission_median": emis_s.median(), "emission_q75": emis_s.quantile(0.75), "emission_max": emis_s.max(),
                "concentration_min": conc_s.min(), "concentration_median": conc_s.median(), "concentration_q75": conc_s.quantile(0.75), "concentration_max": conc_s.max(),
            }])
            audit.to_csv(quad_diag_dir / f"04_{pol}_quadrantes_auditoria.csv", index=False, encoding="utf-8-sig")
            z[[c for c in ["nome", "sigla", "EMIS_TOTAL_GS", "EMIS_INDUSTRIAL_GS", "EMIS_URBANA_GS", "EMIS_THR_INDUSTRIAL_GS", "EMIS_THR_URBANA_GS", "EMIS_ALTA_INDUSTRIAL", "EMIS_ALTA_URBANA", "EMIS_PRESSAO_TIPO", "EMIS_DENS_GS_KM2", "EMIS_HOTSPOT_P95", "EMIS_ALTA_TOTAL", "EMIS_ALTA_FOCAL", "EMIS_PRESSAO_ALTA", "EMIS_CRITERIO", "GRUPO_EMISSOR_LOCAL", "EMIS_DENTRO_MUN_GS", "EMIS_FORA_MUN_GS", "CONTR_EXTERNA_PCT", ann_col, f"{pol}_QUAD_ANUAL"] if c in z.columns]].to_csv(
                common_dir / f"04_{pol}_quadrantes_por_zona.csv", index=False, encoding="utf-8-sig"
```

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- quantile: Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/management.py

Prioriza zonas no esquema de gestão territorial da etapa anterior a partir dos campos e pesos declarados. É uma rotina distinta das regiões espaciais de gestão pós-banca. Antes de reutilizar, conferir quais indicadores, cortes e versões de concentração lhe foram fornecidos.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\management.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| __future__ | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- z: ABC_A_ALL_SHARE_PCT, PRIORIDADE_SCORE, PRIOR_CONC_PCTL, PRIOR_EMIS_PCTL, PRIOR_MON_GAP, PRIOR_REG_SCORE.

**Campos e chaves gerados.**

- z: ABC_A_RED30_EST_PCT_ALL, ACAO_GESTAO_SUGERIDA, EIXO_GESTAO_PRIORITARIO, ESTRATEGIA_FONTES, MONITORAMENTO_PRIORIDADE, PRIORIDADE_CLASSE, PRIORIDADE_SCORE, PRIOR_CONC_PCTL, PRIOR_EMIS_PCTL, PRIOR_MON_GAP, PRIOR_REG_SCORE, zone_index.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| _pct_rank(s) | 29-33 | Chamadas efetivas: pd.to_numeric, .clip, .sum, pd.Series, x.rank, x.notna Retorno: x.rank(pct=True, method='average').clip(0, 1), pd.Series(np.nan, index=x.index). |
| build_management_priority(zones, pollutant, abc_summary=None) | 36-156 | Chamadas efetivas: zones.copy, next, np.where, float, max, .astype, z.apply, z.index.rename Retorno: z, 'estratégia multissetorial - contribuição de concentração distribuída'. |
| management_methodology_table() | 159-167 | Chamadas efetivas: pd.DataFrame, float, getattr Retorno: pd.DataFrame([{'componente': 'Concentração anual relativa', 'peso': float(getattr(config, 'MANAGEMENT_WEIGHT_CONCENTRATION', 0.35)), 'metrica': 'percentil da concentração anual média por zona'}, {'com. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/management.py, linhas 30-36.

```python
    x=pd.to_numeric(s,errors="coerce")
    if x.notna().sum()==0:
        return pd.Series(np.nan,index=x.index)
    return x.rank(pct=True,method="average").clip(0,1)

# Build management priority
def build_management_priority(zones, pollutant, abc_summary=None):
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/manifesto_insumos_auditoria.py

Relaciona as bases de cada módulo sem mover ou alterar insumos originais.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\manifesto_insumos_auditoria.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- {p} — chamada p.open, linha 34.
- E:/projeto/output/06_censo_ibge/censo_diagnostico.csv — chamada pd.read_csv, linha 50.

**Saídas.**

- E:/projeto/output/15_auditoria_metodologica/manifesto_bases_por_modulo.csv — chamada .to_csv, linha 63.
- E:/projeto/output/15_auditoria_metodologica/manifesto_bases_resumo.json — chamada .write_text, linha 64.

**Campos e chaves lidos.**

- families: População e apoio territorial.
- x: modulo.

**Campos e chaves gerados.**

- families: Coordenadas das estações, Cálculo diário horário e conferência, Código dos indicadores, Documentos e referências cruzadas, EMI executado, Geometrias disponibilizadas para conciliação, Inventário e entradas, Memoriais industriais e urbanos, Meteorologia e cálculo horário, Monitoramento anual, Monitoramento histórico, Parâmetros sanitários, População e apoio territorial, Zoneamento e grade.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| digest(p) | 32-36 | Chamadas efetivas: hashlib.sha256, h.hexdigest, p.open, iter, h.update, f.read Retorno: h.hexdigest(). |
| run() | 39-65 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/manifesto_insumos_auditoria.py, linhas 32-40.

```python
def digest(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)
    return h.hexdigest()

# Run
def run():
    r=config.BASE;families={}
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/mapa_maximas_24h.py

Máximas diárias por receptor (FIRST), sem confundir com episódio simultâneo.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\mapa_maximas_24h.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| aermod_post | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| rasterio | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| rasterio.features | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| rasterio.transform | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| scipy.interpolate | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| standards | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- candidates[0] — chamada path.open, linha 84.

**Saídas.**

- {outdir}/{pol}_maximas_24h_receptores.csv — chamada maxima.to_csv, linha 81.
- {outdir}/{pol}_episodio_maximo_24h.csv — chamada .to_csv, linha 83.
- {outdir}/{pol}_maximas_24h_interpoladas.tif — chamada rasterio.open, linha 96.
- {outdir}/maximas_24h_metadados.json — chamada .write_text, linha 100.

**Campos e chaves lidos.**

- out: X, Y.
- config.DIRS: pos_cache, post.
- maxima: X, Y.

**Campos e chaves gerados.**

- out: N_DAYS.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| first_high(daily) | 46-59 | Chamadas efetivas: .copy, .any, .reset_index, .to_numpy, .all, ValueError, d.duplicated, d.sort_values Retorno: out.sort_values(['X', 'Y']).reset_index(drop=True). |
| build_24h(outdir) | 62-101 | grava produtos Retorno: (layers, options, metadata). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/mapa_maximas_24h.py, linhas 85-91.

```python
            header = src.readline().strip()
        metadata[pol] = dict(source=str(path),header=header,period_start=str(daily.date.min().date()),period_end=str(daily.date.max().date()),receptors=len(maxima),max_ug_m3=float(peak.CONC),date=str(peak.date.date()),X=float(peak.X),Y=float(peak.Y),excluded_incomplete_days=int((daily.N_HOURS!=24).sum()),background=0,statistic='FIRST: maior média de 24 h por receptor; datas não necessariamente coincidentes',pollutant_identification='Diretório do projeto; cabeçalho conserva referência PTS.isc, a confirmar no arquivo de controle da simulação')
        step=100.
        xmin,ymin=maxima[['X','Y']].min();xmax,ymax=maxima[['X','Y']].max()
        xs=np.arange(xmin,xmax+step,step);ys=np.arange(ymax,ymin-step,-step)
        xx,yy=np.meshgrid(xs,ys)
        surface=LinearNDInterpolator(maxima[['X','Y']].values,maxima.CONC.values)(xx,yy)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/mapas_apendices.py

Figuras permanentes dos apêndices; não executa o AERMOD.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\mapas_apendices.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| alocacao_territorial_emissoes | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| cartografia_apendices | Módulo autoral local; sua ficha está neste relatório. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| diagnostico_grupos_periodo | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| integracao_metodologica | Módulo autoral local; sua ficha está neste relatório. |
| io_utils | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.lines | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.patches | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.ticker | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| methodology_rules | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| standards | Módulo autoral local; sua ficha está neste relatório. |
| stations | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| textwrap | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| vector_portable | Módulo autoral local; sua ficha está neste relatório. |
| zone_analysis | Módulo autoral local; sua ficha está neste relatório. |


**Entradas.**

- E:/projeto/config.DIRS['out']/11_integracao/proveniencia_modelagem.csv — chamada pd.read_csv, linha 175.
- E:/projeto/config.DIRS['out']/11_integracao/{pol}_receptores_anuais.csv — chamada pd.read_csv, linha 184.
- E:/projeto/config.DIRS['out']/06_censo_ibge/censo_populacao_por_zoneamento.csv — chamada pd.read_csv, linha 228.
- E:/projeto/saude/saude_funcoes_cr_incidencia.csv — chamada pd.read_csv, linha 236.

**Saídas.**

- E:/projeto/config.DIRS['out']/11_integracao/apendices/Figura_{code}.{ext} — chamada fig.savefig, linha 138.
- E:/projeto/config.DIRS['out']/11_integracao/apendices/PM10_grupos_periodo_comum.csv — chamada contrib.to_csv, linha 223.
- E:/projeto/config.DIRS['out']/11_integracao/apendices/estacoes_anuais.csv — chamada annual.to_csv, linha 249.
- E:/projeto/config.DIRS['out']/11_integracao/apendices/estacoes_trienios.csv — chamada rolling.to_csv, linha 250.
- E:/projeto/config.DIRS['out']/11_integracao/apendices/atributos_figuras.csv — chamada .to_csv, linha 251.
- E:/projeto/config.DIRS['out']/11_integracao/apendices/resumo_figuras.json — chamada .write_text, linha 253.
- E:/projeto/config.DIRS['out']/11_integracao/apendices/index.html — chamada .write_text, linha 256.

**Campos e chaves lidos.**

- config.DIRS: limite_cong, out, post, qar.
- config.FILES: municipality.
- annual.loc: station_id.
- facts: pollutants.
- prov.loc: file.
- prov: group, pollutant.
- modelannual: year.
- lim: 24H, ANNUAL.
- POL: PM10, PM25.
- cr: baseline_rate_per_100k, control_ugm3, endpoint, exposure, rr_high, rr_low, rr_per_10ug.
- z.loc: PM25_annual_exposure.

**Campos e chaves gerados.**

- pal: Informação insuficiente.
- handles: origem.
- st: number.
- : integrated, integrated_year, quadrants.
- z: PM10_dominant_common_period, health_application, health_fraction_pct, pop_estimada, pop_ge30_estimada, pop_metodo_figura.
- facts: PM10_common_period, health, health_fraction, population_missing, population_sum.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| coord(value, pos, hemisphere) | 77-78 | Chamadas efetivas: .replace, abs Retorno: f'{abs(value):.2f}°{hemisphere}'.replace('.', ','). |
| render(z, muni, fields, code, titles, note, extent, *, stations=None, eligible=None, numeric=False, hatches=None) | 81-139 | grava produtos |
| run() | 144-257 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/mapas_apendices.py, linhas 242-248.

```python
        z[name]=np.nan
        z.loc[eligible_health,name]=100*(-np.expm1(-np.log(rr)/10*np.maximum(z.loc[eligible_health,'PM25_annual_exposure']-cr.control_ugm3,0)))
    z['health_application']=np.where(eligible_health,'Fração calculada; óbitos pendentes','Exposição ambiente não elegível')
    facts['health_fraction']={'n_zones':int(eligible_health.sum()),'min_pct':float(z.health_fraction_pct.min()),'max_pct':float(z.health_fraction_pct.max()),'rr':float(cr.rr_per_10ug),'counterfactual':float(cr.control_ugm3),'baseline_rate_available':bool(pd.notna(cr.baseline_rate_per_100k))}
    render(z,muni,['pop_estimada','health_fraction_pct'],'E1',['População estimada','Avaliação sanitária parcial'],
           'Habitantes estimados · Censo 2022 · alocação proporcional às interseções\nMantidos moradores rurais; refinamento por uso do solo em validação',extent,numeric=True)
    facts['health']='Fração calculada onde há monitoramento anual elegível; óbitos não quantificados por ausência de taxa basal'
```

Logaritmo natural. Na função de risco, β=ln(RR)/10 converte um risco relativo por 10 µg/m³ para a escala de 1 µg/m³.

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- log: Logaritmo natural. Na função de risco, β=ln(RR)/10 converte um risco relativo por 10 µg/m³ para a escala de 1 µg/m³.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/mapas_complementares.py

Complementos cartográficos com o mesmo renderizador dos apêndices.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\mapas_complementares.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| aermod_sources | Módulo autoral local; sua ficha está neste relatório. |
| alocacao_territorial_emissoes | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| cartografia_apendices | Módulo autoral local; sua ficha está neste relatório. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| io_utils | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| landuse | Módulo autoral local; sua ficha está neste relatório. |
| mapa_maximas_24h | Módulo autoral local; sua ficha está neste relatório. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| rasterio | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| rasterio.features | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| rasterio.transform | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| scipy.interpolate | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| standards | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| vector_portable | Módulo autoral local; sua ficha está neste relatório. |


**Entradas.**

- {OUT}/atributos_figuras.gpkg — chamada gpd.read_file, linha 78.
- {OUT}/resumo_figuras.json — chamada .read_text, linha 80.
- {OUT}/complementos_manifesto.json — chamada .read_text, linha 84.
- E:/projeto/config.DIRS['out']/13_rateio_emissoes/Correspondencia_ID.csv — chamada pd.read_csv, linha 92.
- E:/projeto/config.DIRS['out']/11_integracao/{pol}_receptores_anuais.csv — chamada pd.read_csv, linha 117.
- E:/projeto/config.DIRS['grade_generated']/grade_receptores_adaptativa.csv — chamada pd.read_csv, linha 139.
- E:/projeto/config.DIRS['vias']/vias_cong.shp — chamada gpd.read_file, linha 150.
- E:/projeto/config.DIRS['uso_terra']/mapbiomas-brazil-collection-101-congonhas-2024.tif — chamada rasterio.open, linha 155.
- E:/projeto/config.DIRS['out']/13_rateio_emissoes/Resumo_zonas.csv — chamada pd.read_csv, linha 162.
- {OUT}/index.html — chamada page.read_text, linha 186.

**Saídas.**

- E:/projeto/config.DIRS['out']/13_rateio_emissoes/fontes_rateio_{pol}.gpkg — chamada .to_file, linha 105.
- {OUT}/{pol}_concentracao_interpolada.tif — chamada rasterio.open, linha 133.
- E:/projeto/config.DIRS['out']/13_rateio_emissoes/zoneamento_rateio.gpkg — chamada .to_file, linha 179.
- {OUT}/complementos_manifesto.json — chamada .write_text, linha 184.
- {OUT}/index.html — chamada page.write_text, linha 190.

**Campos e chaves lidos.**

- config.FILES: municipality.
- config.DIRS: grade_generated, limite_cong, out, uso_terra, vias.
- facts: bounds_degrees.
- item: codigo, descricao, titulo.
- associations: poluente.
- s: dens_area, dens_linha, geometry, group_id, massa, source_id, source_type.
- df: VALID_YEAR, X, Y, year.
- valid: X, Y.
- grid: utm_x, utm_y.
- roads: fclass.
- summaries: poluente.
- revised: PM10_emission_class, PM10_massa_rateada_t_ano, PM25_emission_class, PM25_massa_rateada_t_ano, geometry, nome, zone_index.

**Campos e chaves gerados.**

- s: dens_area, dens_linha, massa, rateio.
- grid: localizacao.
- roads: classe.
- layer: massa_quantificada.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 76-191 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/mapas_complementares.py, linhas 121-127.

```python
    for p,pol in zip(points,['PM10','PM25']):
        valid=p.dropna(subset=['ANNUAL_MEAN']).groupby(['X','Y'],as_index=False).ANNUAL_MEAN.mean()
        xmin,ymin,xmax,ymax=p.total_bounds;step=100.
        xs=np.arange(xmin,xmax+step,step);ys=np.arange(ymax,ymin-step,-step)
        xx,yy=np.meshgrid(xs,ys)
        surface=LinearNDInterpolator(valid[['X','Y']].values,valid.ANNUAL_MEAN.values)(xx,yy)
        color_stages=('PF','PI4','PI3','PI2')
```

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

Trecho de codigo/mapas_complementares.py, linhas 148-154.

```python
    draw([grid],['localizacao'],'G2',['Grade de receptores'],
         f'{len(grid)} receptores; {inside.sum()} no município e {(~inside).sum()} externos, por teste geométrico. Não confundir ordem dos IDs com localização.',palette={'Dentro do município':'#26728f','Fora do município':'#ba7b45'})
    roads=gpd.read_file(config.DIRS['vias']/'vias_cong.shp')
    roads['classe']=roads.fclass.map(lambda v:'Rodovias principais' if v in ['motorway','trunk','primary','motorway_link','trunk_link','primary_link'] else 'Vias secundárias' if v in ['secondary','tertiary','secondary_link','tertiary_link'] else 'Vias locais e demais caminhos')
    draw([roads],['classe'],'H1',['Rede viária'],
         'Cadastro viário disponível; hierarquia derivada de fclass. A presença da via não comprova emissão inventariada nem volume de tráfego.',palette={'Rodovias principais':'#a54d40','Vias secundárias':'#b28d4f','Vias locais e demais caminhos':'#838f96'})
    raster=config.DIRS['uso_terra']/'mapbiomas-brazil-collection-101-congonhas-2024.tif'
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/mapas_direcionais_pareados.py

Um encarte MP10/MP2,5 por direção e duração, sem recalcular os dados.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\mapas_direcionais_pareados.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| argparse | Parâmetros fornecidos ao iniciar o programa. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| cartografia_apendices | Módulo autoral local; sua ficha está neste relatório. |
| concurrent.futures | Execução concorrente quando prevista pela rotina; não equivale a um novo método de cálculo. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| figuras_analises_direcionais | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| html | Escape e construção de páginas HTML de documentação/visualização. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| paleta_concentracoes | Módulo autoral local; sua ficha está neste relatório. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| subprocess | Chamada de outros programas e verificação de seus resultados de execução. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/16_revisao_pos_banca/zoneamento_pos_banca.gpkg — chamada gpd.read_file, linha 51.
- E:/projeto/output/16_revisao_pos_banca/celulas_analise.gpkg — chamada gpd.read_file, linha 51.
- E:/projeto/output/11_integracao/apendices/resumo_figuras.json — chamada .read_text, linha 52.
- E:/projeto/output/16_revisao_pos_banca/vento/analises_espaciais/{p}_{t}_receptores.csv — chamada pd.read_csv, linha 53.
- E:/projeto/output/16_revisao_pos_banca/vento/{p}_envelopes_{'horarios' if t == '1h' else 'diarios_persistentes'}.csv — chamada pd.read_csv, linha 54.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/perfis_normalizados_grupos_estacoes.csv — chamada pd.read_csv, linha 55.
- E:/projeto/output/15_auditoria_metodologica/revisao_cientifica/vinculos_estacoes_receptores.csv — chamada pd.read_csv, linha 56.
- E:/projeto/output/11_integracao/nova_modelagem/estacoes_trienio_comum.csv — chamada pd.read_csv, linha 57.
- E:/projeto/output/16_revisao_pos_banca/figuras/index.html — chamada p.read_text, linha 105.

**Saídas.**

- os.environ.get('CONGONHAS_PAIRED_OUTPUT', str(DATA / 'pares'))/index.html — chamada .write_text, linha 96.
- E:/projeto/output/16_revisao_pos_banca/figuras/index.html — chamada p.write_text, linha 108.

**Campos e chaves lidos.**

- eligible: n_design_years, pollutant.
- v: name.
- cells: geometry, receptor_id.

**Campos e chaves gerados.**

- sub: Q, Q_common, dominant_name.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run(directions, periods=None, concentrations_only=False) | 49-82 | lê dados; Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. |
| index() | 85-108 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/mapas_direcionais_pareados.py, linhas 65-71.

```python
                table=tables[pol,period];sub=table[table.direction.eq(direction)].copy()
                common=np.quantile(table.groupby('receptor_id').concentration.max(),[.2,.4,.6,.8])
                sub['Q']=sub.quintile.map(lambda v:'Q'+str(v));sub['Q_common']=['Q'+str(v) for v in np.searchsorted(common,sub.concentration,side='left')+1]
                sub['dominant_name']=sub.dominant_group.map({k:v['name'] for k,v in GROUPS.items()})
                pair.append(cells[['receptor_id','geometry']].merge(sub,on='receptor_id',validate='one_to_one'))
                raw=envelopes[pol,period];raw=raw[raw.direction.eq(direction)];v=table.concentration;positive=v[v>0]
                low=max(10.**np.floor(np.log10(positive.quantile(.02))),.01);cap=float(positive.quantile(.99));unit=10.**np.floor(np.log10(cap));cap=max(10*low,np.floor(cap/unit)*unit)
```

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

**Cálculos a observar nesta rotina.**

- quantile: Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/mapas_nova_modelagem.py

Cartografia da rodada nova no padrão dos apêndices, sem apagar a anterior.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\mapas_nova_modelagem.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| cartografia_apendices | Módulo autoral local; sua ficha está neste relatório. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| io_utils | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| vector_portable | Módulo autoral local; sua ficha está neste relatório. |


**Entradas.**

- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/zoneamento_nova_modelagem.gpkg — chamada gpd.read_file, linha 43.
- E:/projeto/config.DIRS['out']/11_integracao/apendices/resumo_figuras.json — chamada .read_text, linha 45.
- E:/projeto/config.DIRS['out']/13_rateio_emissoes/fontes_rateio_{pol}.gpkg — chamada gpd.read_file, linha 53.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/index.html — chamada index.read_text, linha 63.
- E:/projeto/config.DIRS['out']/11_integracao/apendices/index.html — chamada current.read_text, linha 70.

**Saídas.**

- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/auditoria_densidades.json — chamada .write_text, linha 62.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/index.html — chamada index.write_text, linha 67.
- E:/projeto/config.DIRS['out']/11_integracao/apendices/index.html — chamada current.write_text, linha 73.

**Campos e chaves lidos.**

- config.DIRS: limite_cong, out.
- config.FILES: municipality.
- s: dens_area, dens_linha, massa, source_type, support_m2.

**Campos e chaves gerados.**

- s: density_checked, support_m2.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 41-74 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/mapas_nova_modelagem.py, linhas 41-49.

```python
def run():
    out=config.DIRS['out']/'11_integracao/nova_modelagem';cart.OUT=out
    z=gpd.read_file(out/'zoneamento_nova_modelagem.gpkg')
    m=read(first_existing(config.FILES['municipality'],config.DIRS['limite_cong'],['*.kml','*.kmz','*.gpkg','*.shp'])).to_crs(config.CRS_PROJECT)
    extent=json.loads((config.DIRS['out']/'11_integracao/apendices/resumo_figuras.json').read_text(encoding='utf8'))['bounds_degrees']
    cart.render(z,m,['PM10_saturacao_comparativa','PM25_saturacao_comparativa'],'S1',['MP₁₀ · saturação comparativa','MP₂,₅ · saturação comparativa'],
        'Pior condição anual/24 h em 2021–2023. PI-2 como referência de planejamento. Contribuição primária sem fundo; não constitui classe conclusiva do ar ambiente.',extent,
        palette={'Abaixo da faixa preventiva':'#a6cde0','Próxima do padrão':'#f4cf75','Acima do padrão':'#c94343','Informação insuficiente':'#dddddd'})
    cart.render(z,m,['PM10_grupo_principal','PM25_grupo_principal'],'D1',['MP₁₀ · grupo principal','MP₂,₅ · grupo principal'],
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/maps.py

Maps. Processamento ou módulo de apoio. A organização passa por _valid_geometry_mask, _base_ax, _surface_cmap, _road_field, _download_ibge_regional_boundaries, _load_regional_boundaries, _regional_name_field, _plot_fallback_regional_labels, _load_model_grid_points, _focus_extent.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\maps.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| __future__ | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| contextily | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| io_utils | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| matplotlib.cm | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.lines | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.patches | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.tri | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| rasterio.plot | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| scipy.interpolate | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| tempfile | Arquivos temporários definidos pelo processamento. |
| urllib.parse | Requisições e manipulação de endereços de serviços públicos. |
| urllib.request | Requisições e manipulação de endereços de serviços públicos. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- getattr(config, 'REGIONAL_BOUNDARIES_CACHE', Path(__file__).resolve().parent / 'base_regional' / 'municipios_vizinhos_cache.geojson') — chamada gpd.read_file, linha 190.
- first_existing(config.FILES.get('grid_500m'), config.DIRS.get('grade'), ['*500m*.csv', '*grid*.csv']) — chamada pd.read_csv, linha 304.

**Saídas.**

- getattr(config, 'REGIONAL_BOUNDARIES_CACHE', Path(__file__).resolve().parent / 'base_regional' / 'municipios_vizinhos_cache.geojson') — chamada reg.to_file, linha 226.
- {out_png} — chamada fig.savefig, linha 1373.

**Campos e chaves lidos.**

- config.FILES: regional_municipalities.
- d: x, y.
- st: color, linestyle, linewidth.
- sb: station_name.
- points: CONC, geometry.
- g: _value.
- STATUS_COLORS: atendimento, insuficiente, nao_atendimento.
- data: CONC.
- area: surface_rate_gs_m2.
- sub: _v.
- s: _v, emission_total_gs, source_type, urban_subgroup.
- r: _v.
- pts: _v.
- show: ABC_CLASS, ABC_CUM_PCT, MEAN_GROUP_CONC, group_name.
- class_colors: A, B, C.
- z: _plot.
- zones: EMIS_DENS_CLASS.

**Campos e chaves gerados.**

- d: x, y.
- sb: station_name.
- sp: station_name.
- g: _value, geometry.
- area: surface_rate_gs_m2.
- sub: _v.
- pp: geometry.
- s: _v.
- z: _plot.
- pnt: geometry.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| _valid_geometry_mask(gdf) | 144-145 | Chamadas efetivas: gdf.geometry.map Retorno: gdf.geometry.map(lambda geom: geom is not None and (not geom.is_empty)). |
| _base_ax(title) | 150-167 | Chamadas efetivas: plt.subplots, ax.set_title, ax.set_xlabel, ax.set_ylabel, ax.set_aspect, ax.ticklabel_format, ax.tick_params, ax.get_yticklabels Retorno: (fig, ax). |
| _surface_cmap() | 170-172 | Chamadas efetivas: LinearSegmentedColormap.from_list Retorno: LinearSegmentedColormap.from_list('congonhas_air', colors, N=256). |
| _road_field(roads) | 175-180 | Chamadas efetivas: .lower, lower.get, str, getattr, .strip Retorno: lower.get(target), None. |
| _download_ibge_regional_boundaries(municipality) | 183-231 | lê dados; grava produtos Retorno: reg, reg.to_crs(municipality.crs). |
| _load_regional_boundaries(municipality) | 234-270 | Chamadas efetivas: str, config.FILES.get, .buffer, .copy, Path, config.DIRS.get, target.exists, _download_ibge_regional_boundaries Retorno: _REGIONAL_CACHE[key], _REGIONAL_CACHE[key]. |
| _regional_name_field(gdf) | 273-280 | Chamadas efetivas: .lower, str Retorno: None, None. |
| _plot_fallback_regional_labels(ax, municipality) | 283-295 | Chamadas efetivas: municipality.geometry.union_all, float, getattr, union.buffer, ax.text, str, dict |
| _load_model_grid_points(municipality) | 298-330 | lê dados Retorno: g if not g.empty else None, None. |
| _focus_extent(ax, municipality, model_context=False) | 333-342 | Chamadas efetivas: float, municipality.geometry.union_all, ax.set_xlim, ax.set_ylim, union.buffer, getattr |
| _plot_regional_background(ax, municipality, roads=None, zones=None, show_buffer=False, show_grid=False) | 345-420 | Chamadas efetivas: bool, setattr, _focus_extent, _try_add_basemap, municipality.geometry.union_all, float, union.buffer, _load_regional_boundaries |
| _set_extent(ax, municipality, points=None, use_points=True) | 423-431 | Chamadas efetivas: bool, _focus_extent, _add_scalebar, _add_north_arrow, getattr, _try_add_basemap |
| _try_add_basemap(ax) | 434-460 | Chamadas efetivas: float, getattr, ctx.add_basemap Retorno: False, False. |
| _fmt_dist(m) | 463-467 | Organiza parâmetros, expressões ou retorno sem chamada externa. Retorno: f'{m:g} m', f'{km:g} km'. |
| _add_scalebar(ax, length_m=None) | 470-485 | Chamadas efetivas: ax.get_xlim, ax.get_ylim, ax.add_patch, ax.text, Rectangle, _fmt_dist |
| _add_standard_ticks_to_cbar(cbar, vmin, vmax, standard_lines) | 488-501 | Chamadas efetivas: cbar.ax.get_xaxis_transform, cbar.ax.axvline, cbar.ax.text, float, colors.get |
| _add_north_arrow(ax, loc='br') | 504-517 | Chamadas efetivas: ax.get_xlim, ax.get_ylim, ax.annotate, ax.text, dict |
| _legend_below(ax, handles, ncol=3, title=None, fontsize=8) | 520-525 | Chamadas efetivas: ax.legend, .set_fontweight, leg.get_title |
| _legend_right(ax, handles, title=None, fontsize=8) | 528-533 | Chamadas efetivas: ax.legend, .set_fontweight, leg.get_title |
| plot_roads_by_class(ax, roads, legend=True, alpha=1.0, zorder=1) | 535-551 | Chamadas efetivas: _road_field, roads.to_crs, roads.plot, sub.plot, handles.append, getattr, _legend_below, Line2D Retorno: handles, []. |
| plot_representativity(municipality, zones, station_points, station_buffers, pollutant, out_png, roads=None) | 554-587 | grava produtos |
| _masked_triangulation(points, domain) | 590-601 | Chamadas efetivas: points.geometry.x.to_numpy, points.geometry.y.to_numpy, mtri.Triangulation, domain.geometry.union_all, .mean, np.array, tri.set_mask, geom.covers Retorno: tri. |
| plot_surface(points, value_col, domain, municipality, zones, title, units, out_png, standard=None, standard_lines=None, roads=None) | 604-659 | grava produtos |
| _extract_contour_value(gdf) | 662-673 | Chamadas efetivas: pd.api.types.is_numeric_dtype, s.astype, pd.to_numeric, txt.str.extract, .sum, max, vals.notna, len Retorno: None, pd.to_numeric(s, errors='coerce'). |
| plot_contour_polygons(contours, municipality, title, out_png, units='µg/m³', roads=None, standard_lines=None) | 676-715 | grava produtos |
| plot_status_zones(zones, status_col, municipality, title, out_png, model_context=False) | 718-736 | grava produtos |
| plot_quadrants(zones, col, municipality, title, out_png) | 739-753 | grava produtos |
| plot_separated_emission_concentration(zones, class_col, municipality, title, out_png) | 756-791 | grava produtos |
| plot_quadrant_scatter(zones, emission_col, concentration_col, class_col, title, out_png) | 794-827 | grava produtos |
| plot_landuse(raster_array, transform, code_to_color, code_to_name, boundary, title, out_png, roads=None, enterprises=None, stations=None) | 830-874 | grava produtos |
| plot_plume_frame(points, municipality, zones, title, out_png, vmax=None, standard_lines=None, roads=None, dpi=None, min_percentile=None, min_fraction_max=None) | 877-941 | grava produtos |
| plot_category_map(zones, col, municipality, title, out_png, palette=None, legend_title='Classe') | 944-983 | grava produtos |
| plot_zoning(zones, municipality, out_png, title='Zoneamento municipal de Congonhas') | 986-1014 | grava produtos |
| _plot_outline_mixed(ax, gdf, color, linewidth=0.7, alpha=0.7, zorder=2) | 1017-1028 | Chamadas efetivas: .copy, lines.plot, polys.boundary.plot, pts.plot, gdf.geometry.geom_type.isin |
| plot_source_emission_spatial(sources, municipality, out_png, title='Distribuição espacial da emissão nas fontes') | 1031-1093 | grava produtos; Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. |
| plot_source_total_emission_spatial(sources, municipality, out_png, title='Emissão total por fonte') | 1096-1135 | grava produtos |
| plot_abc_curve(global_abc, out_png, title='Curva ABC das contribuições por grupo') | 1138-1175 | grava produtos |
| plot_numeric_zone_map(zones, col, municipality, out_png, title, legend_label, cmap='cividis', fmt='.1f') | 1178-1197 | grava produtos |
| plot_sources_map(sources, municipality, out_png, title='Fontes de emissão') | 1200-1263 | grava produtos |
| plot_emission_density(zones, municipality, out_png, title='Densidade de emissão por zona', sources=None) | 1266-1328 | grava produtos; Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. |
| plot_emission_density_classes(zones, municipality, out_png, title='Classes de densidade de emissão') | 1331-1362 | grava produtos |
| plot_road_classes(roads, municipality, out_png, title='Rede viária classificada por fclass') | 1365-1374 | grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/maps.py, linhas 905-911.

```python
    vmax_local = float(np.nanmax(positive))
    eps = max(float(np.nanpercentile(positive, pctl)), frac * vmax_local, 1e-6)
    ZI = np.where(np.isfinite(ZI) & (ZI >= eps), ZI, np.nan)
    if np.isfinite(ZI).sum() == 0:
        plt.close(fig)
        return
    zmin = float(np.nanmin(ZI))
```

Percentil que ignora NaN. O número e o período de valores válidos continuam definindo sua representatividade.

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/maps.py, linhas 1053-1059.

```python
        vals = area["surface_rate_gs_m2"].to_numpy(dtype=float)
        vmin = float(np.nanpercentile(vals, 2)) if len(vals) > 2 else float(np.nanmin(vals))
        vmax = float(np.nanpercentile(vals, 98)) if len(vals) > 2 else float(np.nanmax(vals))
        vmin = max(vmin, float(np.nanmin(vals[vals > 0])))
        vmax = max(vmax, vmin * 1.0001)
        norm = LogNorm(vmin=vmin, vmax=vmax) if vmax / vmin > 20 else Normalize(vmin=vmin, vmax=vmax)
        area.plot(ax=ax, column="surface_rate_gs_m2", cmap="cividis", norm=norm,
```

Percentil que ignora NaN. O número e o período de valores válidos continuam definindo sua representatividade.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- nanpercentile: Percentil que ignora NaN. O número e o período de valores válidos continuam definindo sua representatividade.
- quantile: Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.
- sqrt: Raiz quadrada. No ajuste ponderado do k-means, multiplicar a coluna por √peso faz o peso entrar uma única vez na distância ao quadrado.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/medias_horarias_verificadas.py

Reconstrói médias diárias a partir das saídas horárias respeitando códigos, horas válidas e tratamento de calmarias, e compara o resultado com a saída nativa diária do AERMOD.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\medias_horarias_verificadas.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| out_aermod_reader | Módulo autoral local; sua ficha está neste relatório. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/houremiss/AERMET-3Y.SFC — chamada pd.read_csv, linha 71.
- E:/projeto/houremiss/AERMET-3Y.PFL — chamada pd.read_csv, linha 76.
- E:/projeto/houremiss/AERMET-3Y.SFC — chamada s.read_bytes, linha 86.
- E:/projeto/houremiss/AERMET-3Y.PFL — chamada p.read_bytes, linha 86.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_medias_diarias_1h_manifesto.json — chamada meta.read_text, linha 94.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_medias_diarias_1h.csv.gz — chamada pd.read_csv, linha 101.
- selected['ALL', '24H'] — chamada read_table, linha 113.
- selected['ALL', '1H'] — chamada pd.read_csv, linha 116.

**Saídas.**

- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_medias_diarias_1h.csv.gz — chamada check.to_csv, linha 135.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_denominadores_diarios.csv — chamada daytable.to_csv, linha 137.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_auditoria_media_anual_horaria.csv — chamada a.to_csv, linha 142.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_medias_diarias_1h_manifesto.json — chamada .write_text, linha 144.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/auditoria_medias_horarias.json — chamada .write_text, linha 147.

**Campos e chaves lidos.**

- config.DIRS: out, post.
- cal: CODE, year.
- m: comparison_passed, daily_post, meteorology.
- d: date, day.
- selected: 1H, 24H, ALL, ANNUAL.
- raw24: CODE, X, Y, day.
- chunk: CONC, X, Y.
- sums: count, sum.
- a: sum.

**Campos e chaves gerados.**

- cal: day, year.
- d: date, year.
- raw24: day.
- chunk: day.
- sums: daily_from_1h, denominator, mean_div24, valid_hours.
- check: difference.
- a: annual_reconstructed, denominator.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| model_daily_mean(hourly_sum, valid_hours) | 59-62 | Chamadas efetivas: np.any, ValueError, np.asarray, np.maximum Retorno: np.asarray(hourly_sum) / np.maximum(valid_hours, 18). |
| identity(p) | 65-66 | Chamadas efetivas: Path, str, p.resolve, p.stat Retorno: {'path': str(p.resolve()), 'bytes': p.stat().st_size, 'mtime_ns': p.stat().st_mtime_ns}. |
| met_calendar() | 69-86 | lê dados Retorno: (cal, {'sfc': identity(s), 'pfl': identity(p), 'sfc_sha256': hashlib.sha256(s.read_bytes()).hexdigest(), 'pfl_sha256': hashlib.sha256(p.read_bytes()).hexdigest()}). |
| cached_daily(path24) | 89-103 | lê dados Retorno: d.rename(columns={'daily_from_1h': 'CONC'})[['X', 'Y', 'date', 'year', 'CONC']]. |
| run() | 106-148 | lê dados; grava produtos Retorno: report. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/medias_horarias_verificadas.py, linhas 108-114.

```python
 OUT.mkdir(exist_ok=True,parents=True);cal,met=met_calendar();valid=cal.set_index('CODE').valid
 days=cal.groupby('day').valid.sum().rename('valid_hours');report={}
 for pol,folder in [('PM10','PM10'),('PM25','PM2-5')]:
  selected,_=discover(config.DIRS['post']/folder);path=selected['ALL','1H'];parts=[];nrows=0;invalid_nonzero=0
  print(pol,'lendo integralmente POST de 1 h',flush=True)
  raw24=read_table(selected['ALL','24H']);raw24['day']=raw24.CODE//100
  raw24=raw24[raw24.day.between(210101,231231)][['X','Y','day','CONC']]
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/medias_horarias_verificadas.py, linhas 122-128.

```python
   ok=chunk.CODE.map(valid);assert ok.notna().all()
   invalid_nonzero+=int((~ok&chunk.CONC.ne(0)).sum())
   parts.append(chunk.groupby(['X','Y','day'],as_index=False).CONC.agg(['sum','count']).reset_index())
  assert invalid_nonzero==0,'Concentração não nula em hora meteorológica inválida; revisar calendário.'
  sums=pd.concat(parts).groupby(['X','Y','day'],as_index=False)[['sum','count']].sum()
  assert sums['count'].eq(24).all() and len(sums)==nr*1095
  sums['valid_hours']=sums.day.map(days);sums['denominator']=np.maximum(sums.valid_hours,18)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/methodology_rules.py

Regras compartilhadas do seminário; não executa simulações nem grava arquivos.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\methodology_rules.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| __future__ | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| standards | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- a: annual_hours, emission_tpy.
- sub.loc: emission_tpy, group_id.
- daily: CONC, X, Y, date.
- row: ANNUAL_MODEL, P98_MODEL.
- lim: 24H, ANNUAL.

**Campos e chaves gerados.**

- a: _annual_hours, emission_gs, emission_tpy, group_id.
- groups: annual_hours_max, annual_hours_min, annualization_basis, emission_class, high_emission, minor_threshold_tpy, threshold_tpy.
- d: CONC, date, quarter, year.
- result: MIN_QUARTER_COMPLETENESS, VALID_YEAR.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| group_mass_classes(allocations, zone_ids, pollutant, *, annual_hours=8760.0, annualization_basis='cenario_continuo') | 42-107 | Chamadas efetivas: list, allocations.copy, a.group_id.fillna, pd.to_numeric, .any, .sum, .to_numpy, np.select Retorno: (pd.DataFrame(rows).set_index('zone_index'), groups). |
| concentration_priority(statuses) | 110-115 | Chamadas efetivas: any, statuses.get, str, max, enumerate Retorno: 'P' + str(max([0] + [i for i, v in enumerate(values, 1) if v == 'nao_atendimento'])), 'Informação insuficiente'. |
| add_zone_priorities(zones, pollutant) | 118-123 | Chamadas efetivas: zones.copy, concentration_priority, z.iterrows Retorno: z. |
| model_annual_metrics(daily) | 126-142 | Chamadas efetivas: .copy, .dt.normalize, .any, pd.to_numeric, .agg, .fillna, range, counts.min Retorno: result.reset_index(). |
| model_period_metrics(yearly, years, pollutant) | 145-159 | Chamadas efetivas: tuple, yearly.groupby, pd.DataFrame, .reindex, bool, rows.append, np.isfinite, valid.all Retorno: pd.DataFrame(rows). |
| abc_classes(values, a_limit=80.0, b_limit=95.0) | 162-184 | Chamadas efetivas: np.asarray, np.any, enumerate, ValueError, np.full, result.append, np.diff, len Retorno: np.asarray(result, dtype=object), np.full(len(v), 'insuficiente', dtype=object). |
| rolling_station_metrics(yearly, start_year=2018, end_year=None) | 187-217 | Chamadas efetivas: .any, int, yearly.groupby, pd.DataFrame, ValueError, yearly.year.max, group.set_index, range Retorno: pd.DataFrame(rows), pd.DataFrame(). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/methodology_rules.py, linhas 75-81.

```python
        a['_annual_hours']=hours
    groups=a.groupby(['zone_index','group_id'],as_index=False)[['emission_gs','emission_tpy']].sum()
    groups['threshold_tpy']=100.
    groups['minor_threshold_tpy']=minor
    groups['annualization_basis']=annualization_basis
    groups['annual_hours_min']=a.groupby(['zone_index','group_id'])._annual_hours.min().to_numpy()
    groups['annual_hours_max']=a.groupby(['zone_index','group_id'])._annual_hours.max().to_numpy()
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/methodology_rules.py, linhas 93-99.

```python
        mx=float(sub.emission_tpy.max()) if len(sub) else 0.0
        unknown=float(sub.loc[sub.group_id.eq('NAO_IDENTIFICADO'),'emission_tpy'].sum())
        total=float(sub.emission_tpy.sum())
        high=total>100 and not np.isclose(total,100,rtol=0,atol=1e-10)
        rows.append({'zone_index':zid,'emission_total_gs':float(sub.emission_gs.sum()),
                     'emission_max_group_gs':float(sub.emission_gs.max()) if len(sub) else 0.,
                     'emission_total_tpy':float(sub.emission_tpy.sum()),'emission_max_group_tpy':mx,
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/monitoramento_mma.py

Padroniza as novas planilhas das estações, reúne o histórico disponível e produz indicadores diários, anuais, por quadrimestre e por triênio. Os critérios vêm de config: dia com pelo menos 18 horas válidas e ano com pelo menos 50% de dias válidos em cada quadrimestre no recorte adotado. Preserva a cobertura por estação/poluente e não torna automaticamente simultâneos os anos de monitoramento e modelagem.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\monitoramento_mma.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| calendar | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| standards | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| unicodedata | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |


**Entradas.**

- {path} — chamada pd.read_excel, linha 155.
- E:/projeto/config.DIRS['cache']/monitoramento_mma/assinatura.json — chamada key.read_text, linha 133.
- E:/projeto/config.DIRS['cache']/monitoramento_mma/leitura.json — chamada .read_text, linha 134.

**Saídas.**

- E:/projeto/config.DIRS['cache']/monitoramento_mma/leitura.json — chamada .write_text, linha 145.
- E:/projeto/config.DIRS['cache']/monitoramento_mma/assinatura.json — chamada key.write_text, linha 146.

**Campos e chaves lidos.**

- out: DV, PM10, PM25, VV, datetime.
- cols: VV.
- config.DIRS: cache.
- a: station_id, year.
- x: path.
- old: DATA.
- f: datetime.
- df: datetime.

**Campos e chaves gerados.**

- out: DV, station_id.
- day: quadrimestre, valid_day, year.
- r: n_valid_hourly, n_valid_hourly_historical.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| norm(value) | 47-48 | Chamadas efetivas: re.sub, .lower, .decode, .encode, unicodedata.normalize, .replace, str Retorno: re.sub('[^a-z0-9]', '', unicodedata.normalize('NFKD', str(value).replace('º', '').replace('°', '')).encode('ascii', 'ignore').decode().lower()). |
| read_raw(path) | 61-92 | lê dados Retorno: (out, audit). |
| load_network(folder=None) | 95-147 | lê dados; grava produtos Retorno: ({sid: g.copy() for sid, g in d.groupby('station_id')}, audit), ({sid: g.copy() for sid, g in d.groupby('station_id')}, audit). |
| add_missing_legacy_years(data, audit, paths) | 150-170 | lê dados Retorno: (combined.groupby(['station_id', 'datetime'], as_index=False).mean(numeric_only=True), audit). |
| daily_and_yearly(df, pol, first=2017, last=2025) | 173-190 | Chamadas efetivas: .mean, .reindex, .astype, day.n_hours.ge, day.groupby, df.assign, pd.date_range, sub.value.dropna Retorno: (day, pd.DataFrame(yearly), pd.DataFrame(periods)). |
| all_tables(frames, first=2017, last=2025) | 193-199 | Chamadas efetivas: frames.items, pd.concat, daily_and_yearly, ys.append, qs.append, .sum, .notna Retorno: (pd.concat(ys, ignore_index=True), pd.concat(qs, ignore_index=True), daily). |
| selected_metrics(yearly, rolling, frames, end=2025) | 202-210 | Chamadas efetivas: yearly.groupby, pd.DataFrame, .to_dict, int, rows.append, .sum, .notna, f.datetime.dt.year.between Retorno: pd.DataFrame(rows). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/monitoramento_mma.py, linhas 62-68.

```python
    raw=pd.read_excel(path,header=None)
    header=max(range(min(10,len(raw))),key=lambda i:sum(norm(v) in TOKENS for v in raw.iloc[i]))
    cols={TOKENS[norm(v)]:j for j,v in enumerate(raw.iloc[header]) if norm(v) in TOKENS}
    if not cols:raise ValueError(f'Cabeçalho não reconhecido: {path}')
    n=norm(re.split(r'20\d{2}',path.stem)[0]);matches=[key for key in NAMES if key in n]
    if len(matches)!=1:raise ValueError(f'Estação ambígua: {path}')
    sid,name=NAMES[matches[0]]
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/monitoramento_mma.py, linhas 77-83.

```python
        out[target]=pd.to_numeric(s.map(lambda v:v.replace(',','.') if isinstance(v,str) else v),errors='coerce').replace([np.inf,-np.inf],np.nan)
    year=int(re.search(r'(20\d{2})',path.name)[1]);other=int((out.datetime.notna()&out.datetime.dt.year.ne(year)).sum())
    out=out[out.datetime.dt.year.eq(year)].copy();out.datetime=out.datetime.dt.floor('h')
    for pol in ['PM10','PM25']:
        if pol not in out:out[pol]=np.nan
        out[pol]=out[pol].mask(out[pol].le(0) if config.ZERO_AS_MISSING else out[pol].lt(0))
    for c in ['VV','PP','RS']:
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/network_history.py

Avaliação histórica da rede; independente da execução dos POSTFILEs AERMOD.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\network_history.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| argparse | Parâmetros fornecidos ao iniciar o programa. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| monitoramento_mma | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| rasterio | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| rasterio.features | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shapely.ops | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| stations | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/config.DIRS['out']/06_censo_ibge/censo_setores_congonhas.gpkg — chamada gpd.read_file, linha 194.
- config.FILES['landuse_2024'] — chamada rasterio.open, linha 197.

**Saídas.**

- {folder}/{name}.svg — chamada fig.savefig, linha 122.
- {folder}/{name}.png — chamada fig.savefig, linha 123.
- {out}/cobertura_populacao_setores.csv — chamada .to_csv, linha 244.
- {out}/cobertura_populacional.csv — chamada result.to_csv, linha 245.
- out or OUT/execucao.json — chamada .write_text, linha 284.
- out or OUT/representatividade_anual.csv — chamada annual.to_csv, linha 273.
- out or OUT/representatividade_periodos.csv — chamada .to_csv, linha 274.
- out or OUT/ultrapassagens.csv — chamada exceed.to_csv, linha 275.
- out or OUT/auditoria_series.csv — chamada .to_csv, linha 276.
- out or OUT/series_diarias.csv — chamada .to_csv, linha 277.

**Campos e chaves lidos.**

- config.DIRS: out.
- d.loc: mean_ug_m3.
- eligible.loc: mean_ug_m3.
- a: annual_mean_ug_m3, profile, year.
- config.FILES: landuse_2024, station_coords, station_network.
- support.loc: population.
- sub.loc: station_id.
- result: coverage_type.
- f: PM10, PM25.

**Campos e chaves gerados.**

- daily: valid_hours, year.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| daily_series(frame, pollutant, first_year, last_year) | 59-74 | Chamadas efetivas: .replace, values.mask, pd.DataFrame, .value.mean, .rename, pd.date_range, daily.reindex, .astype Retorno: daily. |
| summarize(daily, station, pollutant) | 77-118 | Chamadas efetivas: PROFILES.items, daily.groupby, range, int, annual.append, .items, period_valid.append, periods.append Retorno: (annual, periods, exceed). |
| save_figure(fig, folder, name) | 121-124 | grava produtos |
| figures(dailies, annual, exceed, out) | 127-181 | Chamadas efetivas: folder.mkdir, plt.rcParams.update, dailies.items, config.STATION_DISPLAY_NAMES.get, plt.subplots, daily.mean_ug_m3.where, .plot, zip |
| population_support() | 184-209 | lê dados Retorno: gpd.GeoDataFrame(rows, crs=sectors.crs). |
| coverage_estimate(support, geometry) | 212-214 | Chamadas efetivas: .clip, float, .sum, support.geometry.intersection Retorno: (float((support.population * fractions).sum()), fractions). |
| population_coverage(stations, annual, out) | 217-252 | grava produtos Retorno: result. |
| run(frames=None, stations=None, out=None) | 255-288 | grava produtos Retorno: (annual, exceed, coverage). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/network_history.py, linhas 65-71.

```python
    raw = pd.DataFrame({'hour': frame.datetime.dt.floor('h'), 'value': values})
    hourly = raw.groupby('hour').value.mean()
    daily = hourly.resample('D').agg(['mean','count']).rename(columns={'mean':'mean_ug_m3','count':'valid_hours'})
    calendar = pd.date_range(f'{first_year}-01-01',f'{last_year}-12-31',freq='D',name='date')
    daily = daily.reindex(calendar)
    daily['valid_hours'] = daily.valid_hours.fillna(0).astype(int)
    daily['year'] = daily.index.year
```

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

Trecho de codigo/network_history.py, linhas 84-90.

```python
                sub = d[((d.index.month-1)//months+1)==number]
                n = int(sub[flag].sum())
                ok = n/len(sub) >= minimum
                period_valid.append(ok)
                periods.append(dict(station_id=station,pollutant=pollutant,profile=profile,year=year,
                    period_type='quadrimestre' if months==4 else 'trimestre',period=number,
                    calendar_days=len(sub),valid_days=n,valid_days_pct=100*n/len(sub),representative=ok))
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/out_aermod_reader.py

Identifica arquivos e combinações de grupos/períodos, usa cabeçalhos quando disponíveis e a convenção dos nomes para arquivos sem cabeçalho.

**Papel.** Aquisição/leitura. **Fonte inspecionada.** E:\projeto\codigo\out_aermod_reader.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| medias_horarias_verificadas | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- {path} — chamada .open, linha 63.
- {path} — chamada pd.read_csv, linha 93.
- {path} — chamada read_table, linha 117.
- {log} — chamada .read_text, linha 125.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- h: group, has_data, n_receptors, period.
- df: CONC, GRP, X, Y.
- d: AVE, CODE, CONC, X, Y, date, year.
- config.DIRS: post.
- coords: X, Y.
- zones: geometry, zone_index.
- original: X, Y, geometry.
- merged.loc: geometry.
- p.loc: geometry.
- strict: X, Y, zone_index.
- links: X, Y, zone_index.

**Campos e chaves gerados.**

- PLT_GROUPS: GALL.
- d: date, year.
- original: X, Y.
- links: spatial_support.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| filename_identity(path) | 52-58 | Chamadas efetivas: .stem.upper, re.search, re.match, PLT_GROUPS.get, canonical_post_group, Path, .startswith Retorno: (None, None), (PLT_GROUPS.get(match[2]), 'ANNUAL' if match[1] == 'AN00' else '24H' if match[1].startswith('24') else '1H'). |
| header(path) | 61-75 | Chamadas efetivas: .join, re.search, filename_identity, dict, .open, canonical_post_group, ValueError, lines.append Retorno: dict(group=hg or fg, period=period or fp, n_receptors=int(count[1]) if count else None, has_data=bool(line.strip()) and (not line.startswith('*'))). |
| discover(folder) | 78-88 | Chamadas efetivas: sorted, .glob, header, ignored.append, ValueError, Path, str Retorno: (selected, ignored). |
| read_table(path) | 91-100 | lê dados Retorno: df. |
| annual(path, years=(2021, 2022, 2023)) | 103-107 | lê dados Retorno: d[['X', 'Y', 'year', 'CONC']]. |
| daily(path, log=None, years=(2021, 2022, 2023)) | 110-130 | lê dados Retorno: (d[['X', 'Y', 'date', 'year', 'CONC']], sorted((str(x.date()) for x in excluded))). |
| saturation_class(value) | 133-135 | Chamadas efetivas: np.isfinite Retorno: 'Abaixo da faixa preventiva' if value <= 90 else 'Próxima do padrão' if value <= 100 else 'Acima do padrão', 'Informação insuficiente'. |
| exploratory_four_class(value) | 138-141 | Chamadas efetivas: np.isfinite Retorno: 'Baixa' if value <= 50 else 'Média' if value <= 90 else 'Alta' if value <= 100 else 'Muito alta', 'Informação insuficiente'. |
| link_receptors(coords, zones, grid) | 144-167 | Chamadas efetivas: .copy, original.geometry.x.round, original.geometry.y.round, .any, gpd.GeoDataFrame, gpd.sjoin, xy.merge, merged.geometry.notna Retorno: (links, dict(zones_strict_export=int(initial.zone_index.nunique()), zones_original_precision=int(strict.zone_index.nunique()), zones_with_boundary=int(links.zone_index.nunique()), boundary_tolerance_m. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/out_aermod_reader.py, linhas 166-167.

```python
    links['spatial_support']=['interior' if tuple(r) in keys else 'fronteira_numerica' for r in links[['X','Y','zone_index']].to_numpy()]
    return links,dict(zones_strict_export=int(initial.zone_index.nunique()),zones_original_precision=int(strict.zone_index.nunique()),zones_with_boundary=int(links.zone_index.nunique()),boundary_tolerance_m=1e-7,matched_original_points=int(resolved.sum()),max_rounding_shift_m=float(distance.max()))
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/painel_nova_modelagem.py

Painel nova modelagem. Processamento ou módulo de apoio. A organização passa por run.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\painel_nova_modelagem.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/atlas_manifest.json — chamada .read_text, linha 31.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/zoneamento_nova_modelagem.csv — chamada pd.read_csv, linha 32.

**Saídas.**

- Argumento fornecido pelo chamador — chamada .to_json, linha 34.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/index.html — chamada .write_text, linha 54.

**Campos e chaves lidos.**

- config.DIRS: out.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 29-54 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/painel_nova_modelagem.py, linhas 29-37.

```python
def run():
    out=config.DIRS['out']/'11_integracao/nova_modelagem'
    products=json.loads((out/'atlas_manifest.json').read_text(encoding='utf8'))
    rows=pd.read_csv(out/'zoneamento_nova_modelagem.csv')
    cols=['zone_index','PM10_ISZ_parcial','PM25_ISZ_parcial','PM10_grupo_principal','PM25_grupo_principal']
    data=rows[cols].where(rows[cols].notna(),None).to_json(orient='records',force_ascii=False)
    html='''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Congonhas · qualidade do ar</title>
<style>:root{--ink:#203d42;--muted:#637778;--line:#dce5e3}*{box-sizing:border-box}body{margin:0;background:#f3f6f5;color:var(--ink);font:16px system-ui}header{background:#173c43;color:white;padding:36px max(5vw,20px)}header small{letter-spacing:2px}h1{font-size:32px;margin:10px 0}main{max-width:1240px;margin:auto;padding:24px}nav{display:flex;gap:8px;flex-wrap:wrap;margin:16px 0}button,select,input{font:inherit;border:1px solid #a9bdbb;border-radius:8px;padding:10px;background:white;color:var(--ink)}button{cursor:pointer}button.active{background:var(--ink);color:white}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.card,section{background:white;padding:22px;border-radius:12px;border:1px solid var(--line);margin:12px 0}.number{font-size:34px;font-weight:650}.muted{color:var(--muted);font-size:14px}img{width:100%;display:block}a{color:#166674}.toolbar{display:flex;gap:12px;align-items:center;flex-wrap:wrap}table{width:100%;border-collapse:collapse;font-size:14px}td,th{padding:12px;text-align:left;border-bottom:1px solid var(--line)}.scroll{max-height:600px;overflow:auto}.hidden{display:none}footer{padding:28px;color:var(--muted)}@media(max-width:650px){.cards{grid-template-columns:1fr}h1{font-size:25px}}</style>
<header><small>CONGONHAS · AVALIAÇÃO TERRITORIAL</small><h1>Qualidade do ar, zona por zona</h1><p>Modelagem 2021–2023 · inventário de referência 2023 · MP10 e MP2,5</p></header>
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/paleta_concentracoes.py

Paleta contínua de concentração aprovada, independente dos cortes numéricos.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\paleta_concentracoes.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| concentration_cmap() | 26-29 | Chamadas efetivas: LinearSegmentedColormap.from_list, cmap.set_over Retorno: cmap. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/paleta_concentracoes.py, linhas 26-29.

```python
def concentration_cmap():
    cmap=LinearSegmentedColormap.from_list('concentracao_azul_vermelho',CORES_CONCENTRACAO)
    cmap.set_over('#ae1325')
    return cmap
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/perfis_concentracao_estacoes.py

Séries absolutas e sazonalidade meteorológica, com os dados já auditados.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\perfis_concentracao_estacoes.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.dates | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| medias_horarias_verificadas | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| out_aermod_reader | Módulo autoral local; sua ficha está neste relatório. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| perfis_concentracao_viewer | Módulo autoral local; sua ficha está neste relatório. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/wrf/AERMET-3Y.SFC — chamada pd.read_csv, linha 103.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/periodos_secos_meteorologicos.csv — chamada pd.read_csv, linha 153.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/dados_series/{pol}_basilica.js — chamada .read_text, linha 156.
- E:/projeto/output/16_revisao_pos_banca/figuras/index.html — chamada p.read_text, linha 170.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/distancias_grupos_estacoes.csv — chamada pd.read_csv, linha 182.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/grupos_fontes_horarias_e_estaticas.csv — chamada pd.read_csv, linha 183.
- E:/projeto/output/09_projeto_dissertacao/seminarios_02/apresentacao/apoio_meteorologia_perfis/pares_horarios_{pol}.csv — chamada pd.read_csv, linha 190.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/perfis_normalizados_grupos_estacoes.csv — chamada pd.read_csv, linha 195.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/{pol}_{group}_cache.json — chamada .read_text, linha 200.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/{pol}_{g}_estacoes.csv.gz — chamada pd.read_csv, linha 203.

**Saídas.**

- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/precipitacao_diaria_estacoes.csv — chamada wide.to_csv, linha 120.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/periodos_secos_meteorologicos.csv — chamada periods.to_csv, linha 127.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/precipitacao_referencia_diaria.csv — chamada ref.to_csv, linha 130.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/precipitacao_mensal_conferencia.csv — chamada bymonth.to_csv, linha 132.
- E:/projeto/output/16_revisao_pos_banca/figuras/PB17_perfis_grupos.{ext} — chamada fig.savefig, linha 166.
- E:/projeto/output/16_revisao_pos_banca/figuras/index.html — chamada p.write_text, linha 173.
- Argumento fornecido pelo chamador — chamada .to_json, linha 183.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/dados_series/{key}.js — chamada .write_text, linha 225.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/Concentracoes_{pol}_{sid}.{ext} — chamada fig.savefig, linha 236.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/perfis_concentracao_por_estacao_grupo.csv — chamada .to_csv, linha 239.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/comparacao_periodo_seco_grupos_estacoes.csv — chamada season_table.to_csv, linha 240.
- E:/projeto/output/16_revisao_pos_banca/perfis_grupos/sintese_seco_demais_dias_ALL.csv — chamada selected.to_csv, linha 242.
- Mais 2 referências na ficha HTML e no inventário JSON.

**Campos e chaves lidos.**

- wd: count, sum.
- config.DIRS: cache.
- daily: count, sum.
- payload: daily, groups, observed, profiles, stats.
- p: mean, p10, p90.
- periods: source.
- v: name.
- observed: station_id.
- metadata: stations.
- full_observed: CODE, station_id.
- check: observed.
- profiles.loc: group_id.
- profiles: pollutant.
- selected: 1H.
- obs_daily: count, mean.
- md: count, mean.
- paired: dry, modelled, observed.
- pr: mean, p10, p90.
- season_table: group_id.

**Campos e chaves gerados.**

- s: day, rain.
- raw: PP, day.
- ref: dry_WRF, dry_regional.
- caps: PB17_perfis_grupos.
- cal: dry.
- metadata: distances, flags.
- full_observed: CODE.
- : observed.
- data: modelled.
- p: group_id, pollutant, season, station_id.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| dry_interval(series, reference) | 91-99 | Chamadas efetivas: series.to_numpy, int, .all, ValueError, np.argmax, float, np.cumsum, np.isfinite Retorno: (start, end, float(anomaly[start] - anomaly[end])). |
| meteorology() | 102-137 | lê dados; grava produtos Retorno: (ref, periods, dict(regional_source=identity(path), SFC=identity(sfc), rain_stations=wide.columns.tolist(), method='Maior queda da anomalia acumulada diária em cada ano, relativa à média diária 2021-2. |
| numeric(values) | 140-141 | Chamadas efetivas: round, np.isfinite, float Retorno: [None if not np.isfinite(v) else round(float(v), 4) for v in values]. |
| clean_json(value) | 144-148 | Chamadas efetivas: isinstance, clean_json, np.isfinite, value.items Retorno: value, {k: clean_json(v) for k, v in value.items()}. |
| summary_figure() | 151-173 | lê dados; grava produtos |
| run() | 176-249 | lê dados; grava produtos; Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/perfis_concentracao_estacoes.py, linhas 215-221.

```python
                for season,sub in [('Total',paired),('Período seco',paired[paired.dry]),('Demais dias',paired[~paired.dry])]:
                    prof=sub.groupby('hour')[['observed','modelled']].mean().reindex(range(24));low=sub.groupby('hour')[['observed','modelled']].quantile(.1).reindex(range(24));high=sub.groupby('hour')[['observed','modelled']].quantile(.9).reindex(range(24));maximum=sub.groupby('hour')[['observed','modelled']].max().reindex(range(24))
                    payload['profiles'][group][season]={}
                    for variable in ['observed','modelled']:
                        payload['profiles'][group][season][variable]={'mean':numeric(prof[variable]),'p10':numeric(low[variable]),'p90':numeric(high[variable]),'max':numeric(maximum[variable])}
                    p=prof.reset_index();p['pollutant']=pol;p['station_id']=sid;p['group_id']=group;p['season']=season;allprofiles.append(p)
                    seasons.append(dict(pollutant=pol,station_id=sid,group_id=group,season=season,n_pairs=len(sub),observed_mean=sub.observed.mean(),modelled_mean=sub.modelled.mean(),observed_max=sub.observed.max(),modelled_max=sub.modelled.max(),hourly_r=sub.observed.corr(sub.modelled)))
```

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- quantile: Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/perfis_concentracao_viewer.py

Interface offline com valores absolutos e carregamento por estação.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\perfis_concentracao_viewer.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

- {out}/index.html — chamada .write_text, linha 102.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| write_viewer(out, metadata) | 24-102 | grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/perfis_concentracao_viewer.py, linhas 24-32.

```python
def write_viewer(out,metadata):
    template=r'''<!doctype html><html lang="pt-BR"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Concentrações nas estações</title>
<style>
body{font:16px/1.55 Arial,sans-serif;max-width:1250px;margin:30px auto;padding:0 22px;color:#183d4c;background:#fff}
h1{font-size:29px}h2{font-size:21px;margin-top:35px}p{max-width:1080px}
.controls{display:flex;gap:16px;flex-wrap:wrap;align-items:end;padding:16px 0;border-top:1px solid #d8e0e1;border-bottom:1px solid #d8e0e1}
label{display:flex;flex-direction:column;font-size:14px;color:#375563}select,input{font:16px Arial;padding:8px;max-width:360px;border:1px solid #abbfc7;border-radius:4px;background:#fff}
.check{display:inline-flex;flex-direction:row;align-items:center;gap:8px}.check input{width:auto}
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/populacao_urbana_zoneamento.py

Populacao urbana zoneamento. Processamento ou módulo de apoio. A organização passa por normalize_text, main.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\populacao_urbana_zoneamento.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| rasterio | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| rasterio.features | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shapely.ops | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/06_censo_ibge/censo_setores_congonhas.gpkg — chamada gpd.read_file, linha 64.
- E:/projeto/output/03_zoneamento/zoneamento_congonhas.gpkg — chamada gpd.read_file, linha 65.
- E:/projeto/output/PM10/PV/zoneamento_PM10_PV_atendimento_combinado.gpkg — chamada gpd.read_file, linha 66.
- E:/projeto/uso_terra/mapbiomas-brazil-collection-101-congonhas-2024.tif — chamada rasterio.open, linha 79.

**Saídas.**

- E:/projeto/output/06_censo_ibge/censo_alocacao_urbana_zoneamento_detalhe.csv — chamada allocation.to_csv, linha 176.
- E:/projeto/output/06_censo_ibge/censo_alocacao_urbana_zoneamento_auditoria.csv — chamada audit_df.to_csv, linha 177.
- E:/projeto/output/06_censo_ibge/censo_populacao_urbana_por_zoneamento.csv — chamada zone_population.to_csv, linha 178.
- E:/projeto/output/06_censo_ibge/censo_populacao_validada_por_zoneamento.csv — chamada zone_population.to_csv, linha 179.
- E:/projeto/output/06_censo_ibge/censo_populacao_urbana_por_status_PM10_PV.csv — chamada summary.to_csv, linha 180.
- E:/projeto/output/06_censo_ibge/zoneamento_populacao_validada.gpkg [camada 'populacao_validada'] — chamada population_gdf.to_file, linha 188.
- E:/projeto/output/PM10/zoneamento_PM10_integrado_populacao.gpkg [camada 'zoneamento_PM10_integrado'] — chamada integrated.to_file, linha 191.

**Campos e chaves lidos.**

- sectors: DOM_PART_OCUP, POP_TOTAL, SITUACAO.
- zones: sigla_macr.
- zone_population: area_elegivel_m2, pop_confianca, pop_estimada, pop_evidencia, pop_urbana_estimada, sigla_macr.
- pm10: PM10_PV_status, zone_index.
- summary: pop_urbana_estimada.
- populated.loc: POP_TOTAL.
- populated: situacao_norm.

**Campos e chaves gerados.**

- sectors: DOM_PART_OCUP, POP_TOTAL, situacao_norm.
- zones: zone_index.
- zone_population: elegivel_indicador_urbano, pop_ano_censo, pop_ano_uso_solo, pop_confianca, pop_dens_hab_km2, pop_evidencia, pop_metodo, pop_presenca.
- summary: percentual_pop_urbana.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| normalize_text(series: pd.Series) | 59-60 | Chamadas efetivas: .str.casefold, .str.strip, .astype, series.fillna Retorno: series.fillna('').astype(str).str.strip().str.casefold(). |
| main() | 63-197 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/populacao_urbana_zoneamento.py, linhas 114-120.

```python
                intersections.append((zone.zone_index, geom.area))
        eligible_area = sum(area for _, area in intersections)
        allocated = 0.0
        for zone_index, area in intersections:
            weight = area / eligible_area if eligible_area > 0 else 0.0
            population = sector.POP_TOTAL * weight
            allocated += population
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/populacao_urbana_zoneamento.py, linhas 153-159.

```python
    numeric_cols = ["pop_estimada", "pop_urbana_estimada", "pop_rural_confirmada", "area_elegivel_m2"]
    zone_population = allocation.groupby("zone_index", as_index=False)[numeric_cols].sum() if not allocation.empty else pd.DataFrame(columns=["zone_index", *numeric_cols])
    evidence_by_zone = allocation.groupby("zone_index")["pop_evidencia"].agg(lambda x: ";".join(sorted(set(x)))).reset_index()
    confidence_rank = {"baixa": 1, "media": 2, "alta": 3}
    confidence_by_zone = allocation.groupby("zone_index")["pop_confianca"].agg(lambda x: max(x, key=lambda v: confidence_rank[v])).reset_index()
    zone_population = zone_population.merge(evidence_by_zone, on="zone_index", how="left").merge(confidence_by_zone, on="zone_index", how="left")
    zone_population = zones.drop(columns="geometry").merge(zone_population, on="zone_index", how="left")
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/post_amostragem.py

Lê de forma eficiente os arquivos POST e amostra as concentrações pelo código temporal e coordenadas, preservando o vínculo entre receptor, hora/dia e grupo.

**Papel.** Aquisição/leitura. **Fonte inspecionada.** E:\projeto\codigo\post_amostragem.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| out_aermod_reader | Módulo autoral local; sua ficha está neste relatório. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- self.path — chamada self.path.open, linha 90.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- self.info: n_receptors, period.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| FixedPost() | 28-104 | Chamadas efetivas: Path, header, divmod, np.array, np.memmap, int, pd.date_range, .to_numpy Retorno: result, values. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/post_amostragem.py, linhas 29-37.

```python
    def __init__(self,path):
        self.path=Path(path)
        self.info=header(self.path)
        self.nr=self.info['n_receptors']
        if not self.nr:
            raise ValueError('Cabeçalho sem número de receptores')
        with self.path.open('rb') as f:
            self.offset=0
            for line in f:
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/preparar_adi_revisado_auditoria.py

ADI de MP2,5 com taxas dos memoriais, preservando a modelagem original.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\preparar_adi_revisado_auditoria.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/adi_ado_sum/PM25.ADI — chamada source.read_text, linha 59.
- E:/projeto/output/14_auditoria_entradas/revisao_Vale_Fabrica_20261025/alteracoes_taxas.json — chamada .read_text, linha 61.
- E:/projeto/adi_ado_sum/PM25.ADI — chamada source.read_bytes, linha 80.
- E:/projeto/output/15_auditoria_metodologica/PM25_Entrada_Revisada.ADI — chamada dest.read_bytes, linha 80.

**Saídas.**

- E:/projeto/output/15_auditoria_metodologica/PM25_Entrada_Revisada.ADI — chamada dest.write_bytes, linha 78.
- E:/projeto/output/15_auditoria_metodologica/Correcao_ADI_PM25.csv — chamada .to_csv, linha 79.
- E:/projeto/output/15_auditoria_metodologica/ADI_PM25_revisao.json — chamada .write_text, linha 81.

**Campos e chaves lidos.**

- x: pol.
- entry: id, source, total_g_s.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| parse(lines) | 34-54 | Chamadas efetivas: enumerate, loc.items, re.search, line.split, list, np.asarray, map, .extend Retorno: (loc, params, parents, positions, area). |
| run() | 57-83 | lê dados; grava produtos Retorno: report. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/preparar_adi_revisado_auditoria.py, linhas 50-56.

```python
        elif typ=='AREAPOLY':
            xy=np.asarray(vertices[sid]);xy-=xy[0];area[sid]=abs(np.sum(xy[:,0]*np.roll(xy[:,1],-1)-np.roll(xy[:,0],-1)*xy[:,1]))/2
        elif typ=='AREACIRC':area[sid]=math.pi*p[2]**2
        else:area[sid]=1.
    return loc,params,parents,positions,area

# Run
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/preparar_adi_revisado_auditoria.py, linhas 65-71.

```python
        assert children
        before=sum(params[c][0]*area[c] for c in children);desired=float(entry['total_g_s'])
        for child in children:
            old=params[child][0]
            new=old*desired/before if before>0 else desired/sum(area[c] for c in children)
            if not np.isclose(new,old,rtol=1e-12,atol=1e-15):
                i=positions[child];p=lines[i].split();qpos=3 if p[0]=='SO' else 2
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/preparar_analises_extensiveis.py

Preparar analises extensiveis. Processamento ou módulo de apoio. A organização passa por extrair, main.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\preparar_analises_extensiveis.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| ast | Inspeção/transformação da sintaxe Python sem executar o processamento científico. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- {path} — chamada path.read_text, linha 30.

**Saídas.**

- {root}/config/analise_extensivel.json — chamada .write_text, linha 178.
- {root}/codigo/reproduzir_analise_configuravel.py — chamada .write_text, linha 180.

**Campos e chaves lidos.**

- v: nome.
- cfg: semente.

**Campos e chaves gerados.**

- cfg: como_ampliar.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| extrair(path, names) | 29-31 | lê dados Retorno: '\n\n'.join((ast.get_source_segment(text, n) for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names)). |
| main() | 168-180 | grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/preparar_analises_extensiveis.py, linhas 29-37.

```python
def extrair(path,names):
    text=path.read_text('utf-8-sig');tree=ast.parse(text)
    return '\n\n'.join(ast.get_source_segment(text,n) for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names)

CORE=r'''from pathlib import Path
import argparse
import hashlib
import importlib.metadata
import json
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/preparar_bpip_importacao.py

Preparar bpip importacao. Processamento ou módulo de apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\preparar_bpip_importacao.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| collections | Estruturas de contagem, agrupamento e coleções auxiliares. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- externos.pm10_bpi_6bd03da — chamada source.read_bytes, linha 32.
- E:/projeto/output/14_auditoria_entradas/correcao_BPIP_FUNIT/PM10_validado.bpi — chamada target.read_bytes, linha 32.
- E:/projeto/output/14_auditoria_entradas/correcao_BPIP_FUNIT/PM10_BPIP_EPA.pro — chamada .read_text, linha 33.
- E:/projeto/output/14_auditoria_entradas/correcao_BPIP_FUNIT/BPIP_parametros_separados.INP — chamada .read_text, linha 55.

**Saídas.**

- E:/projeto/output/14_auditoria_entradas/correcao_BPIP_FUNIT/PM10_BPIP_importacao.pro — chamada normalized.write_bytes, linha 47.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/preparar_bpip_importacao.py, linhas 31-39.

```python
shutil.copy2(source, target)
assert source.read_bytes() == target.read_bytes()
lines = (out / 'PM10_BPIP_EPA.pro').read_text(encoding='cp1252').splitlines()
counts = defaultdict(int)
result = []
for line in lines:
    m = re.match(r'^\s*SO\s+(BUILDHGT|BUILDWID|BUILDLEN|XBADJ|YBADJ)\s+(.{8})(.*)$', line)
    if m:
        kw, sid, tail = m.groups()
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/preparar_continuidade_pos_banca.py

Grade candidata e cenários temporais de ensaio; não modifica ADI/EMI correntes.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\preparar_continuidade_pos_banca.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| aermod_sources | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| standards | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/16_revisao_pos_banca/zoneamento_pos_banca.gpkg — chamada gpd.read_file, linha 57.
- E:/projeto/output/11_integracao/nova_modelagem/PM25_indicadores_trienais_receptores.csv — chamada pd.read_csv, linha 58.
- E:/projeto/output/11_integracao/nova_modelagem/estacoes_rede_atual.gpkg — chamada gpd.read_file, linha 70.
- E:/projeto/adi_ado_sum/{adi} — chamada source_path.read_text, linha 93.

**Saídas.**

- E:/projeto/output/16_revisao_pos_banca/preparacao_modelagem/Vinculo_grade_candidata_311_zonas.csv — chamada .to_csv, linha 80.
- E:/projeto/output/16_revisao_pos_banca/preparacao_modelagem/Grade_candidata_AERMOD.csv — chamada d.to_csv, linha 81.
- E:/projeto/output/16_revisao_pos_banca/preparacao_modelagem/Grade_candidata_AERMAP.INP — chamada .write_text, linha 83.
- E:/projeto/output/16_revisao_pos_banca/preparacao_modelagem/Perfis_horarios_sensibilidade.csv — chamada .to_csv, linha 90.
- E:/projeto/output/16_revisao_pos_banca/preparacao_modelagem/{pol}_{name}_EMISFACT.INC — chamada .write_text, linha 120.
- E:/projeto/output/16_revisao_pos_banca/preparacao_modelagem/{pol}_{name}_SENSIBILIDADE.ADI — chamada .write_text, linha 124.
- E:/projeto/output/16_revisao_pos_banca/preparacao_modelagem/Fontes_candidatas_perfil.csv — chamada .to_csv, linha 126.
- E:/projeto/output/16_revisao_pos_banca/preparacao_modelagem/manifesto_continuidade.json — chamada .write_text, linha 127.
- E:/projeto/output/16_revisao_pos_banca/preparacao_modelagem/LEIA_ME.md — chamada .write_text, linha 128.
- E:/projeto/output/16_revisao_pos_banca/saude_cenarios_preparados.csv — chamada .to_csv, linha 147.

**Campos e chaves lidos.**

- all_candidates: X, Y, zone_index.
- d: X, Y, receptor_id.
- zone_links.loc: inside_zone_after_rounding.
- zone_links: X, Y, geometry_fragment, inside_zone_after_rounding, origin, receptor_id, zone_index.
- roads.loc: Desc.
- STANDARDS: PM25.

**Campos e chaves gerados.**

- zone_links: geometry_fragment, inside_zone_after_rounding.
- summary: temporal_scenarios.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 55-148 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/preparar_continuidade_pos_banca.py, linhas 145-150.

```python
   target=STANDARDS['PM25'][stage]['ANNUAL'];delta=max(c-target,0) if np.isfinite(c) else np.nan
   health.append({'zone_index':r.zone_index,'stage':stage,'annual_target_ug_m3':target,'observed_annual_mean':c,'reduction_ug_m3':delta,'fraction_RR108_pct':100*(-np.expm1(-np.log(1.08)/10*delta)) if np.isfinite(delta) else np.nan,'status':'Sensibilidade com RR=1,08 herdado; conferir fonte original e elegibilidade antes de publicação sanitária','baseline_events':np.nan})
 pd.DataFrame(health).to_csv(ROOT/'saude_cenarios_preparados.csv',index=False)
 print(json.dumps(summary,ensure_ascii=False),flush=True)

if __name__=='__main__':run()
```

Logaritmo natural. Na função de risco, β=ln(RR)/10 converte um risco relativo por 10 µg/m³ para a escala de 1 µg/m³.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- log: Logaritmo natural. Na função de risco, β=ln(RR)/10 converte um risco relativo por 10 µg/m³ para a escala de 1 µg/m³.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/preparar_correcao_ids7.py

Preparar correcao ids7. Consolidação/migração: conferir pré-condições. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Consolidação/migração: conferir pré-condições. **Fonte inspecionada.** E:\projeto\codigo\preparar_correcao_ids7.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/14_auditoria_entradas/entrada_BPIP_7caracteres/auditoria_base.json — chamada .read_text, linha 29.
- E:\projeto/output/14_auditoria_entradas/testes_BPIP_GERDAU/dados_testes.json — chamada .read_text, linha 30.
- E:\projeto/output/14_auditoria_entradas/correcao_BPIP_FUNIT/PM10_validado.bpi — chamada bpi.read_text, linha 52.

**Saídas.**

- E:/projeto/output/14_auditoria_entradas/entrada_BPIP_7caracteres/alteracoes.json — chamada .write_text, linha 48.
- E:/projeto/output/14_auditoria_entradas/entrada_BPIP_7caracteres/PM10_IDS7.bpi — chamada .write_bytes, linha 63.

**Campos e chaves lidos.**

- t: maps.
- a: files, hour, loc, par, points.
- f: name, points, src.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/preparar_correcao_ids7.py, linhas 28-36.

```python
out=Path(_cp_texto('output/14_auditoria_entradas/entrada_BPIP_7caracteres', 'posix'))
a=json.loads((out/'auditoria_base.json').read_text(encoding='utf8'))
t=json.loads(Path(_cp_texto('output/14_auditoria_entradas/testes_BPIP_GERDAU/dados_testes.json', 'posix')).read_text(encoding='utf8'))
heights={x[2]:x[4] for x in t['maps'] if x[0]=='T02_IDs_atuais'}
ids=sorted({p[2] for f in a['files'] for p in f['points']})
mapping={sid:re.sub(r'^FDI','FD',re.sub(r'^FPO','FP',sid)) for sid in ids}
assert len(set(mapping.values()))==len(mapping) and max(map(len,mapping.values()))<=7
assert not (set(mapping.values()) & (set(a['loc'])-set(ids)))
assert not (set(ids)&set(a['hour']))
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. Rotina histórica: conferir pré-condições e versão de dados antes de qualquer execução.

## codigo/preparar_testes_fontes_bpip.py

Preparar testes fontes bpip. Processamento ou módulo de apoio. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\preparar_testes_fontes_bpip.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| openpyxl | Leitura/escrita de planilhas XLSX; não é o mecanismo do Excel aberto. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- externos.downloads_f68ae09/EXP_PTS.ADI — chamada .read_text, linha 33.
- externos.downloads_f68ae09/EXP_PTS.bpi — chamada .read_text, linha 39.
- E:\projeto/output/14_auditoria_entradas/correcao_BPIP_FUNIT/comparacao_GERDAU.json — chamada .read_text, linha 42.

**Saídas.**

- E:/projeto/output/14_auditoria_entradas/testes_BPIP_GERDAU/dados_testes.json — chamada .write_text, linha 67.

**Campos e chaves lidos.**

- x: atual, original.
- payload: total_pts_g_s.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/preparar_testes_fontes_bpip.py, linhas 65-69.

```python
    cases.append(dict(name=name,note=note,rows=data))
payload=dict(meta=meta,cases=cases,maps=maps,total_pts_g_s=sum(r[16] for r in rows),source=str(d/'EXP_PTS.ADI'))
(out/'dados_testes.json').write_text(json.dumps(payload,ensure_ascii=False),encoding='utf8')
print('53 fontes POINT; seis cenários; emissão PTS total preservada:',payload['total_pts_g_s'])
print('Alturas flare:',[(r[1],r[5]) for r in rows if r[1].startswith('FLARE')])
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/preservar_vetores_docx.py

SVG nativo do Office com PNG de compatibilidade: texto e traços vetoriais no PDF.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\preservar_vetores_docx.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| docx | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.opc.constants | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.opc.packuri | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.opc.part | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.oxml | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.oxml.ns | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| lxml | Consulta/edição XML, incluindo os componentes internos de DOCX, PPTX e SVG. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/11_integracao/nova_modelagem/figuras_seminario_manifesto.json — chamada .read_text, linha 42.
- sources[code] — chamada source.read_bytes, linha 67.

**Saídas.**

- E:/projeto/output/09_projeto_dissertacao/seminarios_02/Projeto_Ricardo-Queiroz_{version}.docx — chamada doc.save, linha 74.
- E:/projeto/temp/qa_seminarios/vetores_docx.json — chamada .write_text, linha 75.

**Campos e chaves lidos.**

- x: arquivo, codigo.

**Campos e chaves gerados.**

- sources: A1.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 41-76 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/preservar_vetores_docx.py, linhas 41-49.

```python
def run():
    manifest=json.loads((OUT/'figuras_seminario_manifesto.json').read_text(encoding='utf8'))
    sources={x['codigo']:Path(x['arquivo']).with_suffix('.svg') for x in manifest if x['arquivo']!='ORIGINAL'}
    flow=FOLDER/'figuras/Fluxograma_metodologia.svg'
    if flow.exists():sources['A1']=flow
    audit={}
    for version in ['Entrega','Leitura']:
        path=FOLDER/f'Projeto_Ricardo-Queiroz_{version}.docx';doc=Document(path);ps=list(doc.paragraphs);changed=[]
        for i,p in enumerate(ps):
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/propagar_diarias_horarias.py

Propaga médias horárias verificadas e exige estabilidade das classes.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\propagar_diarias_horarias.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| methodology_rules | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| out_aermod_reader | Módulo autoral local; sua ficha está neste relatório. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| standards | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- {p} — chamada gpd.read_file, linha 49.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_receptores_anuais.csv — chamada pd.read_csv, linha 52.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_vinculo_receptor_zona.csv — chamada pd.read_csv, linha 63.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{name} — chamada pd.read_csv, linha 80.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/auditoria_medias_horarias.json — chamada .read_text, linha 85.

**Saídas.**

- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_receptores_anuais.csv — chamada .to_csv, linha 62.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_indicadores_trienais_receptores.csv — chamada period.to_csv, linha 62.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{name} — chamada table.to_csv, linha 81.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{name} — chamada z.to_file, linha 83.
- p.with_suffix('.csv') — chamada .to_csv, linha 83.
- E:/projeto/config.DIRS['out']/15_auditoria_metodologica/propagacao_diarias_1h.json — chamada p.write_text, linha 84.
- E:/projeto/config.DIRS['out']/15_auditoria_metodologica/Conferencia_POST_1h_24h.md — chamada .write_text, linha 89.

**Campos e chaves lidos.**

- config.DIRS: aermod_logs, out, post.
- selected: 24H, ALL.
- lim: 24H, ANNUAL.
- table: pollutant.
- table.loc: zone_index.
- v: max_annual_difference, max_daily_difference.

**Campos e chaves gerados.**

- new: ANNUAL_DAILY_MEAN, MAX24, peak_date.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 47-91 | lê dados; grava produtos Retorno: report. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/propagar_diarias_horarias.py, linhas 63-69.

```python
  links=pd.read_csv(OUT/f'{pol}_vinculo_receptor_zona.csv');linked=period.merge(links,on=['X','Y'],validate='one_to_many')
  means=linked.groupby('zone_index')[['ANNUAL_MODEL','P98_MODEL']].mean();maxima=linked.groupby('zone_index')[['ANNUAL_MODEL','P98_MODEL']].max()
  for p,z in zones.items():
   for scenario in ['PV','PF']:
    lim=STANDARDS[pol][scenario]
    oldclass=z[f'{pol}_model_annual_trienal'].gt(lim['ANNUAL'])|z[f'{pol}_model_p98_trienal'].gt(lim['24H'])
    newclass=means.ANNUAL_MODEL.gt(lim['ANNUAL'])|means.P98_MODEL.gt(lim['24H'])
```

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/publicar_rateio_refinado.py

Publica somente atributos de emissão, sem recalcular concentrações.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\publicar_rateio_refinado.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| alocacao_territorial_emissoes | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| vector_portable | Módulo autoral local; sua ficha está neste relatório. |


**Entradas.**

- E:/projeto/config.DIRS['out']/13_rateio_emissoes/Resumo_zonas.csv — chamada pd.read_csv, linha 43.
- E:/projeto/config.DIRS['out']/13_rateio_emissoes/Empreendimentos.csv — chamada pd.read_csv, linha 44.

**Saídas.**

- E:/projeto/config.DIRS['out']/11_integracao/zoneamento_integrado.csv — chamada .to_csv, linha 62.
- E:/projeto/config.DIRS['out']/13_rateio_emissoes/Comparacao_classes.csv — chamada .to_csv, linha 63.
- E:/projeto/config.DIRS['out']/13_rateio_emissoes/publicacao_refinada.json — chamada .write_text, linha 65.

**Campos e chaves lidos.**

- config.DIRS: out.
- summary: poluente.
- groups: poluente.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 35-66 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/publicar_rateio_refinado.py, linhas 35-43.

```python
def run():
    out=config.DIRS['out'];base=out/'11_integracao'
    backup=config.BASE/'temp/backup_refinamento_20261022/integracao';backup.mkdir(parents=True,exist_ok=True)
    for path in base.glob('zoneamento_integrado.*'):
        if not (backup/path.name).exists():shutil.copy2(path,backup/path.name)
    z=read(base/'zoneamento_integrado.gpkg').set_index('zone_index',drop=False)
    previous=read(backup/'zoneamento_integrado.gpkg').set_index('zone_index',drop=False)
    z=apply_territorial_totals(z)
    summary=pd.read_csv(out/'13_rateio_emissoes/Resumo_zonas.csv')
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/receptor_grid.py

Receptor grid. Processamento ou módulo de apoio. A organização passa por _union_all, _iter_polygons, _iter_lines, _make_valid_polygonal, _largest_polygon, _interior_geocenter, _point_in_footprint, _choose_column, _normalize_zones, _normalize_population_sectors.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\receptor_grid.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| __future__ | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| io_utils | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| matplotlib.lines | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| rasterio | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| rasterio.features | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| rasterio.mask | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| scipy.spatial | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| shapely | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shapely.ops | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| xml.etree.ElementTree | Leitura/edição de XML de projetos e documentos. |


**Entradas.**

- getattr(config, 'FILES', {}).get('landuse_2024', '') — chamada rasterio.open, linha 321.
- getattr(config, 'FILES', {}).get('station_coords', '') — chamada pd.read_excel, linha 480.

**Saídas.**

- getattr(config, 'FILES', {}).get('station_coords', '') — chamada path.write_text, linha 1128.
- {out_png} — chamada fig.savefig, linha 1170.
- {out_dir}/grade_receptores_adaptativa.csv — chamada tab.to_csv, linha 1193.
- {out_dir}/grade_receptores_adaptativa_excel_ptbr.csv — chamada tab.to_csv, linha 1194.
- {out_dir}/grade_diagnostico_por_setor.csv — chamada diagnostics.to_csv, linha 1195.
- {out_dir}/grade_resumo_contagem.csv — chamada summary.to_csv, linha 1202.
- {writer} — chamada tab.to_excel, linha 1204.
- {writer} — chamada diagnostics.to_excel, linha 1205.
- {writer} — chamada summary.to_excel, linha 1206.
- {out_dir}/grade_receptores_adaptativa.gpkg [camada 'receptores'] — chamada receptors.to_file, linha 1214.
- {out_dir}/grade_receptores_adaptativa.gpkg [camada 'limite_congonhas'] — chamada .to_file, linha 1218.
- {out_dir}/grade_receptores_adaptativa.gpkg [camada 'faixas_buffer'] — chamada rings.to_file, linha 1221.
- Mais 2 referências na ficha HTML e no inventário JSON.

**Campos e chaves lidos.**

- z: _grid_zone_id, _grid_zone_name.
- z.loc: _grid_zone_id.
- p: geometry, population.
- part: geometry.
- m: geometry, population.
- zr: _grid_zone_id, _grid_zone_name.
- coords: x_raw, y_raw.
- raw: geometry.
- rec: geometry.
- r: geometry, kind.
- zones: _grid_area_km2, _grid_zone_id, _grid_zone_name, geometry.
- row: geometry.
- receptors: kind.
- sectors_norm: _grid_population.
- diagnostics: coverage_tolerance_m2, representative_ok, uncovered_area_m2.
- failures: zone_id.

**Campos e chaves gerados.**

- z: _grid_area_km2, _grid_geometry_source, _grid_zone_id, _grid_zone_name, geometry.
- s: _grid_population, _grid_sector_area_m2, geometry.
- coords: utm_x, utm_y.
- old: community_id, roles, spacing_m, station_id, zone_ids.
- row: ZELEV, ZFLAG, ZHILL, receptor_id, utm_x, utm_y.
- tab: latitude, longitude.
- source_paths: uso_solo_preferencia_grade.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| GridGenerationError() | 86-87 | Organiza parâmetros, expressões ou retorno sem chamada externa. |
| _union_all(values) | 104-108 | Chamadas efetivas: list, unary_union, GeometryCollection Retorno: unary_union(values), GeometryCollection(). |
| _iter_polygons(geom) | 111-123 | Chamadas efetivas: isinstance, out.extend, _iter_polygons Retorno: [], []. |
| _iter_lines(geom) | 126-138 | Chamadas efetivas: isinstance, out.extend, _iter_lines Retorno: [], []. |
| _make_valid_polygonal(geom) | 141-155 | Chamadas efetivas: _iter_polygons, GeometryCollection, _union_all, make_valid, geom.buffer Retorno: _union_all(parts) if parts else GeometryCollection(), GeometryCollection(). |
| _largest_polygon(geom) | 158-160 | Chamadas efetivas: _iter_polygons, max Retorno: max(parts, key=lambda g: g.area) if parts else None. |
| _interior_geocenter(geom) | 163-177 | Chamadas efetivas: _make_valid_polygonal, geom.covers, _largest_polygon, geom.representative_point, polylabel, largest.representative_point Retorno: geom.representative_point(), None. |
| _point_in_footprint(point, footprint) | 180-188 | Chamadas efetivas: footprint.covers, nearest_points, footprint.representative_point Retorno: point, point. |
| _choose_column(columns, candidates) | 191-196 | Chamadas efetivas: .casefold, candidate.casefold, .strip, str Retorno: None, lower[candidate.casefold()]. |
| _normalize_zones(zones, municipality) | 199-246 | Chamadas efetivas: .reset_index, _make_valid_polygonal, z.geometry.map, invalid_original.any, z.geometry.copy, original_geometry.map, clipped_geometry.map, clip_fallback.any Retorno: (z, mun_geom). |
| _normalize_population_sectors(sectors, mun_geom) | 249-266 | Chamadas efetivas: .reset_index, _choose_column, pd.to_numeric, s.geometry.map, .copy, _make_valid_polygonal, s.intersects, g.intersection Retorno: (s, pop_col), (None, None). |
| _community_components(parts, link_distance_m) | 269-293 | Chamadas efetivas: _iter_polygons, set, sorted, enumerate, max, _union_all, float, cluster.intersects Retorno: out, []. |
| _weighted_community_point(members, footprint) | 296-305 | Chamadas efetivas: np.array, _point_in_footprint, float, Point, max, weights.sum, np.average, m.get Retorno: _point_in_footprint(point, footprint). |
| _load_landuse_preference_footprint(mun_geom) | 308-353 | Chamadas efetivas: Path, bool, .get, int, getattr, GeometryCollection, path.exists, rasterio.open Retorno: (GeometryCollection(), {'status': 'disabled'}), (GeometryCollection(), {'status': 'missing', 'path': str(path), 'classes': classes}). |
| _population_anchor_records(zones, sectors, mun_geom, landuse_footprint=None) | 356-470 | Chamadas efetivas: float, zones.iterrows, getattr, str, gpd.GeoDataFrame, candidates.iterrows, bool, _community_components Retorno: (records, fp, zone_population). |
| _station_records(zones, mun_geom) | 473-538 | lê dados Retorno: records, []. |
| _sample_line(line, spacing) | 541-553 | Chamadas efetivas: float, max, bool, int, math.ceil, line.interpolate, range Retorno: ([line.interpolate(d) for d in distances], actual), ([], 0.0). |
| _boundary_records(zones, mun_geom) | 556-621 | Chamadas efetivas: float, max, boundaries.append, _union_all, _iter_lines, unique.values, bool, getattr Retorno: (records, network, max_actual_spacing), ([], GeometryCollection(), 0.0). |
| _split_zone_ids(value) | 624-625 | Chamadas efetivas: .split, str Retorno: {x for x in str(value or '').split(' / ') if x}. |
| _merge_text_tokens(a, b) | 628-630 | Chamadas efetivas: .join, sorted, .split, str Retorno: ' / '.join(sorted(vals)). |
| _deduplicate_records(records, tolerance_m=None) | 633-655 | Chamadas efetivas: max, list, float, dict, _merge_text_tokens, buckets.values, int, old.get Retorno: list(buckets.values()). |
| _coverage_uncovered(zone_geom, points, radius) | 658-665 | Chamadas efetivas: _union_all, _make_valid_polygonal, p.buffer, zone_geom.difference, .difference, covered.buffer, zone_geom.buffer Retorno: zone_geom, _make_valid_polygonal(zone_geom.difference(covered)). |
| _add_internal_coverage(zones, records) | 668-740 | Chamadas efetivas: float, zones.iterrows, list, getattr, str, _coverage_uncovered, max, reversed Retorno: combined. |
| _has_zone_role(record, zone_id) | 743-744 | Chamadas efetivas: _split_zone_ids, record.get Retorno: zone_id in _split_zone_ids(record.get('zone_ids')). |
| _is_representative_kind(kind) | 747-749 | Chamadas efetivas: str, kind.startswith Retorno: kind == 'COMUNIDADE' or kind.startswith('GEOCENTRO'). |
| _distance_to_any(point, others) | 752-755 | Chamadas efetivas: min, float, point.distance Retorno: min((float(point.distance(other)) for other in others)), np.inf. |
| _spacing_ok(point, others, min_spacing) | 758-759 | Chamadas efetivas: _distance_to_any, float Retorno: _distance_to_any(point, others) >= float(min_spacing) - 1e-06. |
| _lattice_points_from_anchor(zone_geom, anchor, spacing) | 762-780 | Chamadas efetivas: max, range, out.sort, float, int, math.floor, math.ceil, Point Retorno: out. |
| _fallback_points_for_gap(gap_geom, spacing) | 783-792 | Chamadas efetivas: sorted, _iter_polygons, _coverage_tolerance_m2, points.append, max, polylabel, int, part.representative_point Retorno: points[:max(1, int(math.ceil(gap_geom.area / max(1.0, spacing * spacing))))]. |
| _gap_fill_candidate(gap_geom, fixed_points, min_spacing, sample_step) | 795-814 | Chamadas efetivas: _largest_polygon, _spacing_ok, max, _sample_geometry, polylabel, float, points.sort, largest.representative_point Retorno: (preferred, True), (None, False). |
| _select_zone_anchor(zone_records, zone_geom) | 817-830 | Chamadas efetivas: _interior_geocenter, representatives.sort, _is_representative_kind, r.get, KIND_PRIORITY.get, str, pd.notna, float Retorno: _interior_geocenter(zone_geom), representatives[0]['geometry']. |
| _add_internal_lattice_coverage(zones, records) | 833-908 | Chamadas efetivas: float, zones.iterrows, _deduplicate_records, getattr, str, _select_zone_anchor, _lattice_points_from_anchor, _coverage_uncovered Retorno: _deduplicate_records(records + additions). |
| _external_grid_records(mun_geom) | 911-962 | Chamadas efetivas: float, _make_valid_polygonal, mun_geom.buffer, lattice, records.extend, gpd.GeoDataFrame, getattr, GridGenerationError Retorno: (records, rings), rows. |
| _sample_geometry(geom, step) | 965-986 | Chamadas efetivas: max, _iter_lines, np.asarray, float, math.floor, _sample_line, coords.extend, geom.representative_point Retorno: np.asarray(coords, dtype=float). |
| _coverage_tolerance_m2(zone_geom) | 989-993 | Chamadas efetivas: float, max, getattr Retorno: max(absolute, relative). |
| _zone_diagnostics(zones, records, zone_population, boundary_max_spacing) | 996-1064 | Chamadas efetivas: float, zones.iterrows, pd.DataFrame, getattr, str, _coverage_uncovered, _coverage_tolerance_m2, _sample_geometry Retorno: pd.DataFrame(rows). |
| _records_to_gdf(records) | 1067-1090 | Chamadas efetivas: _deduplicate_records, records.sort, enumerate, gpd.GeoDataFrame, dict, row.setdefault, float, rows.append Retorno: gpd.GeoDataFrame(rows, geometry='geometry', crs=config.CRS_PROJECT). |
| _write_kml(receptors, path) | 1093-1107 | Chamadas efetivas: receptors.to_crs, ET.Element, ET.SubElement, geographic.itertuples, path.parent.mkdir, .write, str, ET.ElementTree |
| _write_rec(receptors, path) | 1110-1128 | grava produtos |
| _plot_grid(zones, mun_geom, rings, communities, receptors, out_png) | 1131-1171 | grava produtos |
| _export_outputs(receptors, zones, municipality, communities, rings, diagnostics, out_dir, operational_dir, source_paths=None) | 1174-1285 | grava produtos Retorno: manifest. |
| generate_receptor_grid(municipality: gpd.GeoDataFrame, zones: gpd.GeoDataFrame, census_sectors: gpd.GeoDataFrame, out_dir: Path, operational_dir: Path  /  None=None, source_paths: dict  /  None=None) | 1288-1390 | Chamadas efetivas: Path, ensure_dirs, _normalize_zones, _normalize_population_sectors, _load_landuse_preference_footprint, _population_anchor_records, _station_records, _boundary_records Retorno: {'status': 'ok', 'total_receptors': int(len(receptors)), 'receptors': receptors, 'diagnostics': diagnostics, 'communities': communities, 'rings': rings, 'boundary_network': boundary_network, 'manifest. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/receptor_grid.py, linhas 299-305.

```python
    if weights.sum() > 0 and centroids:
        x = float(np.average([p.x for p in centroids], weights=weights))
        y = float(np.average([p.y for p in centroids], weights=weights))
        point = Point(x, y)
    else:
        point = footprint.centroid
    return _point_in_footprint(point, footprint)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Média com ou sem pesos. As unidades do resultado são as da variável antes de eventual normalização.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- average: Média com ou sem pesos. As unidades do resultado são as da variável antes de eventual normalização.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/referencias_cruzadas_seminario.py

Completa REF nativos sem reescrever os parágrafos editados pelo usuário.

**Papel.** Histórico editorial: entrega de seminários encerrada. **Fonte inspecionada.** E:\projeto\codigo\referencias_cruzadas_seminario.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| copy | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| lxml | Consulta/edição XML, incluindo os componentes internos de DOCX, PPTX e SVG. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- E:/projeto/output/09_projeto_dissertacao/seminarios_02/Projeto_Ricardo-Queiroz_{version}.docx — chamada ZipFile, linha 141.

**Saídas.**

- E:/projeto/temp/{version}_referencias.docx — chamada ZipFile, linha 206.
- E:/projeto/temp/qa_seminarios/referencias_{version}.json — chamada .write_text, linha 211.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| text(p) | 31-31 | Chamadas efetivas: .join, p.xpath Retorno: ''.join(p.xpath('.//w:t/text()', namespaces=NS)). |
| format_ref_run(r) | 34-43 | Chamadas efetivas: r.find, E.SubElement, Q, E.Element, r.insert, rp.findall, fonts.set, .set |
| run_text(s, template=None) | 45-49 | Chamadas efetivas: E.Element, E.SubElement, t.set, Q, r.append, template.find, deepcopy Retorno: r. |
| field_spans(p) | 52-63 | Chamadas efetivas: child.iter, Q, e.get, stack.append, stack.pop, spans.append, len Retorno: spans. |
| boundary(p, offset, is_end=False) | 66-81 | Chamadas efetivas: field_spans, list, len, text, .index, run_text, p.remove, p.insert Retorno: len(p), list(p).index(last) + 1 if is_end else list(p).index(first). |
| add_bookmark(p, a, b, name, bid) | 84-86 | Chamadas efetivas: boundary, E.Element, endnode.set, p.insert, node.set, Q, str |
| replace_range(p, a, b, nodes) | 89-100 | Chamadas efetivas: list, children.index, enumerate, text, len, all, p.remove, p.insert |
| ref_nodes(name, cached, template, eq=False) | 103-112 | Chamadas efetivas: format_ref_run, result.append, run_text, E.Element, Q, E.SubElement, e.set Retorno: result. |
| preserve_plural_labels(p, targets) | 115-136 | Chamadas efetivas: reversed, field_spans, re.fullmatch, targets.get, list, children.index, next, run_text Retorno: changed. |
| run(version='Entrega', update_method=False) | 139-212 | grava produtos Retorno: info. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/referencias_cruzadas_seminario.py, linhas 200-206.

```python
    replace_range(p,a,b,nodes);inserted+=1
  plural_fixed=sum(preserve_plural_labels(p,targets) for p in d.findall('.//w:p',NS) if p not in captions)
  names={e.get(Q('name')) for e in d.findall('.//w:bookmarkStart',NS)}
  refs=[re.search(r'\bREF\s+(\S+)',s)[1] for s in d.xpath('.//w:instrText/text()',namespaces=NS) if re.search(r'\bREF\s+(\S+)',s)]
  assert all(name in names for name in refs),set(refs)-names
  xml=E.tostring(d,xml_declaration=True,encoding='UTF-8',standalone=True);tmp=R/f'temp/{version}_referencias.docx'
  with ZipFile(tmp,'w',compression=ZIP_DEFLATED) as out:
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. Rotina histórica: conferir pré-condições e versão de dados antes de qualquer execução.

## codigo/regenerar_mapas_atuais.py

Refaz somente a apresentação dos resultados correntes, sem recalcular dados.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\regenerar_mapas_atuais.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| cartografia_apendices | Módulo autoral local; sua ficha está neste relatório. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| stations | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/zoneamento_avaliacao_atual.gpkg — chamada gpd.read_file, linha 52.
- E:/projeto/config.DIRS['out']/11_integracao/apendices/resumo_figuras.json — chamada .read_text, linha 53.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/estacoes_metricas_anuais.csv — chamada pd.read_csv, linha 62.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/estacoes_trienio_atual.csv — chamada pd.read_csv, linha 66.
- E:/projeto/config.DIRS['out']/13_rateio_emissoes/fontes_rateio_{pol}.gpkg — chamada gpd.read_file, linha 81.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_densidade_1ha.gpkg — chamada gpd.read_file, linha 82.

**Saídas.**

- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/identificacao_estacoes_figura_B1.csv — chamada .to_csv, linha 72.

**Campos e chaves lidos.**

- config.DIRS: out, qar.
- yearly.loc: station_id.
- yearly: annual_mean, pollutant.
- roll.loc: station_id.
- roll: n_design_years, pollutant.
- stations: number, station_id, station_name.
- z: health_fraction_pct, pop_estimada.
- sources: dens_linha.
- area: density_t_ha.

**Campos e chaves gerados.**

- stations: number.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 50-93 | lê dados; grava produtos Retorno: float(np.ceil(value / step) * step), [0, *[v for v in [0.1, 1, 10, 100, 1000, 10000] if v < maximum / 3], maximum]. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/regenerar_mapas_atuais.py, linhas 50-58.

```python
def run():
    cart.OUT=OUT
    z=gpd.read_file(OUT/'zoneamento_avaliacao_atual.gpkg')
    extent=json.loads((config.DIRS['out']/'11_integracao/apendices/resumo_figuras.json').read_text(encoding='utf8'))['bounds_degrees']
    muni=gpd.GeoDataFrame(geometry=[z.geometry.union_all()],crs=z.crs)
    for pol in ['PM10','PM25']:
        for integrated in [False,True]:
            code=('B4' if pol=='PM10' else 'B5') if integrated else ('B2' if pol=='PM10' else 'B3')
            fields=[f'{pol}_{s}_'+('integrado_rotulo' if integrated else 'status_rotulo') for s in ['PV','PF']]
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/relatorio_recortes_vento.py

Audita e descreve o calendário efetivamente utilizado nos recortes.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\projeto\codigo\relatorio_recortes_vento.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/16_revisao_pos_banca/vento/calendario_vento_horario.csv — chamada pd.read_csv, linha 45.
- E:/projeto/output/16_revisao_pos_banca/vento/dias_direcao_persistente.csv — chamada pd.read_csv, linha 45.

**Saídas.**

- E:/projeto/output/16_revisao_pos_banca/vento/horas_por_direcao.csv — chamada table.to_csv, linha 55.
- E:/projeto/output/16_revisao_pos_banca/vento/dias_persistentes_por_direcao.csv — chamada daily.to_csv, linha 58.
- E:/projeto/output/16_revisao_pos_banca/vento/Relatorio_recortes_vento.md — chamada .write_text, linha 103.
- E:/projeto/dissertacao/metodologia/recortes-vento.md — chamada .write_text, linha 105.
- E:/projeto/dissertacao/metodologia/horas-por-direcao.csv — chamada table.to_csv, linha 105.
- E:/projeto/output/16_revisao_pos_banca/vento/auditoria_recortes.json — chamada .write_text, linha 106.

**Campos e chaves lidos.**

- c: CODE, direction_idx.
- d: direction_idx, eligible.
- table: 2021, 2022, 2023, direction, mean_speed_m_s, percent_valid, total_hours.
- d.loc: day, direction_idx.
- hours: % válidas, Velocidade m/s.

**Campos e chaves gerados.**

- daily: Total.
- hours: % válidas, Velocidade m/s.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run(sync_editorial=False) | 44-107 | lê dados; grava produtos Retorno: text, ' /  ' + '  /  '.join(map(str, f.columns)) + '  / \n /  ' + '  /  '.join(['---'] * len(f.columns)) + '  / \n' + '\n'.join((' /  ' + '  /  '.join(map(str, row)) + '  / ' for row in f.itertuples(index=False, name=N. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/relatorio_recortes_vento.py, linhas 46-52.

```python
    assert len(c)==26280 and len(d)==1095 and c.CODE.is_unique
    valid=c.direction_idx.ge(0);assert valid.sum()==24892
    rows=[]
    for i,(direction,name) in enumerate(zip(DIRS,NAMES)):
        sub=c[c.direction_idx.eq(i)];row=dict(direction=direction,name=name)
        for year in [2021,2022,2023]:row[str(year)]=int(sub.year.eq(year).sum())
        row.update(total_hours=len(sub),percent_valid=100*len(sub)/valid.sum(),percent_all=100*len(sub)/len(c),mean_speed_m_s=sub.wind_speed.mean(),persistent_days=int(d.direction_idx.eq(i).sum()))
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/relatorio_recortes_vento_pdf.py

Exporta o relatório auditado, com tabelas legíveis e figuras separadas.

**Papel.** Documentação/apoio. **Fonte inspecionada.** E:\projeto\codigo\relatorio_recortes_vento_pdf.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| reportlab.lib | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.enums | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.pagesizes | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.lib.styles | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.pdfbase | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.pdfbase.ttfonts | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| reportlab.platypus | Diagramação de relatórios PDF e desenho de texto/tabelas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| xml.sax.saxutils | Leitura/edição de XML de projetos e documentos. |


**Entradas.**

- Path(__file__).resolve().parents[1]/output/16_revisao_pos_banca/vento/Relatorio_recortes_vento.md — chamada .read_text, linha 42.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- styles: BodyAir, CellAir, HeadAir, TitleAir.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 35-57 | lê dados |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/relatorio_recortes_vento_pdf.py, linhas 35-43.

```python
def run():
    for name,font in [('Arial','arial.ttf'),('Arial-Bold','arialbd.ttf')]:pdfmetrics.registerFont(TTFont(name,_cp_externo('fonts_4d9cd6a')+font))
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='BodyAir',fontName='Arial',fontSize=10.5,leading=13,alignment=TA_JUSTIFY,spaceAfter=5))
    styles.add(ParagraphStyle(name='TitleAir',fontName='Arial-Bold',fontSize=17,leading=21,spaceAfter=15,textColor=colors.HexColor('#174b5d')))
    styles.add(ParagraphStyle(name='HeadAir',fontName='Arial-Bold',fontSize=12,leading=16,spaceBefore=8,spaceAfter=6,textColor=colors.HexColor('#174b5d'),keepWithNext=True))
    styles.add(ParagraphStyle(name='CellAir',fontName='Arial',fontSize=8.3,leading=11))
    story=[];text=(OUT/'Relatorio_recortes_vento.md').read_text(encoding='utf8')
    for block in text.split('\n\n'):
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/representativity.py

Representativity. Processamento ou módulo de apoio. A organização passa por _pick_adt_field, pm_road_distance_class, add_nearest_diagnostics, buffers_by_pollutant, station_coverage_by_zone.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\representativity.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| __future__ | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- r: _adt.
- r.loc: _adt.
- metrics: pollutant.
- m: n_design_years.

**Campos e chaves gerados.**

- out: adt_disponivel, adt_via_mais_proxima, classe_influencia_via_mp, dist_empreendimento_m, dist_via_m, dist_via_principal_m, raio_m, representatividade_inicial.
- r: _adt.
- bufs: geometry.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| _pick_adt_field(roads) | 38-43 | Chamadas efetivas: .lower, candidate.lower, str Retorno: None, lower[candidate.lower()]. |
| pm_road_distance_class(distance_m, adt) | 46-78 | Chamadas efetivas: float, pd.isna Retorno: 'Urbana', 'Indefinida'. |
| add_nearest_diagnostics(stations, roads=None, enterprises=None) | 81-127 | Chamadas efetivas: stations.copy, roads.to_crs, roads.geometry.union_all, out.geometry.distance, _pick_adt_field, enterprises.to_crs, enterprises.geometry.union_all, roads.copy Retorno: out. |
| buffers_by_pollutant(stations, metrics, pollutant, require_design_value=True) | 130-139 | Chamadas efetivas: .copy, stations.merge, gpd.GeoDataFrame, merged.copy, bufs.geometry.buffer, .fillna, pd.to_numeric, metrics.get Retorno: (points, bufs). |
| station_coverage_by_zone(zones, buffers, pollutant) | 142-150 | Chamadas efetivas: zones.copy, buffers.geometry.union_all, z.geometry.area.replace, z.geometry.intersection Retorno: z, z. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/representativity.py, linhas 38-46.

```python
def _pick_adt_field(roads):
    lower = {str(c).lower(): c for c in roads.columns}
    for candidate in config.ADT_FIELD_CANDIDATES:
        if candidate.lower() in lower:
            return lower[candidate.lower()]
    return None

# Pm road distance class
def pm_road_distance_class(distance_m, adt):
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/reproduzir_analise_configuravel.py

Reproduz a classificação atual a partir de matrizes já consolidadas e permite testar outra variável com origem, campo, agregação, transformação e pesos declarados. Grava em pasta separada, sem substituir os mapas publicados.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\reproduzir_analise_configuravel.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| argparse | Parâmetros fornecidos ao iniciar o programa. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| importlib.metadata | Importação e identificação de versões das bibliotecas. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| rasterio | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| rasterio.features | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| rasterio.windows | Leitura e escrita de rasters, transformação entre pixel e coordenada e amostragem por geometria. |
| scipy.cluster.hierarchy | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.cluster.vq | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.optimize | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.sparse | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.spatial | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.stats | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| warnings | Controle de avisos de bibliotecas sem alterar a definição do estimador. |


**Entradas.**

- caminho(spec['arquivo']) — chamada gpd.read_file, linha 68.
- caminho(spec['arquivo']) — chamada pd.read_csv, linha 78.
- caminho(spec['arquivo']) — chamada rasterio.open, linha 82.
- args.config — chamada .read_text, linha 236.

**Saídas.**

- caminho(config['saida'])/analise_configuravel.gpkg [camada 'resultados'] — chamada out.to_file, linha 228.
- caminho(config['saida'])/indicadores.csv — chamada .to_csv, linha 229.
- caminho(config['saida'])/comparacao_k.csv — chamada table.to_csv, linha 230.
- caminho(config['saida'])/normalizacao.csv — chamada params.to_csv, linha 230.
- caminho(config['saida'])/sensibilidade.csv — chamada .to_csv, linha 230.
- caminho(config['saida'])/moran.csv — chamada .to_csv, linha 231.
- caminho(config['saida'])/manifesto.json — chamada .write_text, linha 233.

**Campos e chaves lidos.**

- spec: arquivo, camada, campo, nome.
- support: geometry.
- src: geometry.
- overlap: _a, _av.
- s: _a, _av.
- config: base, campo_bacia, cenarios, chaves, inicializacoes, k_testados, normalizacao, saida, semente, suporte_calculo, variaveis.
- v: nome.
- setting: pesos.
- table: cenario.
- local: cluster, q.

**Campos e chaves gerados.**

- work: _i.
- overlap: _a, _av.
- out: completo, estabilidade, q_fdr, r_moran, r_quintil.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| ler_camada(spec) | 66-68 | lê dados Retorno: gpd.read_file(path, layer=spec['camada']) if spec.get('camada') else gpd.read_file(path). |
| anexar_variavel(base, spec, support) | 71-105 | lê dados Retorno: pd.to_numeric(base[field], errors='coerce').to_numpy(), pd.to_numeric(base[[left]].merge(src[[right, field]], left_on=left, right_on=right, how='left', validate='many_to_one')[field], errors='coerce'). |
| matriz(base, support, config) | 108-124 | Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original. Retorno: (norm, valid, pd.DataFrame({'variavel': fields, 'centro_ou_minimo': center, 'escala_ou_amplitude': scale})). |
| ari(a, b) | 127-132 | Chamadas efetivas: np.unique, len, .reshape, comb, .sum, tab.sum, np.bincount, a.max Retorno: (x - e) / den if den else 1.0. |
| fitkm(x, k, seed, starts=12) | 135-144 | Ajusta centroides pelo k-means. A matriz de entrada, a inicialização ++, a semente e as repetições determinam a solução reproduzida. Retorno: best. |
| silhouette(x, l) | 147-154 | Chamadas efetivas: distance.cdist, enumerate, float, same.sum, min, s.append, np.mean, .sum Retorno: float(np.mean(s)). |
| bh(p) | 157-158 | Chamadas efetivas: np.asarray, np.argsort, np.empty, np.minimum, np.minimum.accumulate, len, np.arange Retorno: o. |
| align(labels, reference) | 161-163 | Chamadas efetivas: .reshape, linear_sum_assignment, dict, np.array, max, zip, labels.max, reference.max Retorno: np.array([lookup[v] for v in labels]). |
| queen(g) | 166-168 | Chamadas efetivas: g.sindex.query, len, csr_matrix, w.maximum, w.setdiag, w.eliminate_zeros, np.ones Retorno: w. |
| moran_w(values, w, local=False, seed=SEED) | 171-188 | Chamadas efetivas: np.flatnonzero, .tocsr, len, float, np.random.default_rng, range, np.empty, bh Retorno: (rec, {'p': p, 'q': q, 'cluster': cl, 'Ii': Ii}, original), ({'n': n, 'isolados': int((~good).sum()), 'I': np.nan, 'p': np.nan}, None, original). |
| executar(config) | 191-233 | grava produtos; Agrupamento hierárquico. Com method=ward, as fusões procuram o menor aumento da dispersão interna.; Associação por postos. Mede ordenação conjunta, não igualdade de magnitude nem desempenho frente a observações ausentes. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/reproduzir_analise_configuravel.py, linhas 113-119.

```python
            if np.any(values[np.isfinite(values)]<0):raise ValueError('log1p exige valores não negativos nesta análise')
            values=np.log1p(values)
        elif transform!='identidade':raise ValueError('Transformação desconhecida: '+transform)
        columns.append(values);fields.append(spec['nome'])
    x=np.column_stack(columns);valid=np.isfinite(x).all(axis=1)
    if valid.sum()<8:raise ValueError('Menos de oito registros completos; revisar entradas e lacunas')
    if config['normalizacao']=='minmax':
```

Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original.

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/reproduzir_analise_configuravel.py, linhas 128-134.

```python
    _,a=np.unique(a,return_inverse=True);_,b=np.unique(b,return_inverse=True);n=len(a)
    tab=np.bincount(a*(b.max()+1)+b,minlength=(a.max()+1)*(b.max()+1)).reshape(a.max()+1,b.max()+1)
    comb=lambda x:(x*(x-1)/2).sum()
    x=comb(tab);r=comb(tab.sum(0));s=comb(tab.sum(1));e=r*s/(n*(n-1)/2);den=(r+s)/2-e
    return (x-e)/den if den else 1.

# Fitkm
```

Conta ocorrências ou soma pesos por identificador inteiro. O vetor weights define se há contagem ou acumulação ponderada.

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- log1p: Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original.
- std: Desvio-padrão. Na padronização z, coloca colunas em escala comparável; conferir ddof no trecho.
- bincount: Conta ocorrências ou soma pesos por identificador inteiro. O vetor weights define se há contagem ou acumulação ponderada.
- kmeans2: Ajusta centroides pelo k-means. A matriz de entrada, a inicialização ++, a semente e as repetições determinam a solução reproduzida.
- cdist: Matriz de distâncias entre observações. É usada no agrupamento, na silhouette ou na comparação entre centroides.
- linear_sum_assignment: Alinha rótulos de grupos pela maior correspondência; evita contar como mudança apenas a troca do número do grupo.
- sqrt: Raiz quadrada. No ajuste ponderado do k-means, multiplicar a coluna por √peso faz o peso entrar uma única vez na distância ao quadrado.
- linkage: Agrupamento hierárquico. Com method=ward, as fusões procuram o menor aumento da dispersão interna.
- fcluster: Transforma a árvore hierárquica em rótulos de grupos segundo o critério fornecido.
- spearmanr: Associação por postos. Mede ordenação conjunta, não igualdade de magnitude nem desempenho frente a observações ausentes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/revisao_bibliografica_v38.py

Revisao bibliografica v38. Histórico editorial: entrega de seminários encerrada. As instruções são executadas no corpo principal, na ordem do arquivo.

**Papel.** Histórico editorial: entrega de seminários encerrada. **Fonte inspecionada.** E:\projeto\codigo\revisao_bibliografica_v38.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| __future__ | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/revisao_bibliografica_v38.py, linhas 12-20.

```python
_cp_file = _cp_Path(globals().get('__file__', _cp_Path.cwd() / 'codigo' / 'script.py')).resolve()
for _cp_parent in [_cp_file.parent, *_cp_file.parents]:
    _cp_code = _cp_parent if (_cp_parent / 'caminhos_congonhas.py').is_file() else _cp_parent / 'codigo'
    if (_cp_code / 'caminhos_congonhas.py').is_file():
        if str(_cp_code) not in _cp_sys.path: _cp_sys.path.insert(0, str(_cp_code))
        break
from caminhos_congonhas import raiz_projeto as _cp_raiz, texto_caminho as _cp_texto, externo as _cp_externo, adaptar_texto as _cp_adaptar
# FIM DOS CAMINHOS PORTÁTEIS

```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. Rotina histórica: conferir pré-condições e versão de dados antes de qualquer execução.

## codigo/revisao_espacial_pos_banca.py

É a análise espacial inicial pós-banca e reúne funções reutilizadas. Seu agrupamento original utiliza quatro indicadores; não deve ser confundido com a matriz conjunta de seis indicadores do pôster atual.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\revisao_espacial_pos_banca.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| scipy | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.cluster.hierarchy | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.cluster.vq | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.sparse.csgraph | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| scipy.spatial | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| shapely | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/13_rateio_emissoes/fontes_rateio_{pol}.gpkg — chamada gpd.read_file, linha 159.
- E:/projeto/output/11_integracao/nova_modelagem/zoneamento_nova_modelagem.gpkg — chamada gpd.read_file, linha 204.
- E:/projeto/output/11_integracao/nova_modelagem/{pol}_indicadores_trienais_receptores.csv — chamada pd.read_csv, linha 208.
- E:/projeto/output/11_integracao/nova_modelagem/{pol}_indicadores_trienais_receptores.csv — chamada path.read_bytes, linha 209.
- E:/projeto/output/11_integracao/nova_modelagem/PM10_indicadores_trienais_receptores.csv — chamada pd.read_csv, linha 217.
- E:/projeto/output/11_integracao/nova_modelagem/{pol}_fechamento_receptores.csv — chamada pd.read_csv, linha 237.
- E:/projeto/output/11_integracao/nova_modelagem/{pol}_receptores_anuais.csv — chamada pd.read_csv, linha 248.

**Saídas.**

- {path} — chamada path.write_text, linha 82.
- E:/projeto/output/16_revisao_pos_banca/{pol}_fontes_celulas.csv — chamada .to_csv, linha 177.
- E:/projeto/output/16_revisao_pos_banca/{pol}_lisa_receptores.csv — chamada .to_csv, linha 224.
- E:/projeto/output/16_revisao_pos_banca/{pol}_lisa_bivariado.csv — chamada .to_csv, linha 226.
- E:/projeto/output/16_revisao_pos_banca/{name}.gpkg — chamada frame.to_file, linha 300.
- E:/projeto/output/16_revisao_pos_banca/{name}.csv — chamada .to_csv, linha 300.
- E:/projeto/output/16_revisao_pos_banca/vinculo_celula_zona.csv — chamada links.to_csv, linha 301.
- E:/projeto/output/16_revisao_pos_banca/correlogramas.csv — chamada .to_csv, linha 301.
- E:/projeto/output/16_revisao_pos_banca/sensibilidade_espacial.csv — chamada .to_csv, linha 301.
- E:/projeto/output/16_revisao_pos_banca/comparacao_agrupamentos.csv — chamada .to_csv, linha 301.
- E:/projeto/output/16_revisao_pos_banca/limiares_associativos_validacao_espacial.csv — chamada .to_csv, linha 301.
- E:/projeto/output/16_revisao_pos_banca/contribuicoes_regioes.csv — chamada .to_csv, linha 301.

**Campos e chaves lidos.**

- v: kind.
- cells: geometry, receptor_id.
- d: ANNUAL_MODEL, P98_MODEL, X, Y.
- points: PM25_annual, X, Y, receptor_id.
- stats: pols.
- r: silhouette.
- best: k, method.
- a: year.
- z: geometry, zone_index.
- z.loc: zone_index.

**Campos e chaves gerados.**

- points: cluster_profile, receptor_id.
- stats: cell_area_conservation_relative_error, clustering_selection, geometric_fragments, k8_distance_m, zone_coverage, zone_quintile_area_sums.
- inter: area_m2, support_method, zone_area_fraction.
- z: fragmento_menor_1m2.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| save_json(path, data) | 81-82 | grava produtos |
| bh(p) | 85-87 | Chamadas efetivas: np.asarray, np.argsort, np.empty_like, np.minimum, np.minimum.accumulate, np.arange, len Retorno: out. |
| weights(xy, k) | 90-93 | Chamadas efetivas: len, .query, sparse.csr_matrix, cKDTree, min, np.full, np.repeat, ids.ravel Retorno: (w, ids, dist). |
| moran(z, w, permutations=999, seed=SEED) | 96-103 | Chamadas efetivas: len, float, np.random.default_rng, range, np.asarray, np.mean, w.sum, rng.permutation Retorno: {'I': observed, 'expected': expected, 'p_two_sided': p, 'permutations': permutations}. |
| local_moran(x, ids, y=None, permutations=999, seed=SEED) | 106-121 | Chamadas efetivas: np.asarray, len, .mean, np.random.default_rng, np.empty, range, bh, np.where Retorno: pd.DataFrame({'local_I': stat, 'p_conditional': p, 'q_FDR': q, 'z': z, 'spatial_lag': lag, 'quadrant': quad, 'cluster': np.where(q <= 0.05, quad, 'Não significativo')}). |
| silhouette(x, labels) | 124-131 | Chamadas efetivas: distance.cdist, np.unique, enumerate, float, same.sum, min, s.append, np.mean Retorno: float(np.mean(s)). |
| ari(a, b) | 134-138 | Chamadas efetivas: np.zeros, np.add.at, len, c, np.unique, np.sum, float, a.max Retorno: float((s - expected) / (mx - expected)) if mx > expected else 1.0. |
| relative_quartile(v) | 141-142 | Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. Retorno: (np.searchsorted(q, np.asarray(v), side='left') + 1, q). |
| relative_quintile(v) | 145-147 | Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. Retorno: (np.searchsorted(q, np.asarray(v), side='left') + 1, q). |
| cells_for(points, municipality) | 150-155 | Chamadas efetivas: voronoi_polygons, gpd.GeoDataFrame, make_valid, MultiPoint, .all, points.geometry.to_list, points.receptor_id.to_numpy, len Retorno: cells. |
| emission_allocation(cells, municipality, pol) | 158-178 | lê dados; grava produtos Retorno: (masses, {'total_source_mass_tpy': float(sources.massa.sum()), 'municipal_mass_expected_tpy': expected, 'allocated_mass_tpy': float(masses.sum()), 'absolute_error_tpy': err, 'sources_missing_geometry_. |
| stump(x, y, min_fraction=0.1) | 181-185 | Chamadas efetivas: np.argsort, len, np.cumsum, np.arange, max, np.argmin, int, .any Retorno: (float((sx[cut] + sx[cut + 1]) / 2), float(sy[:cut + 1].mean()), float(sy[cut + 1:].mean())), None. |
| thresholds(x, y, xy, pol, unit) | 188-199 | Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original. Retorno: out. |
| main() | 202-303 | lê dados; grava produtos; Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original.; Agrupamento hierárquico. Com method=ward, as fusões procuram o menor aumento da dispersão interna.; Ajusta centroides pelo k-means. A matriz de entrada, a inicialização ++, a semente e as repetições determinam a solução reproduzida. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/revisao_espacial_pos_banca.py, linhas 124-130.

```python
def silhouette(x,labels):
 d=distance.cdist(x,x);classes=np.unique(labels);s=[]
 for i,label in enumerate(labels):
  same=labels==label;n=same.sum()
  if n<=1:s.append(0.);continue
  a=d[i,same].sum()/(n-1);b=min(d[i,labels==c].mean() for c in classes if c!=label)
  s.append((b-a)/max(a,b) if max(a,b)>0 else 0.)
```

Matriz de distâncias entre observações. É usada no agrupamento, na silhouette ou na comparação entre centroides.

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

Trecho de codigo/revisao_espacial_pos_banca.py, linhas 141-147.

```python
def relative_quartile(v):
 q=np.quantile(v,[.25,.5,.75]);return np.searchsorted(q,np.asarray(v),side='left')+1,q

# Relative quintile
def relative_quintile(v):
 """Cinco faixas P20/P40/P60/P80; empates permanecem juntos."""
 q=np.quantile(v,[.2,.4,.6,.8]);return np.searchsorted(q,np.asarray(v),side='left')+1,q
```

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- std: Desvio-padrão. Na padronização z, coloca colunas em escala comparável; conferir ddof no trecho.
- cdist: Matriz de distâncias entre observações. É usada no agrupamento, na silhouette ou na comparação entre centroides.
- quantile: Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.
- log1p: Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original.
- sqrt: Raiz quadrada. No ajuste ponderado do k-means, multiplicar a coluna por √peso faz o peso entrar uma única vez na distância ao quadrado.
- average: Média com ou sem pesos. As unidades do resultado são as da variável antes de eventual normalização.
- linkage: Agrupamento hierárquico. Com method=ward, as fusões procuram o menor aumento da dispersão interna.
- fcluster: Transforma a árvore hierárquica em rótulos de grupos segundo o critério fornecido.
- kmeans2: Ajusta centroides pelo k-means. A matriz de entrada, a inicialização ++, a semente e as repetições determinam a solução reproduzida.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/revisao_trienal_grupos.py

Indicadores trienais por receptor, saturação coerente e decomposição urbana.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\revisao_trienal_grupos.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| cartografia_apendices | Módulo autoral local; sua ficha está neste relatório. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| methodology_rules | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| out_aermod_reader | Módulo autoral local; sua ficha está neste relatório. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| standards | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/zoneamento_periodo_comum.gpkg — chamada gpd.read_file, linha 52.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_receptores_anuais.csv — chamada pd.read_csv, linha 57.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_vinculo_receptor_zona.csv — chamada pd.read_csv, linha 60.

**Saídas.**

- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_indicadores_trienais_receptores.csv — chamada period.to_csv, linha 59.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_todos_grupos_por_zona.csv — chamada zonegroups.to_csv, linha 76.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{pol}_ABC_sintese_criticos.{ext} — chamada ax.figure.savefig, linha 96.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/ABC_zonas_criticas.csv — chamada .to_csv, linha 98.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/componentes_urbanos_por_zona.csv — chamada .to_csv, linha 99.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/zoneamento_periodo_comum.gpkg — chamada .to_file, linha 100.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/zoneamento_periodo_comum.csv — chamada .to_csv, linha 100.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/zoneamento_nova_modelagem.gpkg — chamada .to_file, linha 101.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/zoneamento_nova_modelagem.csv — chamada .to_csv, linha 101.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/revisao_trienal.json — chamada .write_text, linha 102.

**Campos e chaves lidos.**

- config.DIRS: out, post.
- selected: ANNUAL.
- row: URB, URB-FER, URB-NUC, URB-VIA.
- zonegroups: URB-FER, URB-NUC, URB-VIA.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 51-102 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/revisao_trienal_grupos.py, linhas 61-67.

```python
        p=period.merge(links,on=['X','Y'],validate='one_to_many')
        means=p.groupby('zone_index')[['ANNUAL_MODEL','P98_MODEL']].mean()
        maxima=p.groupby('zone_index')[['ANNUAL_MODEL','P98_MODEL']].max()
        ia=100*means.ANNUAL_MODEL/STANDARDS[pol]['PV']['ANNUAL'];idaily=100*means.P98_MODEL/STANDARDS[pol]['PV']['24H']
        if f'{pol}_ISZ_envelope_anterior' not in z:z[f'{pol}_ISZ_envelope_anterior']=z[f'{pol}_ISZ_parcial']
        z[f'{pol}_ISZ_parcial']=np.maximum(ia,idaily).reindex(z.index)
        z[f'{pol}_saturacao_comparativa']=z[f'{pol}_ISZ_parcial'].map(saturation_class)
```

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

Trecho de codigo/revisao_trienal_grupos.py, linhas 71-77.

```python
        for group in GROUPS:
            t=annual(selected[group,'ANNUAL']).groupby(['X','Y'],as_index=False).CONC.mean()
            t=t.rename(columns={'CONC':group});frames.append(t.set_index(['X','Y']))
        allgroups=pd.concat(frames,axis=1).reset_index().merge(links,on=['X','Y'],validate='one_to_many')
        zonegroups=allgroups.groupby('zone_index')[list(GROUPS)].mean()
        zonegroups.to_csv(OUT/f'{pol}_todos_grupos_por_zona.csv')
        primary=[g for g in GROUPS if GROUPS[g]['kind']=='primary']
```

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/revisar_poster_20261109.py

Prepara os painéis e resumos atuais do pôster Congonhas, incluindo o perfil conjunto, a densidade de emissão e as contribuições das regiões prioritárias.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\revisar_poster_20261109.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| cartografia_apendices | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.figure | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| openpyxl | Leitura/escrita de planilhas XLSX; não é o mecanismo do Excel aberto. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| pyproj | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| revisar_poster_e_guias_20261108 | Módulo autoral local; sua ficha está neste relatório. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| svg_compativel_word | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| xml.etree.ElementTree | Leitura/edição de XML de projetos e documentos. |


**Entradas.**

- E:/projeto/descontinuado/2026_11_09_poster_rodovias_inventariadas/manifesto.json — chamada m.read_text, linha 73.
- {path} — chamada path.read_bytes, linha 74.
- E:/projeto/output/13_cmas_posters/Congonhas/Emissoes_densidade_sensibilidade_por_zona.gpkg — chamada gp.read_file, linha 88.
- E:/projeto/output/16_revisao_pos_banca/celulas_analise.gpkg — chamada gp.read_file, linha 89.
- E:/projeto/output/16_revisao_pos_banca/cenario_geral/PM25_anual_receptores.csv — chamada pd.read_csv, linha 90.
- E:/projeto/output/13_rateio_emissoes/fontes_rateio_PM25.gpkg — chamada gp.read_file, linha 108.
- E:/projeto/output/11_integracao/apendices/resumo_figuras.json — chamada .read_text, linha 117.
- E:/projeto/output/16_revisao_pos_banca/limiares_cinco_faixas_validacao.csv — chamada pd.read_csv, linha 146.
- E:/projeto/output/16_revisao_pos_banca/cenario_geral/PM25_1h_receptores.csv — chamada pd.read_csv, linha 154.
- E:/projeto/output/16_revisao_pos_banca/cenario_geral/{pol}_{per}_receptores.csv — chamada pd.read_csv, linha 157.
- E:/projeto/output/16_revisao_pos_banca/contribuicoes_prioridades_pooled_PM25.csv — chamada pd.read_csv, linha 164.

**Saídas.**

- E:/projeto/descontinuado/2026_11_09_poster_rodovias_inventariadas/manifesto.json — chamada m.write_text, linha 75.
- E:/projeto/output/13_cmas_posters/Congonhas/Auditoria_vias_inventariadas_densidade.csv — chamada .to_csv, linha 115.
- E:/projeto/codigo/recursos_poster/assets/dados_poster_20261109.json — chamada .write_text, linha 173.
- E:/projeto/output/13_cmas_posters/Congonhas/Perfis_conjuntos_estatisticas.csv — chamada .to_csv, linha 174.
- E:/projeto/output/13_cmas_posters/Congonhas/Cortes_emissao_boxplot_PM25.csv — chamada cuts.to_csv, linha 175.
- E:/projeto/output/13_cmas_posters/Congonhas/Auditoria_revisao_poster_20261109.json — chamada .write_text, linha 176.

**Campos e chaves lidos.**

- c: PM25_annual, geometry, receptor_id.
- annual: concentration, dominant_group, receptor_id.
- d: ID.
- roads: corridor_m2, length_m, massa, source_id, source_type, width_m.
- v: name, value.
- cuts: basis, pollutant.
- pooled.loc: share_pct.
- pooled: group_id.

**Campos e chaves gerados.**

- roads: corridor_m2, density_corridor, length_m, width_m.
- g: dominant_name.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| archive(path) | 67-75 | lê dados; grava produtos |
| run() | 78-177 | lê dados; grava produtos; Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. Retorno: original_save(fig, *args, **kwargs). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/revisar_poster_20261109.py, linhas 151-157.

```python
        vals=d.cut_train.to_numpy()
        box.append(dict(percentile=int(q),concentration=float(d.concentration_cut.iloc[0]),full_cut=float(d.cut_all_data.iloc[0]),values=vals.tolist(),q25=float(np.quantile(vals,.25)),median=float(np.median(vals)),q75=float(np.quantile(vals,.75)),minimum=float(vals.min()),maximum=float(vals.max()),balanced_accuracy_mean=float(d.balanced_accuracy_test.mean())))
    cluster=[]
    labels=pd.read_csv(P/'cenario_geral/PM25_1h_receptores.csv')[['receptor_id','best_cluster']]
    for pol in ['PM10','PM25']:
        for per in ['1h','24h','anual']:
            f=pd.read_csv(P/f'cenario_geral/{pol}_{per}_receptores.csv')
```

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Cálculos a observar nesta rotina.**

- quantile: Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/revisar_poster_e_guias_20261108.py

Insumos cartográficos do pôster, com rateio zonal auditável e escala física.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\revisar_poster_e_guias_20261108.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| cartografia_apendices | Módulo autoral local; sua ficha está neste relatório. |
| copy | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.colors | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.figure | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.font_manager | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.path | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.textpath | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shapely | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| svg_compativel_word | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| xml.etree.ElementTree | Leitura/edição de XML de projetos e documentos. |


**Entradas.**

- E:/projeto/descontinuado/2026_11_08_poster_detalhado/manifesto.json — chamada f.read_text, linha 55.
- {p} — chamada p.read_bytes, linha 56.
- E:/projeto/output/16_revisao_pos_banca/zoneamento_pos_banca.gpkg — chamada gp.read_file, linha 117.
- E:/projeto/output/16_revisao_pos_banca/celulas_analise.gpkg — chamada gp.read_file, linha 118.
- E:/projeto/output/13_rateio_emissoes/fontes_rateio_PM25.gpkg — chamada gp.read_file, linha 119.
- E:/projeto/output/16_revisao_pos_banca/limiares_cinco_faixas_validacao.csv — chamada pd.read_csv, linha 137.
- E:/projeto/output/11_integracao/apendices/resumo_figuras.json — chamada .read_text, linha 154.

**Saídas.**

- E:/projeto/descontinuado/2026_11_08_poster_detalhado/manifesto.json — chamada f.write_text, linha 57.
- E:/projeto/output/13_cmas_posters/Congonhas/Rateio_emissoes_MP25_por_fonte_zona.csv — chamada .to_csv, linha 147.
- E:/projeto/output/13_cmas_posters/Congonhas/Emissoes_densidade_sensibilidade_por_zona.csv — chamada .to_csv, linha 148.
- E:/projeto/output/13_cmas_posters/Congonhas/Emissoes_densidade_sensibilidade_por_zona.gpkg — chamada z.to_file, linha 151.
- E:/projeto/output/13_cmas_posters/Congonhas/Auditoria_mapas_emissao_poster.json — chamada .write_text, linha 153.

**Campos e chaves lidos.**

- z: density, high_area_pct, zone_index.
- f: balanced_accuracy_test, basis, cut_all_data, cut_train, percentile_target, pollutant.

**Campos e chaves gerados.**

- z: area_km2, density, high_area_pct, high_band, mass_tpy, unstable_area_pct.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| archive(p) | 50-57 | lê dados; grava produtos |
| svg_path(path) | 60-68 | Chamadas efetivas: path.iter_segments, .join, out.append Retorno: ' '.join(out). |
| prepare_svg(source, target, scale=200000, method=False) | 71-111 | Chamadas efetivas: ET.parse, tree.getroot, set, list, ET.SubElement, next, root.findall, max |
| run() | 114-183 | lê dados; grava produtos Retorno: original_save(fig, *args, **kwargs). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/revisar_poster_e_guias_20261108.py, linhas 134-140.

```python
            if mode!='point':remaining=remaining.difference(z.geometry.iloc[i])
    assert abs(mass.sum()-expected)<.001,(mass.sum(),expected)
    z['mass_tpy']=mass;z['area_km2']=z.area/1e6;z['density']=np.divide(mass,z.area/1e6,out=np.full(len(z),np.nan),where=z.area>0)
    f=pd.read_csv(R/'output/16_revisao_pos_banca/limiares_cinco_faixas_validacao.csv');f=f[(f.pollutant=='PM25')&(f.basis=='density_tpy_km2')&(f.percentile_target==80)]
    cut=float(f.cut_all_data.iloc[0]);lo=float(f.cut_train.min());hi=float(f.cut_train.max())
    high=np.zeros(len(z));unstable=np.zeros(len(z));covered=np.zeros(len(z))
    for r in c.itertuples():
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/revisar_seminario_contraste_series.py

Atualiza o texto corrente, preservando a formatação e o desenvolvimento integral.

**Papel.** Histórico editorial: entrega de seminários encerrada. **Fonte inspecionada.** E:\projeto\codigo\revisar_seminario_contraste_series.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| copy | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| docx | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.enum.text | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.oxml | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.oxml.ns | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.shared | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/11_integracao/nova_modelagem/identificacao_estacoes_figura_B1.csv — chamada pd.read_csv, linha 68.
- E:/projeto/output/10_avaliacao_rede/anuais_mma.csv — chamada pd.read_csv, linha 69.
- E:/projeto/output/10_avaliacao_rede/trienios_mma.csv — chamada pd.read_csv, linha 69.
- E:/projeto/output/11_integracao/nova_modelagem/figuras_seminario_manifesto.json — chamada .read_text, linha 95.

**Saídas.**

- E:/projeto/output/09_projeto_dissertacao/seminarios_02/Projeto_Ricardo-Queiroz_Entrega.docx — chamada d.save, linha 112.
- E:/projeto/output/11_integracao/nova_modelagem/figuras_seminario_manifesto.json — chamada .write_text, linha 112.

**Campos e chaves lidos.**

- item: codigo.
- x: codigo.

**Campos e chaves gerados.**

- item: titulo.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| text(p, value) | 42-46 | Chamadas efetivas: p.add_run |
| fmt(x) | 49-49 | Chamadas efetivas: pd.isna, .replace Retorno: 'n.d.' if pd.isna(x) else f'{x:.2f}'.replace('.', ','). |
| run() | 52-113 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/revisar_seminario_contraste_series.py, linhas 42-50.

```python
def text(p,value):
    if p.runs:
        p.runs[0].text=value
        for r in p.runs[1:]:r.text=''
    else:p.add_run(value)

# Fmt
def fmt(x):return 'n.d.' if pd.isna(x) else f'{x:.2f}'.replace('.',',')

```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. Rotina histórica: conferir pré-condições e versão de dados antes de qualquer execução.

## codigo/revisar_seminario_monitoramento_mma.py

Atualização do texto e tabelas; a leitura é derivada integralmente da entrega.

**Papel.** Histórico editorial: entrega de seminários encerrada. **Fonte inspecionada.** E:\projeto\codigo\revisar_seminario_monitoramento_mma.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| copy | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| docx | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.enum.text | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.oxml | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.oxml.ns | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.shared | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.text.paragraph | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/11_integracao/nova_modelagem/estacoes_trienio_atual.csv — chamada pd.read_csv, linha 132.
- E:/projeto/output/11_integracao/nova_modelagem/identificacao_estacoes_figura_B1.csv — chamada pd.read_csv, linha 132.
- E:/projeto/output/10_avaliacao_rede/anuais_mma.csv — chamada pd.read_csv, linha 161.
- E:/projeto/output/10_avaliacao_rede/trienios_mma.csv — chamada pd.read_csv, linha 167.
- E:/projeto/output/11_integracao/nova_modelagem/figuras_seminario_manifesto.json — chamada .read_text, linha 173.

**Saídas.**

- E:/projeto/output/09_projeto_dissertacao/seminarios_02/Projeto_Ricardo-Queiroz_Entrega.docx — chamada d.save, linha 172.
- E:/projeto/output/11_integracao/nova_modelagem/figuras_seminario_manifesto.json — chamada .write_text, linha 180.

**Campos e chaves lidos.**

- selected: pollutant, station_id.
- x: codigo, titulo.

**Campos e chaves gerados.**

- x: titulo.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| settext(p, t) | 44-48 | Chamadas efetivas: p.add_run |
| after(p, t, style=None) | 51-54 | Chamadas efetivas: OxmlElement, p._p.addnext, Paragraph, v.add_run, .append, deepcopy, p._p.pPr.find, v._p.get_or_add_pPr Retorno: v. |
| fmt(v) | 57-57 | Chamadas efetivas: pd.isna, .replace Retorno: 'n.d.' if pd.isna(v) else f'{v:.2f}'.replace('.', ','). |
| table(d, headers, rows, anchor=None, font=8.5) | 60-80 | Chamadas efetivas: d.add_table, enumerate, OxmlElement, .append, t._tbl.tblPr.append, zip, e.set, borders.append Retorno: t. |
| run() | 83-181 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/revisar_seminario_monitoramento_mma.py, linhas 44-52.

```python
def settext(p,t):
    if p.runs:
        p.runs[0].text=t
        for r in p.runs[1:]:r.text=''
    else:p.add_run(t)

# After
def after(p,t,style=None):
    n=OxmlElement('w:p');p._p.addnext(n);v=Paragraph(n,p._parent);v.style=style or p.style
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. Rotina histórica: conferir pré-condições e versão de dados antes de qualquer execução.

## codigo/revisar_texto_orientadora.py

Revisão científica de 31/10 sobre a Entrega autoral preservada.

**Papel.** Histórico editorial: entrega de seminários encerrada. **Fonte inspecionada.** E:\projeto\codigo\revisar_texto_orientadora.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| copy | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| docx | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.enum.table | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.enum.text | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.oxml | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.oxml.ns | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| docx.shared | Geração/edição da estrutura DOCX por python-docx; não calcula indicadores ambientais. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| lxml | Consulta/edição XML, incluindo os componentes internos de DOCX, PPTX e SVG. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| referencias_cruzadas_seminario | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/09_projeto_dissertacao/seminarios_02/Projeto_Ricardo-Queiroz_Entrega.docx — chamada current.read_bytes, linha 188.
- E:/projeto/descontinuado/2026-10-31_revisao_cientifica/output/09_projeto_dissertacao/seminarios_02/Projeto_Ricardo-Queiroz_Entrega.docx — chamada BASE.read_bytes, linha 188.
- E:/projeto/output/15_auditoria_metodologica/revisao_cientifica/robustez_cientifica.json — chamada .read_text, linha 192.
- E:/projeto/temp/revisao_orientadora_31/redacao_proposta.json — chamada .read_text, linha 193.

**Saídas.**

- E:/projeto/output/09_projeto_dissertacao/seminarios_02/Projeto_Ricardo-Queiroz_Entrega.docx — chamada d.save, linha 256.
- E:/projeto/temp/revisao_orientadora_31/texto_revisado.txt — chamada .write_text, linha 258.
- E:/projeto/temp/revisao_orientadora_31/alteracoes_aplicadas.json — chamada .write_text, linha 259.

**Campos e chaves lidos.**

- r: coverage, performance, zonal.
- x: bias, changed, correlation, coverage_cut_pct, covered_zones, mae, modelled_mean, n, observed_mean, pollutant, radius_m, rmse, station_id.
- c: area_pct, population_pct_of_allocated, zones.
- a: abc_A_identical_75_80_85, abc_tested_zones, concentration_population_rank, critical_cuts, mass_density_rank, mean_vs_max, source_shares_equal_zone_pct, source_shares_population_weighted_pct, thresholds.
- b: abc_A_identical_75_80_85, abc_tested_zones, concentration_population_rank, critical_cuts, mass_density_rank, mean_vs_max, source_shares_equal_zone_pct, source_shares_population_weighted_pct, thresholds.
- v: high_concentration_footprint, model_observed_mean_ratio, monitored_footprint, n, pollutant.
- m: area_pct, population_pct_of_allocated, zones.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| num(v, d=1) | 54-54 | Chamadas efetivas: .replace Retorno: f'{v:,.{d}f}'.replace(',', '@').replace('.', ',').replace('@', '.'). |
| rewrite(p, s) | 57-67 | Chamadas efetivas: next, list, p.add_run, deepcopy, p._p.xpath, any, r._r.insert, p._p.remove |
| change_caption(p, suffix) | 70-78 | Chamadas efetivas: E.fromstring, text, re.search, replace_range, .replace, E.tostring, m.end, len |
| table(doc, headers, rows, widths) | 81-109 | Chamadas efetivas: doc.add_table, zip, enumerate, OxmlElement, .append, Pt, Cm, len Retorno: t. |
| caption(doc, kind, n, suffix) | 112-120 | Chamadas efetivas: doc.add_paragraph, p.add_run, str, OxmlElement, r._r.append, x.set, qn |
| appendix(doc, r) | 123-182 | Chamadas efetivas: doc.add_paragraph, next, caption, table, heading._p.insert, rows.append, rows.extend, p.text.startswith |
| run() | 185-261 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/revisar_texto_orientadora.py, linhas 260-263.

```python
    start=next(i for i,p in enumerate(d.paragraphs) if p.text=='INTRODUÇÃO/REVISÃO DA LITERATURA');end=next(i for i,p in enumerate(d.paragraphs) if p.text=='CRONOGRAMA')
    print('Texto atualizado;',sum(len(p.text.split()) for p in d.paragraphs[start:end]),'palavras no corpo;',len(d.inline_shapes),'figuras preservadas;',len(d.tables),'tabelas.',flush=True)

if __name__=='__main__':run()
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. Rotina histórica: conferir pré-condições e versão de dados antes de qualquer execução.

## codigo/risk.py

Implementa a avaliação sanitária complementar de Congonhas. Calcula β=ln(RR)/10 e AF=1−exp(−β×ΔC); casos potencialmente evitáveis são AF×população×incidência basal/100.000, com fator temporal 1/365 na avaliação aguda. Preserva função, desfecho, faixa etária e fonte de exposição; verifica se o intervalo de confiança contém RR. Sem população e incidência adequadas, retorna screening_only ou inputs_incomplete, em vez de inventar casos. Não integra o pôster CMAS atual e não permite somar desfechos/estudos sobrepostos como casos distintos.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\risk.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| __future__ | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| aermod_post | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| io_utils | Módulo autoral local; sua ficha está neste relatório. |
| math | Funções matemáticas escalares. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- paths['population'] — chamada pd.read_csv, linha 391.
- paths['functions'] — chamada pd.read_csv, linha 392.
- paths['daily_override'] — chamada pd.read_csv, linha 420.
- paths['costs'] — chamada pd.read_csv, linha 527.

**Saídas.**

- {input_dir}/saude_populacao_zonas.csv — chamada .to_csv, linha 147.
- {input_dir}/saude_funcoes_cr_incidencia.csv — chamada .to_csv, linha 149.
- {input_dir}/saude_custos_internacoes.csv — chamada .to_csv, linha 151.
- {input_dir}/saude_pm25_diario_zonas.csv — chamada .to_csv, linha 156.
- {input_dir}/LEIA-ME_impacto_saude.txt — chamada notes.write_text, linha 158.
- {out_root}/05_impacto_saude/exposicao_pm25_anual_por_zona.csv — chamada .to_csv, linha 389.
- {out_root}/05_impacto_saude/populacao_saude_utilizada.csv — chamada pop.to_csv, linha 409.
- {out_root}/05_impacto_saude/impacto_saude_indicadores_exposicao_zona.csv — chamada .to_csv, linha 413.
- {out_root}/05_impacto_saude/impacto_saude_fracao_atribuivel_cronica_zona_endpoint.csv — chamada chronic_af.to_csv, linha 418.
- {out_root}/05_impacto_saude/exposicao_pm25_diaria_por_zona.csv — chamada daily.to_csv, linha 426.
- {out_root}/05_impacto_saude/impacto_saude_fracao_atribuivel_aguda_zona_endpoint.csv — chamada acute_af.to_csv, linha 430.
- {out_root}/05_impacto_saude/impacto_saude_cronico_por_zona_funcao.csv — chamada cr.to_csv, linha 483.
- Mais 7 referências na ficha HTML e no inventário JSON.

**Campos e chaves lidos.**

- z: health_delta_cf_ugm3, health_pm25_annual_ugm3, zone_index.
- d: PM25_UGM3, date, delta_c, exposure, study.
- sb: ANNUAL_3YR.
- cand: ANNUAL_3YR.
- daily: PM25_UGM3, X, Y, date, zone_index.
- pts: X, Y.
- zones: geometry, zone_index.
- cp: zone_index.
- functions: exposure.
- f: age_group, cid, control_ugm3, endpoint, population_column, rr_high, rr_low, rr_per_10ug, study.
- paths: costs, daily_override, functions, population.
- pop: zone_index.
- fun: exposure.
- r: date, zone_index.
- summary_fun: exposure.
- cost_res: cases_avoidable, total_admissions, total_cost_brl.

**Campos e chaves gerados.**

- out: zone_name.
- d: PM25_UGM3, af_pct, baseline_cases, baseline_population, baseline_rate_per_100k, date, delta_c, notes.
- z: health_counterfactual_ugm3, health_delta_cf_ugm3, health_delta_pv_ugm3, health_exposure_source, health_monitor_cov_pct, health_person_ugm3_excess_cf, health_pm25_annual_ugm3, health_pop_above_cf, health_pop_above_pv, health_population_exposed, health_pv_annual_ugm3, health_zone_classified, zone_index.
- sb: ANNUAL_3YR.
- zg: zone_index.
- cp: zone_index.
- g: endpoint, study.
- pop: zone_index.
- daily: PM25_UGM3, date.
- byfun: exposure.
- cost_res: avoidable_cost_brl, total_admissions, total_cost_brl.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| _beta(rr) | 99-101 | Chamadas efetivas: float, math.log Retorno: math.log(rr) / 10.0 if rr > 0 else np.nan. |
| _rr_ci_valid(rr, lo, hi) | 104-108 | Chamadas efetivas: float Retorno: float(lo) <= float(rr) <= float(hi) and float(lo) > 0 and (float(hi) > 0), False. |
| _zone_name_field(zones) | 111-115 | Organiza parâmetros, expressões ou retorno sem chamada externa. Retorno: None, c. |
| _population_template(zones) | 118-125 | Chamadas efetivas: zones.copy, _zone_name_field, pd.DataFrame, .astype Retorno: out. |
| _incidence_template() | 128-136 | Chamadas efetivas: pd.DataFrame Retorno: d. |
| write_health_templates(input_dir: Path, zones) | 139-168 | grava produtos Retorno: {'population': pop_path, 'functions': cr_path, 'costs': cost_path, 'daily_override': daily_override, 'notes': notes}. |
| build_hybrid_annual_exposure(zones_pm25, station_buffers=None) | 171-207 | Chamadas efetivas: zones_pm25.copy, np.where, .copy, pd.to_numeric, sb.geometry.union_all, float, z.iterrows, .notna Retorno: z, z. |
| build_daily_zone_model(post_path: Path, zones) | 210-250 | Chamadas efetivas: read_post_daily_cached, .copy, gpd.GeoDataFrame, zg.itertuples, daily.merge, pd.to_datetime, .rename, pd.DataFrame Retorno: out, pd.DataFrame(). |
| build_health_screening_indicators(exposure, census_zone_population=None) | 253-295 | Chamadas efetivas: exposure.copy, pd.to_numeric, float, .clip, np.where, census_zone_population.copy, z.merge, z.get Retorno: z. |
| build_chronic_af_screening(screening_zones, functions) | 298-324 | Chamadas efetivas: .copy, chronic.iterrows, pd.DataFrame, .agg, screening_zones.iterrows, float, _beta, pd.isna Retorno: d.groupby(['zone_index', 'endpoint'], as_index=False).agg(mean_af_pct=('attributable_fraction_pct', 'mean'), min_af_pct=('attributable_fraction_pct', 'min'), max_af_pct=('attributable_fraction_pct', '. |
| build_acute_af_screening(daily, functions) | 327-358 | Chamadas efetivas: .copy, acute.iterrows, pd.concat, .agg, pd.DataFrame, pd.to_numeric, d.dropna, .clip Retorno: d.groupby(['zone_index', 'endpoint'], as_index=False).agg(mean_daily_af_pct=('mean_daily_af_pct', 'mean'), max_daily_af_pct=('max_daily_af_pct', 'max'), days_above_control=('days_above_control', 'max'. |
| _baseline_rate(row) | 361-369 | Chamadas efetivas: pd.notna, float, pd.to_numeric, pd.Series, row.get Retorno: np.nan, float(rate). |
| _calc_cases(delta_c, baseline_rate_per_100k, population, rr, rr_low=np.nan, rr_high=np.nan, period_factor=1.0) | 372-381 | Chamadas efetivas: _beta, _rr_ci_valid, np.exp Retorno: (cases, low, high, beta). |
| run_health_risk_module(zones_pm25, out_root: Path, station_buffers=None, pm25_post_path=None, census_zone_population=None) | 384-538 | lê dados; grava produtos Retorno: {'status': 'ok', 'summary': out_dir / 'impacto_saude_resumo_endpoint.csv', 'function_summary': out_dir / 'impacto_saude_resumo_por_funcao.csv', 'zone_summary': zone_summary_path, **screening_meta, **p. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/risk.py, linhas 100-106.

```python
    rr=float(rr)
    return math.log(rr)/10.0 if rr>0 else np.nan

# Rr ci valid
def _rr_ci_valid(rr, lo, hi):
    try:
        return float(lo) <= float(rr) <= float(hi) and float(lo)>0 and float(hi)>0
```

Logaritmo natural. Na função de risco, β=ln(RR)/10 converte um risco relativo por 10 µg/m³ para a escala de 1 µg/m³.

Trecho de codigo/risk.py, linhas 203-209.

```python
            continue
        val=float(np.average(cand["ANNUAL_3YR"].to_numpy(dtype=float),weights=w.to_numpy(dtype=float))) if w.sum()>0 else float(cand["ANNUAL_3YR"].mean())
        z.at[idx,"health_pm25_annual_ugm3"]=val
        z.at[idx,"health_exposure_source"]="monitoramento"
    return z

# Build daily zone model
```

Média com ou sem pesos. As unidades do resultado são as da variável antes de eventual normalização.

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Cálculos a observar nesta rotina.**

- log: Logaritmo natural. Na função de risco, β=ln(RR)/10 converte um risco relativo por 10 µg/m³ para a escala de 1 µg/m³.
- average: Média com ou sem pesos. As unidades do resultado são as da variável antes de eventual normalização.
- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- exp: Função exponencial. No módulo sanitário, a fração potencialmente evitável é 1−exp(−β×ΔC), condicionada à função concentração-resposta e ao contrafactual.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/rodar_revisao_pos_banca.py

Atualização explícita dos produtos científicos; não edita o seminário entregue.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\rodar_revisao_pos_banca.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| argparse | Parâmetros fornecidos ao iniciar o programa. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| subprocess | Chamada de outros programas e verificação de seus resultados de execução. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/rodar_revisao_pos_banca.py, linhas 8-16.

```python
"""Atualização explícita dos produtos científicos; não edita o seminário entregue."""
# INÍCIO DOS CAMINHOS PORTÁTEIS
import sys as _cp_sys
from pathlib import Path as _cp_Path
_cp_file = _cp_Path(globals().get('__file__', _cp_Path.cwd() / 'codigo' / 'script.py')).resolve()
for _cp_parent in [_cp_file.parent, *_cp_file.parents]:
    _cp_code = _cp_parent if (_cp_parent / 'caminhos_congonhas.py').is_file() else _cp_parent / 'codigo'
    if (_cp_code / 'caminhos_congonhas.py').is_file():
        if str(_cp_code) not in _cp_sys.path: _cp_sys.path.insert(0, str(_cp_code))
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/rosa_vento_seletor.py

Rosa meteorológica da entrada WRF/AERMET com seleção angular independente.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\rosa_vento_seletor.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| functools | Composição, cache e auxiliares de funções. |
| matplotlib.patches | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/16_revisao_pos_banca/vento/calendario_vento_horario.csv — chamada pd.read_csv, linha 37.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- c: direction_idx.
- ax.spines: polar.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| histogram() | 35-44 | lê dados Retorno: (h, 100 * h / len(v)). |
| draw(ax, selected=None, fontsize=5.5) | 47-73 | Chamadas efetivas: histogram, ax.set_theta_zero_location, ax.set_theta_direction, ax.set_facecolor, ax.set_ylim, range, ax.set_xticks, enumerate Retorno: freq. |
| add_to_figure(fig, selected, top=0.1) | 76-83 | Chamadas efetivas: fig.add_axes, ax.set_gid, draw, ax.set_yticklabels, fig.legend, legend.set_gid, Patch Retorno: ax. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/rosa_vento_seletor.py, linhas 42-48.

```python
    h=np.zeros((12,6),dtype=int);np.add.at(h,(directions,speed),1)
    assert h.sum()==len(v)
    return h,100*h/len(v)

# Draw
def draw(ax,selected=None,fontsize=5.5):
    _,freq=histogram();ax.set_theta_zero_location('N');ax.set_theta_direction(-1)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/rosa_vento_seletor.py, linhas 49-55.

```python
    selected_idx=DIRS.index(selected) if selected in DIRS else None
    ax.set_facecolor('white');ax.set_ylim(0,np.ceil(freq.sum(axis=1).max()/5)*5)
    for i in range(12):
        lo=i*30-15;hi=i*30+15
        cuts=[lo,hi]
        if selected_idx is not None:
            for offset in [-360,0,360]:
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/sensibilidade_eolica_wg_scof.py

Cenario de um disturbio/hora, separado das entradas-base. Nao executa AERMOD.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\sensibilidade_eolica_wg_scof.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| collections | Estruturas de contagem, agrupamento e coleções auxiliares. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| openpyxl | Leitura/escrita de planilhas XLSX; não é o mecanismo do Excel aberto. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/14_auditoria_entradas/inventarios_wg_scof_extraidos.json — chamada .read_text, linha 42.
- E:/projeto/output/14_auditoria_entradas/revalidacao_final/fontes_correntes.json — chamada .read_text, linha 48.
- E:/projeto/output/12_houremiss/sensibilidade_WG_SCOF_1h/HOUREMIS-{pol}-WG-SCOF-2021-2023.EMI — chamada ep.open, linha 115.
- E:/projeto/output/12_houremiss/sensibilidade_WG_SCOF_1h/HOUREMIS-{pol}-WG-SCOF-2021-2023.EMI — chamada ep.read_bytes, linha 121.
- E:/projeto/houremiss/WRF_SAM.xlsx — chamada metpath.read_bytes, linha 124.

**Saídas.**

- E:/projeto/output/12_houremiss/sensibilidade_WG_SCOF_1h/HOUREMIS-{pol}-WG-SCOF-2021-2023.EMI — chamada ep.open, linha 106.
- E:/projeto/output/12_houremiss/sensibilidade_WG_SCOF_1h/Taxas_horarias_{pol}_g_s_m2.csv — chamada cp.open, linha 111.
- E:/projeto/output/12_houremiss/sensibilidade_WG_SCOF_1h/Massas_anuais.csv — chamada .open, linha 122.
- E:/projeto/output/12_houremiss/sensibilidade_WG_SCOF_1h/manifesto.json — chamada .write_text, linha 125.

**Campos e chaves lidos.**

- data: ANEXO 4 - Pré Inventário SCOF.xlsx, EDA WG - Inventário de Emissões - Amanda.xls.
- s: id, poluente.
- src: area_modelo_m2, taxa_nativa, taxa_total_g_s.
- wg: ARRASTE_OK, MOVIMENTAÇÃO_OK, RESUMO_OK.
- manifest: ustar_max_m_s.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| cell(rows, row, col) | 46-47 | Chamadas efetivas: dict Retorno: dict(dict(rows)[row])[col]. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/sensibilidade_eolica_wg_scof.py, linhas 65-71.

```python
for day,r in days.items(): monthly[day[:2]].append(r)
fpp = {k:1-sum(x>.254 for x in rr)/len(rr) for k,rr in monthly.items()}
rainfactor = np.array([fpp[k[:2]] for k in keys])
ustar = .053*gust
changes=[]; totals=[]; outputs=[]; parameters=[]
for pol,file,k,mc in [('PM10','PM10_Sources.xlsx',.5,13),('PM25','PM2-5_Sources.xlsx',.075,12)]:
    path=ROOT/'entrada_aermod'/file
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/sensibilidade_eolica_wg_scof.py, linhas 102-108.

```python
            mask=np.array([key[0]==year for key in keys]); factor=area*3600/1e6
            totals.append(dict(poluente=pol,id=sid,ano=year,base_t_ano=src['taxa_total_g_s']*31.536,erosao_t_ano=float(erosion[mask].sum()*factor),movimentacao_t_ano=movement*31.536,total_cenario_t_ano=float(rate[mask].sum()*factor)))
    matrix=np.array(rates).T
    ep=OUT/f'HOUREMIS-{pol}-WG-SCOF-2021-2023.EMI'
    with ep.open('w',encoding='ascii',newline='') as f:
        for key,rr in zip(keys,matrix):
            y,m,d,h=key
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/sincronizar_figuras_documentos.py

Substitui só os recursos gráficos; preserva texto, campos e dimensões Word.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\sincronizar_figuras_documentos.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| lxml | Consulta/edição XML, incluindo os componentes internos de DOCX, PPTX e SVG. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| posixpath | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| subprocess | Chamada de outros programas e verificação de seus resultados de execução. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- E:/projeto/output/11_integracao/nova_modelagem/figuras_seminario_manifesto.json — chamada .read_text, linha 38.
- E:/projeto/temp/qa_seminarios/svg_word/manifesto.json — chamada .read_text, linha 43.
- E:/projeto/output/09_projeto_dissertacao/seminarios_02/Projeto_Ricardo-Queiroz_{version}.docx — chamada ZipFile, linha 46.
- sources[key] — chamada source.read_bytes, linha 60.
- compatible['output'] — chamada svg.read_bytes, linha 67.

**Saídas.**

- E:/projeto/temp/{version}_figuras_sincronizadas.docx — chamada ZipFile, linha 71.
- E:/projeto/temp/qa_seminarios/figuras_documentos_30.json — chamada .write_text, linha 74.

**Campos e chaves lidos.**

- x: arquivo, codigo.
- NS: r.
- compatible: output, sha256.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 37-74 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/sincronizar_figuras_documentos.py, linhas 37-45.

```python
def run():
 manifest=json.loads((R/'output/11_integracao/nova_modelagem/figuras_seminario_manifesto.json').read_text(encoding='utf8'))
 sources={x['codigo']:Path(x['arquivo']) for x in manifest if x['arquivo']!='ORIGINAL'}

 aliases={'H1':'H3','I1':'I2'};report=[]
 subprocess.run([str(R/'codigo/.venv/Scripts/python.exe'),str(R/'codigo/svg_compativel_word.py')],check=True)
 compatible_sources=json.loads((R/'temp/qa_seminarios/svg_word/manifesto.json').read_text(encoding='utf8'))
 for version in ['Entrega','Leitura']:
  path=F/f'Projeto_Ricardo-Queiroz_{version}.docx';updates={};figures=[]
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/sincronizar_rateio_corrente.py

Propaga apenas massas revisadas; concentrações e geometrias são preservadas.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\sincronizar_rateio_corrente.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/config.DIRS['out']/13_rateio_emissoes/Resumo_zonas.csv — chamada pd.read_csv, linha 45.
- E:/projeto/config.DIRS['out']/13_rateio_emissoes/Balanco_fontes.csv — chamada pd.read_csv, linha 45.
- E:/projeto/config.DIRS['out']/14_auditoria_entradas/entrada_BPIP_7caracteres/alteracoes.json — chamada .read_text, linha 46.
- E:/projeto/config.DIRS['out']/13_rateio_emissoes/fontes_rateio_{pol}.gpkg — chamada gpd.read_file, linha 48.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{name}.gpkg [camada 'zoneamento'] — chamada gpd.read_file, linha 76.
- E:/projeto/config.DIRS['out']/06_censo_ibge/censo_populacao_por_zoneamento.csv — chamada pd.read_csv, linha 74.
- E:/projeto/config.DIRS['out']/15_auditoria_metodologica/auditoria_emi_252.json — chamada a.read_text, linha 84.

**Saídas.**

- E:/projeto/config.DIRS['out']/13_rateio_emissoes/fontes_rateio_{pol}.gpkg — chamada s.to_file, linha 57.
- E:/projeto/config.DIRS['out']/11_integracao/nova_modelagem/{name}.gpkg — chamada z.to_file, linha 66.
- p.with_suffix('.csv') — chamada .to_csv, linha 82.
- E:/projeto/temp/sincronizacao_p.name [camada 'zoneamento'] — chamada z.to_file, linha 81.
- E:/projeto/config.DIRS['out']/15_auditoria_metodologica/auditoria_emi_252.json — chamada a.write_text, linha 86.

**Campos e chaves lidos.**

- config.DIRS: out.
- s: massa, source_id.
- balance: poluente.
- summary: poluente.
- z: zone_index.

**Campos e chaves gerados.**

- s: dens_area, dens_linha, massa, source_id.
- v: status.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 43-87 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/sincronizar_rateio_corrente.py, linhas 43-51.

```python
def run():
    root=config.DIRS['out'];d=root/'13_rateio_emissoes';nova=root/'11_integracao/nova_modelagem'
    summary=pd.read_csv(d/'Resumo_zonas.csv');balance=pd.read_csv(d/'Balanco_fontes.csv')
    ids=json.loads((root/'14_auditoria_entradas/entrada_BPIP_7caracteres/alteracoes.json').read_text(encoding='utf8'))['mapping']
    for pol in ['PM10','PM25']:
        src=d/f'fontes_rateio_{pol}.gpkg';s=gpd.read_file(src)
        s['source_id']=s.source_id.map(lambda v:ids.get(v,v))
        mass=balance[balance.poluente.eq(pol)].set_index('id_fonte').massa_fonte_t_ano
        before=s.massa.copy();after=s.source_id.map(mass)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/source_apportionment.py

Calcula a atribuição e a curva ABC da etapa territorial anterior, selecionando receptor de maior P98 por zona e datas críticas de ALL e recuperando os grupos nessas mesmas datas. Ordena parcelas exclusivas e mantém grupos sobrepostos separados. Esse módulo não deve ser confundido com o resumo anual das regiões prioritárias ou a recuperação do evento ALL nos envelopes direcionais da etapa atual.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\source_apportionment.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| __future__ | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| aermod_post | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| folium | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| methodology_rules | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| standards | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| time | Medição de duração e acompanhamento de tarefas. |


**Entradas.**

- {out_html} — chamada out_html.read_text, linha 376.

**Saídas.**

- {out_html} — chamada out_html.write_text, linha 584.
- {out_html} — chamada m.save, linha 535.

**Campos e chaves lidos.**

- cand: P98_MODEL.
- critical_receptors: X, Y, zone_index.
- data: date.
- sub: ABC_CLASS, ABC_SHARE_PCT, ALL_CRIT_MEAN, CONC, GROUP_CRIT_MEAN, emission_gs.
- dates: ALL_CONC, X, Y, date, zone_index.
- recs: X, Y, zone_index.
- s: ABC_CUM_PCT, ALL_ANNUAL_MEAN, ALL_CRIT_MEAN, GROUP_ANNUAL_MEAN, GROUP_CRIT_MEAN.
- d: ALL_CRIT_MEAN, GROUP_CRIT_MEAN, emission_gs, group_id, overlap_group.
- sub.loc: ABC_SHARE_PCT, GROUP_CRIT_MEAN, emission_gs, group_name.
- g: ABC_SHARE_PCT, MEAN_GROUP_CONC, emission_gs.
- pri: ABC_CLASS, ABC_SHARE_PCT, emission_gs, group_id, group_name.
- a: GROUP_CRIT_MEAN.

**Campos e chaves gerados.**

- data: year.
- s: ANNUAL_CONTRIBUTION_PCT, CONTRIBUTION_PCT, group_id, group_name, overlap_group, post_file, source_averaging.
- d: ALL_CRIT_MEAN, GROUP_CRIT_MEAN, emission_gs, group_id, group_name.
- sub: ABC_CLASS, ABC_CUM_PCT, ABC_RANK, ABC_SHARE_PCT, ALL_SHARE_PCT, EMISSION_ZONE_TOTAL_GS, GROUP_CRIT_MEAN, GROUP_SUM_TO_ALL_PCT.
- g: ABC_CLASS, ABC_CUM_PCT, ABC_RANK, ABC_SHARE_PCT, MEAN_GROUP_CONC.
- zz: zona_nome.
- datasets: GLOBAL.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| group_from_post(path: Path, info=None) | 58-67 | Chamadas efetivas: canonical_post_group, str, inspect_pos_header, info.get Retorno: str(info.get('group') or path.stem), g. |
| select_zone_critical_receptors(zones, model_points, pollutant) | 70-89 | Chamadas efetivas: model_points.to_crs, zones.iterrows, pd.DataFrame, pd.to_numeric, vals.idxmax, rows.append, mp.geometry.distance, .sum Retorno: pd.DataFrame(rows). |
| critical_dates_all(all_post: Path, critical_receptors: pd.DataFrame, pollutant: str, percentile=0.98) | 92-113 | Chamadas efetivas: read_post_daily_cached, .copy, all_df.merge, data.groupby, pd.DataFrame, nearest_rank_percentile, hit.itertuples, pd.to_datetime Retorno: pd.DataFrame(rows), pd.DataFrame(). |
| source_apportionment_critical_days(post_dir: Path, pollutant: str, all_post: Path, zones, model_points) | 116-211 | Chamadas efetivas: print, select_zone_critical_receptors, critical_dates_all, .copy, read_post_daily_cached, .agg, set, discover_group_posts_any Retorno: (result, recs, dates), (pd.DataFrame(), recs, dates). |
| build_abc_analysis(contrib_df: pd.DataFrame, a_limit=None, b_limit=None) | 214-304 | Chamadas efetivas: float, contrib_df.copy, pd.to_numeric, .copy, d.groupby, pd.DataFrame, .agg, .reset_index Retorno: (abc, zone_summary, global_abc), (pd.DataFrame(), pd.DataFrame(), pd.DataFrame()). |
| build_emission_abc_by_zone(allocations: pd.DataFrame, a_limit=None, b_limit=None) | 307-367 | Chamadas efetivas: float, allocations.copy, pd.to_numeric, .copy, .astype, .map, .sum, agg.groupby Retorno: (abc, summary, glob), (pd.DataFrame(), pd.DataFrame(), pd.DataFrame()). |
| write_emission_abc_dashboard(abc_df: pd.DataFrame, global_abc: pd.DataFrame, out_html: Path, pollutant: str, title: str  /  None=None) | 370-384 | lê dados; grava produtos |
| build_abc_reduction_scenarios(abc_df: pd.DataFrame, reductions=None) | 387-422 | Chamadas efetivas: abc_df.copy, pd.to_numeric, d.groupby, pd.DataFrame, getattr, .copy, .any, float Retorno: pd.DataFrame(rows), pd.DataFrame(). |
| _abc_svg(sub: pd.DataFrame, width=300, height=95) | 425-444 | Chamadas efetivas: .copy, max, np.linspace, .join, len, sub.sort_values, .to_numpy, zip Retorno: f"<svg width='{width}' height='{height}' viewBox='0 0 {width} {height}' style='background:#fafafa;border:1px solid #e5e7eb'><line x1='{pad}' y1='{y80:.1f}' x2='{width - pad}' y2='{y80:.1f}' stroke='#d. |
| write_source_interactive_map(zones, contrib_df, municipality, out_html: Path, title='Source apportionment', abc_df=None, abc_summary=None) | 447-535 | grava produtos |
| write_abc_dashboard(abc_df: pd.DataFrame, global_abc: pd.DataFrame, out_html: Path, pollutant: str, title: str  /  None=None) | 538-584 | grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/source_apportionment.py, linhas 83-89.

```python
        vals = pd.to_numeric(cand["P98_MODEL"], errors="coerce")
        if vals.notna().sum() == 0:
            continue
        idx = vals.idxmax()
        rec = cand.loc[idx]
        rows.append({"zone_index": zid, "X": float(rec.X), "Y": float(rec.Y), "P98_MODEL": float(rec.P98_MODEL)})
    return pd.DataFrame(rows)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/source_apportionment.py, linhas 239-245.

```python
        sub = sub.sort_values(["GROUP_CRIT_MEAN", "group_name"], ascending=[False, True]).reset_index(drop=True)
        total_groups = float(sub["GROUP_CRIT_MEAN"].sum())
        all_mean = float(sub["ALL_CRIT_MEAN"].mean()) if sub["ALL_CRIT_MEAN"].notna().any() else np.nan
        if total_groups <= 0:
            continue
        sub["ABC_SHARE_PCT"] = 100.0 * sub["GROUP_CRIT_MEAN"] / total_groups
        sub["ABC_CUM_PCT"] = sub["ABC_SHARE_PCT"].cumsum()
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/standards.py

Standards. Processamento ou módulo de apoio. A organização passa por nearest_rank_percentile, annual_p98.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\standards.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| math | Funções matemáticas escalares. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| nearest_rank_percentile(values, p=0.98) | 57-72 | Chamadas efetivas: np.asarray, arr.sort, max, float, list, np.isfinite, min, int Retorno: float(arr[rank - 1]), np.nan. |
| annual_p98(values) | 75-88 | Chamadas efetivas: np.asarray, np.sort, float, list, len, np.isfinite Retorno: float(arr[-rank]), float('nan'). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/standards.py, linhas 57-65.

```python
def nearest_rank_percentile(values, p=0.98):
    """Percentil por posto (nearest-rank), sem interpolação.

    Para n valores ordenados crescentemente, usa posição ceil(p*n), limitada a 1..n.
    Essa forma é mais próxima do procedimento de seleção por posto usado em métricas
    regulatórias do que a interpolação linear padrão de muitas bibliotecas.
    """
    import math
    import numpy as np
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/stations.py

Stations. Processamento ou módulo de apoio. A organização passa por _norm_col, detect_columns, load_station_file, expected_days_in_quarter, station_metrics_for_pollutant, load_all_station_metrics, station_yearly_metrics, read_station_coords, build_station_gdf, _pretty_station_name.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\stations.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| __future__ | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| calendar | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| io_utils | Módulo autoral local; sua ficha está neste relatório. |
| math | Funções matemáticas escalares. |
| methodology_rules | Módulo autoral local; sua ficha está neste relatório. |
| monitoramento_mma | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| standards | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- {path} — chamada pd.read_excel, linha 135.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- out: PM10, PM25, x_raw, y_raw.
- df: datetime.
- config.DIRS: qar.
- metrics: pollutant.
- mm: n_valid_hourly, station_id.
- coords0: station_id.
- net: _sid.
- coords: E, N.
- gdf: station_id.

**Campos e chaves gerados.**

- out: E, N, PM10, PM25, coord_swap_detected, station_id.
- result: n_valid_hourly.
- m: station_id.
- r: coord_match, station_id.
- net: _sid.
- gdf: station_name.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| _norm_col(c) | 61-62 | Chamadas efetivas: re.sub, .lower, str Retorno: re.sub('[^a-z0-9,.-]+', '', str(c).lower()). |
| detect_columns(df) | 65-70 | Chamadas efetivas: next, _norm_col, cols.items Retorno: (date_col, pm10_col, pm25_col). |
| load_station_file(path: Path) | 73-88 | lê dados Retorno: out, None. |
| expected_days_in_quarter(year, quarter) | 91-93 | Chamadas efetivas: list, sum, range, calendar.monthrange Retorno: sum((calendar.monthrange(year, m)[1] for m in months)). |
| station_metrics_for_pollutant(df: pd.DataFrame, pollutant: str) | 96-107 | Chamadas efetivas: daily_and_yearly, rolling_station_metrics, .to_dict, .mean, int, .sum, .groupby, hourly.notna Retorno: result, {'pollutant': pollutant, 'n_valid_hourly': 0, 'years_valid': '', 'P98_3YR': np.nan, 'ANNUAL_3YR': np.nan, 'n_design_years': 0}. |
| load_all_station_metrics(qar_dir: Path) | 110-126 | Chamadas efetivas: config.DIRS.get, station_frames.items, regional.exists, load_network, sorted, pd.DataFrame, .resolve, .glob Retorno: (pd.DataFrame(rows), station_frames). |
| station_yearly_metrics(station_frames: dict) | 129-131 | Chamadas efetivas: all_tables Retorno: all_tables(station_frames)[0]. |
| read_station_coords(path: Path) | 134-158 | lê dados Retorno: out. |
| build_station_gdf(metrics: pd.DataFrame, coord_path: Path, kmz_path: Path  /  None=None) | 161-224 | Chamadas efetivas: read_station_coords, .copy, sorted, .tolist, pd.DataFrame, gpd.GeoDataFrame, .map, .unique Retorno: (gdf, unresolved), (gpd.GeoDataFrame(columns=['station_id', 'geometry'], geometry='geometry', crs=config.CRS_PROJECT), unresolved). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/stations.py, linhas 92-98.

```python
    months = list(range((quarter - 1) * 3 + 1, (quarter - 1) * 3 + 4))
    return sum(calendar.monthrange(year, m)[1] for m in months)

# Station metrics for pollutant
def station_metrics_for_pollutant(df: pd.DataFrame, pollutant: str):
    """MMA 2020, Quadro 7; triênio recente explícito, sem saltar lacunas."""
    from monitoramento_mma import daily_and_yearly
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/stations.py, linhas 99-105.

```python
    from methodology_rules import rolling_station_metrics
    if pollutant not in df or df[pollutant].notna().sum()==0:
        return {"pollutant":pollutant,"n_valid_hourly":0,"years_valid":"","P98_3YR":np.nan,"ANNUAL_3YR":np.nan,"n_design_years":0}
    _,yearly,_=daily_and_yearly(df,pollutant)
    roll=rolling_station_metrics(yearly,2017,2025)
    result=roll[roll.end_year.eq(2025)].iloc[0].to_dict()
    hourly=df.assign(datetime=df.datetime.dt.floor('h')).groupby('datetime')[pollutant].mean()
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/svg_compativel_word.py

Mantém as espessuras finas ao converter SVG para PDF no Word.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\svg_compativel_word.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| copy | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| xml.etree | Leitura/edição de XML de projetos e documentos. |


**Entradas.**

- E:/projeto/temp/qa_seminarios/svg_word/manifesto.json — chamada manifest.read_text, linha 73.
- E:/projeto/output/11_integracao/nova_modelagem/figuras_seminario_manifesto.json — chamada .read_text, linha 74.
- Path(item['arquivo']).with_suffix('.svg') — chamada source.read_bytes, linha 77.

**Saídas.**

- E:/projeto/temp/qa_seminarios/svg_word/manifesto.json — chamada manifest.write_text, linha 81.

**Campos e chaves lidos.**

- style: stroke-opacity.
- item: arquivo.
- previous: output.

**Campos e chaves gerados.**

- style: stroke.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| polygon_path(poly) | 35-37 | Chamadas efetivas: .join, ring Retorno: ' '.join((ring(v.coords) for v in [poly.exterior, *poly.interiors])), 'M ' + ' L '.join((f'{x:.7f} {y:.7f}' for x, y in coords)) + ' z'. |
| convert(source, target) | 40-68 | Chamadas efetivas: E.parse, d.getroot, list, root.iter, dict, style.get, float, p.get Retorno: count. |
| run() | 71-82 | lê dados; grava produtos Retorno: records. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/svg_compativel_word.py, linhas 35-43.

```python
def polygon_path(poly):
 def ring(coords):return 'M '+' L '.join(f'{x:.7f} {y:.7f}' for x,y in coords)+' z'
 return ' '.join(ring(v.coords) for v in [poly.exterior,*poly.interiors])

# Convert
def convert(source,target):
 d=E.parse(source);root=d.getroot();parents={x:p for p in root.iter() for x in p};count=0
 for p in list(root.iter()):
  if p.tag.rsplit('}',1)[-1]!='path':continue
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/test_absolute_classification.py

Test absolute classification. Conferência/teste. A organização passa por allocation, test_strict_boundaries_and_missing_zone, test_annualization_and_hours, test_sum_sources_of_same_group_inside_each_zone, test_reject_unknown_pollutant_bad_data_and_unsubstantiated_actual, test_empty_inventory_does_not_crash, test_unidentified_sources_are_not_an_invented_major_group, test_all_six_priorities_and_missing, test_period_metrics_compare_every_stage_strictly.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\projeto\codigo\test_absolute_classification.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| methodology_rules | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| standards | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| unittest | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- z.loc: emission_max_group_tpy, emission_total_tpy.

**Campos e chaves gerados.**

- a: annual_hours, emission_gs, group_id, zone_index.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| AbsoluteClassificationTests() | 30-97 | Chamadas efetivas: pd.DataFrame, group_mass_classes, self.assertEqual, self.allocation, self.assertAlmostEqual, self.assertTrue, self.assertFalse, range Retorno: pd.DataFrame({'zone_index': range(len(masses)), 'group_id': 'G', 'emission_gs': np.asarray(masses) / 31.536}). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/test_absolute_classification.py, linhas 31-39.

```python
    def allocation(self, masses):
        return pd.DataFrame({'zone_index':range(len(masses)), 'group_id':'G',
                             'emission_gs':np.asarray(masses)/31.536})

    def test_strict_boundaries_and_missing_zone(self):
        z,g=group_mass_classes(self.allocation([0,3,5,100,100.001]),range(6),'PM10')
        self.assertEqual(z.emission_class.tolist(),['Sem emissão alocada','Minoritária',
            'Minoritária','Intermediária','Majoritária','Sem emissão alocada'])
        z,_=group_mass_classes(self.allocation([3,3.001]),range(2),'PM25')
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/test_alocacao_territorial_emissoes.py

Test alocacao territorial emissoes. Conferência/teste. A organização passa por zones, test_area_and_volume, test_line_with_external_fraction, test_overlap_not_duplicated, test_point_boundary_pending, test_line_on_shared_boundary, test_oblique_line_closure_large_coordinates, test_point_visual_polygon_is_not_footprint, test_volume_without_footprint_stays_pending, test_total_of_two_groups_is_high.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\projeto\codigo\test_alocacao_territorial_emissoes.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| alocacao_territorial_emissoes | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| unittest | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| RateioTests() | 28-63 | Chamadas efetivas: gpd.GeoDataFrame, self.zones, partition, self.assertEqual, self.assertAlmostEqual, pd.Series, geometry_for_allocation, self.assertIsNone Retorno: gpd.GeoDataFrame(geometry=geoms, crs=31983). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/test_alocacao_territorial_emissoes.py, linhas 40-46.

```python
        p,o,a,t=partition(box(0,0,100,10),z,'área')
        self.assertAlmostEqual(sum(f for _,f,_ in p),.8);self.assertAlmostEqual(a,.2)
    def test_point_boundary_pending(self):
        z=self.zones([box(0,0,50,10),box(50,0,100,10)])
        self.assertEqual(partition(Point(50,5),z,'ponto')[:3],([],0.,1.))
    def test_line_on_shared_boundary(self):
        z=self.zones([box(0,0,50,10),box(50,0,100,10)])
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Trecho de codigo/test_alocacao_territorial_emissoes.py, linhas 51-57.

```python
        p,o,a,t=partition(LineString([(600000.123,7730001.111),(600099.987,7730087.678)]),z,'comprimento')
        self.assertAlmostEqual(sum(f for _,f,_ in p)+o+a,1,places=12)
    def test_point_visual_polygon_is_not_footprint(self):
        s=pd.Series({'source_type':'POINT','geometry':box(0,0,10,10)})
        geom,basis=geometry_for_allocation(s,{'Num_Coords':1,'X1':5,'Y1':5})
        self.assertEqual(geom,Point(5,5));self.assertEqual(basis,'ponto')
    def test_volume_without_footprint_stays_pending(self):
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/test_auditoria_consolidada.py

Test auditoria consolidada. Conferência/teste. A organização passa por test_epa_table_boundaries, test_population_overlap_is_pending_not_duplicated, test_hour_count_refers_to_selected_triennium, test_fully_overlapped_zone_is_missing_population_not_zero.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\projeto\codigo\test_auditoria_consolidada.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| censo_ibge | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| monitoramento_mma | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| standards | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| unittest | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- .loc: POP_TOTAL.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| AuditRegression() | 30-57 | Chamadas efetivas: self.assertTrue, gpd.GeoDataFrame, allocate_population_to_zones, self.assertAlmostEqual, pd.DataFrame, self.assertEqual, np.isnan, p.POP_TOTAL.sum |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/test_auditoria_consolidada.py, linhas 39-45.

```python
        p,a=allocate_population_to_zones(s,z,['POP_TOTAL'])
        self.assertAlmostEqual(p.POP_TOTAL.sum(),70)
        self.assertAlmostEqual(a.POP_TOTAL_ambiguous.sum(),20)
        self.assertAlmostEqual(a.POP_TOTAL_outside.sum(),10)
        self.assertAlmostEqual(a.balance_error.max(),0)

    def test_hour_count_refers_to_selected_triennium(self):
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/test_cenario_geral.py

Test cenario geral. Conferência/teste. A organização passa por test_peak_uses_full_valid_calendar_and_first_tie, test_no_valid_period_is_not_a_zero_concentration.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\projeto\codigo\test_cenario_geral.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| cenario_geral_pos_banca | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| unittest | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| GeneralScenarioTests() | 27-37 | Chamadas efetivas: np.array, peak_from_valid, np.testing.assert_array_equal, self.assertRaises |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/test_cenario_geral.py, linhas 28-36.

```python
    def test_peak_uses_full_valid_calendar_and_first_tie(self):
        values=np.array([[999,999],[5,8],[7,8],[6,20.]])
        c,t=peak_from_valid(values,[21010101,21010102,21010103,21010104],[False,True,True,True])
        np.testing.assert_array_equal(c,[7,20])
        np.testing.assert_array_equal(t,[21010103,21010104])
        c,t=peak_from_valid(values,[21010101,21010102,21010103,21010104],[False,True,True,False])
        np.testing.assert_array_equal(t,[21010103,21010102])

    def test_no_valid_period_is_not_a_zero_concentration(self):
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/test_complementacoes_20261106.py

Test complementacoes 20261106. Conferência/teste. A organização passa por test_meteorological_directions_and_boundaries, test_percentile_boundaries_are_right_closed, test_ties_do_not_create_artificial_groups, test_associative_cut_on_known_step, test_single_class_is_not_reported_as_valid_cut.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\projeto\codigo\test_complementacoes_20261106.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| analises_direcionais_pos_banca | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| complementar_quintis_gestao | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| revisao_espacial_pos_banca | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| unittest | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| ComplementaryTests() | 28-39 | Chamadas efetivas: np.testing.assert_array_equal, np.arange, relative_quintile, np.testing.assert_allclose, self.assertEqual, binary_cut, self.assertTrue, sector8 |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/test_complementacoes_20261106.py, linhas 29-37.

```python
    def test_meteorological_directions_and_boundaries(self):
        np.testing.assert_array_equal(sector8([0,360,22.49,22.5,90,180,270,337.5,-1,np.nan]),[0,0,0,1,2,4,6,0,-1,-1])
    def test_percentile_boundaries_are_right_closed(self):
        x=np.arange(101);q,c=relative_quintile(x)
        np.testing.assert_allclose(c,[20,40,60,80]);np.testing.assert_array_equal(q[[20,40,60,80,81]],[1,2,3,4,5])
    def test_ties_do_not_create_artificial_groups(self):
        q,_=relative_quintile(np.zeros(50));self.assertEqual(len(set(q)),1)
    def test_associative_cut_on_known_step(self):
        x=np.arange(100);y=x>49;cut=binary_cut(x,y);self.assertEqual(cut,49.5);self.assertEqual(balanced_accuracy(y,x>cut),1)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/test_direcoes_perfis.py

Testes numéricos de seleção de eventos, agrupamentos e estação seca.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\projeto\codigo\test_direcoes_perfis.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| analisar_espacial_direcoes | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| perfis_concentracao_estacoes | Módulo autoral local; sua ficha está neste relatório. |
| post_amostragem | Módulo autoral local; sua ficha está neste relatório. |
| revisao_espacial_pos_banca | Módulo autoral local; sua ficha está neste relatório. |
| scipy.spatial.distance | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| tempfile | Arquivos temporários definidos pelo processamento. |
| unittest | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

- {directory}/01_GALL.POS — chamada p.write_text, linha 43.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| DirectionalProfileTests() | 33-61 | grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/test_direcoes_perfis.py, linhas 60-63.

```python
        x=np.array([[0,0],[1,0],[0,1],[10,10],[11,10],[10,11]],float);lab=np.array([1,1,1,2,2,2])
        self.assertAlmostEqual(silhouette_fast(cdist(x,x),lab),silhouette(x,lab),places=12)

if __name__=='__main__':unittest.main()
```

Matriz de distâncias entre observações. É usada no agrupamento, na silhouette ou na comparação entre centroides.

**Cálculos a observar nesta rotina.**

- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- cdist: Matriz de distâncias entre observações. É usada no agrupamento, na silhouette ou na comparação entre centroides.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/test_integracao_metodologica.py

Test integracao metodologica. Conferência/teste. A organização passa por test_group_mass_sums_before_threshold, test_missing_model_year_not_replaced, test_missing_quarter_invalid, test_duplicate_model_date_rejected, test_coverage_union_and_small_bad_overlap, test_portable_roundtrip.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\projeto\codigo\test_integracao_metodologica.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| methodology_rules | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| tempfile | Arquivos temporários definidos pelo processamento. |
| unittest | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| vector_portable | Módulo autoral local; sua ficha está neste relatório. |
| zone_analysis | Módulo autoral local; sua ficha está neste relatório. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- z.loc: emission_class, emission_high, emission_max_group_tpy, emission_total_tpy.
- a: VALID_YEAR, emission_gs.
- z: test_text.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| IntegrationTests() | 35-72 | Chamadas efetivas: pd.DataFrame, group_mass_classes, self.assertAlmostEqual, self.assertTrue, self.assertEqual, model_annual_metrics, model_period_metrics, self.assertFalse |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/test_integracao_metodologica.py, linhas 42-48.

```python
        self.assertEqual(z.loc[3,'emission_class'],'Sem emissão alocada')
        self.assertAlmostEqual(g.emission_gs.sum(),a.emission_gs.sum())
    def test_missing_model_year_not_replaced(self):
        d=pd.DataFrame({'X':0.,'Y':0.,'date':pd.date_range('2023-01-01','2023-12-31'),'CONC':2.})
        a=model_annual_metrics(d)
        self.assertTrue(a.VALID_YEAR.all())
        p=model_period_metrics(a,[2021,2022,2023],'PM10')
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/test_interpolacao_cartografica.py

Test interpolacao cartografica. Conferência/teste. A organização passa por test_linear_preserves_nodes_and_does_not_extrapolate, test_conama_annual_boundaries_inclusive.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\projeto\codigo\test_interpolacao_cartografica.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| scipy.interpolate | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| standards | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| unittest | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| InterpolationTests() | 27-39 | Chamadas efetivas: np.array, LinearNDInterpolator, np.testing.assert_allclose, self.assertAlmostEqual, self.assertTrue, f, float, np.isnan |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/test_interpolacao_cartografica.py, linhas 28-36.

```python
    def test_linear_preserves_nodes_and_does_not_extrapolate(self):
        xy=np.array([[0,0],[1000,0],[0,1000],[1000,1000]])
        v=np.array([5,15,25,35]);f=LinearNDInterpolator(xy,v)
        np.testing.assert_allclose(f(xy),v)
        self.assertAlmostEqual(float(f([[500,500]])[0]),20.)
        self.assertTrue(np.isnan(f([[2000,2000]])[0]))
    def test_conama_annual_boundaries_inclusive(self):
        for pol,expected in [('PM10',[15,20,30,35,40]),('PM25',[5,10,15,17,20])]:
            limits=[STANDARDS[pol][s]['ANNUAL'] for s in STAGE_ORDER]
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/test_inventario_anual.py

Test inventario anual. Conferência/teste. A organização passa por test_mixed_geometry_preserves_area, test_ids, test_annual_mass_not_annualized_twice, test_known_high_not_masked_by_unknown.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\projeto\codigo\test_inventario_anual.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| aermod_sources | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| methodology_rules | Módulo autoral local; sua ficha está neste relatório. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| unittest | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- m.loc: emission_class, emission_high, emission_total_tpy.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| InventoryTests() | 30-53 | Chamadas efetivas: Polygon, _clean_geometry, self.assertEqual, pd.DataFrame, group_mass_classes, self.assertTrue, self.assertFalse, GeometryCollection |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/test_inventario_anual.py, linhas 31-39.

```python
    def test_mixed_geometry_preserves_area(self):
        poly=Polygon([(0,0),(2,0),(2,2),(0,2)])
        g=_clean_geometry(GeometryCollection([poly,LineString([(2,2),(3,3)])]))
        self.assertEqual(g.geom_type,'Polygon');self.assertEqual(g.area,4)

    def test_ids(self):
        for source,group in [('AEX01BCCA','CSN-CDP'),('VIA02CPI','CSN-PIR'),('CH01GER','GERDAU'),('VIA01VMF','VALE_FAB'),('VIA01VMV','VALE_VIG'),('AEX01FEP','FERRO'),('WG01','WGM')]:
            self.assertEqual(infer_primary_group_from_source(source),group)
        self.assertEqual(canonical_group('VALE S.A. - Mina de Fábrica'),'VALE_FAB')
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/test_maximas_24h.py

Test maximas 24h. Conferência/teste. A organização passa por test_maximum_not_concurrent_and_tie, test_duplicates_rejected.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\projeto\codigo\test_maximas_24h.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| mapa_maximas_24h | Módulo autoral local; sua ficha está neste relatório. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| unittest | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| TestFirst() | 26-35 | Chamadas efetivas: pd.DataFrame, first_high, self.assertEqual, r.CONC.tolist, r.N_DAYS.tolist, r.date.dt.day.tolist, self.assertRaises, pd.to_datetime |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/test_maximas_24h.py, linhas 27-35.

```python
    def test_maximum_not_concurrent_and_tie(self):
        d=pd.DataFrame({'X':[1,1,2,2,3],'Y':[0]*5,'date':pd.to_datetime(['2023-01-01','2023-01-02','2023-01-01','2023-01-02','2023-01-01']),'GRP':['ALL']*5,'N_HOURS':[24,24,24,24,18],'CONC':[9,1,2,10,999]})
        r=first_high(d)
        self.assertEqual(r.CONC.tolist(),[9,10])
        self.assertEqual(r.N_DAYS.tolist(),[2,2])
        self.assertEqual(r.date.dt.day.tolist(),[1,2])
    def test_duplicates_rejected(self):
        d=pd.DataFrame({'X':[1,1],'Y':[0,0],'date':pd.to_datetime(['2023-01-01']*2),'GRP':['ALL']*2,'N_HOURS':[24]*2,'CONC':[1,2]})
        with self.assertRaises(ValueError):first_high(d)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/test_medias_horarias.py

Test medias horarias. Conferência/teste. A organização passa por test_calm_hours_do_not_become_valid_zeros, test_zero_total_keeps_valid_calendar, test_impossible_calendar_rejected.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\projeto\codigo\test_medias_horarias.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| medias_horarias_verificadas | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| unittest | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| DailyMeans() | 26-35 | Chamadas efetivas: self.assertAlmostEqual, np.testing.assert_array_equal, float, model_daily_mean, self.assertRaises |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/test_medias_horarias.py, linhas 27-35.

```python
 def test_calm_hours_do_not_become_valid_zeros(self):
  self.assertAlmostEqual(float(model_daily_mean(120,20)),6)
  self.assertAlmostEqual(float(model_daily_mean(120,12)),120/18)
  self.assertAlmostEqual(float(model_daily_mean(120,24)),5)
 def test_zero_total_keeps_valid_calendar(self):
  np.testing.assert_array_equal(model_daily_mean([0,180,190],[24,18,19]),[0,10,10])
 def test_impossible_calendar_rejected(self):
  for n in [-1,25]:
   with self.assertRaises(ValueError):model_daily_mean(100,n)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/test_methodology_rules.py

Test methodology rules. Conferência/teste. A organização passa por test_abc_crossing_and_ties, test_abc_zero_and_invalid, annual, test_windows_start_2018_and_do_not_invent_2025, test_missing_year_not_skipped, test_duplicate_year_rejected, test_duplicate_hours_do_not_make_valid_day, test_model_mean_not_worst, test_model_complementary_missing_metrics_rejected, test_monitor_precedence_preserves_model_metrics.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\projeto\codigo\test_methodology_rules.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| methodology_rules | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| source_apportionment | Módulo autoral local; sua ficha está neste relatório. |
| stations | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| unittest | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| unittest.mock | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| zone_analysis | Módulo autoral local; sua ficha está neste relatório. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- out.loc: 2021-2023, 2022-2024, ANNUAL_3YR, status_PF.
- m: n_design_years, n_valid_hourly.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| RevisedMethodologyTests() | 36-112 | Chamadas efetivas: self.assertEqual, pd.DataFrame, rolling_station_metrics, self.assertTrue, self.annual, .set_index, station_metrics_for_pollutant, gpd.GeoDataFrame Retorno: pd.DataFrame({'station_id': ['s'] * 8, 'pollutant': ['PM10'] * 8, 'year': range(2017, 2025), 'valid_year': [True] * 8, 'annual_mean': [10.0] * 8, 'p98': [20.0] * 8}). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/test_methodology_rules.py, linhas 37-45.

```python
    def test_abc_crossing_and_ties(self):
        self.assertEqual(abc_classes([90,8,2]).tolist(),['A','B','C'])
        self.assertEqual(abc_classes([50,30,15,5]).tolist(),['A','A','B','C'])
        self.assertEqual(abc_classes([40,40,10,10]).tolist(),['A','A','B','B'])

    def test_abc_zero_and_invalid(self):
        self.assertEqual(abc_classes([0,0]).tolist(),['insuficiente']*2)
        with self.assertRaises(ValueError):abc_classes([2,-1])
        with self.assertRaises(ValueError):abc_classes([1,2])
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/test_monitoramento_mma.py

Test monitoramento mma. Conferência/teste. A organização passa por frame, test_three_quadrimesters_at_fifty_percent_are_valid, test_one_day_below_half_invalidates_year, test_duplicated_half_hours_do_not_double_count, test_leap_year_denominators_and_temperature_header, test_legacy_only_supplies_missing_whole_years, test_exploratory_severity_respects_both_durations_and_equal_limits.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\projeto\codigo\test_monitoramento_mma.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| auditar_series_e_gravidade | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| monitoramento_mma | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| unittest | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| unittest.mock | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- f: datetime.
- d.loc: PM10.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| MmaValidity() | 30-70 | Chamadas efetivas: pd.DataFrame, daily_and_yearly, self.assertTrue, self.assertEqual, self.frame, self.assertFalse, f.assign, severity Retorno: pd.DataFrame({'datetime': dates, 'PM10': 10.0, 'station_id': 's'}). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/test_monitoramento_mma.py, linhas 31-39.

```python
    def frame(self,year=2023):
        dates=[]
        for month in [1,5,9]:
            end=pd.Timestamp(year,month+3,1)+pd.offsets.MonthEnd(0)
            days=pd.date_range(pd.Timestamp(year,month,1),end)
            for day in days[:int(np.ceil(len(days)/2))]:dates.extend(pd.date_range(day,periods=16,freq='h'))
        return pd.DataFrame({'datetime':dates,'PM10':10.,'station_id':'s'})

    def test_three_quadrimesters_at_fifty_percent_are_valid(self):
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/test_network_history.py

Test network history. Conferência/teste. A organização passa por frame, test_leap_year_and_duplicate_hours, test_strict_exceedance_and_missing_not_zero, test_pi4_period_denominator, test_seasonal_calendar_not_only_observed_days, test_population_union_not_sum.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\projeto\codigo\test_network_history.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| network_history | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shapely.ops | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| unittest | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- s.loc: PI-2, PI-3, exceedance_pct, exceedances.
- r: annual_representative, calendar_days, exceedances, profile.
- full.loc: PF, PI-4, exceedances, valid_days.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| HistoricalNetworkTests() | 33-83 | Chamadas efetivas: pd.DataFrame, self.frame, daily_series, self.assertEqual, summarize, .set_index, self.assertFalse, self.assertTrue Retorno: pd.DataFrame({'datetime': pd.date_range(start, periods=hours, freq='h'), 'PM10': value}). |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/test_network_history.py, linhas 40-46.

```python
        self.assertEqual(len(d),366)
        self.assertEqual(d.valid_hours.sum(),16)
        self.assertEqual(d.valid_relatorio_MMA.sum(),1)
        self.assertEqual(d.valid_projeto.sum(),1)

    def test_strict_exceedance_and_missing_not_zero(self):
        d=daily_series(self.frame(value=100),'PM10',2024,2024)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/test_out_aermod_reader.py

Test out aermod reader. Conferência/teste. A organização passa por test_numeric_plt_mapping, test_exact_groups, test_boundaries, test_recover_only_documented_rounding.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\projeto\codigo\test_out_aermod_reader.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| groups | Módulo autoral local; sua ficha está neste relatório. |
| out_aermod_reader | Módulo autoral local; sua ficha está neste relatório. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| unittest | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- audit: zones_original_precision, zones_strict_export.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| Tests() | 30-52 | Chamadas efetivas: self.assertEqual, gpd.GeoDataFrame, pd.DataFrame, link_receptors, len, filename_identity, saturation_class, canonical_post_group |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/test_out_aermod_reader.py, linhas 31-39.

```python
    def test_numeric_plt_mapping(self):
        self.assertEqual(len(PLT_GROUPS),29)
        self.assertEqual(filename_identity('24H1G028.PLT'),('SCOF','24H'))
        self.assertEqual(filename_identity('AN00G025.PLT'),('VALE_FAB','ANNUAL'))
        self.assertEqual(filename_identity('01HGALL.PLT'),('ALL','1H'))
        self.assertEqual(filename_identity('01_GURB-VIA.POS'),('URB-VIA','1H'))
    def test_exact_groups(self):
        for gid in ['URB','URB-FER','URB-NUC','URB-VIA','SCOF','COOPERA','VALE_FAB']:
            self.assertEqual(canonical_post_group('24_G'+gid),gid)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/test_revisao_pos_banca.py

Verificações científicas de identidades e cenários, sem reproduzir mapas.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\projeto\codigo\test_revisao_pos_banca.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| revisao_espacial_pos_banca | Módulo autoral local; sua ficha está neste relatório. |
| scipy | Agrupamento, matrizes esparsas, distâncias, interpolação e estatísticas; conferir as chamadas na ficha. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| unittest | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| SpatialMethodsTests() | 28-40 | Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/test_revisao_pos_banca.py, linhas 35-41.

```python
 def test_local_statistics_reconstruct_global(self):
  xy=np.array([(i,j) for i in range(6) for j in range(6)]);w,ids,_=weights(xy,4);x=np.log1p(xy[:,0]+xy[:,1]);l=local_moran(x,ids,permutations=99)
  self.assertAlmostEqual(l.local_I.sum()/(len(x)-1),moran(x,w,99)['I'])
  self.assertTrue((l.q_FDR>=l.p_conditional-1e-12).all())
 def test_ties_are_not_artificially_split(self):
  q,_=relative_quartile(np.zeros(20));self.assertEqual(len(set(q)),1)

```

Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original.

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- log1p: Calcula ln(1+x), reduzindo assimetria e preservando zero. O resultado transformado não mantém a unidade física original.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/test_robustez_cientifica.py

Test robustez cientifica. Conferência/teste. A organização passa por test_bias_magnitude_and_association_are_distinct, test_unpaired_values_are_excluded, test_equal_rankings_and_ties, test_opposite_top_priorities.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\projeto\codigo\test_robustez_cientifica.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| avaliar_robustez_cientifica | Módulo autoral local; sua ficha está neste relatório. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| unittest | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- s: bias, correlation, jaccard, mae, n, reference_top_count, rmse, shared_top_count, spearman.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| ScientificComparisons() | 27-50 | Chamadas efetivas: agreement, self.assertEqual, self.assertAlmostEqual, self.assertIsNone, ranking_compare |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/test_robustez_cientifica.py, linhas 28-36.

```python
    def test_bias_magnitude_and_association_are_distinct(self):
        s=agreement([1,2,3],[3,4,5])
        self.assertEqual(s['n'],3)
        self.assertAlmostEqual(s['bias'],2)
        self.assertAlmostEqual(s['mae'],2)
        self.assertAlmostEqual(s['rmse'],2)
        self.assertAlmostEqual(s['correlation'],1)

    def test_unpaired_values_are_excluded(self):
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/transparencia_logos_poster.py

Transparência nativa de imagem do PowerPoint, sem redesenhar os logos.

**Papel.** Cartografia/apresentação. **Fonte inspecionada.** E:\projeto\codigo\transparencia_logos_poster.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| lxml | Consulta/edição XML, incluindo os componentes internos de DOCX, PPTX e SVG. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| posixpath | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- {path} — chamada zipfile.ZipFile, linha 34.
- E:/projeto/codigo/recursos_poster/assets/{f} — chamada .read_bytes, linha 38.

**Saídas.**

- {path} — chamada zipfile.ZipFile, linha 55.

**Campos e chaves lidos.**

- files: ppt/slides/_rels/slide1.xml.rels, ppt/slides/slide1.xml.
- N: a, r.

**Campos e chaves gerados.**

- files: ppt/slides/slide1.xml.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run(path) | 32-57 | lê dados |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/transparencia_logos_poster.py, linhas 32-40.

```python
def run(path):
    path=Path(path)
    with zipfile.ZipFile(path) as z: files={n:z.read(n) for n in z.namelist()}
    root=E.fromstring(files['ppt/slides/slide1.xml']);changed=[]
    rels={v.get('Id'):(v.get('Target').lstrip('/') if v.get('Target').startswith('/') else posixpath.normpath('ppt/slides/'+v.get('Target'))) for v in E.fromstring(files['ppt/slides/_rels/slide1.xml.rels'])}
    assets=Path(_cp_texto('codigo/recursos_poster/assets', 'posix'))
    names={hashlib.sha256((assets/f).read_bytes()).hexdigest():n for n,f in [('UFMG','logo_ufmg.png'),('SMARH','logo_smarh_original.png'),('GPAMA','logo_gpama.png'),('Mover','logo_o3_mover_transparente.png'),('CAPES','logo_capes.png'),('Atmosfera','logo_atmosfera_original.png')]}
    for pic in root.findall('.//p:pic',N):
        props=pic.find('p:nvPicPr/p:cNvPr',N)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/validar_documentacao_codigos.py

Validar documentacao codigos. Conferência/teste. A organização passa por corpo_normalizado, main, visit_Call.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\projeto\codigo\validar_documentacao_codigos.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| ast | Inspeção/transformação da sintaxe Python sem executar o processamento científico. |
| documentar_portabilidade | Módulo autoral local; sua ficha está neste relatório. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| importlib.util | Importação e identificação de versões das bibliotecas. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| subprocess | Chamada de outros programas e verificação de seus resultados de execução. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- info['raiz']/codigo/caminhos_projeto.json — chamada .read_text, linha 51.
- E:/projeto/temp/preparacao_20261114/produtos_preservados.json — chamada .read_text, linha 77.
- entry['path'] — chamada .read_bytes, linha 78.

**Saídas.**

- info['raiz']/temp/preparacao_20261114/configuracao_teste.json — chamada file.write_text, linha 72.
- info['raiz']/info['saida']/Validacao_codigos.json — chamada .write_text, linha 76.
- E:/projeto/temp/preparacao_20261114/validacao_portabilidade.json — chamada .write_text, linha 80.

**Campos e chaves lidos.**

- cfg: externos.
- info: raiz, saida.
- r: equivalencia_calculo.
- entry: path, sha256.

**Campos e chaves gerados.**

- testcfg: arquivos.
- report: posteres_preservados.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| corpo_normalizado(source, root, cfg) | 30-44 | grava produtos Retorno: ast.dump(tree, include_attributes=False), self.generic_visit(node). |
| main() | 47-80 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/validar_documentacao_codigos.py, linhas 74-80.

```python
        finally:os.environ.pop(env+'_CONFIG',None)
        report[key]={'scripts':len(rows),'verificacoes':rows,'equivalencias_confirmadas':sum(r['equivalencia_calculo'] is True for r in rows),'raiz_com_espaco':'OK','remapeamento_arquivo':'OK'}
        out=root/info['saida'];out.mkdir(exist_ok=True,parents=True);(out/'Validacao_codigos.json').write_text(json.dumps(report[key],ensure_ascii=False,indent=2),encoding='utf8')
    originals=json.loads(Path('E:/projeto/temp/preparacao_20261114/produtos_preservados.json').read_text('utf8'))
    for entry in originals:assert hashlib.sha256(Path(entry['path']).read_bytes()).hexdigest()==entry['sha256'],entry['path']
    report['posteres_preservados']=len(originals)
    Path('E:/projeto/temp/preparacao_20261114/validacao_portabilidade.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({k:({n:v for n,v in r.items() if n!='verificacoes'} if isinstance(r,dict) else r) for k,r in report.items()},ensure_ascii=True),flush=True)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/validar_massas_entrada.py

Releitura independente das entradas correntes e conservação dos HOUREMISS.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\projeto\codigo\validar_massas_entrada.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| collections | Estruturas de contagem, agrupamento e coleções auxiliares. |
| conciliar_nucleos_urbanos | Módulo autoral local; sua ficha está neste relatório. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| csv | Leitura/escrita de tabelas delimitadas com separador e codificação explícitos. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| hashlib | Assinaturas SHA-256 para identificar alterações de arquivos; não é validação do conteúdo científico. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| openpyxl | Leitura/escrita de planilhas XLSX; não é o mecanismo do Excel aberto. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- E:/projeto/output/14_auditoria_entradas/manifesto_correcao_20261022.json — chamada .read_text, linha 90.
- E:/projeto/output/12_houremiss/memoria_calculo.json — chamada .read_text, linha 91.
- E:/projeto/output/12_houremiss/calculos_horarios.npz — chamada np.load, linha 93.
- E:/projeto/output/14_auditoria_entradas/areas_houremiss.json — chamada .read_text, linha 100.
- E:/projeto/output/14_auditoria_entradas/conferencia_fontes.json — chamada .read_text, linha 101.
- E:/projeto/output/14_auditoria_entradas/entrada_BPIP_7caracteres/alteracoes.json — chamada id_file.read_text, linha 104.
- E:/projeto/output/14_auditoria_entradas/revisao_Vale_Fabrica_20261025/alteracoes_taxas.json — chamada .read_text, linha 106.
- E:/projeto/output/15_auditoria_metodologica/cenario_emissoes_ativo.json — chamada active_path.read_text, linha 109.
- E:/projeto/output/15_auditoria_metodologica/massas_9_fontes_cenario_252.csv — chamada .open, linha 113.
- E:/projeto/entrada_aermod/{filepol}_Sources.xlsx — chamada path.read_bytes, linha 117.
- E:/projeto/output/12_houremiss/HOUREMIS-{emipol}-2021-2023.EMI — chamada emi.open, linha 124.
- E:/projeto/output/12_houremiss/HOUREMIS-{emipol}-2021-2023.EMI — chamada emi.read_bytes, linha 152.
- Mais 1 referências na ficha HTML e no inventário JSON.

**Saídas.**

- E:/projeto/output/14_auditoria_entradas/revalidacao_final/fontes_correntes.json — chamada .write_text, linha 172.
- E:/projeto/output/14_auditoria_entradas/revalidacao_final/Massas_fontes_2021_2023.csv — chamada .open, linha 173.
- E:/projeto/output/14_auditoria_entradas/revalidacao_final/validacao_final.json — chamada .write_text, linha 182.

**Campos e chaves lidos.**

- mem: mapping.
- n: corrigido, keys, source_ids.
- r: id, poluente, status, taxa_nativa, taxa_total_g_s.
- f: edits, pol.
- x: id.
- report: arquivos, avisos, emi.
- manifest: arquivos.
- correction: source, total_g_s.
- v: ano, id, massa_t_ano, poluente.

**Campos e chaves gerados.**

- : status.
- report: avisos, cenario_executado_252, emi_consolidados.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| read_sources(path) | 60-84 | Chamadas efetivas: load_workbook, .iter_rows, w.close, str, int, float, ValueError, sum Retorno: result. |
| run() | 87-184 | lê dados; grava produtos Retorno: report. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/validar_massas_entrada.py, linhas 72-78.

```python
            pts=[(x-xy[0][0],y-xy[0][1]) for x,y in xy]
            area=abs(sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(pts,pts[1:]+pts[:1])))/2
        elif typ in ('LINE_AREA','LINE','RLINE'):
            length=sum(math.dist(a,b) for a,b in zip(xy,xy[1:]));area=length*float(r[12])
        elif typ=='AREA_CIRC':area=math.pi*float(r[6])**2
        elif typ=='AREA':area=float(r[12])*float(r[13])
        total=q*area if area is not None else q if typ in ('POINT','VOLUME','LINE_VOLUME') else None
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/validar_planilhas_ids7.py

Validar planilhas ids7. Conferência/teste. A organização passa por cells.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\projeto\codigo\validar_planilhas_ids7.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| math | Funções matemáticas escalares. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| xml.etree.ElementTree | Leitura/edição de XML de projetos e documentos. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- E:/projeto/output/14_auditoria_entradas/entrada_BPIP_7caracteres/alteracoes.json — chamada .read_text, linha 26.
- {path} — chamada zipfile.ZipFile, linha 30.

**Saídas.**

- E:/projeto/output/14_auditoria_entradas/entrada_BPIP_7caracteres/verificacao_planilhas.json — chamada .write_text, linha 62.

**Campos e chaves lidos.**

- p: files.
- f: edits, name, src.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| cells(path) | 29-43 | Chamadas efetivas: zipfile.ZipFile, .findall, z.namelist, c.get, c.find, .join, ET.fromstring, si.itertext Retorno: d. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/validar_planilhas_ids7.py, linhas 29-37.

```python
def cells(path):
 with zipfile.ZipFile(path) as z:
  strings=[]
  if 'xl/sharedStrings.xml' in z.namelist():
   strings=[''.join(si.itertext()) for si in ET.fromstring(z.read('xl/sharedStrings.xml'))]
  d={}
  for c in ET.fromstring(z.read('xl/worksheets/sheet1.xml')).findall('.//s:sheetData/s:row/s:c',ns):
   typ=c.get('t');v=c.find('s:v',ns);f=c.find('s:f',ns)
   if f is not None:val=('formula',f.text)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/vector_portable.py

I/O vetorial sem dependência de GDAL; preserva CRS e geometrias, sem alterar segurança.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\vector_portable.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| geopandas | Camadas vetoriais com referência espacial, reprojeção, recorte e interseção de geometrias. |
| io_utils | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| pyproj | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| shapefile | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| shapely | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shapely.geometry | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shapely.geometry.polygon | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| shapely.ops | Operações geométricas usadas nas áreas, distâncias, limites e relações espaciais. |
| sqlite3 | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| struct | Decodificação binária com tipos, tamanhos e ordem de bytes definidos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| xml.etree.ElementTree | Leitura/edição de XML de projetos e documentos. |


**Entradas.**

- {path} — chamada gpd.read_file, linha 44.
- path.with_suffix('.cpg') — chamada .read_text, linha 45.
- path.with_suffix('.prj') — chamada .read_text, linha 48.

**Saídas.**

- Path(path).with_suffix('.prj') — chamada .write_text, linha 118.
- Path(path).with_suffix('.cpg') — chamada .write_text, linha 119.
- Path(path).with_name(Path(path).stem + '_campos.csv') — chamada .to_csv, linha 120.

**Campos e chaves lidos.**

- r.__geo_interface__: features.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| read(path) | 38-70 | lê dados Retorno: gpd.GeoDataFrame.from_features(features, crs=CRS.from_wkt(path.with_suffix('.prj').read_text())), gpd.GeoDataFrame(geometry=geoms, crs=4326). |
| write_gpkg(gdf, path, layer='zoneamento') | 73-98 | Chamadas efetivas: Path, path.with_name, tmp.exists, gdf.crs.to_epsg, c.close, tmp.replace, FileExistsError, sqlite3.connect Retorno: '"' + s.replace('"', '""') + '"', 'INTEGER' if pd.api.types.is_integer_dtype(s) or pd.api.types.is_bool_dtype(s) else 'REAL' if pd.api.types.is_numeric_dtype(s) else 'TEXT'. |
| write_shp(gdf, path) | 101-120 | grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/vector_portable.py, linhas 38-46.

```python
def read(path):
    path=Path(path)
    if path.suffix.lower()=='.shp':
        try:
            import shapefile
        except ImportError:
            return gpd.read_file(path)
        enc=path.with_suffix('.cpg').read_text().strip() if path.with_suffix('.cpg').exists() else 'utf-8'
        with shapefile.Reader(str(path),encoding=enc) as r:
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/visualizar_abc_direcional.py

ABC consultável por região, evitando centenas de páginas estáticas.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\visualizar_abc_direcional.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| cartografia_apendices | Módulo autoral local; sua ficha está neste relatório. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| matplotlib | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| matplotlib.pyplot | Construção de gráficos, mapas, barras de cores e exportação vetorial/raster. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- Path(output) if output is not None else globals()['OUT']/'regioes_gerais.csv' if general else 'regioes_direcionais.csv' — chamada pd.read_csv, linha 49.
- Path(output) if output is not None else globals()['OUT']/ABC_contribuicoes_regioes.csv — chamada pd.read_csv, linha 100.
- Path(output) if output is not None else globals()['OUT']/index.html — chamada entry.read_text, linha 92.
- Path(output) if output is not None else globals()['OUT']/regioes_direcionais.csv — chamada pd.read_csv, linha 100.

**Saídas.**

- Path(output) if output is not None else globals()['OUT']/abc_por_regiao.html — chamada .write_text, linha 91.
- Path(output) if output is not None else globals()['OUT']/index.html — chamada entry.write_text, linha 94.
- Path(output) if output is not None else globals()['OUT']/figuras/{pol}_{period}_Contribuicoes_prioridades.{ext} — chamada fig.savefig, linha 112.

**Campos e chaves lidos.**

- regions: label, region_id, region_type.
- abc: region_id.
- values: ABC, cumulative_before_pct, group_name, share_pct.
- all_abc: label, period, pollutant, region_type.
- all_regions: area_km2, region_id.

**Campos e chaves gerados.**

- d: weighted.
- plot: Demais grupos.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run(output=None) | 45-114 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/visualizar_abc_direcional.py, linhas 104-110.

```python
            d=sub.merge(all_regions[['region_id','area_km2']],on='region_id',validate='many_to_one');d['weighted']=d.contribution*d.area_km2
            v=d.groupby(['direction','group_name']).weighted.sum().unstack(fill_value=0).reindex(DIRS)
            shares=100*v.div(v.sum(axis=1),axis=0);names=v.sum().nlargest(6).index.tolist();plot=shares[names].copy();plot['Demais grupos']=shares.drop(columns=names).sum(axis=1)
            fig,ax=plt.subplots(figsize=(9,4.4));left=np.zeros(8)
            for group,color in zip(plot.columns,['#247c96','#64ada8','#bdc77c','#d6b06a','#b77f79','#8c83aa','#d9e1de']):
                ax.barh(DIRS,plot[group],left=left,color=color,label=group);left+=plot[group].to_numpy()
            ax.set(xlim=(0,100),xlabel='Contribuição nas regiões prioritárias (%)',ylabel='Direção de origem do vento');ax.invert_yaxis();fig.subplots_adjust(left=.12,right=.99,top=.98,bottom=.31)
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/visualizar_perfis_grupos.py

Entrada compatível para o visualizador corrente em concentração absoluta.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\visualizar_perfis_grupos.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| perfis_concentracao_estacoes | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/visualizar_perfis_grupos.py, linhas 8-16.

```python
"""Entrada compatível para o visualizador corrente em concentração absoluta."""
# INÍCIO DOS CAMINHOS PORTÁTEIS
import sys as _cp_sys
from pathlib import Path as _cp_Path
_cp_file = _cp_Path(globals().get('__file__', _cp_Path.cwd() / 'codigo' / 'script.py')).resolve()
for _cp_parent in [_cp_file.parent, *_cp_file.parents]:
    _cp_code = _cp_parent if (_cp_parent / 'caminhos_congonhas.py').is_file() else _cp_parent / 'codigo'
    if (_cp_code / 'caminhos_congonhas.py').is_file():
        if str(_cp_code) not in _cp_sys.path: _cp_sys.path.insert(0, str(_cp_code))
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/webservice.py

Webservice. Processamento ou módulo de apoio. A organização passa por nice_name, map_tags, methodology_stage, scan_maps, filter_maps, run_worker, home, run_project, serve_output, view_html.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\webservice.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| __future__ | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| datetime | Calendários, datas e duração dos períodos avaliados. |
| flask | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| subprocess | Chamada de outros programas e verificação de seus resultados de execução. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| threading | Coordenação de execução e tarefas de apoio. |
| time | Medição de duração e acompanhamento de tarefas. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- value: keys.
- m: pretty, rel.
- STATE: last_run, log, running.
- section: description, title.

**Campos e chaves gerados.**

- STATE: last_run, log, running.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| nice_name(stem: str) | 268-273 | Chamadas efetivas: PRETTY.items, .replace, .join, k.lower, stem.lower, w.capitalize, parts.split, stem.replace Retorno: ' '.join((w.capitalize() for w in parts.split())), v. |
| map_tags(rel: str) | 276-286 | Chamadas efetivas: rel.lower, tags.append Retorno: tags or ['mapa']. |
| methodology_stage(rel: str) | 289-307 | Chamadas efetivas: rel.lower, name.startswith, any Retorno: 'etapa8', 'etapa3'. |
| scan_maps() | 310-339 | Chamadas efetivas: _SCAN_CACHE.update, OUTPUT_DIR.exists, max, list, sorted, time.time, _SCAN_CACHE.get, OUTPUT_DIR.rglob Retorno: maps, []. |
| filter_maps(items, cat, pol='all', scen='all') | 342-364 | Chamadas efetivas: list, cat.lower, any, .lower, methodology_stage Retorno: [m for m in out if c in m['rel'].lower() or c in m['pretty'].lower()], out. |
| run_worker() | 367-383 | Chamadas efetivas: .strftime, .append, str, subprocess.Popen, proc.wait, datetime.now, py.exists, line.rstrip |
| home() | 387-420 | Chamadas efetivas: APP.route, request.args.get, max, scan_maps, filter_maps, METHODOLOGY_SECTIONS.get, render_template_string, int Retorno: render_template_string(TEMPLATE, maps=filtered_page, n_maps=len(items), running=STATE['running'], last_run=STATE['last_run'], log_text='\n'.join(STATE['log'][-100:]), title=section['title'] if section. |
| run_project() | 424-427 | Chamadas efetivas: APP.route, redirect, .start, url_for, threading.Thread Retorno: redirect(url_for('home')). |
| serve_output(rel) | 431-435 | Chamadas efetivas: APP.route, send_from_directory, p.exists, abort Retorno: send_from_directory(OUTPUT_DIR, rel). |
| view_html(rel) | 439-445 | Chamadas efetivas: APP.route, abort, p.exists, p.suffix.lower, url_for Retorno: f"<!doctype html><html lang='pt-br'><head><meta charset='utf-8'><title>Mapa interativo</title>\n    <style>html,body{{margin:0;height:100%;background:#f5f9fc;font-family:Arial,sans-serif}} .top{{paddi. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/webservice.py, linhas 268-276.

```python
def nice_name(stem: str) -> str:
    for k, v in PRETTY.items():
        if k.lower() in stem.lower():
            return v
    parts = stem.replace("PM25", "MP2,5").replace("PM10", "MP10").replace("_", " ").replace("-", " ")
    return " ".join(w.capitalize() for w in parts.split())

# Map tags
def map_tags(rel: str):
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## codigo/zone_analysis.py

Zone analysis. Processamento ou módulo de apoio. A organização passa por _worst_status, _monitor_status_for_zone, _model_status_for_zone, classify_zones_attainment, threshold, classify_quadrants, fill_missing_by_neighbors, f.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\codigo\zone_analysis.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| __future__ | Dependência importada; conferir as chamadas efetivas abaixo e a instalação do ambiente correspondente. |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| config | Módulo autoral local; sua ficha está neste relatório. |
| numpy | Matrizes numéricas, máscaras de validade, transformações, percentis e estatísticas vetorizadas. |
| pandas | Leitura tabular, chaves de junção, agrupamento por período e exportação de indicadores. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| standards | Módulo autoral local; sua ficha está neste relatório. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- overlaps: station_id.
- valid_sb.loc: geometry.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| _worst_status(values) | 30-38 | Chamadas efetivas: set, str, pd.notna Retorno: 'sem_dado', 'nao_atendimento'. |
| _monitor_status_for_zone(geom, centroid, valid_sb, union_all, union_bad, status_col) | 41-104 | Chamadas efetivas: float, getattr, .copy, overlaps.geometry.covers, _worst_status, int, overlaps.geometry.intersection, pd.to_numeric Retorno: (cov_pct, bad_cov_pct, mon_status, mon_p98, mon_ann, n_monitor), (cov_pct, bad_cov_pct, mon_status, mon_p98, mon_ann, n_monitor). |
| _model_status_for_zone(cand, pollutant, scenario) | 107-137 | Chamadas efetivas: cand.copy, len, int, .mean, .max, getattr, pd.to_numeric, np.isfinite Retorno: (mod_status, n_model, n_bad, p98_mean, p98_max, ann_mean, ann_max). |
| classify_zones_attainment(zones, station_buffers, model_points, pollutant, scenario) | 140-231 | Chamadas efetivas: zones.copy, z.iterrows, .set_index, station_buffers.to_crs, .copy, model_points.to_crs, _monitor_status_for_zone, rows.append Retorno: z. |
| threshold(series, method='median', positive_only=False) | 234-248 | Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial. Retorno: np.nan, float(s.median()). |
| classify_quadrants(zones, emission_col, concentration_col, out_col='QUADRANTE', method=None, emission_high_col=None) | 251-286 | Chamadas efetivas: zones.copy, getattr, pd.to_numeric, threshold, z.apply, .any, float, pd.notna Retorno: z, 'alta_emissao_alta_concentracao'. |
| fill_missing_by_neighbors(zones, col, valid_values=None, max_iters=2) | 289-314 | Chamadas efetivas: zones.copy, range, miss.iterrows, .astype, vals.value_counts, .isna, .isin, neigh.touches Retorno: z. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de codigo/zone_analysis.py, linhas 96-102.

```python
            if np.isfinite(ww).any() and ww.sum() > 0:
                value = float(np.average(vv, weights=ww))
            else:
                value = float(np.mean(vv))
            if out_name == "p98":
                mon_p98 = value
            else:
```

Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.

Média com ou sem pesos. As unidades do resultado são as da variável antes de eventual normalização.

Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.

Trecho de codigo/zone_analysis.py, linhas 246-252.

```python
    if method == "q75":
        return float(s.quantile(0.75))
    raise ValueError(method)

# Classify quadrants
def classify_quadrants(zones, emission_col, concentration_col, out_col="QUADRANTE", method=None, emission_high_col=None):
    z = zones.copy()
```

Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

**Cálculos a observar nesta rotina.**

- sum: Soma no eixo definido. Em suportes sobrepostos, uma soma entre vizinhanças pode contar o mesmo local repetidas vezes.
- average: Média com ou sem pesos. As unidades do resultado são as da variável antes de eventual normalização.
- mean: Média no eixo explicitado. Não representa automaticamente média anual ou diária sem a seleção temporal correspondente.
- quantile: Quantil da amostra fornecida. O eixo e o conjunto de dados da chamada definem se o quantil é temporal ou espacial.

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## dissertacao/ferramentas/ajustar_word.py

Ajustes editoriais portáveis; não altera o texto nem rasteriza figuras.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\dissertacao\ferramentas\ajustar_word.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| lxml | Consulta/edição XML, incluindo os componentes internos de DOCX, PPTX e SVG. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| tempfile | Arquivos temporários definidos pelo processamento. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- {path} — chamada zipfile.ZipFile, linha 43.

**Saídas.**

- {tmp} — chamada zipfile.ZipFile, linha 101.

**Campos e chaves lidos.**

- files: word/document.xml, word/settings.xml.

**Campos e chaves gerados.**

- files: word/document.xml, word/settings.xml.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| q(s) | 30-30 | Organiza parâmetros, expressões ou retorno sem chamada externa. Retorno: '{' + W + '}' + s. |
| child(parent, name) | 32-38 | Chamadas efetivas: parent.find, q, ET.Element, parent.insert, parent.append Retorno: node. |
| run(path) | 41-106 | Chamadas efetivas: Path, ET.fromstring, root.iter, ET.tostring, .set, tempfile.mkstemp, os.close, print Retorno: st.get(q('val')) if st is not None else ''. |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de dissertacao/ferramentas/ajustar_word.py, linhas 30-38.

```python
def q(s):return '{'+W+'}'+s
# Child
def child(parent,name):
    node=parent.find(q(name))
    if node is None:
        node=ET.Element(q(name))
        if name in {'pPr','rPr','tblPr','tcPr','trPr'}:parent.insert(0,node)
        else:parent.append(node)
    return node
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## dissertacao/ferramentas/gerar.py

Gera os quatro produtos sem sobrescrever o formato anterior.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\dissertacao\ferramentas\gerar.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| os | Integração com sistema operacional e variáveis de ambiente. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| subprocess | Chamada de outros programas e verificação de seus resultados de execução. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 25-35 | Chamadas efetivas: subprocess.run, os.environ.get, shutil.which, candidate.exists, SystemExit, str |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de dissertacao/ferramentas/gerar.py, linhas 25-33.

```python
def run():
    quarto=os.environ.get('QUARTO_PATH') or shutil.which('quarto')
    if not quarto:
        candidate=ROOT.parent/'codigo/ferramentas/quarto-1.11.9/bin/quarto.exe'
        if candidate.exists():quarto=str(candidate)
    if not quarto:raise SystemExit('Instale o Quarto ou defina QUARTO_PATH para seu executável.')
    for folder,name,extra in [(ROOT,'Dissertacao_Congonhas',[]),(ROOT/'artigo','Artigo_CMAS_Congonhas',['--artigo'])]:
        for format,destination in [('html','_book/html'),('docx','_book/word')]:
            subprocess.run([quarto,'render','--to',format,'--output-dir',destination],cwd=folder,check=True)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## dissertacao/ferramentas/preparar_site.py

Reúne livro, artigo, visualizador e Word no diretório do GitHub Pages.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\dissertacao\ferramentas\preparar_site.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- Path(__file__).resolve().parents[1]/visualizador/catalogo.json — chamada .read_text, linha 40.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- catalog: catalog.
- item: src.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run() | 30-43 | lê dados |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de dissertacao/ferramentas/preparar_site.py, linhas 30-38.

```python
def run():
    TARGET.mkdir(exist_ok=True)
    for source,destination in [(ROOT/'_book/html',TARGET),(ROOT/'artigo/_book/html',TARGET/'artigo'),(ROOT/'_visualizador',TARGET/'visualizador')]:
        assert (source/'index.html').is_file(),source
        shutil.copytree(source,destination,dirs_exist_ok=True)
    downloads=TARGET/'downloads';downloads.mkdir(exist_ok=True)
    for source in [ROOT/'_book/word/Dissertacao_Congonhas.docx',ROOT/'artigo/_book/word/Artigo_CMAS_Congonhas.docx']:
        assert source.is_file(),source
        shutil.copy2(source,downloads/source.name)
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## dissertacao/ferramentas/preparar_visualizador.py

Prepara as prévias para o site e para a leitura sem conexão.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\dissertacao\ferramentas\preparar_visualizador.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| shutil | Cópia e movimentação de arquivos, inclusive preservação de versões geradas. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- {part} — chamada zipfile.ZipFile, linha 32.
- Path(__file__).resolve().parents[1]/visualizador/catalogo.json — chamada .read_text, linha 39.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Campos e chaves lidos.**

- data: catalog.
- x: mode.
- item: src.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de dissertacao/ferramentas/preparar_visualizador.py, linhas 31-39.

```python
for part in parts:
    with zipfile.ZipFile(part) as z:
        for item in z.infolist():
            destination=(target/item.filename).resolve()
            assert destination.is_relative_to(target.resolve()) and item.filename.startswith('imagens/') and item.filename.endswith('.webp'),item.filename
            assert item.file_size<4_000_000,item.filename
        z.extractall(target)
for name in ['index.html','dados.js','README.md']:shutil.copy2(source/name,target/name)
data=json.loads((source/'catalogo.json').read_text(encoding='utf8'))
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## dissertacao/ferramentas/verificar_exportacoes.py

Não publicar artefatos que contenham apenas outro formato de saída.

**Papel.** Conferência/teste. **Fonte inspecionada.** E:\projeto\dissertacao\ferramentas\verificar_exportacoes.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| lxml | Consulta/edição XML, incluindo os componentes internos de DOCX, PPTX e SVG. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| sys | Argumentos, interpretador Python e caminhos de importação. |
| zipfile | Leitura/empacotamento de arquivos ZIP e estruturas internas de documentos. |


**Entradas.**

- {folder}/_book/html/index.html — chamada html.read_text, linha 29.
- {folder}/_book/word/{name}.docx — chamada zipfile.ZipFile, linha 30.

**Saídas.**

Interface por parâmetros, retorno de funções ou programas chamados; os caminhos literais e as funções estão no inventário e no código integral.

**Sequência.** A rotina executa no corpo principal. Os pontos de leitura/escrita acima e os trechos abaixo mostram a ordem de processamento. Não é uma função que possa ser importada sem considerar esses efeitos.

**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de dissertacao/ferramentas/verificar_exportacoes.py, linhas 28-33.

```python
    assert html.is_file() and html.stat().st_size>1000,html
    assert '<html' in html.read_text(encoding='utf8'),html
    with zipfile.ZipFile(word) as f:
        body=ET.fromstring(f.read('word/document.xml'))
        if folder.name=='artigo':assert body.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}lnNumType'),'Artigo sem numeração de linhas'
    print(name+': HTML e Word presentes e verificados')
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 

## dissertacao/ferramentas/vincular_github.py

Configura o endereço; não cria repositório nem faz upload.

**Papel.** Processamento ou módulo de apoio. **Fonte inspecionada.** E:\projeto\dissertacao\ferramentas\vincular_github.py.

**Bibliotecas e dependências.**

| Importação | Uso na implementação |
| --- | --- |
| caminhos_congonhas | Configuração local dos caminhos, independente dos cálculos. |
| json | Configurações, metadados e registros estruturados de auditoria. |
| pathlib | Caminhos de arquivos independentes da concatenação manual de separadores. |
| re | Extração e validação de padrões textuais, datas, identificadores e linhas dos modelos. |
| subprocess | Chamada de outros programas e verificação de seus resultados de execução. |
| sys | Argumentos, interpretador Python e caminhos de importação. |


**Entradas.**

- Path(__file__).resolve().parents[1]/_quarto.yml — chamada p.read_text, linha 30.
- Path(__file__).resolve().parents[1]/artigo/_quarto.yml — chamada article.read_text, linha 36.

**Saídas.**

- Path(__file__).resolve().parents[1]/_quarto.yml — chamada p.write_text, linha 33.
- Path(__file__).resolve().parents[1]/artigo/_quarto.yml — chamada article.write_text, linha 37.
- Path(__file__).resolve().parents[1]/repositorio.json — chamada .write_text, linha 41.

**Etapas e interfaces.** As funções abaixo são apresentadas na ordem do arquivo. A existência de uma função não significa que seja chamada em toda execução.

| Função/interface | Linhas | Operação e retorno |
| --- | --- | --- |
| run(url) | 27-42 | lê dados; grava produtos |


**Trechos citados do código.** A numeração corresponde ao arquivo inspecionado nesta edição. São citações do processamento, não instruções para executar fragmentos isolados.

Trecho de dissertacao/ferramentas/vincular_github.py, linhas 27-35.

```python
def run(url):
    url=url.rstrip('/').removesuffix('.git')
    if not re.fullmatch(r'https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',url):raise ValueError('Informe https://github.com/CONTA/REPOSITORIO')
    root=Path(__file__).resolve().parents[1];p=root/'_quarto.yml';s=p.read_text(encoding='utf8')
    s=re.sub(r'^  repo-(?:url|branch|actions):.*\n','',s,flags=re.M)
    s=s.replace('book:\n','book:\n  repo-url: '+json.dumps(url)+'\n  repo-branch: main\n  repo-actions: [edit, issue, source]\n',1)
    p.write_text(s,encoding='utf8')
    article=root/'artigo/_quarto.yml'
    if article.exists():
```

**Reutilização e limites.** Alterar arquivos pelo JSON de caminhos e preservar nomes de campos/chaves, tipos e unidades citados. Antes de trocar a entrada, verificar a cobertura, o sistema de referência e a unicidade das chaves. Um teste ou auditoria confere consistência dentro do recorte previsto; não substitui a justificativa científica do método. 
