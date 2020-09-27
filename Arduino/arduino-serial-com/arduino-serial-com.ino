#define simonBtn0 39
#define simonBtn1 37
#define simonBtn2 35
#define simonBtn3 33
#define simonLum1 47
#define simonLum2 45
#define simonLum3 43
#define simonLum4 41
#define simonLumVictoire 51
#define simonLumErreur 53



#define filErreur 52
#define filVictoire 50
#define fil1 46
#define fil2 44
#define fil3 42
#define fil4 40
#define fil5 38

#define calcLumErreur 36
#define calcLumVictoire 34
#define calcLum1 30
#define calcLum2 28
#define calcLum3 26
#define calcLum4 24

#define symboleVictoire 69
#define symboleErreur 68
#define symboleLum0 66
#define symboleLum1 65
#define symboleLum2 64
#define symboleLum3 63U
#define symboleBtn0 61
#define symboleBtn1 60
#define symboleBtn2 59
#define symboleBtn3 58


#define BoutonVictoire 29
#define BoutonErreur 31
#define BoutonBandeRouge 2
#define BoutonBandeVert 3
#define BoutonBandeBleu 4
#define BoutonContact 25


#define chronoErr1 18
#define chronoErr2 17
#define chronoErr3 16
#define chronoErr4 15
#define chronoSon 19
 



#include <Wire.h> // Enable this line if using Arduino Uno, Mega, etc.
#include <Adafruit_GFX.h>
#include "Adafruit_LEDBackpack.h"

Adafruit_7segment matrix = Adafruit_7segment();
int etatBlink = 0;
int etatLum = 5;


void setup() {
  Serial.begin(19200);
  Serial.setTimeout(500); 

  matrix.begin(0x70);
  matrix.setBrightness(5);
  matrix.blinkRate(0);


  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(simonLum1, OUTPUT);
  pinMode(simonLum2, OUTPUT);
  pinMode(simonLum3, OUTPUT);
  pinMode(simonLum4, OUTPUT);
  pinMode(simonLumVictoire, OUTPUT);
  pinMode(simonLumErreur, OUTPUT);
  
  pinMode(calcLumErreur, OUTPUT);
  pinMode(calcLumVictoire, OUTPUT);
  pinMode(calcLum1, OUTPUT);
  pinMode(calcLum2, OUTPUT);
  pinMode(calcLum3, OUTPUT);
  pinMode(calcLum4, OUTPUT);

  pinMode(filErreur, OUTPUT);
  pinMode(filVictoire, OUTPUT);

  pinMode(symboleLum0, OUTPUT);
  pinMode(symboleLum1, OUTPUT);
  pinMode(symboleLum2, OUTPUT);
  pinMode(symboleLum3, OUTPUT);
  pinMode(symboleVictoire, OUTPUT);
  pinMode(symboleErreur, OUTPUT);
  
  pinMode(BoutonVictoire, OUTPUT);
  pinMode(BoutonErreur, OUTPUT);
  pinMode(BoutonBandeRouge, OUTPUT);
  pinMode(BoutonBandeVert, OUTPUT);
  pinMode(BoutonBandeBleu, OUTPUT);
  pinMode(chronoErr1, OUTPUT);
  pinMode(chronoErr2, OUTPUT);
  pinMode(chronoErr3, OUTPUT);
  pinMode(chronoErr4, OUTPUT);

  pinMode(fil1, INPUT_PULLUP);
  pinMode(fil2, INPUT_PULLUP);
  pinMode(fil3, INPUT_PULLUP);
  pinMode(fil4, INPUT_PULLUP);
  pinMode(fil5, INPUT_PULLUP);

  pinMode(simonBtn0, INPUT_PULLUP);
  pinMode(simonBtn1, INPUT_PULLUP);
  pinMode(simonBtn2, INPUT_PULLUP);
  pinMode(simonBtn3, INPUT_PULLUP);

  pinMode(symboleBtn0, INPUT_PULLUP);
  pinMode(symboleBtn1, INPUT_PULLUP);
  pinMode(symboleBtn2, INPUT_PULLUP);
  pinMode(symboleBtn3, INPUT_PULLUP);

  pinMode(BoutonContact, INPUT_PULLUP);

  pinMode(chronoSon, INPUT_PULLUP);




  matrix.writeDigitNum(0, 0, 0);
  matrix.writeDigitNum(1, 0, 0);
  matrix.writeDigitNum(3, 0, 0);
  matrix.writeDigitNum(4, 0, 0);
  matrix.drawColon(1);
  matrix.writeDisplay();
  digitalWrite(simonLum1, 1);
  digitalWrite(simonLum2, 1);
  digitalWrite(simonLum3, 1);
  digitalWrite(simonLum4, 1);
  digitalWrite(simonLumVictoire, 1);
  digitalWrite(simonLumErreur, 1);
  
  digitalWrite(calcLumErreur, 1);
  digitalWrite(calcLumVictoire, 1);
  digitalWrite(calcLum1, 1);
  digitalWrite(calcLum2, 1);
  digitalWrite(calcLum3, 1);
  digitalWrite(calcLum4, 1);

  digitalWrite(symboleVictoire, 1);
  digitalWrite(symboleErreur, 1);
  digitalWrite(symboleLum0, 1);
  digitalWrite(symboleLum1, 1);
  digitalWrite(symboleLum2, 1);
  digitalWrite(symboleLum3, 1);

  digitalWrite(filVictoire, 1);
  digitalWrite(filErreur, 1);
  digitalWrite(BoutonVictoire, 1);
  digitalWrite(BoutonErreur, 1);
  digitalWrite(BoutonBandeRouge, 1);
  digitalWrite(BoutonBandeVert, 1);
  digitalWrite(BoutonBandeBleu, 1);
  digitalWrite(chronoErr1, 1);
  digitalWrite(chronoErr2, 1);
  digitalWrite(chronoErr3, 1);
  digitalWrite(chronoErr4, 1);
  
}
void loop() {
  
  if (Serial.available() > 0) {

    String data = Serial.readStringUntil('\n');

    // Traitement Sortie
    for(int i=0;i<data.length();i++){
      data[i] = data[i] - '0';
    }
    
    digitalWrite(simonLum1, data[0]);
    digitalWrite(simonLum2, data[1]);
    digitalWrite(simonLum3, data[2]);
    digitalWrite(simonLum4, data[3]);
    digitalWrite(simonLumVictoire, data[4]);
    digitalWrite(simonLumErreur, data[5]);
    
    digitalWrite(calcLumErreur, data[6]);
    digitalWrite(calcLumVictoire, data[7]);
    digitalWrite(calcLum1, data[8]);
    digitalWrite(calcLum2, data[9]);
    digitalWrite(calcLum3, data[10]);
    digitalWrite(calcLum4, data[11]);

    digitalWrite(symboleVictoire, data[12]);
    digitalWrite(symboleErreur, data[13]);
    digitalWrite(symboleLum0, data[14]);
    digitalWrite(symboleLum1, data[15]);
    digitalWrite(symboleLum2, data[16]);
    digitalWrite(symboleLum3, data[17]);

    digitalWrite(filVictoire, data[18]);
    digitalWrite(filErreur, data[19]);

    if(etatLum != 0){

      byte lala = data[20] ;
      if(lala == 0xfd){ // signe "-"
        matrix.writeDigitRaw(0,0b0000000001000000);
      }else{    
        matrix.writeDigitNum(0, data[20], 0);   
      }
      matrix.writeDigitNum(1, data[21], 0);
      matrix.writeDigitNum(3, data[22], 0);
      matrix.writeDigitNum(4, data[23], 0);
      matrix.drawColon(data[24]);
      matrix.writeDisplay();
    }
    digitalWrite(BoutonVictoire, data[25]);
    digitalWrite(BoutonErreur, data[26]);
    digitalWrite(BoutonBandeRouge, data[27]);
    digitalWrite(BoutonBandeVert, data[28]);
    digitalWrite(BoutonBandeBleu, data[29]);
      
    digitalWrite(chronoErr1, data[30]);
    digitalWrite(chronoErr2, data[31]);
    digitalWrite(chronoErr3, data[32]);
    digitalWrite(chronoErr4, data[33]);
    
    if(etatBlink != data[34]){
      matrix.blinkRate( data[34]);
      etatBlink = data[34];
    }
    
    if(data[35] == 0){
      if(etatLum != 0){
        matrix.setBrightness(0);
        matrix.writeDigitRaw(0,0b0000000000000000);
        matrix.writeDigitRaw(1,0b0000000000000000);
        matrix.writeDigitRaw(2,0b0000000000000000);
        matrix.writeDigitRaw(3,0b0000000000000000);
        matrix.writeDigitRaw(4,0b0000000000000000);
        matrix.writeDisplay();
        etatLum = 0;
      }
    }
    else if(data[35] == 1){
      if(etatLum != 3){
        matrix.setBrightness(3);
        etatLum = 3;
      }
    } 
    else{
      if(etatLum != 15){
        matrix.setBrightness(15);
        etatLum = 15;
      }
    }

    


    // Traitement entree
    Serial.print(digitalRead(simonBtn0));
    Serial.print(digitalRead(simonBtn1));
    Serial.print(digitalRead(simonBtn2));
    Serial.print(digitalRead(simonBtn3));

    Serial.print(digitalRead(symboleBtn0));
    Serial.print(digitalRead(symboleBtn1));
    Serial.print(digitalRead(symboleBtn2));
    Serial.print(digitalRead(symboleBtn3));

    Serial.print(digitalRead(fil1));
    Serial.print(digitalRead(fil2));
    Serial.print(digitalRead(fil3));
    Serial.print(digitalRead(fil4));
    Serial.print(digitalRead(fil5));
    Serial.print(digitalRead(BoutonContact));
    Serial.print(digitalRead(chronoSon));

    Serial.print('\n');

  }
  delay(2);
}
