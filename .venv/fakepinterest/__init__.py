#Aqui vamos definir o APP - Criar o nosso site

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager #aula 43.10
from flask_bcrypt import Bcrypt #aula 43.10
import os

#cria nosso APP
app = Flask(__name__)

#implementar uma conexão com BD qdo disponivel e uma opção qdo offline:
#if os.getenv("DEBUG") == 0:
#    link_banco = os.getenv("DATABASE_URL")
#else:
#    link_banco = 'sqlite:///comunidade.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db' #aula 43.9
app.config['SECRET_KEY'] = "fb20b75fd1c781bddbf676256743b7bd" #aula 43.10
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"

database = SQLAlchemy(app) # aula 43.9
bcrypt = Bcrypt(app)#aula 43.10
login_manager = LoginManager(app)#aula 43.10
login_manager.login_view = "homepage" #login será feito na homepage # aula 43.10

#importações dos demais arquivos sempre no final, nunca antes
#precisa do routes para funcionar
from fakepinterest import routes
