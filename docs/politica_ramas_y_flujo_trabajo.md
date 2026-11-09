# Politica de Ramas, Versionado y Flujo de Trabajo (EGCFlow)

Este documento establece la normativa de gestion del codigo fuente, uso del repositorio y flujo de integracion para el proyecto **Film-Hub**, adoptando estrictamente el modelo **EGCFlow** definido en la asignatura **Evolucion y Gestion de la Configuracion (EGC)** de la ETSII (Universidad de Sevilla).

---

## 1. Regla Fundamental: Prohibicion de Pull Requests Internas

Conforme al programa docente y los apuntes oficiales de EGC (Capitulo 3, Seccion 3.5.3):

> **Regla de Catedra EGC**: En EGCFlow **no se utilizan Pull Requests como mecanismo para integrar trabajo dentro del mismo equipo**. 
> La razon es didactica: el alumnado debe dominar las operaciones directas con la herramienta Git desde la linea de comandos (traer cambios, mezclar ramas, resolver conflictos manualmente en local, verificar el resultado y dejar el arbol en estado consistente), sin delegar el proceso en la interfaz web de GitHub ni ocultarlo tras un boton.
> 
> **Ambito exclusivo de las Pull Requests**: Los Pull Requests se reservan **unica y exclusivamente para interacciones entre diferentes equipos** (por ejemplo, cuando nuestro equipo propone una mejora o correccion al repositorio de otro grupo, o viceversa, existiendo una frontera clara entre proyectos).

---

## 2. El Modelo de Ramas: EGCFlow

EGCFlow se articula en torno a una linea principal de entregas inmutables (`main`), una linea de integracion compartida del equipo (`trunk` o `trunk`) y ramas de tarea de ciclo de vida corto.

```text
       v1.0.0                    v1.1.0 (Hito oficial)
main     +-------------------------+-------------------------> (Releases inmutables)
        ^                         ^
trunk  +-------+-------+---------+-------+-----------------> (Linea de integracion continua)
          \     ^ \     ^         /       ^
feature/   +---+   \   /         +---+---+
WI-178              +-+
feature/WI-200
```

### 2.1. Ramas Permanentes

1. **`main` (Linea de Entrega y Produccion)**:
   - Contiene unicamente versiones estables, probadas y etiquetadas formalmente mediante SemVer (`vX.Y.Z`).
   - Cada commit en `main` representa una Release oficial del software.
   - Solo se actualiza desde `trunk` en los hitos oficiales de entrega previa validacion exhaustiva.

2. **`trunk` (Linea de Integracion Continua)**:
   - Tronco comun de integracion del equipo. Todos los cambios terminados se incorporan directamente aqui desde la terminal.
   - Debe mantenerse en estado saludable: las pruebas automatizadas y las comprobaciones estaticas de estilo deben ejecutarse en verde en todo momento.
   - De `trunk` nacen todas las ramas de tarea.

### 2.2. Ramas Efimeras (Ramas de Tarea)

Las ramas de tarea representan una unidad de trabajo autocontenida. Queda expresamente prohibido el uso de ramas nominales por desarrollador (por ejemplo, `rama-juan` o `adrian-dev`), ya que oscurecen la historia y degradan la trazabilidad.

| Tipo de Rama | Patron de Nomenclatura | Proposito | Rama Origen | Rama Destino |
| :--- | :--- | :--- | :--- | :--- |
| **Feature / WI** | `feature/WI-<id>-<resumen>` | Desarrollo de un Work Item asignado (ej: `feature/WI-200-2fa-totp`). | `trunk` | `trunk` |
| **Bugfix** | `bugfix/issue-<id>-<resumen>` | Correccion de un defecto detectado (ej: `bugfix/issue-24-csv-null-year`). | `trunk` | `trunk` |
| **Chore** | `chore/<descripcion>` | Tareas de infraestructura, dependencias o configuracion Docker. | `trunk` | `trunk` |
| **Docs** | `docs/<descripcion>` | Creacion o actualizacion de documentacion tecnica. | `trunk` | `trunk` |
| **Hotfix** | `hotfix/<version>-<resumen>` | Correccion urgente sobre produccion. | `main` | `main` y `trunk` |

---

## 3. Convencion de Commits: Conventional Commits

Cada commit debe ser atomico y seguir la especificacion **Conventional Commits**, verificada automaticamente por el pipeline de integracion continua (`CI_commits.yml`).

### 3.1. Formato Estandar

```text
<tipo>(<ambito>): <descripcion en imperativo en minusculas> (#<id_issue>)

[cuerpo explicativo opcional: justificacion tecnica del cambio]

[pie opcional: referencias de cierre]
```

### 3.2. Tipos de Commit Permitidos

- `feat`: Nueva funcionalidad asociada a un Work Item.
- `fix`: Correccion de un defecto o fallo reportado.
- `test`: Inclusion o modificacion de pruebas automatizadas.
- `refactor`: Modificacion interna de codigo sin alteracion de comportamiento externo.
- `chore`: Tareas de compilacion, configuracion auxiliar o dependencias.
- `ci`: Ajustes en pipelines de integracion y despliegue continuo (`.github/workflows/`).
- `docs`: Modificaciones exclusivas en archivos de documentacion.
- `style`: Ajustes de formato o espaciado sin impacto funcional.

### 3.3. Ambitos Principales (`scope`)

- `dataset`: Modulo de conjuntos de datos cinematograficos y procesamiento CSV.
- `auth`: Autenticacion, usuarios, roles y 2FA.
- `session`: Gestion y control de sesiones activas concurrentes.
- `badge`: Generador de insignias vectoriales SVG.
- `fakenodo`: Simulador de la API de Zenodo.
- `rosemary`: Comandos y extensiones de la CLI Rosemary.
- `docker`: Configuracion de contenedores y servicios Compose.

### 3.4. Ejemplos de Referencia

- Correcto: `feat(auth): implement totp secret generation and qr render (#200)`
- Correcto: `test(dataset): add unit tests for rfc 4180 csv validation (#178)`
- Correcto: `fix(session): invalidate expired session tokens on logout (#202)`
- Incorrecto: `Arreglado el login` (no sigue el estandar, carece de tipo, ambito y referencia a issue).
- Incorrecto: `feat: cambios varios` (descripcion ambigua y ambito omitido).

---

## 4. Ciclo de Trabajo e Integracion Local con Git CLI (Paso a Paso)

Todo integrante del equipo debe ejecutar las integraciones a traves de la terminal de Git, sin recurrir a Pull Requests internas:

### Paso 1: Actualizar la base local y crear la rama de tarea
```bash
git checkout trunk
git pull origin trunk
git checkout -b feature/WI-200-2fa-totp
```

### Paso 2: Desarrollo guiado por pruebas (TDD)
1. Escribir primero las pruebas unitarias que definan el requisito en `tests/`.
2. Ejecutar la prueba y comprobar que falla (Fase Roja):
   ```bash
   docker compose exec web pytest app/features/auth/tests/test_totp.py
   ```
3. Implementar el codigo fuente estrictamente necesario hasta que la prueba pase (Fase Verde).
4. Refactorizar el codigo preservando las pruebas en verde.

### Paso 3: Validaciones de calidad y estilo en el contenedor
Antes de preparar la integracion, comprobar linters y pruebas:
```bash
# Validacion estatica
docker compose exec web flake8 app rosemary
docker compose exec web black --check app rosemary
docker compose exec web isort --check-only app rosemary

# Suite completa de pruebas de regresion
docker compose exec web pytest app/features/ --ignore-glob='*selenium*'
```

### Paso 4: Sincronizar con el estado mas reciente de `trunk`
Para evitar conflictos diferidos y asegurar una historia lineal:
```bash
git fetch origin trunk
git rebase origin/trunk
```
Si surgen conflictos, resolverlos manualmente en el editor, marcar los archivos resueltos con `git add <archivo>` y continuar con `git rebase --continue`.

### Paso 5: Integracion local en `trunk` y revision cruzada
Una vez la rama de tarea esta rebasada y las pruebas pasan en verde:
```bash
# Cambiar a la linea de integracion y actualizar
git checkout trunk
git pull origin trunk

# Fusionar la rama de tarea
git merge --no-ff feature/WI-200-2fa-totp -m "feat(auth): merge feature/WI-200-2fa-totp into trunk (#200)"
```
*Nota de Revision*: Antes de realizar el push definitivo, el responsable de la tarea realiza una revision rapida (peer review presencial o via llamada en Discord) con el QA Lead o el DevOps Lead para verificar que el diff es limpio y no incluye secretos ni archivos temporales.

### Paso 6: Verificacion final y push directo a `trunk`
```bash
# Ultima comprobacion de seguridad de pruebas
docker compose exec web pytest app/features/ --ignore-glob='*selenium*'

# Publicar en el repositorio remoto
git push origin trunk
```

### Paso 7: Destruccion de la rama de tarea
Conforme a los principios de EGC: *"las ramas que dejan de usarse se destruyen"*:
```bash
# Borrado de la rama local
git branch -d feature/WI-200-2fa-totp

# Borrado de la rama remota si hubiera sido publicada previamente
git push origin --delete feature/WI-200-2fa-totp
```

---

## 5. Uso Exclusivo de Pull Requests: Colaboracion Entre Diferentes Equipos

Las Pull Requests quedan reservadas de forma exclusiva para la comunicacion y colaboracion **entre distintos grupos**:

- **Caso 1: Contribucion a otro equipo**: Cuando el equipo Film-Hub detecta un bug o propone una mejora en el repositorio de otro grupo de la asignatura, se abre una Pull Request formal hacia el repositorio de dicho equipo utilizando la [Plantilla de Pull Request entre Equipos](plantillas/plantilla_pull_request.md).
- **Caso 2: Recepcion de propuesta de otro equipo**: Si otro grupo envia una Pull Request a Film-Hub, el equipo evalua los cambios, ejecuta los flujos de CI, debate la propuesta en reunion y decide si aceptarla o rechazarla.

---

## 6. Politica de Versionado y Releases (SemVer)

Film-Hub aplica la especificacion **Semantic Versioning 2.0.0** (`MAJOR.MINOR.PATCH`):
- **MAJOR**: Modificaciones que introducen incompatibilidades directas con versiones anteriores.
- **MINOR**: Incorporacion de nuevas funcionalidades manteniendo compatibilidad retroactiva.
- **PATCH**: Correcciones de defectos y parches compatibles con la version previa.

### Procedimiento para Publicar una Release Oficial en `main`:
1. Comprobar que `trunk` se encuentra en un estado estable y todos los pipelines de CI estan en verde.
2. Integrar `trunk` en `main` mediante Git CLI:
   ```bash
   git checkout main
   git pull origin main
   git merge --ff-only trunk
   ```
3. Crear la etiqueta inmutable firmada:
   ```bash
   git tag -a v1.0.0 -m "release: version v1.0.0 para evaluacion oficial de Film-Hub"
   git push origin main --tags
   ```
4. El push de la etiqueta dispara automaticamente el workflow `CD_dockerhub.yml`, construyendo y registrando la imagen Docker inmutable.
