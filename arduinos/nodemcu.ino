#include <ESP8266WiFi.h> 
#include <PubSubClient.h>

const char* SSID = "luan";                // SSID / nome da rede WiFi que deseja se conectar
const char* PASSWORD = "12345678";  // Senha da rede WiFi que deseja se conectar
WiFiClient wifiClient;  

const char* BROKER_MQTT = "iot.eclipse.org"; //URL do broker MQTT que se deseja utilizar
int BROKER_PORT = 1883;                      // Porta do Broker MQTT

#define ID_MQTT "bco1"
#define TOPICO "a"
PubSubClient MQTT(wifiClient);        // Instancia o Cliente MQTT passando o objeto espClient

void mantemConexoes();  //Garante que as conexoes com WiFi e MQTT Broker se mantenham ativas
void conectaWiFi();     //Faz conexão com WiFi
void conectaMQTT();     //Faz conexão com Broker MQTT


void setup() {
  pinMode(D0,OUTPUT);
  pinMode(D1,OUTPUT);
  pinMode(D2,OUTPUT);  
  Serial.begin(115200);
  conectaWiFi();
  MQTT.setServer(BROKER_MQTT, BROKER_PORT);  
  MQTT.setCallback(recebePacote); 
}

void loop() {
  digitalWrite(D0,0);
  digitalWrite(D1,0);
  digitalWrite(D2,255);  
  mantemConexoes();
  if (!MQTT.connected()) 
       conectaMQTT(); 
  MQTT.loop();
  
}

void mantemConexoes() {
  if (WiFi.status() == WL_CONNECTED) {
     return;
  }
    
    conectaWiFi(); //se não há conexão com o WiFI, a conexão é refeita
}

void conectaWiFi() {


        
  Serial.print("Conectando-se na rede: ");
  Serial.print(SSID);
  Serial.println("  Aguarde!");

  WiFi.begin(SSID, PASSWORD); // Conecta na rede WI-FI  
  while (WiFi.status() != WL_CONNECTED) {
      delay(100);
      Serial.print(".");
  }
  
  Serial.println();
  Serial.print("Conectado com sucesso, na rede: ");
  Serial.print(SSID);  
  Serial.print("  IP obtido: ");
  Serial.println(WiFi.localIP()); 
}

void conectaMQTT() { 
    while (!MQTT.connected()) {
        Serial.print("Conectando ao Broker MQTT: ");
        Serial.println(BROKER_MQTT);
        if (MQTT.connect(ID_MQTT)) {
            Serial.println("Conectado ao Broker com sucesso!");
            MQTT.subscribe(TOPICO);
        } 
        else {
            Serial.println("Noo foi possivel se conectar ao broker.");
            Serial.println("Nova tentatica de conexao em 10s");
            delay(10000);
        }
    }
}

void recebePacote(char* topic, byte* payload, unsigned int length) 
{
      String msg;
    //obtem a string do payload recebido
    for(int i = 0; i < length; i++) 
    {
       char c = (char)payload[i];
       msg += c;
    }
    if (msg == "0") {
       Serial.println("não está apropriado");
       digitalWrite(D0,255);
       digitalWrite(D1,0);
       digitalWrite(D2,0);       
    }else{
      if (msg == "1") {
         Serial.println("está apropriado");
         digitalWrite(D0,0);
         digitalWrite(D1,255);
         digitalWrite(D2,0);       
      }
    }
      delay(5000);
   
    
}

