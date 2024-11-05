from flask import Flask, request, jsonify, send_from_directory
from flask_mysqldb import MySQL

app = Flask(__name__)

# Conexión por Xampp
# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'test'

mysql = MySQL(app)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/add')
def add():
    return send_from_directory('.', 'add_users.html')

@app.route('/update/<int:id>')
def update():
    return send_from_directory('.', 'update_users.html')

# Ruta para obtener todos los usuarios (GET)
@app.route('/users', methods=['GET'])
def get_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    results = cur.fetchall()
    cur.close()
    return jsonify(results)

# Ruta para agregar un nuevo usuario (CREATE)
@app.route('/add_users', methods=['POST'])
def add_user():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Usuario agregado exitosamente!'}), 201

# Ruta para editar un usuario (UPDATE)
@app.route('/update_users/<int:id>', methods=['PUT'])
def update_user(id):
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET name=%s, email=%s, password=%s WHERE id=%s", (name, email, password, id))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Usuario actualizado exitosamente!'})

# Ruta para eliminar un usuario (DELETE)
@app.route('/delete_users/<int:id>', methods=['DELETE'])
def delete_user(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Usuario eliminado exitosamente"})

if __name__ == '__main__':
    app.run(debug=True)
