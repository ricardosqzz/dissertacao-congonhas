# Artigo CMAS

Texto integral corrente, com MP10 e MP2,5. Editar os arquivos de `secoes/` e o resumo em `index.qmd`. O Word é gerado em um único arquivo, com fonte Arial 12, entrelinha dupla e numeração contínua de linhas. As figuras permanecem separadas e são chamadas nos locais previstos. A submissão final depende da revisão científica e das instruções do periódico.

```text
quarto render --to html --output-dir _book/html
quarto render --to docx --output-dir _book/word
python ../ferramentas/ajustar_word.py _book/word/Artigo_CMAS_Congonhas.docx --artigo
```

O título do artigo pode diferir do título oficialmente registrado para o pôster. A lista de autores da versão corrente, inclusive Leila, foi preservada.
