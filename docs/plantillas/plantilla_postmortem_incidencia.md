# Plantilla de Analisis Post-Mortem de Incidencias

> Esta plantilla se cumplimenta obligatoriamente tras resolver cualquier incidencia de severidad Critica o Mayor, conforme al Capitulo 5 de EGC ("Analizar lo aprendido").

---

## 1. Identificacion del Incidente
- **Identificador de Incidencia**: Issue #[ID]
- **Titulo del Incidente**: [Descripcion sucinta del fallo]
- **Fecha de Deteccion**: DD/MM/AAAA HH:MM
- **Fecha de Resolucion**: DD/MM/AAAA HH:MM
- **Tiempo Total de Mitigacion (MTTR)**: [ej: 2 horas 15 minutos]
- **Responsable de la Depuracion**: [@usuario]
- **Severidad Asignada**: [Critica | Mayor]

---

## 2. Resumen Ejecutivo
[Breve explicacion para el equipo y el profesorado: que ocurrio, cual fue el impacto y como se soluciono de forma definitiva.]

---

## 3. Impacto Operativo y Tecnico
- **Componentes o Modulos Afectados**: [ej: `filmdataset`, `auth`, `sessions`]
- **Entorno Afectado**: [Produccion / Staging / Desarrollo Local]
- **Efecto Observable**: [ej: Errores HTTP 500 al procesar archivos CSV superiores a 10MB; bloqueo de login 2FA]

---

## 4. Cronologia de Eventos
- **HH:MM**: Deteccion inicial del fallo mediante [log / reporte manual / fallo en test].
- **HH:MM**: Comienzo de la fase de reproduccion en entorno limpio Docker.
- **HH:MM**: Diagnostico de la causa raiz confirmada.
- **HH:MM**: Creacion de la prueba automatizada de regresion en Pytest.
- **HH:MM**: Implementacion de la correccion y verificacion en verde.
- **HH:MM**: Integracion de la correccion en `trunk` y despliegue del hotfix.

---

## 5. Diagnostico de la Causa Raiz
[Explicar con rigor tecnico el defecto latente en el codigo que provoco el fallo. Distinguir con claridad entre el sintoma externo y la causa interna.]

---

## 6. Acciones de Prevencion y Lecciones Aprendidas

### 6.1. Que fallo en nuestros mecanismos de prevencion?
- Por que las pruebas unitarias existentes no detectaron el defecto con anterioridad?
- Faltaba una comprobacion estatica o una validacion de esquema en la base de datos?

### 6.2. Medidas Correctivas Adoptadas para el Futuro
- [ ] **Nueva Prueba de Regresion**: Prueba incorporada en `app/features/<feature>/tests/` para impedir reapariciones.
- [ ] **Mejora en Pipeline CI**: Inclusion de nueva comprobacion automatica si procede.
- [ ] **Actualizacion Documental**: Modificacion de especificaciones o guias de desarrollo en `docs/`.

