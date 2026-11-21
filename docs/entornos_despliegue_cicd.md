# Entornos de Despliegue - Film-Hub

Este documento define los entornos en los que desarrollamos, probamos y desplegamos **Film-Hub**, así como nuestros criterios de aislamiento, configuración y recuperación ante fallos. Hemos diseñado esta arquitectura buscando un enfoque **realista y asumible para un equipo de cuatro estudiantes**, aprovechando la infraestructura ya presente en el repositorio y servicios gratuitos en la nube.

> Este documento se complementa con la [Metodología de CI/CD y Estrategia de Pruebas](Metodologia_CI-CD.md) y la [Política de Ramas y Flujo de Trabajo (EGCFlow)](politica_ramas_y_flujo_trabajo.md).

---

## 1. Cadena de Entornos de Despliegue

Para reducir errores antes de exponer cambios a usuarios reales (o al profesorado durante las evaluaciones), separamos claramente el momento de tener una versión lista para entregar (*release*) del acto de instalarla y ejecutarla en un entorno concreto (*deploy*). Con ese objetivo, organizamos el recorrido del código en **cuatro entornos** que aumentan progresivamente nuestra confianza sobre cada cambio:

```text
+-------------------+     +---------------------+     +----------------------+     +--------------------+
|  1. DESARROLLO    |     |  2. PRUEBAS / CI    |     |  3. PREPRODUCCIÓN    |     |   4. PRODUCCIÓN    |
|     (Local)       | --> |  (GitHub Actions)   | --> |     (Staging)        | --> |   (Render.com)     |
| Docker Compose    |     | Runner ubuntu-24.04 |     | Imagen render + BD   |     | Imagen render + BD |
| Flask debug/seed  |     | efímero y hermético |     | de pruebas separada  |     | externa (filess.io)|
+-------------------+     +---------------------+     +----------------------+     +--------------------+
   ramas de tarea            cada push / rama            rama de integración            rama main
```

### 1.1. Resumen Comparativo de Entornos

| Característica | Desarrollo (Local) | Pruebas / Integración (CI) | Preproducción (*Staging*) | Producción |
| :--- | :--- | :--- | :--- | :--- |
| **Propósito** | Programar, depurar rápido y pasar tests locales | Validar cada cambio en un entorno limpio y aislado | Probar la aplicación integrada antes de hitos/entregas | Servicio accesible en vivo para demostración y uso real |
| **Infraestructura** | Docker Compose en el portátil de cada integrante (o Dev Container) | Runners efímeros `ubuntu-24.04` en GitHub Actions | Servicio web gratuito en Render.com (o comprobación local de `Dockerfile.render`) | Servicio web PaaS en **Render.com** (plan gratuito) |
| **Rama asociada** | Ramas de tarea (`feature/*`, `bugfix/*`, `chore/*`, `docs/*`) | Todas las ramas (Nivel 1) y rama de integración / `main` (Nivel 2) | Rama de integración (`trunk`) | Rama `main` (estados estables y etiquetados) |
| **`FLASK_ENV`** | `development` | `testing` | `production` | `production` |
| **Servidor web** | Flask dev server (`--reload --debug`, puerto `5000`) tras Nginx (`80`) | Cliente de pruebas Flask / servidor temporal en Selenium | Gunicorn (`0.0.0.0:80`) vía `render_entrypoint.sh` | Gunicorn (`0.0.0.0:80`) vía `render_entrypoint.sh` |
| **Base de datos** | MariaDB 12.0.2 en contenedor (`uvlhubdb` + `uvlhubdb_test`) | Contenedor de servicio `mariadb:12.0.2` (`uvlhubdb_test`) efímero | MariaDB externa independiente de producción (plan gratuito en `filess.io`) | MariaDB externa en `filess.io` con datos estables |
| **Servicio Zenodo** | `fakenodo` en local | `fakenodo` / dobles de prueba | `fakenodo` | `fakenodo` (o Zenodo Sandbox si se requiere validar integración real) |
| **Activación** | Manual por cada desarrollador | Automática con cada `git push` | Automática / bajo demanda tras integrar cambios en `trunk` | **Entrega Continua**: aprobación manual en GitHub (`CD_render.yml`) |

---

## 2. Descripción Detallada de Cada Entorno

### 2.1. Entorno de Desarrollo (Local)

Es el espacio de trabajo diario de los cuatro miembros del equipo. Para evitar el clásico problema de *"en mi máquina funciona"*, hemos decidido no configurar el entorno a mano ni depender de instrucciones de memoria, sino reproducirlo a partir de ficheros declarativos versionados en el repositorio.

* **Opción principal elegida — Docker Compose (`docker/docker-compose.dev.yml`)**:
  * Levanta de forma aislada la aplicación Flask con Python 3.13 (`Dockerfile.dev`), la base de datos MariaDB 12.0.2 (`Dockerfile.mariadb`), el proxy inverso Nginx (`nginx:1.29.1` en el puerto `80`) y los contenedores de Selenium Grid (`selenium-hub`, `selenium-chrome`, `selenium-firefox`) para pruebas E2E.
  * El script `docker/entrypoints/development_entrypoint.sh` espera a que MariaDB esté lista, crea la base de datos de pruebas (`uvlhubdb_test`), aplica las migraciones de Alembic (`flask db upgrade`), siembra datos iniciales (`rosemary db:seed -y`) si la base de datos está vacía y arranca Flask con recarga automática (`--reload --debug`).
  * La gestión cotidiana (linters, tests, migraciones, consola de BD) se realiza mediante la CLI del proyecto **`rosemary`**.
* **Opción integrada con el editor — Dev Containers (`.devcontainer/devcontainer.json`)**:
  * Quien trabaje con Visual Studio Code puede abrir el proyecto dentro del *Dev Container* configurado en el repositorio.
  * Esto unifica automáticamente el intérprete de Python (`/opt/venv/bin/python`), el formateador (`black`), el linter (`flake8`) y las extensiones esenciales, manteniendo el entorno local homogéneo independientemente de que cada integrante use Windows, macOS o Linux.
* **Alternativas descartadas para el día a día**:
  * **Instalación directa / `venv` (`.env.local.example`)**: aísla únicamente las dependencias de Python, pero no MariaDB ni utilidades del sistema, lo que aumenta el riesgo de diferencias entre máquinas. Solo se contempla de forma puntual si alguien no puede ejecutar Docker.
  * **Máquina virtual con Vagrant + Ansible (`vagrant/Vagrantfile`)**: aunque el repositorio base incluye esta configuración con Ubuntu 24.04 sobre VirtualBox (2 GB RAM, 4 vCPU), su consumo de disco y memoria y sus tiempos de arranque resultan excesivos para trabajar a diario en nuestros portátiles. Por ello optamos por contenedores Docker como mejor equilibrio entre aislamiento y agilidad.

---

### 2.2. Entorno de Pruebas e Integración Continua (CI)

Es un entorno **efímero, limpio y hermético** ejecutado en **GitHub Actions** (`ubuntu-24.04`) sin coste para el equipo. Al ejecutarse siempre sobre una máquina recién creada que se destruye al finalizar, evitamos la deriva de entornos (*environment drift*) y detectamos de inmediato dependencias no declaradas, ficheros olvidados o configuraciones locales ocultas.

* **Nivel 1 — CI rápida (en cada `push` a cualquier rama)**:
  * `CI_commits.yml`: valida el formato Conventional Commits (ignorando *merge commits*).
  * `CI_lint.yml`: ejecuta `flake8`, `black --check` e `isort --check-only` sobre `app` y `rosemary`.
  * `CI_pytest.yml`: levanta un servicio limpio `mariadb:12.0.2` con `healthcheck`, instala `requirements.txt` y `rosemary`, y ejecuta `pytest -m "not e2e" --cov=app` exigiendo cobertura mínima.
* **Nivel 2 — CI completa (al integrar en la rama de integración y en `main`)**:
  * `CI_full.yml`: ejecuta la suite E2E con Selenium (`pytest -v -m e2e`) contra MariaDB y realiza una compilación de comprobación (*dry-run*) de `docker/images/Dockerfile.render` para asegurar que el artefacto desplegable sigue construyéndose sin errores.
* **Pruebas de carga (Locust)**:
  * Por coste y tiempo de ejecución, hemos decidido no ejecutar las pruebas de carga (`rosemary locust`) en la CI automática; se lanzan de forma manual en local antes de hitos relevantes.

---

### 2.3. Entorno de Preproducción (*Staging*)

El objetivo de preproducción es validar los cambios integrados en condiciones **lo más parecidas posible a producción** antes de llevarlos a `main` y exponerlos en el entorno final.

Como somos un equipo de estudiantes sin presupuesto para alquilar servidores VPS ni infraestructuras dedicadas, adoptamos una solución pragmática con dos mecanismos complementarios:

1. **Instancia de *Staging* en Render.com (opción principal en nube)**:
   * Un servicio web independiente en Render.com (plan gratuito) apuntando a la rama de integración (`trunk`) y construido con el **mismo** `docker/images/Dockerfile.render` y el **mismo** `docker/entrypoints/render_entrypoint.sh` que producción.
   * Utiliza `FLASK_ENV=production` y Gunicorn (exactamente igual que producción), pero con `FLASK_APP_NAME="Film-Hub (Staging)"` y conectado a una **base de datos MariaDB independiente** (en `filess.io`) con datos de prueba para no contaminar nunca la base de datos de producción.
   * Nos sirve para que QA, Frontend y PM realicen pruebas de aceptación manuales, comprueben migraciones de base de datos en un contenedor real y validen la integración de los Work Items antes de cada seguimiento oficial.
2. **Validación local del contenedor de producción (respaldo ante límites del plan gratuito)**:
   * Si en algún momento las cuotas del plan gratuito (límite de horas o de bases de datos gratuitas) impiden mantener activa la instancia *staging* en la nube, el responsable de DevOps valida localmente la imagen construida con `Dockerfile.render` apuntando a una MariaDB local limpia antes de autorizar el paso a `main`.
   * Así garantizamos en todo caso que se prueban la imagen multi-etapa, Gunicorn, la carga de módulos de producción (`features_prod` en `pyproject.toml`) y las migraciones de Alembic antes de desplegar.

---

### 2.4. Entorno de Producción

Es el entorno accesible públicamente donde se ejecuta la versión estable de **Film-Hub** para usuarios finales y para la evaluación del proyecto.

* **Plataforma PaaS — Render.com**:
  * Elegimos Render frente a administrar un servidor VPS propio (con Nginx, certificados TLS, Watchtower y webhooks manuales) porque evita mantener máquinas configuradas a mano difíciles de reproducir (*servidores copo de nieve*), gestiona HTTPS automáticamente y el repositorio ya incluye `Dockerfile.render` y `render_entrypoint.sh` preparados para ello.
* **Empaquetado reproducible (imagen Docker multi-etapa)**:
  * `docker/images/Dockerfile.render` construye la imagen en dos etapas sobre `python:3.13-slim`: una etapa `builder` que compila las dependencias necesarias dentro de un entorno virtual `/opt/venv` y una etapa final ligera que solo incluye el runtime, `mariadb-client`, el código de `app/`, `migrations/`, `pyproject.toml` y los scripts de arranque.
  * Al arrancar el contenedor, `render_entrypoint.sh` espera a la disponibilidad de MariaDB (`scripts/wait-for-db.sh`), aplica las migraciones pendientes con `flask db upgrade` y lanza la aplicación con **Gunicorn** en el puerto `80`.
* **Base de datos externa**:
  * MariaDB alojada en un proveedor gestionado con capa gratuita (como **filess.io**), conectada mediante variables de entorno (`MARIADB_HOSTNAME`, `MARIADB_PORT`, `MARIADB_DATABASE`, `MARIADB_USER`, `MARIADB_PASSWORD`). El arranque de la aplicación (`app/__init__.py`) respeta explícitamente puertos personalizados mediante `MARIADB_PORT`.
* **Limitaciones conocidas y asumidas**:
  * **Arranque en frío (*cold start*)**: el plan gratuito de Render suspende el servicio tras periodos de inactividad, por lo que la primera petición puede tardar unos segundos en responder.
  * **Sistema de ficheros efímero**: al redesplegar o reiniciar el contenedor en el plan gratuito, los archivos guardados únicamente en disco local del contenedor pueden perderse; los metadatos persistentes viven siempre en MariaDB y los depósitos simulados se apoyan en `fakenodo`.
  * **Sin alta disponibilidad ni escalado horizontal**: una única instancia es suficiente para el volumen de tráfico de nuestro proyecto.

---

## 3. Gestión de Configuración, Módulos y Secretos

Para mantener la trazabilidad y la seguridad en todos los entornos, aplicamos las siguientes reglas:

1. **Separación entre código y configuración**:
   * El comportamiento específico de cada entorno (nombre de la app, modo de Flask, credenciales de base de datos, dominio, `SECRET_KEY`) nunca se codifica en el código fuente, sino que se inyecta mediante variables de entorno.
   * En el repositorio solo se versionan plantillas de ejemplo sin datos reales: `.env.docker.example`, `.env.local.example`, `.env.docker.production.example` y `.env.vagrant.example`.
2. **Protección de secretos**:
   * El fichero `.env` real está excluido explícitamente en `.gitignore`.
   * En GitHub Actions, el secreto `RENDER_DEPLOY_HOOK_URL` se almacena exclusivamente en el entorno protegido `production` de GitHub.
   * En Render (tanto *staging* como producción), `SECRET_KEY` (obligatoria en `ProductionConfig`) y las credenciales de MariaDB se configuran desde el panel de variables de entorno de la plataforma.
3. **Activación declarativa de funcionalidades por entorno**:
   * El archivo `pyproject.toml` (`[tool.splent]`) declara de forma explícita qué módulos (`features`, `features_dev`, `features_prod`) se cargan según el entorno (`dev` frente a `prod`). Esto nos permite controlar qué se activa en cada entorno sin añadir herramientas externas de *feature flags*.
4. **Migraciones de base de datos**:
   * Cualquier cambio en el modelo de datos se gestiona siempre mediante migraciones versionadas en `migrations/` (Alembic / Flask-Migrate), nunca modificando tablas a mano en la base de datos de *staging* o producción.

---

## 4. Estrategia de Entrega, Despliegue y Recuperación

### 4.1. Por qué elegimos Entrega Continua y no Despliegue Continuo Automático

En Film-Hub hemos optado por **Entrega Continua (*Continuous Delivery*)** con aprobación manual para pasar a producción:

* Como trabajamos con **EGCFlow sin Pull Requests internas** (integraciones por `git merge` en local), un despliegue automático inmediato tras cada `push` a `main` podría publicar un error humano sin filtro previo.
* Con `CD_render.yml`, tras finalizar en verde `CI_full.yml` sobre `main`, el flujo queda en espera en el entorno `production` de GitHub hasta que el responsable de DevOps aprueba explícitamente el disparo del *Deploy Hook* de Render.
* Asimismo, descartamos estrategias de *rollout* progresivo (*canary releases*, despliegue *blue-green* o balanceo de tráfico por porcentajes), ya que requieren múltiples instancias y observabilidad avanzada que no se justifican para el alcance y recursos de nuestro equipo.

### 4.2. Recuperación ante Fallos: *Rollback* y *Rollforward*

Asumiendo que incluso con CI/CD y preproducción puede llegar un fallo a producción, hemos definido dos respuestas según la naturaleza del problema:

* ***Rollback* (vuelta atrás rápida)**:
  * **Cuándo usarlo**: si el fallo aparece justo tras un despliegue y **no** ha habido migraciones destructivas en MariaDB (cuando la versión anterior sigue siendo compatible con el esquema y datos actuales).
  * **Cómo ejecutarlo**:
    1. Desde el panel de **Render.com**, seleccionar el último despliegue estable anterior y pulsar **Rollback** (recuperación en pocos minutos sin rehacer el código).
    2. En Git, reflejar el estado en `main` si procede (por ejemplo mediante `git revert` para no reescribir la historia compartida) y registrar la incidencia en [Gestión de Bugs e Incidencias](gestion_bugs_e_incidencias.md).
* ***Rollforward* (corrección hacia delante)**:
  * **Cuándo usarlo**: si el despliegue introdujo una migración de esquema o un cambio de formato de datos incompatible con la versión anterior, donde volver atrás provocaría más errores.
  * **Cómo ejecutarlo**:
    1. Crear una rama `hotfix/<resumen>` desde `main`.
    2. Añadir una prueba de regresión que reproduzca el fallo y aplicar la corrección mínima.
    3. Validar en local y en CI, fusionar en `main` (y sincronizar de vuelta a `trunk`), y aprobar el nuevo despliegue en Render mediante `CD_render.yml`.
