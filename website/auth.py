import flask
import pyrebase
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore, auth as autentic





auth = Blueprint('auth', __name__)

@auth.route('/logout')
def logout():
    return redirect(url_for("views.index"))

@auth.route('/logout_button')
def logout_button():
    session['logged_in'] = False
    return redirect(url_for("auth.logout"))


firebaseConfig = {
                    'apiKey': "AIzaSyD1SYgZv_Wvdw8DNUmlvgmzwG95hecMK3Q",
                    'authDomain': "projetopdibs.firebaseapp.com",
                    'databaseURL': "https://projetopdibs-default-rtdb.europe-west1.firebasedatabase.app",
                    'projectId': "projetopdibs",
                    'storageBucket': "projetopdibs.appspot.com",
                    'messagingSenderId': "420620551966",
                    'appId': "1:420620551966:web:e71a7853b05dab7ba76b0f",
                    'measurementId': "G-0KQJPNLH8J"
}

firebase = pyrebase.initialize_app(firebaseConfig)

autenti = firebase.auth()

cred = credentials.Certificate("projetopdibs-firebase-adminsdk-itq2r-d62c10c242.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def login_user(email, password):
    try:
        autenti.sign_in_with_email_and_password(email, password)
        session['logged_in'] = True
        session['user'] = email
    except Exception as e:
     flash("Erro no login", "danger")
     return redirect('url_for("auth.login")')


@auth.route('/login', methods=['POST'])
def login():
     session['logged_in'] = True
     
     return redirect(url_for('views.index'))

@auth.route('/login_form', methods=['POST'])
def login_form():
   if request.method == "POST":
        
    # Obter os valores dos campos do formulário
        email = request.form['email']
        password = request.form['password']
        
    # Chamar a função de login 
        login_user(email, password)
        
        
        return redirect(url_for("auth.login"))
   else:
    
        return redirect(url_for("auth.login"))



# REGISTO

def register_user(email, password):
    try:
        # Cria o usuário no Firebase Authentication
        autenti.create_user_with_email_and_password(email, password)

        flash("Conta Criada com sucesso", "success")
        # Registo bem-sucedido, você pode redirecionar o usuário ou realizar outras ações necessárias.
        
  
    except Exception as e:
        
        return render_template("registo.html")


@auth.route('/registo', methods=['POST'])
def registo():
     
    return render_template("registo.html")



@auth.route('/resgisto_form', methods=['POST'])
def registo_form():
    if request.method == "POST":
        # Obter os valores do formulário
        email = request.form['email']
        password = request.form['password']

        # Verificar o comprimento da senha
        if not len(password) >= 6:
            flash("A Password deve ter mais de 6 caracteres!", "danger")
            return redirect(url_for("auth.registo"))

        try:
            
            user = autentic.get_user_by_email(email)
            flash("Este email já está sendo usado por outro usuário.", "danger")
            return redirect(url_for("auth.registo"))
        except Exception:
           
            register_user(email, password)

            return redirect(url_for("auth.registo"))
            

    return redirect(url_for("auth.registo"))




#CONTACTOS

@auth.route('/contactos_form', methods=['POST'])
def contactos_form():
   nome = request.form.get('nome')
   apelido = request.form.get('apelido')
   email = request.form.get('email')
   numero = request.form.get('numero')
   mensagem = request.form.get('mensagem')

   
   contatos_ref = db.collection('contactos')
   novo_contato = {
        'nome': nome,
        'apelido': apelido,
        'email': email,
        'numero': numero,
        'mensagem': mensagem
    }
   contatos_ref.add(novo_contato)
   flash("Contacto enviado com sucesso!", "success")
   return render_template("contactos.html")

#Marcações

@auth.route('/marcacoes', methods=['POST'])
def marcacoes():
     
    return render_template("marcacoes.html")


@auth.route('/marcacoes_form', methods=['POST'])
def marcacoes_form():
   nome = request.form.get('nome_m')
   email = request.form.get('email_m')
   mediador = request.form.get('mediador_m')
   motivo = request.form.get('motivo_m')
   assunto = request.form.get('assunto_m')
   data = request.form.get('data_m')
    # Salve os dados no Firestore
   marcacoes_ref = db.collection('consultas')
   novo_marcacoes = {
        'nome': nome,
        'email': email,
        'mediador': mediador,
        'motivo': motivo,
        'assunto': assunto,
        'data': data
    }
   marcacoes_ref.add(novo_marcacoes)
   flash("Marcação enviada com sucesso!", "success")
   return redirect(url_for("auth.marcacoes"))

           

    





