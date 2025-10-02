# Sistema de Gestión de Productos - Frontend

Sistema completo que integra 4 microservicios diferentes (Python, Node.js, PHP y Java) para gestionar productos, categorías, marcas y unidades.

## 🏗️ Arquitectura

El sistema está compuesto por:

1. **API Gateway (Python Flask)** - Puerto 5000
   - Actúa como punto de entrada único
   - Consume las 4 APIs backend
   
2. **API Categorías (Python)** - Puerto 3001
3. **API Marcas (Node.js)** - Puerto 3002
4. **API Unidades (PHP)** - Puerto 3003
5. **API Productos (Java Spring Boot)** - Puerto 8080
6. **Frontend (Vue.js)** - Servidor de desarrollo

## 📋 Requisitos Previos

- Python 3.8+
- Node.js 16+
- PHP 7.4+
- Java 11+
- npm o yarn

## 🚀 Instalación

### 1. Instalar dependencias del API Gateway (Python)

```bash
cd product-api
pip install -r requirements.txt
```

### 2. Configurar las APIs backend

Asegúrate de que las siguientes APIs estén corriendo:

- **Python API (Categorías)**: http://localhost:3001/
- **Node.js API (Marcas)**: http://localhost:3002/
- **PHP API (Unidades)**: http://localhost:3003/
- **Java API (Productos)**: https://8080-firebase-product-service-java-1759371536787.cluster-fsmcisrvfbb5cr5mvra3hr3qyg.cloudworkstations.dev/api/v1/products

## ▶️ Ejecución

### 1. Iniciar el API Gateway (Python)

```bash
cd product-api
python api.py
```

El gateway estará disponible en: http://localhost:5000

### 2. Iniciar el Frontend

```bash
# En el directorio raíz del proyecto FRONTEND
npm install
npm run dev
```

El frontend estará disponible en: http://localhost:5173 (o el puerto que Vite asigne)

## 🔌 Endpoints del API Gateway

### Información general
- `GET /` - Información del gateway y endpoints disponibles
- `GET /health` - Estado de salud de todas las APIs

### Categorías
- `GET /categorias` - Obtener todas las categorías

### Marcas
- `GET /marcas` - Obtener todas las marcas

### Unidades
- `GET /unidades` - Obtener todas las unidades

### Productos
- `GET /productos` - Obtener todos los productos
- `GET /productos/<id>` - Obtener un producto por ID
- `POST /productos` - Crear un nuevo producto

### Obtener todo
- `GET /all` - Obtener datos de todas las APIs en una sola petición

## 📦 Estructura de Datos

### Producto (Java API)
```json
{
  "id_pro": 1,
  "nom_pro": "Taladro Eléctrico",
  "pre_pro": 150.50,
  "id_uni": 1,
  "id_marca": 2,
  "id_cat": 3,
  "stk_pro": 25.0,
  "estado": "Y"
}
```

### Categoría
```json
{
  "id_cat": 1,
  "nom_cat": "Herramientas"
}
```

### Marca
```json
{
  "id_marca": 1,
  "nom_marca": "DeWalt"
}
```

### Unidad
```json
{
  "id_uni": 1,
  "nom_uni": "Unidad"
}
```

## 🛠️ Tecnologías Utilizadas

- **Frontend**: Vue.js 3 (Composition API)
- **API Gateway**: Flask + Flask-CORS + Requests
- **Estilos**: CSS3 (Grid, Flexbox, Gradientes)
- **HTTP Client**: Fetch API

## 🎨 Características del Frontend

- ✅ Diseño responsive (móvil y escritorio)
- ✅ Búsqueda en tiempo real de productos
- ✅ Tarjetas de estadísticas
- ✅ Vista de grid para productos
- ✅ Integración con múltiples APIs
- ✅ Manejo de errores
- ✅ Animaciones y transiciones suaves

## 🔧 Configuración de URLs

Si necesitas cambiar las URLs de las APIs, edita el archivo `product-api/api.py`:

```python
API_CATEGORIAS = "http://localhost:3001/"
API_MARCAS = "http://localhost:3002/"
API_UNIDADES = "http://localhost:3003/"
API_PRODUCTOS = "https://..."
```

Y también en `src/main.js` si deseas que el frontend consuma directamente las APIs:

```javascript
const response = await fetch('http://localhost:3001/');
```

## 🐛 Solución de Problemas

### Error de CORS
Si encuentras errores de CORS, asegúrate de que todas las APIs backend tengan CORS habilitado.

### Timeout de conexión
El gateway tiene un timeout de 5 segundos. Si una API tarda más, aumenta el valor en `api.py`:
```python
response = requests.get(API_PRODUCTOS, timeout=10)  # 10 segundos
```

### API no disponible
Verifica el estado de las APIs usando:
```bash
curl http://localhost:5000/health
```

## 📝 Notas

- El API Gateway actúa como proxy reverso, facilitando la comunicación entre el frontend y múltiples backends
- Todas las peticiones son asíncronas para mejor rendimiento
- El sistema maneja errores de conexión de forma elegante

## 👨‍💻 Desarrollo

Para desarrollo local, puedes usar el modo debug:

```bash
# Python API Gateway
python api.py  # Debug mode está activado por defecto
```

## 📄 Licencia

Este proyecto es para fines educativos.