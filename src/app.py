"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Instanciar la familia Jackson
jackson_family = FamilyStructure("Jackson")

# Manejo de errores personalizados
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Sitemap para ver rutas disponibles
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# 1) Obtener todos los miembros de la familia
@app.route('/members', methods=['GET'])
def get_all_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2) Obtener un miembro específico por ID
@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member:
            return jsonify(member), 200
        else:
            return jsonify({"error": "Miembro no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3) Agregar un nuevo miembro
@app.route('/members', methods=['POST'])
def add_member():
    try:
        data = request.get_json()

        # Validar que el cliente envíe los campos requeridos
        required_fields = ["first_name", "age", "lucky_numbers"]
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": "Faltan campos requeridos"}), 400
        
        # Validar tipo y valor de age (debe ser > 0)
        if not isinstance(data["age"], int) or data["age"] <= 0:
            return jsonify({"error": "La edad debe ser un entero mayor a 0"}), 400
        
        # Validar lucky_numbers sea lista
        if not isinstance(data["lucky_numbers"], list):
            return jsonify({"error": "lucky_numbers debe ser una lista"}), 400

        # Preparar el miembro a agregar (sin last_name, se agrega automáticamente)
        member_to_add = {
            "first_name": data["first_name"],
            "age": data["age"],
            "lucky_numbers": data["lucky_numbers"]
        }
        # Si envían un id explícito, usarlo
        if "id" in data:
            member_to_add["id"] = data["id"]

        # Agregar el miembro a la familia
        new_member = jackson_family.add_member(member_to_add)

        # Retornar el miembro agregado con ID y last_name
        return jsonify(new_member), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 4) Eliminar un miembro por ID
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        deleted = jackson_family.delete_member(member_id)
        if deleted:
            return jsonify({"done": True}), 200
        else:
            return jsonify({"error": "Miembro no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
