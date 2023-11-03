import psycopg2
import datetime as date

class Conexao:

    _db = None
    _rs = []
    def __init__(self, hst, db, usr, pwd):
        try:
            self._db = psycopg2.connect(host= hst, database= db, user= usr, password= pwd)
            print("Conexão bem sucedida![Dados]")
        except Exception as e:
            print("Falha na conexão...[Dados]")
            # print(type(e))
            # print(e.args)
            print(e)            
    
    def fecharConexao(self) -> None:
        try:
            self._db.close()
            print("Conexão encerrada com sucesso![Dados]")
        except Exception as e:
            print("Falha ao executar comando..[Dados]",e)
    
    def gravarColeta(self, valor, ph:bool):
        if self.necessitaGravar():
            insert_query = "INSERT INTO Dados(data_coleta, hora_coleta, valor, ph) VALUES(%s, %s, %s, %s)"
            if ph:
                values = (date.date.today(), date.datetime.now().time().strftime('%H:%M:%S') ,valor, True)
            else:
                values = (date.date.today(), date.datetime.now().time().strftime('%H:%M:%S') ,valor, False)

            try:
                cur = self._db.cursor()
                cur.execute(insert_query, values)
                self._db.commit()
                cur.close()
                print("Novo dado adicionado!")           
            except Exception as e:
                print("Problema na inserção...",e)
        else:
            lst_check = self.horaUltimaGravacao()[0][0]
            hora_nova = (date.datetime.combine(date.datetime.min, lst_check) + date.timedelta(minutes=0.5)).time()
            print("Ultima coleta realizada às "+ str(lst_check) + "\nPróxima coleta será às "+str(hora_nova))
    
    def horaUltimaGravacao(self):
        SELECT_QUERY = "Select hora_coleta from Dados Where id_coleta = (Select max(id_coleta) from Dados)"
        rs = None
        try:
            cur = self._db.cursor()
            cur.execute(SELECT_QUERY)
            rs = cur.fetchall()
            cur.close()
            return rs           
        except Exception as e:
            print("Erro: ", e)
            return None
    def mostrarUltimoValor(self):
        SELECT_QUERY = "Select valor from dados where id_coleta = (select max(id_coleta) from dados)"
        rs = None
        try:
            cur = self._db.cursor()
            cur.execute(SELECT_QUERY)
            rs = cur.fetchall()
            cur.close()
            return rs           
        except Exception as e:
            print("Erro: ", e)
            return None
    def necessitaGravar(self)->bool:
        lst_check = self.horaUltimaGravacao()[0][0]
        hora1 = date.datetime.strptime(str(lst_check), "%H:%M:%S").time()
        hora2 = date.datetime.now().time()
        diferenca_horaria = (hora2.hour * 3600 + hora2.minute * 60 + hora2.second - (hora1.hour * 3600 + hora1.minute * 60 + hora1.second))/3600
        # 5 min = 0.08 horas
        # 30 segundos = 0.00833333 horas
        if diferenca_horaria > 0.00833333:
            return True
        else:
            return False
           

