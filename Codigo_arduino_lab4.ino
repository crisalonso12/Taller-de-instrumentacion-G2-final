const int canal_0_pin = A0;
const int canal_1_pin = A1;
const int control_pin = 2;  

const int s0Pin = 9;
const int s1Pin = 3;
const int s2Pin = 4;

const int s0Pin2 = 6;
const int s1Pin2 = 7;
const int s2Pin2 = 8;


volatile int valor_canal_0;
volatile int valor_canal_1;

void setup() {
  
  pinMode(canal_0_pin, INPUT);
  pinMode(canal_1_pin, INPUT);
  pinMode(control_pin, OUTPUT);

  pinMode(s0Pin, OUTPUT);
  pinMode(s1Pin, OUTPUT);
  pinMode(s2Pin, OUTPUT);

  pinMode(s0Pin2, OUTPUT);
  pinMode(s1Pin2, OUTPUT);
  pinMode(s2Pin2, OUTPUT);
  Serial.begin(9600);

  // Configuración del temporizador para generar interrupciones a una tasa de 5000 Hz
  TCCR1A = 0; // Configuración normal del temporizador
  TCCR1B = (1 << WGM12) | (1 << CS11); // Modo CTC, sin preescaler
  OCR1A = 3199; // Valor de comparación para obtener una interrupción cada 3200 ciclos (16 MHz / 3200 = 5000 Hz)
  TIMSK1 = (1 << OCIE1A); // Habilitar interrupción de comparación A
}

ISR(TIMER1_COMPA_vect) {
 
  digitalWrite(control_pin, HIGH);

  
  valor_canal_0 = analogRead(canal_0_pin);
  float voltaje_canal_0 = (valor_canal_0 / 1023.0) * 5.0;
  valor_canal_1 = analogRead(canal_1_pin);
  float voltaje_canal_1 = (valor_canal_1 / 1023.0) * 5.0;

   Serial.print(voltaje_canal_0);
   Serial.print(",");
   Serial.println(voltaje_canal_1);

  
  digitalWrite(control_pin, LOW);
}

void loop() {
   char input;
  
  if (Serial.available() > 0) {
    input = Serial.read(); // Leer el valor ingresado como un número entero

    switch (input){
      case '1':
      digitalWrite(s0Pin, HIGH);
      digitalWrite(s1Pin, LOW);
      digitalWrite(s2Pin, LOW);
      Serial.println("ATE1");
      break;
      
      case '2':
      digitalWrite(s0Pin, LOW);
      digitalWrite(s1Pin, HIGH);
      digitalWrite(s2Pin, LOW);
      Serial.println("ATE2");
      break;
      
      case '3':
      digitalWrite(s0Pin, HIGH);
      digitalWrite(s1Pin, HIGH);
      digitalWrite(s2Pin, LOW);
      Serial.println("ATE3");
      break;
      
      case '4':
      digitalWrite(s0Pin, LOW);
      digitalWrite(s1Pin, LOW);
      digitalWrite(s2Pin, HIGH);
      Serial.println("SEG");
      break;
      
      case '5':
      digitalWrite(s0Pin, HIGH);
      digitalWrite(s1Pin, LOW);
      digitalWrite(s2Pin, HIGH);
      Serial.println("GAN1");
      break;
      
      case '6':
      digitalWrite(s0Pin, LOW);
      digitalWrite(s1Pin, HIGH);
      digitalWrite(s2Pin, HIGH);
      Serial.println("GAN2");
      break;
      
      case '7':
      digitalWrite(s0Pin, HIGH);
      digitalWrite(s1Pin, HIGH);
      digitalWrite(s2Pin, HIGH);
      Serial.println("GAN3");
      break;

      case 'a':
      digitalWrite(s0Pin2, HIGH);
      digitalWrite(s1Pin2, LOW);
      digitalWrite(s2Pin2, LOW);
      Serial.println("2ATE1");
      break;
      
      case 'b':
      digitalWrite(s0Pin2, LOW);
      digitalWrite(s1Pin2, HIGH);
      digitalWrite(s2Pin2, LOW);
      Serial.println("2ATE2");
      break;
      
      case 'c':
      digitalWrite(s0Pin2, HIGH);
      digitalWrite(s1Pin2, HIGH);
      digitalWrite(s2Pin2, LOW);
      Serial.println("2ATE3");
      break;
      
      case 'd':
      digitalWrite(s0Pin2, LOW);
      digitalWrite(s1Pin2, LOW);
      digitalWrite(s2Pin2, HIGH);
      Serial.println("2SEG");
      break;
            
      case 'e':
      digitalWrite(s0Pin2, HIGH);
      digitalWrite(s1Pin2, LOW);
      digitalWrite(s2Pin2, HIGH);
      Serial.println("2GAN1");
      break;
      
      case 'f':
      digitalWrite(s0Pin2, LOW);
      digitalWrite(s1Pin2, HIGH);
      digitalWrite(s2Pin2, HIGH);
      Serial.println("2GAN2");
      break;
           
      case 'g':
      digitalWrite(s0Pin2, HIGH);
      digitalWrite(s1Pin2, HIGH);
      digitalWrite(s2Pin2, HIGH);
      Serial.println("2GAN3");
      break;
    }
  }
}
