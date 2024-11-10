# -*- coding: utf-8 -*-
"""Seminario_de_grado.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TUIgNnVwy36uxMBLi8C5fGeGVWZC9b4M

# Herramienta procesamiento de Datos para analisis de alertas tempranas

Importación de librerias necesarias para ejecución del codigo
"""

from google.colab import files
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

from google.colab import files
uploaded = files.upload()

filename = 'datos_estudiantes.xlsx'

df = pd.read_excel(filename)

csv_filename = '/content/datos_estudiantes.csv'
df.to_csv(csv_filename, index=False)

print(f"Archivo CSV guardado en: {csv_filename}")

df_csv = pd.read_csv(csv_filename)

print(df_csv.head())

"""###Incialmente se sube el archivo en extensión .CSV con la data necesaria para el procesamiento de datos
Se muestran las primeras 5 filas de cada columan del Data Frame

Crear y leer Data Frame para iniciar con el procesamiento de los datos
"""

df = pd.read_csv('datos_estudiantes.csv')
print(df.head())

"""Se muestran todas las columnas integradas en el Data Frame"""

print(df.info())

"""Elimina las filas con valores nulos en el DataFrame df"""

df.dropna(inplace=True)

"""Los valores de las variables de las columnas MOMENTO 1 y MOMENTO 2 los conviere a tipo numérico, y cualquier valor que no se pueda convertir se reemplaza por NaN. Esto es útil para limpiar los datos y preparar el DataFrame para análisis numéricos.


"""

df['MOMENTO 1'] = pd.to_numeric(df['MOMENTO 1'], errors='coerce')
df['MOMENTO 2'] = pd.to_numeric(df['MOMENTO 2'], errors='coerce')

"""Se imprime que tipos de datos tiene cada columan para verificar que las variables anteriores hayan cambiado de object a float"""

print("Tipos de datos de las columnas:")
print(df.dtypes)

"""Identificar situaciones que requieren atención, como calificaciones bajas en 'MOMENTO 1' o 'MOMENTO 2' inferiores a 3.0.

Identificar número de fallas que se encuentra en un rango de 3 a 5 por cada momento

El resultado es un DataFrame que solo incluye las filas que cumplen con al menos una de las condiciones especificadas.

Se crea un nuevo Data Frame llamado "Alertas Tempranas" con los registros que cumplieron las condiciones especificadas anteriormente.
"""

alertas = df[
    (df['MOMENTO 1'] < 3.0) |
    ((df['FALLAS MOMENTO1'] >= 3) & (df['FALLAS MOMENTO1'] <= 5)) |
    (df['MOMENTO 2'] < 3.0) |
    ((df['FALLAS MOMENTO2'] >= 3) & (df['FALLAS MOMENTO2'] <= 5))
]

print("DataFrame de alertas:")
print(alertas)

"""Se crea un nuevo Data Frame llamado "alertas_unicos" que contendrá solo las filas con valor único por cada estudiate con su ID, eliminando las duplicados. Esto es útil para análisis posteriores donde solo necesitas considerar una instancia de cada ID"""

alertas_unicos = alertas.drop_duplicates(subset='ID')

"""# Muestra las alertas únicas"""

print("Alertas únicas por ID:")
print(alertas_unicos)

"""Valida y numera la cantidad de estudiantes que cumplen las regla establecida para generar las alertas tempranas del primer y segundo momento de evaluación"""

cantidad_estudiantes = alertas_unicos['ID'].nunique()
print(f"\nCantidad de estudiantes únicos que cumplen con las condiciones: {cantidad_estudiantes}")

"""Comando para exportar el nuevo Data Frame en un archivo "alertas_unicas.csv" que sera utilizado en la siguiente etapa de la evaluación de la herramienta"""

# Exportar el archivo CSV sin duplicados
datos_estudiantes_csv = 'alertas_unicas.csv'
alertas_unicos.to_csv(datos_estudiantes_csv, index=False)

files.download(datos_estudiantes_csv)

"""Código Inicial para el Modelo Predictivo"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_excel('datos_estudiantes.xlsx')

print("Primeras filas del conjunto de datos:")
print(df.head())
print("\nInformación general del conjunto de datos:")
print(df.info())

categorical_columns = ['SEDE', 'PROGRAMA', 'JORNADA', 'MATERIA', 'ESTADO', 'GENERO', 'LUGAR DE RESIDENCIA']
le = LabelEncoder()
for col in categorical_columns:
    df[col] = le.fit_transform(df[col].astype(str))

import pandas as pd
import numpy as np

for col in ['MOMENTO 1', 'MOMENTO 2', 'MOMENTO 3', 'FINAL']:
    # Reemplazar guiones con NaN
    df[col] = df[col].replace('-', np.nan, regex=True)
    # Reemplazar comas por puntos y convertir a float
    df[col] = df[col].str.replace(',', '.', regex=True).astype(float)

import pandas as pd
import numpy as np

for col in ['MOMENTO 1', 'MOMENTO 2', 'MOMENTO 3', 'FINAL']:
    # Reemplazar guiones con NaN
    df[col] = df[col].replace('-', np.nan, regex=True)
    # Convertir la columna a tipo cadena antes de usar .str.replace
    df[col] = df[col].astype(str).str.replace(',', '.', regex=True).astype(float)
    #Reemplazamos la , por . y convertimos la columna a float.

X = df.drop(columns=['ESTADO'])
y = df['ESTADO']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

import pandas as pd
import numpy as np
import re

# Función para extraer el valor numérico
def extract_number(value):
    try:
        # Busca números con o sin decimales al inicio de la cadena
        number = re.search(r"^\d+(\.\d+)?", str(value)).group(0)
        return float(number)
    except (AttributeError, TypeError):
        # Si no encuentra un número, retorna NaN
        return np.nan

# Aplicar la función a las columnas relevantes de tu DataFrame
for col in ['MOMENTO 1', 'MOMENTO 2', 'MOMENTO 3', 'FINAL']:
    df[col] = df[col].apply(extract_number)

# Resto de tu código...

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

for columna in X.columns:
    if X[columna].dtype == 'object': # Busca columnas con tipo de dato 'object' (texto)
        if '43006C' in X[columna].values:
            print(f"La columna '{columna}' contiene el valor '43006C'")
            break

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Identificar la columna que contiene '43006C' (o cualquier valor con 'C')
for columna in X.columns:
    if X[columna].dtype == 'object':
        if any(X[columna].astype(str).str.contains('C')):  # Verificar si algún valor contiene 'C'
            print(f"La columna '{columna}' contiene valores con 'C'")
            columna_con_c = columna
            break
else:
    columna_con_c = None  # Si no se encuentra ninguna columna con 'C'

# Verificar si se encontró una columna con 'C' antes de continuar
if columna_con_c is not None:  # <--  Agregar esta condición
    # Eliminar la 'C' de los valores en la columna identificada
    X[columna_con_c] = X[columna_con_c].astype(str).str.replace('C', '')
    print(f"Se ha eliminado la 'C' de la columna '{columna_con_c}'")

    # Convertir la columna a numérica si es necesario
    try:
        X[columna_con_c] = pd.to_numeric(X[columna_con_c])
    except ValueError:
        print(f"La columna '{columna_con_c}' aún contiene valores no numéricos después de eliminar la 'C'. "
              f"Puede que necesites realizar una limpieza adicional.")

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Crear y entrenar el modelo
modelo_rf = RandomForestClassifier(n_estimators=100, random_state=42)
modelo_rf.fit(X_train, y_train)

predicciones = modelo_rf.predict(X_test)



from sklearn.metrics import accuracy_score
precision = accuracy_score(y_test, predicciones)
print(f"Precisión del modelo: {precision}")



import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# ... (Código anterior para limpiar los datos y entrenar el modelo) ...

# Hacer predicciones sobre los datos de prueba
predicciones = modelo_rf.predict(X_test)

# Calcular las métricas
precision = accuracy_score(y_test, predicciones)
precision_positiva = precision_score(y_test, predicciones)
sensibilidad = recall_score(y_test, predicciones)
f1 = f1_score(y_test, predicciones)

# Imprimir las métricas
print(f"Precisión: {precision}")
print(f"Precisión (positiva): {precision_positiva}")
print(f"Sensibilidad (Recall): {sensibilidad}")
print(f"Puntuación F1: {f1}")

# Crear la matriz de confusión
matriz_confusion = confusion_matrix(y_test, predicciones)

# Mostrar la matriz de confusión con Seaborn
plt.figure(figsize=(8, 6))
sns.heatmap(matriz_confusion, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Clase 0 (Predicha)", "Clase 1 (Predicha)"],
            yticklabels=["Clase 0 (Real)", "Clase 1 (Real)"])
plt.title("Matriz de Confusión")
plt.xlabel("Clase Predicha")
plt.ylabel("Clase Real")
plt.show()



print(classification_report(y_test, y_pred))

probas = modelo_rf.predict_proba(X_test)[:, 1]

umbral = 0.7
alto_riesgo = probas > umbral

df = pd.DataFrame({
        'proba': probas,
    'alto_riesgo': alto_riesgo})

print(df)

# Visualizar los nombres de las columnas del DataFrame
print("\nNombres de las columnas:")
print(df.columns)

filename = 'alertas_unicas.csv'

df = pd.read_csv('alertas_unicas.csv')
print(df.head())

df['probabilidad_desercion'] = 1

probabilidad_desercion= df.copy()

print(probabilidad_desercion.head())

# Suponiendo que 'alto_riesgo' se define por una condición en la columna 'probabilidad_desercion'
alto_riesgo = df['probabilidad_desercion'] > 0.8  # Ajusta la condición según tu lógica

# Ahora 'alto_riesgo' tendrá la misma longitud que 'df'
estudiantes_en_riesgo = df.loc[alto_riesgo, ['ID', 'probabilidad_desercion']]
print(estudiantes_en_riesgo)

estudiantes_en_riesgo = df.loc[alto_riesgo, ['ID', 'probabilidad_desercion']]
print(estudiantes_en_riesgo)