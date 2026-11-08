# Guia de estudo do pôster e da metodologia de Congonhas

Este guia reúne a metodologia completa já documentada e uma leitura detalhada de cada painel do pôster CMAS, incluindo os grupos contribuintes, a estabilidade dos limiares e um roteiro de apresentação. Os resultados pertencem ao cenário existente e não representam uma nova simulação calibrada. Revisão de 08/11/2026.

Este guia explica o que cada etapa produz, como os cálculos são realizados e como os resultados devem ser interpretados. A pesquisa procura verificar o que a análise conjunta de concentrações, emissões e organização espacial acrescenta ao diagnóstico por zoneamento. Além de localizar áreas prioritárias, precisa mostrar em que condições essa classificação é estável e quais limitações ainda dependem de novos dados ou de outra execução do modelo.

O município permanece como referência de gestão e as 311 identificações de zoneamento são preservadas. Entretanto, a análise começa nos receptores da modelagem. Essa escolha evita reduzir de imediato uma zona extensa e heterogênea a uma única média. Os padrões encontrados são posteriormente relacionados às zonas por suas proporções de área. Assim, uma mesma zona pode conter áreas receptoras prioritárias, áreas emissoras e locais com menor impacto relativo.

## As bases e a escala da análise

O projeto reúne inventário de emissões, localização e geometria das fontes, saídas do AERMOD, meteorologia WRF processada pelo AERMET, monitoramento de qualidade do ar, zoneamento, limites municipais, vias, uso da terra e população censitária. Cada base cumpre uma função. O inventário informa quanto e onde se emite. O modelo estima a concentração recebida. O monitoramento fornece observações para confrontar essas estimativas. As bases territoriais permitem interpretar os resultados no espaço em que vivem as pessoas e são tomadas decisões públicas.

O inventário de ano-base 2023 foi aplicado às condições meteorológicas de 2021-2023. Isso representa o comportamento de um mesmo inventário sob três anos de dispersão, e não três inventários anuais independentes. A média anual modelada considera as condições de todos os períodos elegíveis. Ela não substitui as direções horárias por uma única direção predominante. A predominância aparece como resultado da frequência de ocorrência dos ventos.

A rede regional contém 1.497 receptores. No suporte municipal atualmente utilizado, 1.008 são internos e 489 são externos. As células de Voronoi, recortadas pela união do zoneamento, atribuem a cada receptor uma área de suporte para cálculos de área e interseção. Elas não demonstram que a concentração real seja uniforme dentro da célula. A interpolação suavizada das plumas é apenas uma representação visual e não cria novas observações para os testes estatísticos.

A união cadastral utilizada tem aproximadamente 304,07 km². A conferência encontrou 31 geometrias menores que 1 m², das quais 18 têm menos de 0,01 m². Preservar seus identificadores mantém a rastreabilidade, mas não confirma que sejam unidades territoriais independentes adequadas. Esses fragmentos precisam ser verificados na camada de origem. A comparação com o limite municipal oficial também deve anteceder a consolidação cartográfica definitiva.

## Preparação da modelagem e verificação das concentrações

O AERMOD é o modelo de dispersão que gerou as concentrações de referência. As entradas precisam conservar a geometria, a altura de liberação, os parâmetros físicos, o tratamento do terreno e a massa de cada fonte. Uma taxa de fonte de área em g/s/m² deve ser integrada pela área representada. Uma taxa linear exige o comprimento correspondente. Apenas depois dessa integração a taxa total pode ser convertida em massa anual. Para operação contínua durante 8.760 horas, 1 g/s corresponde a 31,536 t/ano. Calendários e fatores temporais diferentes exigem integração do período efetivamente representado.

As fontes de erosão eólica com emissão variável são tratadas pelos arquivos HOUREMIS, atualmente com 252 vínculos de fontes. A entrada estática dessas fontes deve permanecer coerente com a vinculação horária, evitando somar a mesma emissão duas vezes. Os ajustes de área devem conservar a massa, distribuindo-a sobre a geometria efetivamente importada. Núcleos urbanos agregados permanecem estáticos nesta etapa, pois sua composição não permite atribuir a todos os processos um perfil horário único com segurança.

As médias diárias são reconstruídas dos arquivos POST de 1 h, usando o calendário meteorológico independente e o denominador de horas efetivas reproduzido para o cenário. O procedimento exige ao menos 18 horas válidas e respeita o tratamento de calmarias. A série reconstruída foi confrontada integralmente com a saída nativa de 24 h. As diferenças máximas inferiores a 0,000008 µg/m³ são compatíveis com o arredondamento dos arquivos. Essa conferência demonstra consistência numérica do processamento, sem demonstrar concordância com a atmosfera observada.

Para longa duração, utiliza-se a média das três médias anuais nativas do AERMOD. O P98 diário é calculado separadamente em cada ano e depois promediado no triênio. Não se reúnem todos os dias em um único percentil e não se descartam os maiores valores para reduzir a superestimação. O cenário geral complementar usa máximos de 1 h, máximos de 24 h e a média anual trienal, mantendo explícita a diferença entre um envelope extremo e um indicador de longa duração.

A comparação observado-modelado deve utilizar o mesmo ponto, o mesmo período e a mesma convenção de horário. São examinados viés, erros, correlação, séries diárias e perfis por hora, mês e dia da semana. A hipótese de registros observados em UTC foi documentada e precisa de confirmação pelos responsáveis pelas estações. O fuso não deve ser escolhido pelo melhor ajuste estatístico. Perfis normalizados ajudam a comparar a forma das curvas, enquanto os gráficos em concentração preservam a informação sobre a magnitude do desvio.

## Objetivo 1 Caracterização territorial e classificação dos padrões

O diagnóstico por padrões de qualidade do ar permanece separado da classificação relativa pós-banca. No monitoramento, devem ser verificados instrumentos, períodos, lacunas e representatividade em cada escala temporal. A regra adotada para os quadrimestres considera 50% de dados válidos, sem substituir os demais critérios aplicáveis às médias. A cobertura espacial emprega o entorno de 4 km adotado no estudo e o limiar de 50% da área da zona. Uma estação só informa o poluente que mede e o período em que sua série é elegível. Por isso, as coberturas de MP10 e MP2,5 não devem ser igualadas automaticamente.

O monitoramento elegível prevalece no produto integrado de atendimento, enquanto a modelagem complementa a informação espacial conforme os critérios documentados. Um resultado exclusivamente modelado inferior ao referencial não basta, diante do viés conhecido, para comprovar atendimento ambiental. Quando o monitoramento recente e a modelagem pertencem a períodos diferentes, a comparação territorial deve identificar esse contraste. A validação do modelo, por sua vez, exige períodos efetivamente coincidentes.

A classificação relativa inicia pelas concentrações em cada receptor municipal. Os percentis P20, P40, P60 e P80 definem cinco intervalos. Q1 contém valores até P20. Q2 contém valores acima de P20 e até P40. Q3 vai de acima de P40 até P60. Q4 vai de acima de P60 até P80. Q5 reúne valores acima de P80. Empates podem impedir que cada classe contenha exatamente 20% dos receptores. Essas classes expressam posição no cenário, sem definir níveis legais de qualidade do ar ou risco sanitário.

Essa divisão é diferente do agrupamento por aprendizado de máquina. Ward e k-means procuram receptores semelhantes considerando várias variáveis simultaneamente. Os indicadores recebem transformação log(1+C) e padronização para evitar que uma escala numérica domine o ajuste. Foram comparadas soluções de dois a seis grupos, com inicializações e sementes documentadas. A silhueta avalia a separação interna das soluções, sem medir a precisão do AERMOD.

Há duas comparações que precisam permanecer distintas. A referência de quatro indicadores utiliza as médias anuais e os P98 dos dois poluentes e favoreceu Ward com dois grupos, com silhueta de aproximadamente 0,533. A extensão de seis indicadores utiliza máximos de 1 h, máximos de 24 h e médias anuais dos dois poluentes. Ela favoreceu k-means com dois grupos e silhueta de aproximadamente 0,481. A diferença entre as silhuetas não demonstra melhora ou piora do modelo, porque os conjuntos de variáveis são diferentes. Como as coordenadas não entram nesses ajustes, um mesmo grupo pode ocorrer em partes descontínuas do município.

O Moran global verifica se valores semelhantes apresentam organização espacial no conjunto. O Moran local examina cada receptor em relação à vizinhança. A referência usa oito vizinhos municipais mais próximos, pesos padronizados por linha, transformação log(1+C) e 999 permutações condicionais bilaterais. A correção de Benjamini-Hochberg controla a taxa nominal de falsas descobertas em 5% por campo analisado.

Alto-alto significa valor relativamente alto acompanhado por vizinhos relativamente altos. Baixo-baixo representa a combinação oposta. Alto-baixo e baixo-alto indicam contrastes locais. Não significativo significa que o teste não forneceu evidência suficiente após a correção. Essa classe não significa ausência de poluição e não deve ser preenchida artificialmente como baixa concentração.

Os correlogramas apresentam a distância no eixo horizontal e o Moran no vertical, usando bandas de 750 m até 7,5 km. A curva ajuda a reconhecer em que escalas a semelhança espacial diminui. Ela não determina, isoladamente, a distância de transporte de uma fonte. As comparações com quatro e doze vizinhos mostram quanto os resultados dependem da vizinhança. O índice de Jaccard mede a interseção entre conjuntos dividida pela união. Sua redução indica que a fronteira dos conjuntos prioritários é sensível ao critério escolhido, sem demonstrar alteração física nas concentrações.

## Objetivo 2 Relação entre emissão e concentração

As fontes são localizadas por seus identificadores e geometrias. Fontes pontuais são atribuídas uma única vez. Fontes de área são rateadas pela fração que intercepta cada unidade de análise. Fontes lineares são rateadas pelo comprimento. Fontes de volume com suporte poligonal são distribuídas pela geometria cadastral disponível, mantendo a ressalva de que esse polígono não comprova uma superfície física emissora. A soma das parcelas deve recuperar a massa independente que pertence ao suporte municipal.

A massa em t/ano informa quanto foi atribuído a uma unidade. A densidade em t/ano/km² divide essa massa pela área da unidade e permite comparar suportes de tamanhos diferentes. Essa densidade não é a taxa superficial em g/s/m² usada na entrada do modelo. Valores elevados podem decorrer de massa concentrada em uma área pequena e precisam ser conferidos contra a geometria e a unidade, em vez de apenas reduzir o limite da legenda. O rateio atual conservou aproximadamente 9.069,04 t/ano de MP10 e 3.330,93 t/ano de MP2,5 no suporte municipal.

O diagnóstico de massa superior a 100 t/ano por fonte ou zona permanece como informação histórica separada. A nova relação espacial procura cortes de emissão associados aos alvos de concentração P20, P40, P60 e P80. Para cada alvo, procura-se um corte crescente de emissão que melhor separe receptores acima e abaixo daquele valor de concentração. O critério é a acurácia balanceada, que atribui igual importância à sensibilidade e à especificidade.

Os cortes são ajustados e testados em partições espaciais, com blocos de 2 e 4 km. Isso reduz o otimismo que poderia resultar de dividir aleatoriamente receptores vizinhos muito semelhantes. O desempenho fora do treino e a variação dos cortes entre partições acompanham o resultado. Quatro cortes só produzem cinco faixas associativas quando são finitos, distintos e crescentes. Quando essa condição falha em um recorte, a saída registra que cinco faixas associativas não foram identificadas. Quintis independentes de emissão, quando apresentados como alternativa, precisam ser identificados como outra classificação.

Na referência anual, os cortes de densidade associados aos quatro alvos foram aproximadamente 0,00055, 0,09, 4,03 e 28,13 t/ano/km² para MP10, e 1,15, 2,05, 7,06 e 8,50 t/ano/km² para MP2,5. São associações empíricas deste cenário e suporte. Não informam quanto uma empresa pode emitir nem quanto uma emissão adicional aumentará a concentração. Uma análise de resposta ao controle exige alterar fontes documentadas e executar outro cenário.

A matriz emissão-concentração usa alta concentração acima de P80 e alta emissão acima do corte associado a P80. As outras posições são denominadas demais concentrações e demais emissões. Uma célula com alta emissão e concentração fora da faixa superior pode exportar contribuição para outros locais, mas essa interpretação precisa de investigação fonte-receptor. Uma célula com alta concentração e menor emissão local pode receber contribuições externas. O Moran bivariado acrescenta a associação entre a concentração focal e a emissão na vizinhança, sem identificar sozinho o responsável ou a trajetória de transporte.

## A extensão por direção do vento

O calendário possui 26.280 horas entre 2021 e 2023. Foram atribuídas direções a 24.892 horas válidas. As demais correspondem a calmarias ou outras condições excluídas da associação direcional. O dia técnico de 2024 não participa dos indicadores. Os setores de 45° são centrados em N, NE, L, SE, S, SO, O e NO. Eles representam a direção de onde o vento sopra.

Em 1 h, seleciona-se o maior valor de cada receptor entre as horas pertencentes ao setor. Guardam-se o horário desse máximo e as contribuições dos grupos nesse mesmo evento. Dois receptores podem atingir seus máximos em horas diferentes. Portanto, o mapa é um envelope condicionado, e não uma pluma simultânea. A meteorologia da entrada representa um perfil do domínio e não um campo tridimensional reconstruído em cada zona.

Em 24 h, são utilizadas médias diárias completas em dias com direção persistente. Além das 18 horas válidas, o recorte exige resultante circular mínima de 0,5 e ao menos 50% das horas no setor da direção média. Esses dois critérios são escolhas exploratórias do estudo. Foram identificados 463 dias persistentes, enquanto a referência diária geral contém 1.075 dias elegíveis. O setor SE reúne 328 dias persistentes, o setor S apenas um e SO apenas dois. A comparação de máximos precisa considerar essa desigualdade de amostra.

Os mesmos testes de quintis, Moran, associação bivariada, cortes de emissão, regiões e contribuições são repetidos nos campos direcionais dos dois poluentes. A união dos oito envelopes horários recupera o máximo horário geral. Em 24 h, essa união não substitui a referência completa, pois os dias com vento variável foram excluídos dos recortes persistentes. A referência geral contém máximos superiores em 574 receptores municipais de MP10 e 749 de MP2,5 em comparação com aquela união.

A rosa apresentada no visualizador usa os mesmos 24.892 vetores da apresentação, as mesmas classes de velocidade e setores gráficos de 30°. O destaque seleciona o intervalo de 45° usado na análise, sem modificar as frequências de fundo. Assim, a divisão visual da rosa e o recorte dos testes têm resoluções distintas e explicitadas. A seleção muda o resultado exibido, não recalcula o AERMOD.

## Objetivo 3 Contribuições e regiões de gestão

As concentrações dos grupos emissores representam a parcela recebida em um receptor. Para longa duração, utilizam as médias anuais nativas dos mesmos três anos. Para os máximos horários e diários, as parcelas são recuperadas no evento do máximo de ALL no mesmo receptor. Somar máximos independentes dos grupos produziria uma combinação que pode nunca ter ocorrido.

Empresas e Urbano Total formam a partição exclusiva conferida contra ALL. O agregado AEX e os subgrupos urbanos são informações sobrepostas, por isso não são somados novamente. Urbano Total reúne vias, núcleos urbanos e ferrovias, com processos de ressuspensão e combustão. Sua contribuição não deve ser atribuída indistintamente à atividade administrativa municipal ou apenas ao escapamento de veículos.

Os papéis propostos de gestão distinguem prioridade receptora, controle de fontes, menor impacto relativo e acompanhamento. A prioridade receptora contém concentração acima de P80. O controle de fontes reúne emissão acima do corte associado a P80 e concentração fora da faixa superior. O menor impacto relativo reúne concentração até P40 e emissão até o corte associado a P40. As demais combinações ficam em acompanhamento. Menor impacto relativo não significa segurança sanitária ou atendimento legal.

Células de mesmo papel são reunidas quando compartilham um segmento de fronteira maior que 1 cm. Contato apenas por vértice não une regiões. As regiões preservam área, concentração, composição das fontes, evidência local de Moran e interseção com o zoneamento. Na referência anual de MP2,5, 202 receptores prioritários formaram 14 regiões, aproximadamente 52,4 km² e interseção com 137 identificadores de zona. As 137 zonas não são consideradas prioritárias em sua área integral apenas por essa interseção.

A participação regional de um grupo é calculada como a soma de sua concentração ponderada pela área de suporte, dividida pela soma de ALL com os mesmos pesos. Essa razão não é necessariamente a média simples das porcentagens de cada receptor. No conjunto das regiões receptoras prioritárias de MP2,5, as parcelas foram aproximadamente 74,7% para Gerdau, 16,5% para Urbano Total e 8,9% para os demais grupos. São parcelas de concentração modelada recebida, sem equivalência à porcentagem de massa emitida no município.

A curva ABC ordena os grupos por contribuição nesse recorte receptor. A classe A reúne os primeiros grupos até atingir ou cruzar 80% do acumulado. B prossegue até atingir ou cruzar 95%, e C contém o restante. O grupo que cruza o limite permanece na classe anterior. Não se força que 20% dos grupos pertençam a A, pois a composição depende da distribuição real das contribuições. A curva muda quando o conjunto de regiões selecionado muda. Essa é a razão para distinguir a ABC das prioridades acima de P80 da antiga ABC restrita aos agrupamentos alto-alto.

As propostas apoiam a escolha de locais para investigação e de grupos para cenários de controle. O índice preventivo e a classificação por padrões mantidos no projeto constituem diagnósticos separados. A decisão de gestão deve considerar dados, incertezas e a competência do órgão ambiental. As categorias relativas não podem ser interpretadas automaticamente como graus legais de saturação ou limites de licenciamento.

## Objetivo 4 População e avaliação sanitária

A população censitária precisa ser distribuída com apoio de evidências residenciais. A interseção entre setores censitários e zoneamento, sozinha, pode atribuir moradores a grandes áreas industriais ou a locais sem residência. O refinamento dasimétrico utiliza uso da terra, domicílios e outras informações de ocupação para restringir a distribuição e conservar a população dos setores de origem. Áreas rurais não são excluídas automaticamente, pois podem conter moradores.

A avaliação sanitária utiliza exposição de longa duração e função concentração-resposta compatível com o desfecho e a população, seguindo a fundamentação de Andreão et al. (2020). Para uma função log-linear, a fração potencialmente evitável pode ser escrita como F = 1 - exp(-β × ΔC), em que ΔC é a redução de exposição e β deriva do risco relativo e do incremento de concentração da referência. Se a concentração já estiver abaixo da meta do cenário, não se cria redução negativa para aumentar artificialmente a fração.

Os cenários de referência podem representar diferentes metas de redução, com a natureza de cada uma identificada. Um mesmo coeficiente não deve ser aplicado indiscriminadamente a MP10, MP2,5, idades e doenças diferentes. Converter a fração em número de internações ou óbitos exige taxas basais e população elegível coerentes com o período e o desfecho. A pesquisa ainda depende dessas verificações para essa quantificação. O pôster atual não apresenta estimativas de eventos sanitários evitados.

## O que está consolidado e o que ainda precisa ser testado

O processamento já permite examinar o campo de concentrações, sua classificação relativa, os padrões de associação espacial, o rateio conservativo das emissões, as contribuições dos grupos e a tradução territorial para as 311 identificações. Também permite comparar a meteorologia completa com os envelopes direcionais. Esses produtos organizam a evidência e tornam verificáveis as escolhas metodológicas.

Ainda precisam ser consolidados o cadastro territorial, a convenção temporal das estações, o suporte residencial e as bases sanitárias. A revisão das entradas de MP2,5 e os novos perfis de emissão exigem nova modelagem antes de serem apresentados como melhoria. CALMET ou outro campo meteorológico mais detalhado poderá ser investigado como cenário adicional, sem substituir retrospectivamente o vento efetivamente usado no AERMOD.

O cenário de sensibilidade temporal deve manter a massa anual, os fatores não negativos e os limites operacionais. A parcela já tratada pelo EMI precisa ficar separada do novo ajuste. O perfil observado em uma estação resulta da combinação de emissão, meteorologia, transporte e fontes externas, por isso não pode ser copiado diretamente como perfil emissor. Distâncias ajudam a interpretar a comparação, mas não são pesos de contribuição suficientes. O ajuste deve usar poucos parâmetros, períodos de treino e avaliação reservada, incluindo estações independentes quando possível.

Para interpretar a confiabilidade, é necessário separar três perguntas. A verificação numérica testa se os arquivos e as contas são consistentes. A análise de estabilidade testa se as prioridades dependem de critérios como vizinhança, suporte e recorte temporal. A avaliação observado-modelado testa a proximidade do cenário com a realidade medida. Um resultado favorável em uma dessas dimensões não substitui as outras. Essa separação sustenta a contribuição científica e evita tratar uma figura visualmente completa como evidência suficiente de validação.

## Referências de apoio

Anselin (1995), Local Indicators of Spatial Association, Geographical Analysis, 27, 93-115. Benjamini e Hochberg (1995), controle da taxa de falsas descobertas, Journal of the Royal Statistical Society B, 57, 289-300. Roberts et al. (2017), validação com estrutura espacial e temporal, Ecography, 40, 913-929. Clappier et al. (2017), distinção entre contribuição e sensibilidade, Geoscientific Model Development, 10, 4245-4256. Andreão et al. (2020), impactos de partículas sobre mortalidade e hospitalizações no Brasil, Journal of Environmental Management, 270, 110840. Ribeiro et al. (2025), episódios críticos de PTS em área influenciada por mineração, Environmental Technology, DOI 10.1080/09593330.2025.2556349. As referências completas e os resultados de auditoria permanecem nos capítulos e nas pastas analíticas do projeto.


## Leitura detalhada do pôster, painel por painel

O pôster utiliza MP2,5 como fio principal. O painel de k-means incorpora os seis indicadores dos dois poluentes, e essa informação está expressa em sua legenda. O título permanece exatamente igual ao resumo simples aceito. Sua expressão attainment-status screening registra a origem do trabalho, mas o desenvolvimento atual distingue esse diagnóstico das classes relativas introduzidas após a banca. Na apresentação, essa evolução deve ser explicada como aprofundamento do diagnóstico territorial, sem apresentar quintis como novos padrões legais.

A leitura pode começar no objetivo e seguir os quatro passos do método. Depois, os seis mapas à direita são lidos por linha, da esquerda para a direita. A primeira linha descreve as concentrações e seus perfis conjuntos. A segunda apresenta a emissão por zona e a sensibilidade da identificação de alta emissão. A terceira relaciona emissão e concentração e traduz os resultados em papéis propostos de gestão. O gráfico de contribuição mostra quais grupos respondem pela concentração recebida nas regiões prioritárias, e a conclusão retoma a diferença entre gerar e receber poluição.

## Painel 1 Classes relativas de concentração anual

O valor atribuído a cada receptor corresponde à média das três médias anuais nativas do AERMOD. Em seguida, a distribuição dos receptores municipais é dividida pelos percentis 20, 40, 60 e 80. Para MP2,5, os cortes são aproximadamente 21,23, 29,40, 43,93 e 72,34 µg/m³. Q1 inclui valores até P20; Q2 vai de valores acima de P20 até P40; Q3 segue até P60; Q4 segue até P80; Q5 contém os valores acima de P80.

Essas faixas permitem reconhecer contrastes dentro do próprio campo modelado. Um receptor em Q1 pertence à parte inferior da distribuição municipal examinada, mas pode continuar com concentração elevada em termos sanitários ou normativos. Da mesma forma, estar em Q5 não significa que um evento crítico legal foi caracterizado. A classificação é relativa, condicionada ao cenário e ao poluente. Os cortes do MP10 são diferentes porque sua distribuição é diferente.

As áreas coloridas representam os suportes espaciais dos receptores. A quantidade de receptores em cada quintil tende a ser semelhante, mas a área de cada quintil não precisa ser 20% do município. Esse ponto ajuda a explicar por que uma cor pode ocupar uma região extensa sem indicar que a regra dos percentis foi aplicada incorretamente. As zonas municipais aparecem como referência de gestão, sem determinar os quintis no ajuste inicial.

A contribuição deste painel é substituir uma leitura visual uniforme por um gradiente interno verificável. Ele mostra onde concentrar a investigação seguinte, mas não explica sozinho a causa das maiores concentrações. Essa explicação depende dos grupos emissores, da meteorologia e da relação fonte-receptor.

## Painel 2 Perfis conjuntos por k-means

Aqui, cada receptor é descrito por seis valores: máximo horário, máximo diário e média anual para MP10 e para MP2,5. A transformação log(1+C) reduz a influência de amplitudes extremas, e a padronização evita que o indicador numericamente maior domine a distância. O k-means procura grupos de receptores com perfis semelhantes nesse espaço de seis dimensões.

A solução apresentada possui dois grupos e silhueta de aproximadamente 0,481. A silhueta descreve a separação dos grupos naquelas variáveis e não mede a precisão da concentração modelada. O algoritmo não recebe como instrução produzir um grupo de alta e outro de baixa poluição. Essa interpretação só pode ser atribuída depois de examinar os centróides e os valores originais. Por esse motivo, o mapa utiliza Group 1 e Group 2, evitando dar ao número do grupo uma hierarquia automática.

Os dois grupos também não equivalem aos cinco quintis. Quintis dividem uma variável segundo a ordenação de seus valores. O k-means combina várias variáveis para reconhecer perfis. A solução anterior de Ward com quatro indicadores respondeu a outra configuração de entrada e sua silhueta não deve ser comparada como se fosse uma melhoria ou piora do AERMOD.

A utilidade científica do painel é verificar se os padrões persistem quando se consideram, conjuntamente, períodos curtos e longos e as duas frações de partículas. O aparecimento de áreas descontínuas de uma mesma classe é permitido, porque as coordenadas não foram usadas como atributos do k-means. A continuidade necessária a regiões de gestão será examinada em uma etapa própria.

## Painel 3 Densidade de emissão nas zonas

Este é um resultado de massa, não de concentração. As 1.228 fontes do cadastro utilizado são intersectadas com as zonas. A massa das fontes de área é repartida pela área de interseção, a das fontes lineares pelo comprimento e a das fontes pontuais por sua localização, evitando duplicar pontos sobre limites. Para fontes de volume representadas por polígonos, utiliza-se o suporte cadastral disponível, sem afirmar que ele corresponde a uma superfície física de emissão comprovada.

Para o novo painel, a soma municipal de MP2,5 foi 3.330,9340163 t/ano. O total rateado recuperou esse valor com diferença numérica inferior a 0,000001 t/ano. A densidade de cada zona foi obtida dividindo sua massa em t/ano pela área em km². O maior valor zonal foi aproximadamente 236,91 t/ano/km². A barra usa valores até 250 t/ano/km² e uma progressão de amarelo para vermelho, abrangendo o máximo calculado.

Foram detectadas pequenas sobreposições do cadastro. A soma das áreas dos 311 registros é aproximadamente 304,0813 km², enquanto a união ocupa 304,0702 km². Para a emissão não ser contada duas vezes, o rateio desta figura atribui uma única vez cada parcela sobreposta, seguindo uma ordem determinística que preserva primeiro os fragmentos menores. Os identificadores originais foram mantidos. Essa é uma regra de tratamento geométrico e não uma alteração oficial do zoneamento.

Também existem 31 fragmentos menores que 1 m² no cadastro. Eles permanecem identificados, mas sua densidade exige cautela por depender de um denominador muito pequeno. Uma verificação futura do cadastro municipal é mais apropriada do que interpretar tais fragmentos como unidades autônomas de decisão. O detalhamento por fonte e zona foi salvo em planilha textual para permitir conferir cada parcela.

É importante distinguir densidade em t/ano/km² da entrada superficial em g/s/m². A primeira descreve a massa anual atribuída a uma unidade territorial. A segunda é uma taxa usada na representação física de determinadas fontes do modelo. Elas não podem ser trocadas na interpretação. A emissão zonal também não equivale à concentração recebida pela zona, pois parte do material pode ser transportada para outros receptores.

## Painel 4 Alta emissão e estabilidade

O limiar apresentado, aproximadamente 8,49545 t/ano/km², foi ajustado para separar células acima ou abaixo do P80 da concentração anual de MP2,5. Seu ajuste foi feito no suporte original das células de análise. Não se trata de 100 t/ano, não é um limite permissível e não representa a massa adicional que poderia ser licenciada. Ele é uma associação empírica do cenário, poluente, escala e dados utilizados.

O mapa traduz esse resultado para as zonas por interseção. A cor mostra a porcentagem da área de cada zona que coincide com células acima do limiar. Assim, uma zona com 60% de sua área nessa condição aparece na faixa >50-75%. Isso não significa que 60% de sua massa está acima de um limite, nem que toda a zona recebeu a mesma classe. Essa forma de apresentação conserva as diferenças internas que seriam perdidas se a média de uma zona muito extensa recebesse uma única decisão binária.

A estabilidade aparece como hachura nas células que trocam de classe dentro da faixa de cortes obtidos nas partições espaciais de validação. Os valores extremos dos dez cortes foram aproximadamente 7,10835 e 10,23432 t/ano/km². Uma célula abaixo ou igual ao menor corte permanece na outra classe em todos esses cortes. Uma célula acima do maior corte permanece alta em todos eles. As células entre os extremos são sensíveis à escolha do corte dentro desse conjunto de testes.

A hachura não é um intervalo de confiança, uma probabilidade de poluição ou uma nova classe de concentração. Ela identifica dependência da classificação em relação ao ajuste amostral espacial examinado. Em uma zona, a cor e a hachura respondem a perguntas diferentes: a cor resume a extensão da classificação principal; a hachura mostra onde essa classificação é menos estável quando o corte muda.

As partições utilizaram blocos de 2 e 4 km. A acurácia balanceada média nos conjuntos de teste foi aproximadamente 0,767, considerando igualmente a identificação de valores acima e abaixo do alvo. Esse desempenho indica associação útil no desenho avaliado, mas não elimina dependência espacial residual nem demonstra um efeito causal da emissão local. Também não substitui uma simulação de controle com alteração efetiva das fontes.

## Painel 5 Relação emissão-concentração

A matriz cruza concentração acima de P80 com emissão acima do corte associado a esse alvo. Ela cria quatro combinações. Alta emissão e alta concentração sinalizam coexistência de fontes concentradas e maior carga recebida no suporte analisado. Alta emissão com concentração fora da faixa superior identifica uma situação em que a contribuição pode se deslocar para outros locais ou variar conforme as condições meteorológicas. Alta concentração com emissão fora da faixa superior sugere investigar contribuições recebidas de outras áreas. A combinação restante não significa ausência de poluição.

Essas interpretações orientam hipóteses, sem demonstrar que toda concentração de uma célula é gerada pelas fontes dentro dela. Uma mineradora ou grupo distante pode contribuir muito para um receptor. Inversamente, uma fonte dentro de uma zona pode contribuir pouco para o receptor utilizado no indicador daquela zona em um determinado período. O detalhamento por grupo e os campos por direção do vento permitem investigar essa diferença.

A comparação entre os painéis de emissão e esta matriz deve respeitar a escala de análise. A densidade do painel 3 é uma média zonal calculada diretamente das fontes. A decisão da matriz foi ajustada nas células e depois relacionada às zonas. Por isso, não se deve esperar que cada cor zonal do painel de densidade corresponda exatamente a uma classe binária da matriz. Essa distinção é parte do cuidado com o problema da unidade espacial modificável.

Uma conclusão útil é que localização das emissões e localização das maiores concentrações são informações complementares. A associação espacial acrescenta uma estrutura territorial à análise; ela não autoriza converter a relação observada em uma regra linear universal de emissão e concentração.

## Painel 6 Regiões propostas de gestão

As funções propostas são prioridade receptora, controle de fontes, menor impacto relativo e acompanhamento. A prioridade receptora reúne células com concentração anual acima de P80. O controle de fontes destaca emissão acima do corte de P80 em células que não estão na faixa superior de concentração. O menor impacto relativo combina concentração até P40 e emissão até o corte associado a P40. As combinações restantes permanecem em acompanhamento.

Células do mesmo papel são agrupadas quando compartilham um segmento de fronteira, sem unir regiões que só se tocam em um vértice. Na referência anual de MP2,5, 202 receptores prioritários formaram 14 regiões, com aproximadamente 52,39 km². Essas regiões interceptam 137 registros de zoneamento. As 137 zonas não foram consideradas prioritárias em toda a sua extensão somente por essa interseção.

As quatro funções são propostas para interpretação e planejamento. Elas não substituem o zoneamento oficial, a avaliação de atendimento a padrões ou a análise do órgão ambiental. A delimitação mantém rastreabilidade até os receptores e permite discutir ações diferentes em áreas que geram emissões e áreas que recebem as maiores concentrações.

O monitoramento pode complementar a decisão sobre onde investigar ou ampliar a rede. Antes disso, precisam ser verificados período, disponibilidade e representatividade de cada estação. Uma região modelada sem estação não é uma região sem poluição observada; é uma área para a qual a evidência de campo disponível não oferece o mesmo apoio. A análise de saúde permanece na dissertação, mas foi mantida fora deste pôster para concentrar a comunicação nos resultados territoriais.

## Gráfico de contribuição e leitura da ABC

O gráfico do pôster resume a contribuição recebida nas 14 regiões receptoras prioritárias, ponderando as concentrações pela área dos suportes. Gerdau representa aproximadamente 74,6563%, Urbano Total 16,4811% e os demais grupos 8,8626%. Esses valores não representam a fração da massa municipal emitida por cada empreendimento. Também não são uma porcentagem de doença, de população exposta ou de responsabilidade jurídica.

Na curva ABC completa, os grupos aparecem no eixo horizontal em ordem decrescente de contribuição para o recorte receptor. A altura de cada barra informa a participação individual do grupo. A linha informa a soma acumulada das participações da esquerda para a direita. É normal que o mesmo nome seja mencionado no eixo e na interpretação do resultado, pois a barra identifica o grupo cuja contribuição está sendo discutida.

A classe A reúne os primeiros grupos até alcançar ou ultrapassar 80% do acumulado. A classe B prossegue até 95%, e a classe C contém o restante. Não se impõe que 20% das empresas sejam A. Neste recorte agrupado, Gerdau e Urbano Total já somam aproximadamente 91,14%, razão pela qual são centrais à explicação. A ABC individual de uma das 14 regiões pode ter outra composição, que não deve ser confundida com o agregado do pôster.

Urbano Total inclui vias, núcleos urbanos e ferrovias. As vias incluem ressuspensão e combustão. Esse agregado não representa apenas escapamento e não deve ser atribuído automaticamente à prefeitura. Além disso, ele se sobrepõe aos três subgrupos urbanos. AEX é outro agregado sobreposto, com áreas expostas de diferentes empresas. Somar empresas, Urbano Total, seus subgrupos e AEX duplicaria contribuições.

## Moran, correlograma e incerteza

O Moran global anual de MP2,5 foi aproximadamente 0,754, com p de 0,001. Isso indica organização espacial no teste especificado, sem demonstrar a precisão do AERMOD ou identificar a empresa responsável pelo padrão. O Moran local distingue associações alto-alto, baixo-baixo e contrastes, aplicando correção de falsas descobertas. Uma célula não significativa não equivale a baixa concentração.

O correlograma é um gráfico, não uma pluma espacial. Ele apresenta a associação em função da distância e ajuda a reconhecer escalas de semelhança. A estabilidade dos conjuntos alto-alto foi examinada trocando oito vizinhos por quatro e doze. Os Jaccard de MP2,5 foram aproximadamente 33,3% e 64,1%, respectivamente. A diferença evidencia que os limites locais dependem da vizinhança. Isso recomenda evitar fronteiras operacionais rígidas sem avaliação adicional.

No estudo existem incertezas de inventário, geometria, tempo de emissão, meteorologia, representação do terreno, proximidade de receptores e escolha da unidade espacial. O teste de estabilidade do corte aborda apenas uma parte delas. A concordância observado-modelado aborda outra dimensão. A transformação dos indicadores em classes relativas melhora a discriminação interna, mas não corrige o viés da concentração por si só.

## Escala, tamanho físico e qualidade

O enquadramento geográfico foi preservado. A mudança de 1:170.000 para 1:200.000 nesta revisão decorre da redução física dos seis mapas de resultado para caberem em três linhas no pôster de 120 por 90 cm. Os mapas do método permanecem em 1:440.000 em seu tamanho físico. As escalas foram calculadas pela largura geodésica do encarte e pela largura real da figura no PPTX, evitando apenas trocar o texto da caixa.

A escala numérica vale quando o pôster é impresso no tamanho original e sem ajuste adicional à página. Se houver redução, a escala numérica muda novamente. A barra de distância acompanha a redução e continua utilizável. Os SVG preservam as geometrias e a tipografia vetorial no PDF. Ao apresentar uma imagem de prévia na tela, sua aparência não deve ser confundida com a resolução do PDF vetorial final.

## Padrão de apresentação oral

Uma apresentação breve pode durar quatro minutos. Nos primeiros 35 segundos, explicar a necessidade de relacionar fontes, áreas receptoras e planejamento territorial. Nos 45 segundos seguintes, percorrer os quatro passos metodológicos sem detalhar fórmulas. Dedicar um minuto à primeira e à segunda linha de mapas, distinguindo concentração, massa e estabilidade. Usar mais um minuto para a matriz, as regiões propostas e o gráfico de contribuições. Encerrar em 40 segundos com aplicação, limites e próximos testes.

Na conversa ampliada, a ordem deve ser a mesma, mas cada mapa pode receber um a dois minutos. Comece dizendo o que foi calculado, mostre como ler a cor e somente depois explique o que o resultado permite concluir. Ao final de cada painel, conecte-o ao próximo. A densidade descreve geração de massa; o limiar testa sua associação com o campo modelado; a matriz distingue combinações; a análise de grupos investiga quem contribui para a concentração recebida.

Para uma pergunta sobre magnitude, volte à avaliação observado-modelado e deixe claro que as classes relativas não são uma calibração. Para uma pergunta sobre licenciamento, explique a função orientadora do diagnóstico e a necessidade de avaliar cenários e requisitos pelo órgão competente. Para uma pergunta sobre vento, diferencie envelope de máximos condicionados de uma pluma simultânea. Essa sequência mantém a apresentação técnica e permite reconhecer os limites sem perder a contribuição principal.

## Perguntas frequentes

Por que não manter apenas atendimento e não atendimento? Essa avaliação continua necessária, mas pode discriminar pouco quando grande parte do cenário supera o referencial. As classes relativas acrescentam contraste territorial e não substituem os padrões.

O k-means descobriu as zonas oficiais? Não. Ele agrupou perfis de concentração nos receptores. A etapa posterior relacionou esses perfis e as regiões propostas aos 311 registros do zoneamento.

Uma zona de alta emissão é necessariamente a que recebe maior concentração? Não. Dispersão, localização, altura e características das fontes podem separar geração e recepção. É justamente essa diferença que motiva a matriz e a avaliação dos grupos.

A hachura indica erro na emissão? Não. Ela indica que a decisão alta/outra emissão muda quando usamos cortes diferentes obtidos na validação espacial. Uma auditoria de inventário é necessária para avaliar erro na massa.

Os cenários direcionais são novas modelagens? Não. Eles filtram e resumem resultados já simulados usando a direção meteorológica associada aos eventos. Alterar o perfil de emissão ou testar redução de uma fonte exige nova simulação.

Qual é a contribuição científica? Mostrar como a escala, a associação espacial e as contribuições recebidas modificam a interpretação que seria obtida apenas pela concentração ou pela massa local. A confiabilidade dessa contribuição é examinada por consistência numérica, comparação observado-modelado e testes de estabilidade, que são dimensões distintas.


## Todos os grupos e suas participações nas prioridades receptoras

A tabela apresenta os 24 grupos exclusivos do recorte anual de MP2,5. Todas as participações utilizam as mesmas regiões e ponderação por área. Valores pequenos não significam ausência de emissão ou irrelevância em outro receptor ou período. Os processos específicos de cada empresa devem ser conferidos no inventário, sem atribuir uma tipologia a partir apenas de seu nome.

| ID do grupo | Empreendimento ou agregado | Concentração recebida (%) |
| --- | --- | --- |
| GERDAU | Gerdau | 74,65627 |
| URB | Urbano Total | 16,48113 |
| VALE_FAB | Vale Fábrica | 3,47221 |
| LGA | LGA Mineração | 1,52957 |
| CSN-CDP | CSN Casa de Pedra | 0,97735 |
| SCOF | SCOF | 0,91772 |
| FERRO | Ferro+ | 0,87629 |
| VALE_VIG | Vale Viga | 0,65512 |
| CDA | CDA Logística | 0,16727 |
| ECOMIN | Ecomining América | 0,11216 |
| CSN-PIR | CSN Namisa/Pires | 0,06530 |
| WGM | WG Mineração | 0,05220 |
| TERRA-MI | Terra Minas | 0,01595 |
| NOGD | Nogueira Duarte | 0,00725 |
| SAPPORO | Sapporo Indústria e Comércio | 0,00522 |
| TERRAMAR | Terramares | 0,00410 |
| LL-TRANS | LL Transportes | 0,00160 |
| LM-MIN | LM Mining Company | 0,00126 |
| COC | Concrelagos Concreto | 0,00061 |
| RODEIRO | Rodeiro | 0,00053 |
| MONT-MIN | Monteminas Minérios | 0,00044 |
| COOPERA | Cooperauto | 0,00021 |
| BVC | BVC Transportes | 0,00016 |
| SILVANO | Silvano Transportes | 0,00007 |

O grupo ALL reúne todas as fontes. AEX reúne áreas expostas distribuídas entre diferentes empreendimentos e se sobrepõe aos grupos empresariais. Na execução auditada, o arquivo horário consolidado utilizado pelo autor contém 252 fontes; a antiga expectativa de 243 fontes do dicionário não deve ser usada como contagem da execução. URB-FER, URB-NUC e URB-VIA detalham ferrovias, núcleos e vias, respectivamente, e se sobrepõem ao Urbano Total. A presença de ALL, AEX e dos subgrupos explica por que os 29 grupos de saída não equivalem a 29 parcelas independentes para soma.

Os resultados atuais de participação são atribuíveis ao cenário modelado e ao recorte de prioridades receptoras. Para verificar uma empresa em detalhe, deve-se selecionar a região, recuperar sua contribuição naquele receptor ou conjunto de suportes e compará-la ao ALL do mesmo período. A massa emitida pela empresa dentro da zona é consultada separadamente no rateio por fonte, sem usar a contribuição de concentração como substituta da massa.

## Arquivos para consulta e reprodução

Pôster editável e PDF em E:/projeto/output/13_cmas_posters/Congonhas/Poster_CMAS_Session12_Congonhas. O detalhamento das emissões está em Rateio_emissoes_MP25_por_fonte_zona.csv e Emissoes_densidade_sensibilidade_por_zona.csv, nessa mesma pasta. A auditoria e a base geográfica acompanham esses arquivos. Os cortes originais e a validação estão em E:/projeto/output/16_revisao_pos_banca/limiares_cinco_faixas_validacao.csv. O visualizador privado permanece na pasta visualizador dos resultados pós-banca.

## Referências e apoio à apresentação

A interpretação deve manter a distinção entre contribuição, sensibilidade e resposta ao controle discutida por Clappier et al. (2017), Geoscientific Model Development, DOI https://doi.org/10.5194/gmd-10-4245-2017 . O Moran local tem como referência Anselin (1995), DOI https://doi.org/10.1111/j.1538-4632.1995.tb00338.x . As referências recentes e os textos completos já organizados na revisão pós-banca permanecem na biblioteca do projeto, sem duplicar seus arquivos neste guia. O exemplo de episódios de poeira de Ribeiro et al. (2025), DOI https://doi.org/10.1080/09593330.2025.2556349 , pode apoiar a discussão de meteorologia e episódios, mas não transforma o recorte direcional desta análise em um modelo preditivo equivalente.

O agradecimento da CAPES segue a formulação oficial em inglês, Finance Code 001, disponível em https://www.gov.br/capes/pt-br/centrais-de-conteudo/logomarca . O apoio do Mover Programme, Track V, project [27192*83], foi mantido conforme o resumo expandido.
