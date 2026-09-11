#!/usr/bin/env python3
"""
MATRO Kitapçığı — Sayfa 06, 07, 08, 09, 10 ve 14 için Hassas Düzeltmeler
- Kafa, gövde, ödül çeki veya araç kesintileri sıfırlandı.
- Mükerrer (aynı fotoğrafın birden fazla kullanımı) tamamen elendi.
- Alakasız toplantı veya sosyal medya çıkartmaları temizlendi.
- Her sayfaya fotoğraflarının en-boy oranına göre özel mizanpaj uygulandı.
"""

import os
import subprocess

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PAGES_DIR = os.path.join(PROJECT_ROOT, 'docs', 'kitapcik-hazirlik', 'sayfalar')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'docs', 'kitapcik-hazirlik', 'ornek-tasarimlar')
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def asset_url(rel):
    return f"file://{os.path.join(PROJECT_ROOT, rel.lstrip('/'))}"

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Barlow:ital,wght@0,700;0,800;0,900;1,800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600;700&display=swap');

@page { size: 210mm 297mm; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --c-bg: #FFFFFF; --c-ink: #0B1012; --c-text-muted: #475569; --c-text-subtle: #64748B;
  --c-border: #CBD5E1; --c-volt: #0D9488; --c-volt-light: #F0FDFA; --c-medal: #D97706;
  --c-medal-light: #FEF3C7; --c-surface: #F8FAFC;
  --font-display: 'Barlow', sans-serif; --font-sans: 'Inter', sans-serif; --font-mono: 'JetBrains Mono', monospace;
}

body.page-sheet {
  width: 1240px; height: 1754px; background: var(--c-bg); color: var(--c-ink); font-family: var(--font-sans);
  display: flex; flex-direction: column; justify-content: space-between; padding: 44px 56px 36px 56px;
  position: relative; overflow: hidden; -webkit-font-smoothing: antialiased;
}

.page-header {
  display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid var(--c-ink);
  padding-bottom: 12px; margin-bottom: 16px; flex-shrink: 0;
}
.brand-left { display: flex; align-items: center; gap: 14px; }
.header-logo { height: 36px; width: auto; object-fit: contain; }
.dept-name { font-size: 11px; font-weight: 500; color: var(--c-text-muted); }
.header-meta-right { display: flex; align-items: center; gap: 14px; }
.section-tag { font-family: var(--font-mono); font-size: 11px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: var(--c-volt); }
.page-index-badge { font-family: var(--font-mono); font-size: 11px; font-weight: 700; border: 1.5px solid var(--c-ink); padding: 2px 7px; border-radius: 2px; }

.page-footer {
  display: flex; justify-content: space-between; align-items: center; border-top: 1.5px solid var(--c-ink);
  padding-top: 10px; font-family: var(--font-mono); font-size: 11px; color: var(--c-text-subtle); flex-shrink: 0;
}
.footer-site { color: var(--c-ink); font-weight: 700; }
.page-number { font-weight: 800; color: var(--c-ink); }

.media-unit { display: flex; flex-direction: column; height: 100%; min-height: 0; overflow: hidden; }
.img-box { width: 100%; flex: 1; min-height: 0; position: relative; overflow: hidden; background-color: #F8FAFC; border-radius: 4px; border: 1px solid var(--c-border); }
.img-box img { width: 100%; height: 100%; object-fit: cover; display: block; }
.caption-bar { display: flex; align-items: center; gap: 8px; padding-top: 6px; font-family: var(--font-sans); line-height: 1.25; flex-shrink: 0; }
.caption-tag {
  font-family: var(--font-mono); font-size: 9px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase;
  color: #FFFFFF; background-color: var(--c-ink); padding: 2px 6px; border-radius: 2px; white-space: nowrap;
}
.caption-text { font-size: 11px; font-weight: 500; color: #475569; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.bullet-list { list-style: none; display: flex; flex-direction: column; gap: 8px; margin-top: 8px; }
.bullet-list li { display: flex; align-items: flex-start; gap: 8px; font-size: 13.5px; font-weight: 600; color: var(--c-ink); }
.bullet-list li::before { content: '■'; color: var(--c-volt); font-size: 9px; margin-top: 3px; }

.tech-box { background: var(--c-surface); border: 1.5px solid var(--c-border); border-radius: 4px; padding: 16px; display: flex; flex-direction: column; justify-content: space-between; }
.award-pill {
  background: var(--c-medal-light); border: 1px solid #FCD34D; color: #92400E; padding: 7px 12px;
  border-radius: 3px; font-size: 11.5px; font-weight: 700; display: inline-flex; align-items: center; gap: 8px;
}
.trophy-dot { width: 6px; height: 6px; background: var(--c-medal); border-radius: 50%; }
"""

# ==============================================================================
# SAYFA 06 — ASHİNA İHA (Hero tam kadraj, alttaki uçuş sahasında uçaklar net)
# ==============================================================================
def html_p06():
    return f"""<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8"><style>{CSS}
.ashina-hero {{{{ width: 100%; height: 530px; margin-bottom: 20px; flex-shrink: 0; }}}}
.ashina-mid {{{{ display: grid; grid-template-columns: 1.25fr 1fr; gap: 24px; margin-bottom: 20px; flex-shrink: 0; }}}}
.ashina-lower {{{{ display: grid; grid-template-columns: 0.9fr 1.1fr; grid-template-rows: 350px; height: 350px; gap: 20px; margin-bottom: 4px; flex-shrink: 0; }}}}
</style></head>
<body class="page-sheet">
  <header class="page-header">
    <div class="brand-left">
      <img class="header-logo" src="{asset_url('public/logo-matro-siyah.png')}" alt="MATRO Logo">
      <div class="dept-name">Bursa Teknik Üniversitesi // MATRO Havacılık Kümesi</div>
    </div>
    <div class="header-meta-right">
      <div class="section-tag">Sabit & Döner Kanat</div>
      <div class="page-index-badge">06</div>
    </div>
  </header>

  <!-- Üst Hero: TÜBİTAK İHA Yarışma Alanı (Kafalar ve uçaklar tam odakta, yazı kesintisi yok) -->
  <div class="media-unit ashina-hero">
    <div class="img-box">
      <img style="object-position: center 42%;" src="{asset_url('public/media/galeri-ashina-teknofest-grup.jpg')}" alt="ASHİNA Takımı">
    </div>
    <div class="caption-bar">
      <span class="caption-tag">YARIŞMA SAHNESİ</span>
      <span class="caption-text">TÜBİTAK Uluslararası İHA Yarışması pistinde ASHİNA ekibimiz ve iki yarışma uçağımız</span>
    </div>
  </div>

  <div class="ashina-mid">
    <div>
      <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 4px;">
        <img style="height: 38px; width: auto;" src="{asset_url('public/media/logolar/takimlar/ashina.png')}" alt="ASHİNA Logo">
        <div>
          <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--c-volt);">İNSANSIZ HAVA ARAÇLARI TAKIMI</div>
          <h1 style="font-family: var(--font-display); font-size: 46px; font-weight: 900; line-height: 0.95; text-transform: uppercase;">ASHİNA</h1>
        </div>
      </div>
      <p style="font-size: 14px; line-height: 1.52; color: #475569; margin-top: 8px;">
        <strong>ASHİNA</strong>, aerodinamik gövdesinden otonom uçuş kontrol yazılımına kadar tamamen öğrencilerimiz tarafından geliştirilen sabit kanat İHA sistemimizdir. Yapay zekâlı görüntü işleme ile yer hedeflerini otonom tespit eder.
      </p>
      <ul class="bullet-list">
        <li>Tam otonom hedef arama, tanıma ve lazer güdümlü işaretleme</li>
        <li>Hafifletilmiş karbon-balsa sandviç kanat yapısıyla 45 dk seyir süresi</li>
      </ul>
    </div>

    <div class="tech-box">
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; border-bottom: 1.5px solid var(--c-ink); padding-bottom: 4px;">İHA PARAMETRELERİ</div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 10px 0;">
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">KANAT AÇIKLIĞI</span><div style="font-size: 13px; font-weight: 700;">1900 mm Sandviç</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">AĞIRLIK</span><div style="font-size: 13px; font-weight: 700;">4.2 kg (Kalkış)</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">AVİYONİK</span><div style="font-size: 13px; font-weight: 700;">Pixhawk 6C + Jetson</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">MENZİL</span><div style="font-size: 13px; font-weight: 700;">25 km Telemetri</div></div>
      </div>
      <div class="award-pill">
        <span class="trophy-dot"></span>
        <span>TEKNOFEST 2026 TÜBİTAK İHA FİNALİSTİ</span>
      </div>
    </div>
  </div>

  <!-- Alt İkili: CAD Kanat Modellemesi + Pist Uçuş Sahası (Yerdeki uçak ve ekip eksiksiz!) -->
  <div class="ashina-lower">
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center center;" src="{asset_url('public/media/tasarim-ashina-iha.jpg')}" alt="CAD">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">CAD MODELLEME</span>
        <span class="caption-text">Kafes kanat aerodinamik taşıyıcı yüzey optimizasyonu</span>
      </div>
    </div>
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center 25%;" src="{asset_url('public/media/galeri-ashina-saha.jpg')}" alt="Pist Testi">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">PİST UÇUŞ TESTİ</span>
        <span class="caption-text">Uçuş pistinde kalkış öncesi aerodinamik yüzey ve telemetri kontrolleri</span>
      </div>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // ASHİNA İHA</div>
    <div class="page-number">SAYFA 06</div>
  </footer>
</body>
</html>"""

# ==============================================================================
# SAYFA 07 — MATROVER & LUNA (Geniş 16:9 Hero + Rektörlü Tarımsal İKA + Batarya)
# ==============================================================================
def html_p07():
    return f"""<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8"><style>{CSS}
.rover-hero {{ width: 100%; height: 500px; margin-bottom: 20px; flex-shrink: 0; }}
.rover-mid {{ display: grid; grid-template-columns: 1.25fr 1fr; gap: 24px; margin-bottom: 20px; flex-shrink: 0; }}
.rover-lower {{ display: grid; grid-template-columns: 1.35fr 0.65fr; grid-template-rows: 380px; height: 380px; gap: 20px; margin-bottom: 4px; flex-shrink: 0; }}
</style></head>
<body class="page-sheet">
  <header class="page-header">
    <div class="brand-left">
      <img class="header-logo" src="{asset_url('public/logo-matro-siyah.png')}" alt="MATRO Logo">
      <div class="dept-name">Bursa Teknik Üniversitesi // MATRO Kara Sistemleri</div>
    </div>
    <div class="header-meta-right">
      <div class="section-tag">Gezegen Keşif & Otonom Tarım</div>
      <div class="page-index-badge">07</div>
    </div>
  </header>

  <!-- Üst Hero: 16:9 Geniş Kadraj (Tüm öğrenciler ve 2 rover tam kadrajda, sıfır kesinti) -->
  <div class="media-unit rover-hero">
    <div class="img-box">
      <img style="object-position: center 30%;" src="{asset_url('public/media/takim-matrover.jpg')}" alt="MATROVER Ekibi">
    </div>
    <div class="caption-bar">
      <span class="caption-tag">ROVER SAHASI</span>
      <span class="caption-text">TEKNOFEST çadırında iki adet tam fonksiyonel otonom keşif robotumuz ve MATROVER ekibimiz</span>
    </div>
  </div>

  <div class="rover-mid">
    <div>
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--c-volt); margin-bottom: 4px;">İNSANSIZ KARA ARAÇLARI VE ROVER</div>
      <h1 style="font-family: var(--font-display); font-size: 46px; font-weight: 900; line-height: 0.95; text-transform: uppercase;">MATROVER & LUNA</h1>
      <p style="font-size: 14px; line-height: 1.52; color: #475569; margin-top: 8px;">
        <strong>MATROVER</strong> ve <strong>LUNA</strong>, engebeli arazi şartlarında otonom engelden kaçma, haritalama ve 5 eksenli robotik kolla numune toplama görevlerini yürüten kara robotlarımızdır. Rocker-bogie süspansiyon geometrisi dik hendek ve kayaları aşar.
      </p>
      <ul class="bullet-list">
        <li>Bağımsız yönlendirilebilir 6x6 fırçasız cer motoru tahriki</li>
        <li>LiDAR tabanlı 3D SLAM haritalama ve otonom yol planlama</li>
      </ul>
    </div>

    <div class="tech-box">
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; border-bottom: 1.5px solid var(--c-ink); padding-bottom: 4px;">ROVER PARAMETRELERİ</div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 10px 0;">
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">SÜSPANSİYON</span><div style="font-size: 13px; font-weight: 700;">Rocker-Bogie 6x6</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">TIRMANMA</span><div style="font-size: 13px; font-weight: 700;">40° Eğim // 35 cm</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">HESAPLAMA</span><div style="font-size: 13px; font-weight: 700;">NVIDIA Jetson Orin</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">GÜÇ SİSTEMİ</span><div style="font-size: 13px; font-weight: 700;">48V 20Ah LiFePO4</div></div>
      </div>
      <div class="award-pill">
        <span class="trophy-dot"></span>
        <span>TEKNOFEST 2026 İKA & ROVER FİNALİSTİ</span>
      </div>
    </div>
  </div>

  <!-- Alt İkili: Tarımsal İKA (Rektör ve Takım Tam Kadrajda!) + BMS Batarya Devresi -->
  <div class="rover-lower">
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center 30%;" src="{asset_url('public/media/galeri-tika-tarimsal-ika.jpg')}" alt="Tarımsal İKA">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">TARIMSAL İKA</span>
        <span class="caption-text">TEKNOFEST Tarımsal İKA alanında prototip robotumuz, üniversite rektörümüz ve ekibimiz</span>
      </div>
    </div>
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center center;" src="{asset_url('public/media/galeri-luna-batarya.jpg')}" alt="BMS Batarya">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">DONANIM</span>
        <span class="caption-text">Özel tasarım BMS batarya yönetim sistemi</span>
      </div>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // MATROVER & LUNA</div>
    <div class="page-number">SAYFA 07</div>
  </footer>
</body>
</html>"""

# ==============================================================================
# SAYFA 08 — LODOS & İDA (İskele Sahası + Gövde İmalat + Sahilde Finalist Ekip)
# ==============================================================================
def html_p08():
    return f"""<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8"><style>{CSS}
.lodos-hero {{ width: 100%; height: 530px; margin-bottom: 20px; flex-shrink: 0; }}
.lodos-mid {{ display: grid; grid-template-columns: 1.25fr 1fr; gap: 24px; margin-bottom: 20px; flex-shrink: 0; }}
.lodos-lower {{ display: grid; grid-template-columns: 0.95fr 1.05fr; grid-template-rows: 360px; height: 360px; gap: 20px; margin-bottom: 4px; flex-shrink: 0; }}
</style></head>
<body class="page-sheet">
  <header class="page-header">
    <div class="brand-left">
      <img class="header-logo" src="{asset_url('public/logo-matro-siyah.png')}" alt="MATRO Logo">
      <div class="dept-name">Bursa Teknik Üniversitesi // MATRO Deniz Sistemleri</div>
    </div>
    <div class="header-meta-right">
      <div class="section-tag">Mavi Vatan İDA</div>
      <div class="page-index-badge">08</div>
    </div>
  </header>

  <!-- Üst Hero: Yarışma İskelesinde LODOS ve Takım (Telefon paraziti temizlendi) -->
  <div class="media-unit lodos-hero">
    <div class="img-box">
      <img style="object-position: center 20%;" src="{asset_url('public/media/galeri-lodos-saha.jpg')}" alt="LODOS Sahil Ekibi">
    </div>
    <div class="caption-bar">
      <span class="caption-tag">YARIŞMA İSKELESİ</span>
      <span class="caption-text">TEKNOFEST Mavi Vatan yarışma iskelesinde LODOS otonom deniz aracımız başında finalist ekibimiz</span>
    </div>
  </div>

  <div class="lodos-mid">
    <div>
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--c-volt); margin-bottom: 4px;">İNSANSIZ DENİZ ARACI TAKIMI</div>
      <h1 style="font-family: var(--font-display); font-size: 46px; font-weight: 900; line-height: 0.95; text-transform: uppercase;">LODOS & İDA</h1>
      <p style="font-size: 14px; line-height: 1.52; color: #475569; margin-top: 8px;">
        <strong>LODOS</strong>, deniz ve göl yüzeyinde otonom devriye, şamandıra tanıma ve liman yanaşma görevlerini icra eden insansız su üstü aracımızdır. Dalgalı deniz koşullarına dayanıklı trimaran gövdesi ve su jeti itki sistemiyle yüksek manevra kabiliyetine sahiptir.
      </p>
      <ul class="bullet-list">
        <li>Çift fırçasız itki sistemiyle yüksek manevra ve diferansiyel sürüş</li>
        <li>Yapay görme ile şamandıra algılama ve COLREGS çatışma önleme</li>
      </ul>
    </div>

    <div class="tech-box">
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; border-bottom: 1.5px solid var(--c-ink); padding-bottom: 4px;">TEKNİK ÖZELLİKLER</div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 10px 0;">
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">GÖVDE</span><div style="font-size: 13px; font-weight: 700;">Kompozit Trimaran</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">SÜRAT</span><div style="font-size: 13px; font-weight: 700;">16 Knot (Azami)</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">İTKİ</span><div style="font-size: 13px; font-weight: 700;">Çift BLDC Su Jeti</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">MENZİL</span><div style="font-size: 13px; font-weight: 700;">15 km RF Köprüsü</div></div>
      </div>
      <div class="award-pill">
        <span class="trophy-dot"></span>
        <span>TEKNOFEST 2026 MAVİ VATAN FİNALİSTİ</span>
      </div>
    </div>
  </div>

  <!-- Alt İkili: LODOS Trimaran Gövde İmalatı + Deniz Kenarında Finalist Ekip (Haluk Bayraktar'ın kesik yüzü yerine ekibin tam resmi!) -->
  <div class="lodos-lower">
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center center;" src="{asset_url('public/media/galeri-lodos-deniz-test.jpg')}" alt="LODOS Gövde">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">GÖVDE İMALATI</span>
        <span class="caption-text">Atölyede LODOS kompozit trimaran gövdesi ve kavitasyon nozulları</span>
      </div>
    </div>
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center 25%;" src="{asset_url('public/media/takim-ida.jpg')}" alt="İDA Ekibi">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">FİNALİST EKİP</span>
        <span class="caption-text">İnsansız deniz aracı ekibimiz Mavi Vatan yarışma parkuru kıyısında</span>
      </div>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // LODOS & İDA</div>
    <div class="page-number">SAYFA 08</div>
  </footer>
</body>
</html>"""

# ==============================================================================
# SAYFA 09 — İSS & PRUSA (Mükerrer Havuz Görseli Sıfırlandı, Alüminyum Şasi ve Takım Eklendi)
# ==============================================================================
def html_p09():
    return f"""<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8"><style>{CSS}
.prusa-hero {{ width: 100%; height: 530px; margin-bottom: 20px; flex-shrink: 0; }}
.prusa-mid {{ display: grid; grid-template-columns: 1.25fr 1fr; gap: 24px; margin-bottom: 20px; flex-shrink: 0; }}
.prusa-lower {{ display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 360px; height: 360px; gap: 20px; margin-bottom: 4px; flex-shrink: 0; }}
</style></head>
<body class="page-sheet">
  <header class="page-header">
    <div class="brand-left">
      <img class="header-logo" src="{asset_url('public/logo-matro-siyah.png')}" alt="MATRO Logo">
      <div class="dept-name">Bursa Teknik Üniversitesi // MATRO Sualtı Sistemleri</div>
    </div>
    <div class="header-meta-right">
      <div class="section-tag">Otonom Sualtı Robotu</div>
      <div class="page-index-badge">09</div>
    </div>
  </header>

  <!-- Üst Hero: PRUSA AUV Olimpik Havuz Görevinde (Tek ve Dominant) -->
  <div class="media-unit prusa-hero">
    <div class="img-box">
      <img style="object-position: center 30%;" src="{asset_url('public/media/galeri-iss-auv-havuz.jpg')}" alt="PRUSA Havuz Testi">
    </div>
    <div class="caption-bar">
      <span class="caption-tag">HAVUZ GÖREVİ</span>
      <span class="caption-text">PRUSA AUV olimpik havuzda kapıdan geçiş ve sualtı hedef tanıma görevinde</span>
    </div>
  </div>

  <div class="prusa-mid">
    <div>
      <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 4px;">
        <img style="height: 38px; width: auto;" src="{asset_url('public/media/logolar/takimlar/btu-auv.png')}" alt="PRUSA Logo">
        <div>
          <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--c-volt);">İNSANSIZ SUALTI SİSTEMLERİ</div>
          <h1 style="font-family: var(--font-display); font-size: 46px; font-weight: 900; line-height: 0.95; text-transform: uppercase;">İSS & PRUSA</h1>
        </div>
      </div>
      <p style="font-size: 14px; line-height: 1.52; color: #475569; margin-top: 8px;">
        <strong>PRUSA</strong>, 50 metre derinliğe kadar sızdırmaz basınç kapsülü ve 8 adet manyetik kaplinli iticisi ile 6 serbestlik derecesinde otonom seyrüsefer yapan sualtı robotumuzdur.
      </p>
      <ul class="bullet-list">
        <li>Akustik konumlandırma (DVL / USBL) ve IMU sensör füzyonu</li>
        <li>Sualtı optik kamera ile renk bozulmalarını düzelten yapay zekâ</li>
      </ul>
    </div>

    <div class="tech-box">
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; border-bottom: 1.5px solid var(--c-ink); padding-bottom: 4px;">ROBOTİK PARAMETRELERİ</div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 10px 0;">
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">BASINÇ</span><div style="font-size: 13px; font-weight: 700;">5 Bar (50 Metre)</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">İTİCİLER</span><div style="font-size: 13px; font-weight: 700;">8x Manyetik Kaplin</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">YAZILIM</span><div style="font-size: 13px; font-weight: 700;">ROS 2 / Gazebo</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">AĞIRLIK</span><div style="font-size: 13px; font-weight: 700;">18.5 kg (Pozitif)</div></div>
      </div>
      <div class="award-pill">
        <span class="trophy-dot"></span>
        <span>TEKNOFEST 2026 İSS FİNALİSTİ</span>
      </div>
    </div>
  </div>

  <!-- Alt İkili: İzometrik CAD Şeması + Alüminyum Gövde / Torpido Tüpü (Mükerrer havuz karesi tamamen temizlendi!) -->
  <div class="prusa-lower">
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center center;" src="{asset_url('public/media/tasarim-iss-auv-izometrik.jpg')}" alt="CAD">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">İZOMETRİK CAD</span>
        <span class="caption-text">6 eksen serbestlikli 8 itici yerleşimi ve basınç tüpü CAD modeli</span>
      </div>
    </div>
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center center;" src="{asset_url('public/media/takim-iss-sualti-araci.jpg')}" alt="Gövde">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">MEKANİK ŞASİ</span>
        <span class="caption-text">Alüminyum 6061-T6 korozyon dirençli gövde ve torpido fırlatma mekanizması</span>
      </div>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // PRUSA AUV</div>
    <div class="page-number">SAYFA 09</div>
  </footer>
</body>
</html>"""

# ==============================================================================
# SAYFA 10 — ZEMHERİ & SARA (Mükerrer ve Alakasız Kareler Temizlendi, Roket Odakta)
# ==============================================================================
def html_p10():
    return f"""<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8"><style>{CSS}
.zemheri-hero {{ width: 100%; height: 530px; margin-bottom: 20px; flex-shrink: 0; }}
.zemheri-mid {{ display: grid; grid-template-columns: 1.25fr 1fr; gap: 24px; margin-bottom: 20px; flex-shrink: 0; }}
.zemheri-lower {{ display: grid; grid-template-columns: 1.05fr 0.95fr; grid-template-rows: 360px; height: 360px; gap: 20px; margin-bottom: 4px; flex-shrink: 0; }}
</style></head>
<body class="page-sheet">
  <header class="page-header">
    <div class="brand-left">
      <img class="header-logo" src="{asset_url('public/logo-matro-siyah.png')}" alt="MATRO Logo">
      <div class="dept-name">Bursa Teknik Üniversitesi // MATRO Savunma & Roket</div>
    </div>
    <div class="header-meta-right">
      <div class="section-tag">Sualtı Roket Teknolojisi</div>
      <div class="page-index-badge">10</div>
    </div>
  </header>

  <!-- Üst Hero: Yarışma Çadırında ZEMHERİ Ekibi ve Prototip Roket -->
  <div class="media-unit zemheri-hero">
    <div class="img-box">
      <img style="object-position: center 25%;" src="{asset_url('public/media/galeri-zemheri-takim.jpg')}" alt="ZEMHERİ Ekibi">
    </div>
    <div class="caption-bar">
      <span class="caption-tag">FİNALİST TAKIM</span>
      <span class="caption-text">ZEMHERİ sualtı roketi ekibimiz yarışma çadırında prototip roketleriyle</span>
    </div>
  </div>

  <div class="zemheri-mid">
    <div>
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--c-volt); margin-bottom: 4px;">SUALTI ROKETİ VE SAVUNMA SİSTEMLERİ</div>
      <h1 style="font-family: var(--font-display); font-size: 46px; font-weight: 900; line-height: 0.95; text-transform: uppercase;">ZEMHERİ & SARA</h1>
      <p style="font-size: 14px; line-height: 1.52; color: #475569; margin-top: 8px;">
        <strong>ZEMHERİ</strong>, deniz tabanında konuşlu bir fırlatma kapsülünden ateşlenerek su yüzeyini aşıp havada hedefine yönelen yenilikçi sualtı roketi projemizdir. Yüksek basınca dayanıklı gövdesi su yüzeyinde güvenli ateşleme sağlar.
      </p>
      <ul class="bullet-list">
        <li>Sualtından fırlatılmaya uygun çift kademeli kapsül mekanizması</li>
        <li>Basınç sensörü tetiklemeli elektronik ateşleme ve telemetri sistemi</li>
      </ul>
    </div>

    <div class="tech-box">
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; border-bottom: 1.5px solid var(--c-ink); padding-bottom: 4px;">ROKET PARAMETRELERİ</div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 10px 0;">
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">FIRTLATMA</span><div style="font-size: 13px; font-weight: 700;">15 m Su Derinliği</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">İTKİ</span><div style="font-size: 13px; font-weight: 700;">Katı Yakıt Motoru</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">AVİYONİK</span><div style="font-size: 13px; font-weight: 700;">STM32 + 6-IMU</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">KURTARMA</span><div style="font-size: 13px; font-weight: 700;">Çift Paraşüt Sistemi</div></div>
      </div>
      <div class="award-pill">
        <span class="trophy-dot"></span>
        <span>TEKNOFEST 2026 MAVİ VATAN FİNALİSTİ</span>
      </div>
    </div>
  </div>

  <!-- Alt İkili: Mavi Vatan Final Sahası + Sahil Brifingi (Alakasız toplantı karesi tamamen temizlendi!) -->
  <div class="zemheri-lower">
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center 30%;" src="{asset_url('public/media/galeri-zemheri-final.jpg')}" alt="Mavi Vatan Finali">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">MAVİ VATAN FİNALİ</span>
        <span class="caption-text">TEKNOFEST Mavi Vatan finallerinde ZEMHERİ roket sistemi saha testinde</span>
      </div>
    </div>
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center center;" src="{asset_url('public/media/takim-zemheri.jpg')}" alt="Saha Brifingi">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">SAHA BRİFİNGİ</span>
        <span class="caption-text">ZEMHERİ ekibimiz yarışma standında hakem heyetine sunum öncesinde</span>
      </div>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // ZEMHERİ ROKETİ</div>
    <div class="page-number">SAYFA 10</div>
  </footer>
</body>
</html>"""

# ==============================================================================
# SAYFA 14 — BÜRKÜT (Selçuk Bayraktar Ödül Töreni Tam Kadraj, Haluk Bayraktar Brifingi)
# ==============================================================================
def html_p14():
    return f"""<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8"><style>{CSS}
.burkut-hero {{ width: 100%; height: 530px; margin-bottom: 20px; flex-shrink: 0; }}
.burkut-mid {{ display: grid; grid-template-columns: 1.25fr 1fr; gap: 24px; margin-bottom: 20px; flex-shrink: 0; }}
.burkut-lower {{ display: grid; grid-template-columns: 1.2fr 0.8fr; grid-template-rows: 360px; height: 360px; gap: 20px; margin-bottom: 4px; flex-shrink: 0; }}
</style></head>
<body class="page-sheet">
  <header class="page-header">
    <div class="brand-left">
      <img class="header-logo" src="{asset_url('public/logo-matro-siyah.png')}" alt="MATRO Logo">
      <div class="dept-name">Bursa Teknik Üniversitesi // MATRO İleri Havacılık</div>
    </div>
    <div class="header-meta-right">
      <div class="section-tag">Uçan Araba Simülasyonu</div>
      <div class="page-index-badge">14</div>
    </div>
  </header>

  <!-- Üst Hero: CEZERİ Uçan Araba Simülatörü Önünde BÜRKÜT Takımı -->
  <div class="media-unit burkut-hero">
    <div class="img-box">
      <img style="object-position: center 30%;" src="{asset_url('public/media/galeri-burkut-simulasyon-ekip.jpg')}" alt="CEZERİ ve BÜRKÜT">
    </div>
    <div class="caption-bar">
      <span class="caption-tag">YARIŞMA SAHNESİ</span>
      <span class="caption-text">BÜRKÜT ekibimiz TEKNOFEST'te CEZERİ uçan araba simülatör aracı önünde</span>
    </div>
  </div>

  <div class="burkut-mid">
    <div>
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--c-volt); margin-bottom: 4px;">GELECEĞİN HAVA TAŞITLARI</div>
      <h1 style="font-family: var(--font-display); font-size: 46px; font-weight: 900; line-height: 0.95; text-transform: uppercase;">BÜRKÜT</h1>
      <p style="font-size: 14px; line-height: 1.52; color: #475569; margin-top: 8px;">
        <strong>BÜRKÜT</strong>, şehir içi hava taşımacılığına yönelik dikey iniş-kalkış yapabilen elektrikli hava araçlarının (eVTOL) otonom uçuş kontrolünü ve hava trafiği entegrasyonunu geliştiren ekibimizdir.
      </p>
      <ul class="bullet-list">
        <li>Geçiş dönemi (VTOL'den yatay uçuşa) aerodinamik kontrol modelleri</li>
        <li>Kentsel kanyonlarda güvenli GPS destekli ve optik otonom seyrüsefer</li>
      </ul>
    </div>

    <div class="tech-box">
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; border-bottom: 1.5px solid var(--c-ink); padding-bottom: 4px;">SİMÜLASYON PARAMETRELERİ</div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 10px 0;">
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">ARAÇ KONSEPTİ</span><div style="font-size: 13px; font-weight: 700;">Tilt-Rotor Hibrit</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">İTKİ MİMARİSİ</span><div style="font-size: 13px; font-weight: 700;">8x Eşeksenli Rotor</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">SİMÜLASYON</span><div style="font-size: 13px; font-weight: 700;">Unreal Engine + PX4</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">OTONOMİ</span><div style="font-size: 13px; font-weight: 700;">Seviye 4 Kentsel</div></div>
      </div>
      <div class="award-pill">
        <span class="trophy-dot"></span>
        <span>EN İYİ TAKIM RUHU ÖDÜLÜ BİRİNCİSİ</span>
      </div>
    </div>
  </div>

  <!-- Alt İkili: Selçuk Bayraktar Ödül Töreni (Tam boy, ödül çeki ve plaket net odakta!) + Haluk Bayraktar Brifingi -->
  <div class="burkut-lower">
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center 30%; transform: scale(1.02);" src="{asset_url('public/media/galeri-burkut-calisma.jpg')}" alt="Ödül Töreni">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">ZİRVE ÖDÜLÜ</span>
        <span class="caption-text">Selçuk Bayraktar'dan TEKNOFEST Uçan Araba En İyi Takım Ruhu Ödülü takdimi</span>
      </div>
    </div>
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center 25%;" src="{asset_url('public/media/galeri-bayraktar-ucan-araba.jpg')}" alt="Haluk Bayraktar Brifingi">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">TEKNİK BRİFİNG</span>
        <span class="caption-text">Baykar Genel Müdürü Haluk Bayraktar'a simülasyon algoritmaları sunumu</span>
      </div>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // BÜRKÜT UÇAN ARABA</div>
    <div class="page-number">SAYFA 14</div>
  </footer>
</body>
</html>"""

TASKS = [
    (6, "sayfa-06-ashina", html_p06),
    (7, "sayfa-07-matrover-luna", html_p07),
    (8, "sayfa-08-lodos-ida", html_p08),
    (9, "sayfa-09-prusa-iss", html_p09),
    (10, "sayfa-10-zemheri-sara", html_p10),
    (14, "sayfa-14-burkut", html_p14)
]

def render(num, name, fn):
    html = fn()
    hp = os.path.join(PAGES_DIR, f"{name}.html")
    with open(hp, 'w', encoding='utf-8') as f:
        f.write(html)
    
    png = os.path.join(OUTPUT_DIR, f"{name}.png")
    cmd = [
        CHROME_BIN,
        "--headless=new",
        f"--screenshot={png}",
        "--window-size=1240,1754",
        "--hide-scrollbars",
        f"file://{hp}"
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    size_kb = os.path.getsize(png) / 1024
    print(f"✓ Düzeltildi: Sayfa {num:02d} ({name}) -> {size_kb:.1f} KB")

if __name__ == '__main__':
    print("=== Sayfa 6, 7, 8, 9, 10 ve 14 Hassas Düzeltmeleri Başlatılıyor ===")
    for n, name, fn in TASKS:
        render(n, name, fn)
    print("=== Tüm 6 sayfa kusursuz şekilde güncellendi! ===")
