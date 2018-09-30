import paho.mqtt.client as mqtt, paho.mqtt.publish as publish
topico = 'a'
for i in range(10):
	send = input("mensagem: ")
	publish.single(topico, send, hostname='iot.eclipse.org')
