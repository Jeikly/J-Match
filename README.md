# J-Match — Corte I

**Proyecto:** J-Match, asistente especializado en smartwatches.  
**Equipo:** J-Soft. **Asignatura:** Nuevas Tecnologías (SEP149).  
**Alcance de este corte:** CRUD de smartwatches conectado a SQLite. La recomendación con IA es una funcionalidad futura, **no implementada en este corte**.

## Requisitos

- Python 3.10 o superior.
- Flask 3.x.

## Cómo ejecutar en Windows

1. Extrae este ZIP en una carpeta.
2. Abre la terminal en la carpeta donde está `app.py`.
3. Ejecuta:

```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

4. Abre http://127.0.0.1:5000 en el navegador.

En macOS/Linux: `python3 -m venv .venv`, `source .venv/bin/activate`, `pip install -r requirements.txt`, `python app.py`.

## Qué hace

- **Create:** registrar un smartwatch.
- **Read:** consultar el catálogo.
- **Update:** editar datos y características.
- **Delete:** eliminar un smartwatch (confirmación previa).
- Validaciones de campos y claves foráneas activas.

## Modelo de datos

- `categorias` (1:N con `smartwatches`).
- `smartwatches` (entidad principal del CRUD).
- `caracteristicas` (catálogo de funciones).
- `smartwatch_caracteristicas` (relación N:M).

El esquema está en `schema.sql`; la base inicial en `jmatch.db`.

## Demostración para la profesora

1. Abrir el catálogo y mostrar su estado inicial.
2. Crear un smartwatch con nombre, modelo, categoría y precio.
3. Verificar que aparece en el listado.
4. Editar el precio o una característica y guardar.
5. Eliminarlo y confirmar que desapareció.
6. Abrir `app.py` y explicar una ruta y una consulta SQL.

## Seguridad y límites

Este prototipo es para **uso local y académico**. No incluye autenticación, CSRF ni configuración de producción. No publicarlo en Internet sin implementar estas medidas y cambiar la clave secreta. Las características de los relojes deben verificarse antes de registrarse. No usar la base de datos de ejemplo como evidencia de especificaciones comerciales.

## Bitácora IA

Registrar los prompts **exactos**, fechas, respuestas y decisiones reales; no inventar registros. Documentar un error real encontrado y su corrección.

## GitHub

Crear un repositorio nuevo y realizar commits por etapas (modelo, CRUD, interfaz, README). No afirmar que ya está publicado hasta subirlo y comprobar la URL.
