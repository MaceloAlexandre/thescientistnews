from database import conectardb
from models.comentario import Comentario

class ComentarioDAO:
    def adicionar_comentario(self, comentario):
        conexao = conectardb()
        cursor = None
        try:
            cursor = conexao.cursor()
            cursor.execute(""" 
                INSERT INTO comentarios (conteudo, criado_em, editado, oculto, autor, postagem_id, nome_autor)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                comentario.conteudo,
                comentario.criado_em,
                comentario.editado,
                comentario.oculto,
                comentario.autor,
                comentario.postagem_id,
                comentario.nome_autor
            ))
            conexao.commit()
        except Exception as e:
            print(f"Erro ao adicionar comentário: {e}")
            conexao.rollback()
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    def listar_comentarios(self, postagem_id):
        conexao = conectardb()
        cursor = None
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT id, nome_autor, conteudo, criado_em, autor, oculto, postagem_id
                FROM comentarios
                WHERE postagem_id = %s AND oculto = FALSE
                ORDER BY id DESC
            """, (postagem_id,))
            resultados = cursor.fetchall()
            comentarios = []
            for row in resultados:
                comentario = Comentario(
                    id=row[0],
                    nome_autor=row[1],
                    conteudo=row[2],
                    criado_em=row[3],
                    autor=row[4],
                    oculto=row[5],
                    postagem_id=row[6]
                )
                comentarios.append(comentario)
            return comentarios
        except Exception as e:
            print(f"Erro ao listar comentários: {e}")
            return []
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    def editar_comentario(self, comentario_id, novo_conteudo):
        conexao = conectardb()
        cursor = None
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                UPDATE comentarios
                SET conteudo = %s, editado = TRUE
                WHERE id = %s
            """, (novo_conteudo, comentario_id))
            conexao.commit()
        except Exception as e:
            print(f"Erro ao editar comentário: {e}")
            conexao.rollback()
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    def excluir_comentario(self, comentario_id):
        conexao = conectardb()
        cursor = None
        try:
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM comentarios WHERE id = %s", (comentario_id,))
            conexao.commit()
        except Exception as e:
            print(f"Erro ao excluir comentário: {e}")
            conexao.rollback()
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    def ocultar_comentario(self, comentario_id):
        conexao = conectardb()
        cursor = None
        try:
            cursor = conexao.cursor()
            cursor.execute("UPDATE comentarios SET oculto = TRUE WHERE id = %s", (comentario_id,))
            conexao.commit()
        except Exception as e:
            print(f"Erro ao ocultar comentário: {e}")
            conexao.rollback()
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()

    def get_comentario_por_id(self, comentario_id):
        conexao = conectardb()
        cursor = None
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT id, nome_autor, conteudo, criado_em, autor, oculto, postagem_id
                FROM comentarios
                WHERE id = %s
            """, (comentario_id,))
            resultado = cursor.fetchone()

            if resultado:
                comentario = Comentario(
                    id=resultado[0],
                    nome_autor=resultado[1],
                    conteudo=resultado[2],
                    criado_em=resultado[3],
                    autor=resultado[4],
                    oculto=resultado[5],
                    postagem_id=resultado[6]
                )
                return comentario
            else:
                return None
        except Exception as e:
            print(f"Erro ao buscar comentário por ID: {e}")
            return None
        finally:
            if cursor: cursor.close()
            if conexao: conexao.close()
