import psycopg2
import pickle


class Database:
    def __init__(self):
        comando = pickle.load(open('loginbd.pkl', 'rb'))
        self.conn = psycopg2.connect(comando)
        self.cur = self.conn.cursor()

    def __str__(self):
        return "Banco de dados"

    def encerrar(self):
        self.cur.close()
        self.conn.close()

    def execute_query(self, query):
        self.cur.execute(query)
        self.conn.commit()

    def select(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()
