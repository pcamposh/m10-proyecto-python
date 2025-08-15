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

# Ventas por Empresa

# ventas_por_empresa = df_final.dropna()
ventas_por_empresa = df_final.groupby("empresa_corregida")["monto"].sum().reset_index()
ventas_por_empresa.sort_values(by="monto", ascending=False, inplace=True)


# Ventas por vendedor

ventas_por_vendedor = df_final.groupby("vendedor")["monto"].sum().reset_index()
ventas_por_vendedor.sort_values(by="monto", ascending=False, inplace=True)

print(ventas_por_empresa)

# Gráficos de Venta por Empresa y Vendedor

plt.figure(figsize=(10,5))
plt.barh(ventas_por_empresa["empresa_corregida"], ventas_por_empresa["monto"], color="skyblue")
plt.xlabel("Total vendido por Empresa")
plt.ylabel("Empresa")
plt.gca().invert_yaxis()
plt.title("Ventas por Empresa")

plt.savefig("ventas_por_empresa.png", bbox_inches="tight")


plt.figure(figsize=(10,5))
plt.barh(ventas_por_vendedor["vendedor"], ventas_por_empresa["monto"], color="skyblue")
plt.xlabel("Total vendido por Vendedor")
plt.ylabel("Vendedor")
plt.gca().invert_yaxis()
plt.title("Ventas por Vendedor")

plt.savefig("ventas_por_vendedor.png", bbox_inches="tight")

plt.close()


# CREAR REPORTE PDF

from fpdf import FPDF
from datetime import datetime

# Instancia y configuración inicial del documento PDF
pdf=FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()


# Agregar título al documento PDF

pdf.set_font("Arial", style="B", size=16)
fecha_hora_actual = datetime.now().strftime("%d/%m/%Y  %H:%M:%S")
titulo = f"Reporte de Ventas - {fecha_hora_actual}"

pdf.cell(200, 10, titulo, ln=True, align="C")

# Se agrega línea en blanco de tamaño 20
pdf.ln(10)


def dibujar_tabla(titulo, dataset, columna):
    # Agregar tablas 

    pdf.set_font("Arial", size=14, style="B")

    pdf.cell(200, 10, titulo, ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", size=12)

    for index, row in dataset.iterrows():
        pdf.cell(100, 10, row[columna], border=1)
        pdf.cell(50, 10, f"$ {row["monto"]:.2f}", border=1, ln=True)

    pdf.ln(5)

# Llamar función para ventas por Empresa
dibujar_tabla("Monto vendido por Empresa", ventas_por_empresa, "empresa_corregida")


# Llamar función para ventas por Vendedor
dibujar_tabla("Monto vendido por Vendedor", ventas_por_vendedor, "vendedor")


# Imprimir PDF

pdf.output("reporte_ventas.pdf")
