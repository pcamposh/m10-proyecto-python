import os
import pandas as pd

from thefuzz import fuzz, process

directorio = r"C:\PCH\Análisis de datos\material_clase_1208\proyecto"
os.chdir(directorio)

# print("Directorio de trabajo: ", os.getcwd())

df_ventas = pd.read_csv("Vendedores.csv")
df_vendedores = pd.read_csv("Ventas.csv")

#print(df_ventas.info())
#print(df_vendedores.info())

df_ventas["empresa"] = df_ventas["empresa"].str.lower().str.strip()
df_vendedores["empresa"] = df_vendedores["empresa"].str.lower().str.strip()

def encontrar_mejor_match(nombre, lista_empresas):
    mejor_match, score = process.extractOne(nombre, lista_empresas, scorer=fuzz.token_sort_ratio)

    print(score)
    return mejor_match if score > 50 else None

df_ventas["empresa_corregida"] = df_ventas["empresa"].apply(lambda x : encontrar_mejor_match(x, df_vendedores["empresa"].tolist()))

df_final = df_ventas.merge(df_vendedores, left_on="empresa_corregida", right_on="empresa", how="left")
 
df_final.rename(columns={"empresa_x": "empresa_original"}, inplace=True)
 
#print(df_final.head())
 
df_sin_match = df_final[df_final["empresa_corregida"].isna()]
 
print(df_sin_match.head())

df_final.to_csv("resultados_cruce.csv", index=False)

df_sin_match.to_csv("registros_sin_cruce.csv", index=False)


# SEGUNDA PARTE

import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime

# Ventas por Empresa

ventas_por_empresa = df_final.groupby("empresa_corregida")["monto"].sum().reset_index()

print(ventas_por_empresa)