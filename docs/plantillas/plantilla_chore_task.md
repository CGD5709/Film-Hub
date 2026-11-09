# Plantilla de Tarea de Mantenimiento o Infraestructura (Chore)

> Utilizar esta plantilla para planificar y documentar tareas tecnicas internas que no introducen funcionalidades visibles al usuario final (CI/CD, scripts, Docker, dependencias, refactorizaciones internas).

---

## 1. Informacion General
- **Titulo**: [chore]: [Descripcion concisa de la tarea tecnica]
- **Responsable**: [@usuario]
- **Revisor Tecnico**: [@usuario_revisor]
- **Area Afectada**: [Docker / CI-CD / Rosemary / Dependencias / Refactor]
- **Rama Asociada**: `chore/<resumen-slug>`

---

## 2. Descripcion y Justificacion Tecnica
[Detallar la necesidad tecnica que motiva la tarea: actualizacion de imagen base, depuracion de scripts, optimizacion de pipelines o ajuste de dependencias.]

---

## 3. Plan de Actuacion Tecnico
- [ ] Tarea 1: [Detalle del cambio en configuracion o codigo].
- [ ] Tarea 2: [Pruebas de verificacion local en Docker].
- [ ] Tarea 3: [Comprobacion de ausencia de regresiones en la suite general].

---

## 4. Validacion Realizada
- [ ] Verificado que el cambio no altera el comportamiento funcional existente.
- [ ] Comprobado el paso en verde de linters (`flake8`, `black`, `isort`).
- [ ] Ejecutada la suite completa de pruebas de regresion en `app/features/`.

