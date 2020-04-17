from flask import Flask, flash, url_for, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#Creacion de la Base de Datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///libros.sqlite3'
app.config['SECRET_KEY'] = 'uippc3'

db = SQLAlchemy(app)
#Creacion de la Tabla Libros
class libros(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    materia = db.Column(db.String(50))
    autor = db.Column(db.String(200))
    cantidad = db.Column(db.Integer)
    precio = db.Column(db.String(10))

    def __init__(self, nombre, autor, materia, cantidad,precio):
        self.nombre = nombre
        self.autor = autor
        self.materia = materia
        self.cantidad = cantidad
        self.precio = precio

#Creacion de tabla usuarios
class usuarios(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    usuario = db.Column(db.String(20))
    password = db.Column(db.String(15))

    def __init__(self, usuario,password):
        self.usuario = usuario
        self.password = password



#Loggin al sistema Libraria Petra
@app.route('/')
def inicio():
    return render_template('login.html')

#Muestra la Pagina Principal con la lista de libros
@app.route('/mostrar_todo/')
def mostrar_todo():
    return render_template('mostrar_todo.html', libros=libros.query.all())
    #return redirect(url_for('login'))

#Acceso a usuario
@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        if usuario == 'ogonzalez' and password == '123456':
            #return render_template('mostrar_todo.html', libros=libros.query.all())
            return redirect(url_for('mostrar_todo'))
    else:
        return render_template('login.html')


@app.route('/nuevo/', methods=['GET', 'POST'])
#Agrega libros nuevos en la Base de Datos
def nuevo():
    if request.method == 'POST':
        if not request.form['nombre'] or not request.form['autor'] or not request.form['materia']:
            flash('Por favor introduzca todos los campos', 'error')
        else:
            libro = libros(request.form['nombre'],
                                     request.form['autor'],
                                     request.form['materia'],
                                     request.form['cantidad'],request.form['precio'])
            db.session.add(libro)
            db.session.commit()
            flash('Registro guardado con exito!')
            return redirect(url_for('mostrar_todo'))
    return render_template('nuevo.html')

#Elimina elementos en la Base de Datos
@app.route('/eliminar/',methods =['GET','POST'])
def eliminar():
    if request.method == 'POST':
        borrar = request.form['id'] #Asigna el ID enviado por el formulario a la variable borrar
        u = libros.query.get(borrar)
        db.session.delete(u)
        db.session.commit()
        return redirect(url_for('mostrar_todo'))

#Realiza venta de libros
@app.route('/comprar/',methods = ['GET','POST'])
def comprar():
    if request.method == 'POST':
        comprar = request.form['id']
        cant = request.form['cantidad']
        u = libros.query.get(comprar)
        if int(cant) > int(u.cantidad):
            flash('No hay suficientes libros')
            return redirect(url_for('mostrar_todo'))
        else:
             int(u.cantidad)
             int(cant)
             flag = int (u.cantidad) - int (cant)
             flag = int(flag)
             print(flag)
             u.cantidad = flag
             db.session.commit()
             flash('Libro Vendido!')
             return redirect(url_for('mostrar_todo'))


if __name__ == '__main__':
 db.create_all()
app.run()
