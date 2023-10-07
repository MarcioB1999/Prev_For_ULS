import pandas as pd
import numpy as np


def describe_var(dataframe,var):

    lista = []
    for i in dataframe[var].values:
        lista.append(list(i))

    lista = np.array(lista)

    lista = pd.DataFrame(data=lista,columns=[f'{var}{i}' for i in range(17)])

    return lista


def arrumaDataFrame(resultados):
    resultados_dataframe = {}
    for column in range(len(resultados.columns[:-5])):
        coluna_aux = []
        for element in range(len(resultados)):
            coluna_aux.append(np.array([float(elemento) for elemento in resultados.iloc[element,column][1:-1].split(',')]))
        
        resultados_dataframe[resultados.columns[column]] = coluna_aux


    for column in resultados.columns[4:]:
        resultados_dataframe[column] = resultados[column]


    return pd.DataFrame(resultados_dataframe)


def dataFrame_to_boxPlot(dataFrame,var):
    data = {}
    column_value = []
    column_ = []
 
    for column in range(len(dataFrame.columns)):
        column_value += list(dataFrame.iloc[:,column])
        column_ += [dataFrame.columns[column] for i in range(len(dataFrame))]

    data[var]=column_value
    data[dataFrame.columns[0][0]]=column_
    return pd.DataFrame(data)