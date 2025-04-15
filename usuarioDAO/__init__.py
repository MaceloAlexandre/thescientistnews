from database import conectardb
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from models.usuario import Usuario

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
                INSERT INTO usuarios (nome, email, senha_hash, is_admin)
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



novo_usuario = Usuario(
    nome="Macelo Alexandre",
    email="macelo_example@hotmail.com",
    senha=generate_password_hash("123"),
    is_admin=True
)

dao = UsuarioDAO()
dao.cadastrar_usuario(novo_usuario)