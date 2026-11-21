# Metodología de Trabajo, Revisiones de Código y Ciclo de Vida de Issues - Film-Hub

**Autor:** Juan Felipe Pardo Carrillo (Quality Assurance Lead)  
**Asignatura:** Evolución y Gestión de la Configuración (EGC 2026/2027)  
**Proyecto:** Film-Hub  

Este documento define las pautas metodológicas de trabajo diario, el procedimiento de **revisión de código por pares sin Pull Requests internas** y las responsabilidades exactas de cada rol desde que se asigna un *Work Item* (issue) hasta su cierre e integración definitiva en el repositorio.

> Este documento complementa a la [Política de Ramas y Flujo de Trabajo (EGCFlow)](politica_ramas_y_flujo_trabajo.md), la [Metodología de CI/CD y Estrategia de Pruebas](Metodologia_CI-CD.md), la [Gestión de Bugs e Incidencias](gestion_bugs_e_incidencias.md) y el [Registro de Decisiones](toma_de_decisiones.md).

---

## 1. Fundamento Teórico y Principios de la Asignatura

De acuerdo con la teoría oficial de EGC, la calidad y trazabilidad del proyecto se apoyan en tres pilares que condicionan nuestra forma de trabajar:

1. **Integración directa con Git CLI (sin Pull Requests internas)**:  
   En **EGCFlow** están prohibidas las Pull Requests para integrar trabajo dentro del mismo equipo. Las mezclas se realizan directamente desde la terminal mediante `git merge` sobre la rama de integración (`trunk`), resolviendo conflictos en local y dejando el repositorio en un estado coherente. Las Pull Requests quedan reservadas exclusivamente para proponer cambios a repositorios de otros equipos.
2. **Revisión humana complementaria a la automatización**:  
   Los linters (`flake8`, `black`, `isort`) y las pruebas automatizadas verifican estilo y regresiones, pero no pueden evaluar la intención de diseño, el reparto de responsabilidades, la claridad de la solución o la cobertura real de casos límite. Toda tarea requiere una **revisión humana por pares (*peer review*) previa al merge en `trunk`**, garantizando además que al menos dos personas del equipo conozcan cada línea de código.
3. **Trazabilidad de extremo a extremo**:  
   Cada unidad de trabajo debe poder reconstruirse desde la necesidad hasta la entrega siguiendo la cadena:
   ```text
   Issue / Tarjeta Kanban  ──►  Rama de tarea  ──►  Commits atómicos (#id)  ──►  CI Nivel 1 (verde)  ──►  Revisión por pares  ──►  Merge a trunk + CI Nivel 2
   ```

---

## 2. Flujo de Estados en el Tablero Kanban

Para dar visibilidad al avance del equipo antes de cada seguimiento oficial, todo Work Item o incidencia transita por cinco estados claros en el tablero de GitHub Projects:

```text
[ Pendiente ] ──► [ En Progreso ] ──► [ En Revisión ] ──► [ Hecho ]
                         │                   │
                         └──► [ Bloqueada ] ◄┘
```

| Estado | Significado en Film-Hub | Condición de entrada / salida |
| :--- | :--- | :--- |
| **Pendiente** | Issue asignado en [Descomposición de WIs](descomposicion_work_items.md), pendiente de inicio. | Tiene responsable y revisor pre-merge definidos. |
| **En Progreso** | El responsable ha creado su rama de tarea desde `trunk` y está implementando código y pruebas. | Pasa a *En Revisión* cuando CI Nivel 1 está en verde. |
| **Bloqueada** | El avance depende de otro WI, de una migración previa o de una decisión técnica pendiente. | Se notifica en el canal oficial y se desbloquea tras resolver la dependencia. |
| **En Revisión** | Código terminado, rebasado sobre `trunk`, con CI Nivel 1 en verde y entregado al revisor técnico. | Pasa a *Hecho* tras el visto bueno del revisor y el merge en `trunk`. |
| **Hecho** | Integrado en `trunk`, CI Nivel 2 (`CI_full.yml`) en verde, rama efímera eliminada e issue cerrado. | Cumple íntegramente la *Definition of Done* (Sección 5). |

### 2.1. Uso con GitHub Issues, GitHub Projects y Etiquetas (*Labels*)

El tablero se gestiona directamente con las herramientas nativas de GitHub (**GitHub Issues** + **GitHub Projects** en vista *Board*), sin herramientas externas:

* **Tarjetas**: Cada tarjeta del tablero es una **Issue normal de GitHub** vinculada al *Project* del repositorio. Las cinco columnas del tablero (`Pendiente`, `En Progreso`, `Bloqueada`, `En Revisión`, `Hecho`) corresponden al campo `Status` de GitHub Projects.
* **Etiquetas (*Labels*) recomendadas en GitHub Issues**: Para filtrar rápidamente las issues por dificultad oficial de EGC, tipo y módulo, se utilizan las siguientes etiquetas estándar:
  * **Dificultad (según normativa EGC)**: `difficulty: mandatory`, `difficulty: high`, `difficulty: medium`.
  * **Tipo de tarea**: `type: work-item`, `type: docs`, `type: ci-cd`, `type: bug`.
  * **Estado rápido** (opcional, complementario al tablero): `status: in-review`, `status: blocked`.

---

## 3. Qué Tiene que Hacer Cada Uno en un Issue

Para evitar solapamientos o pasos olvidados, el ciclo de vida de cualquier Work Item se reparte entre el **Autor (Responsable)**, el **Revisor Técnico** y los **Roles Transversales (QA, PM, DevOps)**.

### 3.1. Responsabilidades del Autor del Issue (*Assignee*)

Quien tiene asignado un Work Item es dueño de su diseño interno y ejecuta estos 7 pasos en orden:

1. **Preparación y rama**:
   - Mover la tarjeta del issue a **En Progreso**.
   - Actualizar `trunk` y crear la rama de tarea correspondiente (`feature/WI-<id>-<resumen>` o `bugfix/issue-<id>-<resumen>`):
     ```bash
     git checkout trunk
     git pull origin trunk
     git checkout -b feature/WI-<id>-<resumen>
     ```
2. **Toma de decisiones durante el desarrollo**:
   - Las decisiones menores de implementación interna las toma de forma autónoma.
   - Si surge una decisión que afecta a más de un módulo, cambia el esquema común o altera la planificación, debe plantearse para **acuerdo unánime (4/4)** y registrarse en [toma_de_decisiones.md](toma_de_decisiones.md) (y con su ADR correspondiente si es arquitectónica).
3. **Implementación y pruebas obligatorias**:
   - Desarrollar la funcionalidad junto con sus **pruebas unitarias y de servicio** (y pruebas de integración HTTP si añade o modifica rutas; pruebas Selenium E2E si modifica flujos principales de UI, conforme a [Metodologia_CI-CD.md](Metodologia_CI-CD.md)).
   - Realizar commits atómicos siguiendo **Conventional Commits** e incluyendo la referencia a la issue: `feat(<ambito>): <descripcion> (#<id>)`.
4. **Validación local previa al `push`**:
   - Ejecutar las comprobaciones locales con la CLI del proyecto (`rosemary`):
     ```bash
     rosemary linter:fix
     rosemary linter
     rosemary test
     ```
   - Si la tarea afecta a vistas o flujos de pantalla, ejecutar también `rosemary selenium`.
5. **Subida a remoto y verificación de CI Nivel 1**:
   - Hacer `git push -u origin <rama-tarea>` y comprobar en GitHub Actions que los tres workflows rápidos (`CI_commits.yml`, `CI_lint.yml` y `CI_pytest.yml`) finalizan en **verde**.
6. **Sincronización con `trunk` y solicitud de revisión**:
   - Antes de pedir revisión, traer los últimos cambios de `trunk` para evitar conflictos posteriores:
     ```bash
     git fetch origin trunk
     git rebase origin/trunk
     ```
   - Si hay conflictos, resolverlos manualmente en local, volver a pasar `rosemary test` y actualizar la rama remota (`git push --force-with-lease` si se rebasó).
   - Mover la tarjeta a **En Revisión** y avisar por el canal oficial al **Revisor Pre-Merge** asignado en [descomposicion_work_items.md](descomposicion_work_items.md), indicando el nombre de la rama y el comando para inspeccionar los cambios (`git diff trunk..<rama>`).
7. **Corrección, integración en `trunk` y limpieza**:
   - Si el revisor detecta errores o mejoras, corregirlos en la misma rama y volver a verificar CI Nivel 1.
   - Con el visto bueno explícito del revisor, fusionar en local sobre `trunk` y subir los cambios:
     ```bash
     git checkout trunk
     git pull origin trunk
     git merge --no-ff feature/WI-<id>-<resumen> -m "feat(<ambito>): integrate WI-<id> into trunk (#<id>)"
     git push origin trunk
     ```
   - Comprobar que **CI Nivel 2 (`CI_full.yml`)** pasa en verde en `trunk`.
   - Eliminar la rama de tarea en local y remoto (`git branch -d <rama>` y `git push origin --delete <rama>`), cerrar la issue comentando el hash del commit de integración y mover la tarjeta a **Hecho**.

---

### 3.2. Responsabilidades del Revisor Técnico (*Peer Reviewer*)

Como no existen Pull Requests internas en GitHub, el revisor asignado realiza una **revisión pre-merge por pares** sobre la rama publicada por el autor antes de que este haga `git merge` hacia `trunk`.

#### Cómo inspeccionar los cambios en local sin PR
El revisor actualiza su repositorio y compara la rama del compañero frente a `trunk`:
```bash
git fetch origin
git diff origin/trunk..origin/feature/WI-<id>-<resumen>
```
También puede cambiar a la rama (`git checkout origin/feature/WI-<id>-<resumen>`) para ejecutar los tests en su propio entorno Docker o revisarla junto al autor en una llamada breve de Discord si el cambio es complejo.

#### Lista de comprobación de la revisión humana
El revisor no pierde tiempo en reglas de estilo que ya comprueba `CI_lint.yml`; se centra en lo que las herramientas automáticas no detectan:
- [ ] **Alcance y criterios de aceptación**: La solución cumple los requisitos definidos para el Work Item sin dejar casos a medias.
- [ ] **Diseño y claridad**: El código es legible, modular, sin lógica duplicada ni cambios ajenos al issue mezclados en los mismos commits.
- [ ] **Calidad de las pruebas**: Existen tests para casos válidos y casos de error/límite (no solo el *happy path*), y no se han desactivado ni debilitado pruebas de otros módulos.
- [ ] **Seguridad y configuración**: No hay credenciales, claves ni ficheros `.env` reales versionados; las migraciones Alembic (si existen) no generan doble cabecera (*multiple heads*).
- [ ] **CI Nivel 1 en verde**: El último `push` de la rama pasó `CI_commits`, `CI_lint` y `CI_pytest` sin errores.

#### Resolución de la revisión
* **Si todo está correcto**: El revisor comunica su aprobación explícita (en el canal del equipo o dejando un comentario de validación en la issue de GitHub) autorizando el `merge` a `trunk`.
* **Si detecta un bug o defecto**:
  1. No autoriza el `merge` a `trunk`.
  2. Aplica el protocolo de [gestion_bugs_e_incidencias.md](gestion_bugs_e_incidencias.md): **avisa directamente** al autor por el canal oficial y **registra el bug en la tabla** de dicho documento.
  3. Cuando el autor corrija el fallo en su rama, el revisor vuelve a comprobar que el error no se reproduce y actualiza el estado a `Resuelto` antes de dar luz verde al merge.

---

### 3.3. Responsabilidades de los Roles Transversales en Cada Ciclo

Aunque cada issue tiene un autor y un revisor concreto, los perfiles de coordinación velan por el conjunto del repositorio:

* **QA Lead (Juan Felipe Pardo Carrillo)**:
  - Verifica que todos los WIs cumplen la política de pruebas y cobertura (`--cov-fail-under`) definida en [Metodologia_CI-CD.md](Metodologia_CI-CD.md).
  - Audita el cumplimiento de las revisiones pre-merge y supervisa que los bugs registrados en [gestion_bugs_e_incidencias.md](gestion_bugs_e_incidencias.md) queden validados antes de pasar de `trunk` a `main`.
* **Project Manager (José Vicente Sánchez Montilla)**:
  - Mantiene actualizado el estado del tablero Kanban y vela por el cumplimiento de los hitos docentes (23 nov, 30 nov y 14/16 dic).
  - Modera los acuerdos unánimes (4/4) cuando una incidencia técnica afecta al alcance o a más de un módulo en [toma_de_decisiones.md](toma_de_decisiones.md).
* **DevOps Lead (Luis Lucena Prieto)**:
  - Supervisa la salud de los workflows en `.github/workflows/`, la integridad de las migraciones Alembic y el funcionamiento del entorno de preproducción.
  - Valida la integración completa en `trunk` (`CI_full.yml` en verde) antes de pasar a `main` y aprueba manualmente el despliegue en producción sobre Render (`CD_render.yml`).
* **Frontend Lead (Adrián Muñoz Aradilla)**:
  - Vela por la coherencia visual, usabilidad y correcto funcionamiento de las plantillas Jinja2 y pruebas E2E de interfaz en los módulos con impacto visual.

---

## 4. Asignación de Revisores por Work Item

Para evitar cuellos de botella y asegurar conocimiento cruzado entre todos los módulos, la asignación de autor y revisor pre-merge sigue lo establecido en [descomposicion_work_items.md](descomposicion_work_items.md):

| Work Item | Autor / Responsable | Revisor Pre-Merge |
| :--- | :--- | :--- |
| **#177 — WI-fakenodo** | Luis Lucena Prieto | José Vicente Sánchez Montilla |
| **#178 — WI-newdataset (Bloque Core)** | Juan Felipe Pardo Carrillo | Luis Lucena Prieto |
| **#178 — WI-newdataset (Bloque UI)** | Adrián Muñoz Aradilla | Juan Felipe Pardo Carrillo |
| **#178 — WI-newdataset (Bloque Filtros/Seeders)** | José Vicente Sánchez Montilla | Adrián Muñoz Aradilla |
| **#188 — Admin roles** | José Vicente Sánchez Montilla | Juan Felipe Pardo Carrillo |
| **#213 — Embeddable badge** | Adrián Muñoz Aradilla | Luis Lucena Prieto |
| **#200 — Two-factor authentication (2FA)** | Juan Felipe Pardo Carrillo | José Vicente Sánchez Montilla |
| **#202 — Active session management** | Luis Lucena Prieto | Juan Felipe Pardo Carrillo |

---

## 5. Criterios de Finalización (*Definition of Done*) de un Issue

Un Work Item o incidencia **solo se considera completamente finalizado y listo para cerrarse** cuando cumple todos los puntos siguientes:

- [ ] **Código y funcionalidad**: Implementación completa de acuerdo con los criterios de aceptación del issue.
- [ ] **Pruebas automatizadas**: Tests unitarios/de servicio (y de integración o Selenium cuando corresponda) añadidos y pasando al 100% sin romper otros módulos.
- [ ] **Calidad y estilo**: `rosemary linter` (`flake8`, `black`, `isort`) sin errores y cobertura dentro del umbral exigido.
- [ ] **Trazabilidad Git**: Commits atómicos conformes a Conventional Commits referenciando `(#<id>)`.
- [ ] **CI Nivel 1 en verde**: Workflows `CI_commits`, `CI_lint` y `CI_pytest` en verde sobre la rama de tarea antes de mezclar.
- [ ] **Revisión por pares aprobada**: Visto bueno explícito del Revisor Pre-Merge asignado (y sin bugs abiertos en `gestion_bugs_e_incidencias.md` asociados a esa rama).
- [ ] **Integración y limpieza**: Código fusionado en `trunk` con Git CLI, `CI_full.yml` en verde tras el push, rama efímera eliminada y tarjeta movida a **Hecho** en el tablero.
