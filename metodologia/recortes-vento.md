# Recortes meteorológicos da modelagem de Congonhas

O relatório descreve como os arquivos meteorológicos de entrada foram associados às saídas do AERMOD. O período analítico é 2021-2023. A meteorologia é a série WRF processada pelo AERMET e efetivamente vinculada ao modelo, cuja identidade com as cópias do projeto foi verificada. A análise não representa uma climatologia construída com todas as estações municipais.

## Horas por direção de origem

Das 26.280 horas do triênio, 24.892 foram associadas a uma direção válida. As 1.388 horas restantes correspondem a calmarias ou condições meteorológicas inválidas para a associação adotada. Elas foram preservadas no calendário de auditoria, sem serem atribuídas a um dos oito setores. O dia técnico de 2024 não entra nos indicadores.

As direções são meteorológicas, isto é, indicam de onde sopra o vento. Cada setor tem 45 graus, centrado em N, NE, L, SE, S, SO, O e NO. O setor norte reúne [337,5°, 360°] e [0°, 22,5°). Os demais seguem intervalos contíguos, fechados à esquerda e abertos à direita. A velocidade é a informada na SFC, em m/s. Ela é descrita, mas não cria subgrupos adicionais nesta análise.

| Direção | 2021 | 2022 | 2023 | Total h | % válidas | Velocidade m/s |
| --- | --- | --- | --- | --- | --- | --- |
| N | 632 | 791 | 821 | 2244 | 9.01 | 1.50 |
| NE | 973 | 998 | 886 | 2857 | 11.48 | 1.59 |
| L | 1208 | 1016 | 1067 | 3291 | 13.22 | 1.60 |
| SE | 3400 | 3233 | 3038 | 9671 | 38.85 | 1.68 |
| S | 485 | 598 | 480 | 1563 | 6.28 | 1.06 |
| SO | 328 | 291 | 396 | 1015 | 4.08 | 1.17 |
| O | 628 | 576 | 730 | 1934 | 7.77 | 1.75 |
| NO | 638 | 833 | 846 | 2317 | 9.31 | 1.88 |

## Envelopes horários e diários

O envelope de 1 h seleciona a maior concentração em cada receptor entre as horas pertencentes à direção. Os horários dos máximos são mantidos por receptor. Dois receptores, ou dois poluentes, podem atingir o máximo em momentos diferentes. O mapa não é uma pluma simultânea. As contribuições dos grupos são recuperadas no mesmo evento de ALL em cada receptor, evitando somar máximos independentes.

Para o produto de 24 h, usa-se a média diária completa, reconstruída do POST de 1 h e conferida com o POST nativo de 24 h. A atribuição direcional exige pelo menos 18 horas válidas, resultante circular mínima de 0,5 e ao menos metade das horas no setor da direção média. Esses dois últimos critérios são escolhas exploratórias do estudo. Foram identificados 463 dias elegíveis. Os dias sem persistência não foram forçados a uma direção.

| Direção | 2021 | 2022 | 2023 | Total |
| --- | --- | --- | --- | --- |
| N | 4 | 8 | 8 | 20 |
| NE | 6 | 6 | 3 | 15 |
| L | 11 | 6 | 11 | 28 |
| SE | 118 | 109 | 101 | 328 |
| S | 0 | 1 | 0 | 1 |
| SO | 0 | 0 | 2 | 2 |
| O | 10 | 8 | 8 | 26 |
| NO | 12 | 17 | 14 | 43 |

A disponibilidade é desigual entre direções. O recorte diário de sudeste reúne 328 dias, enquanto sul e sudoeste possuem apenas um e dois dias, respectivamente. Esses mapas descrevem envelopes de eventos selecionados, sem igual representatividade temporal. Um máximo obtido de uma amostra maior tem mais oportunidades de incluir episódios elevados. A frequência, a estabilidade entre anos e os dias disponíveis devem acompanhar a comparação; a cor do mapa, isoladamente, não expressa probabilidade de ocorrência. A cobertura das estações é geométrica e baseada na elegibilidade do triênio, sem demonstrar observação válida em todos os eventos selecionados.

## Referência com a meteorologia completa

O cenário geral não filtra por direção, hora do dia ou estação do ano. Ele utiliza todas as horas meteorologicamente válidas para o máximo de 1 h e todos os dias elegíveis para o máximo de 24 h. São 1.075 dias, distribuídos em 357, 359 e 359 dias nos três anos. Para longa duração, mantém-se a média das três médias anuais nativas, sem substituir esse indicador pelo maior ano.

A união dos oito envelopes horários reproduz o máximo horário geral. A união dos envelopes diários de direção persistente não substitui o cenário diário geral. Ao incluir dias com vento variável, o cenário geral tem máximos maiores em 574 dos 1.008 receptores municipais para MP10 e em 749 para MP2,5. Essa diferença decorre do recorte temporal, sem alteração de emissões ou nova simulação.

## Como interpretar as novas figuras

Cada figura reúne MP10 e MP2,5 para a mesma duração e direção, no encarte nativo de 1:440.000. A pequena rosa junto à legenda usa os mesmos 24.892 vetores da apresentação, preservando frequências, setores gráficos de 30 graus e classes de velocidade. O destaque corresponde ao setor analítico de 45 graus selecionado, enquanto as demais direções permanecem em cinza. No visualizador, essa rosa também permite trocar o resultado exibido. As barras de concentração são independentes para os poluentes, mas seus limites permanecem fixos nas oito direções do mesmo poluente e duração. Portanto, a mesma cor em poluentes diferentes não implica igual concentração.

Quintis, Moran local, associação bivariada, matriz emissão-concentração, regiões de gestão e contribuições são calculados sobre os receptores originais. A interpolação é usada apenas para visualizar a concentração. Os grupos AEX e os subgrupos urbanos não são somados novamente às empresas e ao Urbano Total. As classes relativas e os cortes associativos não constituem padrões legais ou emissões permissíveis.

## Rastreabilidade

As entradas estão em E:/projeto/houremiss/AERMET-3Y.SFC e AERMET-3Y.PFL, conciliadas com as cópias em E:/projeto/wrf. As concentrações são lidas em E:/projeto/out-aermod/PM10 e PM2-5. O calendário horário, o diagnóstico de persistência diária, os códigos dos eventos, os manifestos de identidade e as auditorias permanecem na pasta output/16_revisao_pos_banca. Não foi executada nova modelagem para reorganizar essas figuras.
