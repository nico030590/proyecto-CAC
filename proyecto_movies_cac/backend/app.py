from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/cac_movies'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configurar CORS para permitir todas las solicitudes
CORS(app)

db = SQLAlchemy(app)

# Modelo de Usuario
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contraseña = db.Column(db.String(100), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())

# Modelo de Película
class Pelicula(db.Model):
    __tablename__ = 'peliculas'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    año = db.Column(db.Integer)
    genero = db.Column(db.String(50))
    director = db.Column(db.String(100))
    actores = db.Column(db.String(255))
    imagen_url = db.Column(db.String(255))
    trailer_url = db.Column(db.String(255))
    fecha_agregado = db.Column(db.DateTime, default=db.func.current_timestamp())

# Crear todas las tablas en la base de datos
with app.app_context():
    db.create_all()

# Ruta para obtener todos los usuarios
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([usuario.__dict__ for usuario in usuarios]), 200

# Ruta para crear un nuevo usuario
@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.json
    nuevo_usuario = Usuario(nombre=data['nombre'], email=data['email'], contraseña=data['contraseña'])
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({'mensaje': 'Usuario creado correctamente'}), 201

# Ruta para obtener todas las películas
@app.route('/peliculas', methods=['GET'])
def obtener_peliculas():
    peliculas = Pelicula.query.all()
    return jsonify([pelicula.__dict__ for pelicula in peliculas]), 200

# Ruta para crear una nueva película
@app.route('/peliculas', methods=['POST'])
def crear_pelicula():
    data = request.json
    nueva_pelicula = Pelicula(titulo=data['titulo'], descripcion=data['descripcion'], año=data['año'],
                              genero=data['genero'], director=data['director'], actores=data['actores'],
                              imagen_url=data['imagen_url'], trailer_url=data['trailer_url'])
    db.session.add(nueva_pelicula)
    db.session.commit()
    return jsonify({'mensaje': 'Película creada correctamente'}), 201

# Otras rutas pueden incluirse para actualizar, eliminar, etc.

if __name__ == '__main__':
    app.run(debug=True)
