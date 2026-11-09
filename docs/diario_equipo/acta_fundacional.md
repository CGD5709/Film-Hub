# Acta Fundacional del Equipo: Film-Hub

**Asignatura**: Evolucion y Gestion de la Configuracion (EGC)  
**Curso Academico**: 2026/2027  
**Titulacion**: Grado en Ingenieria del Software - ETSII Universidad de Sevilla  
**Fecha de Constitucion**: 14 de Octubre de 2026  
**Fecha de Entrega y Valoracion Oficial**: 09 de Noviembre de 2026  
**Version**: 1.0 (Definitiva)

---

## 1. Identificacion y Constitucion del Equipo

Reunidos los miembros abajo firmantes en la Escuela Tecnica Superior de Ingenieria Informatica de la Universidad de Sevilla, formalizan la constitucion del equipo de trabajo **Film-Hub** para el desarrollo del proyecto correspondiente a la asignatura:

| Nombre Completo | UVUS | Correo Institucional US | Usuario GitHub | Perfil SuperPOP / Rol Asignado |
| :--- | :---: | :---: | :---: | :--- |
| **Jose Vicente Sanchez Montilla** | CGD5709 | jossanmon1@alum.us.es | @CGD5709 | Project Manager (PM) |
| **Luis Lucena Prieto** | RRH9770 | luilucpri@alum.us.es | @LuisLucena5 | DevOps Lead / Backend Developer |
| **Juan Felipe Pardo Carrillo** | HHX3170 | juaparpar@alum.us.es | @jfpaardoo | Quality Assurance (QA) / Backend |
| **Adrian Munoz Aradilla** | QYQ5444 | adrmunara@alum.us.es | @adriaradillam | Frontend Lead / UI-UX |

---

## 2. Definicion del Dominio: Film-Hub

El proyecto aborda la evolucion del repositorio base [UVLHub](https://github.com/EGCETSII/uvlhub) hacia **Film-Hub**, una plataforma orientada a la catalogacion, validacion y exploracion de conjuntos de datos cinematograficos bajo principios de **Ciencia Abierta (Open Science)**.

### Caracteristicas Principales:
- **Formato del Dominio**: Archivos de texto tabular CSV conforme al estandar RFC 4180 con codificacion estricta UTF-8.
- **Conjunto de Referencia**: Dataset publico de The Movie Database (TMDB) con mas de 930.000 titulos.
- **Validacion Automatizada**: Comprobacion de estructura sintactica, cabeceras requeridas (`title`, `year`, `genre`) y consistencia de tipos.
- **Metricas Propias**: Extraccion y persistencia de indicadores de catálogo (volumen de titulos, rango de estreno, genero dominante y calificacion promedio).
- **Retrocompatibilidad**: Preservacion del soporte de modelos UVL para no romper la suite preexistente.

---

## 3. Asignacion Formal de Work Items (WIs)

De acuerdo con la normativa docente oficial para equipos de **4 integrantes** (2 WIs comunes obligatorios, 2 WIs de dificultad High y 2 WIs de dificultad Medium):

| Issue | Titulo del Work Item | Dificultad | Responsable Principal | Justificacion Tecnica |
| :---: | :--- | :---: | :--- | :--- |
| **#177** | **WI-fakenodo**: Servicio simulador Zenodo | **Mandatory** | Luis Lucena Prieto | Desacopla la aplicacion del servicio externo de Zenodo y agiliza los tests. |
| **#178** | **WI-newdataset**: Film-Hub (CSV de Cine) | **Mandatory** | Juan Felipe Pardo / Adrian Munoz | Nucleo del dominio cinematografico y desacoplamiento de Flamapy. |
| **#188** | **Admin roles** (admin, curator, user) | **Medium** | Jose Vicente Sanchez Montilla | Control de acceso basado en roles (RBAC) y panel de administracion. |
| **#213** | **Embeddable badge** (SVG / Markdown / HTML) | **Medium** | Adrian Munoz Aradilla | Insignias dinamicas vectoriales para promocion del dataset en Ciencia Abierta. |
| **#200** | **Two-factor authentication** (2FA / TOTP) | **High** | Juan Felipe Pardo Carrillo | Fortalecimiento de la seguridad mediante claves de un solo uso por tiempo. |
| **#202** | **Active session management** | **High** | Luis Lucena Prieto | Auditoria, control concurrente y revocacion de sesiones a nivel de servidor. |

---

## 4. Compromisos de Calidad y Gestion de Configuracion

El equipo asume formalmente:
1. **Flujo de Ramas**: Aplicacion rigurosa de **EGCFlow** (`main` para releases etiquetadas con SemVer; `trunk` para integracion activa; ramas `feature/*` y `bugfix/*` para tareas concretas).
2. **Sintaxis de Commits**: Cumplimiento de **Conventional Commits** con vinculacion obligatoria a issue (`tipo(ambito): descripcion (#issue)`).
3. **Integracion Continua**: Todo cambio debe superar sin advertencias los flujos de CI (`CI_commits.yml`, `CI_lint.yml` y `CI_pytest.yml`).
4. **Revision por Pares**: Ningun codigo se fusionara a `trunk` sin la aprobacion tecnica previa de al menos un companero de equipo.
5. **Entornos Aislados**: El desarrollo y las pruebas se ejecutaran de manera hermetica sobre contenedores Docker controlados con Rosemary CLI.

---

## 5. Calendario de Hitos Oficiales

- **14 de Octubre de 2026**: Formacion de equipos y determinacion de perfiles SuperPOP. *(Completado)*
- **09 de Noviembre de 2026**: Entrega y valoracion del Acta Fundacional. *(Completado)*
- **23 de Noviembre de 2026**: Seguimiento 2 - Gestion del codigo fuente, trazabilidad e incidencias.
- **30 de Noviembre de 2026**: Seguimiento 3 - Automatizacion de pruebas y flujos CI/CD.
- **14 y 16 de Diciembre de 2026**: Defensa oficial, pruebas individuales y presentacion final del producto.

---

## 6. Firmas de Conformidad

Los cuatro integrantes suscriben el presente documento en señal de conformidad:

| Nombre y Apellidos | Rol Asignado | Firma | Fecha |
| :--- | :---: | :---: | :---: |
| Jose Vicente Sanchez Montilla | Project Manager (PM) | Fdo. Jose Vicente Sanchez | 09/11/2026 |
| Luis Lucena Prieto | DevOps Lead / Backend | Fdo. Luis Lucena Prieto | 09/11/2026 |
| Juan Felipe Pardo Carrillo | QA Lead / Backend | Fdo. Juan Felipe Pardo | 09/11/2026 |
| Adrian Munoz Aradilla | Frontend Lead / UI-UX | Fdo. Adrian Munoz Aradilla | 09/11/2026 |
