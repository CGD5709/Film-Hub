# Plantilla de Reporte de Incidencia (Bug Report)

> Utilizar esta plantilla para notificar cualquier defecto, comportamiento no esperado o fallo funcional detectado en Film-Hub.

---

## 1. Identificacion de la Incidencia
- **Titulo**: [bug]: [Descripcion concisa del fallo observado]
- **Reportado por**: [@usuario]
- **Asignado a**: [@desarrollador_responsable]
- **Severidad**: [Critica | Mayor | Menor | Trivial]
- **Prioridad**: [P0 - Inmediata | P1 - Alta | P2 - Media | P3 - Baja]
- **Modulo o Feature Afectado**: [ej: `filmdataset`, `auth`, `fakenodo`, `sessions`, `badge`]

---

## 2. Descripcion del Fallo
[Explicar con precision el comportamiento anomalo detectado, indicando el endpoint, vista o comando involucrado.]

---

## 3. Entorno de Ejecucion
- **Sistema Operativo**: [Windows / Linux / macOS]
- **Entorno de Despliegue**: [Docker Compose Dev / Docker Compose Prod / Staging PaaS]
- **Navegador y Version**: [Chrome / Firefox / Edge + Version]
- **Identificador de Commit / Tag**: [ej: commit `a1b2c3d` o tag `v0.2.0-beta`]

---

## 4. Pasos para Reproducir el Fallo (Ejemplo Minimo Reproducible)
1. Iniciar sesion con credenciales de prueba.
2. Navegar a la ruta: `/ruta/del/fallo`.
3. Introducir o cargar los siguientes datos: `[detallar entrada]`.
4. Pulsar en el boton o invocar el endpoint: `[accion]`.

---

## 5. Comportamiento Observado vs Comportamiento Esperado

### Comportamiento Observado:
[Detallar lo que ocurre en la realidad, indicando codigos de error HTTP, bloqueo o mensaje en pantalla.]

### Comportamiento Esperado:
[Detallar lo que deberia ocurrir conforme a la especificacion funcional del sistema.]

---

## 6. Registros y Trazas de Excepcion (Stack Trace)
```text
[Insertar aqui el extracto de error obtenido desde 'docker compose logs -f web']
```

---

## 7. Archivos o Datos Adjuntos de Prueba
- [ ] Adjuntar archivo CSV minimo o carga JSON utilizada para disparar el defecto.
