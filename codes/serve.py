import paho.mqtt.client as mqtt, paho.mqtt.publish as publish
import sqlite3
conn = sqlite3.connect('worksec.db')
cursor = conn.cursor()

topico = 'b'
topicop = 'c'

def dono(tag):
	cursor.execute("""select pessoa.nome from pessoa 
					  inner join pessoaequipamento on pessoa.idpessoa = pessoaequipamento.idpessoa
					  inner join equipamento on pessoaequipamento.idequipamento = equipamento.idequipamento 
					  where equipamento.tag = ?
				   """, (tag, ))
	for linha in cursor.fetchall():
		print(linha)
		return linha

def tags():
	i = []
	cursor.execute("""select tag from equipamento""")
	for linha in cursor.fetchall():
		tag = linha[0]
		if(selecsaida(tag)>selecentrada(tag)):
			i.append(tag)
	return i
			
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

def on_connect(client, userdata, flags, rc):
    client.subscribe(topico)


def on_message(client, userdata, msg):
	recived	 = str(msg.payload)
	recived = recived.strip('b')
	recived = recived.strip("'")
	print(recived)
	if(recived == "f"):
		listtags = tags()
		if(len(listtags) == 0):
			publish.single(topicop, "todos os equipamentos estão nos armários", hostname='iot.eclipse.org')
		else:	
			for i in range(len(listtags)):
				nome = dono(listtags[i])
				publish.single(topicop, nome[0], hostname='iot.eclipse.org')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('iot.eclipse.org', 1883, 60)
client.loop_forever()
conn.close()
