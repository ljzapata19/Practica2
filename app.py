from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

app = Flask(__name__)
#app.config['TEMPLATES_AUTO_RELOAD'] = True

app.config.from_pyfile('config.py')

from models import db
from models import Asistencia, Curso, Estudiante, Padre, Preceptor

@app.route('/')
def inicio():
    return render_template('index.html')

def validar_tipo(tipo):
    prece=True
    if (tipo == Padre):
        prece=False
    return prece
        
def validar_Preceptor(correo, clave):
    completion = False
    usuario_actual = None
    usuario_actual = Preceptor.query.filter_by(correo=str(correo)).first()
    dbClave = usuario_actual.clave
    completion = check_password_hash(clave, dbClave)
   
    if completion is not True:
        usuario_actual = None
    return usuario_actual  

@app.route('/', methods=["POST","GET"])
def validar_datos():
    if request.method == 'POST':
        #datos = request.form
        correo = request.form['correo']
        clave = generate_password_hash(request.form['clave'])
        tipo = request.form.get('tipo')
        if tipo == 'Padre':
            return render_template('error.html', error='No es posible ingresar como Padre.')
        else:
            us = validar_Preceptor(correo, clave)
            if us == None:
                return render_template('error.html', error= 'Los datos ingresados son incorrectos. Por favor ingrese nuevamente')
            else:
                return render_template('preceptor.html',usuario=us)

@app.route('/seleccion_asistencia/<int:usuario_id>', methods=["POST","GET"])
def seleccion_asistencia(usuario_id):
    cursos = Curso.query.filter_by(idpreceptor=int(usuario_id)).all()
    dia_actual = datetime.today().date()
    return render_template('seleccion_asistencia.html', cursos=cursos, dia_actual = dia_actual)


@app.route('/registrar_asistencia',methods=["POST","GET"])
def registrar_asistencia():
    if request.method == "POST":
        curso_id = int(request.form.get('curso'))
        clase = request.form.get('clase')
        fecha = request.form.get('fecha')
        estudiantes = Estudiante.query.filter_by(idcurso=curso_id).all()
        estudiantes_ordenados = sorted(estudiantes)
        
        return render_template('registrar_asistencia.html',curso=curso_id, estudiantes = estudiantes_ordenados, clase = clase, fecha = fecha)
    

@app.route('/guardar_asistencia/<fecha>/<int:curso_id>/<int:clase>', methods = ["POST", "GET"])
def guardar_asistencia(fecha, curso_id, clase):
    if request.method == "POST":
        fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
        
        band = False
        est = Estudiante.query.filter_by(idcurso=curso_id).all()
        estudiantes = sorted(est)
        if estudiantes != None:
            for estudiante in estudiantes:
                band = True
                asistencia_key = f'asistencia-{estudiante.id}'
                justificacion_key = f'justificacion-{estudiante.id}'
                asistencia = request.form.get(asistencia_key)
                justificacion = request.form.get(justificacion_key)
                if justificacion is None:
                    justificacion = ""
                nueva_asistencia = Asistencia(fecha=fecha, codigoclase=int(clase), asistio=asistencia, justificacion=justificacion, idestudiante=estudiante.id)
                db.session.add(nueva_asistencia)
            db.session.commit()
        if band:
            return ('Se guardaron nuevas asistencias')
        else:
            return ('No se guardaron nuevas asistencias')
    

@app.route('/seleccion_curso/<int:usuario_id>', methods=["POST","GET"])
def seleccion_curso(usuario_id):
    cursos = Curso.query.filter_by(idpreceptor=int(usuario_id)).all()
    
    return render_template('seleccion_curso.html', cursos=cursos)        

@app.route('/informar_asistencias',methods=["POST","GET"])
def informar_asistencias():
    if request.method == "POST":
        curso_id = int(request.form.get('curso'))
        cursos = Curso.query.filter_by(id=curso_id).all()
        curso = cursos[0]
        estudiantes = Estudiante.query.filter_by(idcurso=curso_id).all()
        estudiantes_ordenados = sorted(estudiantes)
        
        datos=[]
        for estudiante in estudiantes_ordenados:
            presente_aula=0
            ausente_aula_jus=0
            ausente_aula_injus=0
            presente_ef=0
            ausente_ef_jus=0
            ausente_ef_injus=0
            total_ausencias=0
            asistencias = Asistencia.query.with_entities(Asistencia.codigoclase, Asistencia.asistio, Asistencia.justificacion).filter_by(idestudiante = estudiante.id).all()
            for asistencia in asistencias:
                if asistencia.codigoclase == 1:     #aula
                    if asistencia.asistio == "s":   #presente aula
                        presente_aula +=1
                    else:
                        if (asistencia.justificacion != ""): #ausente justificado aula
                            ausente_aula_jus += 1
                        else:
                            ausente_aula_injus += 1     #ausente injustificado aula
                else:           #ef
                    if asistencia.asistio == "s":  #presente ef
                        presente_ef += 1
                    else:
                        if (asistencia.justificacion != ""): #ausente justificado ef
                            ausente_ef_jus +=1
                        else:
                            ausente_ef_injus += 1
            total_ausencias = (ausente_aula_jus + ausente_aula_injus) + (ausente_ef_jus + ausente_ef_injus)*0.5
            datos.append({
                'estudiante': estudiante,
                'presente_aula': presente_aula,
                'ausente_aula_jus': ausente_aula_jus,
                'ausente_aula_injus': ausente_aula_injus,
                'presente_ef': presente_ef,
                'ausente_ef_jus': ausente_ef_jus,
                'ausente_ef_injus': ausente_ef_injus,
                'total_ausencias': total_ausencias
                })
            
        return render_template('informar_asistencia.html',datos = datos, curso = curso)
 

if __name__ == '__main__':
    
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)
    

