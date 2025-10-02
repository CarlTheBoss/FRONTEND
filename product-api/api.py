from flask import Flask, jsonify

app = Flask(__name__)

# Datos de prueba
productos = [
    {"id": 1, "nombre": "Taladro", "precio": 120.50, "stock": 10},
    {"id": 2, "nombre": "Martillo", "precio": 25.00, "stock": 50},
    {"id": 3, "nombre": "Destornillador", "precio": 10.00, "stock": 100},
]

# Ruta principal para test
@app.route('/')
def home():
    return "API de Productos funcionando ✅"

# Obtener todos los productos
@app.route('/productos', methods=['GET'])
def get_productos():
    return jsonify(productos)

# Obtener un producto por ID
@app.route('/productos/<int:id>', methods=['GET'])
def get_producto(id):
    producto = next((p for p in productos if p["id"] == id), None)
    if producto:
        return jsonify(producto)
    return jsonify({"error": "Producto no encontrado"}), 404


if __name__ == '__main__':
    app.run(debug=True)
