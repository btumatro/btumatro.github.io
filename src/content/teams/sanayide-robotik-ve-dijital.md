---
title: Sanayide Robotik Uygulamalar ve Dijital Teknolojiler
subtitle: "PUSULA · ANDROMEDA"
category: Endüstri ve Enerji
status: Aktif
order: 7
image: "/media/takim-sanayide-dijital.jpg"
gallery:
  - "/media/galeri-pusula-ekip-2025.jpg"
  - "/media/galeri-pusula-atolye.jpg"
  - "/media/galeri-sanayide-dijital-arena.jpg"
  - "/media/galeri-teknofest-2022-odul.jpg"
  - "/media/haber-teknofest-2026-diyarbakir.jpg"
  - "/media/webmedya-sanayide-dijital-23.jpg"
  - "/media/webmedya-sanayide-dijital-24.jpg"
  - "/media/webmedya-sanayide-dijital-25.jpg"
  - "/media/webmedya-sanayide-dijital-26.jpg"
  - "/media/galeri-sirius-atolye.jpg"
  - "/media/galeri-sirius-arena.jpg"
  - "/media/galeri-pusula-2026-ekip.jpg"
  - "/media/galeri-pusula-sirius-ekip.jpg"
  - "/media/galeri-pusula-teknofest-calisma.jpg"
  - "/media/galeri-sirius-govde.jpg"
badge: "2026 Finalisti"
instagram: "pusula_takim"
aliases:
  - "PUSULA"
  - "ANDROMEDA"
altTakimlar:
  - ad: "PUSULA"
    aktif: true
    yillar: "2025–2026"
    aciklama: "Sanayide Robotik Uygulamalar ve Sanayide Dijital Teknolojiler yarışmalarında yarışan ekibimiz."
    basarilar:
      - "TEKNOFEST 2026 KOSGEB Sanayide Robotik Uygulamalar — Türkiye Finalisti"
      - "TEKNOFEST 2025 Sanayide Dijital Teknolojiler — Türkiye 8.si"
  - ad: "SIRIUS"
    tur: "Araç"
    yillar: "2026"
    ust: "PUSULA"
    aciklama: "Paleti depodan üretim hattına kendi başına taşıyan otonom forklift."
  - ad: "ANDROMEDA"
    aktif: true
    yillar: "2026"
    aciklama: "Mesleki Yetenek Yarışması Akıllı Fabrika Sistemleri Programlama kategorisinde yarışan ekip."
    basarilar:
      - "TEKNOFEST 2026 Akıllı Fabrika Sistemleri Programlama — Türkiye Finalisti"
focus:
  - Otonom mobil robotlar ve fabrika içi lojistik
  - ROS 2, SLAM ve navigasyon
  - Endüstri 4.0 ve dijital teknolojiler
achievements:
  - "TEKNOFEST 2026 KOSGEB Sanayide Robotik Uygulamalar — Türkiye Finalisti (PUSULA)"
  - "TEKNOFEST 2026 Mesleki Yetenek Yarışması Akıllı Fabrika Sistemleri Programlama — Türkiye Finalisti (ANDROMEDA)"
  - "TEKNOFEST 2025 Sanayide Dijital Teknolojiler — Türkiye 8.si (PUSULA)"
  - "TEKNOFEST 2024 Sanayide Dijital Teknolojiler — Türkiye Finalisti"
  - "TEKNOFEST 2021 Sanayide Dijital Teknolojiler — Türkiye 3.sü"
summary: "Palet taşıyan otonom forklift SIRIUS ile TEKNOFEST 2026 Sanayide Robotik Uygulamalar finalisti olan; 2021'de Türkiye 3.sü, 2025'te Türkiye 8.si olan endüstriyel robotik takımımız."
---

PUSULA, üretim hatlarında robotik ve dijital teknolojiler üzerine çalışan takımımızdır. TEKNOFEST Sanayide Dijital Teknolojiler kategorisinde 2021'de **Türkiye 3.sü**, 2025'te **Türkiye 8.si** olmuş, 2024'te finalde yer almıştır. 2026 sezonunda **ANDROMEDA** ekibimiz de Mesleki Yetenek Yarışması Akıllı Fabrika Sistemleri Programlama kategorisinde Türkiye finalisti oldu.

## SIRIUS: otonom forklift

2026 sezonunun aracı **SIRIUS**, paleti depodan üretim hattına kendi başına taşıyan otonom bir forklifttir. Sanayi ve Teknoloji Bakanlığı ile KOSGEB yürütücülüğündeki **TEKNOFEST Sanayide Robotik Uygulamalar Yarışması**'nda Türkiye finalisti olarak Diyarbakır'da yarıştı.

Yarışmada robot dışarıdan müdahale olmadan üç işi yapar:

1. **Haritalama:** Alanı sensörleriyle algılayıp dijital harita çıkarır.
2. **Görev:** Otomasyon sisteminden gelen görevle alma noktasına gider.
3. **Taşıma:** Yükü alır, bırakma noktasına götürüp indirir.

Parkurda uzaktan kumanda yoktur, enerji araç üstündeki bataryadan sağlanır.

## Ekip

9 öğrenci, 3 alt ekip ve 1 araç:

- **Mekanik:** Şasi, gövde, kaldırma kulesi ve çatal
- **Elektronik ve güç:** Batarya paketi, güç dağıtımı, emniyet devresi
- **Yazılım:** ROS 2, navigasyon, görev ağacı, web panel

## Mimari

- **Arayüz:** Tarayıcıdan açılan yerel web paneli
- **Otonomi:** ROS 2 Humble, SLAM Toolbox, Nav2, EKF, py_trees
- **Denetim:** Python üst seviye karar, C++ alt seviye denetleyiciler (Arduino Mega, ESP32)
- **Sensörler:** LiDAR, kamera, IMU, enkoder, mesafe, limit anahtarı, akım, sıcaklık ve gaz sensörleri

Görev akışının her adımı py_trees'te ayrı bir davranış düğümüdür. Bir adım başarısız olursa akış orada durur ve panelde hangi adımda kalındığı görünür. Palete yanaşmada kamera, enkoder ve LiDAR bağımsız çalışır; tek bir sensörün arızası görevi durdurmaz. 70 cm içinde engel görülürse araç durur, engel kalkınca kaldığı yerden devam eder.
