import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import conectardb
from models.postagem import Postagem

class PostagemDAO:
    def __init__(self):
        self.conexao = conectardb()

    def salvar_postagem(self, postagem):
        try:
            cursor = self.conexao.cursor()
            cursor.execute("""
                INSERT INTO postagens 
                (titulo, resumo, materia, autor, nome_autor, criado_em, categoria, imagem_caminho, fonte_original)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                postagem.titulo,
                postagem.resumo,
                postagem.materia,
                postagem.autor,
                postagem.nome_autor,
                postagem.data_postagem,
                postagem.categoria,
                postagem.midia,
                postagem.fonte_original  # Novo campo
            ))
            self.conexao.commit()
        except Exception as e:
            print(f"Erro ao salvar postagem: {e}")
            self.conexao.rollback()
        finally:
            cursor.close()
            self.conexao.close()

    def listar_postagens(self):
        cursor = self.conexao.cursor()
        cursor.execute("""
            SELECT id, titulo, resumo, materia, imagem_caminho, 
                   criado_em, autor, categoria, nome_autor, fonte_original
            FROM postagens
            ORDER BY criado_em DESC
        """)
        linhas = cursor.fetchall()
        cursor.close()

        postagens = []
        for linha in linhas:
            data_postagem = linha[5]
            data_formatada = data_postagem.strftime('%d/%m/%Y')
            post = {
                "id": linha[0],
                "titulo": linha[1],
                "resumo": linha[2],            # resumo vira texto
                "materia": linha[3],
                "midia": linha[4],
                "data_postagem": data_formatada,
                "autor": linha[6],
                "categoria": linha[7],
                "nome_autor": linha[8],
                "fonte_original": linha[9]       # nome do autor

            }
            postagens.append(post)

        return postagens

    def get_postagem_by_id(self, post_id):
        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute("SELECT * FROM postagens WHERE id = %s", (post_id,))
            postagem = cursor.fetchone()  # Recupera a primeira linha correspondente ao ID

            if postagem:
                data_postagem = postagem[5]
                data_formatada = data_postagem.strftime('%d/%m/%Y')
                postagem_dict = {
                    "id": postagem[0],
                    "titulo": postagem[1],
                    "resumo": postagem[2],  # resumo vira texto
                    "materia": postagem[3],
                    "midia": postagem[4],
                    "data_postagem": data_formatada,
                    "autor": postagem[6],
                    "categoria": postagem[7],
                    "nome_autor": postagem[8],
                    "fonte_original": postagem[9]  # Novo campo
                }
                return postagem_dict
            else:
                return None
        except Exception as e:
            print(f"Erro ao buscar postagem: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def buscar_postagens_por_categoria(self, categoria_nome):
        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute("""
                SELECT * FROM postagens WHERE categoria = %s ORDER BY criado_em DESC
            """, (categoria_nome,))
            linhas =  cursor.fetchall()
            cursor.close()

            postagens = []
            for linha in linhas:
                data_postagem = linha[5]
                data_formatada = data_postagem.strftime('%d/%m/%Y')
                post = {
                    "id": linha[0],
                    "titulo": linha[1],
                    "resumo": linha[2],            # resumo vira texto
                    "materia": linha[3],
                    "midia": linha[4],
                    "data_postagem": data_formatada,
                    "autor": linha[6],
                    "categoria": linha[7],
                    "nome_autor": linha[8],
                    "fonte_original": linha[9]       # nome do autor

                }
                postagens.append(post)

            return postagens
        except Exception as e:
            print(f"Erro ao buscar postagem: {e}")
            return None
        finally:
            if cursor:
                cursor.close()



