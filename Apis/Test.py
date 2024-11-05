from flask import Flask, jsonify, request

app = Flask(__name__)

alumnos = [
    {"id": 1, "name": "Juan Perez", "carrera": "software", "age": 20},
    {"id": 2, "name": "Maria Lopez", "carrera": "software", "age": 22},
]

@app.route('/alumnos', methods=['GET'])
def get_alumnos():
    return jsonify(alumnos)

@app.route('/alumnos/<int:id>', methods=['GET'])
def get_alumno(id):
    alumno = next((alumno for alumno in alumnos if alumno['id'] == id), None)
    if alumno:
        return jsonify(alumno)
    else:
        return jsonify({'error': 'Alumno no encontrado'}), 404

@app.route('/alumnos', methods=['POST'])
def create_alumno():
    new_alumno = request.get_json()
    if not new_alumno or not all(key in new_alumno for key in ("id", "name", "carrera", "age")):
        return jsonify({'error': 'Datos incompletos'}), 400
    alumnos.append(new_alumno)
    return jsonify({'message': 'Alumno creado exitosamente'}), 201

@app.route('/alumnos/<int:id>', methods=['PUT'])
def update_alumno(id):
    alumno = next((alumno for alumno in alumnos if alumno['id'] == id), None)
    if alumno:
        dato = request.get_json()
        if not dato:
            return jsonify({'error': 'Datos incompletos'}), 400
        alumno.update(dato)
        return jsonify(alumno)
    else:
        return jsonify({'error': 'Alumno no encontrado'}), 404

@app.route('/alumnos/<int:id>', methods=['DELETE'])
def delete_alumno(id):
    global alumnos
    alumno = next((alumno for alumno in alumnos if alumno['id'] == id), None)
    if alumno:
        alumnos = [alumno for alumno in alumnos if alumno['id'] != id]
        return jsonify({'message': 'Alumno eliminado exitosamente'}), 200
    else:
        return jsonify({'error': 'Alumno no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)