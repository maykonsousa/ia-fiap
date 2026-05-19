#include <DHT.h>

// ===== CONFIGURAÇÃO DO DHT =====
#define DHTPIN 15
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

// ===== PINOS =====
#define LDR_PIN 34
#define BOTAO_N 12
#define BOTAO_P 13
#define BOTAO_K 14
#define RELE 27

void setup() {
  Serial.begin(115200);
  dht.begin();

  pinMode(BOTAO_N, INPUT_PULLUP);
  pinMode(BOTAO_P, INPUT_PULLUP);
  pinMode(BOTAO_K, INPUT_PULLUP);
  pinMode(RELE, OUTPUT);

  Serial.println("=======================================");
  Serial.println(" SISTEMA DE IRRIGACAO INTELIGENTE 🌱 ");
  Serial.println(" Inicializando sensores...");
  Serial.println("=======================================");
}

void loop() {

  // ===== LEITURA DOS SENSORES =====
  float umidade = dht.readHumidity();
  int ldr = analogRead(LDR_PIN);

  bool N = digitalRead(BOTAO_N) == LOW;
  bool P = digitalRead(BOTAO_P) == LOW;
  bool K = digitalRead(BOTAO_K) == LOW;

  // ===== EXIBIÇÃO DOS DADOS =====
  Serial.println("\n---------------------------------------");
  Serial.println(" LEITURA ATUAL DO SISTEMA ");
  Serial.println("---------------------------------------");

  Serial.print("Umidade do solo: ");
  Serial.print(umidade);
  Serial.println(" %");

  Serial.print("Nivel de pH (simulado - LDR): ");
  Serial.println(ldr);

  Serial.println("\nEstado dos nutrientes (NPK):");

  Serial.print("Nitrogenio (N): ");
  Serial.println(N ? "OK" : "BAIXO");

  Serial.print("Fosforo (P): ");
  Serial.println(P ? "OK" : "BAIXO");

  Serial.print("Potassio (K): ");
  Serial.println(K ? "OK" : "BAIXO");

  // ===== LÓGICA DE IRRIGAÇÃO =====
  Serial.println("\nAnalise do sistema...");

  if (umidade < 60 || !N || !P || !K) {

    digitalWrite(RELE, HIGH);

    Serial.println(">>> IRRIGACAO ATIVADA <<<");
    Serial.println("Motivo: Umidade baixa ou nutrientes insuficientes");

  } else {

    digitalWrite(RELE, LOW);

    Serial.println(">>> IRRIGACAO DESLIGADA <<<");
    Serial.println("Condicoes ideais detectadas");

  }

  Serial.println("---------------------------------------");

  delay(3000);
}
