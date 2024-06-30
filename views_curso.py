from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from trilha import app, db
from models import Cursos
from helpers import recupera_imagem, deleta_arquivo, FormularioCurso
import time


@app.route('/')
def index():
    lista = Cursos.query.order_by(Cursos.id)
    return render_template('lista.html', titulo='Cursos', cursos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    form = FormularioCurso()
    return render_template('novo.html', titulo='Novo Curso', form=form)

@app.route('/criar', methods=['POST',])
def criar():
    form = FormularioCurso(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    curso = form.curso.data
    descricao = form.descricao.data
    escola = form.escola.data
    duracao = form.duracao.data

    novo_curso = Cursos(curso=curso, descricao=descricao, escola=escola, duracao=duracao)
    db.session.add(novo_curso)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{novo_curso.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))
    curso = Cursos.query.filter_by(id=id).first()
    form = FormularioCurso()
    form.curso.data = curso.curso
    form.descricao.data = curso.descricao
    form.escola.data = curso.escola
    form.duracao.data = curso.duracao
    capa_curso = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Curso', id=id, curso=curso, capa_curso=capa_curso, form=form)

@app.route('/atualizar', methods=['POST',])
def atualizar():
    form = FormularioCurso(request.form)

    if form.validate_on_submit():
        curso = Cursos.query.filter_by(id=request.form['id']).first()
        curso.curso = form.curso.data
        curso.descricao = form.descricao.data
        curso.escola = form.escola.data
        curso.duracao = form.duracao.data

    db.session.add(curso)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(id)
    arquivo.save(f'{upload_path}/capa{curso.id}-{timestamp}.jpg')

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    Cursos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Curso deletado com sucesso!')

    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)