# AGENTS.md — Reglas de Desarrollo y Operación para Film-Hub

Este archivo define las normas obligatorias para desarrolladores y asistentes de IA que trabajen en **Film-Hub** (EGC 2026/2027, Universidad de Sevilla).

## 1. Arquitectura del Proyecto

* **Base tecnológica**: Python 3.13, Flask sobre `splent_framework`, SQLAlchemy, Alembic y MariaDB.
* **Estructura modular**: toda funcionalidad vive en `app/features/<feature>/` (modelos, repositorios, servicios, rutas, formularios, plantillas y `tests/`).
* **Registro declarativo**: cada feature se declara en `pyproject.toml` bajo `[tool.splent]` (`features`, `features_dev` para desarrollo/pruebas como `fakenodo`, y `features_prod`).
* **Entorno reproducible**: usar Docker Compose (`docker/docker-compose.dev.yml`) o DevContainer (`.devcontainer/`). No depender de configuraciones manuales locales no versionadas.

## 2. Flujo Git Obligatorio (EGCFlow)

* **Ramas permanentes (no destruir ni hacer force-push)**:
  * `trunk`: línea principal de integración continua del equipo.
  * `main`: línea de entregas estables y releases etiquetadas con SemVer (`vX.Y.Z`).
* **Ramas efímeras (siempre nacidas desde `trunk`)**:
  * `feature/WI-<id>-<resumen>`
  * `bugfix/issue-<id>-<resumen>`
  * `chore/<desc>`, `docs/<desc>`, `ci/<desc>`, `test/<desc>`
  * `hotfix/<version>-<resumen>`
* **Prohibición de Pull Requests internas**: nunca abrir Pull Requests para integrar trabajo dentro del equipo. La integración se realiza en local por Git CLI tras revisión por pares pre-merge:
  ```bash
  git checkout trunk
  git pull origin trunk
  git merge --no-ff <rama-efimera> -m "<tipo>(<alcance>): integrate <resumen> (#<id>)"
  git push origin trunk
  git branch -d <rama-efimera>
  git push origin --delete <rama-efimera>
  ```
* **Prohibición de commits desde GitHub web**: todos los cambios se commitean desde Git CLI local.
* **Identidad Git única**: mantener siempre el mismo `user.name` y `user.email` en todos los commits.
* **Regla de `rebase`**: usar `git rebase` únicamente sobre ramas privadas antes de integrar; nunca reescribir historia compartida en `trunk` o `main`.
* **Prioridad absoluta al build roto**: si `trunk` falla en CI, repararlo tiene prioridad sobre cualquier otra tarea.

## 3. Conventional Commits y Estilo

* **Formato obligatorio**: `<tipo>(<alcance>): <descripción concisa> (#<id_issue>)`
  * Tipos válidos: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
* **Commits atómicos**: cada commit agrupa un único cambio lógico y completo. No mezclar correcciones de bugs con refactorizaciones.
* **Cero emojis**: prohibido incluir emojis en commits, código, documentación, plantillas o comentarios de issues.
* **Estilo Python**: `black` (longitud 120), `isort` (perfil `black`, longitud 120) y `flake8` (longitud 120), configurados en `pyproject.toml`.

## 4. Comandos de Desarrollo, Linting y Pruebas

```bash
# Levantar entorno local de desarrollo
docker compose -f docker/docker-compose.dev.yml up -d

# Comprobar formato y análisis estático
rosemary linter
# Equivalente manual: flake8 && black --check . && isort --check-only .

# Ejecutar pruebas
rosemary test
rosemary test <feature>
pytest -m "not e2e" --cov=app --cov-report=term-missing
```

* Diseñar pruebas con criterio (particiones equivalentes, valores límite, cobertura CRUD y buenos oráculos), evitando pruebas superficiales que solo inflen cobertura.
* Ante un bug, seguir el ciclo de 4 fases documentado en [docs/gestion_bugs_e_incidencias.md](docs/gestion_bugs_e_incidencias.md): escribir primero una prueba de regresión que falle y luego corregir la causa raíz.

## 5. Coordinación de Migraciones Alembic

* Mantener una **única cadena lineal** en `migrations/versions/` (actualmente: `001` -> `a78bb2f87d2c` -> `ac0193c9dea6`).
* Antes de ejecutar `flask db migrate`, actualizar siempre desde `origin/trunk` y comprobar que no existen múltiples cabezas (`flask db heads`).
* Si dos ramas tocan la base de datos en paralelo, coordinar el encadenamiento de `down_revision` al integrar en `trunk`.

## 6. Uso Responsable de Inteligencia Artificial

* La IA puede acelerar borradores de código, pruebas o documentación, pero **el criterio humano es obligatorio** para diseño, seguridad, revisión de código, validación de oráculos y decisiones arquitectónicas (ADRs en `docs/adrs/`).
* Mantener cambios pequeños y revisables; nunca aceptar ni subir código sin entenderlo y verificarlo en ejecución.
* Nunca incluir credenciales, tokens ni archivos `.env` en el repositorio.