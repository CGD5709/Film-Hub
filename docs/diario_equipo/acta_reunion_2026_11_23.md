# Acta de Reunión

**Fecha**: 23 de noviembre de 2026  
**Hora**: Sesión de revisión en clase y reunión posterior de equipo  

## Asistentes
- José Vicente Sánchez Montilla - josevi585@gmail.com - Project Manager
- Juan Felipe Pardo Carrillo - jfpardo05@gmail.com - Responsable de Calidad (QA)
- Luis Lucena Prieto - luislucenap05@gmail.com - Responsable de Despliegue (DevOps) y Desarrollador Backend
- Adrián Muñoz Aradilla - adrmunara@gmail.com - Diseñador UI/UX / Frontend

---

## 1. Orden del Día
- Análisis de las observaciones y críticas recibidas en la primera sesión de revisión de **Film-Hub** (EGC 2026/2027).
- Revisión comparativa frente a prácticas de otros equipos (`Classical-Hub`) y alineación con las 4 prácticas/retos del material oficial de la asignatura EGC 2026/2027.
- Definición y reparto equitativo de las tareas de mejora en issues atómicas (`T0`-`T10`).

---

## 2. ¿Qué hemos hecho desde la última reunión?
- Se ha integrado en `trunk` el Work Item **#188 (Admin roles)** (`a2a9a31`) tras revisión por pares y corrección de defectos (`BUG-01..03`).
- Se ha integrado en `trunk` el bloque **2.A (`[WI-178-Core]`)** (`53530bf`) tras aprobación pre-merge de Luis Lucena, dejando desbloqueados los bloques `2.B` (UI) y `2.C` (Explorador/Seeders) y manteniendo una única cabecera Alembic (`ac0193c9dea6`).
- Durante la sesión de revisión en clase de hoy se detectaron áreas de mejora en la gestión de issues y configuración del repositorio:
  1. Las issues abiertas no seguían una plantilla estructurada dentro de `.github/ISSUE_TEMPLATE/` (y `config.yml` tenía una URL rota).
  2. El tablero de GitHub Projects debe hacerse **público** y las ramas permanentes (`main` y `trunk`) deben contar con **Rulesets** de protección.
  3. Faltan workflows que validen automáticamente la tipología de ramas (`CI_branches.yml`), la referencia obligatoria `(#id)` en commits (`CI_commits.yml`), la seguridad (`CI_security.yml`), un workflow reutilizable (`workflow_call`) y la generación automática de **Releases SemVer + SBOM (Syft)** en `main`.
  4. Conviene incorporar `AGENTS.md`, una guía única de gestión de issues/tablero/comentarios, alinear `docs/Metodologia_CI-CD.md` con `trunk` (eliminando referencias a `develop`), verificar DevContainer + Locust pre-release y compactar el historial previo al fork para dejar únicamente los commits propios de Film-Hub.

---

## 3. ¿Qué haremos a continuación?
- **Planificación unificada y acta (T0 — Juan Felipe Pardo)**: Documentar esta sesión y consolidar la descomposición de los 6 Work Items junto con las 11 tareas de mejora (`T0`-`T10`) en `docs/descomposicion_work_items.md` y `docs/plan_accion_mejoras.md`.
- **Gobernanza en GitHub y tablero (T1, T2, T3 — José Vicente Sánchez)**: Configurar Rulesets en `main` y `trunk`, hacer público el Project, redactar `docs/guia_gestion_issues_y_tablero.md`, normalizar las issues `#1`-`#8`, crear sub-issues de WIs pendientes y coordinar la limpieza del historial heredado del fork antes de activar el bloqueo de `force-push`.
- **Automatización CI/CD y Releases (T4, T5, T6 — Luis Lucena)**: Implementar `CI_branches.yml`, exigir `(#id)` en `CI_commits.yml`, corregir `CI_full.yml` a `trunk`, añadir workflow reutilizable (`workflow_call`) + `CD_release.yml` con SBOM (Syft/licencias) y publicar la Release `v1.0.0`, además de verificar PRE y PROD en Render.
- **Calidad, plantillas y seguridad (T7, T8 — Juan Felipe Pardo)**: Crear las plantillas en `.github/ISSUE_TEMPLATE/` respetando la estructura actual, añadir `AGENTS.md`, ampliar `docs/gestion_bugs_e_incidencias.md` con el ciclo de depuración de 4 fases y `BUG-01..03`, e implementar `CI_security.yml` (Gitleaks + `pip-audit`).
- **Documentación CI/CD y validación de entornos/carga (T9, T10 — Adrián Muñoz)**: Actualizar `docs/Metodologia_CI-CD.md` y `docs/README.md`, validar el DevContainer (Práctica 4) y ejecutar pruebas de carga con `rosemary locust` (Práctica 3) antes de `v1.0.0`.

---

## 4. Conclusiones
- Todas las mejoras quedan convertidas en issues atómicas con `Assignee`, `Labels` normalizadas y **revisor pre-merge cruzado** equilibrado entre los cuatro integrantes.
- Ningún cambio entrará en `trunk` sin issue previa, commit vinculado `(#id)`, CI en verde y revisión humana por pares conforme a EGCFlow.
