# Registro de Decisión Arquitectónica (ADR)

## ADR-001: Adoptar herencia polimórfica Joined Table sobre DataSet para Film-Hub

- **Estado**: Aceptado (validación unánime 4/4)
- **Fecha**: 21/11/2026
- **Autor(es)**: Juan Felipe Pardo Carrillo
- **Revisor(es)**: José Vicente Sánchez Montilla, Luis Lucena Prieto, Adrián Muñoz Aradilla
- **Work Item(s) Asociado(s)**: #178 (`WI-newdataset`), con impacto en #177 (`WI-fakenodo`) y #213 (`Embeddable badge`)

---

## 1. Contexto y Descripción del Problema
En el repositorio base UVLHub, el modelo `DataSet` estaba estrechamente acoplado al dominio de líneas de productos de software: `FeatureModel`, `FMMetaData` (`uvl_filename`, `uvl_version`), `DSMetrics` (`number_of_features`), validación con `flamapy` y subida de archivos `.uvl`.

El Work Item obligatorio `#178` (`WI-newdataset`) exige evolucionar la plataforma hacia **Film-Hub** (datasets tabulares de películas en formato `.csv`), permitiendo que cada tipo de datos defina su propio modelo, validación y lógica de negocio sin duplicar la plataforma, sin llenar un único modelo de condicionales y manteniendo funcionando el tipo UVL original sin regresiones.

---

## 2. Factores de Decisión y Requisitos de Calidad
- **Retrocompatibilidad estricta**: Las tablas existentes (`data_set`, `ds_meta_data`, `feature_model`, `ds_download_record`, `ds_view_record`) y los 267 tests rápidos heredados deben seguir funcionando sin regresiones.
- **Separación limpia de dominios**: Evitar columnas de cine como valores `NULL` en la tabla `data_set` y aislar el validador CSV en el feature modular `app/features/filmdataset/`.
- **Bajo acoplamiento entre compañeros**: Permitir que los bloques `2.B` (UI), `2.C` (Explorador/Seeders) y el `#177` (Fakenodo) trabajen en paralelo sobre un contrato estable.
- **Migración segura en MariaDB**: La nueva migración de Alembic sobre `001.py` debe soportar filas UVL preexistentes mediante un valor por defecto en servidor.

---

## 3. Alternativas Consideradas

### Alternativa 1: Herencia polimórfica Joined Table manteniendo `DataSet` como base (`dataset_type="uvl"`) + `FilmDataset` en tabla `film_dataset`
- **Descripción**: Añadir a `DataSet` una columna discriminadora `dataset_type` (`default="uvl"`, `server_default="uvl"`) como clase base polimórfica y definir `FilmDataset(DataSet)` en una tabla hija propia `film_dataset` dentro de `app/features/filmdataset/models.py`.
- **Ventajas**:
  - (+) Preserva intactos el nombre de clase `DataSet`, todas las claves foráneas existentes (`hubfile`, `featuremodel`, `zenodo`, `explore`) y los 267 tests heredados.
  - (+) Separa completamente los campos específicos de cine en `film_dataset` sin ensuciar `data_set`.
  - (+) Las consultas sobre `DataSet` devuelven instancias polimórficas reales (`FilmDataset` o `DataSet`) de forma transparente.
- **Desventajas**:
  - (-) La clase base mantiene la denominación histórica `DataSet` (con identidad `"uvl"`) en lugar de llamarse `BaseDataset`.

### Alternativa 2: Renombrar `DataSet` a `BaseDataset` abstracta y extraer `UVLDataset` + `FilmDataset`
- **Descripción**: Refactorizar el módulo `dataset` para renombrar la clase base a `BaseDataset` y mover las relaciones con `FeatureModel` a una nueva subclase `UVLDataset`.
- **Ventajas**:
  - (+) Nomenclatura totalmente simétrica entre tipos (`UVLDataset` y `FilmDataset`).
- **Desventajas**:
  - (-) Obliga a modificar imports, claves foráneas, repositorios, seeders y tests en `dataset`, `featuremodel`, `hubfile`, `explore` y `zenodo`.
  - (-) Alto riesgo de conflictos de mezcla con el resto de Work Items paralelos del equipo (`#177`, `#188`, `#213`).

### Alternativa 3: Single Table Inheritance añadiendo columnas de cine directamente a `data_set`
- **Descripción**: Almacenar los campos específicos de películas como columnas anulables dentro de la misma tabla `data_set`.
- **Ventajas**:
  - (+) Evita crear una tabla adicional con clave foránea.
- **Desventajas**:
  - (-) Hincha el modelo base con columnas ajenas a UVL y acopla todos los dominios en una sola tabla, incumpliendo el diseño modular pedido en `#178`.

---

## 4. Decisión Adoptada
Se adopta la **Alternativa 1** por unanimidad del equipo (4/4):
1. Mantener `DataSet` (`app/features/dataset/models.py`) como base polimórfica añadiendo `dataset_type` (`server_default="uvl"`) y `view_template()`.
2. Crear el feature `app/features/filmdataset` con `FilmDataset(DataSet)` sobre tabla `film_dataset` (`polymorphic_identity="film"`), migración Alembic `ac0193c9dea6` sobre `001.py`, y registro en `[tool.splent]` en `pyproject.toml`.
3. Establecer el contrato mínimo obligatorio del dominio CSV (`title`, `year`, `genre` normalizadas + `rating`/`duration` opcionales) y desacoplar el almacenamiento de ficheros mediante `uploads/user_<id>/dataset_<id>/` para reutilizar las descargas ZIP existentes.
4. Añadir `ZenodoService.upload_dataset_file(dataset, deposition_id, filename, user=None)` manteniendo intacto `upload_file` para UVL y consumiendo exclusivamente `ZENODO_API_URL`.

---

## 5. Consecuencias y Efectos Derivados

### Efectos Positivos:
- (+) Cero regresiones sobre UVL (los 267 tests heredados siguen en verde).
- (+) Cualquier nuevo dominio futuro solo requiere crear un feature con `rosemary feature:create` y una subclase de `DataSet`.
- (+) `fakenodo` (`#177`) funciona de forma idéntica para UVL y Film-Hub al compartir `ZenodoService`.

### Efectos Negativos o Deuda Técnica Asumida (Mitigación):
- (-) `ExploreRepository` realizaba originalmente un `INNER JOIN` sobre `DataSet.feature_models`, lo que excluiría a `FilmDataset` del buscador. **Mitigación**: En el bloque `2.C` de `#178` se sustituirá por `outerjoin` para incluir ambos tipos y filtrar por `dataset_type` y métricas de cine.
- (-) Las vistas de `dataset` deberán discriminar por `dataset.dataset_type` (o `view_template()`) para renderizar el bloque específico de tabla paginada. **Mitigación**: Ya expuesto el endpoint JSON paginado `GET /filmdataset/<id>/preview` para su consumo directo en el bloque `2.B`.

---

## 6. Referencias y Trazabilidad
- Issue oficial de referencia: `EGCETSII/uvlhub#178`
- Registro de decisiones del equipo: [toma_de_decisiones.md](../toma_de_decisiones.md) (`DEC-004`)
- Migración asociada: `migrations/versions/ac0193c9dea6_add_dataset_type_and_film_dataset_table.py`
