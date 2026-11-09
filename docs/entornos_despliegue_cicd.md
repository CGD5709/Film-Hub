# Entornos de Despliegue, Estrategia CI/CD y Trazabilidad

Este documento define la arquitectura de despliegue y los flujos automatizados de **Integracion Continua (CI)**, **Entrega Continua (CD)** y **Despliegue Continuo** del proyecto **Film-Hub**, de acuerdo con los fundamentos teoricos y practicos de la asignatura **Evolucion y Gestion de la Configuracion (EGC)**.

---

## 1. Cadena de Entornos de Despliegue

Conforme a la definicion de la disciplina, *"desplegar no equivale a entregar, y la transicion entre entornos progresivos incrementa la certidumbre sobre el comportamiento del sistema antes de exponerlo a usuarios reales"*. Film-Hub articula una cadena de tres entornos aislados:

```text
+-------------------+      +-------------------------+      +---------------------+
|    DESARROLLO     |      | PREPRODUCCION (STAGING) |      |     PRODUCCION      |
|  (Entorno Local)  | ---> |  (Validacion Continua)  | ---> | (Servicio en Vivo)  |
| Docker Compose Dev|      |   Docker Compose Prod   |      | Artefacto Inmutable |
| Hot-reload / Mocks|      | Tests E2E / Fakenodo    |      | Alta Disponibilidad |
+-------------------+      +-------------------------+      +---------------------+
```

### 1.1. Especificacion Comparativa de Entornos

| Parametro | Entorno de Desarrollo (Local) | Entorno de Preproduccion (Staging) | Entorno de Produccion |
| :--- | :--- | :--- | :--- |
| **Infraestructura** | Docker Compose local / DevContainer | Contenedor aislado en servidor staging o PaaS | Contenedor en servidor de produccion (PaaS / VPS) |
| **Rama Asociada** | Ramas de tarea (`feature/*`, `bugfix/*`) | Rama `trunk` tras integracion local | Rama `main` asociada a etiqueta SemVer |
| **Configuracion** | `.env.local` / `docker-compose.dev.yml` | `.env.staging` / `docker-compose.prod.yml` | `.env.production` / `docker-compose.prod.ssl.yml` |
| **Base de Datos** | MariaDB local `uvlhubdb_dev` con datos ficticios | MariaDB staging `uvlhubdb_staging` | MariaDB produccion `uvlhubdb` con copias de seguridad |
| **Servicio Zenodo** | Fakenodo en ejecucion local | Fakenodo para validacion de pruebas E2E | Fakenodo o Zenodo Sandbox oficial |
| **Objetivo** | Programacion diaria y depuracion rapida | Validacion de integracion y pruebas de aceptacion | Servicio final operativo y monitorizado |
| **Disparador** | Manual por el desarrollador | Despliegue automatizado tras merge a `trunk` | Despliegue automatizado tras publicacion de Release |

---

## 2. Flujos de Trabajo en GitHub Actions

Los flujos de automatizacion se localizan en `.github/workflows/` y se ejecutan sobre entornos limpios `ubuntu-24.04`.

```text
[ Evento: Push o Pull Request ]
               |
               +---> 1. CI: Commits Syntax Checker (Conventional Commits)
               +---> 2. CI: Python Lint (flake8, black, isort)
               +---> 3. CI: Pytest (MariaDB Service + Rosemary)
                           |
                           v (Al mergear en trunk con CI en verde)
                     4. CD: Despliegue en Preproduccion (Staging)
                           |
                           v (Al publicar Release vX.Y.Z en main)
                     5. CD: Construccion y Publicacion de Imagen Docker Hub
                           |
                           v
                     6. CD: Notificacion a Webhook de Despliegue en Produccion
```

### 2.1. Pipelines de Integracion Continua (CI)

1. **`CI_commits.yml` (Comprobacion de Sintaxis de Commits)**:
   - Se ejecuta ante cualquier `push` o `pull_request`.
   - Garantiza que los mensajes de commit se ajusten a Conventional Commits (`tipo(ambito): descripcion (#issue)`).

2. **`CI_lint.yml` (Calidad y Formato Estatico)**:
   - Se ejecuta ante cualquier `push` o `pull_request`.
   - Herramientas aplicadas:
     - `flake8`: Cumplimiento del estandar de estilo PEP8.
     - `black --check`: Verificacion de formateo inmutable de codigo.
     - `isort --check-only`: Ordenacion determinista de importaciones.

3. **`CI_pytest.yml` (Suite de Pruebas Automatizadas)**:
   - Se ejecuta ante `push` y `pull_request` con destino en `trunk` y `main`.
   - Inicializa un contenedor de servicio con MariaDB 12 y healthcheck activo.
   - Instala el conjunto de dependencias y la CLI local Rosemary.
   - Ejecuta las pruebas unitarias y de integracion de todos los modulos en `app/features/`.

### 2.2. Pipelines de Entrega Continua (CD - Delivery)

1. **`CD_dockerhub.yml` (Generacion de Artefacto Inmutable)**:
   - Disparador: Publicacion formal de un Release en GitHub (`release: [published]`).
   - Construye la imagen de produccion con `docker/images/Dockerfile.prod` inyectando el argumento `VERSION_TAG=$TAG`.
   - Publica la imagen en Docker Hub bajo dos identificadores:
     - Version inmutable: `<usuario>/filmhub:<version_tag>`
     - Puntero funcional: `<usuario>/filmhub:latest`

### 2.3. Pipelines de Despliegue Continuo (CD - Deployment)

1. **`CD_webhook.yml` (Despliegue Desatendido)**:
   - Disparador: Finalizacion exitosa del workflow de pruebas en `main`.
   - Emite una llamada HTTP POST segura al endpoint de despliegue configurado:
     ```bash
     curl -X POST https://${WEBHOOK_DOMAIN}/webhook/deploy \
          -H "Authorization: Bearer ${WEBHOOK_TOKEN}"
     ```
   - El receptor ejecuta de forma automatica:
     ```bash
     docker compose pull web
     docker compose up -d web
     docker compose exec -T web rosemary db:migrate
     ```

---

## 3. Gestion de Migraciones y Variables de Entorno

- **Principio de Idempotencia**: Toda modificacion sobre el esquema relacional de MariaDB debe ser gestionada mediante Alembic y ejecutada a traves de `rosemary db:migrate`.
- **Aislamiento de Secretos**: Ninguna variable de entorno sensible o credencial de base de datos se versiona en el repositorio. Se configuran mediante paneles de secretos o archivos `.env` excluidos explicitamente en `.gitignore`.

---

## 4. Estrategia de Rollback y Rollforward

Conforme a las directrices de gestion de riesgos de la asignatura:

### 4.1. Procedimiento de Rollback Inmediato
Si una release en produccion presenta un fallo critico bloqueante:
1. Localizar la etiqueta de la version inmediatamente anterior estable en el registro de Docker Hub (ejemplo: `v1.0.1`).
2. Actualizar el puntero del servicio a dicha imagen:
   ```bash
   docker pull <usuario>/filmhub:v1.0.1
   docker tag <usuario>/filmhub:v1.0.1 <usuario>/filmhub:latest
   docker compose up -d web
   ```
3. El tiempo de recuperacion (MTTR) no requiere reconstruccion de codigo fuente ni compilacion intermedia.

### 4.2. Procedimiento de Rollforward
Si el fallo requiere la correccion de datos o un ajuste de codigo que no puede solucionarse mediante reversion de imagen:
1. Crear una rama de intervencion rapida `hotfix/<version>-<resumen>` a partir de `main`.
2. Programar la prueba de regresion que manifieste el defecto.
3. Aplicar la solucion minima, validar en local e integrar directamente en `main` y `trunk` mediante Git CLI.
4. Etiquetar la version con incremento de parche (`PATCH`), construyendo un nuevo artefacto inmutable.

---

## 5. Monitoreo y Verificacion de Salud (Healthcheck)

El servicio cuenta con un endpoint `/health` que retorna el estado del servidor web y su conexion con la base de datos MariaDB:
- Codigo de respuesta HTTP 200 en estado operativo.
- Comprobacion periodica configurada en Docker Compose cada 30 segundos.
- En caso de degradacion continua, Nginx desvia las peticiones hacia la pagina de contingencia `docker/nginx/html/502_prod.html`.
