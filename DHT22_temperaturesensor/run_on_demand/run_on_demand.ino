#include "DHT.h"

#define DHTPIN 12     // what pin did you connect data to

// Uncomment whatever type you're using!
//#define DHTTYPE DHT11   // DHT 11 
#define DHTTYPE DHT22   // DHT 22  (AM2302)
//#define DHTTYPE DHT21   // DHT 21 (AM2301)

// Initialize DHT sensor for normal 16mhz Arduino
DHT dht(DHTPIN, DHTTYPE);

int what;
int i;
float h=3;
float t=-1;

void setup() {
  pinMode(DHTPIN, INPUT);
  digitalWrite(DHTPIN, HIGH);
  Serial.begin(9600);
  delay(250);
  Serial.println("Start!");
  dht.begin();
}

void loop() {
  delay(250);
  
  if(Serial.available() > 0){
    what = Serial.read();
    if(what=='h'){
        Serial.print(h);
    }
    if(what=='t'){
        Serial.print(t);
    }
    if(what=='H'){
        Serial.print("Humidity: ");
        Serial.print(h);
        Serial.print(" %\n");
    }
    if(what=='T'){
        Serial.print("Temperature: ");
        Serial.print(t);
        Serial.print(" C\n");
    }
    if(what!='h' && what!='t' && what!='H' && what!='T'){
        Serial.print("Send 'h' for humidity in percent\nOr send 't' for temperature in Celsius\nCapital letters for human readable output\n");
    }
  }

  if(i>7){
    // Read humidity in percent
    h = dht.readHumidity();
    // Read temperature as Celsius
    t = dht.readTemperature();
    // Check if any reads failed and exit early (to try again).
    if (isnan(h) || isnan(t)) {
      Serial.println("Error!");
      return;
    }
    i=0;
  }
  i++;
}
