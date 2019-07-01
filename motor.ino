const byte Encoder = 2;
int splitString(char* frase);

const byte pwmEsquerda = 6;
const byte tensaoEsquerda1 = 5;
const byte tensaoEsquerda2 = 4;
const byte pwmDireita = 7;
const byte tensaoDireita1 = 2;
const byte tensaoDireita2 = 3;
int segundoMotor = 0;
int primeiroMotor = 0;

void setup() {


pinMode(tensaoEsquerda1, OUTPUT);
digitalWrite(tensaoEsquerda1, LOW);
pinMode(tensaoEsquerda2, OUTPUT);
digitalWrite(tensaoEsquerda2, LOW);
pinMode(tensaoDireita1, OUTPUT);
digitalWrite(tensaoDireita1, LOW);
pinMode(tensaoDireita2, OUTPUT);
digitalWrite(tensaoDireita2, LOW);
pinMode(pwmEsquerda, OUTPUT);
pinMode(pwmDireita, OUTPUT);
Serial.begin(115200);
while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
}
Serial.println("Iniciando arduino");

}

void loop() {

if(Serial.available()> 0){
    String teste = Serial.readString();
    Serial.print("Teste: ");
    Serial.println(teste);
    if(teste == "Zerar\n"){
        digitalWrite(tensaoEsquerda1, HIGH);
        digitalWrite(tensaoEsquerda2, HIGH);
        digitalWrite(tensaoDireita1, HIGH);
        digitalWrite(tensaoDireita2, HIGH);
    Serial.println("Zerando motor");
    }
    else{

      char frase[30];
      teste.toCharArray(frase, sizeof(frase)); 
        primeiroMotor = splitString1(frase);
        
        teste.toCharArray(frase, sizeof(frase)); 
        segundoMotor = splitString(frase);

        motor(primeiroMotor, tensaoEsquerda1, tensaoEsquerda2, pwmEsquerda);
        motor(segundoMotor, tensaoDireita1, tensaoDireita2, pwmDireita);


    }
  
}
}

void motor(int valor, int portaA, int portaB, int pwmVariavel){
        if(valor > 0){
        analogWrite(pwmVariavel, valor);
        digitalWrite(portaA, HIGH);
        digitalWrite(portaB, LOW);
      }else{
         analogWrite(pwmVariavel,-1* valor);
        digitalWrite(portaA, LOW);
        digitalWrite(portaB, HIGH);
      }
 
}
int splitString(char* frase){
  char * saida = strtok(frase, " ");
  char * auxiliar = strtok(NULL, " ");
  String converte = auxiliar;
  return converte.toInt();
}
int splitString1(char* frase){
  char * saida = strtok(frase, " ");
  String converte = saida;
  return converte.toInt();
}