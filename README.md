# Dissertação de Congonhas

Este é o local de escrita da dissertação de Ricardo Silva Queiroz e do artigo científico associado. Os capítulos editáveis geram livros de leitura e um único arquivo Word para cada documento. A base pós-banca foi preservada e complementada com a referência meteorológica completa e a organização metodológica pelos quatro objetivos.

O repositório é privado: [ricardosqzz/dissertacao-congonhas](https://github.com/ricardosqzz/dissertacao-congonhas). A pasta local é `E:/projeto/dissertacao`. [O artigo fica em artigo/](artigo/README.md). [O relatório dos recortes de vento fica em metodologia/](metodologia/recortes-vento.md).

## Onde editar

| Parte | Arquivo |
| --- | --- |
| Introdução | [index.qmd](index.qmd) |
| Objetivos | [02-objetivos.qmd](capitulos/02-objetivos.qmd) |
| Revisão da literatura | [03-revisao.qmd](capitulos/03-revisao.qmd) |
| Material e métodos | [04-metodologia.qmd](capitulos/04-metodologia.qmd) |
| Resultados e discussão | [05-resultados-discussao.qmd](capitulos/05-resultados-discussao.qmd) |
| Conclusões | [06-conclusoes.qmd](capitulos/06-conclusoes.qmd) |
| Recomendações | [07-recomendacoes.qmd](capitulos/07-recomendacoes.qmd) |
| Referências | [08-referencias.qmd](capitulos/08-referencias.qmd) |

Abra o capítulo no GitHub, clique no lápis, altere o texto e confirme em **Commit changes**, descrevendo a mudança. O histórico permite comparar e recuperar versões. Também é possível pressionar `.` no repositório para abrir o editor do GitHub. O acesso de edição depende de permissão de escrita na conta ou no repositório.

As alterações são compartilhadas por versões salvas, sem edição simultânea como no Google Docs. O Codex poderá atualizar estes mesmos arquivos quando o acesso ao GitHub estiver conectado. Antes de começar uma revisão, deve sincronizar as alterações existentes para preservar o que o autor escreveu.

## Como escrever

O texto usa Markdown. Uma linha iniciada por `#` é um capítulo; `##` indica uma seção. A numeração é gerada automaticamente. Para negrito, use `**texto**`; para itálico, `*texto*`. Escreva `MP~10~`, `MP~2,5~` e `O~3~` para obter os índices inferiores no livro e no Word. Os espaços reservados às figuras foram mantidos. As referências atuais continuam no capítulo próprio, sem modificação bibliográfica automática.

## Word e livro de leitura

Cada alteração na branch `main` aciona a geração do Word e dos livros HTML. Abra **Actions**, selecione a execução de **Gerar Word e livro** e baixe **Dissertacao-Word**, **Artigo-Word**, **Livro-HTML** ou **Artigo-HTML** em **Artifacts**. Cada Word é um único documento; o artigo usa entrelinha dupla e numeração contínua de linhas. O livro baixado pode ser aberto pelo arquivo `index.html` após descompactação.

Localmente, com Quarto instalado, execute:

```text
quarto render --to html --output-dir _book/html
quarto render --to docx --output-dir _book/word
python ferramentas/ajustar_word.py _book/word/Dissertacao_Congonhas.docx
```

O Word fica em `_book/word/Dissertacao_Congonhas.docx`. O modelo de estilos em `modelos/referencia-smarh.docx` deriva do documento atual, que foi preparado a partir do `instrdt` do programa. Mantém A4, margens de 3 cm à esquerda e acima e 2 cm à direita e abaixo, Arial 12 e espaçamento de 1,5 no corpo. A paginação, elementos pré-textuais, referências cruzadas e diagramação final devem ser conferidos antes do depósito. A exportação não substitui essa conferência.

O Word exportado pode ser editado para entrega, mas suas mudanças não retornam automaticamente aos capítulos. Para continuar a escrita compartilhada, incorpore essas mudanças ao texto-fonte. O Word não deve virar uma segunda versão editorial independente.

Para gerar os quatro produtos de uma vez, use `python ferramentas/gerar.py` após instalar `requirements-editoriais.txt`. Nesta máquina, o atalho local é `E:/projeto/codigo/exportar_textos.ps1`. Os livros ficam em `_book/html/index.html` e `artigo/_book/html/index.html`; os Word ficam nas respectivas pastas `_book/word/`.

## Publicação do livro

Um repositório privado já permite escrita compartilhada e geração dos arquivos. A publicação de um site de leitura é uma etapa separada. O fluxo **Publicar livro** é manual e exige a variável de repositório `PUBLICAR_LIVRO=true`; ele não publica automaticamente ao editar o texto. Antes de ativá-lo, devem ser escolhidos o público e as permissões. GitHub Pages em plano gratuito exige repositório público. Em repositórios privados, as condições dependem do plano, e a privacidade do site deve ser verificada separadamente.

Os links de edição estão configurados para este repositório. Se o endereço mudar, execute `python ferramentas/vincular_github.py https://github.com/CONTA/REPOSITORIO`. Isso configura os links dos capítulos e, quando houver uma cópia Git local autenticada, sua origem remota. A integração do Codex também pode ler e editar os arquivos diretamente pela conexão com o GitHub, sem depender da autenticação do Git no terminal.

[Pôster CMAS](poster/README.md)

## Organização e rastreabilidade

`capitulos/` e `index.qmd` são o texto corrente. `modelos/` contém o modelo de Word; `ferramentas/` contém apenas as rotinas editoriais. `_book/` contém exportações regeneráveis e não entra no histórico Git. O manifesto de migração registra a base, seus hashes e a correspondência dos capítulos.

Os mapas e os dados permanecem nas pastas analíticas de `E:/projeto`. Este repositório não carrega os arquivos POST, EMI, os inventários integrais, as bases de monitoramento ou PDFs de artigos. Os originais do autor e o seminário concluído foram preservados. A cópia anterior do texto migrado fica em `E:/projeto/descontinuado/2026_11_08_editorial_e_poster`, conforme o manifesto local.

Documentação: [livros e Word no Quarto](https://quarto.org/docs/books/book-output.html), [edição no GitHub](https://docs.github.com/en/repositories/working-with-files/managing-files/editing-files), [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).

