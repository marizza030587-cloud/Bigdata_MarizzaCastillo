# ==============================================================================
# SCRIPT 3: BATERÍA DE CONSULTAS DE EXPLORACIÓN (EDA)
# ==============================================================================

library(tidyverse)

# Cargamos el dataset preprocesado y limpio
df <- read_csv("airbnb_portugal_clean.csv")
print("🔍 Dataset cargado. Iniciando batería de consultas de exploración...")

# =====================================================================
# EJERCICIO 1: Top 5 de Alojamientos Más Caros
# Muestra cómo ordenar datos y seleccionar columnas específicas.
# =====================================================================
print("\n📌 1. TOP 5 ALOJAMIENTOS MÁS CAROS:")

top_caros <- df %>% 
  arrange(desc(price)) %>% 
  select(name, region_origen, price, room_type) %>% 
  head(5)

print(as.data.frame(top_caros)) # Convertimos a data.frame básico para una impresión limpia en consola


# =====================================================================
# EJERCICIO 2: Precio Promedio y Total de Alojamientos por Región
# Enseña el uso fundamental de group_by() y summarise().
# =====================================================================
print("\n📌 2. RESUMEN DEL MERCADO POR REGIÓN (Precio Promedio y Volumen):")

resumen_region <- df %>% 
  group_by(region_origen) %>% 
  summarise(
    precio_promedio = round(mean(price, na.rm = TRUE), 2),
    total_alojamientos = n() # n() cuenta los registros en R, equivalente a count
  ) %>% 
  arrange(desc(precio_promedio))

print(resumen_region)


# =====================================================================
# EJERCICIO 3: El Efecto "Superhost"
# Filtrado analítico para comprobar métricas de comportamiento de hosts.
# =====================================================================
print("\n📌 3. COMPARATIVA: ¿SER SUPERHOST MARCA LA DIFERENCIA?")

efecto_superhost <- df %>% 
  filter(review_scores_rating > 0) %>% 
  group_by(host_is_superhost) %>% 
  summarise(
    precio_medio = round(mean(price, na.rm = TRUE), 2),
    puntuacion_media = round(mean(review_scores_rating, na.rm = TRUE), 2),
    total_propiedades = n()
  )

print(efecto_superhost)


# =====================================================================
# EJERCICIO 4: Filtrado Avanzado Multicriterio (Oportunidades de Inversión)
# Simula una petición real mediante condiciones lógicas cruzadas complejas.
# =====================================================================
print("\n📌 4. BÚSQUEDA DE OPORTUNIDADES (Filtro Cruzado Complejo):")

# En R se usa el operador lógico & de forma directa dentro de filter()
oportunidades <- df %>% 
  filter(
    region_origen == "Bogota" & 
    room_type == "Entire home/apt" & 
    price < 80 & 
    accommodates >= 4 & 
    review_scores_rating >= 4.5
  )

print(paste("🎯 Se han encontrado", nrow(oportunidades), "opciones que cumplen los requisitos del inversor."))

# Mostramos solo las primeras 5 seleccionando columnas de interés
oportunidades_vista <- oportunidades %>% 
  select(name, neighbourhood_cleansed, price, review_scores_rating) %>% 
  head(5)

print(as.data.frame(oportunidades_vista))


# =====================================================================
# EJERCICIO 5: Distribución del Tipo de Alojamiento por Región (Matriz de Contingencia)
# Muestra cómo cruzar dos variables categóricas. Ideal antes de hacer un ggplot.
# =====================================================================
print("\n📌 5. MATRIZ DE DISTRIBUCIÓN: TIPO DE ALOJAMIENTO POR REGIÓN:")

# En R, la función nativa table() genera la matriz de contingencia exacta de un crosstab
matriz_tipos <- table(df$region_origen, df$room_type)
print(matriz_tipos)

library(readr)
library(dplyr)
library(readr)

df <- read_csv(file.choose())
library(tidyverse) # O simplemente library(dplyr)
library(dplyr)
library(dplyr)

print("\n📌 6. BÚSQUEDA ASEQUIBLE DE TIPO DE ALOJAMIENTO (apartamento cerca del mar, 1 dormitorio y 1 baño):")

alojamientos_filtrados <- df %>%
  filter(
    region_origen == "Lisboa",
    room_type == "Entire home/apt",
    price > 100,
    price < 200,
    accommodates >= 2,
    review_scores_rating >= 4.5,
    bedrooms == 1,
    bathrooms_num == 1
  )

print(alojamientos_filtrados)

cat("\nNúmero de alojamientos encontrados:", nrow(alojamientos_filtrados), "\n")
ls()
df <- read.csv(file.choose(), stringsAsFactors = FALSE)
names(df)
library(dplyr)

print("\n📌 6. BÚSQUEDA ASEQUIBLE DE TIPO DE ALOJAMIENTO (apartamento cerca del mar, 1 dormitorio y 1 baño):")

alojamientos_filtrados <- df %>%
  filter(
    region_origen == "Lisboa",
    room_type == "Entire home/apt",
    price > 100,
    price < 200,
    accommodates >= 2,
    review_scores_rating >= 4.5,
    bedrooms == 1,
    bathrooms_num == 1
  )

print(alojamientos_filtrados)

cat("\nNúmero de alojamientos encontrados:",
    nrow(alojamientos_filtrados), "\n")

install.packages("ggplot2")
library(ggplot2)

ggplot(alojamientos_filtrados, aes(x = price)) +
  geom_histogram(
    binwidth = 10,
    fill = "steelblue",
    color = "white",
    boundary = 100
  ) +
  labs(
    title = "Distribución de precios de alojamientos en Lisboa",
    subtitle = "Apartamentos completos con 1 dormitorio y 1 baño",
    x = "Precio del alojamiento",
    y = "Número de alojamientos"
  ) +
  scale_x_continuous(
    breaks = seq(100, 200, by = 10)
  ) +
  theme_minimal(base_size = 12)
# =====================================================================
# EJERCICIO 5: Distribución del Tipo de Alojamiento por Región (Matriz de Contingencia)
# Muestra cómo cruzar dos variables categóricas. Ideal antes de hacer un ggplot.
# =====================================================================
print("\n📌 5. MATRIZ DE DISTRIBUCIÓN: TIPO DE ALOJAMIENTO POR REGIÓN:")

# En R, la función nativa table() genera la matriz de contingencia exacta de un crosstab
matriz_tipos <- table(df$region_origen, df$room_type)
print(matriz_tipos)
# =====================================================================
# EJERCICIO 6: PRECIO MEDIO DE ALOJAMIENTOS POR CIUDAD
# Compara el precio medio y el número de alojamientos.
# =====================================================================

cat("\n📌 EJERCICIO 6. PRECIOS MEDIOS POR CIUDAD\n")

library(dplyr)
library(ggplot2)

# Preparar los datos
datos_ej6 <- df %>%
  mutate(price = as.numeric(price)) %>%
  filter(
    region_origen %in% c("Lisboa", "Oporto"),
    !is.na(price),
    price > 0
  )

# Calcular precio medio y número de alojamientos
resumen_precios <- datos_ej6 %>%
  group_by(region_origen) %>%
  summarise(
    precio_medio = mean(price),
    numero_alojamientos = n(),
    .groups = "drop"
  ) %>%
  arrange(factor(region_origen, levels = c("Lisboa", "Oporto")))

print(resumen_precios)

# Gráfico de barras
grafica_precios_ciudad <- ggplot(
  resumen_precios,
  aes(x = region_origen, y = precio_medio, fill = region_origen)
) +
  geom_col(width = 0.6) +
  geom_text(
    aes(label = paste0(round(precio_medio, 2), " €")),
    vjust = -0.5,
    size = 4
  ) +
  scale_fill_manual(
    values = c("Lisboa" = "#287D8E", "Oporto" = "#E58A35")
  ) +
  scale_y_continuous(
    expand = expansion(mult = c(0, 0.15))
  ) +
  labs(
    title = "Precio medio de alojamientos Airbnb",
    subtitle = "Comparación entre Lisboa y Oporto",
    x = "Ciudad",
    y = "Precio medio por noche (€)"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    legend.position = "none",
    plot.title = element_text(face = "bold"),
    panel.grid.minor = element_blank()
  )

print(grafica_precios_ciudad)

cat("Alojamientos analizados:", nrow(datos_ej6), "\n")

# =====================================================================
# EJERCICIO 7: 10 ALOJAMIENTOS MÁS BARATOS DE OPORTO
# =====================================================================

cat("\n📌 EJERCICIO 7. OPORTUNIDADES ECONÓMICAS EN OPORTO\n")

library(dplyr)
library(ggplot2)

# Seleccionar los alojamientos de Oporto
oportunidades_r <- df %>%
  mutate(price = as.numeric(price)) %>%
  filter(
    region_origen == "Oporto",
    !is.na(name),
    name != "",
    !is.na(price),
    price > 0
  ) %>%
  arrange(price) %>%
  slice_head(n = 10)

# Mostrar los resultados
if (nrow(oportunidades_r) == 0) {
  
  cat("No se encontraron alojamientos válidos en Oporto.\n")
  
} else {
  
  print(
    oportunidades_r %>%
      select(name, price)
  )
  
  # Ordenar para mostrar el más barato arriba
  oportunidades_r <- oportunidades_r %>%
    arrange(desc(price)) %>%
    mutate(name = factor(name, levels = name))
  
  grafica_oportunidades <- ggplot(
    oportunidades_r,
    aes(x = price, y = name, fill = price)
  ) +
    geom_col(width = 0.7) +
    geom_text(
      aes(label = paste0(round(price, 2), " €")),
      hjust = -0.15,
      size = 3.5
    ) +
    scale_fill_gradient(
      low = "#287D8E",
      high = "#E58A35",
      name = "Precio (€)"
    ) +
    scale_x_continuous(
      expand = expansion(mult = c(0, 0.22))
    ) +
    labs(
      title = "10 alojamientos más económicos de Oporto",
      subtitle = "Ordenados por precio por noche",
      x = "Precio por noche (€)",
      y = "Alojamiento"
    ) +
    theme_minimal(base_size = 11) +
    theme(
      plot.title = element_text(face = "bold"),
      panel.grid.minor = element_blank(),
      legend.position = "bottom"
    )
  
  print(grafica_oportunidades)
}

# =====================================================================
# EJERCICIO 8: TOP 10 ALOJAMIENTOS MEJOR VALORADOS
# Lisboa y Oporto, con un mínimo de 5 reseñas.
# =====================================================================

cat("\n📌 EJERCICIO 8. RANKING DE ALOJAMIENTOS\n")

library(dplyr)
library(ggplot2)

datos_ranking <- df %>%
  mutate(
    review_scores_rating = as.numeric(review_scores_rating),
    number_of_reviews = as.numeric(number_of_reviews)
  ) %>%
  filter(
    region_origen %in% c("Lisboa", "Oporto"),
    !is.na(name),
    name != "",
    !is.na(review_scores_rating),
    number_of_reviews >= 5
  )

# Crear un ranking independiente para cada ciudad
for (ciudad in c("Lisboa", "Oporto")) {
  
  ranking_ciudad <- datos_ranking %>%
    filter(region_origen == ciudad) %>%
    arrange(desc(review_scores_rating), desc(number_of_reviews)) %>%
    slice_head(n = 10) %>%
    arrange(review_scores_rating) %>%
    mutate(
      name = factor(name, levels = name)
    )
  
  if (nrow(ranking_ciudad) == 0) {
    
    cat("No hay alojamientos suficientes para", ciudad, "\n")
    
  } else {
    
    print(
      ranking_ciudad %>%
        select(name, review_scores_rating, number_of_reviews)
    )
    
    grafica_ranking <- ggplot(
      ranking_ciudad,
      aes(
        x = review_scores_rating,
        y = name,
        fill = review_scores_rating
      )
    ) +
      geom_col(width = 0.7) +
      geom_text(
        aes(label = round(review_scores_rating, 2)),
        hjust = -0.2,
        size = 3.5
      ) +
      scale_fill_gradient(
        low = "#68747C",
        high = "#287D8E",
        name = "Valoración"
      ) +
      scale_x_continuous(
        limits = c(0, 5),
        breaks = seq(0, 5, 1),
        expand = expansion(mult = c(0, 0.08))
      ) +
      labs(
        title = paste("Top 10 alojamientos mejor valorados -", ciudad),
        subtitle = "Solo alojamientos con al menos 5 reseñas",
        x = "Valoración de los huéspedes",
        y = "Alojamiento"
      ) +
      theme_minimal(base_size = 10) +
      theme(
        plot.title = element_text(face = "bold"),
        panel.grid.minor = element_blank(),
        legend.position = "bottom"
      )
    
    print(grafica_ranking)
  }
}
# =====================================================
# EJERCICIO 9: ANALISIS DE DEMANDA 2 VS 3 DORMITORIOS
# LISBOA Y OPORTO
# =====================================================

library(dplyr)
library(ggplot2)
library(readr)

# Cargar los datos
df_demanda <- read_csv(
  "C:/Users/15/Desktop/DATOS/airbnb_portugal_clean.csv",
  show_col_types = FALSE
)

# Convertir variables a formato numerico
df_demanda <- df_demanda %>%
  mutate(
    bedrooms = as.numeric(bedrooms),
    number_of_reviews = as.numeric(number_of_reviews)
  )

# Identificar ciudades usando region_origen
ciudades <- c("Lisboa", "Oporto")

# Analizar cada ciudad
for (ciudad in ciudades) {
  
  # Filtrar ciudad y alojamientos de 2 o 3 dormitorios
  datos <- df_demanda %>%
    filter(
      region_origen == ciudad,
      bedrooms %in% c(2, 3)
    )
  
  if (nrow(datos) == 0) {
    cat("\nNo hay datos para", ciudad, "\n")
    next
  }
  
  # Calcular indicadores
  resumen <- datos %>%
    group_by(bedrooms) %>%
    summarise(
      numero_alojamientos = n_distinct(id),
      total_resenas = sum(number_of_reviews, na.rm = TRUE),
      media_resenas = mean(number_of_reviews, na.rm = TRUE),
      .groups = "drop"
    )
  
  # Incluir ambas categorias
  resumen <- tibble(bedrooms = c(2, 3)) %>%
    left_join(resumen, by = "bedrooms") %>%
    mutate(
      numero_alojamientos = coalesce(numero_alojamientos, 0L),
      total_resenas = coalesce(total_resenas, 0),
      media_resenas = coalesce(media_resenas, 0)
    )
  
  # Mostrar tabla de resultados
  cat("\n==========", toupper(ciudad), "==========\n")
  
  print(
    resumen %>%
      mutate(
        total_resenas = round(total_resenas, 2),
        media_resenas = round(media_resenas, 2)
      )
  )
  
  # Etiquetas de la grafica
  resumen <- resumen %>%
    mutate(
      tipo_dormitorios = factor(
        bedrooms,
        levels = c(2, 3),
        labels = c("2 dormitorios", "3 dormitorios")
      )
    )
  
  # Crear grafica
  grafica <- ggplot(
    resumen,
    aes(
      x = tipo_dormitorios,
      y = media_resenas,
      fill = tipo_dormitorios
    )
  ) +
    geom_col(width = 0.55) +
    geom_text(
      aes(label = sprintf("%.1f", media_resenas)),
      vjust = -0.5,
      size = 4
    ) +
    scale_fill_manual(
      values = c(
        "2 dormitorios" = "#3498DB",
        "3 dormitorios" = "#E67E22"
      )
    ) +
    scale_y_continuous(
      expand = expansion(mult = c(0, 0.15))
    ) +
    labs(
      title = paste("Demanda aproximada por tamaño -", ciudad),
      x = "Número de dormitorios",
      y = "Media de reseñas por alojamiento"
    ) +
    theme_minimal(base_size = 12) +
    theme(
      plot.title = element_text(
        size = 14,
        face = "bold",
        hjust = 0.5
      ),
      legend.position = "none",
      panel.grid.major.x = element_blank(),
      panel.grid.minor = element_blank()
    )
  
  # Mostrar grafica
  print(grafica)
  
  # Guardar grafica en la carpeta DATOS
  archivo <- paste0(
    "C:/Users/15/Desktop/DATOS/demanda_dormitorios_",
    tolower(ciudad),
    ".png"
  )
  
  ggsave(
    filename = archivo,
    plot = grafica,
    width = 9,
    height = 6,
    dpi = 300
  )
  
  cat("Grafica guardada:", archivo, "\n")
}

# ============================================================
# EJERCICIO 10: MAPA INTERACTIVO DE DEMANDA DE AIRBNB
# LISBOA Y OPORTO
# ============================================================
# Objetivo:
# Representar geograficamente los alojamientos y colorearlos
# segun su demanda aproximada, utilizando el numero de resenas.
#
# Archivo de salida:
# mapa_demanda_lisboa_oporto.html
# ============================================================

# Instalar los paquetes si es necesario (solo una vez)
# install.packages(c("dplyr", "leaflet", "htmlwidgets"))

library(dplyr)
library(leaflet)
library(htmlwidgets)

# ============================================================
# 1. CARGAR LOS DATOS
# ============================================================

df <- read.csv(
  "C:/Users/15/Desktop/DATOS/airbnb_portugal_clean.csv",
  stringsAsFactors = FALSE,
  check.names = FALSE
)

cat("\nMAPA INTERACTIVO DE DEMANDA: LISBOA Y OPORTO\n")
cat("Total de registros iniciales:", nrow(df), "\n")

# ============================================================
# 2. COMPROBAR Y NORMALIZAR LAS COLUMNAS
# ============================================================

# Normalizar nombres de columnas
names(df) <- tolower(trimws(names(df)))

# Admitir diferentes nombres para las coordenadas
if (!"latitude" %in% names(df) && "lat" %in% names(df)) {
  names(df)[names(df) == "lat"] <- "latitude"
}

if (!"longitude" %in% names(df)) {
  alternativas_lon <- c("lon", "lng")
  encontrada <- alternativas_lon[
    alternativas_lon %in% names(df)
  ]
  
  if (length(encontrada) > 0) {
    names(df)[names(df) == encontrada[1]] <- "longitude"
  }
}

# Columnas necesarias para el mapa
columnas_necesarias <- c(
  "name",
  "price",
  "number_of_reviews",
  "bedrooms",
  "latitude",
  "longitude",
  "region_origen"
)

faltantes <- setdiff(columnas_necesarias, names(df))

if (length(faltantes) > 0) {
  stop(
    paste(
      "Faltan columnas necesarias:",
      paste(faltantes, collapse = ", "),
      ". Comprueba los nombres de las columnas del CSV."
    )
  )
}

# ============================================================
# 3. IDENTIFICAR LISBOA Y OPORTO
# ============================================================

df <- df %>%
  mutate(
    region_origen = trimws(as.character(region_origen)),
    bedrooms = suppressWarnings(as.numeric(bedrooms)),
    number_of_reviews = suppressWarnings(
      as.numeric(number_of_reviews)
    ),
    latitude = suppressWarnings(as.numeric(latitude)),
    longitude = suppressWarnings(as.numeric(longitude))
  )

# Seleccionar las dos regiones
datos <- df %>%
  filter(
    tolower(region_origen) %in% c("lisboa", "oporto")
  )

cat("Registros de Lisboa y Oporto:", nrow(datos), "\n")

# ============================================================
# 4. LIMPIAR LOS DATOS GEOGRAFICOS
# ============================================================

# Eliminar alojamientos sin coordenadas validas
datos <- datos %>%
  filter(
    !is.na(latitude),
    !is.na(longitude),
    is.finite(latitude),
    is.finite(longitude),
    between(latitude, -90, 90),
    between(longitude, -180, 180)
  ) %>%
  mutate(
    number_of_reviews = ifelse(
      is.na(number_of_reviews) | number_of_reviews < 0,
      0,
      number_of_reviews
    ),
    name = ifelse(
      is.na(name) | trimws(name) == "",
      "Alojamiento sin nombre",
      as.character(name)
    ),
    price = ifelse(
      is.na(price) | trimws(as.character(price)) == "",
      "No disponible",
      as.character(price)
    ),
    bedrooms_text = ifelse(
      is.na(bedrooms),
      "No disponible",
      as.character(bedrooms)
    )
  )

cat("Alojamientos con coordenadas validas:", nrow(datos), "\n")

if (nrow(datos) == 0) {
  stop("No hay alojamientos con coordenadas validas para el mapa.")
}

# ============================================================
# 5. CLASIFICAR LA DEMANDA APROXIMADA
# ============================================================

# Clasificacion basada en el numero de resenas
datos <- datos %>%
  mutate(
    nivel_demanda = case_when(
      number_of_reviews == 0 ~ "Sin reseñas",
      number_of_reviews <= 10 ~ "Demanda baja",
      number_of_reviews <= 50 ~ "Demanda media",
      TRUE ~ "Demanda alta"
    )
  )

# Asignar colores a cada nivel
colores_demanda <- c(
  "Sin reseñas" = "#95A5A6",
  "Demanda baja" = "#3498DB",
  "Demanda media" = "#F1C40F",
  "Demanda alta" = "#E74C3C"
)

# Crear la paleta de colores
paleta <- colorFactor(
  palette = colores_demanda,
  levels = names(colores_demanda),
  ordered = TRUE
)

# ============================================================
# 6. CREAR EL MAPA INTERACTIVO
# ============================================================

mapa <- leaflet(
  data = datos,
  options = leafletOptions(preferCanvas = TRUE)
) %>%
  leaflet::addTiles(
    urlTemplate = "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
    attribution = '&copy; OpenStreetMap contributors'
  ) %>%
  addCircleMarkers(
    lng = ~longitude,
    lat = ~latitude,
    radius = 4,
    stroke = TRUE,
    weight = 0.5,
    color = "#FFFFFF",
    fillColor = ~paleta(nivel_demanda),
    fillOpacity = 0.75,
    popup = ~paste0(
      "<b>", htmltools::htmlEscape(name), "</b><br>",
      "<b>Ciudad:</b> ",
      htmltools::htmlEscape(region_origen), "<br>",
      "<b>Precio:</b> ",
      htmltools::htmlEscape(price), "<br>",
      "<b>Dormitorios:</b> ",
      bedrooms_text, "<br>",
      "<b>Reseñas:</b> ",
      number_of_reviews, "<br>",
      "<b>Nivel de demanda:</b> ",
      nivel_demanda
    ),
    clusterOptions = markerClusterOptions()
  ) %>%
  addLegend(
    position = "bottomright",
    pal = paleta,
    values = ~nivel_demanda,
    title = "Demanda aproximada",
    opacity = 1
  ) %>%
  addLayersControl(
    overlayGroups = c("Alojamientos"),
    options = layersControlOptions(collapsed = TRUE)
  ) %>%
  fitBounds(
    lng1 = min(datos$longitude),
    lat1 = min(datos$latitude),
    lng2 = max(datos$longitude),
    lat2 = max(datos$latitude)
  )

# ============================================================
# 7. GUARDAR EL MAPA EN HTML
# ============================================================

archivo_salida <- paste0(
  "C:/Users/15/Desktop/DATOS/",
  "mapa_demanda_lisboa_oporto.html"
)

saveWidget(
  widget = mapa,
  file = archivo_salida,
  selfcontained = TRUE
)

# Mostrar el mapa en RStudio
print(mapa)

cat("\nMapa interactivo guardado correctamente en:\n")
cat(archivo_salida, "\n")

# ============================================================
# EJERCICIO 11 - GRAFICO MEJORADO
# MAPA DE CALOR: TIPOS DE ALOJAMIENTO POR BARRIO
# ============================================================

library(dplyr)
library(ggplot2)

# 1. Calcular alojamientos por barrio y tipo
datos_heatmap <- datos %>%
  count(
    neighbourhood_cleansed,
    room_type,
    name = "cantidad"
  ) %>%
  group_by(neighbourhood_cleansed) %>%
  mutate(
    porcentaje = 100 * cantidad / sum(cantidad)
  ) %>%
  ungroup()

# 2. Seleccionar los 15 barrios con mas anuncios
top_barrios <- datos %>%
  count(neighbourhood_cleansed, sort = TRUE) %>%
  slice_head(n = 15) %>%
  pull(neighbourhood_cleansed)

datos_heatmap <- datos_heatmap %>%
  filter(neighbourhood_cleansed %in% top_barrios) %>%
  mutate(
    neighbourhood_cleansed = factor(
      neighbourhood_cleansed,
      levels = rev(top_barrios)
    )
  )

# 3. Crear mapa de calor
grafico_mejorado <- ggplot(
  datos_heatmap,
  aes(
    x = room_type,
    y = neighbourhood_cleansed,
    fill = porcentaje
  )
) +
  geom_tile(
    color = "white",
    linewidth = 0.8
  ) +
  geom_text(
    aes(label = paste0(round(porcentaje, 1), "%")),
    size = 3.5
  ) +
  scale_fill_gradient(
    low = "#E3F2FD",
    high = "#1565C0"
  ) +
  labs(
    title = "Tipos de alojamiento por barrio en Oporto",
    subtitle = "Porcentaje de anuncios por tipo - 15 barrios principales",
    x = "Tipo de alojamiento",
    y = "Barrio",
    fill = "Porcentaje (%)"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    plot.title = element_text(
      face = "bold",
      size = 16
    ),
    axis.text.x = element_text(
      angle = 30,
      hjust = 1
    ),
    panel.grid = element_blank()
  )

# 4. Mostrar grafico
print(grafico_mejorado)

# 5. Guardar grafico
ggsave(
  filename = file.path(
    carpeta,
    "ejercicio11_heatmap_alojamientos.png"
  ),
  plot = grafico_mejorado,
  width = 14,
  height = 9,
  dpi = 300,
  bg = "white"
)

cat("\nMapa de calor guardado correctamente.\n")
