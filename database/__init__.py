import psycopg2

def conectardb():
    conexao = psycopg2.connect(database="TheScientistNews",
                               host="localhost",
                               user="postgres",
                               password="Macelo321",
                               port="5432")
    return conexao


def create_tables(conexao):
    cursor = conexao.cursor()

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
