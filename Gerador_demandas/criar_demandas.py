import pandas as pd
import numpy as np
import datetime
  

init_date = datetime.datetime(2015, 1, 1)

K = 208
  
# timedelta() gets successive dates with 
# appropriate difference
date = [init_date + datetime.timedelta(weeks=i) for i in range(K)]


#funcao_demanda = lambda i: 10000+5*np.log(i+6)+20*np.cos(6.2831*i/50+1.8849)+np.random.normal(0, 8,1)[0]
funcao_demanda = lambda i: 10000+200*np.cos(6.2831*(i+10)/50+1.8849)+np.random.normal(0, 30,1)[0]
demandas = [funcao_demanda(i) for i in range(K)]
  

df_demandas = pd.DataFrame({'date':date,'demandas':demandas})
df_demandas.to_csv('C:/Users/marcio/Documents/Prev_For_ULS/Resultados/tabelas/Demandas_treinamento/demandas')
