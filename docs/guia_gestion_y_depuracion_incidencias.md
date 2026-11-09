# Guia de Gestion y Depuracion Metodica de Incidencias

Este documento establece el protocolo formal para reportar, priorizar, depurar y corregir defectos en **Film-Hub**, aplicando la metodologia estructurada del **Capitulo 5** de la asignatura **Evolucion y Gestion de la Configuracion (EGC)**.

---

## 1. Conceptos Fundamentales: Error, Defecto y Fallo

Para asegurar la precision conceptual en la comunicacion del equipo:

```text
    [ Error Humano ]  ---(equivocacion de diseno o programacion)---> 
    [ Defecto (Bug) ] ---(permanece latente en el artefacto)-------> 
    [ Fallo ]         ---(manifestacion observable durante ejecucion)
```

- **Error**: Accion humana desacertada que genera un resultado no esperado (ejemplo: asumir que un campo numerico nunca contendra valores nulos en el archivo CSV).
- **Defecto (Bug)**: Imperfeccion o manifestacion latente en el codigo fuente como consecuencia del error (ejemplo: ausencia de clausula de salvaguarda `if not row.get('year')`).
- **Fallo**: Discrepancia externa observable entre el comportamiento del sistema y el comportamiento especificado (ejemplo: una excepcion `ValueError` produce un error HTTP 500 al subir una pelicula).

> **Nota Metodologica**: Probar (Testing) no equivale a Depurar (Debugging). Probar identifica la presencia de fallos; depurar localiza la causa raiz (el defecto), la subsana y asegura la ausencia de regresiones.

---

## 2. Metodo de Depuracion en Cuatro Fases

Ante cualquier fallo detectado en la aplicacion, se prohiben modificaciones improvisadas. Es preceptivo seguir estas cuatro etapas:

```text
+-----------------+      +------------------+      +-----------------+      +--------------------+
|  1. REPRODUCIR  | ---> | 2. DIAGNOSTICAR  | ---> |   3. REPARAR    | ---> |    4. ANALIZAR     |
| Entorno Limpio  |      | Hipotesis y Logs |      | TDD / Causa Raiz|      | Suite de Regresion |
| Caso Minimo MRE |      | Pair Debugging   |      | Commit Atomico  |      | Lecciones y Proceso|
+-----------------+      +------------------+      +-----------------+      +--------------------+
```

### Fase 1: Reproducir el Fallo
No se debe abordar la reparacion de un defecto sin contar previamente con un procedimiento de reproduccion determinista.
1. **Entorno Aislado**: Iniciar el entorno en un contenedor limpio mediante Docker Compose para descartar estados residuales locales:
   ```bash
   docker compose -f docker/docker-compose.dev.yml up -d --build
   ```
2. **Ejemplo Minimo Reproducible (MRE)**:
   - Reducir el archivo o la entrada de datos al menor numero de lineas que mantenga la aparicion del fallo.
   - Aislar las variables y condiciones exactas que disparan la anomalia.

### Fase 2: Diagnosticar la Causa Raiz
1. **Formulacion de Hipotesis Falsables**:
   - Plantear una afirmacion contrastable sobre el origen del fallo y verificar si los datos la respaldan o refutan.
2. **Inspeccion de Trazas y Registros (Logs)**:
   - Analizar la traza completa de la excepcion generada en el contenedor:
     ```bash
     docker compose logs -f web
     ```
3. **Tecnicas de Apoyo**:
   - **Explicacion en voz alta (Rubber Duck Debugging)**: Describir el flujo de control para explicitar supuestos no verificados.
   - **Pair Debugging**: Si un desarrollador permanece bloqueado mas de 30 minutos, convocara una sesion de depuracion conjunta con el QA Lead o el DevOps Lead.

### Fase 3: Reparar con Pruebas Automatizadas (TDD)
1. Escribir una prueba automatizada en Pytest que manifieste el fallo detectado.
2. Comprobar que la prueba **falla** por la causa diagnosticada (Fase Roja).
3. Implementar la correccion minima y especifica en el codigo fuente (Fase Verde).
4. Ejecutar la suite completa de pruebas para garantizar que no se introducen regresiones funcionales:
   ```bash
   docker compose exec web pytest app/features/ --ignore-glob='*selenium*'
   ```
5. **Regla de Aislamiento**: No mezclar la reparacion de un bug con tareas de refactorizacion de codigo. La correccion del fallo debe constituir un commit atomico independiente.

### Fase 4: Analizar lo Aprendido
Tras resolver la incidencia:
- Evaluar que comprobacion de linter o prueba de integracion debio detectar el defecto previamente.
- Incorporar la nueva prueba a la bateria permanente de regresion en CI.
- Para incidencias de severidad Critica o Mayor, cumplimentar la plantilla de Analisis Post-Mortem.

---

## 3. Clasificacion por Severidad y Prioridad

### 3.1. Niveles de Severidad (Impacto Tecnico)
- **Critica**: Interrupcion total del servicio, corrupcion de datos o brecha de seguridad grave (ejemplo: omision de validacion en 2FA o caida del servicio de base de datos).
- **Mayor**: Bloqueo de una funcionalidad principal asociada a un Work Item sin alternativa operativa viable.
- **Menor**: Funcionamiento anomalo en caracteristicas no esenciales o con solucion provisional simple.
- **Trivial**: Defectos puramente visuales, desajustes de maquetacion o erratas tipograficas.

### 3.2. Niveles de Prioridad (Urgencia de Intervencion)
- **P0 - Inmediata**: Resolucion en menos de 24 horas; bloquea el progreso del equipo o la entrega de un hito.
- **P1 - Alta**: Se aborda en la iteracion en curso antes de desarrollar nuevas funcionalidades.
- **P2 - Media**: Planificada para la siguiente reunion de sincronizacion.
- **P3 - Baja**: Atencion subordinada a la disponibilidad del calendario.

---

## 4. Ciclo de Vida de Incidencias en GitHub Projects

```text
[ Backlog / Triage ] ---> [ Todo (Priorizada) ] ---> [ In Progress (Rama bugfix) ]
                                                               |
[ Done (Cerrada) ]   <--- [ In Review (PR + CI Verde) ] <------+
```

1. **Backlog / Triage**: Registro de la incidencia con la plantilla oficial `.github/ISSUE_TEMPLATE/bug_report_template.md`. Evaluacion de severidad por PM y QA.
2. **Todo**: Asignacion a un desarrollador para su tratamiento.
3. **In Progress**: Creacion de la rama `bugfix/issue-<id>-<resumen>` y aplicacion del ciclo de depuracion.
4. **In Review**: Pull Request vinculada que incorpora la prueba de regresion y supera los flujos de CI.
5. **Done**: Fusion en `trunk` y cierre automatico del ticket mediante `Fixes #<id>` o `Closes #<id>`.
