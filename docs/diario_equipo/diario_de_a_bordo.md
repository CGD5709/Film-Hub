# Diario de a Bordo y Registro de Decisiones del Equipo Film-Hub

Este documento compila de forma cronologica los hitos de seguimiento, acuerdos organizativos, actas de reuniones y decisiones tecnicas del equipo **Film-Hub** en la asignatura **Evolucion y Gestion de la Configuracion (EGC 2026/2027)**.

---

## Indice de Entradas Cronologicas

1. [Entrada 01 - 14/10/2026: Constitucion del Equipo y Perfiles SuperPOP](#entrada-01---14102026-constitucion-del-equipo-y-perfiles-superpop)
2. [Entrada 02 - 28/10/2026: Seleccion del Dominio Film-Hub y Benchmark TMDB](#entrada-02---28102026-seleccion-del-dominio-film-hub-y-benchmark-tmdb)
3. [Entrada 03 - 04/11/2026: Seleccion de Work Items para Equipo de 4 Integrantes](#entrada-03---04112026-seleccion-de-work-items-para-equipo-de-4-integrantes)
4. [Entrada 04 - 08/11/2026: Formalizacion del Plan de Gestion y Acta Fundacional](#entrada-04---08112026-formalizacion-del-plan-de-gestion-y-acta-fundacional)
5. [Entrada 05 - 09/11/2026: Sesion Presencial de Clase - Hito 1 y Planificacion CI/CD](#entrada-05---09112026-sesion-presencial-de-clase---hito-1-y-planificacion-cicd)
6. [Plantilla para Proximas Entradas](#plantilla-para-proximas-entradas)

---

## Entrada 01 - 14/10/2026: Constitucion del Equipo y Perfiles SuperPOP
- **Fecha**: 14 de octubre de 2026.
- **Asistentes**: Jose Vicente Sanchez Montilla, Luis Lucena Prieto, Juan Felipe Pardo Carrillo, Adrian Munoz Aradilla.
- **Contexto**: Sesion presencial de teoria de EGC dedicada a la constitucion de equipos.
- **Resumen**:
  - Realizacion del test SuperPOP para identificar perfiles complementarios de trabajo en equipo.
  - Asignacion inicial de roles:
    - Jose Vicente Sanchez Montilla: Project Manager (PM).
    - Luis Lucena Prieto: DevOps Lead / Backend Developer.
    - Juan Felipe Pardo Carrillo: Quality Assurance (QA) / Backend Developer.
    - Adrian Munoz Aradilla: Frontend Lead / UI-UX Designer.
  - Firma del documento fisico inicial de constitucion entregado al profesorado.

---

## Entrada 02 - 28/10/2026: Seleccion del Dominio Film-Hub y Benchmark TMDB
- **Fecha**: 28 de octubre de 2026.
- **Asistentes**: Todos los integrantes.
- **Canal**: Discord.
- **Resumen**:
  - Analisis de alternativas para el WI-newdataset (#178). Se evaluan dominios como rutas GPS (GPX), partituras musicales y grafos de procesos.
  - Se selecciona de forma consensuada el dominio **Film-Hub**: catalogacion y validacion de datasets cinematograficos tabulares en formato CSV.
  - Se adopta como benchmark de referencia el dataset publico de The Movie Database (TMDB) con mas de 930.000 peliculas para calibrar pruebas de carga y validaciones.

---

## Entrada 03 - 04/11/2026: Seleccion de Work Items para Equipo de 4 Integrantes
- **Fecha**: 04 de noviembre de 2026.
- **Asistentes**: Todos los integrantes.
- **Lugar**: Biblioteca ETSII.
- **Resumen**:
  - Aplicacion de la regla oficial de dimensionamiento para equipos de 4 personas: 2 WIs comunes obligatorios, 2 WIs de dificultad High y 2 WIs de dificultad Medium.
  - Se seleccionan issues con bajo acoplamiento mutuo para evitar bloqueos en el desarrollo paralelo:
    - Mandatory #177: WI-fakenodo (Luis Lucena con apoyo PM).
    - Mandatory #178: WI-newdataset (Juan Felipe Pardo y Adrian Munoz).
    - Medium #188: Admin roles (Jose Vicente Sanchez).
    - Medium #213: Embeddable badge (Adrian Munoz).
    - High #200: Two-factor authentication 2FA/TOTP (Juan Felipe Pardo).
    - High #202: Active session management (Luis Lucena).

---

## Entrada 04 - 08/11/2026: Formalizacion del Plan de Gestion y Acta Fundacional
- **Fecha**: 08 de noviembre de 2026.
- **Asistentes**: Todos los integrantes.
- **Resumen**:
  - Redaccion y consolidacion del documento oficial de gestion del proyecto.
  - Definicion de politicas de ramas basadas en EGCFlow, Conventional Commits y estandares de codificacion limpia.
  - Incorporacion del protocolo de prevencion de inactividad con apercibimientos formales escalados (24h, 48h, 72h).
  - Firma digital del Acta Fundacional.

---

## Entrada 05 - 09/11/2026: Sesion Presencial de Clase - Hito 1 y Planificacion CI/CD
- **Fecha**: 09 de noviembre de 2026 (12:40 a 14:30).
- **Asistentes**: Jose Vicente Sanchez Montilla, Juan Felipe Pardo Carrillo, Luis Lucena Prieto, Adrian Munoz Aradilla (100% asistencia).
- **Lugar**: Laboratorio de practicas ETSII.
- **Documento Detallado**: Consultar [Acta de Reunion del 09/11/2026](acta_reunion_2026_11_09.md).
- **Acuerdos Principales**:
  - Adopcion formal del flujo de ramas EGCFlow con `main` para releases y `trunk` para integracion activa.
  - Definicion de la cadena de entornos: Desarrollo local con Docker, Preproduccion/Staging tras merge a `trunk` y Produccion tras tag de release en `main`.
  - Protocolo de gestion de defectos siguiendo las 4 fases de EGC (Reproducir, Diagnosticar, Reparar, Analizar).
  - Descomposicion en tareas tecnicas de los 6 Work Items asignados.

---

## Plantilla para Proximas Entradas

```markdown
## Entrada XX - DD/MM/AAAA: [Titulo Descriptivo de la Sesion o Hito]
- **Fecha**: DD de Mes de AAAA (HH:MM a HH:MM).
- **Asistentes**: [Lista de miembros presentes].
- **Lugar o Canal**: [Presencial ETSII / Discord / Meet].
- **Objetivo**: [Proposito de la reunion o actividad].
- **Puntos Tratados**:
  - [Punto 1...]
  - [Punto 2...]
- **Decisiones Adoptadas**:
  - [Decision y justificacion tecnica...]
- **Compromisos y Proximos Pasos**:
  - [Tarea asignada, responsable y plazo...]
```
