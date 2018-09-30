import datetime
import serial
import sqlite3
conn = sqlite3.connect('worksec.db')
cursor = conn.cursor()
porta = 'COM4'
velocidade = 9600
conexao = serial.Serial(porta, velocidade)

def readtag():
	tag = str(conexao.readline().decode('ascii'))
	print("tag len"+ str(len(tag)))
	tag = tag.lower()
	tag = tag.replace(tag[12],"")
	return tag

def selecsaida(tag):
	i=0
	cursor.execute("""select * from saida inner join equipamento on saida.idequipamento = equipamento.idequipamento where equipamento.tag = ?""", (tag,))
	for linha in cursor.fetchall():
		i=i+1
	return i
	
def selecentrada(tag):
	i=0
	cursor.execute("""select * from entrada inner join equipamento on entrada.idequipamento = equipamento.idequipamento where equipamento.tag = ?""", (tag,))
	for linha in cursor.fetchall():
		i=i+1
	return i
	
def saida(idpessoa, idequipamento):
	cursor.execute('INSERT INTO saida(idsaida, idequipamento, idpessoa) VALUES ((select max(idsaida) from saida)+1, ?, ?)', (idequipamento, idpessoa,))
	conn.commit()
	
def entrada(idpessoa, idequipamento):
	cursor.execute('INSERT INTO entrada(identrada, idequipamento, idpessoa) VALUES ((select max(identrada) from entrada)+1, ?, ?)', (idequipamento, idpessoa,))
	conn.commit()
	
'''def inser(tag):
	cursor.execute('INSERT INTO equipamento(idequipamento, descricao, tag) VALUES (3, "capacete", ?)', (tag,))
	conn.commit()
	conn.close()'''
	
def selec(tag):
	cursor.execute("""select pessoa.idpessoa, equipamento.idequipamento, equipamento.validade from pessoa 
					  inner join pessoaequipamento on pessoa.idpessoa = pessoaequipamento.idpessoa
					  inner join equipamento on pessoaequipamento.idequipamento = equipamento.idequipamento where equipamento.tag = ?""", (tag,))
	for linha in cursor.fetchall():
		print(linha)
		if(selecsaida(tag)>selecentrada(tag)):
			if(linha[2] < "2018-09-30"):
				conexao.write(b"asdasdasd")
			entrada(linha[0], linha[1])
		else:
			if(linha[2] < "2018-09-30"):
				conexao.write(b"asdasdasd")
			saida(linha[0], linha[1])
while True:
	selec(readtag())
conn.close()
	
