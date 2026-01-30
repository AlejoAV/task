# Ticket Task App

API REST para gestión de Tareas y Categorías desarrollada en Django REST Framework.

## Requisitos

- Docker instalado en su sistema.

## Instalación y Ejecución con Docker

Siga estos pasos para ejecutar la aplicación utilizando Docker.

### 1. Construir la imagen

Construya la imagen de Docker con el siguiente comando:

```bash
docker build -t taskapp .
```

### 2. Crear Superusuario (Opcional)

Si desea crear un usuario administrador antes de iniciar el servidor (esto ejecutará las migraciones automáticamente si no existen):

```bash
docker run --rm -it -v $(pwd):/app taskapp sh -c "python manage.py migrate && python manage.py createsuperuser"
```

### 3. Iniciar el Servidor

El contenedor está configurado para ejecutar automáticamente las pruebas unitarias y las migraciones al inicio.

Para asegurar que los datos persistan en su máquina local, monte el directorio actual en el contenedor.

```bash
docker run -p 8000:8000 --env-file .env -v $(pwd):/app taskapp
```

La aplicación estará disponible en `http://localhost:8000`.

Para ejecutar el servidor en **segundo plano** (modo detached), añada la opción `-d`:

```bash
docker run -d -p 8000:8000 --env-file .env -v $(pwd):/app taskapp
```

**Nota sobre comportamiento:** 
Al iniciar, el contenedor ejecutará secuencialmente:
1.  Pruebas Unitarias (`pytest`). (Si fallan, se detiene).
2.  Migraciones de Base de Datos (`migrate`).
3.  Servidor Django (`runserver`).

### 4. Ejecutar Pruebas (Manual)

Las pruebas se ejecutan automáticamente al iniciar, pero si desea ejecutarlas manualmente sin levantar el servidor:

```bash
docker run --rm taskapp pytest
```

## Gestión del Contenedor

### Detener el Servidor

Si está ejecutando el servidor en primer plano, simplemente presione `Ctrl + C`.

Si lo ejecutó en segundo plano (`-d`), busque el ID del contenedor y deténgalo:

```bash
docker ps
docker stop <CONTAINER_ID>
```

### Eliminar el Contenedor

Para eliminar el contenedor una vez detenido (útil si no usó el flag `--rm`):

```bash
docker rm <CONTAINER_ID>
```

Para ver los contenedores detenidos y obtener su ID:

```bash
docker ps -a
```

### Eliminar la Imagen

Para eliminar la imagen de Docker creada (liberar espacio):

```bash
docker rmi taskapp
```

### Borrar Datos y Registros

Para eliminar la base de datos y comenzar desde cero (borrar todos los registros):

1.  Detenga cualquier contenedor en ejecución.
2.  Elimine el archivo de base de datos local:

```bash
rm task/db.sqlite3
```

La próxima vez que inicie el servidor, se creará una base de datos nueva y vacía.

## Configuración

Puede configurar la aplicación utilizando las siguientes variables de entorno. Puede definirlas en un archivo `.env` (como se muestra arriba) o pasarlas individualmente con el flag `-e`.

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `SECRET_KEY` | Llave secreta de Django | `django-insecure...` |
| `DEBUG` | Modo depuración (`True`/`False`) | `True` |
| `ALLOWED_HOSTS` | Hosts permitidos (sep. por comas) | `[]` |
| `JWT_TOKEN` | Token secreto para JWT | `12345` |

Ejemplo pasando variables individuales:

```bash
docker run -p 8000:8000 -e DEBUG=False -e ALLOWED_HOSTS=localhost taskapp
```

## Documentación de API

La documentación interactiva de la API está disponible en las siguientes rutas (una vez iniciado el servidor):

- **Swagger UI**: `/api/schema/swagger-ui/`
- **Redoc**: `/api/schema/redoc/`
- **Esquema OpenAPI (YAML)**: `/api/schema/`

### Colección Postman

Si prefiere utilizar Postman, encontrará una colección lista para importar con todos los endpoints configurados en:

`doc/task.postman_collection.json`

## Endpoints Principales

- `/api/login/` (POST): Autenticación JWT.
- `/api/categories/` (CRUD): Gestión de categorías.
- `/api/tasks/` (CRUD): Gestión de tareas.
