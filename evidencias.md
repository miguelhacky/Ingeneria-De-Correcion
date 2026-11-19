# Evidencias — Semana 1, día 4

## Evidencia 1 — Datos iniciales

Repositorio local: `reto-0` en `TALLER7`.

| N.º | Criterio | Descripción del fallo | Archivo y línea |
|---:|---|---|---|
| 1 | Validación de entradas | El registro y la creación de tareas aceptan campos vacíos o excesivamente largos. | `app.py:52`, `app.py:94` |
| 2 | Contraseñas y hash | Las contraseñas se guardaban y comparaban en texto plano. | `app.py:61`, `app.py:82` |
| 3 | Control de acceso | Actualizar o eliminar una tarea no validaba el propietario. | `app.py:111`, `app.py:122` |

## Evidencia 2 — Secretos

La revisión inicial debe ejecutarse con `git grep -n -i --untracked -E "secret|token|key *=|password *=" -- "*.py"`; la clave de desarrollo se elimina antes de publicar.

## Evidencias 3–10

Se completan con capturas de AGENTS.md, pruebas, Ruff, commits, PR, auditoría, firma, tag y Actions cuando estén disponibles.

## Auditoría final — Evidencia 9

| Criterio | Resultado hoy | Cómo se comprobó |
|---|---|---|
| Ejecución | Cumple | `python -m pytest -v` arranca la app mediante el cliente Flask. |
| Validación de entradas | Cumple | `test_rechaza_usuario_vacio` y límites en servidor. |
| Contraseñas y hash | Cumple | `test_no_guarda_contrasena_en_texto_plano` verifica el valor almacenado. |
| Secretos y claves | Cumple parcialmente | `.env` está ignorado y la clave se lee del entorno; falta verificación remota. |
| Control de acceso | Cumple | `test_usuario_no_ve_tareas_de_otro_usuario` y filtro por `user_id`. |
| Dependencias y alucinación | Cumple parcialmente | Dependencias mínimas instaladas y Ruff pasa; falta auditoría en PyPI. |
| Pruebas | Cumple | 4 pruebas pasan y el hook ejecuta pytest. |
| Manejo de errores | Cumple parcialmente | Entradas inválidas devuelven 400; falta una suite completa de 404/errores. |
| Estructura | Cumple | Código en `app.py`, pruebas en `tests/` y comandos documentados. |

## PR local — Evidencia 8

Título sugerido: `Corrige tres fallos de la auditoría del reto 0`.

### Qué cambia

- `test_no_guarda_contrasena_en_texto_plano`: guarda contraseñas con hash.
- `test_rechaza_usuario_vacio`: valida entradas obligatorias y longitud.
- `test_usuario_no_ve_tareas_de_otro_usuario`: filtra tareas por usuario autenticado.

### Por qué se hizo así

Se aplicó el cambio mínimo en el servidor y se conservaron las pruebas como protección permanente.

### Qué podría romperse

Los usuarios creados con contraseñas antiguas en texto plano necesitarían registrarse de nuevo o migrarse de forma controlada.

## Pendientes externos

- Crear/publicar el repositorio público en GitHub y abrir/fusionar el PR desde `correcciones`.
- Trabajar en `plataforma-ludica`: firmar `POLITICA_IA.md`, crear el tag `semana-1` y comprobar Actions.
- Escribir la conclusión personal de 3–5 líneas sin asistencia de IA.
- Exportar las evidencias con capturas como `FajardoMiguelSemana1Dia4.pdf` y subirlo al Drive del curso.

