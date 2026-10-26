import pandas as pd

# Cargamos el dataset preprocesado y limpio
df = pd.read_csv("airbnb_portugal_master.csv", low_memory=False)
print("🔍 Dataset cargado. Iniciando batería de consultas de exploración...")

# =====================================================================
# EJERCICIO 1: Top 5 de Alojamientos Más Caros de Portugal
# Muestra cómo ordenar datos y seleccionar columnas específicas para visualización rápida.
# =====================================================================
print("\n📌 1. TOP 5 ALOJAMIENTOS MÁS CAROS EN PORTUGAL:")
columnas_vista = ['name', 'region_origen', 'price', 'room_type']
top_caros = df.sort_values(by='price', ascending=False)[columnas_vista].head(5)
print(top_caros.to_string(index=False))


# =====================================================================
# EJERCICIO 2: Precio Promedio y Total de Alojamientos por Región
# Enseña el uso fundamental de .groupby() y la agregación de múltiples métricas.
# =====================================================================
print("\n📌 2. RESUMEN DEL MERCADO POR REGIÓN (Precio Promedio y Volumen):")
# 1. Elimina espacios en blanco y caracteres no numéricos si los hubiera (ej: $, €, comas)
df['price'] = df['price'].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False).str.strip()

# 2. Convierte la columna a tipo numérico (los valores no válidos se convertirán en NaN)
df['price'] = pd.to_numeric(df['price'], errors='coerce')
resumen_region = df.groupby('region_origen').agg(
    precio_promedio=('price', 'mean'),
    total_alojamientos=('id', 'count')
).sort_values(by='precio_promedio', ascending=False)

# Formateamos el precio a dos decimales para una lectura limpia
resumen_region['precio_promedio'] = resumen_region['precio_promedio'].round(2)
print(resumen_region)


# =====================================================================
# EJERCICIO 3: El Efecto "Superhost"
# Filtrado analítico para comprobar si los Superhosts cobran más o tienen mejores notas.
# =====================================================================
print("\n📌 3. COMPARATIVA: ¿SER SUPERHOST MARCA LA DIFERENCIA?")
# Filtramos solo los que tienen reseñas válidas (puntuación > 0)
df_con_resenas = df[df['review_scores_rating'] > 0]

efecto_superhost = df_con_resenas.groupby('host_is_superhost').agg(
    precio_medio=('price', 'mean'),
    puntuacion_media=('review_scores_rating', 'mean'),
    total_propiedades=('id', 'count')
).round(2)
print(efecto_superhost)


# =====================================================================
# EJERCICIO 4: Filtrado Avanzado Multicriterio (Oportunidades de Inversión)
# Simula una petición real de un inversor: "Busco apartamentos enteros en Lisboa, 
# económicos (<80€), con buena puntuación y capacidad para mínimo 4 personas".
# =====================================================================
print("\n📌 4. BÚSQUEDA DE OPORTUNIDADES (Filtro Cruzado Complejo):")

filtros = (
    (df['region_origen'].str.upper().str.strip() == 'LISBOA') &
    (df['room_type'] == 'Entire home/apt') &
    (df['price'] < 80) &
    (df['accommodates'] >= 4) &
    (df['review_scores_rating'] >= 4.5)
)

oportunidades = df.loc[
    filtros,
    ['name', 'neighbourhood_cleansed', 'price', 'review_scores_rating']
]

print(
    f"🎯 Se han encontrado {len(oportunidades)} opciones "
    "que cumplen los requisitos del inversor."
)

print(oportunidades.head(5).to_string(index=False))

oportunidades = df[filtros][['name', 'neighbourhood_cleansed', 'price', 'review_scores_rating']]
print(f"🎯 Se han encontrado {len(oportunidades)} opciones que cumplen los requisitos del inversor.")
print(oportunidades.head(5).to_string(index=False))  # Mostramos solo las primeras 5 para no saturar la pantalla


# =====================================================================
# EJERCICIO 5: Distribución del Tipo de Alojamiento por Región (Matriz de Contingencia)
# Muestra cómo cruzar dos variables categóricas usando crosstab, ideal antes de graficar barras apiladas.
# =====================================================================
print("\n📌 5. MATRIZ DE DISTRIBUCIÓN: TIPO DE ALOJAMIENTO POR REGIÓN:")
matriz_tipos = pd.crosstab(df['region_origen'], df['room_type'])
print(matriz_tipos)

print("\n📌 6. BÚSQUEDA ASEQUIBLE DE TIPO DE ALOJAMIENTO (oportunidades de alojamiento barato):")
filtros = (
    (df['region_origen'] == 'Oporto') & 
    (df['room_type'] == 'Entire home/apt') & 
    (df['price'] < 200) & 
    (df['price'] > 100) & 
    (df['accommodates'] >= 4) & 
    (df['review_scores_rating'] >= 4.5)
)

# Guardamos los resultados del filtro
asequible = df.loc[filtros].copy()

# Mostramos el número real de resultados

print(f"🎯 Se han encontrado {len(oportunidades)} oportunidades.")
# Mostramos los primeros 10 alojamientos
columnas = [
    'name',
    'neighbourhood_cleansed',
    'price',
    'accommodates',
    'review_scores_rating'
]

print(asequible[columnas].head(10).to_string(index=False))

print("\n📌 6. BÚSQUEDA ASEQUIBLE DE TIPO DE ALOJAMIENTO (apartamento cerca del mar 1 dormitorios y 1 baños):")
filtros = (
    (df['region_origen'] == 'lisboa') & 
    (df['room_type'] == 'Entire home/apt') & 
    (df['price'] < 200) & 
    (df['price'] > 100) & 
    (df['accommodates'] >= 2) & 
    (df['review_scores_rating'] >= 4.5)
)

# =====================================================================
print("\n📌 6. GRAFICOS DE PRECIOS DE HABITACIONES POR CIUDADES (Graficos de ciudades por coste):")
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
print("\n📌 7. GRÁFICO DE PRECIOS DE LAS OPORTUNIDADES EN OPORTO")
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
# =====================================================
# RANKING DE ALOJAMIENTOS: LISBOA Y OPORTO
# =====================================================

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Cargar los datos limpios
df = pd.read_csv("airbnb_portugal_clean.csv")

# Comprobar las zonas disponibles
print("\nZonas disponibles:")
print(df["neighbourhood_cleansed"].dropna().unique())

# Convertir valoración y número de reseñas a números
df["review_scores_rating"] = pd.to_numeric(
    df["review_scores_rating"], errors="coerce"
)

df["number_of_reviews"] = pd.to_numeric(
    df["number_of_reviews"], errors="coerce"
)

# Identificar Lisboa y Oporto
zona = df["neighbourhood_cleansed"].astype(str).str.strip().str.casefold()

ciudades = {
    "Lisboa": ["lisboa", "lisbon"],
    "Oporto": ["oporto", "porto"]
}

for ciudad, nombres_zona in ciudades.items():

    datos = df[zona.isin(nombres_zona)].copy()

    # Exigir una valoración y al menos 5 reseñas
    datos = datos[
        datos["review_scores_rating"].notna()
        & (datos["number_of_reviews"] >= 5)
        & datos["name"].notna()
    ]

    # Seleccionar los 10 alojamientos mejor valorados
    datos = datos.sort_values(
        "review_scores_rating",
        ascending=False
    ).head(10)

    if datos.empty:
        print(
            f"No se encontraron alojamientos para {ciudad}. "
            "Comprueba los nombres de las zonas impresos arriba."
        )
        continue

    # Ordenar para que el mejor aparezca arriba
    datos = datos.sort_values(
        "review_scores_rating",
        ascending=True
    )

    nombres = datos["name"].astype(str)
    puntuaciones = datos["review_scores_rating"]

    fig, ax = plt.subplots(figsize=(12, 7))

    # Fondo blanco y degradado verde-amarillo-rojo
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    normalizar = plt.Normalize(0, 100)
    colores = plt.cm.RdYlGn(
        normalizar(puntuaciones)
    )

    barras = ax.barh(
        nombres,
        puntuaciones,
        color=colores,
        height=0.75
    )

    # Etiquetas numéricas
    for barra, puntuacion in zip(barras, puntuaciones):
        ax.text(
            barra.get_width() + 1,
            barra.get_y() + barra.get_height() / 2,
            f"{puntuacion:.1f}",
            va="center",
            fontsize=10
        )

    ax.set_title(
        f"Top 10 alojamientos mejor valorados - {ciudad}",
        fontsize=15,
        fontweight="bold"
    )

    ax.set_xlabel("Valoración de huéspedes")
    ax.set_ylabel("Alojamiento")
    ax.set_xlim(0, 110)
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    archivo = f"ranking_{ciudad.lower()}.png"
    plt.savefig(archivo, dpi=300, bbox_inches="tight")

    print(f"Gráfica guardada: {archivo}")

    plt.show()
    plt.close()

# =====================================================
# EJERCICIO 9: ALISIS DE DEMANDA 2 VS 3 DORMITORIOS
# LISBOA Y OPORTO
# =====================================================

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Cargar los datos limpios
df_demanda = pd.read_csv("airbnb_portugal_clean.csv")

# Convertir columnas a formato numérico
df_demanda["bedrooms"] = pd.to_numeric(
    df_demanda["bedrooms"], errors="coerce"
)

df_demanda["number_of_reviews"] = pd.to_numeric(
    df_demanda["number_of_reviews"], errors="coerce"
)

# Normalizar nombres de zonas
zonas = (
    df_demanda["neighbourhood_cleansed"]
    .astype(str)
    .str.strip()
    .str.casefold()
)

# Identificar Lisboa y Oporto
ciudades = {
    "Lisboa": ["lisboa", "lisbon"],
    "Oporto": ["oporto", "porto"]
}

for ciudad, nombres_zona in ciudades.items():

    datos = df_demanda[zonas.isin(nombres_zona)].copy()

    # Seleccionar alojamientos de 2 y 3 dormitorios
    datos = datos[datos["bedrooms"].isin([2, 3])]

    if datos.empty:
        print(
            f"No hay datos para {ciudad}. "
            "Revisa los nombres de las zonas."
        )
        continue

    # Agrupar por número de dormitorios
    resumen = datos.groupby("bedrooms").agg(
        numero_alojamientos=("id", "nunique"),
        total_resenas=("number_of_reviews", "sum"),
        media_resenas=("number_of_reviews", "mean")
    ).reindex([2, 3], fill_value=0)

    print(f"\n===== {ciudad.upper()} =====")
    print(resumen.round(2))

    # Crear gráfica de demanda aproximada
    fig, ax = plt.subplots(figsize=(9, 6))

    colores = ["#3498DB", "#E67E22"]

    barras = ax.bar(
        ["2 dormitorios", "3 dormitorios"],
        resumen["media_resenas"],
        color=colores,
        width=0.55
    )

    # Mostrar valores sobre las barras
    for barra, valor in zip(
        barras, resumen["media_resenas"]
    ):
        ax.text(
            barra.get_x() + barra.get_width() / 2,
            barra.get_height(),
            f"{valor:.1f}",
            ha="center",
            va="bottom",
            fontsize=11
        )

    ax.set_title(
        f"Demanda aproximada por tamaño - {ciudad}",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Número de dormitorios")
    ax.set_ylabel("Media de reseñas por alojamiento")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()

    archivo = f"demanda_dormitorios_{ciudad.lower()}.png"

    plt.savefig(
        archivo,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()
    plt.close()

    print(f"Gráfica guardada: {archivo}")



# ============================================================
# EJERCICIO 10: MAPA INTERACTIVO DE DEMANDA DE AIRBNB
# LISBOA Y OPORTO
# ============================================================
# Objetivo:
# Representar geográficamente los alojamientos y colorearlos
# según su demanda aproximada, utilizando el número de reseñas.
#
# Archivo de salida: mapa_demanda_lisboa_oporto.html
# ============================================================

import pandas as pd
import numpy as np
import folium

from folium.plugins import Fullscreen, MarkerCluster

# ============================================================
# 1. CARGAR LOS DATOS
# ============================================================

df = pd.read_csv(
    "airbnb_portugal_clean.csv",
    low_memory=False
)

print("\n📌 11. MAPA INTERACTIVO DE DEMANDA: LISBOA Y OPORTO")
print(f"Total de registros iniciales: {len(df)}")

# ============================================================
# 2. COMPROBAR Y NORMALIZAR LAS COLUMNAS
# ============================================================

# Admitimos diferentes nombres habituales para las coordenadas.
alternativas = {
    "latitude": ["latitude", "lat"],
    "longitude": ["longitude", "lon", "lng"],
}

for destino, opciones in alternativas.items():
    if destino not in df.columns:
        encontrada = next(
            (col for col in opciones if col in df.columns),
            None
        )

        if encontrada is not None:
            df = df.rename(columns={encontrada: destino})

columnas_necesarias = [
    "name",
    "price",
    "number_of_reviews",
    "bedrooms",
    "latitude",
    "longitude"
]

faltantes = [
    col for col in columnas_necesarias
    if col not in df.columns
]

if faltantes:
    raise ValueError(
        f"Faltan columnas necesarias: {faltantes}. "
        "Revisa los nombres de las columnas del CSV."
    )

# ============================================================
# 3. IDENTIFICAR LISBOA Y OPORTO
# ============================================================

# Preferimos una columna que identifique la ciudad o región.
candidatas_ciudad = [
    "region_origen",
    "city",
    "market",
    "neighbourhood_group_cleansed"
]

col_ciudad = next(
    (col for col in candidatas_ciudad if col in df.columns),
    None
)

if col_ciudad is None:
    raise ValueError(
    
    
        "No se encuentra una columna de ciudad o región. "
        "Añade o identifica la columna que distingue Lisboa "
        "de Oporto antes de generar el mapa."
    )

print(f"Columna utilizada para identificar la ciudad: {col_ciudad}")

ciudad_normalizada = (
    df[col_ciudad]
    .astype("string")
    .str.strip()
    .str.casefold()
    .str.normalize("NFKD")
    .str.encode("ascii", errors="ignore")
    .str.decode("utf-8")
)

# Reconocer distintas formas de escribir los nombres.
es_lisboa = ciudad_normalizada.str.contains(
    r"lisboa|lisbon",
    regex=True,
    na=False
)

es_oporto = ciudad_normalizada.str.contains(
    r"oporto|porto",
    regex=True,
    na=False
)

df["ciudad_mapa"] = np.select(
    [es_lisboa, es_oporto],
    ["Lisboa", "Oporto"],
    default=""
)

df = df[df["ciudad_mapa"].isin(["Lisboa", "Oporto"])].copy()

if df.empty:
    raise ValueError(
        f"No se encontraron registros de Lisboa u Oporto "
        f"en la columna '{col_ciudad}'. "
        "Comprueba los valores disponibles en esa columna."
    )

# ============================================================
# 4. LIMPIAR PRECIOS, RESEÑAS, DORMITORIOS Y COORDENADAS
# ============================================================

def convertir_numero(serie):
    """Convierte números y limpia símbolos monetarios habituales."""
    texto = serie.astype("string").str.strip()

    texto = texto.str.replace(
        r"[€$£\s]",
        "",
        regex=True
    )

    # Admite decimales con coma cuando no hay punto decimal.
    coma_decimal = (
        texto.str.contains(",", na=False)
        & ~texto.str.contains(r"\.", na=False)
    )

    texto.loc[coma_decimal] = (
        texto.loc[coma_decimal]
        .str.replace(",", ".", regex=False)
    )

    # Elimina separadores de miles en formatos como 1,200.50.
    texto.loc[~coma_decimal] = (
        texto.loc[~coma_decimal]
        .str.replace(",", "", regex=False)
    )

    return pd.to_numeric(texto, errors="coerce")


for columna in [
    "price",
    "number_of_reviews",
    "bedrooms",
    "latitude",
    "longitude"
]:
    df[columna] = convertir_numero(df[columna])

# Capacidad, si está disponible.
if "accommodates" in df.columns:
    df["accommodates"] = convertir_numero(df["accommodates"])

# Valoración, si está disponible.
if "review_scores_rating" in df.columns:
    df["review_scores_rating"] = convertir_numero(
        df["review_scores_rating"]
    )

# Eliminar filas sin información geográfica o de demanda.
df = df.dropna(
    subset=[
        "latitude",
        "longitude",
        "number_of_reviews",
        "price"
    ]
).copy()

# Coordenadas válidas.
df = df[
    df["latitude"].between(-90, 90)
    & df["longitude"].between(-180, 180)
    & (df["number_of_reviews"] >= 0)
    & (df["price"] >= 0)
].copy()

# Solo anuncios con 2 o 3 dormitorios para el análisis principal.
df = df[df["bedrooms"].isin([2, 3])].copy()

if df.empty:
    raise ValueError(
        "No quedan alojamientos válidos con coordenadas y "
        "2 o 3 dormitorios. Comprueba los datos y filtros."
    )

# ============================================================
# 5. CLASIFICAR LA DEMANDA POR COLORES
# ============================================================

# Indicador indirecto de demanda:
# número de reseñas acumuladas por alojamiento.
#
# Los umbrales se calculan con los datos disponibles:
# - Demanda baja: hasta el percentil 33.
# - Demanda media: entre los percentiles 33 y 66.
# - Demanda alta: por encima del percentil 66.

p33 = df["number_of_reviews"].quantile(1 / 3)
p66 = df["number_of_reviews"].quantile(2 / 3)

def clasificar_demanda(valor):
    if valor <= p33:
        return "Baja"
    elif valor <= p66:
        return "Media"
    return "Alta"

df["nivel_demanda"] = df["number_of_reviews"].apply(
    clasificar_demanda
)

colores_demanda = {
    "Baja": "#2E86DE",    # Azul
    "Media": "#F1C40F",   # Amarillo
    "Alta": "#E74C3C"     # Rojo
}

print("\nUmbrales de demanda:")
print(f"Demanda baja: hasta {p33:.0f} reseñas")
print(f"Demanda media: hasta {p66:.0f} reseñas")
print(f"Demanda alta: más de {p66:.0f} reseñas")

# ============================================================
# 6. RESUMEN ESTADÍSTICO POR CIUDAD Y DORMITORIOS
# ============================================================

resumen = (
    df.groupby(["ciudad_mapa", "bedrooms"])
    .agg(
        alojamientos=("number_of_reviews", "size"),
        reseñas_totales=("number_of_reviews", "sum"),
        media_reseñas=("number_of_reviews", "mean"),
        precio_medio=("price", "mean")
    )
    .round(2)
)

print("\nResumen de demanda aproximada:")
print(resumen.to_string())

# ============================================================
# 7. CREAR EL MAPA BASE
# ============================================================

mapa = folium.Map(
    location=[40.5, -7.8],
    zoom_start=6,
    tiles="CartoDB positron",
    control_scale=True
)

Fullscreen(
    position="topright",
    title="Pantalla completa",
    title_cancel="Salir de pantalla completa"
).add_to(mapa)

# ============================================================
# 8. CREAR CAPAS POR CIUDAD Y NÚMERO DE DORMITORIOS
# ============================================================

for ciudad in ["Lisboa", "Oporto"]:

    for dormitorios in [2, 3]:

        datos = df[
            (df["ciudad_mapa"] == ciudad)
            & (df["bedrooms"] == dormitorios)
        ]

        if datos.empty:
            continue

        capa = folium.FeatureGroup(
            name=f"{ciudad} · {dormitorios} dormitorios",
            show=True
        )

        # Agrupar marcadores para facilitar la navegación.
        grupo = MarkerCluster(
            name=f"Agrupación {ciudad} {dormitorios}D",
            disableClusteringAtZoom=14
        )

        for _, fila in datos.iterrows():

            nombre = str(fila["name"])
            precio = fila["price"]
            resenas = int(fila["number_of_reviews"])
            nivel = fila["nivel_demanda"]
            color = colores_demanda[nivel]

            valoracion = "No disponible"
            if (
                "review_scores_rating" in df.columns
                and pd.notna(fila.get("review_scores_rating"))
            ):
                valoracion = (
                    f"{fila['review_scores_rating']:.2f} / 5"
                )

            capacidad = "No disponible"
            if (
                "accommodates" in df.columns
                and pd.notna(fila.get("accommodates"))
            ):
                capacidad = str(int(fila["accommodates"]))

            popup_html = f"""
            <div style="width:250px; font-family:Arial;">
                <h4 style="margin-bottom:8px;">{nombre}</h4>
                <b>Ciudad:</b> {ciudad}<br>
                <b>Precio por noche:</b> {precio:.2f} €<br>
                <b>Dormitorios:</b> {dormitorios}<br>
                <b>Capacidad:</b> {capacidad}<br>
                <b>Valoración:</b> {valoracion}<br>
                <b>Número de reseñas:</b> {resenas}<br>
                <b>Demanda estimada:</b>
                <span style="color:{color}; font-weight:bold;">
                    {nivel}
                </span>
            </div>
            """

            marcador = folium.CircleMarker(
                location=[
                    fila["latitude"],
                    fila["longitude"]
                ],
                radius=5 + min(np.log1p(resenas), 4),
                color=color,
                weight=1,
                fill=True,
                fill_color=color,
                fill_opacity=0.75,
                tooltip=(
                    f"{ciudad} | {nombre} | "
                    f"Demanda {nivel} | {resenas} reseñas"
                ),
                popup=folium.Popup(
                    popup_html,
                    max_width=300
                )
            )

            grupo.add_child(marcador)

        capa.add_child(grupo)
        mapa.add_child(capa)

# ============================================================
# 9. LEYENDA DE DEMANDA
# ============================================================

leyenda = """
<div style="
    position: fixed;
    bottom: 35px;
    left: 35px;
    z-index: 9999;
    background-color: white;
    padding: 14px;
    border: 1px solid #cccccc;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    font-family: Arial;
    font-size: 13px;
">
    <b>Demanda aproximada</b><br><br>
    <span style="color:#2E86DE;">●</span>
    Baja: tercio inferior de reseñas<br>
    <span style="color:#F1C40F;">●</span>
    Media: tercio intermedio de reseñas<br>
    <span style="color:#E74C3C;">●</span>
    Alta: tercio superior de reseñas<br><br>
    <small>El tamaño del círculo también aumenta<br>
    con el número de reseñas.</small>
</div>
"""

mapa.get_root().html.add_child(folium.Element(leyenda))

# ============================================================
# 10. CONTROLES Y EXPORTACIÓN HTML
# ============================================================

folium.LayerControl(
    collapsed=False
).add_to(mapa)

# Ajustar el mapa a los alojamientos encontrados.
mapa.fit_bounds(
    [
        [df["latitude"].min(), df["longitude"].min()],
        [df["latitude"].max(), df["longitude"].max()]
    ],
    padding=(25, 25)
)

archivo_salida = "mapa_demanda_lisboa_oporto.html"

mapa.save(archivo_salida)

print(f"\n✅ Mapa guardado correctamente: {archivo_salida}")
print(f"Alojamientos representados: {len(df)}")
print("Abre el archivo HTML en tu navegador para explorar el mapa.")


# ============================================================
# EJERCICIO 12: PRECIOS CON MAYOR DEMANDA EN LISBOA Y OPORTO
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("\n📌 13. ANÁLISIS DE LOS PRECIOS MÁS DEMANDADOS")

# ------------------------------------------------------------
# 1. PREPARAR LOS DATOS
# ------------------------------------------------------------

datos_precios = df.copy()

datos_precios["price"] = pd.to_numeric(
    datos_precios["price"], errors="coerce"
)

datos_precios["number_of_reviews"] = pd.to_numeric(
    datos_precios["number_of_reviews"], errors="coerce"
)

datos_precios = datos_precios[
    datos_precios["ciudad_mapa"].isin(["Lisboa", "Oporto"])
    & datos_precios["price"].between(1, 1000)
    & (datos_precios["number_of_reviews"] >= 0)
].copy()

# ------------------------------------------------------------
# 2. CREAR RANGOS DE PRECIOS
# ------------------------------------------------------------

limites = [0, 50, 75, 100, 150, 200, 300, 500, 1000]

etiquetas = [
    "1-50 €",
    "51-75 €",
    "76-100 €",
    "101-150 €",
    "151-200 €",
    "201-300 €",
    "301-500 €",
    "501-1000 €"
]

datos_precios["rango_precio"] = pd.cut(
    datos_precios["price"],
    bins=limites,
    labels=etiquetas,
    include_lowest=True
)

# ------------------------------------------------------------
# 3. CALCULAR INDICADORES DE DEMANDA
# ------------------------------------------------------------

resumen_precios = (
    datos_precios
    .groupby(
        ["ciudad_mapa", "rango_precio"],
        observed=False
    )
    .agg(
        total_alojamientos=("price", "size"),
        precio_medio=("price", "mean"),
        total_resenas=("number_of_reviews", "sum"),
        media_resenas=("number_of_reviews", "mean")
    )
    .reset_index()
)

resumen_precios[
    ["precio_medio", "media_resenas"]
] = resumen_precios[
    ["precio_medio", "media_resenas"]
].round(2)

print("\n===== DEMANDA POR RANGO DE PRECIOS =====")
print(resumen_precios.to_string(index=False))

# ------------------------------------------------------------
# 4. IDENTIFICAR LOS RANGOS MÁS DESTACADOS
# ------------------------------------------------------------

for ciudad in ["Lisboa", "Oporto"]:

    datos_ciudad = resumen_precios[
        (resumen_precios["ciudad_mapa"] == ciudad)
        & (resumen_precios["total_alojamientos"] > 0)
    ]

    if datos_ciudad.empty:
        print(f"\nNo hay datos disponibles para {ciudad}.")
        continue

    # Rango con más reseñas acumuladas
    mas_resenas = datos_ciudad.loc[
        datos_ciudad["total_resenas"].idxmax()
    ]

    # Rango con mayor media de reseñas por alojamiento
    mayor_media = datos_ciudad.loc[
        datos_ciudad["media_resenas"].idxmax()
    ]

    # Rango con más anuncios disponibles en el dataset
    mas_anuncios = datos_ciudad.loc[
        datos_ciudad["total_alojamientos"].idxmax()
    ]

    print(f"\n===== {ciudad.upper()} =====")

    print(
        "Rango con más reseñas acumuladas: "
        f"{mas_resenas['rango_precio']} "
        f"({int(mas_resenas['total_resenas'])} reseñas)"
    )

    print(
        "Rango con mayor media de reseñas por anuncio: "
        f"{mayor_media['rango_precio']} "
        f"({mayor_media['media_resenas']:.2f} reseñas)"
    )

    print(
        "Rango con más alojamientos: "
        f"{mas_anuncios['rango_precio']} "
        f"({int(mas_anuncios['total_alojamientos'])} anuncios)"
    )

# ------------------------------------------------------------
# 5. GRÁFICO: NÚMERO DE RESEÑAS POR RANGO DE PRECIOS
# ------------------------------------------------------------

tabla_resenas = resumen_precios.pivot(
    index="rango_precio",
    columns="ciudad_mapa",
    values="total_resenas"
).reindex(etiquetas).fillna(0)

ax = tabla_resenas.plot(
    kind="bar",
    figsize=(12, 7),
    color={
        "Lisboa": "#3498DB",
        "Oporto": "#E67E22"
    },
    width=0.8
)

ax.set_title(
    "Demanda aproximada por rango de precios: Lisboa y Oporto",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Precio por noche")
ax.set_ylabel("Número total de reseñas")
ax.set_xticklabels(etiquetas, rotation=35, ha="right")
ax.legend(title="Ciudad")
ax.grid(axis="y", linestyle="--", alpha=0.3)
ax.set_axisbelow(True)

plt.tight_layout()

plt.savefig(
    "demanda_por_precios_lisboa_oporto.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

# ------------------------------------------------------------
# 6. GRÁFICO: MEDIA DE RESEÑAS POR ALOJAMIENTO
# ------------------------------------------------------------

tabla_media = resumen_precios.pivot(
    index="rango_precio",
    columns="ciudad_mapa",
    values="media_resenas"
).reindex(etiquetas).fillna(0)

ax = tabla_media.plot(
    kind="bar",
    figsize=(12, 7),
    color={
        "Lisboa": "#3498DB",
        "Oporto": "#E67E22"
    },
    width=0.8
)

ax.set_title(
    "Media de reseñas por alojamiento según precio",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Precio por noche")
ax.set_ylabel("Media de reseñas por alojamiento")
ax.set_xticklabels(etiquetas, rotation=35, ha="right")
ax.legend(title="Ciudad")
ax.grid(axis="y", linestyle="--", alpha=0.3)
ax.set_axisbelow(True)

plt.tight_layout()

plt.savefig(
    "media_resenas_por_precio_lisboa_oporto.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()

print("\n✅ Gráficos guardados:")
print("- demanda_por_precios_lisboa_oporto.png")
print("- media_resenas_por_precio_lisboa_oporto.png")

import pandas as pd

df = pd.read_csv("airbnb_portugal_clean.csv", low_memory=False)

print(df.columns.tolist())


import pandas as pd

df = pd.read_csv("airbnb_portugal_clean.csv", low_memory=False)

print(df.columns.tolist())

# ============================================================
# EJERCICIO 13: TIPO DE ALOJAMIENTO POR BARRIO MÁS DEMANDADO
# EN OPORTO, REPRESENTADO MEDIANTE LATITUDES Y LONGITUDES
# ============================================================

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------------------------------------
# 1. CONFIGURACIÓN Y CARGA DEL DATASET
# ------------------------------------------------------------

CARPETA = Path(r"C:\Users\15\Desktop\DATOS")

archivos_csv = list(CARPETA.glob("*.csv"))

if not archivos_csv:
    raise FileNotFoundError(
        f"No se encontraron archivos CSV en {CARPETA}. "
        "Comprueba dónde está guardado el dataset."
    )

print("\nArchivos CSV encontrados:")
for i, archivo in enumerate(archivos_csv, start=1):
    print(f"{i}. {archivo.name}")

# Si solo existe un CSV, se selecciona automáticamente.
if len(archivos_csv) == 1:
    ARCHIVO = archivos_csv[0]
else:
    # Si hay varios, intenta seleccionar el dataset de Airbnb.
    candidatos = [
        archivo for archivo in archivos_csv
        if "listing" in archivo.name.lower()
    ]

    if len(candidatos) == 1:
        ARCHIVO = candidatos[0]
    else:
        raise FileNotFoundError(
            "Hay varios archivos CSV y no se puede identificar "
            "el dataset correcto. Asigna su nombre a ARCHIVO."
        )

df = pd.read_csv(ARCHIVO, low_memory=False)

print("\n" + "=" * 65)
print("EJERCICIO 13: ALOJAMIENTOS MÁS DEMANDADOS POR BARRIO")
print("=" * 65)
print(f"Dataset: {ARCHIVO.name}")
print(f"Registros iniciales: {len(df)}")

# ------------------------------------------------------------
# 2. COMPROBAR LAS COLUMNAS NECESARIAS
# ------------------------------------------------------------

columnas_necesarias = [
    "neighbourhood_cleansed",
    "room_type",
    "latitude",
    "longitude"
]

faltantes = [
    columna for columna in columnas_necesarias
    if columna not in df.columns
]

if faltantes:
    raise ValueError(
        f"Faltan estas columnas en el dataset: {faltantes}\n"
        f"Columnas disponibles: {df.columns.tolist()}"
    )

# ------------------------------------------------------------
# 3. LIMPIEZA DE LOS DATOS
# ------------------------------------------------------------

datos = df[columnas_necesarias].copy()

datos["latitude"] = pd.to_numeric(
    datos["latitude"], errors="coerce"
)
datos["longitude"] = pd.to_numeric(
    datos["longitude"], errors="coerce"
)

datos = datos.dropna(
    subset=[
        "neighbourhood_cleansed",
        "room_type",
        "latitude",
        "longitude"
    ]
)

datos["neighbourhood_cleansed"] = (
    datos["neighbourhood_cleansed"].astype(str).str.strip()
)
datos["room_type"] = datos["room_type"].astype(str).str.strip()

# Coordenadas aproximadas del área de Oporto.
# Sirven para descartar coordenadas claramente erróneas.
datos = datos[
    datos["latitude"].between(41.0, 42.0)
    & datos["longitude"].between(-9.0, -7.0)
].copy()

if datos.empty:
    raise ValueError(
        "No quedan registros válidos tras la limpieza. "
        "Comprueba las coordenadas y el dataset."
    )

print(f"Registros válidos para el análisis: {len(datos)}")
print(
    "Barrios identificados:",
    datos["neighbourhood_cleansed"].nunique()
)

# ------------------------------------------------------------
# 4. TIPO DE ALOJAMIENTO MÁS FRECUENTE POR BARRIO
# ------------------------------------------------------------

tabla = pd.crosstab(
    datos["neighbourhood_cleansed"],
    datos["room_type"]
)

# Total de anuncios por barrio.
tabla["Total alojamientos"] = tabla.sum(axis=1)

# Ordenar los barrios según el número total de anuncios.
tabla = tabla.sort_values(
    "Total alojamientos", ascending=False
)

# Tipo de alojamiento con más anuncios en cada barrio.
tipos = tabla.drop(
    columns=["Total alojamientos"]
).idxmax(axis=1)

tabla["Tipo predominante"] = tipos

print("\n--- RESUMEN POR BARRIO ---")
print(tabla.to_string())

# Guardar tabla de resultados.
salida_tabla = CARPETA / "ejercicio13_tipo_alojamiento_por_barrio.csv"
tabla.to_csv(salida_tabla, encoding="utf-8-sig")

print(f"\nTabla guardada en: {salida_tabla}")

# ------------------------------------------------------------
# 5. GRÁFICO: NÚMERO DE ALOJAMIENTOS POR BARRIO
# ------------------------------------------------------------

sns.set_theme(style="whitegrid")

totales = tabla["Total alojamientos"].sort_values(
    ascending=True
)

alto = max(6, len(totales) * 0.38)

plt.figure(figsize=(12, alto))
totales.plot(kind="barh", color="steelblue")

plt.title(
    "Número de anuncios de alojamiento por barrio - Oporto",
    fontsize=14
)
plt.xlabel("Número de anuncios")
plt.ylabel("Barrio")
plt.tight_layout()

plt.savefig(
    CARPETA / "ejercicio13_total_alojamientos_por_barrio.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

# ------------------------------------------------------------
# 6. GRÁFICO: TIPO DE ALOJAMIENTO POR BARRIO
# ------------------------------------------------------------

tabla_tipos = pd.crosstab(
    datos["neighbourhood_cleansed"],
    datos["room_type"]
)

tabla_tipos = tabla_tipos.loc[
    tabla["Total alojamientos"].index
]

ax = tabla_tipos.plot(
    kind="bar",
    stacked=True,
    figsize=(14, 7),
    colormap="Set2"
)

ax.set_title(
    "Tipos de alojamiento por barrio - Oporto",
    fontsize=14
)
ax.set_xlabel("Barrio")
ax.set_ylabel("Número de anuncios")
ax.legend(
    title="Tipo de alojamiento",
    bbox_to_anchor=(1.02, 1),
    loc="upper left"
)

plt.xticks(rotation=45, ha="right")
plt.tight_layout()

plt.savefig(
    CARPETA / "ejercicio13_tipos_por_barrio.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

# ------------------------------------------------------------
# 7. MAPA GEOGRÁFICO MEDIANTE LATITUD Y LONGITUD
# ------------------------------------------------------------

# Cada punto representa un anuncio del dataset.
# Los colores indican el tipo de alojamiento.
# Las coordenadas proceden de latitude y longitude.

plt.figure(figsize=(12, 9))

sns.scatterplot(
    data=datos,
    x="longitude",
    y="latitude",
    hue="room_type",
    alpha=0.55,
    s=22,
    palette="Set1"
)

plt.title(
    "Distribución geográfica de los alojamientos en Oporto",
    fontsize=14
)
plt.xlabel("Longitud")
plt.ylabel("Latitud")
plt.legend(
    title="Tipo de alojamiento",
    bbox_to_anchor=(1.02, 1),
    loc="upper left"
)
plt.tight_layout()

plt.savefig(
    CARPETA / "ejercicio13_mapa_latitud_longitud.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

# ------------------------------------------------------------
# 8. MAPA DE CONCENTRACIÓN POR BARRIO
# ------------------------------------------------------------

# Calculamos el centro geográfico aproximado de los anuncios
# de cada barrio usando la media de sus coordenadas.

coordenadas = (
    datos.groupby("neighbourhood_cleansed")
    .agg(
        latitud_media=("latitude", "mean"),
        longitud_media=("longitude", "mean"),
        total_anuncios=("room_type", "size")
    )
    .sort_values("total_anuncios", ascending=False)
)

# Un punto por barrio. Su tamaño representa el número de anuncios.
plt.figure(figsize=(12, 9))

puntos = plt.scatter(
    coordenadas["longitud_media"],
    coordenadas["latitud_media"],
    s=coordenadas["total_anuncios"] * 2,
    c=coordenadas["total_anuncios"],
    cmap="viridis",
    alpha=0.75,
    edgecolors="black"
)

for barrio, fila in coordenadas.iterrows():
    plt.annotate(
        str(barrio),
        (
            fila["longitud_media"],
            fila["latitud_media"]
        ),
        fontsize=7,
        alpha=0.85
    )

plt.colorbar(
    puntos,
    label="Número de anuncios por barrio"
)

plt.title(
    "Concentración de alojamientos por barrio en Oporto",
    fontsize=14
)
plt.xlabel("Longitud")
plt.ylabel("Latitud")
plt.tight_layout()

plt.savefig(
    CARPETA / "ejercicio13_concentracion_por_barrio.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

# ------------------------------------------------------------
# 9. RESULTADOS FINALES
# ------------------------------------------------------------

print("\n" + "=" * 65)
print("RESULTADOS FINALES DEL EJERCICIO 13")
print("=" * 65)

print("\nTop 10 barrios con más anuncios:")
print(
    tabla[["Total alojamientos", "Tipo predominante"]]
    .head(10)
    .to_string()
)

print("\nCentro geográfico aproximado y anuncios por barrio:")
print(coordenadas.to_string())

print("\nArchivos generados:")
print("- ejercicio13_tipo_alojamiento_por_barrio.csv")
print("- ejercicio13_total_alojamientos_por_barrio.png")
print("- ejercicio13_tipos_por_barrio.png")
print("- ejercicio13_mapa_latitud_longitud.png")
print("- ejercicio13_concentracion_por_barrio.png")

print("\nEjercicio 13 finalizado correctamente.")



