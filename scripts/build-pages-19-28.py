#!/usr/bin/env python3
"""
MATRO 2026 Tanıtım Kitapçığı — 19'dan 28'e Kalan Sayfaları Üretme Betiği
Sayfa 19: Başarı Tablosu
Sayfa 20: 2026 Sezonu Haritası
Sayfa 21: Eğitim Faaliyetleri
Sayfa 22: Teknik Geziler
Sayfa 23: Topluluk Hayatı & Sosyal
Sayfa 24: Yönetim Yapısı & Organizasyon
Sayfa 25: Sponsorluk Kataloğu (Logolar)
Sayfa 26: Sponsorluk Paketleri & Haklar
Sayfa 27: Katılım & Başvuru Süreci
Sayfa 28: Arka Kapak & İletişim
"""

import os
import subprocess

PROJECT_ROOT = '/Users/wildgenie/Projects/btu-matro'
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
"""

def p19():
    return f"""<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8"><style>{CSS}
.award-table {{ width: 100%; border-collapse: collapse; margin-bottom: 24px; }}
.award-table th {{ font-family: var(--font-mono); font-size: 11px; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: var(--c-volt); text-align: left; border-bottom: 2px solid var(--c-ink); padding: 10px 12px; }}
.award-table td {{ font-size: 13.5px; border-bottom: 1px solid var(--c-border); padding: 12px; color: var(--c-ink); }}
.year-tag {{ font-family: var(--font-mono); font-weight: 700; color: var(--c-text-muted); }}
.rank-badge {{ font-family: var(--font-mono); font-weight: 800; color: var(--c-medal); background: var(--c-medal-light); padding: 3px 8px; border-radius: 3px; display: inline-block; }}
.lower-bento-2 {{ display: grid; grid-template-columns: 1.1fr 0.9fr; grid-template-rows: 400px; height: 400px; gap: 20px; margin-bottom: 6px; flex-shrink: 0; }}
</style></head>
<body class="page-sheet">
  <header class="page-header">
    <div class="brand-left">
      <img class="header-logo" src="{asset_url('public/logo-matro-siyah.png')}" alt="MATRO Logo">
      <div class="dept-name">Bursa Teknik Üniversitesi // MATRO Başarı Hafızası</div>
    </div>
    <div class="header-meta-right">
      <div class="section-tag">Başarı Tablosu</div>
      <div class="page-index-badge">19</div>
    </div>
  </header>

  <div style="margin-bottom: 16px;">
    <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; letter-spacing: 0.22em; text-transform: uppercase; color: var(--c-volt);">TARİHÇE & PERFORMANS</div>
    <h1 style="font-family: var(--font-display); font-size: 46px; font-weight: 900; line-height: 0.98; text-transform: uppercase; margin-top: 3px; margin-bottom: 5px;">Emek, Deneyim ve Sonuç</h1>
    <p style="font-size: 15px; font-weight: 500; line-height: 1.45; color: #334155;">
      2013'ten bugüne Türkiye ve uluslararası arenalarda kazanılan 50+ kayıtlı derece ve birinciliklerimiz.
    </p>
  </div>

  <table class="award-table">
    <thead>
      <tr>
        <th style="width: 80px;">YIL</th>
        <th>ORGANİZASYON</th>
        <th>KATEGORİ</th>
        <th>TAKIM</th>
        <th style="width: 140px; text-align: right;">DERECE</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="year-tag">2026</td>
        <td>Genç MÜSİAD — Genç Ticaret Elçileri</td>
        <td>Teknoloji Girişimciliği</td>
        <td><strong>GİRİŞİMCİLİK</strong></td>
        <td style="text-align: right;"><span class="rank-badge">Türkiye 1.si</span></td>
      </tr>
      <tr>
        <td class="year-tag">2025</td>
        <td>TEKNOFEST — ASELSAN</td>
        <td>İnsansız Kara Aracı (İKA)</td>
        <td><strong>MATROVER</strong></td>
        <td style="text-align: right;"><span class="rank-badge">Türkiye 3.sü</span></td>
      </tr>
      <tr>
        <td class="year-tag">2024</td>
        <td>Google Developers Group (GDG)</td>
        <td>Yapay Zekâ Hackathonu</td>
        <td><strong>GİRİŞİMCİLİK</strong></td>
        <td style="text-align: right;"><span class="rank-badge">Türkiye 1.si</span></td>
      </tr>
      <tr>
        <td class="year-tag">2024</td>
        <td>NASA Space Apps Challenge</td>
        <td>Uzay Problemleri Çözümü</td>
        <td><strong>GİRİŞİMCİLİK</strong></td>
        <td style="text-align: right;"><span class="rank-badge">Bölge 1.si</span></td>
      </tr>
      <tr>
        <td class="year-tag">2024</td>
        <td>TEKNOFEST Uçan Araba Simülasyonu</td>
        <td>Kentsel Hava Hareketliliği</td>
        <td><strong>BÜRKÜT</strong></td>
        <td style="text-align: right;"><span class="rank-badge">En İyi Takım Ruhu</span></td>
      </tr>
      <tr>
        <td class="year-tag">2021</td>
        <td>Renault Twizy Mobility Challenge</td>
        <td>Elektrikli & Otonom Mobilite</td>
        <td><strong>EMİZY</strong></td>
        <td style="text-align: right;"><span class="rank-badge">Türkiye 1.si</span></td>
      </tr>
    </tbody>
  </table>

  <!-- Alt İkili: Kupa Vitrini + Renault Twizy Birincilik Karesi -->
  <div class="lower-bento-2">
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center center;" src="{asset_url('public/media/galeri-matro-kupa-vitrini.jpg')}" alt="Kupa Vitrini">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">KUPA VİTRİNİ</span>
        <span class="caption-text">BTÜ Mühendislik Fakültesi fuayesindeki MATRO şampiyonluk kupaları sergisi</span>
      </div>
    </div>
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center 30%;" src="{asset_url('public/media/galeri-matro-birincilik-30000.jpg')}" alt="Twizy Birincilik">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">TÜRKİYE ŞAMPİYONLUĞU</span>
        <span class="caption-text">Renault Twizy Mobility Challenge Türkiye 1.liği ödülü takdimi</span>
      </div>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // BAŞARI HAFIZASI</div>
    <div class="page-number">SAYFA 19</div>
  </footer>
</body>
</html>"""

def p20():
    return f"""<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8"><style>{CSS}
.season-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 20px; }}
.city-card {{ background: var(--c-surface); border: 1.5px solid var(--c-border); border-radius: 4px; padding: 14px; display: flex; flex-direction: column; gap: 4px; }}
.season-hero-box {{ width: 100%; height: 620px; margin-bottom: 6px; flex-shrink: 0; }}
</style></head>
<body class="page-sheet">
  <header class="page-header">
    <div class="brand-left">
      <img class="header-logo" src="{asset_url('public/logo-matro-siyah.png')}" alt="MATRO Logo">
      <div class="dept-name">Bursa Teknik Üniversitesi // MATRO 2026 Sezon Özeti</div>
    </div>
    <div class="header-meta-right">
      <div class="section-tag">Sezon Haritası</div>
      <div class="page-index-badge">20</div>
    </div>
  </header>

  <div style="margin-bottom: 16px;">
    <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; letter-spacing: 0.22em; text-transform: uppercase; color: var(--c-volt);">TEKNOFEST 2026 FİNALLERİ</div>
    <h1 style="font-family: var(--font-display); font-size: 46px; font-weight: 900; line-height: 0.98; text-transform: uppercase; margin-top: 3px; margin-bottom: 5px;">Aynı Çatı, Farklı Şehirler, Tek Hedef</h1>
    <p style="font-size: 15px; font-weight: 500; line-height: 1.45; color: #334155;">
      2026 sezonunda 8 ayrı Ar-Ge takımımız Türkiye'nin dört bir yanında finallerde yarışarak üniversitemizi temsil etti.
    </p>
  </div>

  <div class="season-grid">
    <div class="city-card">
      <div style="font-family: var(--font-mono); font-size: 10px; font-weight: 700; color: var(--c-volt);">MALATYA</div>
      <div style="font-family: var(--font-display); font-size: 20px; font-weight: 800; text-transform: uppercase;">ASHİNA İHA</div>
      <div style="font-size: 11px; color: #64748B;">TÜBİTAK Uluslararası İHA</div>
    </div>
    <div class="city-card">
      <div style="font-family: var(--font-mono); font-size: 10px; font-weight: 700; color: var(--c-volt);">DİYARBAKIR</div>
      <div style="font-family: var(--font-display); font-size: 20px; font-weight: 800; text-transform: uppercase;">PUSULA</div>
      <div style="font-size: 11px; color: #64748B;">Sanayide Dijital AMR</div>
    </div>
    <div class="city-card">
      <div style="font-family: var(--font-mono); font-size: 10px; font-weight: 700; color: var(--c-volt);">MARDİN</div>
      <div style="font-family: var(--font-display); font-size: 20px; font-weight: 800; text-transform: uppercase;">LUNA İKA</div>
      <div style="font-size: 11px; color: #64748B;">İnsansız Kara Aracı</div>
    </div>
    <div class="city-card">
      <div style="font-family: var(--font-mono); font-size: 10px; font-weight: 700; color: var(--c-volt);">GAZİANTEP</div>
      <div style="font-family: var(--font-display); font-size: 20px; font-weight: 800; text-transform: uppercase;">MATRİS</div>
      <div style="font-size: 11px; color: #64748B;">HAVELSAN Sürü İHA</div>
    </div>
  </div>

  <div class="media-unit season-hero-box">
    <div class="img-box">
      <img style="object-position: center 25%;" src="{asset_url('public/media/haber-teknofest-2026-finalleri.jpg')}" alt="TEKNOFEST 2026 Finalistleri">
    </div>
    <div class="caption-bar">
      <span class="caption-tag">RESMÎ SEZON TABLOSU</span>
      <span class="caption-text">2026 Sezonunda Malatya, Diyarbakır, Mardin ve Gaziantep etaplarında eşzamanlı yarışan takımlarımız</span>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // SEZON 2026</div>
    <div class="page-number">SAYFA 20</div>
  </footer>
</body>
</html>"""

def p21():
    return f"""<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8"><style>{CSS}
.edu-bento {{ display: grid; grid-template-columns: 1.3fr 1fr; grid-template-rows: 245px 245px; gap: 16px; margin-bottom: 20px; flex-shrink: 0; }}
.edu-hero {{ grid-column: 1 / 2; grid-row: 1 / 3; }}
.edu-cols {{ display: grid; grid-template-columns: 1.2fr 1fr; gap: 24px; margin-bottom: 6px; flex-shrink: 0; }}
</style></head>
<body class="page-sheet">
  <header class="page-header">
    <div class="brand-left">
      <img class="header-logo" src="{asset_url('public/logo-matro-siyah.png')}" alt="MATRO Logo">
      <div class="dept-name">Bursa Teknik Üniversitesi // MATRO Akademi</div>
    </div>
    <div class="header-meta-right">
      <div class="section-tag">Eğitim Faaliyetleri</div>
      <div class="page-index-badge">21</div>
    </div>
  </header>

  <div style="margin-bottom: 16px;">
    <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; letter-spacing: 0.22em; text-transform: uppercase; color: var(--c-volt);">AKADEMİ & ATÖLYE SEMİNERLERİ</div>
    <h1 style="font-family: var(--font-display); font-size: 46px; font-weight: 900; line-height: 0.98; text-transform: uppercase; margin-top: 3px; margin-bottom: 5px;">Öğrenerek Üretmek</h1>
    <p style="font-size: 15px; font-weight: 500; line-height: 1.45; color: #334155;">
      MATRO, üniversiteye yeni başlayan bir öğrenciyi sıfırdan ileri seviye mühendislik yazılımları ve üretim teknikleriyle buluşturan bir okuldur.
    </p>
  </div>

  <div class="edu-bento">
    <div class="media-unit edu-hero">
      <div class="img-box">
        <img style="object-position: center 20%;" src="{asset_url('public/media/galeri-turkish-technic-sinif.jpg')}" alt="Sınıf Eğitimi">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">KURUMSAL EĞİTİM</span>
        <span class="caption-text">Turkish Technic havacılık ve aviyonik bakım eğitim programı</span>
      </div>
    </div>
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center 30%;" src="{asset_url('public/media/haber-atolye-egitimi.jpg')}" alt="Atölye Eğitimi">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">TEMEL EĞİTİM</span>
        <span class="caption-text">Yeni üyelere lehimleme, PCB dizgisi ve emniyet standartları eğitimi</span>
      </div>
    </div>
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center center;" src="{asset_url('public/media/haber-ikinci-egitim.jpg')}" alt="CAD Semineri">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">YAZILIM SEMİNERİ</span>
        <span class="caption-text">SolidWorks ile parametrik makine modelleme ve analiz çalıştayı</span>
      </div>
    </div>
  </div>

  <div class="edu-cols">
    <div>
      <p style="font-size: 14px; line-height: 1.55; color: #475569;">
        Her eğitim dönemi başında açılan MATRO Akademi kapsamında; Katı Modelleme (CAD), Gömülü Sistem Programlama (C/C++, STM32), Robotik İşletim Sistemi (ROS 2), Yapay Zekâ ve Kompozit İmalat eğitimleri düzenlenir.
      </p>
      <ul class="bullet-list">
        <li>Teorik bilginin atölye uygulamasıyla kalıcı hale getirilmesi</li>
        <li>Sanayi profesyonelleri ve mezun mühendislerle mentörlük seansları</li>
      </ul>
    </div>
    <div class="tech-box">
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; border-bottom: 1.5px solid var(--c-ink); padding-bottom: 4px;">AKADEMİ PROGRAMI</div>
      <div style="font-size: 12.5px; color: var(--c-ink); line-height: 1.5; margin-top: 6px;">
        <div><strong>CAD / CAM:</strong> SolidWorks & ANSYS Fluent</div>
        <div><strong>Yazılım:</strong> ROS 2, Python, OpenCV, YOLO</div>
        <div><strong>Elektronik:</strong> Altium Designer ile PCB Tasarımı</div>
      </div>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // EĞİTİM</div>
    <div class="page-number">SAYFA 21</div>
  </footer>
</body>
</html>"""

def p22():
    return f"""<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8"><style>{CSS}
.trip-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); grid-template-rows: 320px 320px; gap: 16px; margin-bottom: 24px; flex-shrink: 0; }}
</style></head>
<body class="page-sheet">
  <header class="page-header">
    <div class="brand-left">
      <img class="header-logo" src="{asset_url('public/logo-matro-siyah.png')}" alt="MATRO Logo">
      <div class="dept-name">Bursa Teknik Üniversitesi // MATRO Sanayi Gezileri</div>
    </div>
    <div class="header-meta-right">
      <div class="section-tag">Teknik Geziler</div>
      <div class="page-index-badge">22</div>
    </div>
  </header>

  <div style="margin-bottom: 16px;">
    <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; letter-spacing: 0.22em; text-transform: uppercase; color: var(--c-volt);">SANAYİ İLE İÇ İÇE</div>
    <h1 style="font-family: var(--font-display); font-size: 46px; font-weight: 900; line-height: 0.98; text-transform: uppercase; margin-top: 3px; margin-bottom: 5px;">Mühendisliği Yerinde Görmek</h1>
    <p style="font-size: 15px; font-weight: 500; line-height: 1.45; color: #334155;">
      Türkiye'nin öncü savunma, havacılık ve otomotiv tesislerine düzenlediğimiz teknik gezilerle teorik bilgiyi doğrudan sanayi ölçeğinde gözlemliyoruz.
    </p>
  </div>

  <div class="trip-grid">
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center center;" src="{asset_url('public/media/haber-tusas-ziyareti.jpg')}" alt="TUSAŞ Ziyareti">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">HAVACILIK ZİRVESİ</span>
        <span class="caption-text">TUSAŞ Türk Havacılık ve Uzay Sanayii tesisleri teknik inceleme ziyaretimiz</span>
      </div>
    </div>
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center 30%;" src="{asset_url('public/media/haber-tubitak-mam.jpg')}" alt="TÜBİTAK MAM">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">AR-GE MERKEZİ</span>
        <span class="caption-text">TÜBİTAK Marmara Araştırma Merkezi laboratuvar ve test altyapısı ziyareti</span>
      </div>
    </div>
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center 30%;" src="{asset_url('public/media/haber-ermetal-gezisi.jpg')}" alt="ERMETAL Gezisi">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">OTOMOTİV SANAYİ</span>
        <span class="caption-text">ERMETAL Otomotiv pres, kalıp ve robotik kaynak hatları teknik gezisi</span>
      </div>
    </div>
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center 60%; transform: scale(1.1);" src="{asset_url('public/media/galeri-hktm-gezisi.jpg')}" alt="HKTM Gezisi">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">HAREKET KONTROL</span>
        <span class="caption-text">HKTM Gebze tesislerinde hidrolik, pnömatik ve mekatronik sistemler incelemesi</span>
      </div>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // GEZİLER</div>
    <div class="page-number">SAYFA 22</div>
  </footer>
</body>
</html>"""

def p23():
    return f"""<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8"><style>{CSS}
.social-grid {{ display: grid; grid-template-columns: 1.2fr 0.8fr; grid-template-rows: 300px 300px; gap: 16px; margin-bottom: 24px; flex-shrink: 0; }}
.social-hero {{ grid-column: 1 / 2; grid-row: 1 / 3; }}
</style></head>
<body class="page-sheet">
  <header class="page-header">
    <div class="brand-left">
      <img class="header-logo" src="{asset_url('public/logo-matro-siyah.png')}" alt="MATRO Logo">
      <div class="dept-name">Bursa Teknik Üniversitesi // MATRO Sosyal Yaşam</div>
    </div>
    <div class="header-meta-right">
      <div class="section-tag">Topluluk Hayatı</div>
      <div class="page-index-badge">23</div>
    </div>
  </header>

  <div style="margin-bottom: 16px;">
    <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; letter-spacing: 0.22em; text-transform: uppercase; color: var(--c-volt);">BİRLİKTE GÜÇLÜYÜZ</div>
    <h1 style="font-family: var(--font-display); font-size: 46px; font-weight: 900; line-height: 0.98; text-transform: uppercase; margin-top: 3px; margin-bottom: 5px;">Öğrenmenin Ötesinde Bir Aile</h1>
    <p style="font-size: 15px; font-weight: 500; line-height: 1.45; color: #334155;">
      Atölye mesailerinin yorgunluğunu tanışma kahvaltıları, spor turnuvaları, doğa kampları ve sosyal etkinliklerle paylaşıyoruz.
    </p>
  </div>

  <div class="social-grid">
    <div class="media-unit social-hero">
      <div class="img-box">
        <img style="object-position: center 35%;" src="{asset_url('public/media/galeri-tanisma-kahvaltisi.jpg')}" alt="Tanışma Etkinliği">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">TANIŞMA BULUŞMASI</span>
        <span class="caption-text">Dönem başı tanışma toplantısında yeni katılan üyelerimiz ve yönetim kurulumuz</span>
      </div>
    </div>
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center 30%;" src="{asset_url('public/media/haber-bahar-piknigi.jpg')}" alt="Bahar Pikniği">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">GELENEKSEL PİKNİK</span>
        <span class="caption-text">Bahar dönemi sonunda tüm takımların katılımıyla gerçekleşen doğa günü</span>
      </div>
    </div>
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center 30%;" src="{asset_url('public/media/haber-hali-saha.jpg')}" alt="Spor Turnuvası">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">SPOR & DOSTLUK</span>
        <span class="caption-text">Takımlar arası moral ve motivasyon artıran halı saha futbol turnuvaları</span>
      </div>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // TOPLULUK</div>
    <div class="page-number">SAYFA 23</div>
  </footer>
</body>
</html>"""

def p24():
    return f"""<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8"><style>{CSS}
.org-chart {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; flex-shrink: 0; }}
.org-col {{ background: var(--c-surface); border: 1.5px solid var(--c-border); border-radius: 4px; padding: 20px 16px; display: flex; flex-direction: column; gap: 12px; }}
.org-col-title {{ font-family: var(--font-display); font-size: 18px; font-weight: 800; color: var(--c-ink); text-transform: uppercase; border-bottom: 2px solid var(--c-ink); padding-bottom: 8px; }}
.org-list {{ list-style: none; display: flex; flex-direction: column; gap: 8px; font-size: 12.5px; color: #475569; }}
.team-photo-wide {{ width: 100%; height: 440px; margin-bottom: 6px; flex-shrink: 0; }}
</style></head>
<body class="page-sheet">
  <header class="page-header">
    <div class="brand-left">
      <img class="header-logo" src="{asset_url('public/logo-matro-siyah.png')}" alt="MATRO Logo">
      <div class="dept-name">Bursa Teknik Üniversitesi // MATRO Yönetim Yapısı</div>
    </div>
    <div class="header-meta-right">
      <div class="section-tag">Yönetim Kurulu</div>
      <div class="page-index-badge">24</div>
    </div>
  </header>

  <div style="margin-bottom: 16px;">
    <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; letter-spacing: 0.22em; text-transform: uppercase; color: var(--c-volt);">KURUMSAL YÖNETİM</div>
    <h1 style="font-family: var(--font-display); font-size: 46px; font-weight: 900; line-height: 0.98; text-transform: uppercase; margin-top: 3px; margin-bottom: 5px;">Topluluğu Birlikte Yürütüyoruz</h1>
    <p style="font-size: 15px; font-weight: 500; line-height: 1.45; color: #334155;">
      MATRO, demokratik ve şeffaf bir kurulla yönetilir. 32 kişilik yönetim ve komite kadromuz takımların tüm lojistik, finansal ve teknik ihtiyaçlarını koordine eder.
    </p>
  </div>

  <div class="org-chart">
    <div class="org-col">
      <div class="org-col-title">Genel Yönetim</div>
      <ul class="org-list">
        <li><strong>Başkan:</strong> Topluluk Temsili</li>
        <li><strong>Başkan Yrd.:</strong> Operasyon</li>
        <li><strong>Genel Sekreter:</strong> Yazışmalar</li>
        <li><strong>Sayman:</strong> Bütçe & Mali İşler</li>
      </ul>
    </div>
    <div class="org-col">
      <div class="org-col-title">Sponsorluk & Fon</div>
      <ul class="org-list">
        <li><strong>Kurumsal:</strong> Sanayi Bağı</li>
        <li><strong>Proje:</strong> Hibe Dosyaları</li>
        <li><strong>Satınalma:</strong> Tedarik</li>
        <li><strong>Lojistik:</strong> Nakliye</li>
      </ul>
    </div>
    <div class="org-col">
      <div class="org-col-title">Tanıtım & Medya</div>
      <ul class="org-list">
        <li><strong>Görsel Tasarım:</strong> Medya</li>
        <li><strong>Web:</strong> Dijital Portföy</li>
        <li><strong>Basın:</strong> Yayın & Bülten</li>
        <li><strong>Etkinlik:</strong> Organizasyon</li>
      </ul>
    </div>
    <div class="org-col">
      <div class="org-col-title">Ar-Ge & Takımlar</div>
      <ul class="org-list">
        <li><strong>Hava:</strong> İHA Koordinasyonu</li>
        <li><strong>Deniz:</strong> USV & AUV Bağı</li>
        <li><strong>Kara:</strong> Rover & AMR Bağı</li>
        <li><strong>Akademi:</strong> Üye Seminerleri</li>
      </ul>
    </div>
  </div>

  <div class="media-unit team-photo-wide">
    <div class="img-box">
      <img style="object-position: center 35%;" src="{asset_url('public/media/ekip-kampus.jpg')}" alt="Yönetim Kurulu ve Üyeler">
    </div>
    <div class="caption-bar">
      <span class="caption-tag">YÖNETİM & DANIŞMA</span>
      <span class="caption-text">Bursa Teknik Üniversitesi kampüsünde topluluk yönetim kurulu ve aktif üyelerimiz</span>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // YÖNETİM</div>
    <div class="page-number">SAYFA 24</div>
  </footer>
</body>
</html>"""

def p25():
    return f"""<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8"><style>{CSS}
.tier-section {{ margin-bottom: 24px; flex-shrink: 0; }}
.tier-header {{ display: flex; align-items: center; gap: 10px; font-family: var(--font-mono); font-size: 11px; font-weight: 700; letter-spacing: 0.16em; text-transform: uppercase; border-bottom: 1.5px solid var(--c-ink); padding-bottom: 6px; margin-bottom: 14px; }}
.logo-grid {{ display: grid; gap: 16px; }}
.logo-grid.tier-plat {{ grid-template-columns: repeat(3, 1fr); }}
.logo-grid.tier-gold {{ grid-template-columns: repeat(4, 1fr); }}
.logo-grid.tier-bronze {{ grid-template-columns: repeat(6, 1fr); }}
.logo-card {{ background: var(--c-surface); border: 1px solid var(--c-border); border-radius: 4px; padding: 16px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; text-align: center; }}
.logo-card img {{ height: 50px; width: auto; max-width: 100%; object-fit: contain; }}
.logo-name {{ font-size: 11px; font-weight: 700; color: var(--c-ink); }}
.logo-type {{ font-family: var(--font-mono); font-size: 9px; color: var(--c-text-subtle); text-transform: uppercase; }}
</style></head>
<body class="page-sheet">
  <header class="page-header">
    <div class="brand-left">
      <img class="header-logo" src="{asset_url('public/logo-matro-siyah.png')}" alt="MATRO Logo">
      <div class="dept-name">Bursa Teknik Üniversitesi // MATRO Destekçilerimiz</div>
    </div>
    <div class="header-meta-right">
      <div class="section-tag">Sponsorluk Kataloğu</div>
      <div class="page-index-badge">25</div>
    </div>
  </header>

  <div style="margin-bottom: 16px;">
    <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; letter-spacing: 0.22em; text-transform: uppercase; color: var(--c-volt);">GÜÇ BİRLİĞİ</div>
    <h1 style="font-family: var(--font-display); font-size: 46px; font-weight: 900; line-height: 0.98; text-transform: uppercase; margin-top: 3px; margin-bottom: 5px;">Üretimin Arkasındaki Destek</h1>
    <p style="font-size: 15px; font-weight: 500; line-height: 1.45; color: #334155;">
      Araçlarımızın malzeme, yazılım, üretim ve seyahat giderlerinde yanımızda durarak millî teknoloji üretimine katkı sağlayan kurumsal sponsorlarımız.
    </p>
  </div>

  <div class="tier-section">
    <div class="tier-header" style="color: var(--c-volt);"><span>■ Platin Düzey Destekçilerimiz</span></div>
    <div class="logo-grid tier-plat">
      <div class="logo-card">
        <img src="{asset_url('public/media/logolar/vatanjet.png')}" alt="Vatanjet">
        <div class="logo-name">VATANJET</div>
        <div class="logo-type">Ulaşım Sponsoru</div>
      </div>
      <div class="logo-card">
        <img src="{asset_url('public/media/logolar/luna-robotics.png')}" alt="Luna Robotics">
        <div class="logo-name">LUNA ROBOTICS</div>
        <div class="logo-type">Ar-Ge & Malzeme</div>
      </div>
      <div class="logo-card">
        <img src="{asset_url('public/media/logolar/tekyaz.png')}" alt="Tekyaz">
        <div class="logo-name">TEKYAZ</div>
        <div class="logo-type">SolidWorks Yazılım</div>
      </div>
    </div>
  </div>

  <div class="tier-section">
    <div class="tier-header" style="color: var(--c-medal);"><span>■ Altın ve Gümüş Düzey Destekçilerimiz</span></div>
    <div class="logo-grid tier-gold">
      <div class="logo-card">
        <img src="{asset_url('public/media/logolar/akkus-enerji.png')}" alt="Akkuş Enerji">
        <div class="logo-name">AKKUŞ ENERJİ</div>
        <div class="logo-type">Nakit & Enerji</div>
      </div>
      <div class="logo-card">
        <img src="{asset_url('public/media/logolar/kayra-yemek.png')}" alt="Kayra Yemek">
        <div class="logo-name">KAYRA YEMEK</div>
        <div class="logo-type">Gıda Sponsoru</div>
      </div>
      <div class="logo-card">
        <img src="{asset_url('public/media/logolar/biyolift.png')}" alt="Biyolift">
        <div class="logo-name">BİYOLİFT</div>
        <div class="logo-type">Hizmet & Malzeme</div>
      </div>
      <div class="logo-card">
        <img src="{asset_url('public/media/logolar/finemold.png')}" alt="Finemold">
        <div class="logo-name">FINEMOLD</div>
        <div class="logo-type">Kalıp İmalat</div>
      </div>
    </div>
  </div>

  <div class="tier-section">
    <div class="tier-header" style="color: var(--c-text-muted);"><span>■ Bronz Düzey ve Teknik Üretim Sponsorlarımız</span></div>
    <div class="logo-grid tier-bronze">
      <div class="logo-card"><img src="{asset_url('public/media/logolar/ibras.png')}" alt="İbraş"><div class="logo-name">İBRAŞ</div></div>
      <div class="logo-card"><img src="{asset_url('public/media/logolar/pinar-metal.png')}" alt="Pınar Metal"><div class="logo-name">PINAR METAL</div></div>
      <div class="logo-card"><img src="{asset_url('public/media/logolar/marka-lazer.png')}" alt="Marka Lazer"><div class="logo-name">MARKA LAZER</div></div>
      <div class="logo-card"><img src="{asset_url('public/media/logolar/tsg.png')}" alt="TSG"><div class="logo-name">TSG SAC</div></div>
      <div class="logo-card"><img src="{asset_url('public/media/logolar/cakir.png')}" alt="Çakır"><div class="logo-name">ÇAKIR</div></div>
      <div class="logo-card"><img src="{asset_url('public/media/logolar/off-ee.png')}" alt="Off-ee"><div class="logo-name">OFF-EE</div></div>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // SPONSORLAR</div>
    <div class="page-number">SAYFA 25</div>
  </footer>
</body>
</html>"""

def p26():
    return f"""<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8"><style>{CSS}
.package-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; flex-shrink: 0; }}
.pkg-card {{ background: var(--c-surface); border: 1.5px solid var(--c-border); border-radius: 4px; padding: 20px 16px; display: flex; flex-direction: column; justify-content: space-between; gap: 14px; }}
.pkg-tier {{ font-family: var(--font-mono); font-size: 11px; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; }}
.pkg-name {{ font-family: var(--font-display); font-size: 24px; font-weight: 800; color: var(--c-ink); text-transform: uppercase; }}
.pkg-rights {{ list-style: none; display: flex; flex-direction: column; gap: 8px; font-size: 12.5px; color: #475569; }}
.pkg-rights li::before {{ content: "✓ "; color: var(--c-volt); font-weight: 700; }}
.steps-box {{ background: var(--c-ink); color: #FFFFFF; border-radius: 4px; padding: 24px; display: flex; flex-direction: column; gap: 14px; margin-bottom: 6px; flex-shrink: 0; }}
.steps-row {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }}
</style></head>
<body class="page-sheet">
  <header class="page-header">
    <div class="brand-left">
      <img class="header-logo" src="{asset_url('public/logo-matro-siyah.png')}" alt="MATRO Logo">
      <div class="dept-name">Bursa Teknik Üniversitesi // MATRO İş Birliği Modelleri</div>
    </div>
    <div class="header-meta-right">
      <div class="section-tag">Paketler & Haklar</div>
      <div class="page-index-badge">26</div>
    </div>
  </header>

  <div style="margin-bottom: 16px;">
    <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; letter-spacing: 0.22em; text-transform: uppercase; color: var(--c-volt);">GELECEĞE YATIRIM</div>
    <h1 style="font-family: var(--font-display); font-size: 46px; font-weight: 900; line-height: 0.98; text-transform: uppercase; margin-top: 3px; margin-bottom: 5px;">Bir Projenin İhtiyaçları</h1>
    <p style="font-size: 15px; font-weight: 500; line-height: 1.45; color: #334155;">
      MATRO takımlarını destekleyerek genç mühendislik yetenekleriyle doğrudan tanışabilir, Ar-Ge araçlarımız üzerinde markanızı binlerce teknoloji meraklısına ulaştırabilirsiniz.
    </p>
  </div>

  <div class="package-grid">
    <div class="pkg-card" style="border-top: 4px solid var(--c-volt);">
      <div><span class="pkg-tier" style="color: var(--c-volt);">KADEME 01</span><h3 class="pkg-name">Platin</h3></div>
      <ul class="pkg-rights">
        <li>Tüm araçlarda ana logo görünürlüğü</li>
        <li>Takım formalarında göğüs logosu</li>
        <li>Sosyal medyada özel tanıtım filmi</li>
        <li>BTÜ kampüsünde stant ve kariyer günü</li>
      </ul>
    </div>
    <div class="pkg-card" style="border-top: 4px solid var(--c-medal);">
      <div><span class="pkg-tier" style="color: var(--c-medal);">KADEME 02</span><h3 class="pkg-name">Altın</h3></div>
      <ul class="pkg-rights">
        <li>Yarışma araçlarında gövde logosu</li>
        <li>Takım formalarında kol logosu</li>
        <li>Web sitesi ve bültenlerde görünürlük</li>
        <li>Teknik atölye ziyareti ve brifing</li>
      </ul>
    </div>
    <div class="pkg-card" style="border-top: 4px solid #94A3B8;">
      <div><span class="pkg-tier" style="color: #64748B;">KADEME 03</span><h3 class="pkg-name">Gümüş</h3></div>
      <ul class="pkg-rights">
        <li>Seçilen takım aracında logo</li>
        <li>Web sitesi kurumsal logo alanı</li>
        <li>Sosyal medya teşekkür duyurusu</li>
        <li>Yıllık faaliyet raporunda yer alma</li>
      </ul>
    </div>
    <div class="pkg-card" style="border-top: 4px solid #D97706;">
      <div><span class="pkg-tier" style="color: #D97706;">KADEME 04</span><h3 class="pkg-name">Bronz</h3></div>
      <ul class="pkg-rights">
        <li>Malzeme veya tezgâh tahsisi</li>
        <li>Web sitesi destekçi listesi</li>
        <li>Toplu sponsorluk panosunda logo</li>
        <li>Öğrenci CV havuzuna erişim</li>
      </ul>
    </div>
  </div>

  <div class="steps-box">
    <div style="font-family: var(--font-display); font-size: 20px; font-weight: 800; text-transform: uppercase; color: #00F5D4;">Sponsorluk Süreci Nasıl İşler?</div>
    <div class="steps-row">
      <div><div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: #00F5D4;">01 // İLETİŞİM</div><div style="font-size: 13px; color: #CBD5E1; margin-top: 4px;">Topluluk yönetimimizle tanışma ve ihtiyaç duyulan teknik kalemin belirlenmesi.</div></div>
      <div><div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: #00F5D4;">02 // PROTOKOL</div><div style="font-size: 13px; color: #CBD5E1; margin-top: 4px;">Bursa Teknik Üniversitesi Rektörlüğü onaylı resmî sponsorluk protokolü.</div></div>
      <div><div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: #00F5D4;">03 // ENTEGRASYON</div><div style="font-size: 13px; color: #CBD5E1; margin-top: 4px;">Malzemenin araca entegrasyonu, logoların giydirilmesi ve medya duyurusu.</div></div>
      <div><div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: #00F5D4;">04 // RAPORLAMA</div><div style="font-size: 13px; color: #CBD5E1; margin-top: 4px;">Yarışma sonrası detaylı başarı, görünürlük ve basın yansıması raporu teslimi.</div></div>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // PAKETLER</div>
    <div class="page-number">SAYFA 26</div>
  </footer>
</body>
</html>"""

def p27():
    return f"""<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8"><style>{CSS}
.apply-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 24px; flex-shrink: 0; }}
.apply-card {{ background: var(--c-surface); border: 1.5px solid var(--c-border); border-radius: 4px; padding: 24px; display: flex; flex-direction: column; gap: 12px; }}
.banner-wide {{ width: 100%; height: 480px; margin-bottom: 6px; flex-shrink: 0; }}
</style></head>
<body class="page-sheet">
  <header class="page-header">
    <div class="brand-left">
      <img class="header-logo" src="{asset_url('public/logo-matro-siyah.png')}" alt="MATRO Logo">
      <div class="dept-name">Bursa Teknik Üniversitesi // MATRO Üye Kabul</div>
    </div>
    <div class="header-meta-right">
      <div class="section-tag">Katılım Süreci</div>
      <div class="page-index-badge">27</div>
    </div>
  </header>

  <div style="margin-bottom: 16px;">
    <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; letter-spacing: 0.22em; text-transform: uppercase; color: var(--c-volt);">ARAMIZA KATIL</div>
    <h1 style="font-family: var(--font-display); font-size: 46px; font-weight: 900; line-height: 0.98; text-transform: uppercase; margin-top: 3px; margin-bottom: 5px;">MATRO’da Kendi Yolunu Seç</h1>
    <p style="font-size: 15px; font-weight: 500; line-height: 1.45; color: #334155;">
      Bursa Teknik Üniversitesi'nde okuyan tüm bölümlerden öğrencilere kapımız açıktır. Ön bilgi şartı yok; öğrenme azmi ve takım disiplini esastır.
    </p>
  </div>

  <div class="apply-grid">
    <div class="apply-card">
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--c-volt);">ADIM 01</div>
      <h3 style="font-family: var(--font-display); font-size: 22px; font-weight: 800; text-transform: uppercase;">Topluluk Kaydı</h3>
      <p style="font-size: 13.5px; color: #475569; line-height: 1.5;">Dönem başı açılan resmî kayıt formunu doldurarak MATRO ailesine adım at. E-posta listesine ve Discord çalışma gruplarına dahil ol.</p>
    </div>
    <div class="apply-card">
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--c-volt);">ADIM 02</div>
      <h3 style="font-family: var(--font-display); font-size: 22px; font-weight: 800; text-transform: uppercase;">Akademi Eğitimi</h3>
      <p style="font-size: 13.5px; color: #475569; line-height: 1.5;">Temel CAD, kodlama ve atölye emniyet seminerlerine katıl. İlgilendiğin hava, kara, deniz veya yazılım alanındaki mentörlerle tanış.</p>
    </div>
    <div class="apply-card">
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--c-volt);">ADIM 03</div>
      <h3 style="font-family: var(--font-display); font-size: 22px; font-weight: 800; text-transform: uppercase;">Takım Seçimi</h3>
      <p style="font-size: 13.5px; color: #475569; line-height: 1.5;">15 Ar-Ge takımımızdan birinin alt projesinde aday mühendis olarak yer al. Kendi tasarladığın parçayı TEKNOFEST sahnesinde gör.</p>
    </div>
  </div>

  <div class="media-unit banner-wide">
    <div class="img-box">
      <img style="object-position: center 35%;" src="{asset_url('public/media/haber-tanisma-etkinligi.jpg')}" alt="Tanışma Etkinliği">
    </div>
    <div class="caption-bar">
      <span class="caption-tag">ORYANTASYON GÜNÜ</span>
      <span class="caption-text">BTÜ Mimar Sinan Yerleşkesinde yeni dönem üye kayıt ve bilgilendirme standımız</span>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // BAŞVURU</div>
    <div class="page-number">SAYFA 27</div>
  </footer>
</body>
</html>"""

def p28():
    return f"""<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8"><style>{CSS}
.back-cover-container {{ flex: 1; display: flex; flex-direction: column; justify-content: space-between; margin-top: 20px; }}
.back-hero-box {{ width: 100%; height: 780px; border-radius: 4px; overflow: hidden; background: #0B1012; border: 1.5px solid var(--c-border); }}
.contact-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; border-top: 2px solid var(--c-ink); padding-top: 28px; }}
</style></head>
<body class="page-sheet">
  <header class="page-header">
    <div class="brand-left">
      <img class="header-logo" src="{asset_url('public/logo-matro-siyah.png')}" alt="MATRO Logo">
      <div class="dept-name">Bursa Teknik Üniversitesi // Makine Teknolojileri Robot ve Otomasyon Topluluğu</div>
    </div>
    <div class="header-meta-right">
      <div class="section-tag">Portföy Kapanışı</div>
      <div class="page-index-badge">28</div>
    </div>
  </header>

  <div class="back-cover-container">
    <div>
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; letter-spacing: 0.22em; text-transform: uppercase; color: var(--c-volt);">GELECEĞİ BİRLİKTE ÜRETİYORUZ</div>
      <h1 style="font-family: var(--font-display); font-size: 54px; font-weight: 900; line-height: 0.98; text-transform: uppercase; margin-top: 4px; margin-bottom: 6px;">Bir Sonraki Projede Görüşmek Üzere</h1>
      <p style="font-size: 16px; font-weight: 500; line-height: 1.45; color: #334155;">
        2013 yılından bu yana süren teknoloji ve mühendislik yolculuğumuzda bize inanan tüm akademisyenlerimize, sponsorlarımıza ve fedakâr ekip üyelerimize teşekkür ederiz.
      </p>
    </div>

    <div class="media-unit back-hero-box">
      <div class="img-box">
        <img style="object-position: center 20%;" src="{asset_url('public/media/fuar-standi.jpg')}" alt="Fuar Standı ve Ekip">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">GELECEK VİZYONU</span>
        <span class="caption-text">Milli Teknoloji Hamlesi vizyonuyla atölyeden sahaya, dünya standartlarında mühendislik</span>
      </div>
    </div>

    <div class="contact-grid">
      <div>
        <span style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--c-volt); text-transform: uppercase;">Atölye & Yerleşke</span>
        <div style="font-size: 14px; font-weight: 600; color: var(--c-ink); line-height: 1.4; margin-top: 4px;">Bursa Teknik Üniversitesi<br>Mimar Sinan Yerleşkesi<br>Özdemir Bayraktar Atölyesi</div>
      </div>
      <div>
        <span style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--c-volt); text-transform: uppercase;">Elektronik Posta</span>
        <div style="font-size: 14px; font-weight: 600; color: var(--c-ink); line-height: 1.4; margin-top: 4px;">matroiletisim@gmail.com<br>matrobtu@gmail.com</div>
      </div>
      <div>
        <span style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--c-volt); text-transform: uppercase;">Web & Sosyal Medya</span>
        <div style="font-size: 14px; font-weight: 600; color: var(--c-ink); line-height: 1.4; margin-top: 4px;">btumatro.com<br>instagram.com/btumatro<br>linkedin.com/company/btumatro</div>
      </div>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // MATRO 2026</div>
    <div class="page-number">SAYFA 28</div>
  </footer>
</body>
</html>"""

PAGES_19_28 = [
    (19, "sayfa-19-basarilar", p19),
    (20, "sayfa-20-sezon", p20),
    (21, "sayfa-21-egitim", p21),
    (22, "sayfa-22-geziler", p22),
    (23, "sayfa-23-sosyal", p23),
    (24, "sayfa-24-organizasyon", p24),
    (25, "sayfa-25-sponsorlar", p25),
    (26, "sayfa-26-paketler", p26),
    (27, "sayfa-27-katilim", p27),
    (28, "sayfa-28-kapanis", p28),
]

for num, name, fn in PAGES_19_28:
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
    print(f"✓ Üretildi: Sayfa {num:02d} ({name}) -> {size_kb:.1f} KB")

print("19-28 arası tüm sayfalar başarıyla üretildi!")
