#CRIAR OS LINKS - ROTAS DO SITE
from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from fakepinterest.models import Usuario, Foto
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
from flask_login import login_required, login_user, current_user, logout_user
from werkzeug.utils import secure_filename
import os

@app.route("/", methods=["GET", "POST"])
def homepage():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha.encode('utf-8'), form_login.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("homepage.html", form=form_login)


@app.route("/criarconta", methods=["GET", "POST"])
def criar_conta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data.decode('utf-8'))
        usuario = Usuario(username=form_criarconta.username.data,
                          senha=senha, email=form_criarconta.email.data)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("criarconta.html", form=form_criarconta)


@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        # o usuario ta vendo o perfil dele
        form_foto = FormFoto()
        #criação da funcionalidade de enviar fotos
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            # salvar o arquivo dentro da pasta certa, OS join junta os caminhos, no caso os 3 entre ","
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho)
            # criar a foto no banco de dados com o item "imagem" sendo o nome do arqivo
            foto = Foto(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(foto)
            database.session.commit()
        return render_template("perfil.html", usuario=current_user, form=form_foto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form=None)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))


@app.route("/feed")
@login_required #só visualiza se estiver logado
#conseguir ver todas as fotos no feed minhas e de demais usuários aula 43.17
def feed():
    #43.7 para exibir todas as fotos na tela ser[a necessário fazer busca no BD..
    #43.7 vai exibir por ordem de criação as fotospor isso query.order
    #43.7 se eu quiser limitar a qtde a aparecer posso colocar no fim do cód abaixo: ...all() [:10]
    #43.7 "Foto.data_criacao.desc" ta colocando por ordem descendente de criação, pode-se alterar..
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()#[:10]
    return render_template("feed.html", fotos=fotos)