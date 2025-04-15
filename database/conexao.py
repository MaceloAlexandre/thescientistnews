import  psycopg2

def conectardb():
    conexao = psycopg2.connect(database="TheScientistNews",
                               host="localhost",
                               user="postgres",
                               password="Macelo321",
                               port="5432")
    return conexao