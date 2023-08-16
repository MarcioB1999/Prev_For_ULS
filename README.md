# Prev_for_ULS

É razoável se imaginar uso de previsões para modelo ULS que tem o propósito de planejar a linha de produção, ou seja, um serviria como complemento um do outro, em se tratar do planejamento da empresa. Pois com as previsões, teríamos o olhar para o futuro, e com ULS obtemos uma maneira de como lidar com esse futuro, como alocar os recursos.
 Portanto o papel principal desde trabalho é de predição das demandas para o ULS, e analisar o comportamento dos resultados, verificar como as variações que ocorrem entre as previsões afetam os resultados. Visto que, modelos de previsão, proporcionam diferentes previsões, dependendo de vários fatores, desde, algoritmos diferentes, parâmetros diferentes, ou até mesmo entre aprendizagens do mesmo algoritmo.

Pois de que seria útil um modelo para planejamento, ser pouco flexivel de modo a não aceitar de maneira razoável pequenas variações nas previsões.





<img height="250em" src="https://github.com/MarcioB1999/Prev_For_ULS/blob/main/Resultados/img/Demandas.png/">

$\psi\left(i\right) = \lfloor100+10\cos\left(\frac{2\pi\left(i+10\right)}{50}+0.6\pi\right)+\varepsilon_{i}\rfloor$, $i=1,...,52$

com $\varepsilon_{i}\sim N\left(0,1\right)$, $i=1,...,52$

<img height="250em" src="https://github.com/MarcioB1999/Prev_For_ULS/blob/main/Resultados/img/prev_testes.png">


|Métricas | Neural Prophet | Sarima    |
|---------|----------------|-----------|             
|RMSE     | $1.043$        | $1.0286$  |
|MAE      | $0.8573$       | $0.8335$  |
|MAPE     | $0.8646$%     | $0.8409$%|

<img height="250em" src="https://github.com/MarcioB1999/Prev_For_ULS/blob/main/Resultados/img/IC.png">
