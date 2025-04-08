import psycopg2

def conectardb():
    conexao = psycopg2.connect(database="db_gestor_de_eventos",
                               host="localhost",
                               user="postgres",
                               password="Macelo321",
                               port="5432")
    return conexao