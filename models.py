from trilha import db

class Cursos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    curso = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    escola = db.Column(db.String(20), nullable=False)
    duracao = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

class Usuarios(db.Model):
    nome = db.Column(db.String(20),  primary_key=True)
    senha = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name