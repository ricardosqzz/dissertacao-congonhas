# Preparação para discutir o pôster de Congonhas

Sessão 12 do CMAS

Este guia explica o raciocínio da pesquisa, a leitura de cada produto e as condições necessárias para defender os resultados. A referência é o pôster corrente, conferido em 14 de novembro de 2026. A apresentação deve mostrar a contribuição da análise espacial e reconhecer que os resultados ainda pertencem a um cenário modelado com incertezas conhecidas. O estudo não demonstrou uma nova calibração do AERMOD nem transformou os cortes relativos em padrões ambientais.

## A ideia que conecta a apresentação

Uma região com elevada emissão local pode não coincidir com a região que recebe as maiores concentrações. A meteorologia, a geometria e a altura das fontes, o terreno e a posição dos receptores participam dessa relação. Essa diferença sustenta a organização do trabalho. O inventário descreve a emissão. O modelo estima a concentração recebida. A análise espacial investiga a distribuição dessas duas grandezas. O zoneamento oferece a referência territorial para comunicar prioridades e planejar ações.

A contribuição científica precisa ser apresentada como uma investigação da informação adicional obtida ao combinar essas camadas. O método permite examinar se áreas com concentração semelhante também se parecem em outros indicadores, quais combinações de emissão e recepção aparecem no território e quanto a classificação depende das escolhas de escala e de corte. A aplicação pública é uma consequência dessa investigação, com monitoramento direcionado e seleção de áreas para aprofundamento.

O título do resumo foi preservado por orientação do autor. Ele se refere a attainment-status screening, enquanto o desenvolvimento pós-banca ampliou a classificação relativa. Explique essa evolução quando necessário. A conclusão de atendimento a um padrão exige um indicador temporal, um referencial e uma avaliação de representatividade apropriados. Uma posição relativa no campo modelado responde a outra pergunta.

## Bases e suporte espacial

O inventário de ano-base 2023 foi aplicado à meteorologia de 2021 a 2023. Portanto, os três anos representam condições diferentes de dispersão do mesmo inventário. A comparação não mede a evolução histórica real das emissões entre esses anos. As fontes horárias de erosão eólica podem variar com os dados meteorológicos, mas isso não transforma o restante do cadastro em inventários anuais independentes.

A rede regional tem 1.497 receptores. O suporte municipal usado na análise contém 1.008 receptores internos. Os 489 externos continuam importantes para a modelagem regional, mas não entram automaticamente no denominador dos resultados municipais do pôster. Os 311 registros de zoneamento permanecem como destino da tradução territorial. Interseções de células e zonas permitem registrar frações diferentes dentro da mesma zona, em vez de impor uma única condição uniforme.

As células de Voronoi são um suporte de análise e de cálculo de área. Elas não demonstram que a atmosfera seja homogênea dentro de cada polígono. A suavização de mapas também não cria receptores adicionais. As estatísticas devem continuar vinculadas aos pontos e suportes realmente utilizados, com a mesma identificação em todas as tabelas.

## Médias anuais quintis e perfis conjuntos

Os mapas anuais do pôster utilizam a média das três médias anuais nativas do AERMOD. Em cada receptor, os três valores anuais recebem o mesmo peso na média trienal. Isso preserva o tratamento temporal nativo e mantém explícito o indicador de longa duração.

Os quintis dividem a distribuição municipal em cinco faixas relativas, aproximadamente com um quinto dos receptores em cada grupo. Os limites de MP2,5 são 21,2, 29,4, 43,9 e 72,3 µg/m³, com arredondamento para apresentação. Essa operação é uma classificação por posição na distribuição, sem treinamento de k-means. Empates e arredondamentos explicam pequenas diferenças na quantidade de receptores por faixa.

O mapa de perfis conjuntos usa seis entradas, provenientes dos máximos de 1 h, máximos de 24 h e médias anuais dos dois poluentes. Os valores passam por log1p e padronização antes do agrupamento. Foram comparadas soluções Ward e k-means, com diferentes quantidades de grupos. A solução exibida tem k igual a dois, silhueta 0,481 e grupos de 744 e 264 receptores. Esse produto caracteriza semelhança multivariada. Ele não é uma simples substituição dos quintis por dois intervalos.

A silhueta compara a dissimilaridade média de um ponto dentro do próprio grupo com a do grupo alternativo mais próximo. Valores positivos indicam que, em média, a atribuição é mais coerente com o próprio grupo. O valor 0,481 não possui unidade e não é um valor p. Sua interpretação depende dos dados, das transformações, da distância e das soluções comparadas. A seleção foi relativa às alternativas testadas, sem demonstrar duas classes naturais universais ou validar a concentração prevista pelo modelo.

Há uma distinção de versões importante para estudar o código. A revisão espacial inicial também conserva um agrupamento com quatro indicadores, baseado em médias anuais e P98 dos dois poluentes. O painel corrente do pôster usa a solução conjunta de seis indicadores do cenário geral. Os dois produtos não devem ser citados como se tivessem a mesma matriz de entrada.

## Densidade de emissão e vias inventariadas

A densidade expressa massa emitida por ano dividida pela área do suporte territorial. O procedimento deve integrar primeiro as taxas de cada fonte, respeitando suas unidades. Para fontes de área, multiplica-se o fluxo superficial pela área representada. Uma linha exige o comprimento ou o corredor correspondente à sua formulação. A conversão para massa anual precisa conservar os calendários e fatores temporais utilizados.

No mapa do pôster, as vias sobrepostas são fontes viárias do inventário. Sua cor considera a massa dividida pelo corredor modelado, com comprimento e largura documentados. Essa camada não é a malha viária de contexto e não deve ser confundida com uma estimativa direta de tráfego. A massa das vias já participa dos totais de emissão. Sua sobreposição visual não a adiciona novamente ao inventário zonal.

Um valor elevado de densidade não significa, por si só, que a mesma concentração será registrada naquele local. Além da dispersão, a densidade depende do suporte usado no denominador. Por isso a leitura deve considerar a forma da fonte, o tamanho das células e das zonas e a conservação da massa durante o rateio.

## Cortes de emissão e sensibilidade espacial

Os quatro alvos de concentração são P20, P40, P60 e P80. Para cada alvo, o método procura um corte crescente de densidade de emissão que ajude a distinguir concentrações acima e abaixo daquele valor. A escolha maximiza a acurácia balanceada, calculada como a média entre sensibilidade e especificidade. Essa medida evita interpretar um bom resultado obtido apenas pela classe mais frequente como capacidade suficiente de separação.

Foram utilizados blocos espaciais de 2 e 4 km, com cinco partições em cada escala. Cada caixa do pôster reúne dez cortes estimados nos conjuntos de treinamento. O losango representa o corte ajustado com o conjunto completo. Os testes são feitos nos receptores reservados da respectiva partição. Os dez ajustes compartilham dados e não constituem dez experimentos independentes.

Para o alvo P80, o corte completo de MP2,5 é 8,50 t/ano/km² e a acurácia balanceada média de teste é aproximadamente 0,767. Isso não significa que o modelo acertou 76,7% das concentrações nem que toda emissão abaixo do corte garante atendimento. A estimativa é associativa e depende do inventário, do período meteorológico, do suporte espacial e do próprio campo de concentrações modeladas.

O boxplot descreve a distribuição dos cortes entre partições. Ele não é automaticamente um intervalo de confiança do limite físico de emissão. Se os cortes variam, essa variabilidade deve acompanhar a discussão. Cortes associados aos quatro percentis também podem ficar próximos ou perder uma ordem estrita. Nesse caso, cinco intervalos de emissão não podem ser impostos como se fossem cinco estados físicos distintos. A configuração e as tabelas registram quando essa separação não é identificável.

## Matriz de emissão e concentração

A matriz cruza concentração anual acima de P80 com densidade de emissão acima do corte associado a P80. Surgem quatro combinações. Alta concentração e alta emissão indicam coexistência de recepção elevada e emissão local relevante. Alta concentração com menor emissão cadastrada sugere investigar transporte e contribuições de outras áreas. Emissão elevada com menor concentração recebida sugere examinar a dispersão e possíveis receptores a jusante atmosférico. A combinação inferior nas duas dimensões é relativa ao cenário.

Nenhuma dessas classes demonstra causalidade por si só. Uma área com alta concentração pode reunir fontes locais e transportadas. Uma área de alta emissão e concentração menor pode causar impacto fora do seu suporte. A atribuição dos grupos, a meteorologia e a localização das fontes ajudam a desenvolver essa interpretação, mas não substituem o teste de cenários de controle.

## Contribuição dos grupos e leitura da curva ABC

As contribuições são concentrações recebidas dos grupos do AERMOD. Para sintetizar uma região, calcula-se a contribuição média ponderada pela área de suporte e divide-se pelo total recebido na mesma região. Assim, os percentuais se referem à concentração modelada naquele conjunto de receptores e não à fração da massa total do inventário.

Nas prioridades receptoras apresentadas, Gerdau e Urbano Total correspondem a aproximadamente 74,7% e 16,5% da concentração anual recebida. A predominância deve ser interpretada no contexto do cadastro, da meteorologia e do cenário simulado. Ela não constitui atribuição jurídica de responsabilidade ou comprovação de que uma redução proporcional do inventário produzirá necessariamente a mesma redução em todos os indicadores.

Urbano Total reúne vias urbanas, núcleos urbanos e ferrovias, com processos de ressuspensão e combustão conforme o inventário. O total e seus subgrupos se sobrepõem. O grupo AEX também reúne áreas expostas de diferentes empreendimentos. Grupos agregados de diagnóstico não devem ser somados novamente aos grupos primários na apuração de percentuais. A soma precisa usar uma partição de fontes sem sobreposição.

Na curva ABC, os grupos são ordenados da maior para a menor contribuição e a curva mostra a participação acumulada. Os cortes operacionais de 80% e 95% delimitam as faixas A, B e C no método. A classificação é aplicada ao grupo cuja contribuição começa antes do corte, o que pode fazer o acumulado ultrapassar 80% ao terminar o último grupo A. O nome de uma empresa no eixo representa a categoria ordenada, e não uma variável usada para prever sua própria importância.

## Regiões propostas e tradução ao zoneamento

A prioridade receptora do pôster reúne 202 receptores, 14 regiões contíguas, 52,4 km² e interseção com 137 registros de zoneamento. A contiguidade reúne células com a mesma função de gestão. O agrupamento estatístico de dois perfis e as 14 regiões contíguas são produtos diferentes.

As funções propostas incluem prioridade receptora, controle de fontes, menor impacto relativo e acompanhamento. Um resultado não significativo de Moran não impede que uma concentração alta seja importante para gestão. O teste local é uma linha de evidência, sem funcionar como condição obrigatória para aceitar toda prioridade. Da mesma forma, uma zona parcialmente intersectada não deve ser descrita como integralmente pertencente à região.

O método busca orientar onde investigar, monitorar e testar controle. A passagem para uma regra administrativa exige pactuação institucional, avaliação do inventário, informação sobre população exposta, análise dos cenários de redução e exame das incertezas de delimitação. O rótulo menor impacto relativo não equivale a ausência de risco.

## Perguntas e respostas para a discussão

### Pergunta 1

**Por que o título menciona atendimento, mas os mapas apresentam classes relativas?**

O título foi preservado do resumo simples. A revisão pós-banca passou a explorar diferenças internas do campo modelado, enquanto a avaliação normativa foi mantida separadamente. A classificação relativa amplia a informação disponível para gestão, sem redefinir padrões de qualidade do ar.

**English answer.** We retained the submitted abstract title. The current poster develops relative spatial screening, while regulatory attainment remains a separate assessment.

### Pergunta 2

**O k-means faz a mesma coisa que separar por percentis?**

Não. Os quintis ordenam uma concentração anual. O agrupamento usa simultaneamente seis indicadores transformados e padronizados. Dois receptores podem estar no mesmo quintil anual e apresentar comportamentos diferentes nos extremos de 1 h e 24 h.

**English answer.** Quintiles rank one annual indicator. Clustering compares six standardised indicators simultaneously.

### Pergunta 3

**A silhueta 0,481 é boa e qual é o valor p?**

É a medida de separação interna usada para comparar as soluções testadas. Ela não é um teste com valor p e não estabelece uma aprovação universal. O resultado favoreceu a solução apresentada entre as alternativas examinadas, mas precisa ser acompanhado de estabilidade e interpretação física.

**English answer.** The silhouette is an internal separation measure, not a p-value or a measure of model accuracy.

### Pergunta 4

**O corte de 8,50 pode ser adotado como limite de licenciamento?**

O estudo não sustenta essa adoção. O corte descreve uma associação entre densidade emitida e concentração modelada para o cenário analisado. Não incorpora automaticamente condições de outros inventários, meteorologias, geometrias ou medidas de controle. Pode orientar investigação, acompanhada da sua variabilidade.

**English answer.** It is an empirical screening cut for this scenario, not a permissible emission limit.

### Pergunta 5

**Os 0,767 significam 76,7% de acerto do AERMOD?**

Esse número é a acurácia balanceada de um classificador de concentração alta usando um corte de emissão. Não compara concentrações previstas com medições e não mede erro do AERMOD em µg/m³.

**English answer.** It is test balanced accuracy for the emission-cut classifier, not observed-modelled accuracy.

### Pergunta 6

**Por que há 264 receptores no perfil superior e 202 nas prioridades?**

O primeiro número vem do agrupamento conjunto dos seis indicadores. O segundo utiliza a condição anual acima de P80 na proposta de gestão. As entradas e regras são diferentes, portanto os conjuntos não precisam coincidir.

**English answer.** The higher joint profile and annual receiving priority use different inputs and decision rules.

### Pergunta 7

**Moran não significativo indica uma área limpa?**

Não indica. Significa que, com a vizinhança, o atributo e a correção de multiplicidade adotados, não foi identificada a associação local exigida pelo teste. A magnitude da concentração deve ser examinada separadamente.

**English answer.** A non-significant local statistic does not establish clean air or a low concentration.

### Pergunta 8

**O anual usa somente a direção predominante do vento?**

O modelo utiliza a sequência meteorológica disponível e elegível. A média anual acumula as condições do período. A direção predominante é uma característica da frequência dos ventos, sem substituir todas as horas por uma direção única.

**English answer.** Annual results include all eligible meteorological periods, rather than a single prevailing direction.

### Pergunta 9

**As porcentagens dos grupos representam emissão ou concentração?**

As barras representam concentração recebida, ponderada pelo suporte de área das prioridades. A emissão é a massa liberada pelas fontes, apresentada em outros produtos. A diferença é central para interpretar regiões receptoras com emissão local menor.

**English answer.** These are received concentration shares, not shares of locally emitted mass.

### Pergunta 10

**Urbano Total significa culpa do município?**

É uma agregação de processos inventariados, com vias, núcleos e ferrovias. A categoria não identifica isoladamente o agente responsável por cada emissão, e a modelagem não constitui uma atribuição jurídica de responsabilidade.

**English answer.** Urban Total is an inventory grouping of processes, not an automatic assignment of municipal responsibility.

### Pergunta 11

**Por que começar nos receptores e depois passar para as zonas?**

Essa escolha evita que uma média inicial por zona esconda diferenças internas. O resultado pode mostrar quanto da área de uma zona participa de cada função de gestão. A resolução efetiva continua limitada pela grade, pelos dados e pelo suporte espacial.

**English answer.** Receptor-first analysis preserves within-zone differences before translating them to zoning.

### Pergunta 12

**A soma das áreas ou dos registros de zoneamento pode ser repetida?**

Uma zona pode intersectar mais de uma região ou classe. O número de interseções não é igual ao número de zonas exclusivas. As frações de área devem ser calculadas com a geometria correspondente, conferindo sobreposições e preservando os identificadores.

**English answer.** Intersections and unique zoning records are different counts. Area shares must use the correct geometry.

### Pergunta 13

**Os máximos horários e diários são um mesmo evento?**

Nos perfis conjuntos, os máximos são específicos de cada receptor e podem ocorrer em datas diferentes. Eles descrevem o potencial extremo do período, sem representar uma única fotografia temporal da pluma.

**English answer.** Receptor-specific maxima may occur at different times. They are spatial envelopes, not one event.

### Pergunta 14

**Como a incerteza será tratada na continuidade?**

Os testes incluem alternativas de vizinhança, partições espaciais para os cortes e comparação de soluções de agrupamento. Ainda é necessário examinar perfis temporais de emissão, sensibilidade de parâmetros físicos, grade e suporte territorial, além da avaliação observado-modelado em períodos e relógios compatíveis. Uma proposta de teste não deve ser apresentada como melhoria já demonstrada.

**English answer.** Spatial sensitivity is available, while new emission-timing simulations and independent evaluation remain necessary.

### Pergunta 15

**O estudo já estima desfechos de saúde no pôster?**

A avaliação sanitária integra o projeto mais amplo, mas foi retirada deste pôster para manter o foco na classificação espacial e na gestão. Os mapas apresentados não permitem atribuir diretamente internações, mortalidade ou exposição individual a um grupo emissor.

**English answer.** Health assessment belongs to the broader dissertation and is outside this poster.

## Como organizar uma resposta quando faltar um número

Comece pelo indicador sobre o qual a pessoa perguntou, informe o recorte temporal e espacial e só então apresente o valor que está confirmado. Se a pergunta exigir uma comparação ainda não executada, explique qual dado ou teste falta. É preferível dizer que a avaliação está planejada a transformar uma hipótese em resultado. Os arquivos de apoio e os códigos documentados permitem recuperar parâmetros e tabelas sem improvisar números durante a conversa.

## Fontes para aprofundamento

Os valores apresentados foram conferidos no pôster da Sessão 12, na auditoria de revisão de 09/11/2026, nas tabelas de perfis conjuntos e nos produtos de gestão pós-banca. Os procedimentos de referência incluem o [AERMOD Modeling System da US EPA](https://www.epa.gov/scram/air-quality-dispersion-modeling-preferred-and-recommended-models) e a formulação da [silhueta de Rousseeuw](https://doi.org/10.1016/0377-0427%2887%2990125-7). O relatório dos códigos detalha as implementações específicas e seus caminhos de entrada e saída.
