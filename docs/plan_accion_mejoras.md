# Plan de Acción y Reparto de Mejoras (EGC 2026/2027) - Film-Hub

Este documento constituye la guía operativa para ejecutar las mejoras metodológicas, técnicas y de trazabilidad de **Film-Hub** tras la primera sesión de revisión. Integra:

1. Las **4 prácticas y retos oficiales de EGC 2026/2027** (Git CLI sin Pull Requests internas, CI/CD con `workflow_call`, Releases SemVer + SBOM/CRA, pruebas automatizadas/Locust y DevContainers).
2. Los **principios del material oficial de la asignatura EGC 2026/2027**: Capítulos 2 (CI/CD y Releases), 3 (Gestión de código fuente, EGCFlow e IA), 4 (Diseño de pruebas, pirámide y cobertura), 5 (Gestión de tareas, depuración en 4 fases y aprendizaje) y 6 (Aislamiento y reproducibilidad).
3. Las lecciones extraídas del análisis comparativo de otros grupos de EGC.

Todas las tareas respetan **EGCFlow**: ramas efímeras nacidas desde `trunk`, prohibición de Pull Requests internas, prohibición de commits desde la interfaz web de GitHub, identidad Git única por integrante, Conventional Commits vinculados a issue `(#<id>)`, cero emojis, revisión por pares pre-merge e integración local mediante `git merge --no-ff` en `trunk`.

---

## 1. Matriz Global de Reparto y Balance de Carga

### 1.1. Las 11 Issues Atómicas de Mejora

| ID | Título Resumido | Responsable (`Assignee`) | Revisor Pre-Merge | Rama / Tipo | Labels |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **T0** | Acta de revisión (23/11/2026), plan unificado de WIs y mejoras | Juan Felipe (`@jfpaardoo`) | `@CGD5709` | `docs/plan-unificado-tareas` | `type: docs` |
| **T1** | Rulesets (`main` y `trunk`) + hacer público el Project + verificar identidades | José Vicente (`@CGD5709`, Owner) | `@LuisLucena5` | *(Configuración GitHub UI)* | `type: chore` |
| **T2** | Guía de issues, labels, assignees, comentarios, priorización y reglas Git | José Vicente (`@CGD5709`) | `@adriaradillam` | `docs/guia-issues-y-tablero` | `type: docs` |
| **T3** | Normalizar issues `#1`-`#8` y desglosar sub-issues de WIs pendientes | José Vicente (`@CGD5709`) | `@adriaradillam` | *(Gestión GitHub / Tablero)* | `type: chore` |
| **T4** | Workflows `CI_branches.yml`, `CI_commits.yml` (`#id`) y `CI_full.yml` (`trunk`) | Luis Lucena (`@LuisLucena5`) | `@jfpaardoo` | `ci/workflows-branches-commits` | `type: ci-cd` |
| **T5** | Workflow reutilizable (`workflow_call`), SBOM (Syft/licencias) y Release `v1.0.0` | Luis Lucena (`@LuisLucena5`) | `@jfpaardoo` | `ci/release-sbom-and-reusable` | `type: ci-cd` |
| **T6** | Verificar despliegue PRE (`trunk`) y aprobación CD Render (`main`) | Luis Lucena (`@LuisLucena5`) | `@CGD5709` | `ci/verify-render-pre-prod` | `type: ci-cd` |
| **T7** | Plantillas de issues (estructura actual), `AGENTS.md` y ciclo de bugs `#188` | Juan Felipe (`@jfpaardoo`) | `@adriaradillam` | `chore/issue-templates-and-agents` | `type: docs`, `type: chore` |
| **T8** | Workflow de seguridad (`CI_security.yml`: Gitleaks + `pip-audit`) y cobertura | Juan Felipe (`@jfpaardoo`) | `@LuisLucena5` | `ci/security-gitleaks-and-audit` | `type: ci-cd` |
| **T9** | Alinear `Metodologia_CI-CD.md` (Cap. 2 y 4) y actualizar índice `docs/README.md` | Adrián Muñoz (`@adriaradillam`) | `@CGD5709` | `docs/align-cicd-and-readme` | `type: docs` |
| **T10** | Validar DevContainer (Práctica 4) y pruebas Locust pre-release `v1.0.0` (Práctica 3) | Adrián Muñoz (`@adriaradillam`) | `@jfpaardoo` | `chore/verify-devcontainer-and-locust` | `type: test`, `type: chore` |

### 1.2. Balance de Carga Total (Work Items + Tareas T0-T10)

| Integrante | WIs Asignados (`descomposicion_work_items.md`) | Tareas de Mejora | Revisiones WIs | Revisiones Mejoras | Total Revisiones |
| :--- | :--- | :---: | :--- | :---: | :---: |
| **José Vicente (`@CGD5709`)** | `#188` (Hecho), `#178` (2.C) | T1, T2, T3 | `#177`, `#200` | T0, T6, T9 | **5** |
| **Luis Lucena (`@LuisLucena5`)** | `#177`, `#202` | T4, T5, T6 | `#178` (2.A), `#213` | T1, T8 | **4** |
| **Juan Felipe (`@jfpaardoo`)** | `#178` (2.A Hecho), `#200` | T0, T7, T8 | `#188`, `#202`, `#178` (2.B) | T4, T5, T10 | **6** |
| **Adrián Muñoz (`@adriaradillam`)** | `#213`, `#178` (2.B) | T9, T10 | `#178` (2.C) | T2, T3, T7 | **4** |

### 1.3. Orden de Ejecución y Dependencias

```text
[Paso 0: Abrir las 11 issues en GitHub (empezando por T0) con su Assignee y Labels para obtener los #id]
    │
    ├──► T0 (@jfpaardoo): Acta de reunión 23/11/2026 + unificar descomposicion_work_items.md y plan_accion_mejoras.md
    │         │
    │         └──► (Una vez T0 publica acta + plan maestro en trunk y se limpia el historial pre-fork si procede)
    │
    ├──► T1 (@CGD5709): Hacer público el Project + Rulesets iniciales en main/trunk
    ├──► T7 (@jfpaardoo): Plantillas .github/ISSUE_TEMPLATE/ + AGENTS.md + Bugs #188 + Reglas depuración
    │         │
    │         └──► (Una vez T7 y T1 están en trunk)
    │
    ├──► T2 (@CGD5709): Guía de issues, tablero, priorización y reglas Git
    ├──► T4 (@LuisLucena5): CI_branches.yml + CI_commits.yml (#id) + CI_full.yml (trunk)
    ├──► T8 (@jfpaardoo): CI_security.yml (Gitleaks + pip-audit) + revisión --cov-fail-under
    ├──► T10 (@adriaradillam): Validar DevContainer + Locust pre-release
    │         │
    │         └──► (Cuando T2, T4, T8 estén en trunk)
    ├──► T3 (@CGD5709): Normalizar #1-#8 y abrir sub-issues de WIs pendientes
    ├──► T6 (@LuisLucena5): Verificar PRE (trunk) y PROD (main) en Render
    ├──► T9 (@adriaradillam): Actualizar Metodologia_CI-CD.md y docs/README.md
    │         │
    │         └──► T5 (@LuisLucena5): Workflow reutilizable + CD_release.yml (SBOM) + Tag/Release v1.0.0 en main
```

---

## 2. Estructura Estándar de Plantilla de Issue (Formato Actual de Film-Hub)

Todas las plantillas en `.github/ISSUE_TEMPLATE/` conservarán exactamente la estructura actual de las issues existentes (`#3`, `#6`):

```markdown
## Descripción

[Resumen claro del objetivo de la tarea o Work Item, indicando el problema que resuelve o el valor que aporta dentro de Film-Hub.]

## Detalles Técnicos y Requisitos

* **Bloque / Módulo 1:**
  * Requisito técnico concreto, archivo o componente afectado.
  * Detalle de implementación o configuración esperada.
* **Bloque / Módulo 2:**
  * Restricciones de compatibilidad, seguridad o flujo EGCFlow aplicables.

## Criterios de Aceptación

* [ ] Implementación/documentación completa sin cambios ajenos mezclados.
* [ ] Commits atómicos conformes a Conventional Commits referenciando `(#<id_issue>)`.
* [ ] `rosemary linter` y `rosemary test` en verde (si aplica código) y CI Nivel 1 en verde.
* [ ] Revisión pre-merge aprobada por `@<revisor>`.
```

---

## 3. Especificación Detallada de Qué Tiene Que Hacer Cada Uno

---

### BLOQUE A — José Vicente Sánchez Montilla (`@CGD5709`, PM / Propietario del Repositorio)

#### T1 — Protección de Ramas (`main` y `trunk`) y Visibilidad Pública del Project
* **Assignee**: `@CGD5709` | **Revisor**: `@LuisLucena5` | **Labels**: `type: chore` | **Rama**: *(No requiere rama; configuración directa en GitHub UI)*
* **Título de la Issue**: `[CHORE] Proteger ramas main y trunk con Rulesets y hacer público el Project`

**Cuerpo listo para copiar en GitHub:**
```markdown
## Descripción

Configurar la protección formal de las ramas permanentes `main` y `trunk` mediante GitHub Rulesets y cambiar la visibilidad del tablero `Film-Hub EGC 2026/2027` a público para permitir la auditoría docente de los seguimientos.

## Detalles Técnicos y Requisitos

* **Visibilidad del GitHub Project:**
  * Acceder a `Film-Hub EGC 2026/2027` -> `Settings` -> `Manage access` -> `Visibility` y cambiarlo a **Public**.
* **Ruleset sobre `main` (Rama de Producción y Releases):**
  * Prohibir `force-push` (`Block force pushes`) y borrado de rama (`Restrict deletions`).
  * Exigir que los checks de CI (`CI Full`, `CI_lint`, `CI_pytest`, `CI_security`) estén en verde antes de actualizar `main`.
* **Ruleset sobre `trunk` (Rama de Integración Continua):**
  * Prohibir `force-push` y borrado de rama.
  * Exigir los checks de CI Nivel 1 (`CI_branches`, `CI_commits`, `CI_lint`, `CI_pytest`, `CI_security`) en verde.
  * Permitir que cualquiera de los 4 integrantes pueda integrar en `trunk` tras su revisión por pares (evitando cuellos de botella en una sola persona).

## Criterios de Aceptación

* [ ] El Project `Film-Hub EGC 2026/2027` es accesible públicamente sin iniciar sesión privada.
* [ ] Ruleset de `main` y Ruleset de `trunk` activos y verificados.
* [ ] Evidencia comentada en la issue y validada por `@LuisLucena5` antes de cerrar.
```

**Guía paso a paso para `@CGD5709`:**
1. En GitHub, abrir `Projects` -> `Film-Hub EGC 2026/2027` -> menú `...` -> `Settings` -> `Manage access` -> `Visibility: Public`.
2. Ir a `Settings` del repositorio `CGD5709/Film-Hub` -> `Rules` -> `Rulesets`:
   * **Ruleset 1 (`Protect main`)**: Target branch `main`. Activar `Restrict deletions`, `Block force pushes` y `Require status checks to pass` (añadir los checks tras integrarse T4 y T8).
   * **Ruleset 2 (`Protect trunk`)**: Target branch `trunk`. Activar `Restrict deletions`, `Block force pushes` y `Require status checks to pass` (`Conventional Commits`, `lint`, `pytest`, y tras T4/T8 añadir `CI_branches` y `CI_security`). **No** activar `Require a pull request before merging` porque EGCFlow prohíbe PRs internas; los 4 integrantes deben poder hacer `git push origin trunk` tras revisión por pares.
3. Comprobar en `Settings -> Collaborators` que los otros 3 miembros tienen rol `Write` (o `Maintain`).
4. Comentar en la issue las reglas activadas (o capturas), esperar validación de `@LuisLucena5` y cerrar la issue.

---

#### T2 — Guía Operativa de Issues, Tablero, Priorización y Reglas Git (Cap. 3 y 5)
* **Assignee**: `@CGD5709` | **Revisor**: `@adriaradillam` | **Labels**: `type: docs` | **Rama**: `docs/guia-issues-y-tablero`
* **Título de la Issue**: `[DOCS] Guía operativa de issues, labels, assignees, comentarios y reglas Git`

**Cuerpo listo para copiar en GitHub:**
```markdown
## Descripción

Crear un documento normativo único que especifique cómo crear, etiquetar, asignar, priorizar, describir y comentar todas las issues del proyecto, incorporando también las reglas de Git de la Práctica 2 y el Capítulo 3 de EGC.

## Detalles Técnicos y Requisitos

* **Documento `docs/guia_gestion_issues_y_tablero.md`:**
  * Uso obligatorio de las plantillas en `.github/ISSUE_TEMPLATE/` (`work_item.md`, `bug_report.md`, `docs_chore.md`).
  * Convención estricta de títulos: `[WI-<id>] ...`, `[BUG] ...`, `[DOCS] ...`, `[CI/CD] ...`, `[CHORE] ...`, `[TEST] ...`.
  * Catálogo cerrado de `labels` en minúsculas (`type: work-item`, `type: docs`, `type: ci-cd`, `type: bug`, `type: chore`, `type: test`, `difficulty: mandatory/high/medium`, `status: in-review`, `status: blocked`).
  * Criterios de priorización (Cap. 5.2.3): impacto, riesgo, urgencia y dependencias técnicas.
  * Regla de `Assignee` y cierre justificado (Cap. 5.2.3): ninguna issue activa sin responsable; si se cierra como duplicada o no reproducible, documentar justificación explícita.
  * Trazabilidad bidireccional (Cap. 5.2.5): `Issue <-> Rama <-> Commits (#id) <-> Revisión pre-merge <-> CI <-> Release (tag)`.
  * Plantillas de comentarios estructurados: inicio de trabajo, solicitud de revisión pre-merge (`git diff origin/trunk..origin/<rama>`), reporte de defectos, aprobación y cierre con hash del merge.
  * Reglas de Git (Práctica 2 y Cap. 3): identidad única (`user.name` y `user.email` consistentes), prohibición de commits desde la web de GitHub, uso de `rebase` solo en ramas privadas y uso opcional de parches (`git diff` / `git format-patch`).

## Criterios de Aceptación

* [ ] `docs/guia_gestion_issues_y_tablero.md` creado, completo y sin emojis.
* [ ] Commits conformes a Conventional Commits referenciando `(#<id_issue>)`.
* [ ] CI Nivel 1 en verde y revisión pre-merge aprobada por `@adriaradillam`.
```

**Guía paso a paso para `@CGD5709`:**
1. Crear la issue en GitHub y apuntar su número `#<id_T2>`.
2. En local: `git checkout trunk && git pull origin trunk && git checkout -b docs/guia-issues-y-tablero`.
3. Redactar `docs/guia_gestion_issues_y_tablero.md` cubriendo:
   * **Sección 1**: Tipos de issue, uso obligatorio de plantillas y enlace padre/sub-issue en épicas.
   * **Sección 2**: Catálogo exacto de etiquetas en minúsculas y criterios de prioridad (impacto, riesgo, dependencias).
   * **Sección 3**: Flujo Kanban de 5 columnas (`Pendiente -> En Progreso -> En revisión -> Hecho`, con salida lateral a `Bloqueada`), obligatoriedad de `Assignee` y cierre justificado sin cambios si hay duplicados.
   * **Sección 4**: Plantillas literales de comentarios (inicio, petición de revisión con `git diff`, rechazo por bug, aprobación y cierre con hash de `trunk`).
   * **Sección 5**: Normas de Git local (identidad única `git config`, cero commits web, `rebase` solo en rama privada nunca en `trunk`/`main`, e intercambio de parches `git format-patch` si aplica).
4. Commitear (`docs(process): add issue management, board and git workflow guide (#<id_T2>)`), subir, esperar CI Nivel 1 y pedir revisión a `@adriaradillam`.
5. Tras aprobación, integrar con `git merge --no-ff` en `trunk`, borrar rama local/remota y cerrar issue con el hash del merge.

---

#### T3 — Normalización de Issues `#1`-`#8` y Sub-issues de WIs Pendientes
* **Assignee**: `@CGD5709` | **Revisor**: `@adriaradillam` | **Labels**: `type: chore` | **Rama**: *(Gestión directa en GitHub Issues y Project)*
* **Título de la Issue**: `[CHORE] Normalizar issues #1-#8 y crear sub-issues de Work Items pendientes`

**Cuerpo listo para copiar en GitHub:**
```markdown
## Descripción

Auditar las issues ya existentes (`#1`-`#8`) para alinearlas con las plantillas, etiquetas y assignees del proyecto tras la sesión de revisión del 23/11/2026, y desglosar los Work Items pendientes en sub-issues trazables.

## Detalles Técnicos y Requisitos

* **Normalización de issues existentes (`#1` a `#8`):**
  * Verificar que todas tienen `Assignee`, `labels` en minúsculas y formato de cuerpo homogéneo (`Descripción`, `Detalles Técnicos y Requisitos`, `Criterios de Aceptación`).
  * Cerrar `#3` (`[WI-178-Core]`, merge `53530bf`) y `#6` (`[WI-188]`, merge `a2a9a31`) dejando comentario con el hash de integración en `trunk`.
* **Desglose en sub-issues de WIs grandes:**
  * Crear sub-issues para los bloques internos de `#177` (Fakenodo), `#200` (2FA/TOTP) y `#202` (Active Sessions), vinculadas a su issue padre para mejorar la trazabilidad entre commits e issues.

## Criterios de Aceptación

* [ ] Issues `#1`-`#8` normalizadas y las ya integradas en `trunk` cerradas con su hash de merge.
* [ ] Sub-issues creadas y vinculadas a `#177`, `#200` y `#202` con su `Assignee` y `Labels`.
* [ ] Revisión y verificación del tablero aprobadas por `@adriaradillam` en comentario de la issue.
```

**Guía paso a paso para `@CGD5709`:**
1. En GitHub web, revisar `#1`–`#8`: comprobar que ninguna está sin `Assignee`, corregir cualquier etiqueta en mayúsculas a minúsculas, y cerrar `#3` y `#6` si aún figuraban abiertas.
2. Abrir sub-issues bajo `#1` (`WI-fakenodo`: ej. API endpoints + almacenamiento / integración con `ZenodoService` + tests), `#8` (`WI-200 2FA`: modelo/migración + flujo TOTP/QR + tests) y la de `WI-202` (`Active Sessions`), usando ya la plantilla `work_item.md`.
3. Comentar el resumen de normalización y enlaces de las sub-issues en esta issue, esperar confirmación de `@adriaradillam` y cerrar.

---

### BLOQUE B — Luis Lucena Prieto (`@LuisLucena5`, DevOps Lead)

#### T4 — Workflows de Validación de Ramas, Commits con `(#id)` y Triggers en `trunk`
* **Assignee**: `@LuisLucena5` | **Revisor**: `@jfpaardoo` | **Labels**: `type: ci-cd` | **Rama**: `ci/workflows-branches-commits`
* **Título de la Issue**: `[CI/CD] Validar tipología de ramas y referencia (#id) en commits sobre trunk`

**Cuerpo listo para copiar en GitHub:**
```markdown
## Descripción

Añadir validación automática de nomenclatura de ramas en CI y actualizar los workflows existentes para eliminar referencias obsoletas a `develop` y exigir la vinculación de cada commit con su issue (`(#id)`).

## Detalles Técnicos y Requisitos

* **Nuevo workflow `.github/workflows/CI_branches.yml`:**
  * Ejecutado en `push`, comprueba que `github.ref_name` cumple los patrones de EGCFlow:
    * Permanentes: `main`, `trunk`.
    * Efímeras: `feature/WI-<id>-<resumen>`, `bugfix/issue-<id>-<resumen>`, `chore/<desc>`, `docs/<desc>`, `ci/<desc>`, `test/<desc>`, `hotfix/<version>-<resumen>`.
* **Actualización de `.github/workflows/CI_commits.yml`:**
  * Sustituir `origin/develop` por `origin/trunk` en la resolución del rango.
  * Exigir que todo commit no-merge termine con referencia a issue: `^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-zA-Z0-9._/-]+\))?!?: .+ \(#[0-9]+\)$`.
* **Actualización de `.github/workflows/CI_full.yml`:**
  * Cambiar la rama disparadora `develop` por `trunk` (manteniendo `main`).

## Criterios de Aceptación

* [ ] `CI_branches.yml` rechaza nombres de rama fuera de EGCFlow.
* [ ] `CI_commits.yml` exige `(#<id>)` y usa `origin/trunk`.
* [ ] `CI_full.yml` se dispara en `trunk` y `main`.
* [ ] CI Nivel 1 en verde y revisión pre-merge aprobada por `@jfpaardoo`.
```

**Guía paso a paso para `@LuisLucena5`:**
1. Crear `.github/workflows/CI_branches.yml`:
   * Disparar en `on: push` (y opcionalmente ignorar `tags` con `branches: ['**']` para que no choque con tags `v*.*.*`).
   * Regex sugerido en bash:
     ```bash
     BRANCH="${GITHUB_REF_NAME}"
     REGEX='^(main|trunk|feature/WI-[0-9]+-[a-z0-9-]+|bugfix/issue-[0-9]+-[a-z0-9-]+|(chore|docs|ci|test)/[a-z0-9-]+|hotfix/[0-9]+\.[0-9]+\.[0-9]+-[a-z0-9-]+)$'
     ```
2. En `.github/workflows/CI_commits.yml`:
   * Cambiar `origin/develop` por `origin/trunk`.
   * Actualizar `REGEX` para exigir `\(#[0-9]+\)$` al final del asunto (y comprobar que también bloquea emojis si queréis, ej. rechazando caracteres no ASCII en el asunto o verificando en bash).
3. En `.github/workflows/CI_full.yml`:
   * Cambiar `- develop` por `- trunk`.
4. Subir en `ci/workflows-branches-commits` con commits conformes (`ci(workflows): add branch validation and enforce issue refs (#<id_T4>)`), comprobar que pasan en GitHub Actions, pedir revisión a `@jfpaardoo`, hacer `merge --no-ff` en `trunk` y cerrar.

---

#### T5 — Workflow Reutilizable (`workflow_call`), SBOM con Syft (CRA) y Release Automática `v1.0.0`
* **Assignee**: `@LuisLucena5` | **Revisor**: `@jfpaardoo` | **Labels**: `type: ci-cd` | **Rama**: `ci/release-sbom-and-reusable`
* **Título de la Issue**: `[CI/CD] Workflow reutilizable, generación de SBOM con Syft y Release automática v1.0.0`

**Cuerpo listo para copiar en GitHub:**
```markdown
## Descripción

Implementar un workflow reutilizable (`workflow_call`) conforme a la Práctica 1 de EGC y automatizar la generación de Releases en GitHub al publicar tags SemVer (`v*.*.*`), incluyendo la generación de SBOM (Syft) e informe de licencias del reto CRA (*¿Podemos liberar esta aplicación?*).

## Detalles Técnicos y Requisitos

* **Workflow reutilizable (`.github/workflows/_reusable_setup.yml`):**
  * Encapsular la configuración de Python 3.13 + caché `pip` + instalación de `requirements.txt` y `rosemary` mediante `on: workflow_call` para reutilizarlo en `CI_pytest.yml` y `CI_full.yml` (sin duplicar YAML).
* **Workflow de Release y SBOM (`.github/workflows/CD_release.yml`):**
  * Disparado en `push` de tags `v*.*.*` (y `workflow_dispatch`).
  * Generar el **SBOM** del proyecto con **Syft** (`anchore/sbom-action` en formato `spdx-json`) y un informe de licencias de dependencias (`pip-licenses --format=markdown`).
  * Subir ambos ficheros como artefactos inmutables de GitHub Actions y publicarlos adjuntos a la **GitHub Release** con notas autogeneradas (`softprops/action-gh-release` o `gh release create`).
* **Publicación de Release `v1.0.0`:**
  * Tras validar `CI_full.yml` en `trunk`, hacer `git merge --ff-only trunk` en `main`, crear el tag anotado `v1.0.0` y subirlo (`git push origin main --tags`).

## Criterios de Aceptación

* [ ] Existe un workflow reutilizable con `workflow_call` usado por al menos dos workflows.
* [ ] `CD_release.yml` genera SBOM + informe de licencias y crea la Release al subir un tag `v*.*.*`.
* [ ] Regla de inmutabilidad respetada (no sobrescribir tags existentes; si hay corrección, subir `v1.0.1`).
* [ ] Tag `v1.0.0` y Release publicados en `main` con su SBOM adjunto y revisión aprobada por `@jfpaardoo`.
```

**Guía paso a paso para `@LuisLucena5`:**
1. Crear `.github/workflows/_reusable_setup.yml` con `on: workflow_call` y actualizar `CI_pytest.yml` / `CI_full.yml` para llamarlo (o usar un job reutilizable).
2. Crear `.github/workflows/CD_release.yml`:
   * Trigger: `push: tags: ['v[0-9]+.[0-9]+.[0-9]+']` y `workflow_dispatch`.
   * Permisos: `contents: write`.
   * Pasos: `actions/checkout@v5` -> `anchore/sbom-action@v0` generando `sbom.spdx.json` -> setup Python + `pip install -r requirements.txt pip-licenses` -> `pip-licenses --format=markdown --output-file=licenses.md` -> `actions/upload-artifact` -> `softprops/action-gh-release@v2` adjuntando `sbom.spdx.json` y `licenses.md` con `generate_release_notes: true`.
3. Integrar `ci/release-sbom-and-reusable` en `trunk` tras revisión de `@jfpaardoo`.
4. Cuando `trunk` tenga integradas todas las mejoras y `CI_full.yml` esté en verde:
   ```bash
   git checkout main
   git pull origin main
   git merge --ff-only trunk
   git tag -a v1.0.0 -m "release: version v1.0.0 con nucleo Film-Hub y roles admin"
   git push origin main --tags
   ```
   (A partir de aquí, cada hito futuro como `v1.1.0`, `v1.2.0` generará automáticamente su Release y SBOM).

---

#### T6 — Verificación de Entornos PRE (`trunk`) y Aprobación CD Render en PROD (`main`)
* **Assignee**: `@LuisLucena5` | **Revisor**: `@CGD5709` | **Labels**: `type: ci-cd` | **Rama**: `ci/verify-render-pre-prod`
* **Título de la Issue**: `[CI/CD] Verificar despliegue continuo en PRE (trunk) y aprobación CD Render en PROD (main)`

**Cuerpo listo para copiar en GitHub:**
```markdown
## Descripción

Comprobar el funcionamiento real de los entornos de Preproducción (enlazado a `trunk`) y Producción (enlazado a `main` mediante `CD_render.yml` con aprobación manual) tras las integraciones de `#188` y `#178-Core`.

## Detalles Técnicos y Requisitos

* **Entorno PRE (`trunk`):**
  * Verificar que Render aplica las migraciones Alembic (`a78bb2f87d2c` y `ac0193c9dea6`) sin errores y que `/admin/users` y `/filmdataset` responden correctamente.
* **Entorno PROD (`main`):**
  * Verificar que `CD_render.yml` espera aprobación manual en el entorno `production` de GitHub cuando `CI_full.yml` finaliza en `main` y dispara correctamente `RENDER_DEPLOY_HOOK_URL`.
* **Documentación:**
  * Ajustar URLs de PRE/PROD, estado de despliegue o notas operativas en `docs/entornos_despliegue_cicd.md` si hubiera algún cambio.

## Criterios de Aceptación

* [ ] Entorno PRE operativo tras las migraciones de `#188` y `#178-Core`.
* [ ] Flujo `CD_render.yml` verificado con aprobación manual en `production`.
* [ ] Evidencias documentadas en la issue y revisión aprobada por `@CGD5709`.
```

**Guía paso a paso para `@LuisLucena5`:**
1. Comprobar en Render los logs del servicio de Preproducción (`trunk`) verificando `flask db upgrade` limpio sobre `a78bb2f87d2c` y `ac0193c9dea6`.
2. Verificar manualmente en el navegador de PRE que `/filmdataset` y `/admin/users` funcionan (recordando crear/promover un admin en PRE con `rosemary user:promote` si es necesario).
3. En GitHub `Settings -> Environments -> production`, confirmar que hay revisor obligatorio configurado y `RENDER_DEPLOY_HOOK_URL` definido.
4. Tras la release `v1.0.0` en `main`, aprobar manualmente el job de `CD_render.yml` y confirmar que PROD responde en vivo. Dejar evidencias en la issue para revisión de `@CGD5709`.

---

### BLOQUE C — Juan Felipe Pardo Carrillo (`@jfpaardoo`, QA Lead)

#### T0 — Acta de Reunión (23/11/2026) y Planificación Unificada de WIs y Mejoras
* **Assignee**: `@jfpaardoo` | **Revisor**: `@CGD5709` | **Labels**: `type: docs` | **Rama**: `docs/plan-unificado-tareas`
* **Título de la Issue**: `[DOCS] Registrar acta de revisión (23/11/2026) y unificar Work Items con plan de mejoras`

**Cuerpo listo para copiar en GitHub:**
```markdown
## Descripción

Documentar la sesión de revisión en clase del 23/11/2026 y consolidar en un único documento maestro la planificación de los 6 Work Items del proyecto junto con todas las tareas de mejora metodológica, CI/CD y documentación acordadas, incluyendo responsables, revisores, ramas y textos estándar de cada issue.

## Detalles Técnicos y Requisitos

* **Acta de la reunión / sesión de revisión (`docs/diario_equipo/acta_reunion_2026_11_23.md`):**
  * Recoger las críticas recibidas en la primera sesión de revisión (plantillas de issues, visibilidad del tablero, workflows de ramas/commits, releases y trazabilidad), las conclusiones del análisis comparativo y los acuerdos tomados por el equipo.
* **Documento unificado (`docs/descomposicion_work_items.md` + `docs/plan_accion_mejoras.md`):**
  * Integrar en `docs/descomposicion_work_items.md` la tabla maestra conjunta (WIs `#177`, `#178`, `#188`, `#213`, `#200`, `#202` + tareas `T0`-`T10`) y el balance global de desarrollo y revisiones.
  * Publicar `docs/plan_accion_mejoras.md` con la especificación completa de cada tarea (`T0`-`T10`), plantillas de comentarios estructurados y procedimiento de limpieza del historial heredado del fork.

## Criterios de Aceptación

* [ ] `docs/diario_equipo/acta_reunion_2026_11_23.md` creado siguiendo el formato de actas del equipo.
* [ ] Documentación unificada sin emojis, con tildes y enlaces relativos válidos.
* [ ] Carga de desarrollo y revisiones equilibrada entre los cuatro integrantes.
* [ ] CI Nivel 1 en verde y revisión pre-merge aprobada por `@CGD5709`.
```

**Guía paso a paso para `@jfpaardoo`:**
1. Abrir la issue **T0** en GitHub y anotar su `#<id_T0>`.
2. Desde `trunk`: `git checkout -b docs/plan-unificado-tareas`.
3. Redactar `docs/diario_equipo/acta_reunion_2026_11_23.md` documentando la reunión/clase de revisión de hoy y el origen de las tareas `T0`–`T10`.
4. Añadir en `docs/descomposicion_work_items.md` una sección final con el mapa conjunto de `WIs + Mejoras T0-T10`, el balance de carga y el enlace a `plan_accion_mejoras.md`.
5. Verificar que `docs/plan_accion_mejoras.md` y el acta están limpios, sin emojis y con enlaces relativos válidos.
6. Commitear (`docs(diary): add review minutes 23-11-2026 and unified task plan (#<id_T0>)`), pasar CI Nivel 1, pedir revisión a `@CGD5709`, hacer `merge --no-ff` en `trunk` y cerrar.

---

#### T7 — Plantillas de Issues (Estructura Actual), `AGENTS.md` y Ciclo de Bugs `#188`
* **Assignee**: `@jfpaardoo` | **Revisor**: `@adriaradillam` | **Labels**: `type: docs`, `type: chore` | **Rama**: `chore/issue-templates-and-agents`
* **Título de la Issue**: `[CHORE] Plantillas de issues (Work Item, Bug, Docs/Chore), AGENTS.md y registro de bugs #188`

**Cuerpo listo para copiar en GitHub:**
```markdown
## Descripción

Crear las plantillas oficiales en `.github/ISSUE_TEMPLATE/` siguiendo la estructura actual de las issues de Film-Hub, corregir el enlace roto de `config.yml`, añadir `AGENTS.md` en la raíz del repositorio y reforzar `docs/gestion_bugs_e_incidencias.md` con el ciclo de depuración de 4 fases (Capítulo 5) y los bugs resueltos de `#188`.

## Detalles Técnicos y Requisitos

* **Plantillas en `.github/ISSUE_TEMPLATE/`:**
  * Corregir `config.yml` apuntando a `https://github.com/CGD5709/Film-Hub/blob/trunk/docs/gestion_bugs_e_incidencias.md`.
  * Crear `work_item.md`, `bug_report.md` y `docs_chore.md` respetando la estructura actual (`Descripción`, `Detalles Técnicos y Requisitos`, `Criterios de Aceptación`).
* **Archivo `AGENTS.md` en la raíz:**
  * Documentar reglas obligatorias del proyecto: EGCFlow sin PRs internas, prohibición de commits desde web, identidad Git única, regla de arreglar `trunk` inmediatamente si se rompe el build, comandos Docker/Rosemary, Conventional Commits con `(#id)`, cero emojis, uso responsable de IA con criterio humano, arquitectura `app/features/` y coordinación de migraciones Alembic.
* **Actualización de `docs/gestion_bugs_e_incidencias.md`:**
  * Incorporar el ciclo de depuración de 4 pasos del Capítulo 5 (`Reproducir -> Diagnosticar con hipótesis/git bisect -> Reparar con prueba de regresión previa y sin mezclar refactor -> Analizar lo aprendido / Prevención`).
  * Registrar `BUG-01`, `BUG-02` y `BUG-03` de `#188` con estado `Resuelto` y commits `860f7dd` y `e399a3a`.

## Criterios de Aceptación

* [ ] `.github/ISSUE_TEMPLATE/` con `config.yml` corregido y 3 plantillas operativas en formato actual.
* [ ] `AGENTS.md` creado en la raíz sin emojis.
* [ ] `docs/gestion_bugs_e_incidencias.md` ampliado con las 4 fases de depuración y `BUG-01..03` cerrados.
* [ ] CI Nivel 1 en verde y revisión pre-merge aprobada por `@adriaradillam`.
```

**Guía paso a paso para `@jfpaardoo`:**
1. Abrir la issue en GitHub y tomar su `#<id_T7>`.
2. Desde `trunk`: `git checkout -b chore/issue-templates-and-agents`.
3. Corregir `.github/ISSUE_TEMPLATE/config.yml` y crear `.github/ISSUE_TEMPLATE/work_item.md`, `bug_report.md` y `docs_chore.md`.
4. Crear `AGENTS.md` en la raíz incluyendo explícitamente:
   * Prohibición de PRs internas y de commits desde GitHub web.
   * Identidad única Git + regla del `rebase` solo en rama privada.
   * Regla de prioridad absoluta al build roto en `trunk` (Cap. 2.1.7).
   * Uso responsable de IA (cero emojis, cambios pequeños y revisables, verificación humana).
   * Comandos Docker/Rosemary y coordinación de migraciones Alembic.
5. Actualizar `docs/gestion_bugs_e_incidencias.md` añadiendo la sección del ciclo de 4 pasos (Reproducir -> Diagnosticar -> Reparar con test de regresión -> Prevención) y las 3 filas `BUG-01..03` de `#188`.
6. Pasar linters/tests, commitear con `(#<id_T7>)`, pedir revisión a `@adriaradillam`, hacer `merge --no-ff` a `trunk` y cerrar.

---

#### T8 — Workflow de Seguridad (`CI_security.yml`: Gitleaks + `pip-audit`) y Cobertura
* **Assignee**: `@jfpaardoo` | **Revisor**: `@LuisLucena5` | **Labels**: `type: ci-cd` | **Rama**: `ci/security-gitleaks-and-audit`
* **Título de la Issue**: `[CI/CD] Añadir workflow de seguridad (Gitleaks y pip-audit) y revisar cobertura en CI`

**Cuerpo listo para copiar en GitHub:**
```markdown
## Descripción

Incorporar comprobaciones automatizadas de seguridad en GitHub Actions para detectar fugas de secretos/credenciales y vulnerabilidades conocidas en dependencias Python, y auditar el umbral mínimo de cobertura en `CI_pytest.yml`.

## Detalles Técnicos y Requisitos

* **Nuevo workflow `.github/workflows/CI_security.yml`:**
  * Ejecutado en `push`, lanzar **Gitleaks** (`gitleaks/gitleaks-action` o CLI en el historial reciente) para detectar tokens, claves API o ficheros `.env` versionados por error.
  * Ejecutar **`pip-audit`** sobre `requirements.txt` para detectar dependencias con vulnerabilidades conocidas.
* **Auditoría de cobertura en `.github/workflows/CI_pytest.yml`:**
  * Medir el porcentaje real de cobertura en `trunk` tras `#188` y `#178-Core` y subir el umbral `--cov-fail-under` de `70` a `75` o `80` si las pruebas actuales lo superan con margen.

## Criterios de Aceptación

* [ ] `CI_security.yml` ejecutándose en verde sobre la rama.
* [ ] Umbral de cobertura medido y ajustado/justificado en `CI_pytest.yml`.
* [ ] CI Nivel 1 en verde y revisión pre-merge aprobada por `@LuisLucena5`.
```

**Guía paso a paso para `@jfpaardoo`:**
1. Abrir la issue y anotar `#<id_T8>`.
2. Desde `trunk`: `git checkout -b ci/security-gitleaks-and-audit`.
3. Crear `.github/workflows/CI_security.yml` con dos jobs (`secrets-scan` con Gitleaks sobre `fetch-depth: 0` o commits del equipo, y `dependency-audit` con `pip install pip-audit && pip-audit -r requirements.txt`).
4. Revisar el porcentaje de cobertura devuelto por `pytest -m "not e2e" --cov=app --cov-report=term-missing` en Docker y ajustar `--cov-fail-under` en `.github/workflows/CI_pytest.yml`.
5. Subir con commit `ci(security): add gitleaks and pip-audit workflow (#<id_T8>)`, pedir revisión a `@LuisLucena5`, integrar con `--no-ff` en `trunk` y cerrar.

---

### BLOQUE D — Adrián Muñoz Aradilla (`@adriaradillam`, Frontend Lead / Docs & Pruebas)

#### T9 — Alineación Documental (`Metodologia_CI-CD.md` y `docs/README.md`)
* **Assignee**: `@adriaradillam` | **Revisor**: `@CGD5709` | **Labels**: `type: docs` | **Rama**: `docs/align-cicd-and-readme`
* **Título de la Issue**: `[DOCS] Alinear Metodologia_CI-CD.md a trunk/releases/SBOM y actualizar docs/README.md`

**Cuerpo listo para copiar en GitHub:**
```markdown
## Descripción

Eliminar las referencias obsoletas a `develop` y a la ausencia de releases en `docs/Metodologia_CI-CD.md`, incorporar los criterios de diseño de pruebas del Capítulo 4 del temario y actualizar el índice maestro `docs/README.md`.

## Detalles Técnicos y Requisitos

* **Actualización de `docs/Metodologia_CI-CD.md`:**
  * Sustituir todas las menciones residuales a `develop` por `trunk`.
  * Reflejar en la tabla de pipelines los nuevos workflows (`CI_branches.yml`, `CI_security.yml`, `_reusable_setup.yml`, `CD_release.yml` con SBOM y licencias).
  * Actualizar la sección de Entrega Continua incorporando la política de Releases SemVer (`v1.0.0`, `v1.1.0`, ...), artefactos inmutables y la regla de reparación inmediata de build roto en `trunk` (Cap. 2.1.7 y 2.2).
  * Añadir en la sección de Pruebas los criterios de diseño de casos del Capítulo 4: pirámide de pruebas, particiones equivalentes, valores límite, cobertura CRUD y advertencia sobre falsa sensación de seguridad de `--cov-fail-under` (importancia de buenos oráculos).
* **Actualización de `docs/README.md`:**
  * Enlazar `guia_gestion_issues_y_tablero.md`, `plan_accion_mejoras.md`, `docs/adrs/` y `../AGENTS.md`.
  * Verificar que todos los enlaces relativos dentro de `docs/` apuntan a ficheros reales y sin emojis.

## Criterios de Aceptación

* [ ] Cero referencias obsoletas a `develop` en `docs/Metodologia_CI-CD.md`.
* [ ] Releases SemVer, SBOM y criterios de diseño de pruebas del Cap. 4 documentados.
* [ ] `docs/README.md` actualizado con enlaces válidos y sin emojis.
* [ ] CI Nivel 1 en verde y revisión pre-merge aprobada por `@CGD5709`.
```

**Guía paso a paso para `@adriaradillam`:**
1. Abrir la issue y anotar `#<id_T9>`.
2. Desde `trunk` (una vez T2 y T7 estén integradas para que existan los archivos enlazados): `git checkout -b docs/align-cicd-and-readme`.
3. Editar `docs/Metodologia_CI-CD.md` cambiando `develop` -> `trunk`, añadiendo los workflows nuevos, corrigiendo el párrafo de releases/artefactos inmutables y añadiendo el subapartado de criterios de diseño de pruebas (particiones equivalentes, valores límite, CRUD, oráculos).
4. Editar `docs/README.md` para enlazar `guia_gestion_issues_y_tablero.md`, `plan_accion_mejoras.md`, `adrs/` y `../AGENTS.md`.
5. Subir con `docs(ci): align CI/CD methodology with trunk, releases and test design (#<id_T9>)`, pedir revisión a `@CGD5709`, hacer `merge --no-ff` a `trunk` y cerrar.

---

#### T10 — Validación de DevContainer (Práctica 4) y Pruebas de Carga Locust Pre-Release (Práctica 3)
* **Assignee**: `@adriaradillam` | **Revisor**: `@jfpaardoo` | **Labels**: `type: test`, `type: chore` | **Rama**: `chore/verify-devcontainer-and-locust`
* **Título de la Issue**: `[TEST] Validar DevContainer (Práctica 4) y ejecutar pruebas de carga Locust pre-release v1.0.0`

**Cuerpo listo para copiar en GitHub:**
```markdown
## Descripción

Validar el entorno aislado mediante DevContainer (Práctica 4 de EGC) y ejecutar las pruebas de carga con Locust (`rosemary locust`, Práctica 3) sobre las rutas principales antes de publicar la release `v1.0.0`.

## Detalles Técnicos y Requisitos

* **Validación de DevContainer (`.devcontainer/devcontainer.json`):**
  * Comprobar que el contenedor arranca correctamente en VS Code con Python 3.13 y MariaDB, y permite ejecutar `rosemary linter` y `rosemary test` sin configuración manual adicional.
  * Si hay algún ajuste menor necesario en `.devcontainer/`, documentarlo o corregirlo de forma limpia.
* **Pruebas de carga con Locust:**
  * Ejecutar `rosemary locust` en entorno Docker local (por ejemplo sobre `dataset` y `public`, y revisar si `app/features/filmdataset/tests/locustfile.py` está operativo).
  * Recoger resumen de métricas (usuarios simulados, RPS, latencia media/p95, tasa de fallos) como comentario de evidencia en la issue y referenciarlo en `docs/entornos_despliegue_cicd.md` si procede.

## Criterios de Aceptación

* [ ] DevContainer verificado y funcionando con Python 3.13 y MariaDB.
* [ ] Prueba de carga con `rosemary locust` ejecutada con evidencias adjuntas en la issue.
* [ ] CI Nivel 1 en verde y revisión pre-merge aprobada por `@jfpaardoo`.
```

**Guía paso a paso para `@adriaradillam`:**
1. Abrir la issue y anotar `#<id_T10>`.
2. Desde `trunk`: `git checkout -b chore/verify-devcontainer-and-locust`.
3. Probar la apertura del proyecto en DevContainer (VS Code `Reopen in Container`) y ejecutar `rosemary linter` y `rosemary test` dentro.
4. Levantar Docker Compose dev y ejecutar una prueba breve con `rosemary locust` (ej. `rosemary locust public` o `dataset`), capturando métricas de RPS y fallos.
5. Si no hubo que tocar código (o tras pequeños ajustes en `.devcontainer/` / `locustfile.py`), adjuntar las evidencias en un comentario de la issue, solicitar revisión a `@jfpaardoo`, integrar si hay cambios en `trunk` y cerrar la issue.

---

## 4. Plantillas de Comentarios Estructurados para Todas las Issues

Para mantener la trazabilidad exigida en el Capítulo 5 de EGC sin burocracia, usar estos formatos exactos (sin emojis):

### 4.1. Al solicitar revisión pre-merge (`En Progreso -> En revisión`)
```markdown
Implementación finalizada en la rama `<nombre-rama>`.

Cambios realizados:
- `<archivo_1>`: resumen breve del cambio.
- `<archivo_2>`: resumen breve del cambio.

Validaciones locales y CI Nivel 1:
- `rosemary linter` / `flake8` / `black` / `isort`: OK
- `rosemary test`: X passed (sin regresiones)
- Workflows de CI Nivel 1 en verde sobre la rama.

Para revisión de @<revisor>:
`git fetch origin && git diff origin/trunk..origin/<nombre-rama>`
```

### 4.2. Al aprobar la revisión (Revisor)
```markdown
Revisión pre-merge completada sobre `<nombre-rama>` (commit `<hash>`).

Verificado:
- Alcance y criterios de aceptación cumplidos.
- Sin cambios ajenos ni secretos expuestos.
- CI Nivel 1 en verde.

Aprobado para integración en `trunk` mediante `git merge --no-ff` y borrado de la rama efímera.
```

### 4.3. Al cerrar la issue tras integrar en `trunk` (`En revisión -> Hecho`)
```markdown
Integrado en `trunk` mediante merge `--no-ff` tras aprobación de @<revisor> y con CI en verde:

- Commit de integración en `trunk`: `<hash-del-merge>`
- Rama efímera `<nombre-rama>` eliminada en local y remoto conforme a EGCFlow.
```

---

## 5. Limpieza del Historial Heredado del Fork (Dejar Solo Commits de Film-Hub)

Si el equipo decide compactar los commits previos al fork (`EGCETSII/uvlhub`) en **un único commit raíz inicial** conservando intactos todos los commits propios de **Film-Hub** (incluidos autores, fechas y *merge commits* `--no-ff`), debe hacerse **antes** de activar el bloqueo de `force-push` en los Rulesets (**T1**) y con todas las ramas efímeras cerradas o avisando al equipo para resincronizar en local.

### Procedimiento seguro (`git replace` + `git filter-branch`)

1. **Localizar el último commit heredado de `EGCETSII/uvlhub`** (el commit inmediatamente anterior al primer commit del equipo):
   ```powershell
   git checkout trunk
   git pull origin trunk
   git --no-pager log --oneline --reverse | Select-Object -First 30
   # O filtrar por los últimos commits del fork (antes de octubre/noviembre 2026):
   git --no-pager log --oneline main~15..main
   ```
2. **Sustituir el commit base del fork por un commit raíz único** (sin tocar ningún fichero ni perder los commits posteriores de Film-Hub):
   ```powershell
   $FORK_BASE = "<HASH_ULTIMO_COMMIT_UVLHUB>"
   $NEW_ROOT = git commit-tree "$FORK_BASE^{tree}" -m "chore(init): initialize Film-Hub base from EGCETSII/uvlhub"
   git replace $FORK_BASE $NEW_ROOT
   git filter-branch --tag-name-filter cat -- --branches --tags
   git replace -d $FORK_BASE
   ```
3. **Verificar que solo quedan el commit raíz + los commits de Film-Hub** y publicar (coordinado con `@CGD5709`):
   ```powershell
   git --no-pager log --oneline --graph trunk
   git push --force origin main trunk
   ```
4. **Resincronización obligatoria para los 4 integrantes** tras el `push --force`:
   ```powershell
   git fetch origin
   git checkout trunk
   git reset --hard origin/trunk
   git checkout main
   git reset --hard origin/main
   ```
   *(Cualquier rama viva previa tendría que rebasarse con `git rebase --onto origin/trunk <ANTIGUO_BASE> <RAMA>`, por eso conviene hacerlo ahora que `feature/WI-188` y `feature/WI-178-core` ya están en `trunk`).*
