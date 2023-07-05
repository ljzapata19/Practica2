from __main__ import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy(app)

class Asistencia(db.Model):
    __tablename__= 'asistencia'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow().date())    
    codigoclase = db.Column(db.Integer, unique=True, nullable=False)
    asistio = db.Column(db.Text, nullable=False)    
    justificacion = db.Column(db.String(100), nullable=False)
    idestudiante = db.Column(db.Integer, db.ForeignKey('estudiante.id'), nullable=False)

class Curso(db.Model):
    __tablename__= 'curso'
    id = db.Column(db.Integer, primary_key=True)
    anio = db.Column(db.String(80), nullable=False)
    division = db.Column(db.String(80), unique=True, nullable=False)
    idpreceptor = db.Column(db.Integer, db.ForeignKey('preceptor.id'), nullable=False)
    estudiantes = db.relationship('Estudiante', backref='curso', cascade="all, delete-orphan")

class Estudiante(db.Model):
    __tablename__= 'estudiante'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    dni = db.Column(db.String(10), nullable=False)
    idcurso = db.Column(db.Integer, db.ForeignKey('curso.id'), nullable=False)
    idpadre = db.Column(db.Integer, db.ForeignKey('padre.id'))
    asistencias = db.relationship('Asistencia', backref='estudiante', cascade="all, delete-orphan")
    def __lt__(self, otro):
        if self.apellido == otro.apellido:
            return self.nombre < otro.nombre
        else:
            return self.apellido < otro.apellido
    def __eq__(self, otro):
        return self.apellido == otro.apellido and self.nombre == otro.nombre

class Padre(db.Model):
    __tablename__= 'padre'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    correo = db.Column(db.String(120), nullable=False)
    clave = db.Column(db.String(120), nullable=False)
    estudiantes = db.relationship('Estudiante', backref='padre', cascade="all, delete-orphan")

class Preceptor(db.Model):
    __tablename__= 'preceptor'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    correo = db.Column(db.String(120), nullable=False)
    clave = db.Column(db.String(120), nullable=False)
    curso = db.relationship("Curso", backref="preceptor", cascade="all, delete-orphan")    
'''
from __main__ import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Asistencia(db.Model):
    __tablename__= 'asistencia'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime)
    codigoclase = db.Column(db.Integer)
    asistio = db.Column(db.Text) 
    justificacion = db.Column(db.Varchar(100))
    idestudiante = db.Column(db.Integer)

class Curso(db.Model):
    __tablename__= 'curso'
    id = db.Column(db.Integer, primary_key=True)
    anio = db.Column(db.Varchar(80))
    division = db.Column(db.Varchar(80))
    idpreceptor = db.Column(db.Integer)

class Estudiante(db.Model):
    __tablename__= 'estudiante'
    nombre = db.Column(db.Varchar(80))
    apellido = db.Column(db.Varchar(80))
    dni = db.Column(db.Varchar(20)) 
    idcurso = db.Column(db.Integer)
    idpadre = db.Column(db.Integer)
        
class Padre(db.Model):
    __tablename__= 'padre'
    nombre = db.Column(db.Varchar(80))
    apellido = db.Column(db.Varchar(80))
    correo = db.Column(db.Varchar(120)) 
    clave = db.Column(db.Varchar(120))
    
class Preceptor(db.Model):
    __tablename__= 'preceptor'
    nombre = db.Column(db.Varchar(80))
    apellido = db.Column(db.Varchar(80))
    correo = db.Column(db.Varchar(120)) 
    clave = db.Column(db.Varchar(120))
'''