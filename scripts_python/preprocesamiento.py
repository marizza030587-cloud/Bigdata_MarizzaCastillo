import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Cargamos el dataset unificado generado en el paso anterior
# (Asumiendo que ya tenemos el archivo 'airbnb_espana_master.csv')
print("🧹 Iniciando la fase avanzada de preprocesamiento de datos...")
df = pd.read_csv("airbnb_portugal_master.csv", low_memory=False)

# =====================================================================
# RETO 1: TRATAMIENTO DE VALORES NULOS (MISSING VALUES)
# =====================================================================
print("\n1️⃣ Tratando valores nulos...")

# Imputamos 'bedrooms' y 'beds' con la mediana de la región para no sesgar con la media
df['bedrooms'] = df.groupby('region_origen')['bedrooms'].transform(lambda x: x.fillna(x.median()))
df['beds'] = df.groupby('region_origen')['beds'].transform(lambda x: x.fillna(x.median()))

# Para las puntuaciones nulas, creamos una columna bandera (Flag) antes de rellenar.
# Esto es vital en BI para saber si un alojamiento es nuevo y no penalizar su promedio.
df['has_no_reviews'] = df['review_scores_rating'].isna().astype(int)
df['review_scores_rating'] = df['review_scores_rating'].fillna(0)

# El campo superhost lo rellenamos con 'f' (False) si está vacío
df['host_is_superhost'] = df['host_is_superhost'].fillna('f')

print(f"   ✅ Nulos solventados. Habitaciones vacías restantes: {df['bedrooms'].isna().sum()}")


# =====================================================================
# RETO 2: GESTIÓN DE OUTLIERS (VALORES ATÍPICOS EN PRECIOS)
# =====================================================================
print("\n2️⃣ Filtrando valores atípicos (Outliers) en precios...")

# Registramos el tamaño original para el informe analítico
filas_originales = len(df)

# 1. LIMPIEZA: Eliminamos el '$' y las comas de los miles (ej: "$1,034.00" -> "1034.00")
df['price'] = df['price'].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False)

# 2. CONVERSIÓN: Ahora que es texto limpio (solo números y puntos), lo pasamos a numérico
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# 3. FILTRADO: Aplicamos el filtro de negocio
df = df[(df['price'] >= 10) & (df['price'] <= 1000)]

filas_filtradas = filas_originales - len(df)
print(f"   ✅ Outliers eliminados: Se descartaron {filas_filtradas} filas fuera del rango [10€ - 1000€].")


# =====================================================================
# RETO 3: INGENIERÍA DE CARACTERÍSTICAS (FEATURE ENGINEERING)
# =====================================================================
print("\n3️⃣ Ejecutando Ingeniería de Características...")

# Extraer el número de baños desde la columna de texto 'bathrooms_text'
# Ejemplos en el dataset: "1.5 baths", "1 private bath", "Shared half-bath", "Half-bath"
df['bathrooms_text'] = df['bathrooms_text'].fillna('1').astype(str).str.lower()

# Usamos expresiones regulares (regex) para extraer el primer número decimal o entero
df['bathrooms_num'] = df['bathrooms_text'].str.extract(r'(\d+\.?\d*)').astype(float)

# Si el texto dice 'half-bath' (medio baño) y no se extrajo número, le asignamos 0.5
df.loc[df['bathrooms_text'].str.contains('half', na=False) & df['bathrooms_num'].isna(), 'bathrooms_num'] = 0.5

# Cualquier otro caso nulo que quede lo dejamos en 1 baño (el mínimo estándar)
df['bathrooms_num'] = df['bathrooms_num'].fillna(1.0)

# Eliminamos la columna de texto original para limpiar el archivo final
df.drop(columns=['bathrooms_text'], inplace=True)

print("   ✅ Columna numérica 'bathrooms_num' creada con éxito a partir de texto.")


# =====================================================================
# GUARDAR DATASET FINAL Y LIMPIO
# =====================================================================
archivo_final = "airbnb_portugal_clean.csv"
df.to_csv(archivo_final, index=False)

print(f"\n🎉 ¡Preprocesamiento avanzado finalizado!")
print(f"📊 Dataset listo para análisis en R y Power BI.")
print(f"💾 Guardado como: '{archivo_final}' (Total filas: {len(df)})")

# =====================================================================
print("\n📌 7. GRAFICOS DE PRECIOS DE HABITACIONES POR CIUDADES (Graficos de ciudades por coste):")
# Muestra el coste de habitaciones por ciudades en gráficos de barras.
# =====================================================================

import matplotlib.pyplot as plt

# Calculamos el precio medio y el número de alojamientos por región
resumen_precios = (
    df.groupby('region_origen')['price']
    .agg(['mean', 'count'])
    .reindex(['Atenas', 'Creta', 'Egeo', 'Salonica'])
    .dropna()
)

# Mostramos los datos utilizados en el gráfico
print("\nPrecio medio por región:")
print(resumen_precios.round(2))

# Creamos el gráfico de barras
plt.figure(figsize=(10, 6))

barras = plt.bar(
    resumen_precios.index,
    resumen_precios['mean'],
    color=['royalblue', 'seagreen', 'darkorange', 'mediumpurple']
)

plt.title('Precio medio de alojamientos Airbnb por región de Portugal')
plt.xlabel('Región')
plt.ylabel('Precio medio por noche')
plt.bar_label(barras, fmt='%.2f')
plt.grid(axis='y', linestyle='--', alpha=0.4)

plt.tight_layout()

# Guardamos el gráfico como imagen
plt.savefig('precios_medios_por_region.png', dpi=150)

# Mostramos el gráfico en pantalla
plt.show()


# =====================================================================
print("\n📌 8. GRÁFICO DE PRECIOS DE LAS OPORTUNIDADES EN LISBOA")
# =====================================================================

import pandas as pd
import matplotlib.pyplot as plt


# 1. Comprobar que existen datos
if oportunidades.empty:
    print("No hay oportunidades que cumplan los filtros establecidos.")

else:
    # 2. Crear una copia para no modificar el DataFrame original
    datos_grafico = oportunidades.copy()

    # 3. Convertir el precio a formato numérico
    datos_grafico['price'] = pd.to_numeric(
        datos_grafico['price'],
        errors='coerce'
    )

    # 4. Eliminar registros sin nombre o precio válido
    datos_grafico = datos_grafico.dropna(
        subset=['name', 'price']
    )

    # 5. Seleccionar los 10 alojamientos más baratos
    top_oportunidades = (
        datos_grafico
        .nsmallest(10, 'price')
        .sort_values('price', ascending=True)
    )

    # 6. Generar el gráfico si quedan datos válidos
    if not top_oportunidades.empty:

        fig, ax = plt.subplots(figsize=(12, 7))

        barras = ax.barh(
            top_oportunidades['name'].astype(str),
            top_oportunidades['price'],
            color='teal'
        )

        ax.set_title(
            '10 oportunidades de alquiler más baratas en Lisboa'
        )
        ax.set_xlabel('Precio por noche')
        ax.set_ylabel('Alojamiento')

        # Mostrar el precio al final de cada barra
        ax.bar_label(barras, fmt='%.2f', padding=4)

        # El alojamiento más barato aparecerá arriba
        ax.invert_yaxis()

        ax.grid(axis='x', linestyle='--', alpha=0.4)
        ax.set_axisbelow(True)

        plt.tight_layout()

        # Guardar la imagen
        plt.savefig(
            'oportunidades_baratas_Lisboa.png',
            dpi=150,
            bbox_inches='tight'
        )

        # Mostrar el gráfico
        plt.show()

    else:
        print(
            "No hay registros con nombre y precio numérico válido."
        )
# =====================================================================
print("\n📌 7. GRAFICOS DE PRECIOS DE HABITACIONES POR CIUDADES (Graficos de ciudades por coste):")
# Muestra el coste de habitaciones por ciudades en gráficos de barras.
# =====================================================================

import matplotlib.pyplot as plt

# Calculamos el precio medio y el número de alojamientos por región
resumen_precios = (
    df.groupby('region_origen')['price']
    .agg(['mean', 'count'])
    .reindex(['Lisboa', 'Oporto'])
    .dropna()
)

# Mostramos los datos utilizados en el gráfico
print("\nPrecio medio por región:")
print(resumen_precios.round(2))

# Creamos el gráfico de barras
plt.figure(figsize=(10, 6))

barras = plt.bar(
    resumen_precios.index,
    resumen_precios['mean'],
    color=['royalblue', 'seagreen', 'darkorange', 'mediumpurple']
)

plt.title('Precio medio de alojamientos Airbnb por región de Portugal')
plt.xlabel('Región')
plt.ylabel('Precio medio por noche')
plt.bar_label(barras, fmt='%.2f')
plt.grid(axis='y', linestyle='--', alpha=0.4)

plt.tight_layout()

# Guardamos el gráfico como imagen
plt.savefig('precios_medios_por_region.png', dpi=150)

# Mostramos el gráfico en pantalla
plt.show()


# =====================================================================
print("\n📌 8. GRÁFICO DE PRECIOS DE LAS OPORTUNIDADES EN OPORTO")
# =====================================================================

import pandas as pd
import matplotlib.pyplot as plt


# 1. Comprobar que existen datos
if oportunidades.empty:
    print("No hay oportunidades que cumplan los filtros establecidos.")

else:
    # 2. Crear una copia para no modificar el DataFrame original
    datos_grafico = oportunidades.copy()

    # 3. Convertir el precio a formato numérico
    datos_grafico['price'] = pd.to_numeric(
        datos_grafico['price'],
        errors='coerce'
    )

    # 4. Eliminar registros sin nombre o precio válido
    datos_grafico = datos_grafico.dropna(
        subset=['name', 'price']
    )

    # 5. Seleccionar los 10 alojamientos más baratos
    top_oportunidades = (
        datos_grafico
        .nsmallest(10, 'price')
        .sort_values('price', ascending=True)
    )

    # 6. Generar el gráfico si quedan datos válidos
    if not top_oportunidades.empty:

        fig, ax = plt.subplots(figsize=(12, 7))

        barras = ax.barh(
            top_oportunidades['name'].astype(str),
            top_oportunidades['price'],
            color='teal'
        )

        ax.set_title(
            '10 oportunidades de alquiler más baratas en Oporto'
        )
        ax.set_xlabel('Precio por noche')
        ax.set_ylabel('Alojamiento')

        # Mostrar el precio al final de cada barra
        ax.bar_label(barras, fmt='%.2f', padding=4)

        # El alojamiento más barato aparecerá arriba
        ax.invert_yaxis()

        ax.grid(axis='x', linestyle='--', alpha=0.4)
        ax.set_axisbelow(True)

        plt.tight_layout()

        # Guardar la imagen
        plt.savefig(
            'oportunidades_baratas_oporto.png',
            dpi=150,
            bbox_inches='tight'
        )

        # Mostrar el gráfico
        plt.show()

    else:
        print(
            "No hay registros con nombre y precio numérico válido."
        )
 d=pd.read_csv('airbnb_portugal_clean.csv'); print('FILAS:',len(d)); print('COLUMNAS:',d.columns.tolist())"
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize

# ==========================================
# 1. DATOS DE LOS ALOJAMIENTOS
# ==========================================

alojamientos = [
    "Sintra Acampamento Amenities 6 (Spot for your Van)",
    "Sintra Camping Farm with Amenities 3 (Your Tent)",
    "Apartamento Praia Santa Cruz - Casa Duluc",
    "Letsgocamping_pt - FORD FOCUS",
    "Retiro Sereno",
    "Apartamento, para alojamento de média duração.",
    "A Garden in Graça",
    "Autocaravana “Pachucho” pet friendly",
    "A Peaceful Nest With Yard",
    "Giotto 4"
]

precios = [
    30.00,
    30.00,
    38.37,
    48.00,
    53.00,
    56.43,
    56.44,
    57.40,
    58.00,
    59.00
]

# ==========================================
# 2. ORDENAR DE MAYOR A MENOR EN LA GRÁFICA
#    (el precio más barato aparece arriba)
# ==========================================

indices = np.argsort(precios)

alojamientos_ordenados = np.array(alojamientos)[indices]
precios_ordenados = np.array(precios)[indices]

# ==========================================
# 3. CREAR LA FIGURA CON FONDO BLANCO
# ==========================================

fig, ax = plt.subplots(figsize=(12, 7))

fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# ==========================================
# 4. DEGRADADO DE COLORES SEGÚN EL PRECIO
# ==========================================

normalizar = Normalize(
    vmin=min(precios_ordenados),
    vmax=max(precios_ordenados)
)

colormap = plt.cm.viridis
colores = colormap(normalizar(precios_ordenados))

# ==========================================
# 5. CREAR LAS BARRAS HORIZONTALES
# ==========================================

barras = ax.barh(
    alojamientos_ordenados,
    precios_ordenados,
    color=colores,
    edgecolor="none",
    height=0.8
)

# ==========================================
# 6. MOSTRAR LOS PRECIOS AL FINAL DE LAS BARRAS
# ==========================================

for barra, precio in zip(barras, precios_ordenados):
    ax.text(
        barra.get_width() + 0.5,
        barra.get_y() + barra.get_height() / 2,
        f"{precio:.2f}",
        va="center",
        ha="left",
        fontsize=10,
        color="#222222"
    )

# ==========================================
# 7. TÍTULO Y ETIQUETAS
# ==========================================

ax.set_title(
    "10 oportunidades de alquiler más baratas en Oporto",
    fontsize=16,
    fontweight="bold",
    pad=18,
    color="#222222"
)

ax.set_xlabel(
    "Precio por noche",
    fontsize=12,
    labelpad=8
)

ax.set_ylabel(
    "Alojamiento",
    fontsize=12,
    labelpad=10
)

# ==========================================
# 8. CUADRÍCULA Y ESTILO
# ==========================================

ax.set_xlim(0, max(precios_ordenados) + 4)

ax.grid(
    axis="x",
    linestyle="--",
    linewidth=0.7,
    alpha=0.3,
    color="gray"
)

ax.set_axisbelow(True)

# Eliminar bordes superior y derecho
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.tick_params(axis="both", labelsize=10)

# ==========================================
# 9. BARRA DE COLOR DEL DEGRADADO
# ==========================================

mapeo = plt.cm.ScalarMappable(
    norm=normalizar,
    cmap=colormap
)
mapeo.set_array([])

barra_color = fig.colorbar(
    mapeo,
    ax=ax,
    pad=0.02
)

barra_color.set_label(
    "Precio por noche",
    fontsize=10
)

# ==========================================
# 10. AJUSTAR Y MOSTRAR
# ==========================================

plt.tight_layout()
plt.show()
# 📌 RANKING DE HOTELES: LISBOA Y OPORTO

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# IMPORTANTE:
# Cambia df por el nombre de tu DataFrame.
# Ajusta los nombres de las columnas a los de tu archivo.

COLUMNA_CIUDAD = "ciudad"
COLUMNA_HOTEL = "hotel"
COLUMNA_VALORACION = "valoracion"

# 1. Filtrar Lisboa y Oporto
ranking = df[
    df[COLUMNA_CIUDAD].astype(str).str.strip().str.casefold()
    .isin(["lisboa", "lisbon", "oporto", "porto"])
].copy()

# 2. Convertir las valoraciones a números
ranking[COLUMNA_VALORACION] = pd.to_numeric(
    ranking[COLUMNA_VALORACION],
    errors="coerce"
)

ranking = ranking.dropna(
    subset=[COLUMNA_HOTEL, COLUMNA_VALORACION]
)

# 3. Calcular valoración media por hotel y ciudad
ranking = (
    ranking.groupby(
        [COLUMNA_CIUDAD, COLUMNA_HOTEL],
        as_index=False
    )[COLUMNA_VALORACION]
    .mean()
)

# 4. Seleccionar los 10 mejores hoteles de cada ciudad
ranking = ranking.sort_values(
    COLUMNA_VALORACION,
    ascending=False
)

ranking = ranking.groupby(
    COLUMNA_CIUDAD,
    group_keys=False
).head(10)

# 5. Ordenar para que los mejores aparezcan arriba
ranking = ranking.sort_values(
    COLUMNA_VALORACION,
    ascending=True
)

# 6. Crear una gráfica por ciudad
for ciudad in ranking[COLUMNA_CIUDAD].unique():

    datos = ranking[
        ranking[COLUMNA_CIUDAD] == ciudad
    ].copy()

    nombres = datos[COLUMNA_HOTEL].astype(str)
    valores = datos[COLUMNA_VALORACION]

    fig, ax = plt.subplots(figsize=(12, 7))

    # Fondo blanco
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    # Degradado: rojo = menor valoración,
    # verde = mayor valoración
    minimo = valores.min()
    maximo = valores.max()

    if minimo == maximo:
        colores = ["#73B77B"] * len(valores)
    else:
        normalizar = plt.Normalize(minimo, maximo)
        colores = plt.cm.RdYlGn(normalizar(valores))

    barras = ax.barh(
        nombres,
        valores,
        color=colores,
        height=0.75
    )

    # Mostrar puntuaciones al final de las barras
    margen = max((maximo - minimo) * 0.03, 0.1)

    for barra, valor in zip(barras, valores):
        ax.text(
            barra.get_width() + margen,
            barra.get_y() + barra.get_height() / 2,
            f"{valor:.2f}",
            va="center",
            fontsize=10
        )

    ax.set_title(
        f"Ranking de hoteles en {ciudad.title()}",
        fontsize=16,
        fontweight="bold",
        pad=15
    )

    ax.set_xlabel("Valoración media")
    ax.set_ylabel("Hotel")

    ax.set_xlim(0, max(10, maximo + margen * 5))
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    # Guardar un archivo por ciudad
    nombre_archivo = (
        str(ciudad).strip().lower()
        .replace(" ", "_")
    )

    plt.savefig(
        f"ranking_hoteles_{nombre_archivo}.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()
    plt.close()

print("Rankings de Lisboa y Oporto generados.")
323