---
name: Work Item / Feature
about: Definicion de nueva funcionalidad o tarea asociada a un Work Item
title: '[WI-XX]: <titulo de la funcionalidad>'
labels: ['feature', 'work-item']
assignees: ''
---

## 1. Informacion General
- **Work Item**: [WI-177 / WI-178 / WI-188 / WI-200 / WI-202 / WI-213]
- **Responsable**: @
- **Dificultad Estimada**: [Mandatory / High / Medium / Low]
- **Rama Asociada**: `feature/WI-<id>-<resumen-slug>`

## 2. Descripcion
[Explicar que aporta esta funcionalidad y como se integra en Film-Hub]

## 3. Criterios de Aceptacion (Given-When-Then)
```gherkin
Escenario: Caso de exito principal
  Dado [contexto inicial]
  Cuando [el usuario realiza una accion]
  Entonces [el resultado esperado]
```

## 4. Tareas Tecnicas (Checklist TDD)
- [ ] Modelos de datos y migracion de base de datos
- [ ] Pruebas unitarias de comportamiento (Fase Roja)
- [ ] Implementacion de servicios y controladores (Fase Verde)
- [ ] Vistas e interfaz de usuario
- [ ] Comprobacion de linters (flake8, black, isort)
- [ ] Suite completa de Pytest en verde

## 5. Validacion
- [ ] Pruebas unitarias en `app/features/<feature>/tests/`
- [ ] Pruebas de persistencia en base de datos

