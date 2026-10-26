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
# EJERCICIO 6: Búsqueda Asequible de Alojamientos en Lisboa (Histograma)
# Muestra la distribución de precios de los alojamientos filtrados.
# Permite identificar los intervalos de precios con más alojamientos.
# =====================================================================
print("\n📌 6. DISTRIBUCIÓN DE PRECIOS DE ALOJAMIENTOS EN LISBOA:")

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
install.packages(c("leaflet", "htmlwidgets"))
# =====================================================================
# EJERCICIO 7: Mapa Interactivo de Alojamientos en Lisboa (HTML)
# Representa la ubicación de los alojamientos mediante coordenadas.
# Los colores indican el precio y cada marcador muestra información.
# El mapa se guarda como un archivo HTML que se abre en el navegador.
# =====================================================================
print("\n📌 7. MAPA INTERACTIVO DE ALOJAMIENTOS EN LISBOA:")

library(dplyr)
library(leaflet)
library(htmlwidgets)

# Preparar los datos del mapa
mapa_datos <- alojamientos_filtrados %>%
  mutate(
    latitude = as.numeric(latitude),
    longitude = as.numeric(longitude),
    price = as.numeric(price)
  ) %>%
  filter(
    !is.na(latitude),
    !is.na(longitude),
    !is.na(price),
    between(latitude, -90, 90),
    between(longitude, -180, 180)
  )

# Crear una escala de colores según el precio
paleta <- colorNumeric(
  palette = "YlOrRd",
  domain = mapa_datos$price
)

# Crear el mapa interactivo
mapa_lisboa <- leaflet(data = mapa_datos) %>%
  addTiles() %>%
  addCircleMarkers(
    lng = ~longitude,
    lat = ~latitude,
    radius = 5,
    color = ~paleta(price),
    fillOpacity = 0.7,
    stroke = FALSE,
    popup = ~paste0(
      "<b>Alojamiento:</b> ",
      htmltools::htmlEscape(as.character(name)),
      "<br><b>Precio:</b> ",
      price,
      "<br><b>Tipo:</b> ",
      htmltools::htmlEscape(as.character(room_type)),
      "<br><b>Valoración:</b> ",
      ifelse(
        is.na(review_scores_rating),
        "Sin valoración",
        as.character(review_scores_rating)
      ),
      "<br><b>Dormitorios:</b> ",
      bedrooms,
      "<br><b>Baños:</b> ",
      bathrooms_num
    )
  ) %>%
  addLegend(
    position = "bottomright",
    pal = paleta,
    values = ~price,
    title = "Precio",
    opacity = 1
  )

# Mostrar el mapa en RStudio
mapa_lisboa

# Guardar el mapa en la carpeta de trabajo
htmlwidgets::saveWidget(
  mapa_lisboa,
  file = "mapa_alojamientos_lisboa.html",
  selfcontained = TRUE,
  title = "Mapa de alojamientos en Lisboa"
)

# Mostrar la ubicación del archivo
cat(
  "\nMapa guardado en:\n",
  file.path(getwd(), "mapa_alojamientos_lisboa.html"),
  "\n"
)

# Abrir el mapa en el navegador
browseURL(
  file.path(getwd(), "mapa_alojamientos_lisboa.html")
)
# =====================================================================
# EJERCICIO 8: Apartamentos con Mejor Relación Calidad-Precio
# Compara precios y valoraciones en Lisboa y Oporto.
# Los apartamentos baratos y mejor valorados aparecen arriba a la izquierda.
# =====================================================================
print("\n📌 8. GRÁFICA DE CALIDAD-PRECIO EN LISBOA Y OPORTO:")

library(dplyr)
library(ggplot2)

# Filtrar los apartamentos
calidad_precio <- df %>%
  mutate(
    price = as.numeric(price),
    review_scores_rating = as.numeric(review_scores_rating),
    bedrooms = as.numeric(bedrooms),
    bathrooms_num = as.numeric(bathrooms_num),
    accommodates = as.numeric(accommodates)
  ) %>%
  filter(
    region_origen %in% c("Lisboa", "Oporto"),
    room_type == "Entire home/apt",
    price > 100,
    price < 200,
    accommodates >= 2,
    review_scores_rating >= 4.5,
    bedrooms == 1,
    bathrooms_num == 1
  )

# Crear la gráfica
grafica_calidad_precio <- ggplot(
  calidad_precio,
  aes(
    x = price,
    y = review_scores_rating,
    color = region_origen
  )
) +
  geom_point(size = 2.5, alpha = 0.7) +
  labs(
    title = "Mejor relación calidad-precio",
    subtitle = "Apartamentos completos de 1 dormitorio y 1 baño",
    x = "Precio del alojamiento",
    y = "Valoración",
    color = "Ciudad"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    plot.title = element_text(face = "bold"),
    legend.position = "bottom"
  )

# Mostrar la gráfica
print(grafica_calidad_precio)

# Mostrar el número de alojamientos analizados
cat(
  "\nApartamentos encontrados:",
  nrow(calidad_precio), "\n"
)

# =====================================================================
# EJERCICIO 8: APARTAMENTOS CON MEJOR RELACIÓN CALIDAD-PRECIO
# Comparación de Lisboa y Oporto
# =====================================================================

library(dplyr)
library(ggplot2)
library(scales)

cat("\n📌 8. ANÁLISIS DE CALIDAD-PRECIO EN LISBOA Y OPORTO\n")

# 1. Preparar y filtrar los datos
calidad_precio <- df %>%
  mutate(
    price = as.numeric(price),
    review_scores_rating = as.numeric(review_scores_rating),
    bedrooms = as.numeric(bedrooms),
    bathrooms_num = as.numeric(bathrooms_num),
    accommodates = as.numeric(accommodates)
  ) %>%
  filter(
    region_origen %in% c("Lisboa", "Oporto"),
    room_type == "Entire home/apt",
    !is.na(price),
    !is.na(review_scores_rating),
    !is.na(bedrooms),
    !is.na(bathrooms_num),
    !is.na(accommodates),
    price >= 100,
    price <= 900,
    accommodates >= 2,
    review_scores_rating >= 4.5,
    bedrooms == 1,
    bathrooms_num == 1
  )

# 2. Resumen de indicadores por ciudad
indicadores <- calidad_precio %>%
  group_by(region_origen) %>%
  summarise(
    num_apartamentos = n(),
    precio_medio = mean(price, na.rm = TRUE),
    precio_mediano = median(price, na.rm = TRUE),
    valoracion_media = mean(review_scores_rating, na.rm = TRUE),
    valoracion_mediana = median(review_scores_rating, na.rm = TRUE),
    .groups = "drop"
  )

cat("\n📊 INDICADORES POR CIUDAD:\n")
print(indicadores)

# 3. Gráfica de precio y valoración
grafica_calidad_precio <- ggplot(
  calidad_precio,
  aes(
    x = price,
    y = review_scores_rating,
    color = region_origen
  )
) +
  geom_point(
    size = 2.5,
    alpha = 0.55
  ) +
  scale_color_manual(
    values = c(
      "Lisboa" = "#287D8E",
      "Oporto" = "#E9B949"
    )
  ) +
  scale_x_continuous(
    breaks = seq(100, 900, by = 100),
    limits = c(100, 900),
    labels = label_number(big.mark = ".", decimal.mark = ",")
  ) +
  scale_y_continuous(
    breaks = seq(4.5, 5, by = 0.1),
    limits = c(4.5, 5)
  ) +
  labs(
    title = "Apartamentos con mejor relación calidad-precio",
    subtitle = "Lisboa frente a Oporto | 1 dormitorio y 1 baño",
    x = "Precio por noche",
    y = "Valoración de los huéspedes",
    color = "Ciudad",
    caption = paste(
      "Apartamentos completos | Mínimo 2 huéspedes",
      "| Valoración mínima: 4,5"
    )
  ) +
  theme_minimal(base_size = 12) +
  theme(
    plot.title = element_text(
      face = "bold",
      size = 15,
      color = "#263238"
    ),
    plot.subtitle = element_text(color = "grey40"),
    axis.title = element_text(face = "bold"),
    legend.position = "bottom",
    panel.grid.minor = element_blank()
  )

print(grafica_calidad_precio)

# 4. Comparar el precio mediano por ciudad
grafica_precios <- ggplot(
  indicadores,
  aes(
    x = region_origen,
    y = precio_mediano,
    fill = region_origen
  )
) +
  geom_col(width = 0.55, show.legend = FALSE) +
  geom_text(
    aes(label = round(precio_mediano, 2)),
    vjust = -0.5,
    fontface = "bold",
    size = 4
  ) +
  scale_fill_manual(
    values = c(
      "Lisboa" = "#287D8E",
      "Oporto" = "#E9B949"
    )
  ) +
  scale_y_continuous(
    expand = expansion(mult = c(0, 0.15))
  ) +
  labs(
    title = "Precio mediano por ciudad",
    x = NULL,
    y = "Precio por noche"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    plot.title = element_text(face = "bold"),
    panel.grid.minor = element_blank()
  )

print(grafica_precios)

# 5. Número de apartamentos encontrados
cat(
  "\n🏠 TOTAL DE APARTAMENTOS ANALIZADOS:",
  nrow(calidad_precio), "\n"
)

# =====================================================================
# EJERCICIO 9: UBICACIÓN Y TIPO DE PROPIEDAD
# Geografía y distribución de alojamientos en Lisboa y Oporto
# =====================================================================

library(dplyr)
library(ggplot2)
library(scales)

cat("\n📍 EJERCICIO 9: UBICACIÓN Y TIPO DE PROPIEDAD\n")

# 1. Preparar los datos
ubicacion <- df %>%
  mutate(
    price = as.numeric(price),
    latitude = as.numeric(latitude),
    longitude = as.numeric(longitude)
  ) %>%
  filter(
    region_origen %in% c("Lisboa", "Oporto"),
    !is.na(price),
    price > 0,
    !is.na(neighbourhood_cleansed),
    !is.na(room_type)
  )

# Limitar precios extremos para mejorar la visualización
ubicacion <- ubicacion %>%
  filter(price <= 900)

# =====================================================================
# GRÁFICA 1: PRECIO MEDIO POR BARRIO
# =====================================================================

precio_barrio <- ubicacion %>%
  group_by(region_origen, neighbourhood_cleansed) %>%
  summarise(
    precio_medio = mean(price, na.rm = TRUE),
    total_alojamientos = n(),
    .groups = "drop"
  ) %>%
  group_by(region_origen) %>%
  slice_max(
    order_by = total_alojamientos,
    n = 15,
    with_ties = FALSE
  ) %>%
  ungroup()

grafica_barrios <- ggplot(
  precio_barrio,
  aes(
    x = reorder(neighbourhood_cleansed, precio_medio),
    y = precio_medio,
    fill = region_origen
  )
) +
  geom_col(show.legend = FALSE, width = 0.7) +
  geom_text(
    aes(label = round(precio_medio, 0)),
    hjust = -0.15,
    size = 3
  ) +
  coord_flip() +
  facet_wrap(~region_origen, scales = "free_y") +
  scale_fill_manual(
    values = c("Lisboa" = "#287D8E",
               "Oporto" = "#E9B949")
  ) +
  scale_y_continuous(
    expand = expansion(mult = c(0, 0.15))
  ) +
  labs(
    title = "Precio medio por barrio",
    subtitle = "Los 15 barrios con más alojamientos de cada ciudad",
    x = "Barrio",
    y = "Precio medio por noche"
  ) +
  theme_minimal(base_size = 11) +
  theme(
    plot.title = element_text(face = "bold", size = 14),
    panel.grid.minor = element_blank(),
    strip.text = element_text(face = "bold")
  )

print(grafica_barrios)

# =====================================================================
# GRÁFICA 2: TIPO DE PROPIEDAD POR CIUDAD
# =====================================================================

tipo_propiedad <- ubicacion %>%
  count(region_origen, room_type, name = "total") %>%
  group_by(region_origen) %>%
  mutate(porcentaje = total / sum(total) * 100) %>%
  ungroup()

grafica_tipo <- ggplot(
  tipo_propiedad,
  aes(
    x = region_origen,
    y = porcentaje,
    fill = room_type
  )
) +
  geom_col(width = 0.65) +
  scale_fill_brewer(palette = "Set2") +
  scale_y_continuous(
    labels = label_percent(scale = 1),
    expand = c(0, 0)
  ) +
  labs(
    title = "Tipos de alojamiento por ciudad",
    subtitle = "Distribución porcentual",
    x = "Ciudad",
    y = "Porcentaje de alojamientos",
    fill = "Tipo de propiedad"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    plot.title = element_text(face = "bold", size = 14),
    legend.position = "bottom",
    panel.grid.minor = element_blank()
  )

print(grafica_tipo)

# =====================================================================
# GRÁFICA 3: DISTRIBUCIÓN GEOGRÁFICA
# =====================================================================

grafica_mapa <- ggplot(
  coordenadas,
  aes(
    x = longitude,
    y = latitude,
    color = region_origen
  )
) +
  geom_point(
    alpha = 0.35,
    size = 0.7
  ) +
  scale_color_manual(
    values = c(
      "Lisboa" = "#287D8E",
      "Oporto" = "#E9B949"
    )
  ) +
  facet_wrap(
    ~region_origen,
    scales = "fixed"
  ) +
  labs(
    title = "Distribución geográfica de alojamientos",
    subtitle = "Ubicación según latitud y longitud",
    x = "Longitud",
    y = "Latitud",
    color = "Ciudad"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    plot.title = element_text(
      face = "bold",
      size = 14
    ),
    legend.position = "bottom",
    panel.grid.minor = element_blank()
  )

print(grafica_mapa)

# =====================================================================
# TABLA RESUMEN
# =====================================================================

resumen_ubicacion <- ubicacion %>%
  group_by(region_origen, room_type) %>%
  summarise(
    alojamientos = n(),
    precio_medio = round(mean(price, na.rm = TRUE), 2),
    precio_mediano = round(median(price, na.rm = TRUE), 2),
    .groups = "drop"
  )

cat("\n📊 RESUMEN POR CIUDAD Y TIPO DE PROPIEDAD:\n")
print(resumen_ubicacion)

cat("\nTotal de alojamientos analizados:",
    nrow(ubicacion), "\n")

# =====================================================================
# EJERCICIO 10: MEDIA DE RESEÑAS POR PRECIO
# Comparación entre Lisboa y Oporto
# =====================================================================

library(dplyr)
library(ggplot2)

cat("\n📊 EJERCICIO 10: MEDIA DE RESEÑAS POR PRECIO\n")

# 1. Comprobar que existen las columnas necesarias
stopifnot(
  all(c("region_origen", "price", "number_of_reviews") %in% names(df))
)

# 2. Preparar y agrupar los datos
media_resenas_por_precio_lisboa_oporto <- df %>%
  mutate(
    price = as.numeric(price),
    number_of_reviews = as.numeric(number_of_reviews)
  ) %>%
  filter(
    region_origen %in% c("Lisboa", "Oporto"),
    !is.na(price),
    price > 0,
    !is.na(number_of_reviews)
  ) %>%
  mutate(
    intervalo_precio = cut(
      price,
      breaks = c(0, 50, 100, 150, 200, 300, 500, Inf),
      labels = c(
        "0-50", "51-100", "101-150",
        "151-200", "201-300", "301-500", "Más de 500"
      ),
      include.lowest = TRUE
    )
  ) %>%
  group_by(region_origen, intervalo_precio) %>%
  summarise(
    media_resenas = mean(number_of_reviews, na.rm = TRUE),
    total_alojamientos = n(),
    .groups = "drop"
  )

# 3. Mostrar la tabla de resultados
print(media_resenas_por_precio_lisboa_oporto)

# 4. Crear la gráfica comparativa
grafica_resenas_precio <- ggplot(
  media_resenas_por_precio_lisboa_oporto,
  aes(
    x = intervalo_precio,
    y = media_resenas,
    color = region_origen,
    group = region_origen
  )
) +
  geom_line(linewidth = 1, na.rm = TRUE) +
  geom_point(size = 3, na.rm = TRUE) +
  scale_color_manual(
    values = c(
      "Lisboa" = "#287D8E",
      "Oporto" = "#E9B949"
    )
  ) +
  labs(
    title = "Media de reseñas según el precio",
    subtitle = "Comparación entre Lisboa y Oporto",
    x = "Intervalo de precio por noche",
    y = "Media de reseñas por alojamiento",
    color = "Ciudad"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    plot.title = element_text(face = "bold", size = 15),
    legend.position = "bottom",
    axis.text.x = element_text(angle = 30, hjust = 1),
    panel.grid.minor = element_blank()
  )

# 5. Mostrar la gráfica
print(grafica_resenas_precio)

# 6. Número de alojamientos analizados
cat(
  "\nTotal de combinaciones ciudad-intervalo:",
  nrow(media_resenas_por_precio_lisboa_oporto),
  "\n"
)
install.packages(c(
  "flexdashboard",
  "shiny",
  "dplyr",
  "ggplot2",
  "plotly",
  "DT",
  "scales"
))
