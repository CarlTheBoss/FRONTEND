from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__, static_folder=".")
CORS(app)

# Configuración para producción
app.config["JSON_AS_ASCII"] = False
app.config["JSON_SORT_KEYS"] = False

# URLs de las APIs
API_CATEGORIAS = "http://localhost:3001/"  # Python
API_MARCAS = "https://apimarcas.onrender.com/api/marcas"  # Node.js en Render
API_UNIDADES = "https://php-75bb6.wasmer.app/index.php?api=1"  # PHP en Wasmer
API_PRODUCTOS = "https://8080-firebase-product-service-java-1759371536787.cluster-fsmcisrvfbb5cr5mvra3hr3qyg.cloudworkstations.dev/api/v1/products"  # Java


# Ruta principal - Servir el index.html
@app.route("/")
def home():
    return send_from_directory(".", "index.html")


# Servir archivos estáticos (JS)
@app.route("/src/<path:path>")
def serve_static(path):
    return send_from_directory("src", path)


# API Info
@app.route("/api")
def api_info():
    return jsonify(
        {
            "message": "API Gateway funcionando ✅",
            "endpoints": {
                "categorias": "/categorias",
                "marcas": "/marcas",
                "unidades": "/unidades",
                "productos": "/productos",
                "all_data": "/all",
                "health": "/health",
            },
        }
    )


# ==================== CATEGORÍAS ====================
@app.route("/categorias", methods=["GET"])
def get_categorias():
    try:
        response = requests.get(API_CATEGORIAS, timeout=5)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify(
            {"error": f"Error al conectar con API de Categorías: {str(e)}"}
        ), 500


# ==================== MARCAS ====================
@app.route("/marcas", methods=["GET"])
def get_marcas():
    try:
        response = requests.get(API_MARCAS, timeout=5)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error al conectar con API de Marcas: {str(e)}"}), 500


# ==================== UNIDADES ====================
@app.route("/unidades", methods=["GET"])
def get_unidades():
    try:
        response = requests.get(API_UNIDADES, timeout=5)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify(
            {"error": f"Error al conectar con API de Unidades: {str(e)}"}
        ), 500


# ==================== PRODUCTOS ====================
@app.route("/productos", methods=["GET"])
def get_productos():
    try:
        response = requests.get(API_PRODUCTOS, timeout=5)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify(
            {"error": f"Error al conectar con API de Productos: {str(e)}"}
        ), 500


@app.route("/productos/<int:id>", methods=["GET"])
def get_producto(id):
    try:
        response = requests.get(f"{API_PRODUCTOS}/{id}", timeout=5)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify(
            {"error": f"Error al conectar con API de Productos: {str(e)}"}
        ), 500


@app.route("/productos", methods=["POST"])
def create_producto():
    try:
        data = request.get_json()
        response = requests.post(API_PRODUCTOS, json=data, timeout=5)
        response.raise_for_status()
        return jsonify(response.json()), 201
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error al crear producto: {str(e)}"}), 500


# ==================== OBTENER TODO ====================
@app.route("/all", methods=["GET"])
def get_all_data():
    """Endpoint para obtener todos los datos de las 4 APIs en una sola petición"""
    result = {
        "categorias": [],
        "marcas": [],
        "unidades": [],
        "productos": [],
        "errors": [],
    }

    # Intentar obtener categorías
    try:
        response = requests.get(API_CATEGORIAS, timeout=5)
        response.raise_for_status()
        result["categorias"] = response.json()
    except requests.exceptions.RequestException as e:
        result["errors"].append(f"Categorías: {str(e)}")

    # Intentar obtener marcas
    try:
        response = requests.get(API_MARCAS, timeout=5)
        response.raise_for_status()
        result["marcas"] = response.json()
    except requests.exceptions.RequestException as e:
        result["errors"].append(f"Marcas: {str(e)}")

    # Intentar obtener unidades
    try:
        response = requests.get(API_UNIDADES, timeout=5)
        response.raise_for_status()
        result["unidades"] = response.json()
    except requests.exceptions.RequestException as e:
        result["errors"].append(f"Unidades: {str(e)}")

    # Intentar obtener productos
    try:
        response = requests.get(API_PRODUCTOS, timeout=5)
        response.raise_for_status()
        result["productos"] = response.json()
    except requests.exceptions.RequestException as e:
        result["errors"].append(f"Productos: {str(e)}")

    return jsonify(result)


# ==================== HEALTH CHECK ====================
@app.route("/health", methods=["GET"])
def health_check():
    """Verifica el estado de todas las APIs"""
    status = {"gateway": "OK", "apis": {}}

    # Check Categorías
    try:
        response = requests.get(API_CATEGORIAS, timeout=2)
        status["apis"]["categorias"] = "OK" if response.status_code == 200 else "ERROR"
    except:
        status["apis"]["categorias"] = "OFFLINE"

    # Check Marcas
    try:
        response = requests.get(API_MARCAS, timeout=2)
        status["apis"]["marcas"] = "OK" if response.status_code == 200 else "ERROR"
    except:
        status["apis"]["marcas"] = "OFFLINE"

    # Check Unidades
    try:
        response = requests.get(API_UNIDADES, timeout=2)
        status["apis"]["unidades"] = "OK" if response.status_code == 200 else "ERROR"
    except:
        status["apis"]["unidades"] = "OFFLINE"

    # Check Productos
    try:
        response = requests.get(API_PRODUCTOS, timeout=2)
        status["apis"]["productos"] = "OK" if response.status_code == 200 else "ERROR"
    except:
        status["apis"]["productos"] = "OFFLINE"

    return jsonify(status)


if __name__ == "__main__":
    # Obtener configuración desde variables de entorno
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV", "production") != "production"
    host = os.environ.get("HOST", "0.0.0.0")

    print(f"🚀 Iniciando servidor en {host}:{port}")
    print(f"🔧 Modo: {'Development' if debug else 'Production'}")
    print(f"🌐 APIs configuradas:")
    print(f"   - Categorías: {API_CATEGORIAS}")
    print(f"   - Marcas: {API_MARCAS}")
    print(f"   - Unidades: {API_UNIDADES}")
    print(f"   - Productos: {API_PRODUCTOS[:50]}...")

    app.run(host=host, port=port, debug=debug)
