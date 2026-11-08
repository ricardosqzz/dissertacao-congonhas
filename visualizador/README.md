# Visualizador privado de Congonhas

Este visualizador mantém os resultados no repositório privado, sem publicar um site. Para usar a versão pronta, abra **Actions**, selecione a última execução de **Gerar Word e livro** e baixe **Visualizador-privado** em **Artifacts**. Extraia o ZIP inteiro e abra `index.html`. Não é necessário instalar programas, iniciar servidor ou obter chave de API.

A rosa dos ventos permite escolher N, NE, L, SE, S, SO, O ou NO. As pétalas usam os mesmos vetores da entrada WRF/AERMET e as mesmas classes de velocidade da apresentação. O recorte analítico tem setores de 45 graus. A rosa gráfica conserva setores de 30 graus e recebe o destaque angular da seleção. A opção Toda a meteorologia mostra a referência geral, incluindo o indicador anual. O menu Produto troca entre concentrações, quintis, Moran, emissão-concentração, gestão e demais análises.

As imagens WebP são prévias para leitura. Os arquivos PDF e SVG para publicação continuam em `E:/projeto/output/16_revisao_pos_banca`. A escala numérica impressa na figura se refere ao tamanho nativo. Na tela ou em outra dimensão de impressão, a barra de distância acompanha o redimensionamento.

Para ajustar a apresentação, edite `index.html`. `dados.js` e `catalogo.json` são o catálogo gerado. `partes/` contém somente as prévias, divididas em pequenos volumes para armazenamento. A rotina `ferramentas/preparar_visualizador.py` reúne os volumes em um único pacote pronto para baixar e verifica todos os arquivos. Os dados horários, inventários completos, documentos de terceiros e informações individuais de saúde não fazem parte desse pacote.

Não ativar GitHub Pages ou o fluxo de publicação do livro. A opção do autor é manter todos os materiais privados.
