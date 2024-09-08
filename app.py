import flask
from flask import Flask, render_template, request, redirect, flash, session
import pymongo
from datetime import timedelta
from pymongo import MongoClient

client = MongoClient("mongodb+srv://alefdesalvador:filhodorei@sukita.kbmrt.mongodb.net/?retryWrites=true&w=majority&appName=Sukita")

banco_dados = client["fabular"]
usuarios = banco_dados["usuarios"]
mensagens = banco_dados["mensagens"]

app = Flask(__name__)
app.secret_key = "10245516491832603D"
app.permanent_session_lifetime = timedelta(minutes=30)  # Sessão expira em 30 minutos

@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    email = request.form['email']
    usuario = request.form['usuario']
    filtro = {"email": email}
    senha = request.form['senha']
    if usuarios.count_documents(filtro) == 0:
      id = usuarios.count_documents({}) + 1
      usuarios.insert_one({"email": email, "usuario": usuario, "id": id, "senha": senha})
      print(f"Novo usuario cadastrado:\n{email}\n{usuario}")
      mensagens.insert_one({"mensagem": f"Um novo usuário apareceu 🥳, seja bem-vindo(a) {usuario}", "usuario": "Sistema [ ✓ BOT ]"})
      
    
      return redirect('login')
      
    else:
      print("Usuário ja cadastrado")
      render_template('index.html')
      
  return render_template('index.html')
  

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form['email']
    senha = request.form['senha']
    if usuarios.count_documents({"email": email, "senha": senha}) == 1:
      usuario = usuarios.find_one({"email": email, "senha": senha})
      username = usuario.get("usuario")
      session.permanent = True
      session['username'] =  username
      print(f"Login realizado com sucesso {session['username']}")
      return redirect('chat')

    else:
      print("Credenciais invalidas")

  return render_template('login.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
  mensagen = list(mensagens.find())

  return render_template('chat.html', mensagen=mensagen)

@app.route('/enviar_mensagem', methods=['POST'])
def enviar_mensagem():
  mensagem = request.form['message']
  username = session.get('username')
  if username:
    mensagens.insert_one({"mensagem": mensagem, "usuario": username})
    return redirect("chat")

  else:
    return redirect("login")

@app.route('/user/<int:id>')
def user(id):
  # buscar usuarios
  if usuarios.count_documents({"id": id}) == 1:
    usuario = usuarios.find_one({"id": id})
    id1 = usuario.get("id")
    usuario1 = usuario.get("usuario")
    return f'Nome:{usuario1}<br>Id:{id1}'

  else:
    return 'Usuario nao encontrado'

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')
