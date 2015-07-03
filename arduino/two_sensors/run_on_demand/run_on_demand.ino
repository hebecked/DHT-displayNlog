#include "DHT.h"

#define DHTPIN 12     // what pin did you connect data to
#define DHTPIN2 11
 
// Uncomment whatever type you're using!
//#define DHTTYPE DHT11   // DHT 11 
#define DHTTYPE DHT22   // DHT 22  (AM2302)
//#define DHTTYPE DHT21   // DHT 21 (AM2301)

// Initialize DHT sensor for normal 16mhz Arduino
DHT dht(DHTPIN, DHTTYPE);
DHT dht2(DHTPIN2, DHTTYPE);

int what;
int i;
float h=0;
float t=0;
float h2=0;
float t2=0;

void setup() {
/*  pinMode(DHTPIN, INPUT);
  digitalWrite(DHTPIN, HIGH);
  pinMode(DHTPIN2, INPUT);
  digitalWrite(DHTPIN2, HIGH);*/
//Some work arround
pinMode(10, OUTPUT);
digitalWrite(10, HIGH);
//end work arround
  
  Serial.begin(9600);
  delay(250);
  Serial.println("Start!");
  dht.begin();
  dht2.begin();
}

void loop() {
  delay(250);
  
  if(Serial.available() > 0){
    what = Serial.read();
    if(what=='h'){
        Serial.print(h);
    }
    if(what=='j'){
        Serial.print(h2);
    }
    if(what=='t'){
        Serial.print(t);
    }
    if(what=='z'){
        Serial.print(t2);
    }
    if(what=='H'){
        Serial.print("Humidity: ");
        Serial.print(h);
        Serial.print(" %\n");
        Serial.print("Humidity 2: ");
        Serial.print(h2);
        Serial.print(" %\n");
    }
    if(what=='T'){
        Serial.print("Temperature: ");
        Serial.print(t);
        Serial.print(" C\n");
        Serial.print("Temperature 2: ");
        Serial.print(t2);
        Serial.print(" C\n");
    }
    if(what!='h' && what!='t' && what!='H' && what!='T'&& what!='j' && what!='z' && what!='Z' && what!='J'){
        Serial.print("Send 'h' for humidity in percent\nOr send 't' for temperature in Celsius\nCapital letters for human readable output\n");
    }
  }

  if(i>7){
    // Read humidity in percent
    h = dht.readHumidity();
    h2 = dht2.readHumidity();
    // Read temperature as Celsius
    t = dht.readTemperature();
    t2 = dht2.readTemperature();
    // Check if any reads failed and exit early (to try again).
    if (isnan(h) || isnan(t) || isnan(h2) || isnan(t2)) {
      Serial.println("Error!");
      return;
    }
    i=0;
  }
  i++;
}
