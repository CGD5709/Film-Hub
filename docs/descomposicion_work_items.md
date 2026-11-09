# Descomposicion Tecnica de Work Items y Planificacion de Tareas

Este documento recoge la descomposicion tecnica, criterios de aceptacion y planificacion de los **6 Work Items (WIs)** seleccionados para el equipo de 4 integrantes de **Film-Hub**, conforme a la normativa docente oficial de **EGC (2026/2027)**.

---

## Matriz de Asignacion de Work Items

| ID Issue | Titulo del Work Item | Dificultad | Responsable Principal | Revisor Tecnico | Area de Impacto |
| :---: | :--- | :---: | :--- | :--- | :--- |
| **#177** | **WI-fakenodo**: Servicio simulador de Zenodo | **Mandatory** | Luis Lucena Prieto | Jose Vicente Sanchez | Mock API / Docker / Infraestructura |
| **#178** | **WI-newdataset**: Adaptacion a Film-Hub (CSV) | **Mandatory** | Juan Felipe Pardo Carrillo | Adrian Munoz Aradilla | Core Datasets / Validador / Rosemary |
| **#188** | **Admin roles** (admin, curator, user) | **Medium** | Jose Vicente Sanchez Montilla | Juan Felipe Pardo Carrillo | Modulo Auth / Migracion BD / Decorador |
| **#213** | **Embeddable badge** (SVG / Markdown / HTML) | **Medium** | Adrian Munoz Aradilla | Luis Lucena Prieto | Endpoints SVG / UI Component / Assets |
| **#200** | **Two-factor authentication** (2FA / TOTP) | **High** | Juan Felipe Pardo Carrillo | Jose Vicente Sanchez Montilla | Seguridad / PyOTP / QR / Login Flow |
| **#202** | **Active session management** (Auditoria/Cierre)| **High** | Luis Lucena Prieto | Adrian Munoz Aradilla | Sesiones / SQLAlchemy / Tokens / Middleware |

---

## 1. WI-fakenodo (#177 - Obligatorio Comun)

### 1.1. Descripcion y Alcance
Desarrollo de un servicio mock ligero que emula los endpoints de la API de Zenodo requeridos por la plataforma uvlhub. Su implementacion desacopla el desarrollo y la ejecucion de pruebas de la disponibilidad del sandbox de Zenodo y de credenciales reales.

### 1.2. Contrato de Endpoints a Emular
- `POST /api/deposit/depositions`: Creacion de una deposicion y retorno de identificadores de subida.
- `POST /api/deposit/depositions/{id}/files`: Recepcion y almacenamiento de ficheros asociados.
- `POST /api/deposit/depositions/{id}/actions/publish`: Publicacion formal y asignacion de identificador DOI (`10.5281/zenodo.filmhub.<id>`).
- `GET /api/deposit/depositions/{id}`: Consulta de estado y metadatos de la deposicion.
- `DELETE /api/deposit/depositions/{id}`: Eliminacion de borradores no publicados.

### 1.3. Descomposicion en Tareas Tecnicas
- [ ] Tarea 1.1: Definicion de contratos de peticion y respuesta basados en la API oficial de Zenodo.
- [ ] Tarea 1.2: Implementacion de la aplicacion ligera de servicio en Fakenodo.
- [ ] Tarea 1.3: Integracion de Fakenodo en `docker/docker-compose.dev.yml` en puerto dedicado.
- [ ] Tarea 1.4: Parametrizacion de `ZENODO_API_URL` para conmutacion transparente en `.env`.
- [ ] Tarea 1.5: Pruebas automatizadas de contrato HTTP sobre los endpoints simulados.

### 1.4. Criterios de Aceptacion
- Dado que el servicio Fakenodo esta iniciado en el entorno Docker.
- Cuando la aplicacion solicita la publicacion de un dataset validado.
- Entonces Fakenodo responde con codigo HTTP 201 y asigna un DOI simulado consistente.
- Y la deposicion queda registrada en el estado publicado.

---

## 2. WI-newdataset (#178 - Obligatorio Comun)

### 2.1. Descripcion y Alcance
Adaptacion del nucleo de la aplicacion para permitir la carga, validacion, extraccion de metricas y visualizacion de conjuntos de datos cinematograficos tabulares en formato CSV (Film-Hub).

### 2.2. Descomposicion en Tareas Tecnicas
- [ ] Tarea 2.1: Generacion del feature `filmdataset` mediante Rosemary CLI.
- [ ] Tarea 2.2: Creacion de la entidad de datos `FilmDataset` y su correspondiente migracion de base de datos.
- [ ] Tarea 2.3: Programacion del validador `FilmCSVValidator` (verificacion RFC 4180 y cabeceras obligatorias: `title`, `year`, `genre`).
- [ ] Tarea 2.4: Programacion del servicio de calculo de metricas agregadas (`total_movies`, año minimo/maximo, genero mayoritario).
- [ ] Tarea 2.5: Diseño de la vista de detalle con previsualizacion tabular paginada.
- [ ] Tarea 2.6: Suite de pruebas unitarias sobre ficheros CSV conformes, vacios y con valores fuera de rango.

### 2.3. Criterios de Aceptacion
- Dado un usuario autenticado en la plataforma.
- Cuando sube un fichero CSV valido que contiene las cabeceras requeridas.
- Entonces el sistema persiste el dataset, calcula sus metricas de dominio y muestra la tabla de previsualizacion.
- Y si el archivo presenta datos corruptos o carece de cabeceras, retorna error descriptivo HTTP 400.

---

## 3. Issue #188 (Medium): Admin Roles (admin, curator, user)

### 3.1. Descripcion y Alcance
Incorporacion de un modelo de control de acceso basado en roles jerarquicos (RBAC) con tres niveles de privilegio: `user`, `curator` y `admin`.

### 3.2. Descomposicion en Tareas Tecnicas
- [ ] Tarea 3.1: Extension del modelo de usuario con columna de rol y migracion Alembic asociada.
- [ ] Tarea 3.2: Implementacion del decorador de ruta `@role_required(*roles)` que emite HTTP 403 ante accesos no autorizados.
- [ ] Tarea 3.3: Comando de Rosemary CLI para asignacion de roles desde consola (`rosemary user:promote`).
- [ ] Tarea 3.4: Modulo y vista de administracion `/admin/users` para gestion y asignacion de privilegios.
- [ ] Tarea 3.5: Pruebas unitarias de autorizacion verificando denegacion de acceso a usuarios sin privilegios.

### 3.3. Criterios de Aceptacion
- Dado un usuario con rol `user`.
- Cuando intenta acceder a un endpoint restringido al rol `admin`.
- Entonces la solicitud es denegada con codigo de estado HTTP 403.
- Y la peticion solo prospera cuando el usuario posee el rol `admin`.

---

## 4. Issue #213 (Medium): Embeddable Badge (SVG / Markdown / HTML)

### 4.1. Descripcion y Alcance
Generacion dinamica de insignias graficas vectoriales en formato SVG con metricas actualizadas de un dataset publicado, facilitando fragmentos embebibles en Markdown y HTML.

### 4.2. Descomposicion en Tareas Tecnicas
- [ ] Tarea 4.1: Diseño de la plantilla SVG vectorial optimizada y accesible.
- [ ] Tarea 4.2: Implementacion del endpoint `GET /dataset/<id>/badge.svg` con cabeceras `image/svg+xml` y politicas de cache.
- [ ] Tarea 4.3: Soporte de parametros para metricas seleccionables (`movies`, `rating`, `downloads`).
- [ ] Tarea 4.4: Componente visual en la vista de dataset para copiar fragmentos de codigo listos para uso externo.
- [ ] Tarea 4.5: Pruebas unitarias sobre la generacion del XML/SVG y tratamiento de datasets no encontrados (HTTP 404).

### 4.3. Criterios de Aceptacion
- Dado un dataset de cine publicado con identificador valido.
- Cuando se realiza una llamada HTTP al endpoint de insignia.
- Entonces el servidor devuelve un documento SVG valido que refleja la metrica consultada.

---

## 5. Issue #200 (High): Two-Factor Authentication (2FA / TOTP)

### 5.1. Descripcion y Alcance
Mecanismo de seguridad de doble factor basado en contraseñas de un solo uso por tiempo (TOTP - RFC 6238), con soporte de generacion de secreto, visualizacion de codigo QR y codigos de recuperacion de uso unico.

### 5.2. Descomposicion en Tareas Tecnicas
- [ ] Tarea 5.1: Modificacion del modelo de usuario para albergar secreto TOTP, estado de activacion y codigos de rescate hasheados.
- [ ] Tarea 5.2: Flujo de activacion con renderizado de QR y verificacion del primer token temporal.
- [ ] Tarea 5.3: Mecanismo de emision e invalidacion de codigos de rescate de un solo uso.
- [ ] Tarea 5.4: Intercepcion del proceso de inicio de sesion para solicitar token de 6 digitos si 2FA se encuentra habilitado.
- [ ] Tarea 5.5: Procedimiento de desactivacion segura con confirmacion de contraseña actual.
- [ ] Tarea 5.6: Pruebas unitarias de verificacion de tokens temporales, desfase de reloj admisible y codigos invalidos.

### 5.3. Criterios de Aceptacion
- Dado un usuario con autenticacion 2FA activada en su cuenta.
- Cuando completa satisfactoriamente su combinacion de usuario y contraseña.
- Entonces el sistema no inicia la sesion completa hasta que el usuario proporciona un codigo TOTP valido.
- Y si el codigo TOTP o de recuperacion es correcto, se completa el acceso al sistema.

---

## 6. Issue #202 (High): Active Session Management

### 6.1. Descripcion y Alcance
Mecanismo de control, persistencia y auditoria de sesiones concurrentes de usuario a nivel de servidor, posibilitando el cierre selectivo y masivo de sesiones activas.

### 6.2. Descomposicion en Tareas Tecnicas
- [ ] Tarea 6.1: Creacion de la entidad `UserSession` para registrar identificador de sesion, IP, User-Agent, fechas de creacion y ultima actividad.
- [ ] Tarea 6.2: Middleware de actualizacion de ultima actividad con control de frecuencia de escritura.
- [ ] Tarea 6.3: Integracion con el ciclo de login y logout para alta y baja de la sesion en base de datos.
- [ ] Tarea 6.4: Panel de usuario con listado de sesiones abiertas distinguiendo la sesion en curso.
- [ ] Tarea 6.5: Endpoints de revocacion unitaria y de cierre masivo de sesiones restantes.
- [ ] Tarea 6.6: Pruebas automatizadas comprobando que una sesion revocada no permite realizar solicitudes autenticadas posteriores.

### 6.3. Criterios de Aceptacion
- Dado un usuario autenticado simultaneamente en dos navegadores diferentes.
- Cuando el usuario revoca una de las sesiones desde el panel de control.
- Entonces el token de dicha sesion queda invalidado en la base de datos.
- Y cualquier peticion posterior desde el navegador revocado es redirigida al formulario de login.
