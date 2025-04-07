from flask import *
from werkzeug.utils import secure_filename
import os
import datetime as datetime


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = 'MySecretKey*123'


usuarios = [
    {
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
        'nome': 'Usuário Comum 2',
        'email': 'usuario2@email.com',
        'senha': 'senha456',
        'is_adm': False
    }
]


posts = [
    {
        "id": 1,
        "titulo": "Descoberta revolucionária na física quântica",
        "texto": "Cientistas confirmam teletransporte de partículas a 1.200 km de distância...",
        "autor": "Alexandre .M",
        "data_postagem": datetime.datetime(2023, 10, 15, 14, 30),
        "categoria": "fisica",
        "midia": "imagens/fisica.png"
    },
    {
        "id": 2,
        "titulo": "Novo tratamento para Alzheimer mostra eficácia em testes",
        "texto": "Estudo publicado na Nature Medicine revela...",
        "autor": "Ana Souza",
        "data_postagem": datetime.datetime(2023, 10, 14, 9, 15),
        "categoria": "biologia",
        "midia": "imagens/featured3.png"
    },
     {
        "id": 3,
        "titulo": "Satélite brasileiro mapeará desmatamento em tempo real",
        "texto": "Equipamento com tecnologia infravermelha identificará queimadas mesmo sob nuvens...",
        "autor": "Carlos Ribeiro",
        "data_postagem": datetime.datetime(2023, 10, 16, 11, 20),
        "categoria": "tecnologia",
        "midia": "imagens/satilite.png"  # Exemplo com mídia
    },
    {
        "id": 4,
        "titulo": "Vulcão em Marte pode ter entrado em erupção há 50 mil anos",
        "texto": "Dados da sonda MRO sugerem atividade vulcânica recente no planeta vermelho...",
        "autor": "Juliana Santos",
        "data_postagem": datetime.datetime(2023, 10, 13, 16, 45),
        "categoria": "astronomia",
        "midia": "imagens/monte.png"
    }
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

        # Procura o usuário na lista
        usuario_encontrado = None
        for usuario in usuarios:
            if usuario['email'] == email and usuario['senha'] == senha:
                usuario_encontrado = usuario
                break

        if usuario_encontrado:
            # Armazena informações na sessão
            session['user'] = {
                'nome': usuario_encontrado['nome'],
                'email': usuario_encontrado['email'],
                'is_adm': usuario_encontrado['is_adm']
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
        if senha == senha2:
            flash('Cadastro realizado com sucesso', 'success')
            return redirect(url_for('login'))
 
    
    return render_template('registro.html')

@app.route('/iframeposts')
def iframeposts():
    return render_template('iframeposts.html', posts=posts)
    

@app.route('/postar', methods=['POST'])
def postar():
    if request.method == 'POST':
        novo_post = {
            "id": len(posts) + 1,
            "titulo": request.form.get('titulo'),
            "texto": request.form.get('texto'),
            "autor": "Usuário Teste",  # Simulado
            "data_postagem": datetime.datetime.now(),
            "categoria": request.form.get('categoria'),
            "midia": None 
        }
        posts.append(novo_post)
    return redirect(url_for('home'))

@app.route('/post/<int:id>')
def post(id):
    post = posts[id - 1] if id <= len(posts) else None
    if post is None:
        return "Post não encontrado", 404
    return render_template('post.html', post=post)

@app.route('/painel_admin')
def painel_admin():
    if 'user' not in session or not session['user'].get('is_adm', False):
        return redirect(url_for('home'))
    
    return render_template('painel_admin.html', posts=posts, user=session['user'])
if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)