from flask import *
from werkzeug.utils import secure_filename
import os
import datetime as datetime
from database import *
from dao.usuarioDAO import *
from models.usuario import Usuario
from dao.postagemDAO import *
from models.postagem import Postagem
from web_scraping import *
from dao.comentarioDAO import ComentarioDAO
from models.comentario import Comentario


app = Flask(__name__)
app.secret_key = 'MySecretKey*123'


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


usuarios = [
    {   'id': 1,
        'nome': 'Macelo Alexandre',
        'email': 'macelo_example@hotmail.com',
        'senha': '123',
        'is_adm': True  # Este é um administrador
    },
    {
        'nome': 'Usuário Comum 1',
        'email': 'usuario1@email.com',
        'senha': 'senha123',
        'is_adm': False
    },
    {
        'nome': 'Sydney Cristian',
        'email': 'sydney@sydney.com',
        'senha': '123',
        'is_adm': True, # Este é um admim
        "postagens_salvas": []
    }
]


posts = [
    
]

@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Verifica se é admin
    is_admin = session['user'].get('is_adm', False)
    return render_template('home.html',
                         user=session['user'],
                         is_admin=is_admin,)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/verificarlogin', methods=['POST','GET'])
def verificarlogin():

    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')


        usuario = UsuarioDAO()
        usuario_encontrado = usuario.verificar_login(email, senha)

        if usuario_encontrado:
            print(f"{usuario_encontrado.senha}")
            # Armazena informações na sessão
            session['user'] = {
                'id': usuario_encontrado.id,
                'nome': usuario_encontrado.nome,
                'email': usuario_encontrado.email,
                'is_adm': usuario_encontrado.is_admin,
            }   
            # Redireciona para a home com os dados do usuário
            return redirect(url_for('home'))
        else:
            flash('E-mail ou senha incorretos', 'error')
            return redirect(url_for('login'))

    elif request.method == 'GET' and 'user' in session:
        # Se já estiver logado, redireciona para home
        return redirect(url_for('home'))

    # Se não for POST nem GET com sessão, redireciona para login
    return redirect(url_for('login'))
    

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        senha2 = request.form.get('senha2')

        # Validação de tamanho
        if len(nome) > 128 or len(email) > 128:
            flash("Nome ou e-mail excedem o limite de 128 caracteres.", "error")
            return render_template('registro.html')

        # Verificar se as senhas são iguais
        if senha != senha2:
            flash("As senhas não coincidem.", "error")
            return render_template('registro.html')

        # Criptografar senha
        senha_hash = generate_password_hash(senha)

        # Criar objeto Usuario
        novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)

        try:
            dao = UsuarioDAO()
            dao.cadastrar_usuario(novo_usuario)
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"Erro ao cadastrar usuário: {str(e)}", 'error')

    return render_template('registro.html')


@app.route('/iframeposts')
def iframeposts():
    dao = PostagemDAO()
    postagens = dao.listar_postagens()
    return render_template('iframeposts.html', posts=postagens)
    
@app.route('/api/links-para-revisao')
def get_links_para_revisao():
    try:
        # Recupera os links com título e imagem
        links_data = obter_links_olhar_digital()

        # Formata os dados para o frontend
        formatted_links = [
            {
                'url': item['link'],
                'titulo': item['titulo'],
                'imagem': item['imagem']
            }
            for item in links_data
        ]

        return jsonify({'links': formatted_links}), 200

    except Exception as e:
        return jsonify({'error': 'Erro ao obter links', 'detalhes': str(e)}), 500
    

@app.route('/api/get-link-content')
def get_link_content():
    if 'user' not in session or not session['user'].get('is_adm', False):
        return jsonify({'error': 'Não autorizado'}), 401
    
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL não fornecida'}), 400
    
    try:
        # Obtém informações do usuário da sessão
        autor_id = session.get('user'[0])  # Ou seu método de obter o ID do autor
        autor_nome = session.get('user'[1])  # Ou valor padrão
        
        # Usa sua função de extração com os parâmetros de autor
        postagem = extrair_conteudo_post(
            link=url,
            autor=autor_id,
            nome_autor=autor_nome
        )
        
        if not postagem:
            return jsonify({'error': 'Conteúdo não pôde ser extraído'}), 400
        
        return jsonify({
            'success': True,
            'postagem': {
                'titulo': postagem.titulo,
                'resumo': postagem.resumo,
                'materia': postagem.materia,
                'midia': postagem.midia or '',
                'categoria': postagem.categoria,
                'fonte_original': url
            }
        })
    
    except Exception as e:
        print(f"Erro na extração: {str(e)}")  # Log para debug
        return jsonify({
            'success': False,
            'error': f'Erro no servidor ao extrair conteúdo: {str(e)}'
        }), 500
        

@app.route("/visualizar", methods=["GET", "POST"])
def visualizar():
    # Exibir lista de links ou editar a postagem, dependendo da ação
    if request.method == "GET":
        links = obter_links_olhar_digital()  # Obtém os links para exibir
        return render_template("lista_links.html", links=links)
    
    if request.method == "POST":
        link = request.form["link"]  # Link selecionado para edição
        postagem = extrair_conteudo_post(link, autor=1, nome_autor="Macelo Alexandre")
        if postagem:
            return render_template("editor_postagem.html", postagem=postagem)
        return "Erro ao extrair conteúdo."


@app.route('/postar', methods=['POST'])
def postar():
    if request.method == 'POST':
        midia = request.files.get('midia')
        caminho_midia = None

        # Se for um upload de arquivo
        if midia and allowed_file(midia.filename):
            filename = secure_filename(midia.filename)
            midia.save(os.path.join(UPLOAD_FOLDER, filename))
            caminho_midia = f'uploads/{filename}'  # Caminho relativo da mídia
            print(f"Arquivo salvo em: {caminho_midia}")
        
        # Caso a mídia seja uma URL
        elif request.form.get('midia_url'):
            caminho_midia = request.form.get('midia_url')
            print(f"URL da mídia: {caminho_midia}")

        # Criação do objeto Postagem
        postagem = Postagem(
            titulo=request.form.get('titulo'),
            resumo=request.form.get('resumo'),
            materia=request.form.get('materia'),
            autor=session['user']['id'],
            nome_autor=session['user']['nome'],
            data_postagem=datetime.datetime.now(),
            categoria=request.form.get('categoria'),
            midia=caminho_midia,
            fonte_original=request.form.get('fonte_original')  # Salva o caminho ou a URL
        )

        try:
            dao = PostagemDAO()
            dao.salvar_postagem(postagem)
        except Exception as e:
            return redirect(url_for('painel_admin'))
        return redirect(url_for('painel_admin'))

    return render_template('painel_admin.html')


@app.route('/post/<int:id>')
def post(id):
    # Buscar o post no banco de dados usando o id
    dao = PostagemDAO()
    dao.get_postagem_by_id(id)
    post = dao.get_postagem_by_id(id)

    
    if not post:
        # Se o post não for encontrado, retorna erro 404
        abort(404, description="Post não encontrado")

    comentario_dao = ComentarioDAO()
    comentarios_do_post = comentario_dao.listar_comentarios(postagem_id=id)

    return render_template('post.html', post=post, comentarios=comentarios_do_post)


@app.route('/comentar/<int:post_id>', methods=['POST'])
def comentar(post_id):
    if 'user' not in session:
        flash("Você precisa estar logado para comentar", "error")
        return redirect(url_for('login'))

    conteudo = request.form.get('texto')
    if not conteudo.strip():
        return redirect(url_for('post', id=post_id))

    user = session['user']

    comentario = Comentario(
        conteudo=conteudo,
        autor=user['id'],
        nome_autor=user['nome'],
        postagem_id=post_id,
        criado_em=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

    comentario_dao = ComentarioDAO()
    comentario_dao.adicionar_comentario(comentario)

    return redirect(url_for('post', id=post_id))


@app.route('/editar_comentario/<int:id>', methods=['POST'])
def editar_comentario(id):
    if 'user' not in session:
        abort(403)

    novo_texto = request.form.get('novo_texto')
    comentario_dao = ComentarioDAO()

    comentario = comentario_dao.get_comentario_por_id(id)
    if not comentario or comentario.autor != session['user']['id']:
        abort(403)

    comentario_dao.editar_comentario(id, novo_texto)
    return redirect(url_for('post', id=comentario.postagem_id))


@app.route('/excluir_comentario/<int:id>', methods=['POST'])
def excluir_comentario(id):
    if 'user' not in session:
        abort(403)

    comentario_dao = ComentarioDAO()
    comentario = comentario_dao.get_comentario_por_id(id)

    if not comentario:
        abort(404)

    user_id = session['user']['id']
    is_admin = session['user']['is_adm']

    if comentario['autor'] != user_id and not is_admin:
        abort(403)

    comentario_dao.excluir_comentario(id)
    return redirect(url_for('post', id=comentario['postagem_id']))


@app.route('/ocultar_comentario/<int:id>', methods=['POST'])
def ocultar_comentario(id):
    if 'user' not in session or not session['user']['is_adm']:
        abort(403)

    comentario_dao = ComentarioDAO()
    comentario = comentario_dao.get_comentario_por_id(id)
    if not comentario:
        abort(404)

    comentario_dao.ocultar_comentario(id)
    return redirect(url_for('post', id=comentario['postagem_id']))


@app.route('/painel_admin')
def painel_admin():
    if 'user' not in session or not session['user'].get('is_adm', False):
        return redirect(url_for('home'))
    is_admin = session['user'].get('is_adm', False)
    return render_template('painel_admin.html', posts=posts, user=session['user'], is_admin=is_admin)


if __name__ == "__main__":
    app.run(debug=True)