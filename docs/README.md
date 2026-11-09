# Film-Hub - Documentacion Tecnica y Gestion de Configuracion

Repositorio documental del proyecto **Film-Hub**, desarrollado para la asignatura **Evolucion y Gestion de la Configuracion (EGC 2026/2027)** en la Escuela Tecnica Superior de Ingenieria Informatica (ETSII) de la Universidad de Sevilla.

Film-Hub constituye la adaptacion de la plataforma base UVLHub a la gestion, indexacion, validacion y exploracion de conjuntos de datos cinematograficos bajo principios de Ciencia Abierta.

---

## Estructura de la Documentacion

La carpeta `docs/` organiza los procedimientos, especificaciones y plantillas que rigen el ciclo de vida del proyecto:

### 1. Guias Tecnicas y Procedimientos Operativos
- **[Politica de Ramas y Flujo de Trabajo (EGCFlow)](politica_ramas_y_flujo_trabajo.md)**: Modelo de ramas (`main` y `trunk`), integracion con Git CLI en terminal (prohibicion de PRs internas), estandar Conventional Commits y uso exclusivo de PRs para colaboraciones inter-grupos.
- **[Entornos de Despliegue y Estrategia CI/CD](entornos_despliegue_cicd.md)**: Especificacion de entornos (Desarrollo, Preproduccion/Staging y Produccion), flujos en GitHub Actions, registro de imagenes inmutables en Docker Hub y planes de Rollback/Rollforward.
- **[Especificacion del Dominio Film-Hub](especificacion_dominio_filmhub.md)**: Definicion formal del esquema CSV, reglas de validacion sintactica (RFC 4180) y semantica, y computo de metricas cinematograficas.
- **[Descomposicion de Work Items](descomposicion_work_items.md)**: Estructura de descomposicion de los 6 Work Items asignados al equipo de 4 integrantes (#177, #178, #188, #213, #200, #202), criterios de aceptacion y pruebas asociadas.
- **[Guia de Gestion y Depuracion de Incidencias](guia_gestion_y_depuracion_incidencias.md)**: Procedimiento metodologico en cuatro fases (Reproducir, Diagnosticar, Reparar, Analizar), clasificacion de severidad y analisis post-mortem.
- **[Regimen Interno y Resolucion de Conflictos](regimen_interno_y_gestion_conflictos.md)**: Normas de comunicacion, acuerdos de asistencia, protocolo ante inactividad o retrasos y matriz RACI.

### 2. Diario de Equipo y Actas
- **[Acta Fundacional del Equipo](diario_equipo/acta_fundacional.md)**: Documento de constitucion del equipo con asignacion de perfiles y Work Items.
- **[Diario de a Bordo](diario_equipo/diario_de_a_bordo.md)**: Registro estructurado con las entradas cronologicas y seguimiento continuo del proyecto.
- **[Acta de Reunion - 09/11/2026](diario_equipo/acta_reunion_2026_11_09.md)**: Acta oficial de la sesion presencial de clase (12:40 a 14:30).
- **[Plantilla de Acta de Reunion](diario_equipo/plantilla_reunion.md)**: Modelo estandarizado para documentar reuniones de sincronizacion.
- **[Plantilla de Decision Arquitectonica (ADR)](diario_equipo/plantilla_decision_tecnica_ADR.md)**: Modelo para justificar y registrar decisiones tecnicas relevantes.

### 3. Repositorio de Plantillas Operativas (`docs/plantillas/`)
- **[Plantilla de Work Item / Feature](plantillas/plantilla_work_item.md)**
- **[Plantilla de Reporte de Incidencia (Bug Report)](plantillas/plantilla_bug_report.md)**
- **[Plantilla de Pull Request entre Equipos](plantillas/plantilla_pull_request.md)**
- **[Plantilla de Tarea de Mantenimiento (Chore)](plantillas/plantilla_chore_task.md)**
- **[Plantilla de Analisis Post-Mortem](plantillas/plantilla_postmortem_incidencia.md)**
- **[Plantilla de Apercibimiento por Inactividad](plantillas/plantilla_compromiso_inactividad.md)**

---

## Integrantes del Equipo

| Nombre | UVUS | Correo Institucional US | GitHub | Rol Asignado |
| :--- | :---: | :---: | :---: | :--- |
| Jose Vicente Sanchez Montilla | CGD5709 | jossanmon1@alum.us.es | @CGD5709 | Project Manager (PM) |
| Luis Lucena Prieto | RRH9770 | luilucpri@alum.us.es | @LuisLucena5 | DevOps Lead / Backend |
| Juan Felipe Pardo Carrillo | HHX3170 | juaparpar@alum.us.es | @jfpaardoo | Quality Assurance (QA) / Backend |
| Adrian Munoz Aradilla | QYQ5444 | adrmunara@alum.us.es | @adriaradillam | Frontend Lead / UI-UX |
