# 🐳 Guía de Docker - Sistema de Gestión de Productos

Esta guía te ayudará a desplegar el sistema usando Docker y Docker Compose.

## 📋 Requisitos Previos

- Docker instalado (versión 20.10 o superior)
- Docker Compose instalado (versión 2.0 o superior)

### Verificar instalación

```bash
docker --version
docker-compose --version
```

---

## 🚀 Inicio Rápido

### 1. Construir y ejecutar con Docker Compose

```bash
# Construir la imagen y ejecutar el contenedor
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f gateway
```

La aplicación estará disponible en: **http://localhost:5000**

### 2. Detener el servicio

```bash
docker-compose down
```

### 3. Reconstruir después de cambios

```bash
docker-compose up -d --build
```

---

## 🔧 Comandos Docker Útiles

### Construcción manual

```bash
# Construir la imagen
docker build -t product-gateway:latest .

# Ejecutar el contenedor
docker run -d \
  --name product-gateway \
  -p 5000:5000 \
  product-gateway:latest
```

### Gestión de contenedores

```bash
# Ver contenedores en ejecución
docker ps

# Ver todos los contenedores
docker ps -a

# Detener contenedor
docker stop product-gateway

# Eliminar contenedor
docker rm product-gateway

# Ver logs
docker logs -f product-gateway

# Entrar al contenedor (shell)
docker exec -it product-gateway /bin/bash
```

### Gestión de imágenes

```bash
# Listar imágenes
docker images

# Eliminar imagen
docker rmi product-gateway:latest

# Limpiar imágenes no utilizadas
docker image prune -a
```

---

## 📊 Verificar el Estado

### Health Check

```bash
# Verificar estado del contenedor
docker inspect product-gateway | grep -A 5 Health

# O usar curl
curl http://localhost:5000/health
```

### Respuesta esperada

```json
{
  "gateway": "OK",
  "apis": {
    "categorias": "OFFLINE",
    "marcas": "OK",
    "unidades": "OK",
    "productos": "OK"
  }
}
```

---

## 🌐 Variables de Entorno

Puedes personalizar las URLs de las APIs editando el archivo `docker-compose.yml`:

```yaml
environment:
  - FLASK_APP=api.py
  - FLASK_ENV=production
  - PORT=5000
  - HOST=0.0.0.0
```

O pasarlas directamente en el comando `docker run`:

```bash
docker run -d \
  --name product-gateway \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e PORT=5000 \
  product-gateway:latest
```

---

## 📦 Estructura del Contenedor

```
/app/
├── api.py              # Aplicación Flask
├── index.html          # Frontend
├── src/
│   └── main.js        # JavaScript
└── requirements.txt    # Dependencias Python
```

---

## 🔍 Debugging

### Ver logs en tiempo real

```bash
docker-compose logs -f gateway
```

### Inspeccionar el contenedor

```bash
# Ver información del contenedor
docker inspect product-gateway

# Ver procesos dentro del contenedor
docker top product-gateway

# Ver uso de recursos
docker stats product-gateway
```

### Acceder al contenedor

```bash
# Abrir shell en el contenedor
docker exec -it product-gateway /bin/bash

# O usar sh si bash no está disponible
docker exec -it product-gateway sh

# Ejecutar un comando específico
docker exec product-gateway python -c "import requests; print(requests.__version__)"
```

---

## 🌍 Despliegue en Producción

### Optimizaciones recomendadas

1. **Usar imagen multi-stage** (para reducir tamaño):

```dockerfile
# Stage 1: Build
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY product-api/ ./
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "api.py"]
```

2. **Usar gunicorn en producción**:

Agregar a `requirements.txt`:
```
gunicorn==21.2.0
```

Modificar CMD en Dockerfile:
```dockerfile
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "api:app"]
```

3. **Configurar health check**:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1
```

---

## 🐋 Docker Hub

### Subir imagen a Docker Hub

```bash
# Login en Docker Hub
docker login

# Etiquetar la imagen
docker tag product-gateway:latest tuusuario/product-gateway:latest
docker tag product-gateway:latest tuusuario/product-gateway:v1.0.0

# Subir la imagen
docker push tuusuario/product-gateway:latest
docker push tuusuario/product-gateway:v1.0.0

# Descargar y ejecutar desde Docker Hub
docker pull tuusuario/product-gateway:latest
docker run -d -p 5000:5000 tuusuario/product-gateway:latest
```

---

## 🔒 Seguridad

### Buenas prácticas

1. **No ejecutar como root**:

```dockerfile
# Crear usuario no-root
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

USER appuser
```

2. **Escanear vulnerabilidades**:

```bash
# Usar Docker Scout
docker scout cves product-gateway:latest

# O usar Trivy
trivy image product-gateway:latest
```

3. **Limitar recursos**:

```yaml
services:
  gateway:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

---

## 🚢 Despliegue en Cloud

### Render.com

```bash
# Render detecta automáticamente el Dockerfile
# Solo necesitas:
# 1. Conectar tu repositorio
# 2. Seleccionar "Docker" como entorno
# 3. Configurar el puerto 5000
```

### Railway.app

```bash
# Railway también detecta automáticamente el Dockerfile
railway up
```

### Google Cloud Run

```bash
# Construir y subir
gcloud builds submit --tag gcr.io/PROJECT-ID/product-gateway
gcloud run deploy --image gcr.io/PROJECT-ID/product-gateway --platform managed
```

### AWS ECS/Fargate

```bash
# Subir a ECR
aws ecr create-repository --repository-name product-gateway
docker tag product-gateway:latest AWS_ACCOUNT.dkr.ecr.REGION.amazonaws.com/product-gateway
docker push AWS_ACCOUNT.dkr.ecr.REGION.amazonaws.com/product-gateway
```

---

## 🐛 Solución de Problemas

### El contenedor no inicia

```bash
# Ver logs completos
docker logs product-gateway

# Ver últimas 50 líneas
docker logs --tail 50 product-gateway

# Verificar que el puerto no esté en uso
lsof -i :5000
```

### Error de permisos

```bash
# Dar permisos al directorio
chmod -R 755 product-api/
```

### Error de conexión a APIs externas

```bash
# Verificar conectividad desde el contenedor
docker exec product-gateway curl -I https://apimarcas.onrender.com/api/marcas
```

### Contenedor consume mucha memoria

```bash
# Ver uso de recursos
docker stats product-gateway

# Limitar memoria
docker update --memory="512m" product-gateway
```

---

## 📚 Recursos Adicionales

- [Documentación de Docker](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Flask Deployment Options](https://flask.palletsprojects.com/en/2.3.x/deploying/)

---

## 📞 Soporte

Si encuentras algún problema:

1. Verifica los logs: `docker-compose logs -f`
2. Comprueba el health check: `curl http://localhost:5000/health`
3. Revisa la documentación en `README.md`

---

**Última actualización:** 2024  
**Versión:** 1.0.0