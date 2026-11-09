# Acta de Reunion - Film-Hub

**Fecha**: 09 de noviembre de 2026  
**Horario**: 12:40 a 14:30  
**Lugar**: Aula de practicas / laboratorio ETSII (Universidad de Sevilla)  
**Convocada por**: Jose Vicente Sanchez Montilla (Project Manager)  
**Redactada por**: Juan Felipe Pardo Carrillo (Responsable de Calidad - QA)  

---

## 1. Asistencia

| Integrante | Correo Electronico | Rol Asignado | Asistencia |
| :--- | :--- | :--- | :---: |
| Jose Vicente Sanchez Montilla | jossanmon1@alum.us.es | Project Manager (PM) | Presente |
| Juan Felipe Pardo Carrillo | juaparpar@alum.us.es | Responsable de Calidad (QA) / Backend | Presente |
| Luis Lucena Prieto | luislucenap05@gmail.com / luilucpri@alum.us.es | DevOps Lead / Backend Developer | Presente |
| Adrian Munoz Aradilla | adrmunara@alum.us.es | Disenador UI/UX / Frontend Lead | Presente |

Quorum alcanzado: 100% de asistencia.

---

## 2. Orden del Dia

1. **Definicion de CI/CD**: Flujos a implementar en GitHub Actions, hooks de validacion, herramientas de analisis estatico de codigo (linters) y pruebas automatizadas a ejecutar.
2. **Entornos de Despliegue**: Cadena de entornos (Desarrollo, Preproduccion/Staging y Produccion), gestion de variables de configuracion y estrategia de artefactos inmutables.
3. **Gestion de Incidencias y Depuracion**: Procedimiento formal para reporte, clasificacion por severidad y resolucion metodica de bugs segun el ciclo TDD.
4. **Descomposicion y Reparto de Work Items**: Division en tareas tecnicas atomicas de los 6 WIs asignados al equipo de 4 integrantes (#177, #178, #188, #213, #200 y #202).

---

## 3. Puntos Tratados y Debate

- **Integracion y Entrega Continua (CI/CD)**:
  - Se analizan los flujos heredados de uvlhub y se acuerda su adaptacion para la rama `trunk`.
  - Se establece que la comprobacion de sintaxis Conventional Commits y los linters (`flake8`, `black`, `isort`) seran obligatorios en toda Pull Request.
  - Para la suite de `pytest`, se acuerda la ejecucion automatica contra una base de datos MariaDB 12 aislada en contenedor de servicio, excluyendo temporalmente las pruebas de Selenium en la validacion rapida de CI para optimizar tiempos de ejecucion.
- **Estrategia de Despliegue**:
  - Se debate el uso de Render / PaaS frente a servidores propios, acordando una separacion clara entre el entorno de integracion (Staging) y el entorno de Produccion final.
  - Produccion solo recibira imagenes inmutables etiquetadas en Docker Hub procedentes de releases en `main`.
- **Gestion de Defectos**:
  - Se acuerda adoptar de forma vinculante la metodologia en 4 fases explicada en la asignatura: Reproducir (caso minimo), Diagnosticar (hipotesis y logs), Reparar (prueba en rojo antes de tocar codigo) y Analizar lo aprendido (post-mortem y regresion).
- **Asignacion de Tareas**:
  - Se revisa la compatibilidad entre los Work Items elegidos para asegurar que no existan dependencias circulares que bloqueen el trabajo paralelo de los 4 miembros.

---

## 4. Decisiones Tecnicas y de Proyecto

### Decision 1: Adopcion vinculante del modelo de ramas EGCFlow
- **Descripcion**: Se definen dos ramas permanentes: `main` (exclusiva para entregas etiquetadas) y `trunk` (linea de integracion continua activa). Todo el desarrollo se realiza en ramas de tarea (`feature/WI-<id>-<resumen>`, `bugfix/issue-<id>-<resumen>`, `chore/<resumen>`), quedando prohibidos los commits directos a las ramas permanentes.
- **Motivo**: Garantizar la estabilidad de las versiones entregables y proporcionar la trazabilidad bidireccional exigida en las revisiones docentes de EGC.

### Decision 2: Cadena de tres entornos de despliegue con artefactos inmutables
- **Descripcion**: Se formaliza la transicion Desarrollo (Docker local) -> Preproduccion / Staging (despliegue desatendido tras merge a `trunk`) -> Produccion (despliegue por webhook a partir de la imagen publicada en Docker Hub con tag SemVer tras release en `main`).
- **Motivo**: Aislar las pruebas funcionales complejas de los usuarios finales y asegurar un procedimiento de rollback inmediato en produccion en menos de dos minutos.

### Decision 3: Desacoplamiento modular del dominio Film-Hub mediante Rosemary
- **Descripcion**: El soporte para datasets de peliculas en formato CSV (basado en el benchmark de TMDB) se desarrollara dentro de un nuevo feature modular denominado `filmdataset`, generado con `rosemary feature:create filmdataset`.
- **Motivo**: Resolver el WI-newdataset (#178) sin alterar ni romper la retrocompatibilidad con los modelos UVL preexistentes en la plataforma base.

### Decision 4: Asignacion individualizada de Work Items segun perfiles tecnicos
- **Descripcion**: Se ratifica el reparto de responsabilidades tecnicas:
  - WI #177 (Mandatory - Fakenodo): Luis Lucena Prieto (apoyo PM).
  - WI #178 (Mandatory - Film-Hub CSV): Juan Felipe Pardo Carrillo y Adrian Munoz Aradilla.
  - WI #188 (Medium - Admin roles): Jose Vicente Sanchez Montilla.
  - WI #213 (Medium - Embeddable badge): Adrian Munoz Aradilla.
  - WI #200 (High - 2FA / TOTP): Juan Felipe Pardo Carrillo.
  - WI #202 (High - Active session management): Luis Lucena Prieto.
- **Motivo**: Cumplir estrictamente con la normativa de dimensionamiento para equipos de 4 personas (2 comunes, 2 High, 2 Medium) alineando las tareas con las fortalezas del test SuperPOP.

---

## 5. Compromisos y Plan de Accion para el Seguimiento 2 (23/11/2026)

| Tarea / Entregable | Responsable | Fecha Limite | Estado |
| :--- | :--- | :---: | :---: |
| Estructuracion de la documentacion tecnica y plantillas en `docs/` | Juan Felipe Pardo Carrillo | 10/11/2026 | En progreso |
| Ajuste de flujos CI en GitHub Actions para escuchar en `trunk` | Luis Lucena Prieto | 12/11/2026 | Pendiente |
| Especificacion de contratos OpenAPI para el servicio Fakenodo (#177) | Luis Lucena Prieto | 15/11/2026 | Pendiente |
| Creacion del feature `filmdataset` y validador sintactico CSV (#178) | Juan Felipe Pardo Carrillo | 16/11/2026 | Pendiente |
| Diseno de componentes visuales y mockup de insignias SVG (#213) | Adrian Munoz Aradilla | 16/11/2026 | Pendiente |
| Modelo de datos para roles y configuracion del tablero de proyecto (#188) | Jose Vicente Sanchez Montilla | 16/11/2026 | Pendiente |

---

## 6. Proxima Convocatoria

- **Fecha**: Martes, 17 de noviembre de 2026  
- **Horario**: 18:00 a 18:45  
- **Canal**: Discord (Canal de Voz del Equipo Film-Hub)
