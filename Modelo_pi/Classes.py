import numpy as np
import gurobipy as gp
from gurobipy import GRB
import pandas as pd


def uls(datafile,predictD):

  with open(datafile, 'r') as file: 
    linhas = file.readlines()

  # remove linha vazia inicial e elimina os "\n" de cada linha
  linhas = [a.strip() for a in linhas] 


 # ler o tamanho da instancia
    
  N = int(linhas[0])
  #  N = 5 
      
  H = np.zeros(N)#custo no estoque
  P = np.zeros(N)#custo unitário
  F = np.zeros(N)#custo fixo
  D = np.zeros(N)#demanda
    
  P = [float(linhas[1]) for i in range(N)]



  F = [float(linhas[2]) for i in range(N)]





  H = [float(linhas[3]) for i in range(N)]
 

  #D = np.fromstring(linhas[5], dtype=float, sep = ' ')
  D = predictD
    #print(D)
    

    

  #cria o modelo
  m = gp.Model("ulsr") 
  m.Params.LogToConsole = 0

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

  m.optimize()


  resultados = {'x': [x[i].getAttr("x") for i in x],
              's':  [s[i].getAttr("x") for i in s],
              'y': [y[i].getAttr("x") for i in y],
              'ObjVal': m.ObjVal
             }

  return resultados


past = 'C:/Users/marcio/Documents/Prev_For_ULS/Resultados/tabelas/Previsoes/'
            
datafile = "ULS_instancia.txt"

previsoes_sar = []
for index in range(3):
    with open(past+f'Prev_sar/Previsao_sar{index}.txt', "r") as arquivo:
	    previsoes_sar.append([float(demanda) for demanda in arquivo.read().split(',')])

resultados_sar = []           
for i in range(len(previsoes_sar)):
  resultados_sar.append(uls(datafile,previsoes_sar))
    
            


previsoes_np = []
for index in range(3):
    with open(past+f'Prev_pro/Previsao_pro{index}.txt', "r") as arquivo:
	    previsoes_np.append([float(demanda) for demanda in arquivo.read().split(',')])
            
resultados_np = [] 
for i in range(len(previsoes_sar)):
  resultados_np.append(uls(datafile,previsoes_np))



pd.DataFrame(resultados_np).to_csv("C:/Users/marcio/Documents/Prev_For_ULS/Resultados/tabelas/Resultados_pi/resultados_pi_np.csv")
pd.DataFrame(resultados_sar).to_csv("C:/Users/marcio/Documents/Prev_For_ULS/Resultados/tabelas/Resultados_pi/resultados_pi_sar.csv")
