# Kendin Yap: İlk Robotun, Çizgi İzleyen Araç

> **Dizgi notu** (basılmaz): Çift sayfa. Sol: malzeme listesi fotoğrafı (üstten, beyaz
> zemin, parçalar dizili; atölyede çekilmeli) ve bağlantı şeması çizimi. Sağ: adımlar ve
> kod kutusu (mono font). Kod Arduino UNO + L298N sürücü + iki TCRT5000 kızılötesi sensör
> içindir. **Baskı öncesi atölyede bir kez kurulup denenmeli**; pin numaraları çizimle
> birebir aynı olmalı.

## Siyah çizgiyi takip eden bir robot yap

**Spot:** Lise öğrencilerine verdiğimiz Arduino eğitiminin bir adım ötesi. Bir hafta
sonunda, siyah bantla çizdiğin bir parkuru kendi başına takip eden bir robot.

### Malzemeler

- Arduino UNO (veya uyumlu kart)
- L298N motor sürücü modülü
- 2 adet redüktörlü DC motor ve tekerlek, 1 adet sarhoş teker
- 2 adet TCRT5000 kızılötesi çizgi sensörü modülü
- Robot şasisi (hazır kit, kontrplak veya 3B baskı)
- 4'lü AA pil yuvası veya 7,4 V Li-ion paket
- Jumper kablolar, açma-kapama anahtarı
- Beyaz zemin ve siyah elektrik bandı

### Nasıl çalışır?

Kızılötesi sensör, altındaki yüzeye ışık gönderir ve yansımayı ölçer. Beyaz zemin ışığı
yansıtır, siyah bant emer. İki sensör çizginin iki yanına yerleştirilir:

- İkisi de beyaz görüyorsa robot çizginin üstündedir → **düz git**.
- Sol sensör siyahı görüyorsa robot sağa kaymıştır → **sola dön**.
- Sağ sensör siyahı görüyorsa robot sola kaymıştır → **sağa dön**.

Bu, dergideki tüm otonom araçların temelindeki döngünün en sade hâli: **Algıla → Karar ver → Uygula.**

### Bağlantı

| Bileşen | Arduino pini |
|---|---|
| Sol sensör OUT | D2 |
| Sağ sensör OUT | D3 |
| L298N ENA (sol motor hız) | D5 |
| L298N IN1, IN2 (sol motor yön) | D6, D7 |
| L298N IN3, IN4 (sağ motor yön) | D8, D9 |
| L298N ENB (sağ motor hız) | D10 |

Sensörlerin ve sürücünün GND'si Arduino GND ile ortak olmalı. Motorları Arduino'nun 5 V
pininden besleme; pil paketi doğrudan L298N'nin güç girişine bağlanır.

### Kod

```cpp
// Çizgi izleyen robot — MATRO Dergi, Sayı 01
// Sensör modülleri siyah üzerinde HIGH, beyaz üzerinde LOW verir.
// Senin modülün tersini veriyorsa SIYAH değerini LOW yap.
const int SOL_SENSOR = 2, SAG_SENSOR = 3;
const int ENA = 5, IN1 = 6, IN2 = 7, IN3 = 8, IN4 = 9, ENB = 10;
const int SIYAH = HIGH;
const int HIZ = 140;      // 0–255 arası; robot çizgiyi kaçırıyorsa düşür
const int DONUS = 110;

void motorlar(int sol, int sag) {
  // Pozitif değer ileri, negatif değer geri
  digitalWrite(IN1, sol >= 0); digitalWrite(IN2, sol < 0);
  digitalWrite(IN3, sag >= 0); digitalWrite(IN4, sag < 0);
  analogWrite(ENA, abs(sol));
  analogWrite(ENB, abs(sag));
}

void setup() {
  pinMode(SOL_SENSOR, INPUT);
  pinMode(SAG_SENSOR, INPUT);
  for (int p = 5; p <= 10; p++) pinMode(p, OUTPUT);
}

void loop() {
  bool sol = digitalRead(SOL_SENSOR) == SIYAH;
  bool sag = digitalRead(SAG_SENSOR) == SIYAH;

  if (!sol && !sag)      motorlar(HIZ, HIZ);        // düz
  else if (sol && !sag)  motorlar(-DONUS, DONUS);   // sola dön
  else if (!sol && sag)  motorlar(DONUS, -DONUS);   // sağa dön
  else                   motorlar(0, 0);            // iki sensör de siyah: dur
}
```

### Adımlar

1. Motorları ve sarhoş tekeri şasiye tak; sensörleri ön tarafa, yere 5–10 mm yükseklikte
   ve çizgi genişliğinden biraz daha açık aralıkla yerleştir.
2. Tabloya göre kabloları bağla. Pili en son tak.
3. Kodu Arduino IDE ile yükle.
4. Sensör modülündeki küçük potansiyometreyi, beyaz zeminde modülün LED'i yanacak, siyah
   bant üzerinde sönecek şekilde ayarla (yaygın TCRT5000 modüllerinde LED yansıma
   algılanınca yanar).
5. Robotu çizginin üstüne koy ve çalıştır. Motorlardan biri ters dönüyorsa o motorun iki
   kablosunun yerini değiştir.

> **Kutu — Bir üst seviye:** İki sensör yerine beş sensör kullanıp çizginin robota göre
> ne kadar kaydığını ölç ve dönüş hızını bu kaymayla orantılı ayarla. Bu, gerçek
> araçlarda kullanılan PID kontrolünün ilk adımı.

> **Kutu — Güvenlik:** Li-ion pilleri kısa devre yapma, şarj ederken başından ayrılma.
> Motor sürücüsü çalışırken ısınabilir; soğutucusuna dokunma.
