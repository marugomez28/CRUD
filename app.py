import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db_url = os.getenv('DATABASE_URL', 'sqlite:///data/sqlite_db.db')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

with app.app_context():
    db.create_all()

# --- RUTA FRONTEND ---
@app.route('/')
def index():
    return render_template('index.html')

# --- RUTAS CRUD (API) ---
@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    nuevo_usuario = Usuario(nombre=data['nombre'], email=data['email'])
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({"mensaje": "Usuario creado"}), 201

@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    usuarios = Usuario.query.all()
    lista = [{"id": u.id, "nombre": u.nombre, "email": u.email} for u in usuarios]
    return jsonify(lista), 200

@app.route('/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    data = request.get_json()
    usuario = db.session.get(Usuario, id)
    if not usuario:
        return jsonify({"mensaje": "No encontrado"}), 404
    usuario.nombre = data['nombre']
    usuario.email = data['email']
    db.session.commit()
    return jsonify({"mensaje": "Usuario actualizado"}), 200

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    usuario = db.session.get(Usuario, id)
    if not usuario:
        return jsonify({"mensaje": "No encontrado"}), 404
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"mensaje": "Usuario eliminado"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)