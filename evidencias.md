# Evidencias — Semana 1, día 4

## Evidencia 1 — Datos iniciales

Repositorio local: `reto-0` en `TALLER7`.

| N.º | Criterio | Descripción del fallo | Archivo y línea |
|---:|---|---|---|
| 1 | Validación de entradas | Se aceptan usuarios y títulos vacíos o excesivamente largos. | `app.py:52`, `app.py:77` |
| 2 | Contraseñas y hash | La contraseña se guarda directamente en SQLite. | `app.py:56` |
| 3 | Control de acceso | La lista de tareas consulta todas las tareas, sin filtrar por usuario. | `app.py:80` |

## Evidencia 2 — Secretos

La revisión inicial debe ejecutarse con `git grep -n -i --untracked -E "secret|token|key *=|password *=" -- "*.py"`; la clave de desarrollo se elimina antes de publicar.

## Evidencias 3–10

Se completan con capturas de AGENTS.md, pruebas, Ruff, commits, PR, auditoría, firma, tag y Actions cuando estén disponibles.

