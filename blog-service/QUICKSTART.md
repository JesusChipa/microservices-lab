# Blog Service - Quick Start 🚀

## Iniciar Servicio

```bash
# 1. Construir e iniciar servicios
docker-compose up -d --build blog

# 2. Ejecutar migraciones
docker-compose exec blog python manage.py makemigrations
docker-compose exec blog python manage.py migrate

# 3. Cargar datos de ejemplo
docker-compose exec blog python manage.py seed_blog

# 4. (Opcional) Crear superusuario para admin
docker-compose exec blog python manage.py createsuperuser
```

## Probar Endpoints

### Health Check
```bash
curl http://localhost:8001/healthz
```

### Listar Categorías (cacheado 60s)
```bash
curl http://localhost:8001/api/categories/
```

### Listar Posts (paginado, 10 por página)
```bash
curl http://localhost:8001/api/posts/
curl http://localhost:8001/api/posts/?page=2
```

### Buscar Posts
```bash
curl "http://localhost:8001/api/posts/?search=python"
curl "http://localhost:8001/api/posts/?search=docker"
```

### Detalle de Post (cacheado 60s)
```bash
curl http://localhost:8001/api/posts/1/
curl http://localhost:8001/api/posts/introduction-to-python/
```

## Ver Logs
```bash
docker-compose logs -f blog
```

## Detener Servicio
```bash
docker-compose stop blog
```

## Reiniciar Servicio
```bash
docker-compose restart blog
```

## Acceder al Admin Panel
1. Crear superusuario (ver arriba)
2. Ir a: http://localhost:8001/admin/
3. Login con credenciales

## Datos de Seed
- **5 categorías:** Technology, Programming, Web Development, Data Science, DevOps
- **3 autores:** Alice Johnson, Bob Smith, Carol Williams  
- **30 posts:** 24 publicados + 6 borradores

## Servicios Relacionados
- **PostgreSQL:** localhost:5432 (DB compartida: `main_db`)
- **Redis:** localhost:6379 (caché)
- **Auth Service:** localhost:8000 (no conectado aún)

## Próximos Pasos
1. ✅ Servicio corriendo y probado
2. ⏳ Conectar autenticación JWT con Auth Service
3. ⏳ Endpoints protegidos (crear/editar posts)
4. ⏳ Frontend consumiendo la API

## Estructura de URLs
- `/healthz` - Health check
- `/api/categories/` - Lista categorías
- `/api/posts/` - Lista posts (con ?search= y ?page=)
- `/api/posts/{id}/` - Detalle por ID
- `/api/posts/{slug}/` - Detalle por slug
- `/admin/` - Django admin panel

## Caché Redis
- Lista de categorías: TTL 60s
- Detalle de posts: TTL 60s
- Limpiar caché: `docker-compose exec blog python manage.py shell` → `from django.core.cache import cache; cache.clear()`

## Logs Estructurados
Cada request se loguea en JSON:
```json
{"method": "GET", "path": "/api/posts/", "status": 200, "duration_ms": 45.23}
```

## Documentación Completa
Ver `README.md` para documentación completa con ejemplos de respuestas JSON y detalles técnicos.

Ver `openapi.yaml` para el contrato OpenAPI 3.0 completo de la API.
