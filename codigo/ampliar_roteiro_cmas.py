# ENTRADA: output/13_cmas_posters/Congonhas/preparacao_apresentacao/Roteiro_Session12_PT_EN.md.
# SAÍDA: mesmo roteiro, inglês ampliado sobre metodologia e interpretação; versão anterior em descontinuado.
# CAMINHOS: EMI_PROJECT_ROOT ou codigo/caminhos_projeto.json; não altera o seminário encerrado, o pôster ou as concentrações.
from pathlib import Path
import datetime,shutil
from caminhos_congonhas import raiz_projeto
R=raiz_projeto();P=R/'output/13_cmas_posters/Congonhas/preparacao_apresentacao/Roteiro_Session12_PT_EN.md'
METHOD='''For interpretation, we keep three levels separate. The emission inventory describes the sources and their assumed rates. AERMOD estimates transport and dilution under the meteorological conditions. The spatial analysis then summarises those predictions into relative classes, source contributions and candidate management regions. A change in a clustering method does not correct the emissions or the atmospheric model. It changes the way the same modelled information is organised.

The annual indicator preserves the three native annual means, rather than averaging only the largest daily or hourly values. In the joint-profile analysis, hourly and daily maxima deliberately describe different features of the concentration field. We therefore state which indicator enters each map. Neither the quintile boundaries nor the k-means labels should be interpreted as health thresholds.

'''
DISCUSSION='''The management interpretation is also conditional on the modelled scenario. Source contributions describe the concentration received at the selected support, not the percentage of total inventoried mass emitted by a company. Overlapping aggregate groups cannot be added as though they were independent sources. For example, Urban Total already combines the urban subgroups represented in the inventory.

We are continuing to investigate temporal emission assumptions and the atmospheric representation, including conditions associated with weaker nocturnal dilution. A constant source rate can interact with a shallow or weakly mixed layer and produce higher near-ground concentrations without demonstrating that the real emission increased at night. Existing station-based diagnostics in the wider Congonhas project are distinct from the relative screening shown here. Refinement will require an explicitly documented rerun and a comparison on compatible observed-model time and space support; a lower plotted percentile alone is not a correction of the underlying simulation.

'''
def main():
 text=P.read_text('utf8')
 if METHOD.strip() in text:return
 dest=R/'descontinuado'/datetime.datetime.now().strftime('%Y%m%d_%H%M%S')/'roteiro_cmas'/P.name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(P,dest)
 start=text.index('## Full presentation in English');left=text[:start];right=text[start:];right=right.replace('The first map shows',METHOD+'The first map shows',1);right=right.replace('The study makes the distinction',DISCUSSION+'The study makes the distinction',1);text=left+right;text=text.replace('conferido em 14 de novembro de 2026','conferido em 18 de novembro de 2026');P.write_text(text,encoding='utf8');print('Roteiro Session 12 ampliado')
if __name__=='__main__':main()
