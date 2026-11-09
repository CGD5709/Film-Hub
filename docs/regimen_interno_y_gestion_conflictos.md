# Regimen Interno, Convivencia y Resolucion de Conflictos

Este documento establece la normativa interna de colaboracion, comunicacion, toma de decisiones y gestion de discrepancias para el equipo **Film-Hub** durante el desarrollo de la asignatura **Evolucion y Gestion de la Configuracion (EGC)**.

---

## 1. Principios de Actuacion del Equipo

1. **Compromiso Compartido**: Aunque la evaluacion del proyecto contempla calificacion individual, el exito del producto final depende de la sincronizacion equitativa y constante de los cuatro integrantes.
2. **Trazabilidad de Acuerdos**: Cualquier decision organizativa, cambio de diseno o ajuste de alcance debe quedar registrado en el repositorio (diario de a bordo, actas de reunion o registros de decision arquitectonica ADR).
3. **Comunicacion Rigurosa y Constructiva**: El debate tecnico se realiza desde argumentos objetivos sustentados en estandares de ingenieria del software y el material docente oficial.
4. **Calidad no Negociable**: Ningun componente se incorporara a la linea de integracion sin superar las politicas de formato, linters y pruebas automatizadas.

---

## 2. Canales Oficiales de Comunicacion

| Canal | Finalidad | Tiempo Maximo de Respuesta |
| :--- | :--- | :--- |
| **Discord (Voz y Texto)** | Reuniones periodicas de sincronizacion, sesiones de programacion por pares y depuracion conjunta. | Conforme a convocatoria |
| **Grupo de Mensajeria Instantanea** | Notificacion de emergencias, avisos de bloqueo critico o cambios de disponibilidad inmediata. | Menor a 4 horas (horario lectivo) |
| **GitHub Issues y Discussions** | Debate tecnico sobre Work Items, revision de Pull Requests, seguimiento de bugs y diseño de modulos. | Menor a 24 horas |
| **Directorio `docs/` en Repositorio** | Deposito formal de politicas, acuerdos firmados, actas y contratos de interfaces. | Permanente |

---

## 3. Dinamica de Reuniones y Asistencia

### 3.1. Tipos de Sesiones
- **Reunion Semanal de Sincronizacion (Weekly Sync)**: Martes a las 18:00 (duracion estimada: 30-45 minutos). Orden del dia fijo:
  1. Revision de tareas concluidas en el ciclo anterior.
  2. Planificacion de tareas inmediatas.
  3. Deteccion de bloqueos tecnicos y dependencias cruzadas.
- **Sesiones Extraordinarias de Integracion**: Convocadas antes de cada hito oficial de evaluacion para validar el correcto despliegue conjunto en preproduccion.

### 3.2. Asistencia a las Sesiones Docentes Obligatorias
Conforme a la normativa oficial de evaluacion de EGC:
- La asistencia a los tres seguimientos presenciales de evaluacion continua (9, 23 y 30 de noviembre) es **obligatoria**. Cada ausencia no justificada formalmente conlleva una penalizacion individual de **-0,25 puntos**.
- La asistencia a la defensa y revision final del proyecto (14 y 16 de diciembre) es **estrictamente obligatoria**. La inasistencia no justificada supone una penalizacion de **-2,5 puntos** (calificacion final del proyecto: 0 puntos).

---

## 4. Resolucion de Discrepancias Tecnicas

Cuando surjan opiniones contrapuestas sobre decisiones de diseño, librerias o arquitectura:

```text
[ Discrepancia Tecnica ]
           |
           v
1. Analisis Tecnico: Comparativa de opciones, ventajas, costes de mantenimiento y riesgos.
           | (Si se alcanza consenso, se formaliza mediante ADR)
           v
2. Votacion del Equipo: 1 voto por integrante. En caso de empate (2 contra 2):
   - Decisiones de Arquitectura, Backend o Calidad: Voto de calidad de Juan Felipe Pardo (QA).
   - Decisiones de Infraestructura, Contenedores o CI/CD: Voto de calidad de Luis Lucena (DevOps).
   - Decisiones de Planificacion, Alcance o Proceso: Voto de calidad de Jose Vicente Sanchez (PM).
           | (Si persiste bloqueo o afecta a criterios docentes)
           v
3. Consulta y Mediacion del Tutor Docente Asignado
```

---

## 5. Protocolo de Actuacion ante Inactividad o Incumplimiento

Para garantizar la justicia en la calificacion individual y evitar que la inactividad de un miembro perjudique el avance colectivo, se define un protocolo formal y escalonado:

```text
[ Deteccion de falta de comunicacion o retraso injustificado ]
                             |
                             v (24 horas)
        Nivel 1: Contacto Informativo de Alerta Temprana
                             |
                             v (48 horas)
        Nivel 2: Convocatoria Extraordinaria de Regularizacion
                             |
                             v (72 horas)
        Nivel 3: Emision de Notificacion Formal de Apercibimiento
                             |
                             v
        Nivel 4: Reasignacion de Work Items y Comunicacion al Tutor Docente
```

### Detalle de Niveles de Actuacion:
1. **Nivel 1 (24 horas)**: El Project Manager establece comunicacion individualizada para interesarse por la situacion y recordar las entregas acordadas.
2. **Nivel 2 (48 horas)**: Ante la persistencia de falta de respuesta o incumplimiento reiterado de fechas limite, se convoca una reunion extraordinaria obligatoria para redefinir el plan de trabajo.
3. **Nivel 3 (72 horas)**: En ausencia de justificacion y persistiendo el retraso, se remite por correo institucional de la Universidad de Sevilla la **Plantilla de Apercibimiento por Inactividad**, incorporando constancia fehaciente en el diario del equipo.
4. **Nivel 4 (Escalado Docente)**: Si en las siguientes 24 horas no se produce la subsanacion, el equipo solicita audiencia con el profesor tutor de EGC para presentar las evidencias registradas en el repositorio (historico de commits, revision de ramas y actas), aplicando la reduccion de Work Items prevista para equipos de menor tamano y solicitando la evaluacion individual diferenciada.

---

## 6. Matriz RACI de Responsabilidades

Definicion de competencias:
- **R (Responsible)**: Miembro encargado de la ejecucion tecnica directa.
- **A (Accountable)**: Miembro responsable de la aprobacion y calidad final de la entrega.
- **C (Consulted)**: Miembro consultado para contraste tecnico o metodologico.
- **I (Informed)**: Miembro informado del progreso o resultado final.

| Area / Work Item | Jose Vicente (PM) | Luis Lucena (DevOps) | Juan Felipe (QA) | Adrian Munoz (UI) |
| :--- | :---: | :---: | :---: | :---: |
| **Gestion de Proyecto, Hitos y Actas** | **A / R** | I | C | I |
| **Infraestructura Docker, CI/CD y Despliegue** | I | **A / R** | C | I |
| **WI #177 (Servicio Fakenodo)** | C | **A / R** | C | I |
| **WI #178 (Dominio Film-Hub CSV)** | C | C | **A / R** | R |
| **WI #188 (Admin Roles y Permisos)** | **A / R** | I | C | I |
| **WI #213 (Insignias Dinamicas SVG)** | I | C | I | **A / R** |
| **WI #200 (Autenticacion 2FA / TOTP)** | C | C | **A / R** | I |
| **WI #202 (Gestion de Sesiones Activas)** | I | **A / R** | C | C |
| **Revision de Calidad y Pruebas Pytest** | I | C | **A / R** | I |
