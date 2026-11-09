# Especificacion del Dominio Film-Hub: Datasets Cinematograficos

Este documento establece la definicion formal del dominio **Film-Hub**, base del **Work Item Obligatorio Comun WI-newdataset (#178)** en la asignatura **Evolucion y Gestion de la Configuracion (EGC)**.

---

## 1. Justificacion del Dominio y Principios de Ciencia Abierta

En la investigacion relacionada con la industria cinematografica (sistemas de recomendacion, analisis de taquilla, sociologia del entretenimiento y procesamiento de lenguaje natural sobre sinopsis), la reproducibilidad exige disponer de conjuntos de datos estables, versionados y trazables.

**Film-Hub** traslada los principios de la **Ciencia Abierta (Open Science)** al ambito del cine:
1. **Acceso Abierto (Open Access)**: Publicacion libre y descarga directa de los conjuntos de datos indexados.
2. **Formato Estandar e Interoperable**: Uso exclusivo de archivos tabulares CSV conforme a la norma RFC 4180 con codificacion UTF-8.
3. **Identificacion Persistente**: Generacion de identificadores unicos (simulados a traves del servicio Fakenodo) y control de versiones por dataset.
4. **Validacion Determinista**: Protocolo automatizado de validacion previa a la publicacion que verifica la consistencia estructural y semantica de los archivos.

---

## 2. Conjunto de Datos de Referencia (Benchmark)

Film-Hub toma como referencia metodologica y fuente de casos de prueba el conjunto de datos publico de **The Movie Database (TMDB)**:
- **Origen de datos**: [TMDB Movies Dataset (Kaggle - asaniczka)](https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies).
- **Volumen del conjunto**: Superior a 930.000 producciones cinematograficas.
- **Estructura base**: Archivo CSV delimitado por comas con cabecera en primera fila.

---

## 3. Especificacion del Esquema de Datos

Para compatibilizar la flexibilidad de analisis con la verificacion automatica, Film-Hub define un esquema estructurado en **columnas obligatorias** y **columnas complementarias tipadas**:

```text
+-------------------+-------------------+--------------------------------+
| Columna           | Tipo de Dato      | Regla de Validacion / Rango    |
+-------------------+-------------------+--------------------------------+
| title             | Cadena (UTF-8)    | Obligatorio. Longitud <= 255.  |
| year              | Entero            | Obligatorio. Rango [1888, 2030]|
| genre             | Cadena            | Obligatorio. Taxonomia valida. |
| director          | Cadena            | Opcional. Nombre del director. |
| cast              | Cadena            | Opcional. Reparto principal.   |
| duration          | Entero            | Opcional. Minutos (> 0).       |
| rating            | Decimal (Float)   | Opcional. Rango [0.0, 10.0].   |
| votes             | Entero            | Opcional. No negativo (>= 0).  |
| budget            | Decimal (Float)   | Opcional. En USD (>= 0).       |
| revenue           | Decimal (Float)   | Opcional. En USD (>= 0).       |
| language          | Cadena            | Opcional. Codigo ISO 639.      |
| country           | Cadena            | Opcional. Codigo ISO 3166.     |
| overview          | Texto             | Opcional. Descripcion sinopsis.|
+-------------------+-------------------+--------------------------------+
```

### 3.1. Taxonomia Estandarizada de Generos
Para consolidar metricas agregadas, la columna `genre` normaliza o valida contra los generos cinematograficos habituales:
`Action`, `Adventure`, `Animation`, `Comedy`, `Crime`, `Documentary`, `Drama`, `Family`, `Fantasy`, `History`, `Horror`, `Music`, `Mystery`, `Romance`, `Science Fiction`, `TV Movie`, `Thriller`, `War`, `Western`.

---

## 4. Pipeline de Validacion del Servicio

El procesamiento de cualquier archivo `.csv` cargado en la plataforma sigue una secuencia jerarquica de cuatro niveles:

```text
[ Archivo CSV entrante ]
           |
           v
1. Validacion Sintactica (RFC 4180): Codificacion UTF-8, delimitadores uniformes.
           | (Si falla: HTTP 400 "CSV con formato invalido o corrupto")
           v
2. Validacion de Cabeceras: Presencia obligatoria de 'title', 'year' y 'genre'.
           | (Si falla: HTTP 400 "Ausencia de columnas requeridas")
           v
3. Validacion Semantica y Rangos: Comprobacion de tipos enteros y limites numericos.
           | (Si falla: HTTP 400 "Valores fuera de rango en datos")
           v
4. Extraccion de Metricas de Dominio: Calculo de indicadores estadisticos del dataset.
           |
           v
[ Dataset Persistido e Indexado ]
```

### 4.1. Reglas Detalladas de Validacion

1. **Integridad Estructural (RFC 4180)**:
   - Archivo de texto plano delimitado por comas.
   - Codificacion estricta UTF-8 (admitiendo BOM de forma tolerante).
   - Filas con numero homogeneo de delimitadores respecto a la cabecera.

2. **Integridad de Cabecera**:
   - Cabeceras normalizadas a minusculas e insensibles a espacios circundantes.
   - Obligatoriedad estricta de las columnas `title`, `year` y `genre`.

3. **Verificacion de Tipos y Rangos**:
   - `year`: Valor entero comprendido entre 1888 y el año en curso + 2.
   - `rating`: Valor decimal comprendido en el intervalo [0.0, 10.0].
   - `duration`: Entero estrictamente positivo y menor a 1500 minutos.

---

## 5. Metricas de Dominio Calculadas

Durante la ingesta valida de un conjunto de datos, el servicio extrae y persiste metadatos cuantitativos propios del dominio:
- `total_movies`: Recuento total de registros cinematograficos validos.
- `temporal_span`: Intervalo temporal acotado por `(min_year, max_year)`.
- `primary_genre`: Genero con mayor frecuencia de aparicion en el conjunto.
- `average_rating`: Promedio aritmetico de las puntuaciones registradas.
- `average_duration`: Duracion media en minutos de las peliculas que informan este campo.

---

## 6. Arquitectura del Modulo y Desacoplo de Flamapy

El proyecto base uvlhub mantiene una dependencia fuerte con la libreria `flamapy` orientada a modelos de caracteristicas `.uvl`. Para Film-Hub se establece un desacoplamiento modular:

1. **Creacion del Feature `filmdataset` con Rosemary**:
   ```bash
   docker compose exec web rosemary feature:create filmdataset
   ```
2. **Entidades Principales**:
   - `FilmDataset`: Extiende la clase base de dataset incorporando las metricas de dominio calculadas.
   - `FilmCSVValidator`: Servicio encargado de ejecutar la secuencia de validacion de cuatro niveles.
   - `FilmMetricsService`: Servicio de agregacion estadistica de filas procesadas.
3. **Aislamiento de Flamapy**:
   - El modulo `filmdataset` no invoca dependencias de `flamapy`.
   - Se preserva el modulo historico de feature models para mantener la retrocompatibilidad exigida sin generar colisiones de importacion.
