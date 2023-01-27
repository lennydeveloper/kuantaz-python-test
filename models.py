from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from dataclasses import dataclass

db = SQLAlchemy()

@dataclass
class Institucion(db.Model):
    id: int
    nombre: str
    descripcion: str
    direccion: str
    fecha_creacion: datetime
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)
    direccion = db.Column(db.String(100), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    proyectos = db.relationship('Proyecto', backref='institucion')

    def __repr__(self) -> str:
        return f'Nombre: {self.nombre}, id: {self.id}'


@dataclass
class Usuario(db.Model):
    id: int
    nombres: str
    apellidos: str
    rut: str
    fecha_nacimiento: datetime
    cargo: str
    edad: int

    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    rut = db.Column(db.String(20), nullable=False)
    fecha_nacimiento = db.Column(db.DateTime, nullable=False)
    cargo = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=True)
    proyectos = db.relationship('Proyecto', backref='usuario')

    def __repr__(self) -> str:
        return f'Nombre: {self.nombres} {self.apellidos}, id: {self.id}'


@dataclass
class Proyecto(db.Model):
    id: int
    nombre: str
    descripcion: str
    fecha_inicio: datetime
    fecha_termino: datetime

    def default_fecha_termino():
        return datetime.now() + timedelta(days=30)

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)
    fecha_inicio = db.Column(db.DateTime, nullable=False, default=datetime.now())
    fecha_termino = db.Column(db.DateTime, nullable=False, default=default_fecha_termino())
    institucion_id = db.Column(db.Integer, db.ForeignKey('institucion.id'), nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True)

    def __repr__(self) -> str:
        return f'Nombre: {self.nombre}, id: {self.id}'