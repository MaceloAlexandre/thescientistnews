import psycopg2
from models import Usuario
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash



def conectardb():
    conexao = psycopg2.connect(database="TheScientistNews",
                               host="localhost",
                               user="postgres",
                               password="Macelo321",
                               port="5432")
    return conexao


def create_tables(conexao):
    cursor = conexao.cursor()
    # Coisas que alterei e precisa acresentar: alterei a senha para varchar(255), adicionei a coluna categria em postagens e também
    # adicionei o campo nome_autor na tabela de postagens, para que possamos pegar o nome do autor e não só o id.
    # adicionei a coluna nome_autor na tabela comentarios, para que possamos pegar o nome do autor e não só o id.
    # ALTER TABLE postagens 
    #ADD COLUMN fonte_original VARCHAR(255) DEFAULT NULL;

    
    comandos = """
    -- Tabela de usuários
    CREATE TABLE IF NOT EXISTS usuarios (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        email VARCHAR(120) UNIQUE NOT NULL,
        senha_hash VARCHAR(128) NOT NULL,
        is_admin BOOLEAN DEFAULT FALSE,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Tabela de postagens
    CREATE TABLE IF NOT EXISTS postagens (
        id SERIAL PRIMARY KEY,
        titulo VARCHAR(200) NOT NULL,
        resumo TEXT,
        materia TEXT NOT NULL,
        imagem_caminho TEXT,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        autor INTEGER NOT NULL,
        FOREIGN KEY (autor) REFERENCES usuarios(id) ON DELETE CASCADE
    );

    -- Tabela de comentários
    CREATE TABLE IF NOT EXISTS comentarios (
        id SERIAL PRIMARY KEY,
        conteudo TEXT NOT NULL,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        editado BOOLEAN DEFAULT FALSE,
        oculto BOOLEAN DEFAULT FALSE,
        autor INTEGER NOT NULL,
        postagem_id INTEGER NOT NULL,
        FOREIGN KEY (autor) REFERENCES usuarios(id) ON DELETE CASCADE,
        FOREIGN KEY (postagem_id) REFERENCES postagens(id) ON DELETE CASCADE
    );

    -- Tabela de postagens salvas (relacionamento M:N)
    CREATE TABLE IF NOT EXISTS postagens_salvas (
        usuario_id INTEGER NOT NULL,
        postagem_id INTEGER NOT NULL,
        salvo_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (usuario_id, postagem_id),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
        FOREIGN KEY (postagem_id) REFERENCES postagens(id) ON DELETE CASCADE
    );
    """

    cursor.execute(comandos)
    conexao.commit()
    cursor.close()
    conexao.close()


class UsuarioDAO:
    def __init__(self):
        self.conexao = conectardb()

    def verificar_login(self, email, senha_digitada):
        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            row = cursor.fetchone()
            if row:
                usuario = Usuario(*row)
                if check_password_hash(usuario.senha, senha_digitada):
                    return usuario  # Login válido
        except Exception as e:
            print(f"Erro ao verificar login: {e}")
        finally:
            if cursor:
                cursor.close()
            if self.conexao:
                self.conexao.close()
        return None

    def cadastrar_usuario(self, usuario: Usuario):
        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute("""
                INSERT INTO usuarios (nome, email, senha, is_admin)
                VALUES (%s, %s, %s, %s)
            """, (usuario.nome, usuario.email, usuario.senha, usuario.is_admin))
            self.conexao.commit()
            print("Usuário cadastrado com sucesso!")
        except Exception as e:
            print(f"Erro ao cadastrar usuário: {e}")
        finally:
            if cursor:
                cursor.close()
            if self.conexao:
                self.conexao.close()


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



