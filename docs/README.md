# Film-Hub - Documentación Técnica y Gestión de Configuración

Repositorio documental del proyecto **Film-Hub**, desarrollado para la asignatura **Evolución y Gestión de la Configuración (EGC 2026/2027)** en la Escuela Técnica Superior de Ingeniería Informática (ETSII) de la Universidad de Sevilla.

Film-Hub constituye la adaptación de la plataforma base UVLHub a la gestión, indexación, validación y exploración de conjuntos de datos cinematográficos bajo principios de Ciencia Abierta.

---

## Estructura de la Documentación

La carpeta `docs/` organiza los procedimientos, especificaciones y registros que rigen el ciclo de vida del proyecto:

### 1. Guías Técnicas y Procedimientos Operativos
- **[Política de Ramas y Flujo de Trabajo (EGCFlow)](politica_ramas_y_flujo_trabajo.md)**: Modelo de ramas (`main` y `trunk`), integración con Git CLI en terminal (prohibición de PRs internas), estándar Conventional Commits y uso exclusivo de PRs para colaboraciones inter-grupos.
- **[Entornos de Despliegue y Estrategia CI/CD](entornos_despliegue_cicd.md)**: Especificación de entornos (Desarrollo, Preproducción/Staging y Producción), flujos en GitHub Actions, registro de imágenes inmutables en Docker Hub y planes de Rollback/Rollforward.
- **[Descomposición de Work Items](descomposicion_work_items.md)**: Estructura de descomposición de los 6 Work Items asignados al equipo de 4 integrantes (#177, #178, #188, #213, #200, #202), criterios de aceptación y asignación de pares.
- **[Gestión de Bugs e Incidencias](gestion_bugs_e_incidencias.md)**: Procedimiento ágil y simplificado para el reporte y resolución de bugs mediante revisión de pares, comunicación directa y registro tabular centralizado.
- **[Registro y Toma de Decisiones](toma_de_decisiones.md)**: Marco de gobernanza del equipo con requisito de acuerdo unánime (4 de 4) y tabla viva de registro de decisiones tomadas durante el proyecto.

### 2. Diario de Equipo y Actas (`docs/diario_equipo/`)
- **[Acta Fundacional del Equipo](diario_equipo/acta_fundacional.md)**: Documento de constitución del equipo con asignación de perfiles y Work Items.
- **[Acta de Reunión - 09/11/2026](diario_equipo/acta_reunion_2026_11_09.md)**: Acta de la sesión inicial de planificación, CI/CD y reparto documental.
- **[Acta de Reunión - 17/11/2026](diario_equipo/acta_reunion_2026_11_17.md)**: Acta de la sesión de reparto de Work Items y definición de metodología.

### 3. Plantillas Operativas (`docs/plantillas/`)
- **[Plantilla de Decisión Arquitectónica (ADR)](plantillas/plantilla_decision_tecnica_ADR.md)**: Modelo para justificar y documentar decisiones técnicas y de diseño relevantes.

---

## Integrantes del Equipo

| Nombre | UVUS | Correo Institucional US | GitHub | Rol Asignado |
| :--- | :---: | :---: | :---: | :--- |
| José Vicente Sánchez Montilla | CGD5709 | jossanmon1@alum.us.es | @CGD5709 | Project Manager (PM) |
| Luis Lucena Prieto | RRH9770 | luilucpri@alum.us.es | @LuisLucena5 | DevOps Lead / Backend |
| Juan Felipe Pardo Carrillo | HHX3170 | juaparpar@alum.us.es | @jfpaardoo | Quality Assurance (QA) / Backend |
| Adrián Muñoz Aradilla | QYQ5444 | adrmunara@alum.us.es | @adriaradillam | Frontend Lead / UI-UX |
