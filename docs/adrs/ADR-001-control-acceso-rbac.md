# Registro de Decisión Arquitectónica (ADR)

## ADR-001: Adopción de Modelo RBAC con Roles User, Curator y Admin

- **Estado**: Aceptado
- **Fecha**: 22/11/2026
- **Autor(es)**: José Vicente Sánchez Montilla
- **Revisor(es)**: Juan Felipe Pardo Carrillo
- **Work Item(s) Asociado(s)**: #188

---

## 1. Contexto y Descripción del Problema

Inicialmente, Film-Hub gestionaba la seguridad únicamente mediante autenticación con `@login_required` de `Flask-Login`. Todos los usuarios autenticados poseían los mismos privilegios sobre la plataforma y no existía diferenciación entre un usuario ordinario, un moderador de contenidos y un administrador del sistema.

Esto planteaba dos riesgos principales:
1. Rutas críticas de infraestructura y administración (como `/zenodo/test`) quedaban abiertas a cualquier usuario con cuenta activa.
2. No existía un mecanismo arquitectónico para gobernar la validación, curación y moderación de datasets públicos de cine por parte de usuarios especializados sin otorgarles permisos totales sobre el servidor o la base de datos.

---

## 2. Factores de Decisión y Requisitos de Calidad

- **Factor 1: Principio de Mínimo Privilegio y Seguridad**: Proteger rutas administrativas devolviendo HTTP 403 Forbidden cuando el usuario autenticado no posee el rol requerido.
- **Factor 2: Mantenibilidad y Simplicidad**: Evitar sobreingeniería con esquemas de permisos hipercomplejos para un equipo de 4 personas en el marco docente de EGC.
- **Factor 3: Trazabilidad y Testabilidad**: Decoradores reutilizables declarativos (`@role_required(*roles)`, `@admin_required`) testeables de forma aislada e integrable.
- **Factor 4: Gestión de Usuarios Anónimos**: No crear un rol `guest` en base de datos; los usuarios anónimos son simplemente sesiones no autenticadas gestionadas por `current_user.is_anonymous`.

---

## 3. Alternativas Consideradas

### Alternativa 1: Control de Acceso Basado en Roles (RBAC) con Columna `role` en `User` y Decorador `@role_required`
- **Descripción**: Añadir una columna `role` (`String(20)`) en el modelo `User` con valor por defecto `'user'`, soportando los roles `'user'`, `'curator'` y `'admin'`. Controlar el acceso mediante `@role_required(*roles)`.
- **Ventajas**:
  - (+) Simplicidad máxima y mínimo coste de migración Alembic.
  - (+) Claridad en consultas y compatibilidad directa con `Flask-Login`.
  - (+) Permite proteger rutas declarativamente con `@role_required("admin")` o `@role_required("admin", "curator")`.
  - (+) Sin overhead de joins adicionales en cada petición HTTP.
- **Desventajas**:
  - (-) Cada usuario tiene asignado exactamente un rol principal en este estadio (suficiente para los requisitos de Film-Hub).

### Alternativa 2: Esquema RBAC Multi-Tabla con Permisos Granulares (`User` -> `UserRole` -> `Role` -> `Permission`)
- **Descripción**: Crear tablas intermedias para soportar múltiples roles por usuario y permisos atómicos asignados a roles.
- **Ventajas**:
  - (+) Máxima granularidad y configurabilidad dinámica en tiempo de ejecución.
- **Desventajas**:
  - (-) Alta complejidad de esquema y sobreingeniería innecesaria para las 6 issues del proyecto.
  - (-) Consultas con múltiples joins que degradan el rendimiento y complican las migraciones iniciales.

### Alternativa 3: Comprobaciones condicionales ad-hoc por vista
- **Descripción**: Mantener flags booleanos sueltos (`is_admin`, etc.) sin decorador estandarizado.
- **Ventajas**:
  - (+) Implementación rápida sin estructura común.
- **Desventajas**:
  - (-) Alto riesgo de omisión de seguridad en nuevas rutas.
  - (-) Código duplicado y nula extensibilidad para el rol `curator`.

---

## 4. Decisión Adoptada

Se adopta la **Alternativa 1 (RBAC con columna `role` en `User` y decorador `@role_required`)**.

Esta solución satisface íntegramente los criterios de aceptación del **Issue #188**, implementa el principio de mínimo privilegio con tres roles bien delimitados (`user`, `curator`, `admin`) y permite la delegación de tareas de curación de datasets globales sin comprometer el control administrativo de la plataforma.

---

## 5. Consecuencias y Efectos Derivados

### Efectos Positivos:
- (+) Decorador centralizado `@role_required(*roles)` que redirige anónimos a `/login` y aborta con HTTP 403 y plantilla `403.html` para usuarios sin privilegios.
- (+) Panel administrativo `/admin/users` y comandos CLI `rosemary user:promote` y `user:demote` para gobernanza completa.
- (+) Protección de auto-degradación que previene que un administrador se bloquee a sí mismo fuera del sistema.
- (+) Base lista para que el Issue #178 (Film-Hub datasets) pueda asignar tareas de curación al rol `curator`.

### Efectos Negativos o Deuda Técnica Asumida (Mitigación):
- (-) La migración Alembic sobre la tabla `user` debe coordinarse con el Issue #200 (2FA/TOTP) para evitar cabeceras divergentes (`multiple heads`) en `trunk`. (Mitigación documentada en la matriz de dependencias).
