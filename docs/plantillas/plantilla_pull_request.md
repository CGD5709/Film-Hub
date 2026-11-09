# Plantilla de Pull Request entre Equipos (Inter-Grupos)

> **Aviso de Normativa EGC**: En EGCFlow, las Pull Requests dentro del mismo equipo estan prohibidas (la integracion interna se realiza directamente con Git CLI desde terminal). Esta plantilla se utiliza **exclusivamente para colaboraciones, propuestas de cambio y revisiones cruzadas entre diferentes equipos**.

---

## 1. Informacion del Equipo Remitente
- **Equipo Proponente**: [Nombre del equipo emisor, ej: Equipo Film-Hub]
- **Repositorio de Origen**: [Enlace al fork o rama del equipo emisor]
- **Equipo Receptor**: [Nombre del equipo destinatario]
- **Persona de Contacto**: [@usuario_contacto]

---

## 2. Proposito de la Propuesta
- [ ] Correccion de defecto detectado en el repositorio externo.
- [ ] Propuesta de mejora en modulo comun o especificacion de API.
- [ ] Actualizacion de documentacion compartida o pruebas de integracion.

---

## 3. Resumen Tecnico de los Cambios
[Explicar detalladamente que modifica esta propuesta, la justificacion tecnica de los cambios y como pueden ser validados por el equipo receptor.]

---

## 4. Evidencias de Validacion Aportadas
- [ ] Se adjuntan pruebas automatizadas que demuestran la correccion o nueva funcionalidad.
- [ ] La suite de pruebas y linters del proyecto receptor se ejecutan en verde con estos cambios.
- [ ] Se ha verificado la ausencia de efectos secundarios o incompatibilidades hacia atras.

---

## 5. Instrucciones de Prueba para el Equipo Receptor
1. Clonar o traer los cambios de la rama propuesta.
2. Ejecutar el siguiente comando de validacion: `[comando]`.
3. Comportamiento observable esperado: `[detallar resultado]`.

---

## 6. Resolucion del Equipo Receptor (A cumplimentar por el equipo destinatario)
- **Estado**: [ ACEPTADA / RECHAZADA / CAMBIOS SOLICITADOS ]
- **Evaluador(es)**: [@usuario_receptor]
- **Comentarios o Motivos de la Decision**: [Detallar fundamentacion del veredicto]
