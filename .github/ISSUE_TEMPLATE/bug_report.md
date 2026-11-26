---
name: "Reporte de Incidencia (Bug)"
about: "Notificación de defecto, fallo funcional o regresión detectada"
title: "[BUG] <descripción concisa del fallo>"
labels: ["type: bug"]
assignees: ""
---

## Descripción

[Resumen breve y específico del fallo observado, indicando el módulo o Work Item afectado y el contexto en el que aparece.]

## Detalles Técnicos y Requisitos

* **Pasos para reproducir (ejemplo mínimo reproducible):**
  1. [Paso 1]
  2. [Paso 2]
  3. [Paso 3]
* **Comportamiento esperado:**
  * [Qué debería ocurrir según la especificación.]
* **Comportamiento observado:**
  * [Qué ocurre realmente (código HTTP, error o comportamiento anómalo).]
* **Entorno:**
  * Entorno: [Docker Compose Dev / Preproducción Render / Producción Render]
  * Commit o versión: `[hash o tag]`
  * Navegador / SO (si aplica): `[navegador y versión]`
* **Logs, trazas o capturas:**
  ```text
  [Pegar aquí la traza o mensaje de error relevante]
  ```

## Criterios de Aceptación

* [ ] Fallo reproducido y cubierto por una prueba de regresión que falla antes de la corrección.
* [ ] Causa raíz corregida sin mezclar refactorizaciones ajenas en el mismo commit.
* [ ] `rosemary linter`, `rosemary test` y CI Nivel 1 en verde.
* [ ] Commits atómicos conformes a Conventional Commits referenciando `(#<id_issue>)`.
* [ ] Revisión pre-merge aprobada por `@<revisor>` y entrada actualizada en `docs/gestion_bugs_e_incidencias.md`.