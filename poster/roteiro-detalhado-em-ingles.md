# CMAS poster presentation and discussion notes

ATTAINMENT-STATUS SCREENING OF PARTICULATE MATTER TO SUPPORT AIR QUALITY MANAGEMENT IN A MINING-INFLUENCED MUNICIPALITY

This guide supports the current PM2.5 poster. It is a speaking guide and a detailed question-and-answer reference, rather than text to be placed on the poster. The joint clustering panel uses both PM10 and PM2.5; the other main panels focus on PM2.5.

## Four-minute presentation

Good morning. Our study investigates how particulate-matter information can support air quality management in Congonhas, a mining-influenced municipality in Brazil. A concentration map shows where pollution is received, while an emission inventory shows where source mass is generated. These locations do not necessarily coincide. Our purpose is to connect the two perspectives and retain the municipality’s 311 zoning records as the management reference.

The method has four steps. First, we summarized the existing AERMOD scenario over 2021-2023. Second, we examined concentration patterns through five percentile classes, joint clustering and spatial association. Third, we related emission density to concentrations and examined the source contributions received in priority areas. Finally, we intersected those results with the municipal zoning, preserving differences within large zones.

The first map divides annual PM2.5 concentrations into five relative classes. The upper class contains concentrations above the municipal P80, approximately 72.3 micrograms per cubic metre in this scenario. These are descriptive classes. They do not replace ambient air quality standards, and a lower relative class does not mean that air quality is safe.

The second map uses k-means to identify joint concentration profiles. It includes hourly maxima, daily maxima and annual means for both particulate fractions. Two groups were selected, with a silhouette of approximately 0.481. This value describes separation between the groups, rather than the accuracy of the dispersion model.

The next two panels introduce emission information. Source masses were allocated to zones according to their geometry and divided by zone area, recovering approximately 3,330.93 tonnes per year of PM2.5 within the municipality. The numerical panel shows the cuts associated with the four concentration percentile targets. High emission was defined above approximately 8.50 tonnes per year per square kilometre for the P80 target, while the cuts from spatial validation ranged from 7.11 to 10.23. These are empirical associations for this scenario and spatial support, not permissible emission limits.

The last two panels combine emission and concentration. High local emission can coexist with concentrations outside the upper relative class, while a receiving area can have high concentrations and lower local emissions. The resulting management roles distinguish receiving priorities, source-control areas, lower relative impact and follow-up. For annual PM2.5, 202 priority receptors formed 14 contiguous regions, covering approximately 52.4 square kilometres and intersecting 137 zoning records.

Within those receiving priorities, Gerdau contributed approximately 74.7 percent of modelled concentrations, Urban Total 16.5 percent and the other groups 8.9 percent. These are area-weighted concentration shares, not shares of municipal emitted mass. Urban Total combines road resuspension and combustion, urban nuclei and railways.

The main contribution is a traceable distinction between generating areas and receiving areas. Relative patterns, source contributions and zoning provide complementary information for management planning. The boundaries remain conditional on the model scenario, emission inputs and spatial choices. New emission-timing simulations and independent observational evaluation are required before interpreting these results as operational control scenarios. Thank you.

## Explaining the six maps in more detail

The concentration classes describe the distribution across municipal receptors. Equal numbers of receptors in quintile classes do not imply equal land areas because receptor supports have different sizes. Annual means are based on the three native annual model outputs. We do not replace those means with an average that changes the model’s calm-hour treatment.

The joint profile map is independent of percentile ranking. K-means groups receptors by similarity across six transformed and standardized indicators. Coordinates are not input variables, so a group may appear in separate parts of the municipality. The numbers Group 1 and Group 2 are labels, not a legal severity order. Their interpretation depends on the fitted profiles.

The emission-density map uses the actual source geometries. Area sources are split by intersection area, linear sources by length, and point sources are allocated once. Polygonal representations of volume sources are treated as spatial supports, with their physical limitations documented. Small cadastral overlaps are handled deterministically to avoid duplicate mass. The maximum zonal PM2.5 density is approximately 236.91 tonnes per year per square kilometre.

The high-emission panel reports the numerical cut fitted at the original receptor-cell support. The four concentration targets P20, P40, P60 and P80 were associated with emission-density cuts of approximately 1.15, 2.05, 7.06 and 8.50 tonnes per year per square kilometre. Applying the same cuts directly to a mean over a much larger zone would change the statistical support and require a new assessment. The complementary area-share map remains available separately.

Spatial validation used blocks of two and four kilometres. The fitted cuts ranged from approximately 7.11 to 10.23 tonnes per year per square kilometre. The numerical range describes variation across these fits. The complementary map uses hatching to show cells that can change classification within that range. The mean balanced accuracy in the spatial test sets was approximately 0.767. The range is descriptive of the tested partitions and should not be called a confidence interval or a probability of high pollution.

The bivariate panel identifies combinations that deserve different investigations. High emission with lower relative concentration can motivate examination of contributions to other receiving areas. High concentration with lower local emission can motivate investigation of incoming contributions. Neither combination proves a transport pathway or assigns legal responsibility. Group-specific concentrations and event-linked wind information are needed to support the interpretation.

The management regions are proposed analytical roles. Receiving priority is defined by concentration above P80. Source control combines high emission with concentrations outside the upper class. Lower relative impact combines concentration and emission below the corresponding lower targets. Remaining combinations are assigned to follow-up. These roles do not replace official zoning or the environmental authority’s assessment.

## Source contributions and the ABC curve

Each contribution is the concentration from a group received at the receptors in the selected area. For regional aggregation, concentrations are weighted by receptor-support area. Dividing the summed group contribution by the summed ALL concentration gives the regional share. This differs from a simple average of local percentages and from a fraction of inventory mass.

The ABC curve sorts groups from the largest to the smallest share. Bars show individual shares and the line shows their cumulative sum. Class A continues until the cumulative contribution reaches or crosses 80 percent. Class B continues until 95 percent, and Class C contains the remaining contribution. We do not impose a fixed proportion of companies in each class.

Companies and Urban Total form the exclusive partition used to check closure against ALL. AEX overlaps the companies, and the urban subgroups overlap Urban Total. They can be reported as diagnostic breakdowns but must not be added again. The displayed three-bar summary pools the smaller groups only for readability; their individual results remain available in the study guide.

## Spatial association and uncertainty

Annual PM2.5 Moran’s I was approximately 0.754, with a permutation p-value of 0.001. This supports spatial organisation under the specified neighbourhood and transformation. It does not establish that modelled concentrations are unbiased. Local Moran classifications use multiple-testing adjustment, and non-significant cells are not labelled as low pollution.

Neighbourhood sensitivity is important. For PM2.5, overlap between high-high receptor sets was approximately 33.3 percent when comparing four with eight neighbours and 64.1 percent when comparing twelve with eight. Those changes caution against treating a single statistical boundary as an operational boundary without further assessment.

The main remaining uncertainties concern source mass and geometry, emission timing, meteorology, receptor proximity, terrain representation and spatial support. A percentile transformation does not correct the underlying concentration bias. A sensitivity map of classification cuts addresses only one part of this uncertainty, while comparison with observations examines another part.

## Wind-sector results, when asked

Wind directions describe where the wind comes from. The directional hourly maps retain the maximum at each receptor among eligible hours in the selected sector. Different receptors can reach their maxima at different times, so the map is an envelope rather than a simultaneous plume. Daily directional results use complete daily averages on days meeting the study’s persistence criteria. They are not averages of only the selected-direction hours within each day.

The complete three-year reference includes 24,892 valid directional hours and 1,075 eligible days. Only 463 days met the directional persistence criteria. Therefore, a daily maximum from the complete meteorology can exceed all daily directional envelopes. Unequal numbers of hours or days across sectors must be considered before comparing their maxima.

## Acknowledgements

We acknowledge UTFPR, IAG/USP, UFMG, UNIFEI, UERJ, EPUSP and UFSC; VOLKSWAGEN do Brasil Indústria de Veículos Automotores LTDA, RASTECH Automação e Comércio LTDA, Robert BOSCH Limitada and STELLANTIS Automóveis Brasil LTDA; and the Research Development Foundation (Fundep), coordinator of the Mover Programme, Track V, project [27192*83].

This study was financed in part by the Coordenação de Aperfeiçoamento de Pessoal de Nível Superior - Brasil (CAPES) - Finance Code 001.

## Presentation reminders

Point to the map, define what the colour represents, and then explain its implication. Distinguish relative classes from standards, emission mass from received concentration, and sensitivity testing from a new model run. If asked whether the model has been calibrated, explain that the current analyses diagnose the existing scenario and that new documented emission-timing runs are still required. The health assessment remains part of the dissertation and is intentionally outside the scope of this poster.
