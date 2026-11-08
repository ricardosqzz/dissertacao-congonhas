# Fonte editorial da dissertação

- Esta pasta contém o texto corrente da dissertação. Editar os capítulos `.qmd`; o Word é uma exportação.
- Preservar os quatro objetivos, a redação autoral e as incertezas. Não reescrever o seminário entregue.
- Antes de editar, verificar alterações locais e remotas. Sincronizar apenas sem sobrescrever trabalho humano; conflitos devem ser resolvidos pelo conteúdo.
- Não reimportar automaticamente Word sobre capítulos editados. Mudanças feitas no Word precisam de incorporação explícita aos capítulos.
- Manter figuras separadas até solicitação do autor. Insumos pesados e análises permanecem em E:/projeto, fora deste repositório editorial.
- Referências e citações foram preservadas na forma textual da base. Não inventar registros bibliográficos nem converter citações automaticamente sem conferência.
- Padrões relativos e limiares associativos não são classificação legal nem emissões permissíveis. Não afirmar nova simulação ou calibração sem execução.
- Gerar com `quarto render --to html --output-dir _book/html` e `quarto render --to docx --output-dir _book/word`; finalizar Word com `python ferramentas/ajustar_word.py _book/word/Dissertacao_Congonhas.docx`.
- Nunca incluir credenciais, dados individuais de saúde, referências integrais protegidas, caches ou saídas pesadas da modelagem.
- Arquivar produtos gerados substituídos em E:/projeto/descontinuado, com manifesto; preservar arquivos-base.
- O autor autorizou tornar o repositório público em 08/11/2026. Publicar o livro, o artigo e o visualizador no GitHub Pages, mantendo os dados brutos e as referências integrais fora do repositório. O fluxo publicar-livro.yml atualiza o site após alterações na main. _visualizador/ e _site_publico/ são exportações regeneráveis.

