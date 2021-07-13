import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from countryinfo import CountryInfo


df=pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")

def formatea_csv(param):
    df=param
    df=df.drop(['Province/State'], axis=1)
    df=df.drop(['Lat'], axis=1)
    df=df.drop(['Long'], axis=1)
    df=df.T
    row_1=df.iloc[0]
    lista=list(row_1)
    df.columns = lista
    df.index = list(range(0,df.shape[0]))
    df=df.drop([0],axis=0) 
    columns_names = list(df.columns.values)
    for i in columns_names:
        if len(df[i].shape)>1:
            dimension=df[i].shape[1]
            print(dimension)
            col=df[i]
            listar=list(range(0,dimension))
            col.columns = listar
            col[i]= col.iloc[:,:].sum(axis=1)
            df=df.drop([i]*dimension, axis=1)
            df.insert( 4,i, col[i], allow_duplicates=False)
    return df

def graficos_por_millon(df,por_millon=False,*paises):
    tupla=paises
    df=df
    colors=["Red","Blue","Green","Gray","Yellow"]
    lista=list(tupla)
    if por_millon==False:
      for n,i in enumerate(tupla):
        new_col=np.where(df[i].diff().drop([1],axis=0) < 0, 0,df[i].diff().drop([1],axis=0))
        plt.plot(new_col,label=lista[n],color=colors[n])
        plt.legend()
        plt.xlabel("dias")
        plt.ylabel("casos diarios de covid-19 ")
        plt.title("Casos diarios de covid-19 ")
        
    else:
      for n,i in enumerate(tupla):
          country = CountryInfo(lista[n])
          numero=country.info()["population"]/1000000
          new_col=np.where(df[i].diff().drop([1],axis=0) < 0, 0,df[i].diff().drop([1],axis=0))
          #plt.plot(df[i].diff().drop([1],axis=0).abs()/numero,'k', linewidth=1.7,label=lista[n],color=colors[n])
          plt.plot(new_col/numero,'k', linewidth=1.7,label=lista[n],color=colors[n])
          plt.legend()
          plt.xlabel("dias")
          plt.ylabel("casos diarios de covid-19 por millon")
          plt.title("Casos diarios de covid-19 por millon de habitantes")
        
new_df=formatea_csv(df) 
graficos_por_millon(new_df,True,"China","India")           
            
    

    