---
name: "Documentación / Mantenimiento (Docs / Chore / CI-CD / Test)"
about: "Tarea de documentación, configuración, CI/CD, infraestructura o pruebas"
title: "[DOCS|CHORE|CI/CD|TEST] <descripción concisa>"
labels: ["type: chore"]
assignees: ""
---

## Descripción

[Resumen claro del objetivo de la tarea de documentación, configuración, CI/CD o mantenimiento y el valor que aporta al proyecto.]

## Detalles Técnicos y Requisitos

* **Archivos / Componentes afectados:**
  * [Listar ficheros, workflows o configuraciones a crear o modificar.]
* **Requisitos y restricciones:**
  * [Criterios metodológicos, compatibilidad con EGCFlow o dependencias con otras issues.]

## Criterios de Aceptación

* [ ] Entregable completo, sin emojis y sin cambios ajenos mezclados.
* [ ] Commits atómicos conformes a Conventional Commits referenciando `(#<id_issue>)`.
* [ ] CI Nivel 1 en verde sobre la rama (y `rosemary linter` / `rosemary test` si aplica código).
* [ ] Revisión pre-merge aprobada por `@<revisor>`.