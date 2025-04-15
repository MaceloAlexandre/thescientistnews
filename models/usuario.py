class Usuario:
    def __init__(self, id=None, nome='', email='', senha='', is_admin=False, criado_em=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.is_admin = is_admin
        self.criado_em = criado_em
