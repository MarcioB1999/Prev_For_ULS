# Prev_for_ULS

Esse Projeto tem como a principal intenção analisar como os resultados do problema de otimização ULS irão se comportar ao receber previsões de demandas.

## Fluxograma
Ao se executar algum algoritmo de uma fase, com exceção de algoritmos de análises, terá que se executar todos outros algoritmos de fases posteriores. Algoritmos paralelos não necessitam serem excutados um após outro, pois um não influencia no resultado do outro.

### Fase Inicial

A primeira fase consiste basicamente em gerar demandas para o treinamento das previsões. Essa fase esta na pasta Gerador_demandas, que possui o gerador, e uma análise da serie temporal gerada. 

### Fase de Previsão

A partir da serie gerada na fase anterior, treinamos os modelos de series temporais, Sarimax e Nural Prophet. Essa fase esta na pasta Modelos_previsao, que contém um arquivo para cada modelo de previsão, que além de prever, possuem fases de teste, com análise de métricas e resíduos. A pasta possui tambem um arquivo para análise de comparação entre as previsões geradas.

![GHITL](https://github.com/MarcioB1999/Prev_For_ULS/blob/main/Arquivos_Auxiliares/FluxogramaProjeto.png)

### Fase de Otimização

A partir das demandas previstas iremos utilizar no modelo de pi ULS, e obter seus resultados para fase final. Uma observação é que as demandas geradas na fase inicial tambem passaram por essa fase, para seus resultados servirem como base histórica do passado, para analisar como os resultados dos modelos com dados previstos estão se diferenciando dele.

### Fase Final

Essa fase basicamente consiste em analisar os resultados obtidos dos três modos e fazer comparações.

$\textbf{Obs:}$ As duas últimas fases estão na pasta Modelo_pi
