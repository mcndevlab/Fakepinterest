# arquivo temporario existe apenas para criar o banco, após criado perde a função...
from fakepinterest import database, app  # aula 43.9
from fakepinterest.models import Usuario, Foto
# para criar o banco de dados..
with app.app_context():  # aula 43.9
    database.create_all()  # aula 43.9
# Ao executar os comandos acima é criado a pasta "instance" que é uma instancia onde está nosso
# Banco de dados comunidade.db - BD SQL LIGHT (conforme definimos no init..)