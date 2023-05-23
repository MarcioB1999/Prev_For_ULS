import pandas as pd
import numpy as np
import datetime
  
if __name__=="__main__":
    K = 208
    
    # timedelta() gets successive dates with 
    # appropriate difference
    #init_year = 2015
    init_date = datetime.datetime(2015, 1, 1)
    '''for indice in range(int(K/52)):
        init_date.append(datetime.datetime(init_year+indice, 1, 1))'''
    
    #date = []
    #for indice in range(int(K/52)):
    date = [init_date + datetime.timedelta(weeks=i) for i in range(K)]


    #funcao_demanda = lambda i: 10000+5*np.log(i+6)+20*np.cos(6.2831*i/50+1.8849)+np.random.normal(0, 8,1)[0]
    demandas = []
    for indice in range(int(K/52)):
        funcao_demanda = lambda i: 10000+400*np.cos(6.2831*(i+10)/50+1.8849)+np.random.normal(0, 30,1)[0]
        demandas += [funcao_demanda(i) for i in range(52)]
    
    df_demandas = pd.DataFrame({'date':date,'demandas':demandas})
    df_demandas.to_csv('C:/Users/marcio/Documents/Prev_For_ULS/Resultados/tabelas/Demandas_treinamento/demandas')
