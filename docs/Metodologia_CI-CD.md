# Metodología de CI/CD y Estrategia de Pruebas — Film-Hub

**Asignatura:** Evolución y Gestión de la Configuración (EGC 2026/2027)  
**Fecha:** 21/11/2026 | **Proyecto:** Film-Hub (fork de UVLHub)  
**Integrantes:** José Vicente Sánchez Montilla (PM), Juan Felipe Pardo Carrillo (QA), Adrián Muñoz Aradilla (UI/UX), Luis Lucena Prieto (DevOps / Lead Dev)

---

## 1. Contexto y forma de trabajo en el repositorio

En este documento recogemos cómo vamos a organizar la integración continua, el despliegue y las pruebas automatizadas en **Film-Hub**, nuestro fork de UVLHub adaptado a datasets de películas (`WI-newdataset`) y con el servicio simulado `WI-fakenodo`.

Tal y como acordamos en el acta fundacional, trabajamos con **EGCFlow** usando las ramas `main` (producción), `develop` (integración) y ramas de trabajo (`feature/WI-<id>-<desc>`, `bugfix/issue-<id>-<desc>`, `chore/<desc>` y `docs/<desc>`). Sin embargo, en este proyecto no vamos a trabajar con Pull Requests, sino que haremos las integraciones directamente con comandos `git merge` en local y su correspondiente `git push` (actualizaremos también ese punto en el acta fundacional para que ambos documentos coincidan).

Trabajar sin Pull Requests nos lleva a adaptar las reglas de CI/CD de la siguiente manera:

* **Disparadores en `push`:** Eliminamos el disparador `pull_request` de todos los workflows; la CI salta cada vez que alguien hace `git push` a una rama.
* **CI en verde antes de fusionar:** Nadie hace `git merge` de su rama a `develop` (ni de `develop` a `main`) sin comprobar antes que el último `push` de su rama ha pasado todos los workflows rápidos en verde.
* **Merge commits permitidos:** El validador de Conventional Commits revisa todos los commits de trabajo, pero ignora los commits automáticos de fusión (`--no-merges`) que genera Git al ejecutar `git merge`.

---

## 2. Metodología CI/CD y entornos de despliegue

Para el desarrollo diario usamos el entorno local con Docker Compose (`docker-compose.dev.yml`), que levanta de forma aislada la aplicación Flask (Python 3.13), MariaDB 12.0.2, Nginx y Selenium. Para producción hemos elegido **Render.com**, porque el repositorio ya trae preparados `docker/images/Dockerfile.render` y `docker/entrypoints/render_entrypoint.sh`, y permite lanzar despliegues mediante un *Deploy Hook* sin administrar un servidor VPS.

En la parte de CD hemos elegido **Integración Continua (CI) + Entrega Continua (Continuous Delivery)** en lugar de Despliegue Continuo directo. Como no tenemos el filtro previo de una Pull Request antes de tocar `main`, un despliegue totalmente automático podría publicar un error en producción tras un `push` accidental. Con Entrega Continua, el código de `main` pasa todas las pruebas y queda listo para publicarse, pero el disparo final hacia Render requiere una aprobación manual del responsable de DevOps en el entorno `production` de GitHub. Por ahora no gestionamos *releases* ni etiquetas de versión (`vX.Y.Z`): cada actualización aprobada en `main` actualiza directamente producción.

---

## 3. Comprobaciones obligatorias y flujo local

Para evitar subir errores de formato o regresiones, nuestro pipeline comprueba cuatro aspectos en cada subida:

* **Estilo y formato:** Ejecución de `flake8`, `black --check` e `isort --check-only` sobre `app` y `rosemary` (longitud máxima de 120 caracteres según `pyproject.toml`).
* **Conventional Commits:** Validación del formato `<tipo>(<alcance>): <descripción>` en todos los commits que no sean merges.
* **Tests automatizados:** Ejecución de la suite de `pytest` contra una instancia limpia de MariaDB 12.0.2, exigiendo el 100% de pruebas en verde.
* **Cobertura de código:** Cálculo con `pytest-cov` mostrando las líneas sin cubrir y aplicando un umbral mínimo (`--cov-fail-under`, fijado inicialmente en torno al 70% y ajustable en cuanto midamos la cobertura base del fork).

Antes de hacer `git push`, cada miembro del equipo pasa en local los comandos de la CLI del proyecto (`rosemary`): `rosemary linter:fix` para formatear, `rosemary linter` para comprobar `flake8` y `rosemary test` para lanzar las pruebas rápidas. Cuando se tocan vistas o flujos de pantalla, se ejecuta además `rosemary selenium`.

---

## 4. Pruebas existentes en el fork y política de testing

Antes de decidir qué pruebas añadir, hemos auditado qué traía exactamente el fork base de Film-Hub. En total cuenta con **306 funciones de test** (263 pruebas rápidas de `pytest` y 43 pruebas E2E con Selenium) además de **8 ficheros `locustfile.py`** para pruebas de carga:

| Módulo | Unit/Cfg | Repo | Service | Integr. | Selenium | Total | Locust |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `tests/` (global) | 5 | 0 | 0 | 0 | 0 | 5 | No |
| `auth` | 2 | 2 | 2 | 4 | 2 | 12 | Sí |
| `dataset` | 10 | 9 | 12 | 14 | 7 | 52 | Sí |
| `explore` | 0 | 13 | 5 | 6 | 9 | 33 | Sí |
| `featuremodel` | 4 | 5 | 5 | 3 | 4 | 21 | No |
| `flamapy` | 8 | 0 | 7 | 11 | 0 | 26 | Sí |
| `hubfile` | 6 | 7 | 9 | 10 | 0 | 32 | Sí |
| `profile` | 5 | 7 | 8 | 9 | 7 | 36 | Sí |
| `public` | 0 | 0 | 3 | 5 | 6 | 14 | Sí |
| `team` | 0 | 0 | 0 | 2 | 4 | 6 | Sí |
| `webhook` | 12 | 4 | 4 | 9 | 0 | 29 | No |
| `zenodo` | 7 | 6 | 19 | 4 | 4 | 40 | No |
| **Total base** | **59** | **53** | **74** | **77** | **43** | **306** | **8** |

### 4.1. Adaptación de los tests heredados y política para nuevos WIs

Al cambiar el dominio de UVL a películas, una parte de los tests heredados tendrá que evolucionar:

* **`WI-newdataset`:** Los tests de `flamapy` (26), `featuremodel` (21) y las comprobaciones de extensión `.uvl` en `dataset` y `hubfile` están ligados al dominio original. Se sustituirán o adaptarán por pruebas propias del formato y validaciones de Film-Hub para no perder cobertura.
* **`WI-fakenodo`:** Los 40 tests de `zenodo` nos sirven de referencia del contrato esperado (crear *deposition*, subir archivo, publicar y obtener DOI). El nuevo servicio `fakenodo` incluirá sus propios tests unitarios, de servicio y de integración HTTP.

Para el resto de Work Items acordamos una política equilibrada revisada por QA: todos los WIs deben añadir tests unitarios/de servicio de su lógica (y de integración HTTP si crean o modifican rutas), los tests E2E de Selenium solo serán obligatorios en WIs con impacto relevante en la interfaz (subida, listado, exploración o vista del dataset), y ningún cambio puede romper los tests de otros módulos. Las pruebas de carga con Locust no se ejecutan en CI; se lanzan a mano con `rosemary locust` antes de las entregas importantes.

---

## 5. Pipeline de CI/CD en GitHub Actions

### 5.1. Revisión de los workflows heredados del fork

Partiendo de los ficheros que ya existían en `.github/workflows/`, hemos decidido aprovechar la base de CI que encaja con nuestra metodología, descartar los flujos de CD que no aplican y añadir las piezas que faltaban:

| Fichero en `.github/workflows/` | Decisión | Motivo |
| :--- | :--- | :--- |
| `CI_lint.yml` | **Conservar y ajustar** | Ya valida `flake8`, `black` e `isort` con Python 3.13; solo eliminamos el trigger `pull_request`. |
| `CI_commits.yml` | **Conservar y adaptar** | Quitamos `pull_request` y sustituimos la acción de `webiny` por una comprobación con `git log --no-merges` para que no falle con los *merge commits* locales. |
| `CI_pytest.yml` | **Conservar y adaptar** | Quitamos `pull_request`, ampliamos el trigger a `push` en cualquier rama (antes solo `main` y `trunk`), incluimos `tests/` además de `app/features/` y añadimos cobertura con `pytest-cov`. |
| `CD_dockerhub.yml` | **Eliminar** | Publicaba imágenes de `uvlhub` en Docker Hub al crear *releases*; por ahora no usamos Docker Hub ni *releases* formales. |
| `CD_webhook.yml` | **Eliminar** | Estaba orientado a despliegue en VPS por webhook (y además no encaja con Render.com). |
| `CI_full.yml` | **Añadir** | Nivel 2 de CI para ejecutar los tests E2E de Selenium y verificar la construcción de `Dockerfile.render` en `develop` y `main`. |
| `CD_render.yml` | **Añadir** | Nivel 3 para lanzar el despliegue en Render.com desde `main` tras aprobación manual de DevOps. |

### 5.2. Arquitectura final del pipeline (dos niveles de CI + CD)

| Nivel / Workflows | Cuándo se ejecuta | Qué hace | Objetivo |
| :--- | :--- | :--- | :--- |
| **Nivel 1 — CI Rápida**<br>`CI_commits.yml`<br>`CI_lint.yml`<br>`CI_pytest.yml` | En cada `push` a cualquier rama. | 1. Valida Conventional Commits (`--no-merges`).<br>2. Pasa `flake8`, `black --check` e `isort --check-only`.<br>3. Ejecuta `pytest -m "not e2e" --cov=app` (263 tests rápidos + MariaDB 12.0.2). | Dar feedback en ~2-3 min antes de hacer `git merge` hacia `develop`. |
| **Nivel 2 — CI Completa**<br>`CI_full.yml` | Al hacer `push` en `develop` o `main` (o ejecución manual). | 1. Ejecuta los 43 tests E2E con Selenium (`pytest -v -m e2e`) contra MariaDB.<br>2. Comprueba que `Dockerfile.render` construye correctamente. | Validar flujos de navegador y empaquetado tras integrar cambios. |
| **Nivel 3 — CD Render**<br>`CD_render.yml` | Cuando `CI_full.yml` acaba en verde en `main` (o manual). | 1. Espera la aprobación manual en el entorno `production` de GitHub.<br>2. Lanza el *Deploy Hook* de Render (`RENDER_DEPLOY_HOOK_URL`). | Desplegar en producción de forma controlada sin depender de PRs. |

### 5.3. Flujo diario y ajustes iniciales

En el día a día, el ciclo para cada tarea será: crear la rama desde `develop`, implementar junto con sus tests, pasar `rosemary linter:fix`, `rosemary linter` y `rosemary test` en local, hacer `git push` y comprobar que los tres workflows de Nivel 1 (`CI_commits`, `CI_lint` y `CI_pytest`) acaban en verde. Con el visto bueno de QA o Lead Dev, se integra en `develop` mediante `git merge` local y `git push`, lo que dispara `CI_full.yml`. Cuando `develop` esté estable y `CI_full.yml` en verde, se fusiona en `main` y DevOps aprueba el despliegue en Render desde GitHub.

Para dejar el pipeline operativo tras actualizar `.github/workflows/`, completaremos tres pasos iniciales: crear el servicio web en Render apuntando a `Dockerfile.render`, configurar el entorno `production` en GitHub con revisor obligatorio (DevOps) y el secreto `RENDER_DEPLOY_HOOK_URL`, y comprobar en la primera ejecución tanto el porcentaje real de cobertura para fijar `--cov-fail-under` como el arranque de Selenium definido en `tests/selenium_support.py`.