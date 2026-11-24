# Descomposición Técnica de Work Items y Gestión de Dependencias

Este documento recoge la asignación autónoma, el desglose técnico y el mapa mínimo de dependencias de los **6 Work Items (WIs)** de **Film-Hub**, conforme a la normativa de **EGC (2026/2027)** para equipos de 4 integrantes.

---

## Principios de Simplificación y Autonomía

1. **Propiedad Individual para Decisiones Autónomas**: En lugar de fragmentar cada issue entre las 4 personas, los WIs autocontenidos (**#177, #188, #213, #200, #202**) se asignan de forma **individual de principio a fin** (modelo, lógica, vista y tests). El responsable toma las decisiones técnicas de su módulo con total autonomía y trabaja en una única rama `feature/WI-<id>-<resumen>`.
2. **Colaboración Concentrada en el Núcleo Común (#178)**: Solo el WI central de transformación de plataforma (**WI-newdataset: Film-Hub**) se divide en bloques independientes (Backend/Validador, Frontend/UI y Filtros/Seeders).
3. **Dependencias Reducidas al Mínimo**:
   - **4 de los 6 WIs tienen 0 dependencias** entre compañeros y pueden completarse en paralelo desde el día 1.
   - Las únicas dependencias reales son el **orden de migración Alembic sobre la tabla `user`** (entre `#188` y `#200`) y la **definición inicial del modelo `FilmDataset`** en `#178`.
4. **Revisión por Pares Pre-Merge (Sin PRs Internas)**: Al estar prohibidas las Pull Requests dentro del mismo equipo en EGCFlow, cada responsable presenta su `git diff` al **Revisor Único** asignado (presencial o por Discord) antes de fusionar en local con Git CLI sobre `trunk`.

---

## Matriz de Asignación Autónoma y Dependencias

| ID Issue | Título del Work Item | Dificultad | Responsable Principal (Ejecución Completa) | Revisor Pre-Merge | Dependencias Externas |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **#177** | **WI-fakenodo**: Servicio simulador Zenodo | **Mandatory** | **Luis Lucena Prieto** | José Vicente Sánchez | **Ninguna** (servicio aislado) |
| **#178** | **WI-newdataset**: Film-Hub (CSV de Cine) | **Mandatory** | **Juan Felipe Pardo** (Core) / **Adrián Muñoz** (UI) / **José Vicente** (Filtros) | Luis Lucena / Adrián Muñoz | UI y Filtros esperan al modelo base `FilmDataset` |
| **#188** | **Admin roles** (admin, curator, user) | **Medium** | **José Vicente Sánchez Montilla** | Juan Felipe Pardo | **Ninguna** |
| **#213** | **Embeddable badge** (SVG / MD / HTML) | **Medium** | **Adrián Muñoz Aradilla** | Luis Lucena Prieto | **Ninguna** (sin cambios en BD) |
| **#200** | **Two-factor authentication** (2FA / TOTP) | **High** | **Juan Felipe Pardo Carrillo** | José Vicente Sánchez | Solo secuenciar migración en `user` tras **#188** |
| **#202** | **Active session management** | **High** | **Luis Lucena Prieto** | Juan Felipe Pardo | **Ninguna** (tabla `UserSession` propia) |

---

## Mapa Visual de Dependencias

```text
[Día 1 - En Paralelo sin Bloqueos]
  ├── #177 Fakenodo (Luis) ─────────────────────────────────► Listo (0 deps)
  ├── #202 Active Sessions (Luis) ──────────────────────────► Listo (0 deps)
  ├── #213 Embeddable Badge (Adrián) ───────────────────────► Listo (0 deps)
  ├── #188 Admin Roles (José Vicente) ──┐
  │                                     ▼ (Solo orden de migración Alembic en tabla 'user')
  │                                  #200 2FA/TOTP (Juan Felipe) ──► Listo
  └── #178 Core FilmDataset (Juan Felipe)
             │
             ├──► #178 UI Subida y Tabla (Adrián)
             └──► #178 Filtros y Seeders TMDB (José Vicente)
```

---

## 1. WI-fakenodo (#177 - Mandatory)
- **Responsable Único**: Luis Lucena Prieto | **Revisor**: José Vicente Sánchez | **Rama**: `feature/WI-177-fakenodo`
- **Dependencias**: **Ninguna**.

### Tareas (Decisiones Individuales del Responsable)

---

## 2. WI-newdataset (#178 - Mandatory - Film-Hub)
- **Coordinador**: Juan Felipe Pardo Carrillo | **Ramas**: `feature/WI-178-core`, `feature/WI-178-ui`, `feature/WI-178-filters`

### Bloques Desacoplados
| Bloque | Alcance Técnico | Responsable | Revisor | Depende de |
| :--- | :--- | :--- | :--- | :--- |
| **2.A Core y Validación** | `rosemary feature:create filmdataset`, modelo `FilmDataset`, migración Alembic, `FilmCSVValidator` (RFC 4180, `title`, `year`, `genre`), `FilmMetricsService` y tests unitarios. | **Juan Felipe Pardo** | Luis Lucena | **Ninguna** |
| **2.B Interfaz y Vistas** | Formulario de subida CSV, vista de detalle de dataset de cine y tabla paginada de previsualización de películas. | **Adrián Muñoz** | Juan Felipe Pardo | Modelo y rutas de **2.A** |
| **2.C Filtros y Seeders** | Filtros de búsqueda por género/año/rating, seeders de ejemplo basados en TMDB (`test_movies.csv`) y pruebas de integración. | **José Vicente Sánchez** | Adrián Muñoz | Modelo y métricas de **2.A** |

---

## 3. Issue #188 (Medium): Admin Roles (admin, curator, user)
- **Responsable Único**: José Vicente Sánchez Montilla | **Revisor**: Juan Felipe Pardo | **Rama**: `feature/WI-188-admin-roles`
- **Dependencias**: **Ninguna**. (Debe integrar su migración en `trunk` antes de que `#200` genere la suya sobre la tabla `user`).

### Tareas (Decisiones Individuales del Responsable)

---

## 4. Issue #213 (Medium): Embeddable Badge (SVG / Markdown / HTML)
- **Responsable Único**: Adrián Muñoz Aradilla | **Revisor**: Luis Lucena Prieto | **Rama**: `feature/WI-213-embeddable-badge`
- **Dependencias**: **Ninguna** (no modifica esquema de BD).

### Tareas (Decisiones Individuales del Responsable)

---

## 5. Issue #200 (High): Two-Factor Authentication (2FA / TOTP)
- **Responsable Único**: Juan Felipe Pardo Carrillo | **Revisor**: José Vicente Sánchez | **Rama**: `feature/WI-200-2fa-totp`
- **Dependencias**: Únicamente esperar a que **#188** integre su migración en `trunk` antes de generar la migración Alembic sobre la tabla `user` (el código y los tests unitarios pueden avanzarse sin esperar).

### Tareas (Decisiones Individuales del Responsable)

---

## 6. Issue #202 (High): Active Session Management
- **Responsable Único**: Luis Lucena Prieto | **Revisor**: Juan Felipe Pardo | **Rama**: `feature/WI-202-active-sessions`
- **Dependencias**: **Ninguna** (usa tabla `UserSession` independiente).

### Tareas (Decisiones Individuales del Responsable)

## Resumen de Carga Equitativa por Integrante

| Integrante | WIs Asignados | Dificultad Cubierta | Revisiones Pre-Merge |
| :--- | :--- | :--- | :--- |
| **Luis Lucena (DevOps)** | `#177` Fakenodo + `#202` Active Sessions | 1 Mandatory + 1 High | `#178` (Bloque Core), `#213` |
| **Juan Felipe Pardo (QA)** | `#178` Core Film-Hub + `#200` 2FA/TOTP | 1 Mandatory (Core) + 1 High | `#188`, `#202`, `#178` (Bloque UI) |
| **José Vicente Sánchez (PM)** | `#188` Admin Roles + `#178` Filtros/Seeders | 1 Medium + Apoyo Mandatory | `#177`, `#200` |
| **Adrián Muñoz (Frontend)** | `#213` Embeddable Badge + `#178` UI Film-Hub | 1 Medium + UI Mandatory | `#178` (Bloque Filtros) |

---

## Planificación Unificada: Tareas de Mejora Post-Revisión (`T0`-`T10`)

Tras la sesión de revisión en clase del `23/11/2026` (véase el [Acta de Reunión](diario_equipo/acta_reunion_2026_11_23.md)), el equipo incorpora 11 tareas atómicas de proceso, CI/CD, seguridad, pruebas y documentación cuya especificación completa (cuerpos de issue, pasos técnicos y plantillas de comentarios) figura en [Plan de Acción y Reparto de Mejoras](plan_accion_mejoras.md).

| ID | Título Resumido | Responsable (`Assignee`) | Revisor Pre-Merge | Rama / Tipo |
| :---: | :--- | :--- | :--- | :--- |
| **T0** | Acta de revisión (23/11/2026), plan unificado de WIs y mejoras | Juan Felipe (`@jfpaardoo`) | `@CGD5709` | `docs/plan-unificado-tareas` |
| **T1** | Rulesets (`main` y `trunk`) + hacer público el Project | José Vicente (`@CGD5709`) | `@LuisLucena5` | *(Configuración GitHub UI)* |
| **T2** | Guía de issues, labels, assignees, comentarios y reglas Git | José Vicente (`@CGD5709`) | `@adriaradillam` | `docs/guia-issues-y-tablero` |
| **T3** | Normalizar issues `#1`-`#8` y desglosar sub-issues de WIs pendientes | José Vicente (`@CGD5709`) | `@adriaradillam` | *(Gestión GitHub / Tablero)* |
| **T4** | Workflows `CI_branches.yml`, `CI_commits.yml` (`#id`) y `CI_full.yml` (`trunk`) | Luis Lucena (`@LuisLucena5`) | `@jfpaardoo` | `ci/workflows-branches-commits` |
| **T5** | Workflow reutilizable (`workflow_call`), SBOM (Syft/licencias) y Release `v1.0.0` | Luis Lucena (`@LuisLucena5`) | `@jfpaardoo` | `ci/release-sbom-and-reusable` |
| **T6** | Verificar despliegue PRE (`trunk`) y aprobación CD Render (`main`) | Luis Lucena (`@LuisLucena5`) | `@CGD5709` | `ci/verify-render-pre-prod` |
| **T7** | Plantillas de issues (estructura actual), `AGENTS.md` y ciclo de bugs `#188` | Juan Felipe (`@jfpaardoo`) | `@adriaradillam` | `chore/issue-templates-and-agents` |
| **T8** | Workflow de seguridad (`CI_security.yml`: Gitleaks + `pip-audit`) y cobertura | Juan Felipe (`@jfpaardoo`) | `@LuisLucena5` | `ci/security-gitleaks-and-audit` |
| **T9** | Alinear `Metodologia_CI-CD.md` (Cap. 2 y 4) y actualizar índice `docs/README.md` | Adrián Muñoz (`@adriaradillam`) | `@CGD5709` | `docs/align-cicd-and-readme` |
| **T10** | Validar DevContainer (Práctica 4) y pruebas Locust pre-release `v1.0.0` | Adrián Muñoz (`@adriaradillam`) | `@jfpaardoo` | `chore/verify-devcontainer-and-locust` |

### Balance Global Unificado (WIs + Mejoras `T0`-`T10`)

| Integrante | WIs Asignados | Tareas de Mejora | Revisiones WIs | Revisiones Mejoras | Total Revisiones |
| :--- | :--- | :---: | :--- | :---: | :---: |
| **José Vicente (`@CGD5709`)** | `#188` (Hecho), `#178` (2.C) | T1, T2, T3 | `#177`, `#200` | T0, T6, T9 | **5** |
| **Luis Lucena (`@LuisLucena5`)** | `#177`, `#202` | T4, T5, T6 | `#178` (2.A), `#213` | T1, T8 | **4** |
| **Juan Felipe (`@jfpaardoo`)** | `#178` (2.A Hecho), `#200` | T0, T7, T8 | `#188`, `#202`, `#178` (2.B) | T4, T5, T10 | **6** |
| **Adrián Muñoz (`@adriaradillam`)** | `#213`, `#178` (2.B) | T9, T10 | `#178` (2.C) | T2, T3, T7 | **4** |
