# Registro de Decisiones del Equipo

En este documento se recogen los acuerdos y decisiones tomadas por el equipo a lo largo del desarrollo de Film-Hub.

Cualquier decisión que los miembros del equipo hayamos tomado juntos y consideremos importante —ya sea porque afecta a todo el proyecto en su conjunto, porque tiene impacto en más de un módulo o porque modifica la planificación, el diseño o la forma de trabajar, sean estas decisiones a nivel técnico o no— debe estar pactada y validada por todos los miembros del equipo (los cuatro integrantes) y quedar registrada formalmente en la tabla de este documento. Por su parte, las decisiones menores o los detalles específicos del desarrollo del día a día de cada tarea los asume con autonomía la persona responsable de dicha tarea.

Asimismo, si se trata de una **decisión arquitectónica o de diseño**, se creará un documento independiente basado en la [Plantilla de Decisión Arquitectónica (ADR)](plantillas/plantilla_decision_tecnica_ADR.md) ubicada en la carpeta `docs/plantillas/` cumplimentado con el contenido correspondiente (contexto, alternativas evaluadas y consecuencias), y dicho documento quedará referenciado y enlazado directamente en la propia tabla de decisiones.

---

## Registro de Decisiones

| ID | Fecha | Tipo | Título y Descripción de la Decisión | Justificación / Motivo | Documento / ADR | Estado |
| :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| **DEC-001** | 28/10/2026 | Producto  | Adopción del dominio Film-Hub y soporte exclusivo para archivos CSV | Temática que interesa y motiva a los cuatro miembros del equipo, con gran abundancia de datasets públicos. Se limita exclusivamente a formato CSV por ser el tipo de archivo más extendido y común en datasets abiertos, haciendo el desarrollo accesible, viable e interesante. | - | **Aprobada** |
| **DEC-002** | 04/11/2026 | Organización | Reparto de trabajo mediante desarrollo autónomo por tarea y colaboración conjunta en el módulo central de películas (Issue #178) | Minimiza dependencias cruzadas y bloqueos en Git, permitiendo avanzar en paralelo desde el primer día. | - | **Aprobada** |
| **DEC-003** | 09/11/2026 | Proceso / Git | Adopción de EGCFlow con rama `trunk` y prohibición de Pull Requests internas | Cumplimiento de la normativa docente de la asignatura; revisión por pares mediante diff local y merge directo en terminal. | - | **Aprobada** |
| **DEC-004** | 22/11/2026 | Arquitectura / Auth | Control de acceso basado en roles (admin, curator, user) en el modelo User | Define una jerarquía RBAC de 3 roles donde admin gestiona la plataforma, curator valida/cura datasets cinematográficos globales y user opera por defecto (sin rol guest adicional). | [ADR-001](adrs/ADR-001-control-acceso-rbac.md) | **Aprobada** |

