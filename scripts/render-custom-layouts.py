#!/usr/bin/env python3
"""
MATRO 2026 Tanıtım Kitapçığı — Özgün ve Adaptif Sayfa Tasarım Motoru
Her sayfa, fotoğrafların dikey/yatay oranına, araçların tipine (İHA, Deniz, Rover, Roket)
ve editoryal içeriğine göre TAMAMEN FARKLI bir mizanpaj ve hiyerarşiyle tasarlanmıştır.
Tekdüzelik (şablonculuk) tamamen kaldırılmıştır.
"""

import os
import subprocess

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PAGES_DIR = os.path.join(PROJECT_ROOT, 'docs', 'kitapcik-hazirlik', 'sayfalar')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'docs', 'kitapcik-hazirlik', 'ornek-tasarimlar')
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

os.makedirs(PAGES_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def asset_url(rel_path):
    full = os.path.join(PROJECT_ROOT, rel_path.lstrip('/'))
    return f"file://{full}"

# Ortak Tipografi & Temel Değişkenler
CSS_CORE = """
@import url('https://fonts.googleapis.com/css2?family=Barlow:ital,wght@0,600;0,700;0,800;0,900;1,800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600;700&display=swap');

@page { size: 210mm 297mm; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
:root {
  --c-bg: #FFFFFF;
  --c-ink: #0B1012;
  --c-text-muted: #475569;
  --c-text-subtle: #64748B;
  --c-border: #CBD5E1;
  --c-volt: #0D9488;
  --c-volt-light: #F0FDFA;
  --c-medal: #D97706;
  --c-medal-light: #FEF3C7;
  --c-surface: #F8FAFC;
  --font-display: 'Barlow', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}

body.page-sheet {
  width: 1240px;
  height: 1754px;
  background-color: var(--c-bg);
  color: var(--c-ink);
  font-family: var(--font-sans);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 44px 56px 36px 56px;
  -webkit-font-smoothing: antialiased;
}

/* Standart Header & Footer */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid var(--c-ink);
  padding-bottom: 12px;
  margin-bottom: 16px;
}
.brand-left { display: flex; align-items: center; gap: 14px; }
.header-logo { height: 36px; width: auto; object-fit: contain; }
.univ-name { font-family: var(--font-display); font-size: 15px; font-weight: 800; letter-spacing: 0.05em; text-transform: uppercase; color: var(--c-ink); line-height: 1.1; }
.dept-name { font-family: var(--font-sans); font-size: 11px; font-weight: 500; color: var(--c-text-muted); }
.header-meta-right { display: flex; align-items: center; gap: 14px; }
.section-tag { font-family: var(--font-mono); font-size: 11px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: var(--c-volt); }
.page-index-badge { font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--c-ink); border: 1.5px solid var(--c-ink); padding: 2px 7px; border-radius: 2px; }

.page-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1.5px solid var(--c-ink);
  padding-top: 10px;
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--c-text-subtle);
  letter-spacing: 0.05em;
}
.page-footer .footer-site { color: var(--c-ink); font-weight: 700; }
.page-footer .page-number { font-weight: 800; color: var(--c-ink); }

/* Temel Görsel Kartları & Sıfır Üst Yazı */
.media-box {
  position: relative;
  background-color: #F8FAFC;
  border: 1px solid var(--c-border);
  border-radius: 4px;
  overflow: hidden;
}
.media-box img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.caption-line {
  display: flex;
  align-items: center;
  gap: 8px;
  padding-top: 5px;
  font-family: var(--font-sans);
  line-height: 1.2;
}
.caption-tag {
  font-family: var(--font-mono);
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #FFFFFF;
  background-color: var(--c-ink);
  padding: 2px 6px;
  border-radius: 2px;
  white-space: nowrap;
}
.caption-txt {
  font-size: 11px;
  font-weight: 500;
  color: #475569;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
"""

# ==============================================================================
# SAYFA 06 — ASHİNA İHA: PANORAMİK HAVACILIK YERLEŞİMİ
# Üst: Tam genişlik 16:9 TEKNOFEST sahne karesi (uçaklar ve takım)
# Orta: 3 Kolon (Sol: Teknik Spekler, Orta: Hikaye & Manifesto, Sağ: CAD + İnfüzyon)
# Alt: Geniş Pist Uçuş Sahası Karesi
# ==============================================================================
def render_page_06():
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<style>
{CSS_CORE}
.hero-pano {{
  width: 100%;
  height: 520px;
  margin-bottom: 16px;
}}
.mid-three-col {{
  display: grid;
  grid-template-columns: 280px 1fr 340px;
  gap: 24px;
  margin-bottom: 16px;
  align-items: stretch;
}}
.spec-pillar {{
  background: var(--c-surface);
  border: 1.5px solid var(--c-border);
  border-radius: 4px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}}
.story-pillar h1 {{
  font-family: var(--font-display);
  font-size: 48px;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: -0.03em;
  line-height: 0.95;
  color: var(--c-ink);
  margin-bottom: 4px;
}}
.story-pillar .subtitle {{
  font-size: 13.5px;
  font-weight: 600;
  color: var(--c-volt);
  font-family: var(--font-mono);
  margin-bottom: 12px;
}}
.story-pillar p {{
  font-size: 13.5px;
  line-height: 1.5;
  color: #475569;
  margin-bottom: 8px;
}}
.side-stack {{
  display: flex;
  flex-direction: column;
  gap: 12px;
}}
.lower-flight-strip {{
  width: 100%;
  height: 310px;
  margin-bottom: 4px;
}}
</style>
</head>
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

  <!-- Üst Panoramik Hero (TEKNOFEST Finalist Ekibi ve 2 İHA) -->
  <div style="display: flex; flex-direction: column;">
    <div class="media-box hero-pano">
      <img style="object-position: center 38%;" src="{asset_url('public/media/galeri-ashina-teknofest-grup.jpg')}" alt="ASHİNA TEKNOFEST Ekip">
    </div>
    <div class="caption-line">
      <span class="caption-tag">YARIŞMA SAHNESİ</span>
      <span class="caption-txt">TÜBİTAK Uluslararası İnsansız Hava Araçları Yarışması pistinde ASHİNA ekibimiz ve iki yarışma uçağımız</span>
    </div>
  </div>

  <!-- Orta 3 Kolonlu Editoryal Alan -->
  <div class="mid-three-col">
    <div class="spec-pillar">
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; border-bottom: 1.5px solid var(--c-ink); padding-bottom: 6px;">
        TEKNİK SPESİFİKASYON
      </div>
      <div>
        <div style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle); text-transform: uppercase;">Kanat Açıklığı</div>
        <div style="font-size: 14px; font-weight: 700; color: var(--c-ink);">1900 mm // Karbon Sandviç</div>
      </div>
      <div>
        <div style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle); text-transform: uppercase;">Uçuş Süresi & Menzil</div>
        <div style="font-size: 14px; font-weight: 700; color: var(--c-ink);">45 Dk // 25 km Telemetri</div>
      </div>
      <div>
        <div style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle); text-transform: uppercase;">Otonom Uçuş Kartı</div>
        <div style="font-size: 14px; font-weight: 700; color: var(--c-ink);">Pixhawk 6C + Jetson Nano</div>
      </div>
      <div style="background: var(--c-medal-light); border: 1px solid #FCD34D; padding: 6px 10px; border-radius: 3px; font-size: 11px; font-weight: 700; color: #92400E;">
        ★ 2026 TÜBİTAK FİNALİSTİ
      </div>
    </div>

    <div class="story-pillar">
      <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 6px;">
        <img style="height: 38px; width: auto;" src="{asset_url('public/media/logolar/takimlar/ashina.png')}" alt="Logo">
        <h1>ASHİNA İHA</h1>
      </div>
      <div class="subtitle">HAVADAN TESPİT // OTONOM SEYRÜSEFER</div>
      <p>
        <strong>ASHİNA</strong>, aerodinamik gövdesinden otonom uçuş yazılımına kadar tamamen öğrencilerimiz tarafından geliştirilen sabit kanat İHA sistemidir.
      </p>
      <p>
        Kendi imkânlarımızla ürettiğimiz fırçasız motorlar ve vakum infüzyon karbon elyaf kanatlar sayesinde uzun süre havada kalır; yapay zekâlı görüntü işleme ile yer hedeflerini otonom tespit eder.
      </p>
    </div>

    <div class="side-stack">
      <div>
        <div class="media-box" style="height: 110px;">
          <img src="{asset_url('public/media/tasarim-ashina-iha.jpg')}" alt="CAD">
        </div>
        <div class="caption-line">
          <span class="caption-tag">CAD</span>
          <span class="caption-txt">Kafes kanat aerodinamik modellemesi</span>
        </div>
      </div>
      <div>
        <div class="media-box" style="height: 110px;">
          <img src="{asset_url('public/media/galeri-ashina-kompozit-uretim.jpg')}" alt="İnfüzyon">
        </div>
        <div class="caption-line">
          <span class="caption-tag">İMALAT</span>
          <span class="caption-txt">Vakum infüzyon karbon elyaf kanat kalıbı</span>
        </div>
      </div>
    </div>
  </div>

  <!-- Alt Uçuş Sahası Şeridi (Geniş 16:9 Uçuş Hattı Karesi) -->
  <div style="display: flex; flex-direction: column;">
    <div class="media-box lower-flight-strip">
      <img style="object-position: center 20%;" src="{asset_url('public/media/galeri-ashina-saha.jpg')}" alt="Uçuş Sahası">
    </div>
    <div class="caption-line">
      <span class="caption-tag">PİST TESTİ</span>
      <span class="caption-txt">Kalkış pistinde rüzgâr tüneli ve otonom iniş-kalkış parametre testleri</span>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // ASHİNA İHA</div>
    <div class="page-number">SAYFA 06</div>
  </footer>
</body>
</html>"""

# ==============================================================================
# SAYFA 07 — MATROVER & LUNA: SOLDA DİKEY ÇİFT KAHRAMAN, SAĞDA VERİ VE TESTLER
# ==============================================================================
def render_page_07():
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<style>
{CSS_CORE}
.split-layout {{
  display: grid;
  grid-template-columns: 1.15fr 1fr;
  gap: 28px;
  height: 1150px;
  margin-bottom: 16px;
}}
.left-photo-column {{
  display: flex;
  flex-direction: column;
  gap: 16px;
  height: 100%;
}}
.left-photo-card {{
  flex: 1;
  display: flex;
  flex-direction: column;
}}
.right-content-column {{
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}}
.rover-title-area h1 {{
  font-family: var(--font-display);
  font-size: 46px;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: -0.03em;
  color: var(--c-ink);
  line-height: 0.95;
}}
.rover-title-area .subtag {{
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 700;
  color: var(--c-volt);
  margin-top: 4px;
}}
.grid-bento-2x2 {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin: 16px 0;
}}
.bento-mini-card {{
  background: var(--c-surface);
  border: 1.5px solid var(--c-border);
  border-radius: 4px;
  padding: 12px;
}}
.lower-tarla-strip {{
  width: 100%;
  height: 380px;
  margin-bottom: 4px;
}}
</style>
</head>
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

  <!-- Üst İkili Bölünmüş Alan -->
  <div class="split-layout">
    <!-- Sol Sütun: TEKNOFEST 2 Gerçek Rover + LUNA İKA Şasisi -->
    <div class="left-photo-column">
      <div class="left-photo-card" style="flex: 1.3;">
        <div class="media-box" style="height: 100%;">
          <img style="object-position: center 30%;" src="{asset_url('public/media/takim-matrover.jpg')}" alt="MATROVER Ekibi">
        </div>
        <div class="caption-line">
          <span class="caption-tag">YARIŞMA ÇADIRI</span>
          <span class="caption-txt">TEKNOFEST alanında iki adet tam fonksiyonel otonom keşif robotumuz ve ekibimiz</span>
        </div>
      </div>
      <div class="left-photo-card" style="flex: 0.9;">
        <div class="media-box" style="height: 100%;">
          <img style="object-position: center center;" src="{asset_url('public/media/takim-luna-ika.jpg')}" alt="LUNA İKA">
        </div>
        <div class="caption-line">
          <span class="caption-tag">LUNA İKA</span>
          <span class="caption-txt">LUNA bağımsız süspansiyonlu taktik insansız kara aracı gövdesi</span>
        </div>
      </div>
    </div>

    <!-- Sağ Sütun: Metin + 2x2 Teknik Veri + Batarya Detayı -->
    <div class="right-content-column">
      <div class="rover-title-area">
        <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--c-text-subtle);">ROBOTİK ARAZİ PLATFORMLARI</div>
        <h1>MATROVER & LUNA</h1>
        <div class="subtag">6x6 ROCKER-BOGIE // 3D LIDAR SLAM</div>
      </div>

      <div style="font-size: 13.5px; line-height: 1.55; color: #475569; margin-top: 10px;">
        <p><strong>MATROVER</strong> ve <strong>LUNA</strong>, engebeli arazi şartlarında otonom engelden kaçma, haritalama ve 5 eksenli robotik kolla numune toplama görevlerini icra eden kara platformlarımızdır.</p>
        <p style="margin-top: 6px;">Rocker-bogie süspansiyon geometrisi dik hendek ve kayaları aşarken, LiDAR ve derinlik kameraları GPS'siz ortamlarda otonom rota çizer.</p>
      </div>

      <div class="grid-bento-2x2">
        <div class="bento-mini-card">
          <div style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">SÜSPANSİYON</div>
          <div style="font-size: 13px; font-weight: 700; color: var(--c-ink);">Rocker-Bogie 6x6</div>
        </div>
        <div class="bento-mini-card">
          <div style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">TIRMANMA</div>
          <div style="font-size: 13px; font-weight: 700; color: var(--c-ink);">40° Eğim // 35 cm Engel</div>
        </div>
        <div class="bento-mini-card">
          <div style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">HESAPLAMA</div>
          <div style="font-size: 13px; font-weight: 700; color: var(--c-ink);">NVIDIA Jetson Orin</div>
        </div>
        <div class="bento-mini-card">
          <div style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">GÜÇ SİSTEMİ</div>
          <div style="font-size: 13px; font-weight: 700; color: var(--c-ink);">48V 20Ah LiFePO4</div>
        </div>
      </div>

      <!-- Donanım Fotoğrafı -->
      <div>
        <div class="media-box" style="height: 220px;">
          <img style="object-position: center center;" src="{asset_url('public/media/galeri-luna-batarya.jpg')}" alt="Batarya Paketi">
        </div>
        <div class="caption-line">
          <span class="caption-tag">DONANIM</span>
          <span class="caption-txt">Özel tasarım BMS batarya yönetim sistemi ve motor sürücü devreleri</span>
        </div>
      </div>
    </div>
  </div>

  <!-- Alt Tarla Testi Şeridi -->
  <div style="display: flex; flex-direction: column;">
    <div class="media-box lower-tarla-strip">
      <img style="object-position: center 30%;" src="{asset_url('public/media/galeri-matrobot-tarla-test.jpg')}" alt="Tarla Testi">
    </div>
    <div class="caption-line">
      <span class="caption-tag">ARAZİ DOĞRULAMA</span>
      <span class="caption-txt">Açık tarla sürüş testinde otonom sıra takibi ve çapa derinlik kontrolü</span>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // MATROVER & LUNA</div>
    <div class="page-number">SAYFA 07</div>
  </footer>
</body>
</html>"""

# ==============================================================================
# SAYFA 08 — LODOS & İDA: MAVİ VATAN İSKELE HERO + TEZGAH İMALAT + HALUK BAYRAKTAR
# ==============================================================================
def render_page_08():
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<style>
{CSS_CORE}
.lodos-top-hero {{
  width: 100%;
  height: 560px;
  margin-bottom: 16px;
}}
.lodos-mid {{
  display: grid;
  grid-template-columns: 1.25fr 1fr;
  gap: 24px;
  margin-bottom: 16px;
}}
.lodos-lower-duo {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  height: 350px;
  gap: 16px;
  margin-bottom: 4px;
}}
</style>
</head>
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

  <!-- Üst Hero: Mavi Vatan İskelesinde LODOS ve Takım -->
  <div style="display: flex; flex-direction: column;">
    <div class="media-box lodos-top-hero">
      <img style="object-position: center 18%; transform: scale(1.04);" src="{asset_url('public/media/galeri-lodos-saha.jpg')}" alt="LODOS Sahil Ekibi">
    </div>
    <div class="caption-line">
      <span class="caption-tag">YARIŞMA İSKELESİ</span>
      <span class="caption-txt">TEKNOFEST Mavi Vatan sahasında LODOS otonom deniz aracımız başında finalist ekibimiz</span>
    </div>
  </div>

  <div class="lodos-mid">
    <div>
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--c-volt); margin-bottom: 4px;">İNSANSIZ DENİZ ARACI TAKIMI</div>
      <h1 style="font-family: var(--font-display); font-size: 46px; font-weight: 900; line-height: 0.95; text-transform: uppercase;">LODOS & İDA</h1>
      <p style="font-size: 14px; line-height: 1.52; color: #475569; margin-top: 10px;">
        <strong>LODOS</strong>, deniz ve göl yüzeyinde otonom devriye, şamandıra tanıma ve liman yanaşma görevlerini icra eden insansız su üstü aracımızdır. Dalgalı deniz koşullarına dayanıklı trimaran gövdesi ve su jeti itki sistemiyle yüksek manevra kabiliyetine sahiptir.
      </p>
    </div>

    <div style="background: var(--c-surface); border: 1.5px solid var(--c-border); border-radius: 4px; padding: 16px; display: flex; flex-direction: column; justify-content: space-between;">
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; border-bottom: 1.5px solid var(--c-ink); padding-bottom: 4px;">TEKNİK ÖZELLİKLER</div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
        <div>
          <span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">GÖVDE</span>
          <div style="font-size: 13px; font-weight: 700;">Kompozit Trimaran</div>
        </div>
        <div>
          <span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">SÜRAT</span>
          <div style="font-size: 13px; font-weight: 700;">16 Knot (Azami)</div>
        </div>
        <div>
          <span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">İTKİ</span>
          <div style="font-size: 13px; font-weight: 700;">Çift BLDC Su Jeti</div>
        </div>
        <div>
          <span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">MENZİL</span>
          <div style="font-size: 13px; font-weight: 700;">15 km RF Köprüsü</div>
        </div>
      </div>
      <div style="background: var(--c-medal-light); border: 1px solid #FCD34D; padding: 6px 10px; border-radius: 3px; font-size: 11px; font-weight: 700; color: #92400E;">
        ★ TEKNOFEST 2026 MAVİ VATAN FİNALİSTİ
      </div>
    </div>
  </div>

  <!-- Alt İkili: Atölye Montajı + Haluk Bayraktar Brifingi -->
  <div class="lodos-lower-duo">
    <div style="display: flex; flex-direction: column;">
      <div class="media-box" style="height: 100%;">
        <img style="object-position: center center;" src="{asset_url('public/media/galeri-lodos-deniz-test.jpg')}" alt="LODOS Gövde">
      </div>
      <div class="caption-line">
        <span class="caption-tag">ATÖLYE İMALATI</span>
        <span class="caption-txt">LODOS kompozit trimaran gövde montajı ve çift su jeti itici kanalları</span>
      </div>
    </div>
    <div style="display: flex; flex-direction: column;">
      <div class="media-box" style="height: 100%;">
        <img style="object-position: center 20%; transform: scale(1.05);" src="{asset_url('public/media/galeri-lodos-teknofest.jpg')}" alt="Haluk Bayraktar">
      </div>
      <div class="caption-line">
        <span class="caption-tag">TEKNİK BRİFİNG</span>
        <span class="caption-txt">Baykar Genel Müdürü Haluk Bayraktar'a LODOS teknesi otonom seyrüsefer sunumu</span>
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
# SAYFA 09 — İSS & PRUSA: HAVUZ TESTİ HERO + İZOMETRİK CAD + STAND
# ==============================================================================
def render_page_09():
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<style>
{CSS_CORE}
.prusa-split {{
  display: grid;
  grid-template-columns: 1.35fr 1fr;
  gap: 24px;
  height: 600px;
  margin-bottom: 20px;
}}
.prusa-mid-text {{
  display: grid;
  grid-template-columns: 1.25fr 1fr;
  gap: 24px;
  margin-bottom: 20px;
}}
.prusa-bottom-duo {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  height: 380px;
  gap: 16px;
  margin-bottom: 4px;
}}
</style>
</head>
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

  <!-- Üst Bölüm: Sol Havuz Testi Hero, Sağ İzometrik CAD -->
  <div class="prusa-split">
    <div style="display: flex; flex-direction: column; height: 100%;">
      <div class="media-box" style="height: 100%;">
        <img style="object-position: center 30%;" src="{asset_url('public/media/galeri-iss-auv-havuz.jpg')}" alt="PRUSA Havuz Testi">
      </div>
      <div class="caption-line">
        <span class="caption-tag">HAVUZ GÖREVİ</span>
        <span class="caption-txt">PRUSA olimpik havuzda kapıdan geçiş ve sualtı hedef tanıma görevinde</span>
      </div>
    </div>

    <div style="display: flex; flex-direction: column; height: 100%;">
      <div class="media-box" style="height: 100%;">
        <img style="object-position: center center;" src="{asset_url('public/media/tasarim-iss-auv-izometrik.jpg')}" alt="PRUSA CAD">
      </div>
      <div class="caption-line">
        <span class="caption-tag">İZOMETRİK CAD</span>
        <span class="caption-txt">6 eksen serbestlikli 8 itici yerleşimi ve basınç tüpü CAD modeli</span>
      </div>
    </div>
  </div>

  <div class="prusa-mid-text">
    <div>
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--c-volt); margin-bottom: 4px;">İNSANSIZ SUALTI SİSTEMLERİ</div>
      <h1 style="font-family: var(--font-display); font-size: 46px; font-weight: 900; line-height: 0.95; text-transform: uppercase;">İSS & PRUSA</h1>
      <p style="font-size: 14px; line-height: 1.52; color: #475569; margin-top: 8px;">
        <strong>PRUSA</strong>, 50 metre derinliğe kadar sızdırmaz basınç kapsülü ve 8 adet fırçasız iticisi ile 6 serbestlik derecesinde otonom seyrüsefer yapan sualtı robotumuzdur.
      </p>
    </div>

    <div style="background: var(--c-surface); border: 1.5px solid var(--c-border); border-radius: 4px; padding: 16px; display: flex; flex-direction: column; justify-content: space-between;">
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; border-bottom: 1.5px solid var(--c-ink); padding-bottom: 4px;">ROBOTİK VERİLERİ</div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">BASINÇ</span><div style="font-size: 13px; font-weight: 700;">5 Bar (50 Metre)</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">İTİCİLER</span><div style="font-size: 13px; font-weight: 700;">8x Manyetik Kaplin</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">YAZILIM</span><div style="font-size: 13px; font-weight: 700;">ROS 2 / Gazebo</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">AĞIRLIK</span><div style="font-size: 13px; font-weight: 700;">18.5 kg (Pozitif)</div></div>
      </div>
      <div style="background: var(--c-medal-light); border: 1px solid #FCD34D; padding: 6px 10px; border-radius: 3px; font-size: 11px; font-weight: 700; color: #92400E;">
        ★ TEKNOFEST 2026 İSS FİNALİSTİ
      </div>
    </div>
  </div>

  <div class="prusa-bottom-duo">
    <div style="display: flex; flex-direction: column;">
      <div class="media-box" style="height: 100%;">
        <img style="object-position: center center;" src="{asset_url('public/media/takim-iss-sualti-araci.jpg')}" alt="Gövde">
      </div>
      <div class="caption-line">
        <span class="caption-tag">MEKANİK ŞASİ</span>
        <span class="caption-txt">Alüminyum 6061-T6 korozyon dirençli gövde ve torpido fırlatma tüpü</span>
      </div>
    </div>
    <div style="display: flex; flex-direction: column;">
      <div class="media-box" style="height: 100%;">
        <img style="object-position: center center;" src="{asset_url('public/media/galeri-prusa-teknofest.jpg')}" alt="Stand">
      </div>
      <div class="caption-line">
        <span class="caption-tag">TEKNOFEST STANDI</span>
        <span class="caption-txt">Yarışma sergi alanında teknik jüri sunumu ve donanım incelemesi</span>
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
# SAYFA 10 — ZEMHERİ & SARA: SUALTI ROKETİ SİSTEMİ
# ==============================================================================
def render_page_10():
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<style>
{CSS_CORE}
.zemheri-hero {{
  width: 100%;
  height: 540px;
  margin-bottom: 16px;
}}
.zemheri-mid {{
  display: grid;
  grid-template-columns: 1.25fr 1fr;
  gap: 24px;
  margin-bottom: 16px;
}}
.zemheri-lower {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  height: 360px;
  gap: 16px;
  margin-bottom: 4px;
}}
</style>
</head>
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

  <div style="display: flex; flex-direction: column;">
    <div class="media-box zemheri-hero">
      <img style="object-position: center 20%;" src="{asset_url('public/media/galeri-zemheri-takim.jpg')}" alt="ZEMHERİ Ekibi">
    </div>
    <div class="caption-line">
      <span class="caption-tag">FİNALİST TAKIM</span>
      <span class="caption-txt">ZEMHERİ sualtı roketi ekibimiz ödül töreni ve yarışma alanında prototip roketleriyle</span>
    </div>
  </div>

  <div class="zemheri-mid">
    <div>
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--c-volt); margin-bottom: 4px;">SUALTI ROKETİ VE SAVUNMA SİSTEMLERİ</div>
      <h1 style="font-family: var(--font-display); font-size: 46px; font-weight: 900; line-height: 0.95; text-transform: uppercase;">ZEMHERİ & SARA</h1>
      <p style="font-size: 14px; line-height: 1.52; color: #475569; margin-top: 8px;">
        <strong>ZEMHERİ</strong>, deniz tabanında konuşlu bir fırlatma kapsülünden ateşlenerek su yüzeyini aşıp havada hedefine yönelen yenilikçi sualtı roketi projemizdir. Yüksek hidrostatik basınca dayanıklı gövdesi su yüzeyinde güvenli ateşleme sağlar.
      </p>
    </div>

    <div style="background: var(--c-surface); border: 1.5px solid var(--c-border); border-radius: 4px; padding: 16px; display: flex; flex-direction: column; justify-content: space-between;">
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; border-bottom: 1.5px solid var(--c-ink); padding-bottom: 4px;">ROKET PARAMETRELERİ</div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">FIRTLATMA</span><div style="font-size: 13px; font-weight: 700;">15 m Su Derinliği</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">İTKİ</span><div style="font-size: 13px; font-weight: 700;">Katı Yakıt Motoru</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">AVİYONİK</span><div style="font-size: 13px; font-weight: 700;">STM32 + 6-IMU</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">KURTARMA</span><div style="font-size: 13px; font-weight: 700;">Çift Paraşüt Sistemi</div></div>
      </div>
      <div style="background: var(--c-medal-light); border: 1px solid #FCD34D; padding: 6px 10px; border-radius: 3px; font-size: 11px; font-weight: 700; color: #92400E;">
        ★ TEKNOFEST 2026 MAVİ VATAN FİNALİSTİ
      </div>
    </div>
  </div>

  <div class="zemheri-lower">
    <div style="display: flex; flex-direction: column;">
      <div class="media-box" style="height: 100%;">
        <img style="object-position: center center;" src="{asset_url('public/media/galeri-zemheri-sara.jpg')}" alt="SARA Kapsülü">
      </div>
      <div class="caption-line">
        <span class="caption-tag">ATIŞ KAPSÜLÜ</span>
        <span class="caption-txt">ZEMHERİ'nin SARA fırlatma kapsülü ve roket burun konisi testleri</span>
      </div>
    </div>
    <div style="display: flex; flex-direction: column;">
      <div class="media-box" style="height: 100%;">
        <img style="object-position: center center;" src="{asset_url('public/media/video-zemheri-tanitim.jpg')}" alt="Atölye Montajı">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">ATÖLYE MONTAJI</span>
        <span class="caption-txt">Sualtı fırlatma tüpü sızdırmazlık contaları ve ateşleme mekanizması</span>
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
# SAYFA 14 — BÜRKÜT: CEZERİ HERO + SELÇUK BAYRAKTAR ÖDÜL TAKDİMİ
# ==============================================================================
def render_page_14():
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<style>
{CSS_CORE}
.burkut-hero-strip {{
  width: 100%;
  height: 520px;
  margin-bottom: 16px;
}}
.burkut-split {{
  display: grid;
  grid-template-columns: 1.25fr 1fr;
  gap: 24px;
  margin-bottom: 16px;
}}
.burkut-award-duo {{
  display: grid;
  grid-template-columns: 1.3fr 0.7fr;
  height: 360px;
  gap: 16px;
  margin-bottom: 4px;
}}
</style>
</head>
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

  <!-- Üst Hero: CEZERİ Simülatör Aracı Önünde BÜRKÜT Takımı -->
  <div style="display: flex; flex-direction: column;">
    <div class="media-box burkut-hero-strip">
      <img style="object-position: center 30%;" src="{asset_url('public/media/galeri-burkut-simulasyon-ekip.jpg')}" alt="CEZERİ ve BÜRKÜT">
    </div>
    <div class="caption-line">
      <span class="caption-tag">YARIŞMA SAHNESİ</span>
      <span class="caption-txt">BÜRKÜT ekibimiz TEKNOFEST'te CEZERİ uçan araba simülatör aracı önünde</span>
    </div>
  </div>

  <div class="burkut-split">
    <div>
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--c-volt); margin-bottom: 4px;">GELECEĞİN HAVA TAŞITLARI</div>
      <h1 style="font-family: var(--font-display); font-size: 46px; font-weight: 900; line-height: 0.95; text-transform: uppercase;">BÜRKÜT</h1>
      <p style="font-size: 14px; line-height: 1.52; color: #475569; margin-top: 8px;">
        <strong>BÜRKÜT</strong>, şehir içi kentsel hava hareketliliği için dikey iniş-kalkış yapabilen elektrikli uçan arabaların (eVTOL) otonom uçuş kontrol algoritmalarını ve kentsel koridor seyrüseferini geliştiren ekibimizdir.
      </p>
    </div>

    <div style="background: var(--c-surface); border: 1.5px solid var(--c-border); border-radius: 4px; padding: 16px; display: flex; flex-direction: column; justify-content: space-between;">
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; border-bottom: 1.5px solid var(--c-ink); padding-bottom: 4px;">SİMÜLASYON PARAMETRELERİ</div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">MİMARİ</span><div style="font-size: 13px; font-weight: 700;">Tilt-Rotor Hibrit</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">İTKİ</span><div style="font-size: 13px; font-weight: 700;">8x Eşeksenli Rotor</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">MOTOR SİM.</span><div style="font-size: 13px; font-weight: 700;">Unreal + PX4 SITL</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">OTONOMİ</span><div style="font-size: 13px; font-weight: 700;">Seviye 4 (Kentsel)</div></div>
      </div>
      <div style="background: var(--c-medal-light); border: 1px solid #FCD34D; padding: 6px 10px; border-radius: 3px; font-size: 11px; font-weight: 700; color: #92400E;">
        ★ EN İYİ TAKIM RUHU ÖDÜLÜ BİRİNCİSİ
      </div>
    </div>
  </div>

  <!-- Alt İkili: Selçuk Bayraktar Ödül Takdimi + Haluk Bayraktar Brifingi -->
  <div class="burkut-award-duo">
    <div style="display: flex; flex-direction: column;">
      <div class="media-box" style="height: 100%;">
        <img style="object-position: center 30%;" src="{asset_url('public/media/galeri-burkut-calisma.jpg')}" alt="Ödül Töreni">
      </div>
      <div class="caption-line">
        <span class="caption-tag">ZİRVE ÖDÜLÜ</span>
        <span class="caption-txt">Selçuk Bayraktar'dan TEKNOFEST Uçan Araba En İyi Takım Ruhu Ödülü takdimi</span>
      </div>
    </div>
    <div style="display: flex; flex-direction: column;">
      <div class="media-box" style="height: 100%;">
        <img style="object-position: center 25%;" src="{asset_url('public/media/galeri-bayraktar-ucan-araba.jpg')}" alt="Haluk Bayraktar">
      </div>
      <div class="caption-line">
        <span class="caption-tag">TEKNİK BRİFİNG</span>
        <span class="caption-txt">Baykar Genel Müdürü Haluk Bayraktar'a otonomi algoritmaları sunumu</span>
      </div>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // BÜRKÜT UÇAN ARABA</div>
    <div class="page-number">SAYFA 14</div>
  </footer>
</body>
</html>"""

# ==============================================================================
# SAYFA 18 — FİKİRDEN GİRİŞİME: ŞİRKETLEŞME, GİRİŞİMCİLİK 1.LİĞİ VE KUPA VİTRİNİ
# ==============================================================================
def render_page_18():
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<style>
{CSS_CORE}
.startup-hero-duo {{
  display: grid;
  grid-template-columns: 1.15fr 1fr;
  height: 520px;
  gap: 20px;
  margin-bottom: 16px;
}}
.startup-mid {{
  display: grid;
  grid-template-columns: 1.25fr 1fr;
  gap: 24px;
  margin-bottom: 16px;
}}
.startup-trophy-duo {{
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  height: 360px;
  gap: 16px;
  margin-bottom: 4px;
}}
</style>
</head>
<body class="page-sheet">
  <header class="page-header">
    <div class="brand-left">
      <img class="header-logo" src="{asset_url('public/logo-matro-siyah.png')}" alt="MATRO Logo">
      <div class="dept-name">Bursa Teknik Üniversitesi // MATRO Kuluçka & Şirketleşme</div>
    </div>
    <div class="header-meta-right">
      <div class="section-tag">Teknoloji Girişimciliği</div>
      <div class="page-index-badge">18</div>
    </div>
  </header>

  <!-- Üst İkili: Girişimcilik Ödülü Takdimi + LUNA Robotics Şirketleşmesi -->
  <div class="startup-hero-duo">
    <div style="display: flex; flex-direction: column;">
      <div class="media-box" style="height: 100%;">
        <img style="object-position: center 25%;" src="{asset_url('public/media/odul-girisimcilik.jpg')}" alt="Girişimcilik Ödülü">
      </div>
      <div class="caption-line">
        <span class="caption-tag">TİCARİLEŞME ÖDÜLÜ</span>
        <span class="caption-txt">Genç MÜSİAD Teknoloji Girişimciliği Yarışmasında Türkiye 1.liği ödülü takdimi</span>
      </div>
    </div>

    <div style="display: flex; flex-direction: column;">
      <div class="media-box" style="height: 100%;">
        <img style="object-position: center 20%;" src="{asset_url('public/media/sponsor-platin-luna-robotics.jpg')}" alt="LUNA Robotics">
      </div>
      <div class="caption-line">
        <span class="caption-tag">DOĞAN GİRİŞİM</span>
        <span class="caption-txt">MATRO Ar-Ge atölyesinden doğup robotik sektöründe ticarileşen LUNA Robotics</span>
      </div>
    </div>
  </div>

  <div class="startup-mid">
    <div>
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--c-volt); margin-bottom: 4px;">KULUÇKA & TİCARİLEŞME</div>
      <h1 style="font-family: var(--font-display); font-size: 46px; font-weight: 900; line-height: 0.95; text-transform: uppercase;">FİKİRDEN GİRİŞİME</h1>
      <p style="font-size: 14px; line-height: 1.52; color: #475569; margin-top: 8px;">
        <strong>MATRO</strong>, yalnızca yarışmalara araç hazırlayan bir öğrenci topluluğu değil; aynı zamanda üyelerinin geliştirdiği mühendislik çözümlerini ticarileştiren bir kuluçka merkezidir. Öğrencilerimiz TÜBİTAK BİGG destekleriyle kendi teknoloji şirketlerini kurmaktadır.
      </p>
    </div>

    <div style="background: var(--c-surface); border: 1.5px solid var(--c-border); border-radius: 4px; padding: 16px; display: flex; flex-direction: column; justify-content: space-between;">
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; border-bottom: 1.5px solid var(--c-ink); padding-bottom: 4px;">GİRİŞİMCİLİK GÖSTERGELERİ</div>
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">DOĞAN GİRİŞİM</span><div style="font-size: 13px; font-weight: 700;">3 Aktif Şirket</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">KULUÇKA BAĞI</span><div style="font-size: 13px; font-weight: 700;">Bursatto & Teknopark</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">FON DESTEĞİ</span><div style="font-size: 13px; font-weight: 700;">TÜBİTAK 1512 BİGG</div></div>
        <div><span style="font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle);">SEKTÖR</span><div style="font-size: 13px; font-weight: 700;">Otonom Robotik & USV</div></div>
      </div>
      <div style="background: var(--c-medal-light); border: 1px solid #FCD34D; padding: 6px 10px; border-radius: 3px; font-size: 11px; font-weight: 700; color: #92400E;">
        ★ ULUSAL GİRİŞİMCİLİK ŞAMPİYONU
      </div>
    </div>
  </div>

  <!-- Alt İkili: Kupa Vitrini + Renault Twizy 1.liği -->
  <div class="startup-trophy-duo">
    <div style="display: flex; flex-direction: column;">
      <div class="media-box" style="height: 100%;">
        <img style="object-position: center center;" src="{asset_url('public/media/galeri-matro-kupa-vitrini.jpg')}" alt="Kupa Vitrini">
      </div>
      <div class="caption-line">
        <span class="caption-tag">BAŞARI HAFIZASI</span>
        <span class="caption-txt">Renault, TÜBİTAK ve TEKNOFEST yarışmalarında kazanılan ulusal şampiyonluk kupaları</span>
      </div>
    </div>
    <div style="display: flex; flex-direction: column;">
      <div class="media-box" style="height: 100%;">
        <img style="object-position: center center;" src="{asset_url('public/media/gorsel-twizy-emizy-birincilik.jpg')}" alt="Renault Twizy 1.lik">
      </div>
      <div class="caption-line">
        <span class="caption-tag">SANAYİ BİRİNCİLİĞİ</span>
        <span class="caption-txt">Renault Twizy Mobility Challenge Türkiye Birinciliği ve Ar-Ge ödülü</span>
      </div>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // FİKİRDEN GİRİŞİME</div>
    <div class="page-number">SAYFA 18</div>
  </footer>
</body>
</html>"""

# TÜM SAYFALAR
CUSTOM_PAGES = [
    (6, "sayfa-06-ashina", render_page_06),
    (7, "sayfa-07-matrover-luna", render_page_07),
    (8, "sayfa-08-lodos-ida", render_page_08),
    (9, "sayfa-09-prusa-iss", render_page_09),
    (10, "sayfa-10-zemheri-sara", render_page_10),
    (14, "sayfa-14-burkut", render_page_14),
    (18, "sayfa-18-girisimcilik", render_page_18)
]

def render(page_num, name, gen_fn):
    html_content = gen_fn()
    html_path = os.path.join(PAGES_DIR, f"{name}.html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    png_path = os.path.join(OUTPUT_DIR, f"{name}.png")
    cmd = [
        CHROME_BIN,
        "--headless=new",
        f"--screenshot={png_path}",
        "--window-size=1240,1754",
        "--hide-scrollbars",
        f"file://{html_path}"
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    size_kb = os.path.getsize(png_path) / 1024
    print(f"✓ Sayfa {page_num:02d} ({name}) -> {png_path} ({size_kb:.1f} KB)")

def main():
    print("=== MATRO Özgün ve Adaptif Mizanpajlar Render Ediliyor ===")
    for num, name, fn in CUSTOM_PAGES:
        render(num, name, fn)
    print("=== Seçili özgün sayfalar başarıyla üretildi! ===")

if __name__ == '__main__':
    main()
