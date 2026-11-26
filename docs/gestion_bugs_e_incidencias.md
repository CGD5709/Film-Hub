# Gestión de Bugs e Incidencias - Film-Hub

Este documento define el procedimiento ágil y simplificado para el reporte, seguimiento, depuración y resolución de defectos e incidencias en el proyecto **Film-Hub**.

---

## 1. Filosofía y Principio de Simplicidad

Buscamos un flujo **directo, ágil y sin burocracia innecesaria**. Todo el control de incidencias se centraliza en este documento, en las issues abiertas mediante la plantilla `.github/ISSUE_TEMPLATE/bug_report.md` cuando proceda y en la comunicación directa entre compañeros.

---

## 2. Cuándo se Reporta y Cuándo No

* **Durante el desarrollo propio (Autodetección)**:
  Si la persona que está implementando el código encuentra un bug en su propia tarea mientras está desarrollando, **no tiene que reportarlo formalmente**. Lo corrige directamente como parte de su flujo natural de trabajo.
* **En revisión o pruebas cruzadas**:
  Si la persona asignada como revisora encuentra un bug al revisar el código de un compañero, o si cualquier integrante descubre un fallo al probar la aplicación, al ejecutar flujos de otro módulo o en código ya finalizado, **es obligatorio reportarlo**.

---

## 3. Procedimiento de Reporte (2 Pasos)

Cuando se detecta un bug que requiere reporte, se siguen estos dos pasos:

```text
[ Detección del Bug ]
         │
         ├──► 1. Notificación Directa: Avisar al compañero autor por canal oficial (Discord / Chat) o comentario en la issue.
         │
         └──► 2. Registro Inmediato: Añadir la fila correspondiente en la tabla de este archivo.
```

1. **Aviso directo por canal oficial**: Notificar inmediatamente a la persona responsable para que esté al tanto del bloqueo o anomalía.
2. **Añadir el reporte a la tabla de este archivo**: Incorporar una nueva entrada en la [Tabla de Registro de Bugs e Incidencias](#6-tabla-de-registro-de-bugs-e-incidencias) con toda la información necesaria para diagnosticarlo y reproducirlo.

---

## 4. Ciclo de Depuración en 4 Fases (Capítulo 5 de EGC)

Siguiendo el método sistemático de depuración (*Debug It!*, Paul Butcher), corregir una incidencia no consiste en ocultar el síntoma, sino en aplicar cuatro fases ordenadas:

```text
[ 1. Reproducir ] ──► [ 2. Diagnosticar ] ──► [ 3. Reparar ] ──► [ 4. Analizar / Prevenir ]
```

1. **Reproducir**:
   * Controlar **software** (commit o versión exacta), **entorno** (Docker/navegador/configuración) y **entradas**.
   * Reducir el fallo a un ejemplo mínimo reproducible (MRE) y determinista antes de modificar código.
2. **Diagnosticar**:
   * Aplicar el método científico (`Hipótesis -> Experimento -> Observación -> Refinar`), cambiando una sola variable cada vez.
   * Ante regresiones, utilizar `git bisect` (*diff debugging*) para localizar el commit exacto que introdujo el defecto.
   * Apoyarse en *pair debugging* si la investigación se alarga y dejar traza de lo descartado.
3. **Reparar**:
   * Construir la corrección limpiamente sobre la **causa raíz** siguiendo la secuencia:
     1. Reproducir el fallo.
     2. Escribir una **prueba de regresión** que reproduzca el defecto.
     3. Comprobar que la prueba falla por la razón esperada.
     4. Implementar la corrección mínima necesaria.
     5. Comprobar que la nueva prueba pasa.
     6. Ejecutar la suite de regresión (`rosemary test` y `rosemary linter`).
     7. Revisar el cambio antes de integrarlo.
   * **Regla de limpieza**: no mezclar la corrección del bug con refactorizaciones ajenas en el mismo commit.
4. **Analizar lo aprendido (Prevención)**:
   * Reflexionar sobre por qué no se detectó antes (falta de prueba, validación incompleta, plantilla o diseño mejorable) y consolidar una medida preventiva permanente.

---

## 5. Responsabilidad de Resolución y Cierre

* **¿Quién lo soluciona?**: **Siempre la persona que implementó el código originalmente**. El autor original es quien mejor conoce la lógica de su módulo y quien debe aplicar la corrección en su rama.
* **Cierre y validación**: Una vez implementada la solución, la persona que detectó y reportó el bug comprueba que el fallo ya no se reproduce. Tras dicha validación, se actualiza el estado a `Resuelto` en la tabla indicando el commit de corrección.

---

## 6. Tabla de Registro de Bugs e Incidencias

A continuación se registran todos los bugs detectados por el equipo durante las revisiones o pruebas de la aplicación:

| ID | Fecha | Módulo / WI | Descripción del Bug | Pasos para Reproducir y Entorno | Detectado por | Asignado a (Autor Original) | Estado | Commit / Resolución |
| :---: | :---: | :---: | :--- | :--- | :--- | :--- | :---: | :--- |
| *EJ-01* | *DD/MM/AA* | *#178 (Core)* | *Ejemplo: Error 500 al subir CSV con cabeceras en mayúsculas.* | *1. Entorno: Docker Dev local.<br>2. Ir a /dataset/upload.<br>3. Subir archivo con cabecera TITLE en vez de title.<br>4. Lanza KeyError no capturado.* | *Juan Felipe* | *Adrián Muñoz* | *Resuelto* | *commit `fix(core): normalizar cabeceras csv (#178)`* |
| **BUG-01** | 22/11/26 | #188 (auth) | Falta manejador HTTP 403 personalizado y protección CSRF (`FlaskForm`) en el formulario `POST /admin/users` de cambio de roles. | 1. Entorno: Docker Dev local.<br>2. Acceder como usuario `user` a `/admin/users` o `/zenodo/test` (mostraba 403 genérico sin plantilla).<br>3. Enviar `POST /admin/users` sin token CSRF. | Juan Felipe (`@jfpaardoo`) | José Vicente (`@CGD5709`) | Resuelto | Commit `5ed86ae` (integrado en `trunk` vía `1e971e7`). Añadido `@app.errorhandler(403)` con `403.html` y `RoleUpdateForm(FlaskForm)`. |
| **BUG-02** | 22/11/26 | #188 (auth) | Los mensajes `flash()` emitidos por `app/features/auth/routes.py` al cambiar roles o bloquear auto-degradación no se renderizaban en pantalla. | 1. Entorno: Docker Dev local.<br>2. Iniciar sesión como `admin` e ir a `/admin/users`.<br>3. Cambiar un rol o intentar auto-degradarse.<br>4. La acción se ejecutaba sin mostrar alertas en la vista. | Juan Felipe (`@jfpaardoo`) | José Vicente (`@CGD5709`) | Resuelto | Commit `5ed86ae` (integrado en `trunk` vía `1e971e7`). Añadido bloque Bootstrap `get_flashed_messages(with_categories=true)` en `admin_users.html`. |
| **BUG-03** | 22/11/26 | #188 (auth) | Doble campo `user_id` en `admin_users.html` (`form.hidden_tag()` emitía un `user_id` vacío antes del `<input>` con el ID real), haciendo fallar siempre el envío desde navegador, más posible `ValueError` con IDs no numéricos. | 1. Entorno: Docker Dev local y navegador.<br>2. Ir a `/admin/users` y pulsar actualizar rol.<br>3. El POST enviaba `user_id=&user_id=<id>` y `form.validate_on_submit()` devolvía siempre `"Invalid form submission or role"`. | Juan Felipe (`@jfpaardoo`) | José Vicente (`@CGD5709`) | Resuelto | Commit `7136c71` (integrado en `trunk` vía `1e971e7`). Cambiado a `form.hidden_tag('csrf_token')`, validación numérica en `RoleUpdateForm`, control de `ValueError` y test de regresión. |

> **Leyenda de Estados**:
> - `Pendiente`: Notificado y registrado, a la espera de inicio de corrección.
> - `En progreso`: El autor original está trabajando en la solución en su rama de trabajo.
> - `Resuelto`: Corregido por el autor, verificado por el revisor y fusionado.