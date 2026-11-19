# Gestión de Bugs e Incidencias - Film-Hub

Este documento define el procedimiento ágil y simplificado para el reporte, seguimiento y resolución de defectos e incidencias en el proyecto **Film-Hub**.

---

## 1. Filosofía y Principio de Simplicidad

Buscamos un flujo **directo, ágil y sin burocracia innecesaria**. No se emplean formularios externos dispersos ni plantillas complejas: todo el control de incidencias se centraliza en este único documento y en la comunicación directa entre compañeros.

---

## 2. Cuándo se Reporta y Cuándo No

* **Durante el desarrollo propio (Autodetección)**:  
  Si la persona que está implementando el código encuentra un bug en su propia tarea mientras está desarrollando, **no tiene que reportarlo formalmente**. Lo corrige directamente como parte de su flujo natural de trabajo.
* **En revisión o pruebas cruzadas**:  
  Si la persona asignada como revisora encuentra un bug al revisar el código de un compañero, o si cualquier integrante descubre un fallo al probar la aplicación, al ejecutar flujos de otro módulo o en código ya finalizado, **es obligatorio reportarlo**.

---

## 3. Procedimiento de Reporte (2 Pasos)

Cuando se detecta un bug que requiere reporte, se siguen únicamente estos dos pasos:

```text
[ Detección del Bug ]
         │
         ├──► 1. Notificación Directa: Avisar al compañero autor por canal oficial (Discord / Chat).
         │
         └──► 2. Registro Inmediato: Añadir la fila correspondiente en la tabla de este archivo.
```

1. **Aviso directo por canal oficial**: Notificar inmediatamente a la persona responsable por el canal oficial del equipo (Discord / grupo de mensajería) para que esté al tanto del bloqueo o anomalía.
2. **Añadir el reporte a la tabla de este archivo**: Incorporar una nueva entrada en la [Tabla de Registro de Bugs e Incidencias](#5-tabla-de-registro-de-bugs-e-incidencias) con toda la información necesaria para diagnosticarlo y reproducirlo.

---

## 4. Responsabilidad de Resolución y Cierre

* **¿Quién lo soluciona?**: **Siempre la persona que implementó el código originalmente**. El autor original es quien mejor conoce la lógica de su módulo y quien debe aplicar la corrección en su rama.
* **Cierre y validación**: Una vez implementada la solución, la persona que detectó y reportó el bug comprueba que el fallo ya no se reproduce. Tras dicha validación, se actualiza el estado a `Resuelto` en la tabla indicando el commit de corrección.

---

## 5. Tabla de Registro de Bugs e Incidencias

A continuación se registran todos los bugs detectados por el equipo durante las revisiones o pruebas de la aplicación:

| ID | Fecha | Módulo / WI | Descripción del Bug | Pasos para Reproducir y Entorno | Detectado por | Asignado a (Autor Original) | Estado | Commit / Resolución |
| :---: | :---: | :---: | :--- | :--- | :--- | :--- | :---: | :--- |
| *EJ-01* | *DD/MM/AA* | *#178 (Core)* | *Ejemplo: Error 500 al subir CSV con cabeceras en mayúsculas.* | *1. Entorno: Docker Dev local.<br>2. Ir a /dataset/upload.<br>3. Subir archivo con cabecera TITLE en vez de title.<br>4. Lanza KeyError no capturado.* | *Juan Felipe* | *Adrián Muñoz* | *Resuelto* | *commit `fix(core): normalizar cabeceras csv (#178)`* |
| | | | | | | | | |

> **Leyenda de Estados**:
> - `Pendiente`: Notificado y registrado, a la espera de inicio de corrección.
> - `En progreso`: El autor original está trabajando en la solución en su rama de trabajo.
> - `Resuelto`: Corregido por el autor, verificado por el revisor y fusionado.

