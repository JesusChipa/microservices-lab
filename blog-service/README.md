# Blog Service 📝

Microservicio de blog construido con Django + DRF + PostgreSQL + Redis + Docker.

**Puerto:** 8001

## Stack Tecnológico

- **Django 5.0** - Framework web
- **Django REST Framework 3.15** - API REST
- **PostgreSQL** - Base de datos
- **Redis** - Cache
- **Docker** - Containerización
- **Gunicorn** - WSGI server

## Características

✅ **Modelos:**
- `Category` - Categorías de posts
- `Author` - Autores (local por ahora, enlace a Auth después)
- `Post` - Posts con título, contenido, autor, categoría, estado

✅ **Endpoints públicos:**
- `GET /api/categories` - Lista categorías activas
- `GET /api/posts?search=&page=` - Lista posts con búsqueda y paginación
- `GET /api/posts/{id|slug}` - Detalle de post

✅ **Cache Redis:**
- Categories list cacheado 60s
- Post detail cacheado 60s

✅ **Observabilidad:**
- `GET /healthz` - Health check (DB + Redis)
- Logging estructurado JSON por request

✅ **Autenticación (preparado para futuro):**
- Middleware que registra headers `Authorization`
- Listo para validar JWT cuando se conecte al Auth Service

## Instalación y Ejecución

### Con Docker (Recomendado)

1. **Construir e iniciar servicios:**
   ```bash
   docker-compose up --build blog
   ```

2. **Ejecutar migraciones:**
   ```bash
   docker-compose exec blog python manage.py migrate
   ```

3. **Cargar datos de ejemplo:**
   ```bash
   docker-compose exec blog python manage.py seed_blog
   ```

4. **Crear superusuario (opcional):**
   ```bash
   docker-compose exec blog python manage.py createsuperuser
   ```

El servicio estará disponible en: `http://localhost:8001`

### Sin Docker (Desarrollo local)

1. **Instalar dependencias:**
   ```bash
   cd blog-service
   pip install -r requirements.txt
   ```

2. **Configurar variables de entorno:**
   ```bash
   export DB_HOST=localhost
   export DB_NAME=main_db
   export DB_USER=devuser
   export DB_PASS=devpass
   export REDIS_HOST=localhost
   export REDIS_PORT=6379
   export DEBUG=1
   ```

3. **Ejecutar migraciones:**
   ```bash
   python manage.py migrate
   ```

4. **Cargar datos:**
   ```bash
   python manage.py seed_blog
   ```

5. **Iniciar servidor:**
   ```bash
   python manage.py runserver 8001
   ```

## Uso de la API

### 1. Health Check
```bash
curl http://localhost:8001/healthz
```

**Respuesta:**
```json
{
  "service": "blog-service",
  "status": "healthy",
  "checks": {
    "database": "ok",
    "redis": "ok"
  }
}
```

### 2. Listar Categorías
```bash
curl http://localhost:8001/api/categories/
```

**Respuesta:**
```json
[
  {
    "id": 1,
    "name": "Technology",
    "slug": "technology"
  },
  {
    "id": 2,
    "name": "Programming",
    "slug": "programming"
  }
]
```

### 3. Listar Posts (con paginación)
```bash
curl http://localhost:8001/api/posts/
```

**Respuesta:**
```json
{
  "count": 24,
  "next": "http://localhost:8001/api/posts/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Introduction to Python",
      "slug": "introduction-to-python",
      "excerpt": "Python is a powerful and versatile programming language...",
      "author": {
        "id": 1,
        "display_name": "Alice Johnson",
        "email": "alice@example.com"
      },
      "category": {
        "id": 1,
        "name": "Technology",
        "slug": "technology"
      },
      "published_at": "2025-10-23T18:00:00Z",
      "views": 0
    }
  ]
}
```

### 4. Buscar Posts
```bash
curl "http://localhost:8001/api/posts/?search=python"
```

### 5. Detalle de Post
```bash
curl http://localhost:8001/api/posts/1/
# O por slug:
curl http://localhost:8001/api/posts/introduction-to-python/
```

**Respuesta:**
```json
{
  "id": 1,
  "title": "Introduction to Python",
  "slug": "introduction-to-python",
  "body": "Python is a powerful and versatile programming language...\n\nLorem ipsum...",
  "author": {
    "id": 1,
    "display_name": "Alice Johnson",
    "email": "alice@example.com"
  },
  "category": {
    "id": 1,
    "name": "Technology",
    "slug": "technology"
  },
  "status": "published",
  "published_at": "2025-10-23T18:00:00Z",
  "views": 15,
  "created_at": "2025-10-23T17:00:00Z",
  "updated_at": "2025-10-23T18:30:00Z"
}
```

## Datos de Ejemplo (Seed)

El comando `seed_blog` crea:
- **5 categorías:** Technology, Programming, Web Development, Data Science, DevOps
- **3 autores:** Alice Johnson, Bob Smith, Carol Williams
- **30 posts:** 24 publicados, 6 borradores

## Estructura del Proyecto

```
blog-service/
├── blog_service/          # Proyecto Django
│   ├── settings.py        # Configuración
│   ├── urls.py            # URLs principales
│   └── wsgi.py
├── core/                  # Utilidades
│   ├── middleware.py      # Logging y Auth header
│   └── views.py           # Healthcheck
├── categories/            # App de categorías
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── authors/               # App de autores
│   ├── models.py
│   ├── serializers.py
│   └── admin.py
├── posts/                 # App de posts
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── management/
│       └── commands/
│           └── seed_blog.py
├── Dockerfile
├── requirements.txt
├── manage.py
├── openapi.yaml           # Contrato API
└── README.md
```

## Caché

El servicio usa **Redis** para cachear:

1. **Lista de categorías:** 60 segundos
   - Key: generado por Django cache framework
   - TTL: 60s

2. **Detalle de post:** 60 segundos
   - Key: generado por Django cache framework
   - TTL: 60s

Para limpiar caché manualmente:
```bash
docker-compose exec blog python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
```

## Logging

Todos los requests son logueados en formato JSON:

```json
{"method": "GET", "path": "/api/posts/", "status": 200, "duration_ms": 45.23}
```

## Próximos Pasos (Roadmap)

- [ ] Conectar autenticación JWT con Auth Service
- [ ] Validar tokens en middleware
- [ ] Endpoints protegidos para crear/editar posts
- [ ] Sistema de comentarios
- [ ] Tags para posts
- [ ] Likes/reactions
- [ ] Upload de imágenes

## Admin Panel

Acceso al panel de administración: `http://localhost:8001/admin/`

Crear superusuario:
```bash
docker-compose exec blog python manage.py createsuperuser
```

## Testing

```bash
docker-compose exec blog python manage.py test
```

## Licencia

MIT
