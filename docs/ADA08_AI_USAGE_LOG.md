# Mi bitácora profesional de uso de IA - ADA-08

Yo utilicé asistencia de IA para analizar el repositorio, diseñar contratos y automatizar verificaciones. Yo registré decisiones técnicas y evidencia verificable en las siguientes cinco etapas.

## 1. Auditoría inicial

Yo analicé el proyecto heredado de ADA-05 y los artefactos de ADA-07. Yo identifiqué la ausencia de un mapa por tarea, un comando único de validación, lint, CI y protección de evidencia. Yo conservé el baseline antes de implementar el cambio y evalué las ocho dimensiones con los pesos de la rúbrica. Yo registré 61/100 y preservé la suite de 25 pruebas.

## 2. Diseño de AGENTS.md

Yo organicé fuentes de verdad, rutas, comandos estándar, reglas de cambio, stop conditions y Definition of Done. Yo mantuve los requisitos en REQUIREMENTS.md y los criterios de aceptación en SPEC.md. Yo utilicé REPO_MAP para conectar la tarea con código y pruebas y evité duplicar requisitos en adaptadores de herramientas.

## 3. Guardrail y automatización

Yo convertí reglas verificables en scripts: pytest, Ruff, integridad de archivos protegidos, referencias de requisitos, dependencias y permisos de CI. Yo fijé las versiones de las herramientas y comprobé los guardrails mediante mutaciones de copias temporales. Yo mantuve explícito el alcance del análisis estático y de la detección de archivos sensibles.

## 4. Ejecución AFTER

Yo partí del mismo código funcional y utilicé árboles de trabajo separados. Yo implementé CR-ADA08-01 desde el modelo original y conservé los comandos, sus códigos de salida y los parches. Yo observé seis fallos esperados antes del arreglo y la suite verde después. Yo conservé un estado de agente compartido entre condiciones; por eso yo mantuve la validez experimental como PARTIAL.

## 5. Evaluación final y reflexión

Yo calculé 91/100 AFTER y una mejora de 30 puntos. Yo distinguí las 35 pruebas de producto de las quince pruebas del contrato. Yo conservé el mapa, la trazabilidad y el gate compartido como base de trabajo. Yo mantuve pendiente la réplica con estados de agente independientes y reservé los cambios semánticos de requisitos y arquitectura para revisión humana.
