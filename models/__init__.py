from werkzeug.security import generate_password_hash


class Usuario:
    def __init__(self, id=None, nome='', email='', senha='', is_admin=False, criado_em=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.is_admin = is_admin
        self.criado_em = criado_em

class Postagem:
    def __init__(self, titulo, resumo, materia, autor, nome_autor, data_postagem, categoria, midia=None, fonte_original=None):
        self.titulo = titulo
        self.resumo = resumo
        self.materia = materia
        self.autor = autor
        self.nome_autor = nome_autor
        self.data_postagem = data_postagem
        self.categoria = categoria
        self.midia = midia
        self.fonte_original = fonte_original  # Novo campo