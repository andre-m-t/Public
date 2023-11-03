import serial
import re 
from DAO import phDAO 
import time
import os

# DADOS PARA CONEXÃO COM O BANCO
hst = "YourHost"
dB = "YourDbName"
usr = "Username"
pwd_b = "Password"
# ABRINDO CONEXAO COM O BANCO 
con = phDAO.Conexao(hst= hst,db= dB, usr= usr,pwd= pwd_b)

# Configura a porta serial (altere a porta COMx conforme necessário)
ser = serial.Serial('COM5', 9600)

# Abre um arquivo TXT para escrita
with open('registro.txt', 'w') as arquivo:
    try:
        parametro = "ph"
        
        while True:
            texto = ser.readline().decode().strip()
            num = re.findall(r'\d+\.\d+', texto)
            if parametro.lower() in texto.lower():
                con.gravarColeta(num[0], True)
                print("Ph atual: " + str(con.mostrarUltimoValor()[0][0]))
            else:
                con.gravarColeta(num[0], False)
                print("Ph atual: " + str(con.mostrarUltimoValor()[0][0]))
            time.sleep(10)
            os.system("cls")
        # while True:
        #     # Lê dados da porta serial
        #     valor = ser.readline().decode().strip()
        #     # Escreve os dados no arquivo TXT
        #     num = re.findall(r'\d+\.\d+', valor)
        #     # for n in num:
        #     arquivo.write(str(num[0])+"\n")
        #     arquivo.flush()  # Garante que os dados sejam escritos imediatamente no arquivo
    except KeyboardInterrupt:
        pass
con.fecharConexao()
# Fecha a porta serial
ser.close()