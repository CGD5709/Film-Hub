---
name: "Work Item / Feature"
about: "Definición de nueva funcionalidad o sub-issue asociada a un Work Item"
title: "[WI-<id>] <título conciso>"
labels: ["type: work-item"]
assignees: ""
---

## Descripción

[Resumen claro del objetivo del Work Item o sub-issue, indicando el problema que resuelve o el valor que aporta dentro de Film-Hub.]

## Detalles Técnicos y Requisitos

* **Modelo / Persistencia (si aplica):**
  * Modelos, repositorios o migración Alembic encadenada sobre la última revisión de `trunk`.
* **Lógica / Rutas / Interfaz:**
  * Servicios, rutas Flask y vistas afectadas bajo `app/features/<feature>/`.
* **Pruebas y Restricciones:**
  * Pruebas unitarias, de repositorio/servicio e integración cubriendo particiones equivalentes y valores límite.
  * Restricciones de compatibilidad, seguridad o flujo EGCFlow aplicables.

## Criterios de Aceptación

* [ ] Implementación completa sin cambios ajenos mezclados.
* [ ] Commits atómicos conformes a Conventional Commits referenciando `(#<id_issue>)`.
* [ ] `rosemary linter` y `rosemary test` en verde, y CI Nivel 1 en verde sobre la rama.
* [ ] Revisión pre-merge aprobada por `@<revisor>`.