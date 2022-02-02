from flask import render_template, request, redirect, session, flash
from login_n_register_app import app
from login_n_register_app.models.modelo_usuarios import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/', methods=["GET"])
def despliegaRegistroLogin():
    return render_template("index.html")

@app.route('/dashboard', methods=["GET"])
def despliegaDashboard():
    if 'email' in session:       
        return render_template("dashboard.html")
    else:
        return redirect('/')

@app.route('/registroUsuario', methods=["POST"])
def registrarUsuario():
    datosFormulario = request.form
    if not Usuario.validarUsuario(datosFormulario, "register"):
        return redirect('/')
    valUser = {
        "email" : datosFormulario["email"]
    }
    if Usuario.validarRegistrado(valUser):
        flash("Dirección de correo electrónico registrada!", "register")
        return redirect('/')
    encryptedPass = bcrypt.generate_password_hash(datosFormulario["password"])
    nuevoUsuario = {
        "nombre" : datosFormulario["nombre"],
        "apellido" : datosFormulario["apellido"],
        "email" : datosFormulario["email"],
        "password" : encryptedPass,
    }
    session["nombre"] = nuevoUsuario["nombre"]
    session["email"] = nuevoUsuario["email"]
    resultado = Usuario.agregaUsuario(nuevoUsuario)
    if type(resultado) is int and resultado != 0:
        return redirect('/dashboard')

@app.route('/login', methods=["POST"])
def loginUsuario():
    datosFormulario = request.form
    if not Usuario.validarUsuario(datosFormulario, "login"):
        return redirect('/')
    valUser = {
        "email" : datosFormulario["loginUsuario"]
    }
    if not Usuario.validarRegistrado(valUser):
        flash("Dirección de correo electrónico no registrada!", "login")
        return redirect('/')


    tryUser = datosFormulario["loginUsuario"]
    tryPass = datosFormulario["passwordUsuario"]
    usuario = {
        "email" : tryUser,
    }

    resultado = Usuario.verificaUsuario(usuario)
    
    if not bcrypt.check_password_hash(resultado.password, tryPass):
        flash("Contraseña incorrecta", "login")
        return redirect('/')
    else:
        session["nombre"] = resultado.nombre
        session["email"] = resultado.email
        return redirect('/dashboard')

@app.route('/logout', methods=["GET"])
def logoutUsuario():
    session.clear()
    return redirect('/')