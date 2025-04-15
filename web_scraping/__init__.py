import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Agora você pode importar modelos normalmente
from models.postagem import Postagem

import requests
from bs4 import BeautifulSoup
import datetime
from dao import PostagemDAO


URL_SITE_ORIGINAL = "https://olhardigital.com.br"

CLASSES_INDESEJADAS = ["oft-itens", "sn-ad", "ads", "advertisement", "promo", "sponsored"]

def obter_links_olhar_digital():
    response = requests.get(URL_SITE_ORIGINAL)
    soup = BeautifulSoup(response.text, "html.parser")
    
    resultados = []
    posts = soup.select("a.p-item")

    for post in posts:
        # Ignora se o post tiver qualquer classe indesejada
        if any(classe in post.get("class", []) for classe in CLASSES_INDESEJADAS):
            continue

        if 'sponsored' in post.get("rel", []):
            continue  # Ignora links patrocinados

        link = post.get("href")
        if not link or not link.startswith("https"):
            continue

        titulo = post.get("title") or post.text.strip()
        imagem_tag = post.find("img")
        imagem = imagem_tag["src"] if imagem_tag and imagem_tag.has_attr("src") else ""

        resultados.append({
            "link": link,
            "titulo": titulo,
            "imagem": imagem
        })

    print(f"Total de links encontrados: {len(resultados)}")
    return resultados


"""a = obter_links_olhar_digital()
for i, post in enumerate(a):
    print(f"[{i}] {post['link']} - {post['titulo']}")
    print(f"Imagem: {post['imagem']}")
    print("-" * 40)
"""

def extrair_conteudo_post(link, autor, nome_autor):
    resp = requests.get(link)
    soup = BeautifulSoup(resp.text, "html.parser")

    if soup.find_all("div", class_="oft-itens"):
        print(f"Link ignorado (anúncio): {link}")
        return None

    titulo_el = soup.find("h1")
    titulo = titulo_el.text.strip() if titulo_el else "Título não encontrado"

    artigo = soup.find("article", class_="sng-cnt wp-embed-responsive")
    if not artigo:
        return None

    for tag in artigo.find_all(["iframe", "script", "div"], class_=["oft-itens", "sn-ad", "ads", "advertisement", "promo", "sponsored"]):
        tag.decompose()

     # Remove o bloco "Leia mais:" com os links
    for p_tag in artigo.find_all("p"):
        strong = p_tag.find("strong")
        if strong:
            texto_strong = strong.get_text(strip=True).lower()
            # Verifica múltiplas variações (com/sem dois pontos, maiúsculas, etc)
            if any(termo in texto_strong for termo in ["leia mais", "leia também"]):
                ul_tag = p_tag.find_next_sibling("ul")
                p_tag.decompose()
                if ul_tag:
                    ul_tag.decompose()
                continue  # Pula para o próximo parágrafo após remoção


    resumo_div = soup.find('div', class_=lambda x: x and 'sng-exc' in x.split())
    resumo = resumo_div.text.strip() if resumo_div else "Resumo não encontrado"

    conteudo_formatado = []
    for tag in artigo.find_all(['h2', 'h3', 'p', 'li'], recursive=True):
        texto = tag.get_text(strip=True)
        if not texto:
            continue
        if tag.name == 'h2':
            conteudo_formatado.append(f"<h2>{texto}</h2>")
        elif tag.name == 'h3':
            conteudo_formatado.append(f"<h3>{texto}</h3>")
        else:
            conteudo_formatado.append(f"{texto}\n")

    corpo_formatado = "\n".join(conteudo_formatado)

    imagem = ""
    figure = soup.find("figure", class_="sng-img")  # Busca no HTML todo, não só no artigo
    if figure:
        img_tag = figure.find("img")
        if img_tag and img_tag.get("src"):
            imagem = img_tag["src"]
        else:
            # Se não achar <img>, tenta pegar de <source>
            source = figure.find("source")
            if source and source.get("srcset"):
                imagem = source["srcset"].split()[0]  # Pega a primeira URL do srcset

    if not imagem:
        figura_wp = artigo.find("figure", class_="wp-block-image")
        if figura_wp:
            img_tag = figura_wp.find("img")
            if img_tag and img_tag.get("src"):
                imagem = img_tag["src"]

    # 3ª Tentativa: Fallback genérico (primeira imagem do artigo)
    if not imagem:
        for img in artigo.find_all("img"):
            if img.get("src"):
                # Filtra imagens muito pequenas (opcional)
                width = int(img.get("width", 0))
                if width >= 300:  # Ignora thumbnails
                    imagem = img["src"]
                    break

    # Agora você pode usar a variável `imagem` no resto da sua função
    if imagem:
        print(f"Imagem extraída: {imagem}")
        # ... faça algo com a imagem (ex: salvar no banco de dados, etc.)
    else:
        print("Nenhuma imagem encontrada no artigo.")

    categoria = "Não informado"

    data_postagem = datetime.datetime.now()

    postagem = Postagem(
        titulo=titulo,
        resumo=resumo,
        materia=corpo_formatado,
        midia=imagem,
        data_postagem=data_postagem,
        autor=autor,
        categoria=categoria,
        nome_autor=nome_autor

    )

    return postagem


posts = obter_links_olhar_digital()
link = "https://olhardigital.com.br/2025/04/13/ciencia-e-espaco/ia-prevendo-assassinatos-reino-unido-analisa-tecnologia-minority-report/" \

extrair_conteudo_post(link, 1, "Macelo Alexandre")

if not posts:
    print("Nenhum link encontrado.")
    sys.exit()

""" Exibe os links com índice
print("\nLinks encontrados:\n")
for i, link in enumerate(posts):
    print(f"[{i}] {link}")
"""

"""if __name__ == "__main__":
    
    # Pergunta qual link o usuário deseja usar
    while True:
        try:
            indice = int(input("\nDigite o número do link que deseja usar: "))
            if 0 <= indice < len(posts):
                break
            else:
                print("Índice inválido. Tente novamente.")
        except ValueError:
            print("Por favor, digite um número válido.")

    link_post = posts[indice]["link"]
    postagem = extrair_conteudo_post(link_post, 1, "Macelo Alexandre")


    print(postagem.titulo)
    print(postagem.resumo)
    print(postagem.midia)
    print(postagem.data_postagem)
    print(postagem.autor)
    print(f'esse é o nome do autor {postagem.nome_autor}')


    perguntar = input('Você deseja salvar a postagem? (s/n): ')
    if perguntar.lower() == 's':
        try:
            dao = PostagemDAO()
            dao.salvar_postagem(postagem)
            print('deu certo')
        except Exception as e:
            print(f'Erro ao salvar postagem: {e}', 'error')
"""