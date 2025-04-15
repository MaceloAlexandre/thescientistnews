from datetime import datetime

class Comentario:
    def __init__(self, conteudo, autor, nome_autor, postagem_id, criado_em=None, editado=False, oculto=False, id = None):
        self.id = id
        self.conteudo = conteudo
        self.criado_em = criado_em or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.editado = editado
        self.oculto = oculto
        self.autor = autor
        self.nome_autor = nome_autor
        self.postagem_id = postagem_id
