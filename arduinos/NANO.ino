//Programa : RFID - Controle de Acesso leitor RFID
//Autor : FILIPEFLOP

#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 10
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance.

void setup() 
{
  Serial.begin(9600); // Inicia a serial
  SPI.begin();    // Inicia  SPI bus
  mfrc522.PCD_Init();
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  digitalWrite(2,0);
  digitalWrite(3,0);
  digitalWrite(4,255);  
}

void loop() 
{  
  // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent()) 
  {
    return;
  }
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) 
  {
    return;
  }
  //Mostra UID na serial
  String conteudo="";
  byte letra;
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
    conteudo.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : " "));
    conteudo.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  Serial.print(conteudo.substring(1));
  Serial.println("");
  delay(500);
  if(Serial.available()>0){
    digitalWrite(2,0);
    digitalWrite(3,255);
    digitalWrite(4,0);
  }else{
    digitalWrite(2,255);
    digitalWrite(3,0);
    digitalWrite(4,0);
  } 
  delay(1000);
  digitalWrite(2,0);
  digitalWrite(3,0);
  digitalWrite(4,255);
} 

