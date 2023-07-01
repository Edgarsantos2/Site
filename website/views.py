from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/')
def index():
    return render_template("index.html")


@views.route('/login')
def login():
    return render_template("login.html")


@views.route('/registo')
def registo():
    return render_template("registo.html")


@views.route('/contactos')
def contactos():
    return render_template("contactos.html")

@views.route('/equipa')
def equipa():
    return render_template("equipa.html")

@views.route('/simulacao')
def simulacao():
    return render_template("simulacao.html")

@views.route('/acliente')
def acliente():
    return render_template("acliente.html")

@views.route('/marcacoes')
def marcacoes():
    return render_template("marcacoes.html")

@views.route('/seguros')
def seguros():
    return render_template("seguros.html")
