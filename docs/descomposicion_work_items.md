# Descomposición Técnica de Work Items y Reparto Equitativo

Este documento recoge la descomposición técnica, asignación de tareas, revisores y criterios de aceptación de los **6 Work Items (WIs)** de **Film-Hub**, conforme a la normativa de **EGC (2026/2027)** para equipos de 4 integrantes.

---

## Principios de Reparto y Flujo sin Pull Requests Internas

1. **Participación Universal por Complejidad**: Todos los integrantes participan activamente en la resolución de las **2 issues obligatorias (#177, #178)**, las **2 issues Medium (#188, #213)** y las **2 issues High (#200, #202)**, ejecutando 1 tarea atómica y ejerciendo 1 revisión técnica en cada Work Item (6 tareas ejecutadas y 6 revisadas por persona).
2. **Alineación con Roles SuperPOP**:
   - **José Vicente Sánchez Montilla (PM)**: Gobernanza, contratos de API, flujos de negocio, comandos de gestión y coordinación.
   - **Luis Lucena Prieto (DevOps / Backend)**: Infraestructura Docker, middleware, modelos de sesiones, cabeceras HTTP y CLI Rosemary.
   - **Juan Felipe Pardo Carrillo (QA / Backend)**: Validadores, núcleo de seguridad TOTP, pruebas unitarias/integración y suites de regresión.
   - **Adrián Muñoz Aradilla (Frontend / UI-UX)**: Vistas Jinja2, componentes interactivos, plantillas vectoriales SVG y experiencia de usuario.
3. **Revisión por Pares Pre-Merge (Sin PRs Internas)**: Al estar prohibidas las Pull Requests dentro del mismo equipo en EGCFlow, la revisión técnica se realiza **antes del merge local a `trunk`** mediante inspección del `git diff` (presencial o por Discord) junto al revisor asignado. Tras la aprobación, el autor fusiona con Git CLI directamente sobre `trunk` y destruye su rama de tarea.

---

## Matriz General de Coordinación y Carga

| ID Issue | Título del Work Item | Dificultad | Líder / Coordinador (A) | Tareas por Miembro | Revisores Cruzados |
| :---: | :--- | :---: | :--- | :---: | :---: |
| **#177** | **WI-fakenodo**: Servicio simulador Zenodo | **Mandatory** | Luis Lucena Prieto | 1 por integrante (4) | 1 por integrante (4) |
| **#178** | **WI-newdataset**: Film-Hub (CSV de Cine) | **Mandatory** | Juan Felipe Pardo Carrillo | 1 por integrante (4) | 1 por integrante (4) |
| **#188** | **Admin roles** (admin, curator, user) | **Medium** | José Vicente Sánchez Montilla | 1 por integrante (4) | 1 por integrante (4) |
| **#213** | **Embeddable badge** (SVG / MD / HTML) | **Medium** | Adrián Muñoz Aradilla | 1 por integrante (4) | 1 por integrante (4) |
| **#200** | **Two-factor authentication** (2FA / TOTP) | **High** | Juan Felipe Pardo Carrillo | 1 por integrante (4) | 1 por integrante (4) |
| **#202** | **Active session management** | **High** | Luis Lucena Prieto | 1 por integrante (4) | 1 por integrante (4) |

---

## 1. WI-fakenodo (#177 - Mandatory)
**Líder de WI**: Luis Lucena Prieto | **Objetivo**: Emular la API REST de Zenodo para desacoplar las pruebas y el entorno local de credenciales o disponibilidad externa.

### Contrato de Endpoints
- `POST /api/deposit/depositions`
- `POST /api/deposit/depositions/{id}/files`
- `POST /api/deposit/depositions/{id}/actions/publish` (genera DOI `10.5281/zenodo.filmhub.<id>`)
- `GET /api/deposit/depositions/{id}` y `DELETE /api/deposit/depositions/{id}`

### Reparto de Tareas y Revisores
| ID | Tarea Técnica | Rama de Tarea | Responsable | Revisor Pre-Merge |
| :---: | :--- | :--- | :--- | :--- |
| **1.1** | Especificación de contratos JSON/HTTP de Zenodo y documentación de endpoints. | `feature/WI-177-api-contract` | José Vicente Sánchez | Luis Lucena |
| **1.2** | Servicio mock Fakenodo, integración en `docker-compose.dev.yml` y variable `ZENODO_API_URL` en `.env`. | `feature/WI-177-fakenodo-service` | Luis Lucena | Juan Felipe Pardo |
| **1.3** | Integración en UI de publicación mostrando el DOI simulado y estado del depósito. | `feature/WI-177-zenodo-ui-feedback` | Adrián Muñoz | José Vicente Sánchez |
| **1.4** | Suite de pruebas automatizadas de contrato HTTP sobre endpoints simulados en Pytest. | `feature/WI-177-contract-tests` | Juan Felipe Pardo | Adrián Muñoz |

### Criterios de Aceptación
- Con Fakenodo activo en Docker, al publicar un dataset validado el sistema recibe HTTP 201 y un DOI simulado persistente sin conexión a internet.

---

## 2. WI-newdataset (#178 - Mandatory - Film-Hub)
**Líder de WI**: Juan Felipe Pardo Carrillo | **Objetivo**: Adaptar el núcleo de la plataforma para gestionar, validar y visualizar datasets cinematográficos CSV desacoplados de Flamapy.

### Reparto de Tareas y Revisores
| ID | Tarea Técnica | Rama de Tarea | Responsable | Revisor Pre-Merge |
| :---: | :--- | :--- | :--- | :--- |
| **2.1** | Creación del feature `filmdataset` con Rosemary CLI, modelo `FilmDataset` y migración Alembic. | `feature/WI-178-filmdataset-model` | Luis Lucena | Juan Felipe Pardo |
| **2.2** | Validador `FilmCSVValidator` (RFC 4180, cabeceras `title`, `year`, `genre`) y `FilmMetricsService`. | `feature/WI-178-csv-validator-metrics` | Juan Felipe Pardo | José Vicente Sánchez |
| **2.3** | Vistas de subida de CSV, formulario de metadatos y tabla paginada de previsualizacion en UI. | `feature/WI-178-filmdataset-ui` | Adrián Muñoz | Luis Lucena |
| **2.4** | Filtros de exploración por genero/año/rating, seeders de ejemplo y pruebas de integración con `test_movies.csv`. | `feature/WI-178-filters-seeders` | José Vicente Sánchez | Adrián Muñoz |

### Criterios de Aceptación
- Un CSV válido se persiste con sus métricas cinematográficas y tabla de previsualizacion; un CSV corrupto o sin cabeceras requeridas devuelve HTTP 400 descriptivo.

---

## 3. Issue #188 (Medium): Admin Roles (admin, curator, user)
**Líder de WI**: José Vicente Sánchez Montilla | **Objetivo**: Implementar control de acceso basado en roles jerárquicos (RBAC).

### Reparto de Tareas y Revisores
| ID | Tarea Técnica | Rama de Tarea | Responsable | Revisor Pre-Merge |
| :---: | :--- | :--- | :--- | :--- |
| **3.1** | Enum `UserRole` en modelo `User`, migración Alembic y decorador `@role_required(*roles)` (HTTP 403). | `feature/WI-188-role-model-decorator` | José Vicente Sánchez | Juan Felipe Pardo |
| **3.2** | Comando CLI `rosemary user:promote <email> <role>` y seeders de cuentas iniciales por rol. | `feature/WI-188-rosemary-promote` | Luis Lucena | José Vicente Sánchez |
| **3.3** | Panel de administracion `/admin/users` para listado/cambio de roles y plantilla de error 403. | `feature/WI-188-admin-panel-ui` | Adrián Muñoz | Luis Lucena |
| **3.4** | Pruebas unitarias y de integración RBAC verificando permisos diferenciados para `user`, `curator` y `admin`. | `feature/WI-188-rbac-tests` | Juan Felipe Pardo | Adrián Muñoz |

### Criterios de Aceptación
- Un usuario con rol `user` recibe HTTP 403 al intentar acceder a `/admin/users`; solo un `admin` puede gestionar roles.

---

## 4. Issue #213 (Medium): Embeddable Badge (SVG / Markdown / HTML)
**Líder de WI**: Adrián Muñoz Aradilla | **Objetivo**: Generar insignias SVG dinámicas con estadísticas de datasets y snippets listos para incrustar.

### Reparto de Tareas y Revisores
| ID | Tarea Técnica | Rama de Tarea | Responsable | Revisor Pre-Merge |
| :---: | :--- | :--- | :--- | :--- |
| **4.1** | Plantilla SVG vectorial accesible y modal en vista de dataset para copiar snippets Markdown/HTML. | `feature/WI-213-badge-svg-ui` | Adrián Muñoz | José Vicente Sánchez |
| **4.2** | Endpoint `GET /dataset/<id>/badge.svg` con soporte de parametros (`movies`, `rating`, `downloads`). | `feature/WI-213-badge-endpoint` | José Vicente Sánchez | Adrián Muñoz |
| **4.3** | Configuración de cabeceras `Content-Type: image/svg+xml`, `Cache-Control` y compatibilidad Nginx. | `feature/WI-213-cache-headers` | Luis Lucena | Juan Felipe Pardo |
| **4.4** | Pruebas unitarias de generación de XML/SVG válido y respuesta controlada ante ID inexistente (HTTP 404). | `feature/WI-213-badge-tests` | Juan Felipe Pardo | Luis Lucena |

### Criterios de Aceptación
- Una peticion GET a `/dataset/<id>/badge.svg?metric=movies` retorna HTTP 200 con tipo `image/svg+xml` y la métrica actualizada.

---

## 5. Issue #200 (High): Two-Factor Authentication (2FA / TOTP)
**Líder de WI**: Juan Felipe Pardo Carrillo | **Objetivo**: Incorporar segundo factor de autenticación TOTP (RFC 6238) con QR y códigos de rescate.

### Reparto de Tareas y Revisores
| ID | Tarea Técnica | Rama de Tarea | Responsable | Revisor Pre-Merge |
| :---: | :--- | :--- | :--- | :--- |
| **5.1** | Extensión de `User` (`totp_secret`, `is_2fa_enabled`), tabla `BackupCode` hasheada y servicio TOTP (`pyotp`). | `feature/WI-200-totp-core` | Juan Felipe Pardo | Luis Lucena |
| **5.2** | Vistas de configuración 2FA con renderizado de QR (`qrcode`), verificación de 6 digitos y listado de rescate. | `feature/WI-200-2fa-ui-qr` | Adrián Muñoz | Juan Felipe Pardo |
| **5.3** | Flujo de sesión parcial en login (`/auth/2fa/verify`), consumo de códigos de rescate y desactivación con contraseña. | `feature/WI-200-login-2fa-flow` | José Vicente Sánchez | Adrián Muñoz |
| **5.4** | Gestión de dependencias en `requirements.txt`/Docker y pruebas de integración (deriva temporal y errores). | `feature/WI-200-docker-deps-tests` | Luis Lucena | José Vicente Sánchez |

### Criterios de Aceptación
- Un usuario con 2FA activo no completa la sesión tras introducir contraseña hasta validar un código TOTP o de rescate de un solo uso.

---

## 6. Issue #202 (High): Active Session Management
**Líder de WI**: Luis Lucena Prieto | **Objetivo**: Auditar y controlar sesiones activas concurrentes en servidor con cierre selectivo y masivo.

### Reparto de Tareas y Revisores
| ID | Tarea Técnica | Rama de Tarea | Responsable | Revisor Pre-Merge |
| :---: | :--- | :--- | :--- | :--- |
| **6.1** | Modelo `UserSession` (token hash, IP, User-Agent, actividad), migración y middleware con throttling. | `feature/WI-202-session-model-middleware` | Luis Lucena | Juan Felipe Pardo |
| **6.2** | Panel `/profile/sessions` listando dispositivos conectados, sesión actual y botones de revocación. | `feature/WI-202-sessions-ui` | Adrián Muñoz | Luis Lucena |
| **6.3** | Endpoints de revocación individual, cierre masivo ("revocar resto") y comando Rosemary de purga. | `feature/WI-202-revoke-endpoints` | José Vicente Sánchez | Adrián Muñoz |
| **6.4** | Pruebas automatizadas de concurrencia multi-navegador e invalidacion inmediata tras revocación. | `feature/WI-202-session-tests` | Juan Felipe Pardo | José Vicente Sánchez |

### Criterios de Aceptación
- Al revocar una sesión desde el panel de usuario, la siguiente peticion HTTP realizada desde esa sesión es rechazada y redirigida al login.

---

## Resumen de Carga Equitativa por Integrante

| Integrante | Tareas Asignadas (6) | Revisiones Asignadas (6) | WIs Coordinados |
| :--- | :--- | :--- | :--- |
| **José Vicente Sánchez (PM)** | 1.1, 2.4, 3.1, 4.2, 5.3, 6.3 | 1.3, 2.2, 3.2, 4.1, 5.4, 6.4 | #188 (Medium) |
| **Luis Lucena (DevOps)** | 1.2, 2.1, 3.2, 4.3, 5.4, 6.1 | 1.1, 2.3, 3.3, 4.4, 5.1, 6.2 | #177 (Mandatory), #202 (High) |
| **Juan Felipe Pardo (QA)** | 1.4, 2.2, 3.4, 4.4, 5.1, 6.4 | 1.2, 2.1, 3.1, 4.3, 5.2, 6.1 | #178 (Mandatory), #200 (High) |
| **Adrián Muñoz (Frontend)** | 1.3, 2.3, 3.3, 4.1, 5.2, 6.2 | 1.4, 2.4, 3.4, 4.2, 5.3, 6.3 | #213 (Medium) |
