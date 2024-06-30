import os
from trilha import app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators

class FormularioCurso(FlaskForm):
    curso = StringField('Nome do Curso', [validators.DataRequired(), validators.Length(min=1, max=50)])
    descricao = StringField('Descrição', [validators.DataRequired(), validators.Length(min=1, max=200)])
    escola = StringField('Escola', [validators.DataRequired(), validators.Length(min=1, max=20)])
    duracao = StringField('Duração', [validators.DataRequired(), validators.Length(min=1, max=200)])
    salvar = SubmitField('Salvar')

class FormularioUsuario(FlaskForm):
    nome = StringField('Nome', [validators.DataRequired(), validators.Length(min=1, max=20)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    login = SubmitField('Login')


def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo

    return 'capa_padrao.jpg'

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo != 'capa_padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))
