import numpy as np
import gurobipy as gp
from gurobipy import GRB
import pandas as pd
import datetime


MAX_CPU_TIME = 3600.0
EPSILON = 1e-6

def uls(datafile,predictD):

  with open(datafile, 'r') as file: 
    linhas = file.readlines()

  # remove linha vazia inicial e elimina os "\n" de cada linha
  linhas = [a.strip() for a in linhas] 

 # ler o tamanho da instancia
    
  N = len(predictD)
  #  N = 5 
      
  H = np.zeros(N)#custo no estoque
  P = np.zeros(N)#custo unitário
  F = np.zeros(N)#custo fixo
  D = np.zeros(N)#demanda

  #Custo unitario para o produto ser fabricado
  P = [float(linhas[0]) for i in range(N)]


  #Custo para se começar a produzir
  F = [float(linhas[1]) for i in range(N)]

  #Custo unitario para o produto ser estocado
  H = [float(linhas[2]) for i in range(N)]

 
  #D = np.fromstring(linhas[5], dtype=float, sep = ' ')
  #Demandas
  D = predictD
  
  #cria o modelo
  m = gp.Model("uls") 

  m.Params.LogToConsole = 0
  m.setParam(GRB.Param.TimeLimit, MAX_CPU_TIME)
  m.setParam(GRB.Param.MIPGap, EPSILON)
  m.setParam(GRB.Param.Threads, 1)

  #Adicionando Variáveis
  x = m.addVars(N, name='x') 
  s = m.addVars(N, name='s')  
  y = m.addVars(N, vtype=GRB.BINARY, name='y') 

  # funcao objetivo
  obj = 0
  for i in range(0, N):
    obj += P[i] * x[i]
    obj += H[i] * s[i]
    obj += F[i] * y[i]

  m.setObjective(obj, GRB.MINIMIZE)


  m.addConstr(x[0] - s[0] == D[0])
  for i in range(1, N):
    m.addConstr(s[i-1] + x[i] - s[i] == D[i])
    
  for i in range(0, N):
    m.addConstr(x[i] - (D[i:N].sum())*y[i] <= 0)

  m.addConstr(s[N-1] == 0)

  # export .lp
	#model.write(file_name+"_model.lp")

  m.optimize()
  tmp = 0
  if m.status == GRB.OPTIMAL:
    tmp = 1


  resultados = {
     'x': [x[i].getAttr("x") for i in x],
     's':  [s[i].getAttr("x") for i in s],
     'y': [y[i].getAttr("x") for i in y],
     'Demanda': list(predictD),
     'ObjVal': m.ObjVal,
     'ObjBound': m.ObjBound,
     'RunTime': m.Runtime,
     'NodeCount': m.NodeCount,
     'Status': tmp,
    }

  return resultados


if __name__=="__main__":
  

  #pasta previsoes
  past = 'C:/Users/marci/OneDrive/Documents/Codigos/Prev_For_ULS/Resultados/tabelas/Previsoes/'

  #instancia ULs        
  datafile = 'C:/Users/marci/OneDrive/Documents/Codigos/Prev_For_ULS/Modelo_pi/ULS_instancia.txt'


#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
  #carregando as previsoes do sarima
  
  previsoes_sar = []
  for index in range(60):
    with open(past+f'Prev_sar/Previsao_sar{index}.txt', "r") as arquivo:
      previsoes_sar.append([float(demanda) for demanda in arquivo.read().split(',')])

  #resolvendo problema de PI com as previsoes do sarima
  resultados_sar = []           
  for i in range(len(previsoes_sar)):
    resultados_sar.append(uls(datafile,np.array(previsoes_sar[i])))
  
              
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
  #carregando as previsoes do neural prophet
  '''  
  previsoes_np = []
  for index in range(60):
    with open(past+f'Prev_pro/Previsao_pro{index}.txt', "r") as arquivo:
      previsoes_np.append([float(demanda) for demanda in arquivo.read().split(',')])

  #resolvendo problema de PI com as previsoes do neural prophet   
  resultados_np = [] 
  for i in range(len(previsoes_np)):
    resultados_np.append(uls(datafile,np.array(previsoes_np[i])))
  
  '''
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
  #carregando as demandas de treinamento
  '''
  dateparse= lambda dates:datetime.datetime.strptime(dates,'%Y-%m-%d')
  demandas_aux = pd.read_csv('../Resultados/tabelas/Demandas_treinamento/demandas',parse_dates=['date'],date_parser=dateparse)
  demandas_treino = []
  
  #print(demandas_aux)
  filtro_string = [f'(date>="201{i}/01/01" and date<"201{i}/05/01")' for i in range(5,9)]
  filtro = filtro_string[0]+'or'+filtro_string[1]+'or'+filtro_string[2]+'or'+filtro_string[3]
  #print(filtro)
  demandas_aux.query(filtro,inplace=True)
  

  for i in range(5,9): 
    demandas_treino.append(demandas_aux.query(f'date>="201{i}/01/01" and date<"201{i+1}/01/01"')['demandas'])
    


  

  #resolvendo problema de PI com as demandas de treinamento  
  resultados_treino = [] 
  for i in range(len(demandas_treino)):
    resultados_treino.append(uls(datafile,np.array(demandas_treino[i])))
  
  '''
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

  #pd.DataFrame(resultados_np).to_csv("../Resultados/tabelas/Resultados_pi/resultados_pi_np.csv")
  pd.DataFrame(resultados_sar).to_csv("C:/Users/marci/OneDrive/Documents/Codigos/Prev_For_ULS/Resultados/tabelas/Resultados_pi/resultados_pi_sar.csv")
  #pd.DataFrame(resultados_treino).to_csv("../Resultados/tabelas/Resultados_pi/resultados_pi_treino.csv")
  