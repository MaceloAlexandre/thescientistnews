from flask import *
from werkzeug.utils import secure_filename
import os
import datetime as datetime


app = Flask(__name__)
app.secret_key = 'MySecretKey*123'


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
        'nome': 'Sydney Cristian',
        'email': 'sydney@sydney.com',
        'senha': '123',
        'is_adm': True # Este é um admin 
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
    "materia": 
        """O Brasil está prestes a dar um salto significativo no monitoramento ambiental com o lançamento de um novo satélite equipado com tecnologia de ponta. 

        O equipamento será capaz de mapear o desmatamento e detectar queimadas em tempo real, mesmo sob cobertura de nuvens – uma inovação que promete transformar a vigilância das florestas brasileiras.

        Desenvolvido em parceria entre o Instituto Nacional de Pesquisas Espaciais (INPE) e empresas nacionais do setor aeroespacial, o satélite conta com sensores infravermelhos de alta resolução, capazes de capturar alterações na vegetação e identificar focos de calor com precisão milimétrica. A tecnologia infravermelha permite que o monitoramento seja realizado 24 horas por dia, independentemente das condições climáticas ou da luminosidade.

        Segundo especialistas, essa nova ferramenta será crucial para reforçar o combate ao desmatamento ilegal na Amazônia e em outras áreas de preservação. 
        
        Com dados atualizados em tempo real, as autoridades ambientais poderão agir com muito mais agilidade, enviando equipes de fiscalização aos locais exatos onde ocorrerem desmatamentos ou queimadas.

        O uso de satélites com tecnologia de imageamento térmico representa um avanço histórico no controle ambiental. 
        “A velocidade e a precisão com que teremos acesso às informações mudarão completamente a forma como enfrentamos crimes ambientais”, afirma Ana Lucia Mendes, pesquisadora do INPE.

        Além do impacto direto na fiscalização, o sistema permitirá maior transparência no acesso às informações. 
        Os dados coletados serão disponibilizados para o público, organizações ambientais e universidades, fomentando pesquisas e pressionando por ações mais eficazes por parte do poder público.

        O lançamento do satélite está previsto para o primeiro semestre de 2024, a partir do Centro de Lançamento de Alcântara, no Maranhão. 
        Se bem-sucedido, o Brasil entrará para o seleto grupo de países com capacidade própria de monitoramento ambiental em tempo real por meio de satélites.

        Com a floresta amazônica enfrentando níveis alarmantes de desmatamento, iniciativas como essa são vistas como essenciais para a preservação dos biomas e o cumprimento das metas climáticas internacionais assumidas pelo país."""
    ,
    "autor": "Carlos Ribeiro",
    "data_postagem": datetime.datetime(2023, 10, 16, 11, 20),
    "categoria": "tecnologia",
    "midia": "imagens/satilite.png"
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
            print(session['user'])
            print(session['user']['nome'])
            
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
        midia = request.files.get('midia')
        caminho_midia = None

        if midia and allowed_file(midia.filename):
            filename = secure_filename(midia.filename)
            midia.save(os.path.join(UPLOAD_FOLDER, filename))
            caminho_midia = f'uploads/{filename}'  # caminho corrigido para URL

        novo_post = {
            "id": len(posts) + 1,
            "titulo": request.form.get('titulo'),
            "texto": request.form.get('resumo'),
            "materia": request.form.get('materia'),
            "autor": session['user']['nome'],
            "data_postagem": datetime.datetime.now(),
            "categoria": request.form.get('categoria'),
            "midia": caminho_midia
        }

        posts.append(novo_post)
        print(posts)
        return redirect(url_for('painel_admin'))

    return render_template('painel_admin.html')


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
    is_admin = session['user'].get('is_adm', False)
    return render_template('painel_admin.html', posts=posts, user=session['user'], is_admin=is_admin)


if __name__ == "__main__":
    app.run(debug=True)