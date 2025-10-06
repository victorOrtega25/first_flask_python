from flask import Flask, jsonify, request

app = Flask(__name__)

tareas = [
    {"id": 1, "titulo": "Aprender Python", "completada": True},
    {"id": 2, "titulo": "Aprender Flask", "completada": False}
]

@app.route('/')
def hola_mundo():
    return "Bienvenido a mi API de Tareas!"

@app.route('/tareas')
def obtener_tareas():
    return jsonify({"tareas": tareas})

@app.route('/tareas/<int:tarea_id>', methods=['GET'])
def obtener_tarea(id):
    tarea = next((t for t in tareas if t["id"] == id), None)
    if tarea is None:
        return jsonify({"error": "Tarea no encontrada"}), 404
    return jsonify(tarea)

@app.route('/tareas', methods=['POST'])
def crear_tarea():
    if not request.json or not "titulo" in request.json:
        return jsonify({"error": "Datos incorrectos"}), 400
    tarea = {
        "id": tareas[-1]["id"] + 1,
        "titulo": request.json["titulo"],
        "completada": False
    }
    tareas.append(tarea)
    return jsonify(tarea), 201

@app.route('/tareas/<int:tarea_id>', methods=['PUT'])
def actualizar_tarea(tarea_id):
    tarea = next((t for t in tareas if t["id"] == tarea_id), None)
    if tarea is None:
        return jsonify({"error": "Tarea no encontrada"}), 404
    if not request.json:
        return jsonify({"error": "Petición vacía"}), 400

    tarea['titulo'] = request.json.get('titulo', tarea['titulo'])
    
    tarea['completada'] = request.json.get('completada', tarea['completada'])
    return jsonify({"tarea": tarea})

@app.route('/tareas/<int:tarea_id>', methods=['DELETE'])
def eliminar_tarea(tarea_id):
    tarea = next((t for t in tareas if t["id"] == tarea_id), None)
    if tarea is None:
        return jsonify({"error": "Tarea no encontrada"}), 404
    tareas.remove(tarea)
    return jsonify({"resultado": True})

if __name__ == '__main__':
    app.run(debug=True)