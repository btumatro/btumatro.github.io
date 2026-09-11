#!/usr/bin/env python3
"""
MATRO 2026 Tanıtım Kitapçığı & Portföy A4 Sayfa Üretim Motoru (V12 - Autonomous Quality Engine)
- Her sayfa için içeriğin türüne (Hava, Deniz, Kara, Biyomedikal, Kuluçka) uygun özgün mizanpaj.
- Sentetik görseller yalnızca orijinal nesneyle %100 uyuşuyorsa kullanılır; uyuşmayanlar yerine gerçek test kareleri yer alır.
- Sıfır yazı bindirme (Zero-Overlay); etiketler çerçevenin altındaki editoryal altyazı çubuğunda.
- 1'den 28'e kadar tüm sayfaları eksiksiz ve hatasız derler.
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

CSS_MASTER = """
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

/* Header */
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

/* Footer */
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

/* Tipografi */
.eyebrow {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--c-volt);
}
.headline {
  font-family: var(--font-display);
  font-size: 44px;
  font-weight: 900;
  line-height: 0.98;
  letter-spacing: -0.03em;
  text-transform: uppercase;
  color: var(--c-ink);
  margin-top: 3px;
  margin-bottom: 5px;
}
.lead-text {
  font-size: 15px;
  font-weight: 500;
  line-height: 1.45;
  color: #334155;
}

/* Görsel Çerçevesi & Sıfır Üst Yazı */
.media-unit {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.img-box {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  background-color: #F8FAFC;
  border-radius: 4px;
  border: 1px solid var(--c-border);
}
.img-box img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.caption-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding-top: 6px;
  font-family: var(--font-sans);
  line-height: 1.25;
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
.caption-text {
  font-size: 11px;
  font-weight: 500;
  color: #475569;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Bullet & Teknik Kutu */
.bullet-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.bullet-list li {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 13.5px;
  font-weight: 600;
  color: var(--c-ink);
  line-height: 1.35;
}
.bullet-list li::before {
  content: "■";
  color: var(--c-volt);
  font-size: 9px;
  margin-top: 3px;
}

.tech-spec-box {
  background: var(--c-surface);
  border: 1.5px solid var(--c-border);
  border-radius: 4px;
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.box-title {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--c-ink);
  border-bottom: 1.5px solid var(--c-ink);
  padding-bottom: 6px;
  display: flex;
  justify-content: space-between;
}
.spec-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px 14px;
}
.spec-item {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.spec-label {
  font-family: var(--font-mono);
  font-size: 9px;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--c-text-subtle);
}
.spec-value {
  font-size: 12.5px;
  font-weight: 600;
  color: var(--c-ink);
}
.award-pill {
  background: var(--c-medal-light);
  border: 1px solid #FCD34D;
  color: #92400E;
  padding: 7px 12px;
  border-radius: 3px;
  font-size: 11.5px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
}
.award-pill .trophy-dot {
  width: 6px;
  height: 6px;
  background: var(--c-medal);
  border-radius: 50%;
}
"""

def generate_team_page_v12(page_num, page_tag, team_title, team_category, team_logo_path,
                           hero_img, hero_pos, hero_zoom, hero_tag, hero_caption,
                           side1_img, side1_pos, side1_zoom, side1_tag, side1_caption,
                           side2_img, side2_pos, side2_zoom, side2_tag, side2_caption,
                           lead_p, body_p, bullets,
                           award_text, spec_model, specs,
                           ribbon1_img, ribbon1_pos, ribbon1_zoom, ribbon1_tag, ribbon1_caption,
                           ribbon2_img, ribbon2_pos, ribbon2_zoom, ribbon2_tag, ribbon2_caption):
    spec_items_html = ""
    for label, val in specs:
        spec_items_html += f"""
        <div class="spec-item">
          <span class="spec-label">{label}</span>
          <span class="spec-value">{val}</span>
        </div>"""

    bullets_html = "".join([f"<li>{b}</li>" for b in bullets])
    logo_img_tag = f'<img class="team-symbol" src="{asset_url(team_logo_path)}" alt="{team_title} Logo">' if team_logo_path else ''

    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<style>
{CSS_MASTER}
.team-header-row {{
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 14px;
}}
.team-branding {{ display: flex; align-items: center; gap: 18px; }}
.team-symbol {{ height: 50px; width: auto; object-fit: contain; }}
.team-titles {{ display: flex; flex-direction: column; }}
.team-eyebrow {{ font-family: var(--font-mono); font-size: 11.5px; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; color: var(--c-volt); }}
.team-main-name {{ font-family: var(--font-display); font-size: 48px; font-weight: 900; line-height: 0.95; letter-spacing: -0.03em; color: var(--c-ink); text-transform: uppercase; }}
.team-category {{ font-size: 14px; font-weight: 600; color: var(--c-text-muted); margin-top: 3px; }}
.upper-bento {{
  display: grid;
  grid-template-columns: 1.8fr 1fr;
  grid-template-rows: 245px 245px;
  gap: 14px;
  margin-bottom: 18px;
}}
.hero-box {{ grid-column: 1 / 2; grid-row: 1 / 3; }}
.middle-split {{ display: grid; grid-template-columns: 1.25fr 1fr; gap: 24px; margin-bottom: 18px; }}
.desc-text p {{ font-size: 14px; line-height: 1.52; color: #475569; margin-bottom: 8px; }}
.lower-ribbon {{ display: grid; grid-template-columns: 1fr 1fr; height: 280px; gap: 14px; margin-bottom: 6px; }}
</style>
</head>
<body class="page-sheet">
  <header class="page-header">
    <div class="brand-left">
      <img class="header-logo" src="{asset_url('public/logo-matro-siyah.png')}" alt="MATRO Logo">
      <div class="header-brand-text">
        <div class="univ-name">Bursa Teknik Üniversitesi</div>
        <div class="dept-name">MATRO // Ar-Ge Takım Portföyü</div>
      </div>
    </div>
    <div class="header-meta-right">
      <div class="section-tag">{page_tag}</div>
      <div class="page-index-badge">{page_num:02d}</div>
    </div>
  </header>

  <div class="team-header-row">
    <div class="team-branding">
      {logo_img_tag}
      <div class="team-titles">
        <div class="team-eyebrow">Ar-Ge Proje Takımı</div>
        <h1 class="team-main-name">{team_title}</h1>
        <div class="team-category">{team_category}</div>
      </div>
    </div>
    <div class="award-pill">
      <span class="trophy-dot"></span>
      <span>{award_text}</span>
    </div>
  </div>

  <div class="upper-bento">
    <div class="media-unit hero-box">
      <div class="img-box">
        <img style="object-position: {hero_pos}; transform: scale({hero_zoom});" src="{asset_url(hero_img)}" alt="{hero_tag}">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">{hero_tag}</span>
        <span class="caption-text">{hero_caption}</span>
      </div>
    </div>

    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: {side1_pos}; transform: scale({side1_zoom});" src="{asset_url(side1_img)}" alt="{side1_tag}">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">{side1_tag}</span>
        <span class="caption-text">{side1_caption}</span>
      </div>
    </div>

    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: {side2_pos}; transform: scale({side2_zoom});" src="{asset_url(side2_img)}" alt="{side2_tag}">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">{side2_tag}</span>
        <span class="caption-text">{side2_caption}</span>
      </div>
    </div>
  </div>

  <div class="middle-split">
    <div class="desc-text">
      <p><strong>{team_title}</strong>, {lead_p}</p>
      <p>{body_p}</p>
      <ul class="bullet-list">
        {bullets_html}
      </ul>
    </div>

    <div class="tech-spec-box">
      <div class="box-title">
        <span>Teknik Spesifikasyonlar</span>
        <span>{spec_model}</span>
      </div>
      <div class="spec-grid">
        {spec_items_html}
      </div>
    </div>
  </div>

  <div class="lower-ribbon">
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: {ribbon1_pos}; transform: scale({ribbon1_zoom});" src="{asset_url(ribbon1_img)}" alt="{ribbon1_tag}">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">{ribbon1_tag}</span>
        <span class="caption-text">{ribbon1_caption}</span>
      </div>
    </div>

    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: {ribbon2_pos}; transform: scale({ribbon2_zoom});" src="{asset_url(ribbon2_img)}" alt="{ribbon2_tag}">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">{ribbon2_tag}</span>
        <span class="caption-text">{ribbon2_caption}</span>
      </div>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // {team_title}</div>
    <div class="page-number">SAYFA {page_num:02d}</div>
  </footer>
</body>
</html>"""

# ==============================================================================
# SAYFA MODÜLLERİ (1 - 28)
# ==============================================================================

def p01():
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<style>
{CSS_MASTER}
.top-header {{ display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2.5px solid #0B1012; padding-bottom: 20px; }}
.brand-block {{ display: flex; align-items: center; gap: 20px; }}
.brand-logo {{ height: 64px; width: auto; object-fit: contain; }}
.univ-title {{ font-family: var(--font-display); font-size: 21px; font-weight: 800; letter-spacing: 0.04em; text-transform: uppercase; color: #0B1012; line-height: 1; }}
.community-subtitle {{ font-family: var(--font-sans); font-size: 13px; font-weight: 500; color: #52606D; }}
.hero-box {{ width: 100%; height: 870px; border-radius: 4px; overflow: hidden; background-color: #0B1012; border: 1px solid var(--c-border); }}
.hero-box img {{ width: 100%; height: 100%; object-fit: cover; object-position: center 65%; transform: scale(1.08); }}
.hero-caption-under {{ display: flex; justify-content: space-between; align-items: center; padding-top: 8px; font-family: var(--font-mono); font-size: 11px; color: var(--c-text-subtle); border-bottom: 1px solid var(--c-border); padding-bottom: 10px; }}
.title-section {{ display: flex; flex-direction: column; gap: 10px; margin-top: 10px; }}
.main-title {{ font-family: var(--font-display); font-size: 76px; font-weight: 900; line-height: 0.95; letter-spacing: -0.035em; color: #0B1012; text-transform: uppercase; }}
.statement {{ font-size: 19.5px; font-weight: 500; line-height: 1.45; color: #334155; max-width: 980px; }}
.bottom-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; border-top: 2.5px solid #0B1012; padding-top: 20px; }}
.stat-num {{ font-family: var(--font-display); font-size: 40px; font-weight: 900; line-height: 1; color: #0B1012; }}
.stat-num span {{ color: var(--c-volt); }}
.stat-label {{ font-family: var(--font-mono); font-size: 11px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #64748B; margin-top: 4px; }}
</style>
</head>
<body class="page-sheet">
  <header class="top-header">
    <div class="brand-block">
      <img class="brand-logo" src="{asset_url('public/logo-matro-siyah.png')}" alt="MATRO Logo">
      <div style="display: flex; flex-direction: column; gap: 4px;">
        <div class="univ-title">Bursa Teknik Üniversitesi</div>
        <div class="community-subtitle">Makine Teknolojileri Robot ve Otomasyon Topluluğu</div>
      </div>
    </div>
    <div style="text-align: right; font-family: var(--font-mono); font-size: 12px; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: var(--c-volt); line-height: 1.6;">
      <div>Mühendislik Portföyü</div>
      <div>2026–2027 // Sayı 01</div>
    </div>
  </header>

  <div class="hero-box">
    <img src="{asset_url('public/media/mavi-vatan-ekipler.jpg')}" alt="TCG Anadolu Mavi Vatan MATRO Ekipleri">
  </div>
  <div class="hero-caption-under">
    <span><strong style="color: var(--c-ink);">SAHA GÖREVİ:</strong> TCG Anadolu uçuş güvertesinde TEKNOFEST Mavi Vatan finalistlerimiz (LODOS, ZEMHERİ, PRUSA)</span>
    <span>İZMİR / 2026</span>
  </div>

  <div class="title-section">
    <div class="eyebrow">Resmî Tanıtım Kitapçığı & Proje Kataloğu</div>
    <h1 class="main-title">Atölyeden Sahaya</h1>
    <p class="statement">
      Deniz tabanından gökyüzüne uzanan otonom sistemler. Bursa Teknik Üniversitesi MATRO çatısı altında 15 Ar-Ge takımıyla tasarlıyor, üretiyor ve yarışıyoruz.
    </p>
  </div>

  <footer class="bottom-grid">
    <div><div class="stat-num">50<span>+</span></div><div class="stat-label">Kayıtlı Derece</div></div>
    <div><div class="stat-num">07</div><div class="stat-label">Ulusal Birincilik</div></div>
    <div><div class="stat-num">08</div><div class="stat-label">2026 Finalisti</div></div>
    <div><div class="stat-num">15</div><div class="stat-label">Aktif Ar-Ge Takımı</div></div>
  </footer>
</body>
</html>"""

def p02():
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<style>
{CSS_MASTER}
.bento-top {{ display: grid; grid-template-columns: 1.4fr 1fr; grid-template-rows: 245px 245px; gap: 16px; margin-bottom: 20px; }}
.hero-cell {{ grid-column: 1 / 2; grid-row: 1 / 3; }}
.editorial-row {{ display: grid; grid-template-columns: 1.25fr 1fr; gap: 28px; margin-bottom: 20px; }}
.bottom-photo-ribbon {{ display: grid; grid-template-columns: 1.15fr 0.85fr; height: 290px; gap: 16px; margin-bottom: 6px; }}
</style>
</head>
<body class="page-sheet">
  <header class="page-header">
    <div class="brand-left">
      <img class="header-logo" src="{asset_url('public/logo-matro-siyah.png')}" alt="MATRO Logo">
      <div class="header-brand-text">
        <div class="univ-name">Bursa Teknik Üniversitesi</div>
        <div class="dept-name">MATRO // Topluluk Kimliği</div>
      </div>
    </div>
    <div class="header-meta-right">
      <div class="section-tag">Kurumsal Tanıtım</div>
      <div class="page-index-badge">02</div>
    </div>
  </header>

  <div class="bento-top">
    <div class="media-unit hero-cell">
      <div class="img-box">
        <img style="object-position: center 25%;" src="{asset_url('public/media/galeri-turkish-technic-atolye.jpg')}" alt="Turkish Technic">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">SANAYİ EĞİTİMİ</span>
        <span class="caption-text">Turkish Technic Uçak Bakım Hangarında Havacılık ve Aviyonik Laboratuvarı İncelemesi</span>
      </div>
    </div>
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center center;" src="{asset_url('public/media/galeri-ashina-atolye.jpg')}" alt="Atölye Montajı">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">ATÖLYE AR-GE</span>
        <span class="caption-text">Öğrenci atölyemizde döner kanat İHA gövde ve aviyonik montajı</span>
      </div>
    </div>
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center 20%;" src="{asset_url('public/media/fuar-standi.jpg')}" alt="Fuar Standı">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">TEKNOLOJİ FUARI</span>
        <span class="caption-text">Ulusal teknoloji zirvelerinde öğrenci araçlarımızın sergilenmesi</span>
      </div>
    </div>
  </div>

  <div class="editorial-title-block">
    <div class="eyebrow">Kurumsal Kültür & Vizyon</div>
    <h1 class="headline">Birlikte Üreten Bir Topluluk</h1>
    <p class="lead-text">
      MATRO, Bursa Teknik Üniversitesi öğrencilerinin mühendislik fikirlerini disiplinlerarası ekip çalışmasıyla sahaya taşıdığı köklü bir Ar-Ge ekosistemidir.
    </p>
  </div>

  <div class="editorial-row">
    <div>
      <p style="font-size: 14.5px; line-height: 1.55; color: #475569;">
        Hava, kara, deniz ve sualtı araçlarından endüstriyel otomasyona uzanan projelerde mekanik, elektronik ve yazılım uzmanlıkları bir araya gelir. Atölye imalatı, test sahaları ve sanayi gezileri bu sürecin ayrılmaz parçalarıdır.
      </p>
      <ul class="bullet-list" style="margin-top: 10px;">
        <li>Çok disiplinli eşzamanlı mühendislik yaklaşımı</li>
        <li>Teorik bilgiyi doğrudan yarışma aracında uygulama</li>
        <li>Kuşaktan kuşağa aktarılan güçlü atölye hafızası</li>
      </ul>
    </div>

    <div class="tech-spec-box">
      <div class="box-title">
        <span>Topluluk Göstergeleri</span>
        <span>2026 SEZONU</span>
      </div>
      <div class="spec-grid">
        <div class="spec-item"><span class="spec-label">Kuruluş</span><span class="spec-value">2013 // 13 Yıl</span></div>
        <div class="spec-item"><span class="spec-label">Aktif Üye</span><span class="spec-value">350+ Mühendis</span></div>
        <div class="spec-item"><span class="spec-label">Takım Sayısı</span><span class="spec-value">15 Ar-Ge Takımı</span></div>
        <div class="spec-item"><span class="spec-label">Saha Testi</span><span class="spec-value">100+ Saat / Yıl</span></div>
      </div>
      <div class="award-pill">
        <span class="trophy-dot"></span>
        <span>Yılda 15+ Ulusal ve Uluslararası Yarışma</span>
      </div>
    </div>
  </div>

  <div class="bottom-photo-ribbon">
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center 30%;" src="{asset_url('public/media/etkinlik-alper-gezeravci.jpg')}" alt="Alper Gezeravcı">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">TEKNİK ZİYARET</span>
        <span class="caption-text">Astronot Alper Gezeravcı atölyemizde PUSULA robotik platformunu incelerken</span>
      </div>
    </div>
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center 60%; transform: scale(1.1);" src="{asset_url('public/media/galeri-hktm-gezisi.jpg')}" alt="HKTM Gezisi">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">SANAYİ GEZİSİ</span>
        <span class="caption-text">HKTM Hareket Kontrol Teknolojileri Merkezi lobi alanında teknik gezi ekibimiz</span>
      </div>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // KURUMSAL</div>
    <div class="page-number">SAYFA 02</div>
  </footer>
</body>
</html>"""

def p03():
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<style>
{CSS_MASTER}
.process-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 20px; }}
.step-unit {{ display: flex; flex-direction: column; background: var(--c-surface); border: 1.5px solid var(--c-border); border-radius: 4px; overflow: hidden; }}
.step-img-box {{ height: 230px; position: relative; background: #0B1012; }}
.step-img-box img {{ width: 100%; height: 100%; object-fit: cover; }}
.step-number {{ position: absolute; top: 8px; left: 8px; background: #0B1012; color: #FFFFFF; font-family: var(--font-mono); font-size: 10px; font-weight: 700; padding: 3px 6px; border-radius: 2px; }}
.step-info {{ padding: 12px; display: flex; flex-direction: column; gap: 4px; }}
.step-title {{ font-family: var(--font-display); font-size: 16px; font-weight: 800; text-transform: uppercase; color: var(--c-ink); }}
.step-desc {{ font-size: 11.5px; line-height: 1.4; color: #64748B; }}
.flow-summary {{ display: grid; grid-template-columns: 1.25fr 1fr; gap: 28px; margin-bottom: 18px; }}
.bottom-ribbon-2 {{ display: grid; grid-template-columns: 1fr 1fr; height: 290px; gap: 16px; margin-bottom: 6px; }}
</style>
</head>
<body class="page-sheet">
  <header class="page-header">
    <div class="brand-left">
      <img class="header-logo" src="{asset_url('public/logo-matro-siyah.png')}" alt="MATRO Logo">
      <div class="dept-name">Bursa Teknik Üniversitesi // MATRO Üretim Döngüsü</div>
    </div>
    <div class="header-meta-right">
      <div class="section-tag">Metodoloji</div>
      <div class="page-index-badge">03</div>
    </div>
  </header>

  <div class="editorial-title-block">
    <div class="eyebrow">Mühendislik Yaşam Döngüsü</div>
    <h1 class="headline">Bir Fikir Nasıl Projeye Dönüşür?</h1>
    <p class="lead-text">
      Bir aracın yarışma parkuruna çıkması, birbiriyle entegre yürüyen disiplinli tasarım, prototipleme, saha testi ve optimizasyon adımlarının sonucudur.
    </p>
  </div>

  <div class="process-grid">
    <div class="step-unit">
      <div class="step-img-box">
        <img style="object-position: center center;" src="{asset_url('public/media/tasarim-ashina-iha.jpg')}" alt="CAD Tasarım">
        <div class="step-number">ADIM 01</div>
      </div>
      <div class="step-info">
        <div class="step-title">1. Modelleme & CAD</div>
        <div class="step-desc">SolidWorks ortamında kafes kanat aerodinamik İHA modellemesi</div>
      </div>
    </div>

    <div class="step-unit">
      <div class="step-img-box">
        <img style="object-position: center center;" src="{asset_url('public/media/galeri-ashina-kompozit-uretim.jpg')}" alt="Kompozit İmalat">
        <div class="step-number">ADIM 02</div>
      </div>
      <div class="step-info">
        <div class="step-title">2. Atölye & İmalat</div>
        <div class="step-desc">Vakum infüzyon yöntemiyle karbon elyaf kanat kalıplama ve kürleme</div>
      </div>
    </div>

    <div class="step-unit">
      <div class="step-img-box">
        <img style="object-position: center 30%;" src="{asset_url('public/media/galeri-iss-auv-havuz.jpg')}" alt="Havuz Testi">
        <div class="step-number">ADIM 03</div>
      </div>
      <div class="step-info">
        <div class="step-title">3. Simülasyon & Test</div>
        <div class="step-desc">PRUSA AUV olimpik havuzda otonom seyrüsefer ve sızdırmazlık testinde</div>
      </div>
    </div>

    <div class="step-unit">
      <div class="step-img-box">
        <img style="object-position: center center;" src="{asset_url('public/media/galeri-prusa-teknofest.jpg')}" alt="Yarışma Sahnesi">
        <div class="step-number">ADIM 04</div>
      </div>
      <div class="step-info">
        <div class="step-title">4. Sahaya Çıkış</div>
        <div class="step-desc">TEKNOFEST sergi alanında hakem heyetine teknik sunum ve sergileme</div>
      </div>
    </div>
  </div>

  <div class="flow-summary">
    <div>
      <p style="font-size: 14.5px; line-height: 1.55; color: #475569;">
        Süreç sadece araç üretmekle bitmez; testlerde görülen her hata tasarım havuzuna geri beslenir. Öğrencilerimiz V-Model ürün geliştirme metodolojisini bizzat tecrübe eder.
      </p>
      <ul class="bullet-list" style="margin-top: 10px;">
        <li>Görev senaryolarına dayalı parametrik tasarım ve CFD analizleri</li>
        <li>Hafifletilmiş kompozit yapı ve fırçasız tahrik optimizasyonu</li>
      </ul>
    </div>

    <div class="tech-spec-box">
      <div class="box-title"><span>Mühendislik Standartları</span><span>BTÜ KALİTE</span></div>
      <div class="spec-grid">
        <div class="spec-item"><span class="spec-label">CAD / Analiz</span><span class="spec-value">SolidWorks, ANSYS</span></div>
        <div class="spec-item"><span class="spec-label">Gömülü Mimari</span><span class="spec-value">STM32, ROS 2, Jetson</span></div>
        <div class="spec-item"><span class="spec-label">İmalat Yöntemi</span><span class="spec-value">Vakum İnfüzyon, CNC</span></div>
        <div class="spec-item"><span class="spec-label">Doğrulama</span><span class="spec-value">MIL / SIL Simülasyonu</span></div>
      </div>
    </div>
  </div>

  <div class="bottom-ribbon-2">
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center center;" src="{asset_url('public/media/tasarim-iss-auv-izometrik.jpg')}" alt="İzometrik CAD">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">TASARIM DOĞRULAMA</span>
        <span class="caption-text">Sualtı robotu 8 itici yerleşimi ve basınç kapsülü CAD modellemesi</span>
      </div>
    </div>
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center 30%;" src="{asset_url('public/media/galeri-matrobot-tarla-test.jpg')}" alt="Arazi Doğrulama">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">SAHA DOĞRULAMA</span>
        <span class="caption-text">MATROBOT otonom tarım aracı açık tarla sürüş ve çapa testinde</span>
      </div>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // SÜREÇ</div>
    <div class="page-number">SAYFA 03</div>
  </footer>
</body>
</html>"""

def p04():
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<style>
{CSS_MASTER}
.role-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px; }}
.role-card {{ background: var(--c-surface); border: 1.5px solid var(--c-border); border-radius: 4px; padding: 20px; display: flex; flex-direction: column; gap: 10px; }}
.lower-bento-2 {{ display: grid; grid-template-columns: 1.2fr 0.8fr; height: 480px; gap: 18px; margin-bottom: 6px; }}
</style>
</head>
<body class="page-sheet">
  <header class="page-header">
    <div class="brand-left">
      <img class="header-logo" src="{asset_url('public/logo-matro-siyah.png')}" alt="MATRO Logo">
      <div class="dept-name">Bursa Teknik Üniversitesi // MATRO Kariyer Haritası</div>
    </div>
    <div class="header-meta-right">
      <div class="section-tag">Rol Dağılımı</div>
      <div class="page-index-badge">04</div>
    </div>
  </header>

  <div class="editorial-title-block">
    <div class="eyebrow">Disiplinlerarası Mühendislik</div>
    <h1 class="headline">Sen Hangi İşi Üstlenmek İstersin?</h1>
    <p class="lead-text">
      Bir projenin sahaya çıkması yalnızca tek bir uzmanlığa bağlı değildir; mekanik, elektronik, yazılım ve kurumsal yönetimin senkronize çalışmasını gerektirir.
    </p>
  </div>

  <div class="role-grid">
    <div class="role-card">
      <div style="font-family: var(--font-mono); font-size: 10px; font-weight: 700; color: var(--c-volt); text-transform: uppercase;">DİSİPLİN 01</div>
      <h3 style="font-family: var(--font-display); font-size: 20px; font-weight: 800; text-transform: uppercase;">Mekanik & İmalat</h3>
      <p style="font-size: 13px; color: #475569; line-height: 1.5;">CAD tasarım, kompozit vakum infüzyon, CNC işleme, aerodinamik/hidrodinamik CFD analizleri ve yapısal mukavemet testleri.</p>
    </div>
    <div class="role-card">
      <div style="font-family: var(--font-mono); font-size: 10px; font-weight: 700; color: var(--c-volt); text-transform: uppercase;">DİSİPLİN 02</div>
      <h3 style="font-family: var(--font-display); font-size: 20px; font-weight: 800; text-transform: uppercase;">Elektronik & Aviyonik</h3>
      <p style="font-size: 13px; color: #475569; line-height: 1.5;">Özel PCB tasarımı, STM32 mikrodenetleyici mimarisi, güç dağıtımı, BMS batarya yönetimi ve sensör arayüzleri.</p>
    </div>
    <div class="role-card">
      <div style="font-family: var(--font-mono); font-size: 10px; font-weight: 700; color: var(--c-volt); text-transform: uppercase;">DİSİPLİN 03</div>
      <h3 style="font-family: var(--font-display); font-size: 20px; font-weight: 800; text-transform: uppercase;">Otonom Yazılım</h3>
      <p style="font-size: 13px; color: #475569; line-height: 1.5;">ROS 2 mimarisi, SLAM haritalama, görüntü işleme (YOLO), derin öğrenme, seyrüsefer ve yer kontrol istasyonu yazılımları.</p>
    </div>
  </div>

  <div class="lower-bento-2">
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center 30%;" src="{asset_url('public/media/webmedya-sanayide-dijital-31.jpg')}" alt="Atölye Ekip Çalışması">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">EŞZAMANLI MÜHENDİSLİK</span>
        <span class="caption-text">Mekanik ve elektronik ekipleri araç şasisi üzerinde birlikte çalışırken</span>
      </div>
    </div>
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center center;" src="{asset_url('public/media/galeri-turkish-technic-sinif.jpg')}" alt="Teknik Eğitim">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">EĞİTİM & AKTARIM</span>
        <span class="caption-text">Kıdemli üyeler tarafından yeni katılan üyelere teknik çizim ve yazılım seminerleri</span>
      </div>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // ROLLER</div>
    <div class="page-number">SAYFA 04</div>
  </footer>
</body>
</html>"""

def p05():
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<style>
{CSS_MASTER}
.cat-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-bottom: 24px; }}
.cat-card {{ background: var(--c-surface); border: 1.5px solid var(--c-border); border-radius: 4px; padding: 24px; display: flex; flex-direction: column; gap: 12px; }}
.lower-bento-full {{ width: 100%; height: 430px; margin-bottom: 6px; }}
</style>
</head>
<body class="page-sheet">
  <header class="page-header">
    <div class="brand-left">
      <img class="header-logo" src="{asset_url('public/logo-matro-siyah.png')}" alt="MATRO Logo">
      <div class="dept-name">Bursa Teknik Üniversitesi // MATRO Portföy Mimarisi</div>
    </div>
    <div class="header-meta-right">
      <div class="section-tag">Faaliyet Alanları</div>
      <div class="page-index-badge">05</div>
    </div>
  </header>

  <div class="editorial-title-block">
    <div class="eyebrow">Ar-Ge Ekosistemi</div>
    <h1 class="headline">Çalışma Alanlarımız</h1>
    <p class="lead-text">
      MATRO bünyesinde geliştirilen otonom araçlar ve araştırma takımları 4 temel mühendislik kümesinde toplanmıştır.
    </p>
  </div>

  <div class="cat-grid">
    <div class="cat-card">
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--c-volt);">KÜME 01 // HAVACILIK & UZAY</div>
      <h3 style="font-family: var(--font-display); font-size: 26px; font-weight: 800; text-transform: uppercase;">Hava Sistemleri</h3>
      <div style="font-family: var(--font-mono); font-size: 12px; font-weight: 700; background: #E2E8F0; padding: 6px 10px; border-radius: 3px;">ASHİNA · MATRİS · BÜRKÜT · GÖKSAV</div>
      <p style="font-size: 13.5px; color: #475569; line-height: 1.5;">Sabit kanat, döner kanat, otonom sürü İHA algoritmaları, uçan araba kentsel hava hareketliliği ve hava savunma hedef takip sistemleri.</p>
    </div>

    <div class="cat-card">
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--c-volt);">KÜME 02 // DENİZCİLİK & SUALTI</div>
      <h3 style="font-family: var(--font-display); font-size: 26px; font-weight: 800; text-transform: uppercase;">Deniz & Sualtı</h3>
      <div style="font-family: var(--font-mono); font-size: 12px; font-weight: 700; background: #E2E8F0; padding: 6px 10px; border-radius: 3px;">LODOS · PRUSA · ZEMHERİ · SARA</div>
      <p style="font-size: 13.5px; color: #475569; line-height: 1.5;">Otonom insansız su üstü devriye araçları (USV), 50 m derinlik dayanımlı AUV sualtı robotları ve sualtı roket fırlatma teknolojileri.</p>
    </div>

    <div class="cat-card">
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--c-volt);">KÜME 03 // KARA & SANAYİ OTONOMİSİ</div>
      <h3 style="font-family: var(--font-display); font-size: 26px; font-weight: 800; text-transform: uppercase;">Kara & Mobil Robotik</h3>
      <div style="font-family: var(--font-mono); font-size: 12px; font-weight: 700; background: #E2E8F0; padding: 6px 10px; border-radius: 3px;">MATROVER · LUNA · PUSULA · MATROBOT</div>
      <p style="font-size: 13.5px; color: #475569; line-height: 1.5;">Zorlu arazi şartlarında gezegen keşif rover'ları, otonom taktik kara taşıtları ve fabrika içi malzeme aktaran endüstriyel AMR robotları.</p>
    </div>

    <div class="cat-card">
      <div style="font-family: var(--font-mono); font-size: 11px; font-weight: 700; color: var(--c-volt);">KÜME 04 // İLERİ TEKNOLOJİ & SAĞLIK</div>
      <h3 style="font-family: var(--font-display); font-size: 26px; font-weight: 800; text-transform: uppercase;">Aviyonik, RF & Biyoteknoloji</h3>
      <div style="font-family: var(--font-mono); font-size: 12px; font-weight: 700; background: #E2E8F0; padding: 6px 10px; border-radius: 3px;">ÇAĞRI · ALHAZEN · GİRİŞİMCİLİK</div>
      <p style="font-size: 13.5px; color: #475569; line-height: 1.5;">Yazılım tanımlı telsiz (SDR) kablosuz veri bağları, optik tanı spektrometreleri ve yarışma projelerinin ticarileşme süreçleri.</p>
    </div>
  </div>

  <div class="media-unit lower-bento-full">
    <div class="img-box">
      <img style="object-position: center 40%;" src="{asset_url('public/media/mavi-vatan-ekipler.jpg')}" alt="MATRO Takımları">
    </div>
    <div class="caption-bar">
      <span class="caption-tag">MÜHENDİSLİK BİRLİKTELİĞİ</span>
      <span class="caption-text">Hava, deniz, kara ve elektronik takımlarımızın ulusal yarışma finallerindeki ortak temsil gücü</span>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // ALANLAR</div>
    <div class="page-number">SAYFA 05</div>
  </footer>
</body>
</html>"""

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
{CSS_MASTER}
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
{CSS_MASTER}
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
{CSS_MASTER}
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
{CSS_MASTER}
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
{CSS_MASTER}
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
{CSS_MASTER}
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
{CSS_MASTER}
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



def p06():
    # ASHİNA (Havacılık Mizanpajı: Panoramik Hero + 3 Kolon + Pist Uçuşu)
    return render_page_06()

def p07():
    # MATROVER & LUNA (Kara Sistemleri Mizanpajı: Sol Çift Hero, Sağ Veri, Alt Tarla Testi)
    return render_page_07()

def p08():
    # LODOS & İDA (Mavi Vatan İskele Hero + Atölye İmalat + Haluk Bayraktar Brifingi)
    return render_page_08()

def p09():
    # İSS & PRUSA (Havuz Testi Hero + İzometrik CAD + Mekanik Şasi + Stand)
    return render_page_09()

def p10():
    # ZEMHERİ & SARA (Finalist Ekip + Atış Kapsülü + Atölye Montajı)
    return render_page_10()

def p11():
    # MATRİS (Sürü İHA Filosu + Dron Ekibi + Uçuş Sahası)
    return generate_team_page_v12(
        page_num=11,
        page_tag="Havacılık & Yazılım Grubu",
        team_title="MATRİS",
        team_category="Otonom Sürü İHA Algoritmaları & Dağıtık Görev Paylaşımı",
        team_logo_path=None,
        hero_img="public/media/takim-matris-2026.jpg",
        hero_pos="center 60%",
        hero_zoom="1.15",
        hero_tag="DRON FİLOSU",
        hero_caption="Öğrenci atölyemizde kalibre edilen MATRİS sürü quadcopter İHA filosu",
        side1_img="public/media/takim-matris-iha.jpg",
        side1_pos="center center",
        side1_zoom="1.0",
        side1_tag="GÖREV YAZILIMI",
        side1_caption="Sürü İHA merkezi yer kontrol istasyonu ve rota planlama arayüzü",
        side2_img="public/media/galeri-matris-dron-filo.jpg",
        side2_pos="center 20%",
        side2_zoom="1.05",
        side2_tag="TEKNOFEST EKİBİ",
        side2_caption="MATRİS sürü İHA geliştirme ekibimiz TEKNOFEST yarışma alanında",
        lead_p="birden fazla insansız hava aracının merkezi veya dağıtık haberleşme ile ortak bir görevi (alan tarama, formasyon koruma, hedef kuşatma) otonom icra etmesini sağlayan Ar-Ge ekibimizdir.",
        body_p="ROS 2 ve Gazebo tabanlı simülasyonlarda doğrulanan sürü algoritmaları, atölyemizde üretilen özdeş quadcopter filoları üzerine yüklenerek açık hava test sahasında doğrulanır.",
        bullets=[
            "Merkezi ve dağıtık sürü haberleşme protokolleri",
            "Yapay potansiyel alan ve sürü formasyon algoritmaları",
            "Görev anında bir İHA kopsa dahi görevi sürdüren dinamik yapı"
        ],
        award_text="TEKNOFEST 2026 SÜRÜ İHA FİNALİSTİ",
        spec_model="MATRİS SÜRÜ DRON",
        specs=[
            ("Dron Sayısı", "5+ Eşzamanlı Otonom İHA"),
            ("Gövde Çapı", "450 mm Karbon-Polimer Şasi"),
            ("Uçuş Kontrolörü", "Pixhawk 4 / PX4 Autopilot"),
            ("Haberleşme Ağı", "Mesh Wi-Fi / UWB Konumlandırma"),
            ("Hesaplama", "Raspberry Pi 4 Companion"),
            ("Havada Kalış", "18 Dakika Görev Süresi")
        ],
        ribbon1_img="public/media/galeri-matris-test-alani.jpg",
        ribbon1_pos="center 25%",
        ribbon1_zoom="1.05",
        ribbon1_tag="UÇUŞ TEST SAHASI",
        ribbon1_caption="MATRİS sürü İHA ekibimiz sahada otonom filo uçuş denemesi öncesinde",
        ribbon2_img="public/media/galeri-matris-saha.jpg",
        ribbon2_pos="center center",
        ribbon2_zoom="1.0",
        ribbon2_tag="SAHA İSTASYONU",
        ribbon2_caption="Uçuş pistinde telemetri izleme ve otonom kalkış testleri"
    )

def p12():
    # PUSULA & ANDROMEDA (Gerçek TEKNOFEST ve Atölye Montajı)
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<style>
{CSS_MASTER}
.pusula-top-split {{ display: grid; grid-template-columns: 1.55fr 1fr; grid-template-rows: 250px 250px; gap: 16px; margin-bottom: 18px; }}
.pusula-hero {{ grid-column: 1 / 2; grid-row: 1 / 3; }}
.middle-split {{ display: grid; grid-template-columns: 1.25fr 1fr; gap: 24px; margin-bottom: 18px; }}
.lower-duo {{ display: grid; grid-template-columns: 1.15fr 0.85fr; height: 280px; gap: 14px; margin-bottom: 6px; }}
</style>
</head>
<body class="page-sheet">
  <header class="page-header">
    <div class="brand-left">
      <img class="header-logo" src="{asset_url('public/logo-matro-siyah.png')}" alt="MATRO Logo">
      <div class="dept-name">Bursa Teknik Üniversitesi // MATRO Sanayi Robotik</div>
    </div>
    <div class="header-meta-right">
      <div class="section-tag">Sanayi & AMR Sistemleri</div>
      <div class="page-index-badge">12</div>
    </div>
  </header>

  <div class="team-header-row" style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 14px;">
    <div>
      <div class="eyebrow">Endüstriyel Otonomi Takımı</div>
      <h1 class="headline" style="font-size: 46px; margin: 0;">PUSULA & ANDROMEDA</h1>
      <div style="font-size: 14px; font-weight: 600; color: var(--c-text-muted); margin-top: 3px;">
        Sanayide Dijital Teknolojiler, Otonom Fabrika İçi Taşıma & AGV/AMR Sistemleri
      </div>
    </div>
    <div class="award-pill">
      <span class="trophy-dot"></span>
      <span>TEKNOFEST 2026 FİNALİSTİ</span>
    </div>
  </div>

  <div class="pusula-top-split">
    <div class="media-unit pusula-hero">
      <div class="img-box">
        <img style="object-position: center 25%;" src="{asset_url('public/media/takim-sanayide-dijital.jpg')}" alt="PUSULA Takımı ve Robotu">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">YARIŞMA SAHASI</span>
        <span class="caption-text">TEKNOFEST Sanayide Dijital Teknolojiler finalist ekibimiz ve PUSULA otonom taşıma robotumuz</span>
      </div>
    </div>

    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center 35%;" src="{asset_url('public/media/galeri-pusula-atolye.jpg')}" alt="PUSULA Atölye">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">ATÖLYE MONTAJI</span>
        <span class="caption-text">Özdemir Bayraktar Atölyesinde PUSULA mekanik taşıyıcı şasi montajı</span>
      </div>
    </div>

    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center center;" src="{asset_url('public/media/galeri-sanayide-dijital-arena.jpg')}" alt="Yarışma Parkuru">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">OTONOM PARKUR</span>
        <span class="caption-text">Yarışma arenasında otonom palet aktarımı ve engel aşma parkuru</span>
      </div>
    </div>
  </div>

  <div class="middle-split">
    <div>
      <p style="font-size: 14px; line-height: 1.52; color: #475569;">
        <strong>PUSULA</strong>, modern endüstriyel tesislerde fabrika içi malzeme taşıma, palet aktarımı ve otonom hat besleme görevlerini icra eden otonom mobil robot (AMR) projemizdir.
      </p>
      <p style="font-size: 14px; line-height: 1.52; color: #475569; margin-top: 6px;">
        Lazer tabanlı 2D/3D LiDAR sensörleri ve endüstriyel güvenlik tarayıcılarıyla donatılan araç, insanlarla aynı koridorlarda güvenle çalışır ve dinamik engellerden anında kaçınır.
      </p>
      <ul class="bullet-list" style="margin-top: 10px;">
        <li>LiDAR SLAM haritalama ile manyetik şeritsiz serbest seyrüsefer</li>
        <li>150 kg faydalı yük taşıma kapasitesi ve otomatik şarj kenetlenmesi</li>
      </ul>
    </div>

    <div class="tech-spec-box">
      <div class="box-title">
        <span>Teknik Spesifikasyonlar</span>
        <span>PUSULA AMR V2</span>
      </div>
      <div class="spec-grid">
        <div class="spec-item"><span class="spec-label">Taşıma Kapasitesi</span><span class="spec-value">150 kg Faydalı Yük</span></div>
        <div class="spec-item"><span class="spec-label">Seyrüsefer</span><span class="spec-value">Doğal Navigasyon (LiDAR)</span></div>
        <div class="spec-item"><span class="spec-label">Emniyet Sistemi</span><span class="spec-value">Çift Lazer Alan Tarayıcısı</span></div>
        <div class="spec-item"><span class="spec-label">Hız & Eğim</span><span class="spec-value">1.5 m/s Hız // %8 Eğim</span></div>
      </div>
    </div>
  </div>

  <div class="lower-duo">
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center 30%;" src="{asset_url('public/media/etkinlik-alper-gezeravci.jpg')}" alt="Alper Gezeravcı PUSULA">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">TEKNİK İNCELEME</span>
        <span class="caption-text">Astronot Alper Gezeravcı atölyemizde PUSULA robotunun kontrol sistemlerini incelerken</span>
      </div>
    </div>
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center 20%;" src="{asset_url('public/media/webmedya-sanayide-dijital-31.jpg')}" alt="Elektronik Test">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">DONANIM ENTEGRASYONU</span>
        <span class="caption-text">Robot üzerinde motor sürücü kablolaması ve güvenlik sensörü kalibrasyonu</span>
      </div>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // PUSULA & ANDROMEDA</div>
    <div class="page-number">SAYFA 12</div>
  </footer>
</body>
</html>"""

def p13():
    # GÖKSAV & ASHİNA-H (MERGEN Taret Prototipi + Lazer Takip + Savunma Mühendisleri)
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<style>
{CSS_MASTER}
.goksav-hero-box {{ width: 100%; height: 500px; margin-bottom: 18px; }}
.middle-split {{ display: grid; grid-template-columns: 1.25fr 1fr; gap: 24px; margin-bottom: 18px; }}
.lower-ribbon-3 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; height: 270px; gap: 14px; margin-bottom: 6px; }}
</style>
</head>
<body class="page-sheet">
  <header class="page-header">
    <div class="brand-left">
      <img class="header-logo" src="{asset_url('public/logo-matro-siyah.png')}" alt="MATRO Logo">
      <div class="dept-name">Bursa Teknik Üniversitesi // MATRO Hava Savunma</div>
    </div>
    <div class="header-meta-right">
      <div class="section-tag">Hava Savunma Grubu</div>
      <div class="page-index-badge">13</div>
    </div>
  </header>

  <div class="team-header-row" style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 14px;">
    <div>
      <div class="eyebrow">Hava Savunma & Döner Kanat Teknolojileri</div>
      <h1 class="headline" style="font-size: 46px; margin: 0;">GÖKSAV & ASHİNA-H</h1>
      <div style="font-size: 14px; font-weight: 600; color: var(--c-text-muted); margin-top: 3px;">
        Otonom Hava Savunma Taretleri, İHA Önleme Sistemleri & Helikopter Platformları
      </div>
    </div>
    <div class="award-pill">
      <span class="trophy-dot"></span>
      <span>HAVA SAVUNMA AR-GE SİSTEMİ</span>
    </div>
  </div>

  <div class="media-unit goksav-hero-box">
    <div class="img-box">
      <img style="object-position: center 30%;" src="{asset_url('public/media/galeri-mergen-hss.jpg')}" alt="MERGEN Prototip">
    </div>
    <div class="caption-bar">
      <span class="caption-tag">ATÖLYE PROTOTİPİ</span>
      <span class="caption-text">MERGEN 2 eksenli elektro-optik hedef takip tareti, Intel RealSense derinlik kamerası ve pan-tilt mekanizması</span>
    </div>
  </div>

  <div class="middle-split">
    <div>
      <p style="font-size: 14px; line-height: 1.52; color: #475569;">
        <strong>GÖKSAV</strong> ve <strong>MERGEN</strong>, kritik üs bölgelerini mini/mikro İHA tehditlerine karşı korumak amacıyla geliştirilen yapay zekâ güdümlü otonom hava savunma tareti projemizdir.
      </p>
      <p style="font-size: 14px; line-height: 1.52; color: #475569; margin-top: 6px;">
        Derin öğrenme tabanlı nesne tespit modelleri, stereo kameralardan gelen görüntüleri işleyerek yaklaşan hava hedeflerini 3 boyutta kilitler ve pan-tilt taretini mikro saniyeler içinde hedefe doğrultur.
      </p>
      <ul class="bullet-list" style="margin-top: 8px;">
        <li>Stereo optik ve yapay zekâ ile yüksek hızlı hedef tespiti ve takibi</li>
        <li>Fırçasız servo aktüatörlerle 360° pan ve -20°/+85° tilt kabiliyeti</li>
      </ul>
    </div>

    <div class="tech-spec-box">
      <div class="box-title"><span>Teknik Spesifikasyonlar</span><span>MERGEN HSS V1</span></div>
      <div class="spec-grid">
        <div class="spec-item"><span class="spec-label">Sensör Mimarisi</span><span class="spec-value">Intel RealSense D435i</span></div>
        <div class="spec-item"><span class="spec-label">Dönüş Açıları</span><span class="spec-value">Pan: 360° // Tilt: -20° / +85°</span></div>
        <div class="spec-item"><span class="spec-label">Açısal Hız</span><span class="spec-value">120°/saniye İvme</span></div>
        <div class="spec-item"><span class="spec-label">Hedefleme</span><span class="spec-value">YOLOv8 + Kalman Filtresi</span></div>
      </div>
    </div>
  </div>

  <div class="lower-ribbon-3">
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center center;" src="{asset_url('public/media/goksav-test.jpg')}" alt="Saha Testi">
      </div>
      <div class="caption-bar"><span class="caption-tag">OPTİK TAKİP</span><span class="caption-text">Lazer ve optik takip testi</span></div>
    </div>
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center center;" src="{asset_url('public/media/takim-goksav.jpg')}" alt="GÖKSAV Ekibi">
      </div>
      <div class="caption-bar"><span class="caption-tag">SAVUNMA EKİBİ</span><span class="caption-text">GÖKSAV mühendislerimiz</span></div>
    </div>
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center center;" src="{asset_url('public/media/webmedya-suru-iha-35.jpg')}" alt="Gözetleme">
      </div>
      <div class="caption-bar"><span class="caption-tag">AVİYONİK</span><span class="caption-text">Hedef tespit algoritmaları</span></div>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // GÖKSAV HSS</div>
    <div class="page-number">SAYFA 13</div>
  </footer>
</body>
</html>"""

def p14():
    # BÜRKÜT (CEZERİ Hero + Selçuk Bayraktar Ödül Takdimi)
    return render_page_14()

def p15():
    # ÇAĞRI (Gerçek Finalist Ekip Kadrajı + Advance-Up 3.lük)
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<style>
{CSS_MASTER}
.cagri-grid {{ display: grid; grid-template-columns: 1.45fr 1.55fr; gap: 20px; height: 520px; margin-bottom: 18px; }}
.middle-split {{ display: grid; grid-template-columns: 1.25fr 1fr; gap: 24px; margin-bottom: 18px; }}
.lower-ribbon {{ display: grid; grid-template-columns: 1fr 1fr; height: 280px; gap: 14px; margin-bottom: 6px; }}
</style>
</head>
<body class="page-sheet">
  <header class="page-header">
    <div class="brand-left">
      <img class="header-logo" src="{asset_url('public/logo-matro-siyah.png')}" alt="MATRO Logo">
      <div class="dept-name">Bursa Teknik Üniversitesi // MATRO Haberleşme & Aviyonik</div>
    </div>
    <div class="header-meta-right">
      <div class="section-tag">RF & Telsiz Sistemleri</div>
      <div class="page-index-badge">15</div>
    </div>
  </header>

  <div class="team-header-row" style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 14px;">
    <div>
      <div class="eyebrow">Haberleşme ve RF Teknolojileri Takımı</div>
      <h1 class="headline" style="font-size: 46px; margin: 0;">ÇAĞRI</h1>
      <div style="font-size: 14px; font-weight: 600; color: var(--c-text-muted); margin-top: 3px;">
        Kablosuz Haberleşme Sistemleri, Yazılım Tanımlı Telsiz (SDR) & RF Güvenliği
      </div>
    </div>
    <div class="award-pill">
      <span class="trophy-dot"></span>
      <span>KABLOSUZ HABERLEŞME FİNALİSTİ</span>
    </div>
  </div>

  <div class="cagri-grid">
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center 72%; transform: scale(1.36);" src="{asset_url('public/media/webmedya-burkut-46.jpg')}" alt="ÇAĞRI Ekibi">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">FİNALİST EKİP</span>
        <span class="caption-text">TEKNOFEST Kablosuz Haberleşme Yarışması sahnesinde finalist ÇAĞRI ekibimiz</span>
      </div>
    </div>

    <div style="display: flex; flex-direction: column; gap: 14px; height: 100%;">
      <div class="media-unit" style="flex: 1;">
        <div class="img-box">
          <img style="object-position: center 30%;" src="{asset_url('public/media/galeri-advance-up-syntax.jpg')}" alt="Advance-Up 3.lük">
        </div>
        <div class="caption-bar">
          <span class="caption-tag">HACKATHON DERECESİ</span>
          <span class="caption-text">Advance-Up Hackathon yarışmasında Türkiye 3.lüğü ödülümüz</span>
        </div>
      </div>
      <div class="media-unit" style="flex: 1;">
        <div class="img-box">
          <img style="object-position: center center;" src="{asset_url('public/media/webmedya-sanayide-dijital-26.jpg')}" alt="RF Donanımı">
        </div>
        <div class="caption-bar">
          <span class="caption-tag">RF DONANIMI</span>
          <span class="caption-text">Özel tasarım yönlü mikroşerit anten ve sinyal güçlendirici devresi</span>
        </div>
      </div>
    </div>
  </div>

  <div class="middle-split">
    <div>
      <p style="font-size: 14px; line-height: 1.52; color: #475569;">
        <strong>ÇAĞRI</strong>, elektronik harp ve yoğun parazitli ortamlarda güvenli, kriptolu ve kesintisiz kablosuz veri aktarımı sağlayan haberleşme altyapıları geliştiren takımımızdır.
      </p>
      <p style="font-size: 14px; line-height: 1.52; color: #475569; margin-top: 6px;">
        Yazılım tanımlı radyo (SDR) kartları ve FPGA donanımları üzerinde koşan özel modülasyon teknikleri sayesinde araçlarımızın telemetri bağı kesilmeden sürdürülür.
      </p>
      <ul class="bullet-list" style="margin-top: 8px;">
        <li>Frekans atlamalı yayılı spektrum (FHSS) ile karıştırmaya dirençli RF bağı</li>
        <li>FPGA tabanlı yüksek hızlı sinyal işleme ve sayısal filtreleme</li>
      </ul>
    </div>

    <div class="tech-spec-box">
      <div class="box-title">
        <span>Teknik Spesifikasyonlar</span>
        <span>ÇAĞRI SDR PROTOKOLÜ</span>
      </div>
      <div class="spec-grid">
        <div class="spec-item"><span class="spec-label">Çalışma Frekansı</span><span class="spec-value">433 MHz, 868 MHz, 2.4 GHz</span></div>
        <div class="spec-item"><span class="spec-label">Donanım Tabanı</span><span class="spec-value">HackRF One, BladeRF, LimeSDR</span></div>
        <div class="spec-item"><span class="spec-label">Modülasyon</span><span class="spec-value">QPSK, OFDM, LoRa, FHSS</span></div>
        <div class="spec-item"><span class="spec-label">Şifreleme</span><span class="spec-value">AES-256 Donanımsal Kriptolama</span></div>
      </div>
    </div>
  </div>

  <div class="lower-ribbon">
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center center;" src="{asset_url('public/media/galeri-teknopark-ankara.jpg')}" alt="Teknokent Testi">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">ALTYAPI TESTİ</span>
        <span class="caption-text">Teknokent sahasında uzun menzilli RF veri bağı ve paket kaybı ölçümleri</span>
      </div>
    </div>
    <div class="media-unit">
      <div class="img-box">
        <img style="object-position: center center;" src="{asset_url('public/media/galeri-istanbul-fuar-merkezi.jpg')}" alt="Haberleşme Standı">
      </div>
      <div class="caption-bar">
        <span class="caption-tag">TEKNOLOJİ SAHNESİ</span>
        <span class="caption-text">Uluslararası fuar merkezinde kablosuz telemetri altyapımızın tanıtımı</span>
      </div>
    </div>
  </div>

  <footer class="page-footer">
    <div class="footer-site">btumatro.com // ÇAĞRI RF</div>
    <div class="page-number">SAYFA 15</div>
  </footer>
</body>
</html>"""

def p16():
    # ALHAZEN (Biyomedikal Laboratuvarı ve Analiz Cihazları)
    return generate_team_page_v12(
        page_num=16,
        page_tag="Biyoteknoloji & Sağlık Grubu",
        team_title="ALHAZEN",
        team_category="Biyomedikal Cihaz Tasarımı, Optik Spektrometre & Sağlıkta Yapay Zekâ",
        team_logo_path=None,
        hero_img="public/media/galeri-alhazen-laboratuvar.jpg",
        hero_pos="center 30%",
        hero_zoom="1.0",
        hero_tag="LABORATUVAR AR-GE",
        hero_caption="BTÜ Biyomühendislik laboratuvarında optik sensör ve biyokimyasal analiz çalışmaları",
        side1_img="public/media/galeri-alhazen-analiz.jpg",
        side1_pos="center center",
        side1_zoom="1.0",
        side1_tag="OPTİK ANALİZ",
        side1_caption="Taşınabilir spektrofotometre düzeneği ve mikroakışkan hücre tahlili",
        side2_img="public/media/galeri-alhazen-ekipman.jpg",
        side2_pos="center center",
        side2_zoom="1.0",
        side2_tag="ELEKTRONİK DİZGİ",
        side2_caption="Hassas analog ön uç (AFE) amplifikatör ve biyo-potansiyel devresi",
        lead_p="optik prensipler ve yapay zekâ destekli görüntü analizi ile kan ve doku örneklerinde hızlı tanı koyan taşınabilir biyomedikal cihazlar geliştiren ekibimizdir.",
        body_p="Geliştirilen mikrosistemler, sahada laboratuvar ortamı gerektirmeden spektrometrik ölçümler yapar ve sonuçları hekime anında aktarır.",
        bullets=[
            "Mikroakışkan çip entegrasyonuyla hızlı numune hazırlığı ve analizi",
            "Hücresel anomalileri sınıflandıran yapay sinir ağı mimarisi",
            "Düşük gürültülü analog sinyal işleme ve optik filtreleme"
        ],
        award_text="BİYOMEDİKAL AR-GE SİSTEMİ",
        spec_model="ALHAZEN OPTİK TANI",
        specs=[
            ("Dalga Boyu", "340 nm – 850 nm"),
            ("Çözünürlük", "12-bit Hassas Dedektör"),
            ("Yapay Zekâ", "ResNet-18 Sınıflandırma"),
            ("Güç Tüketimi", "Taşınabilir Düşük Güç")
        ],
        ribbon1_img="public/media/takim-alhazen.jpg",
        ribbon1_pos="center center",
        ribbon1_zoom="1.0",
        ribbon1_tag="BİYOMÜHENDİSLİK EKİBİ",
        ribbon1_caption="ALHAZEN biyomedikal ve optik analiz geliştirme ekibimiz laboratuvarda",
        ribbon2_img="public/media/webmedya-cevre-enerji-9.jpg",
        ribbon2_pos="center center",
        ribbon2_zoom="1.0",
        ribbon2_tag="KALİBRASYON",
        ribbon2_caption="Hassas optik sensörlerin standart solüsyonlarla kalibrasyon süreci"
    )

def p17():
    # ASHİNA İNOVASYON (Gerçek Hibrit VTOL Prototipi)
    return generate_team_page_v12(
        page_num=17,
        page_tag="İnovatif Havacılık Grubu",
        team_title="ASHİNA İNOVASYON",
        team_category="Hibrit Dikey Kalkışlı İHA (VTOL), Uzun Menzilli Kargo & Otonom Sivil Görevler",
        team_logo_path="public/media/logolar/takimlar/ashina.png",
        hero_img="public/media/galeri-ashina-uretim.jpg",
        hero_pos="center center",
        hero_zoom="1.0",
        hero_tag="ATÖLYE PROTOTİPİ",
        hero_caption="Özdemir Bayraktar Atölyesinde üretilen 4+1 motorlu hibrit VTOL İHA mekanik montajı",
        side1_img="public/media/tasarim-ashina-iha.jpg",
        side1_pos="center center",
        side1_zoom="1.0",
        side1_tag="AERODİNAMİK CAD",
        side1_caption="Yüksek taşıma kapasiteli taşıyıcı yüzey ve gövde optimizasyonu",
        side2_img="public/media/galeri-ashina-kompozit-uretim.jpg",
        side2_pos="center center",
        side2_zoom="1.0",
        side2_tag="KOMPOZİT İMALAT",
        side2_caption="Vakum infüzyon yöntemiyle üretilen hafif gövde panelleri",
        lead_p="pist ihtiyacı olmadan dar alanlardan dikey havalanıp havada sabit kanatlı uçak verimliliğinde seyreden hibrit VTOL hava araçları geliştiren Ar-Ge ekibimizdir.",
        body_p="4 adet dikey kaldırma motoru ile kalkış ve iniş yapan araç, seyir irtifasına ulaştığında arka itici motorunu devreye alarak 120 km menzile kadar otonom kargo ve haritalama görevlerini yerine getirir.",
        bullets=[
            "Pistsiz kalkış ve inişle her türlü zorlu coğrafyada operasyon kabiliyeti",
            "Hafif karbon fiber kompozit gövde ile 2.5 kg faydalı yük taşıma",
            "Arıza anında motor yedeğiyle güvenli dikey acil iniş protokolü"
        ],
        award_text="İNOVATİF VTOL AR-GE",
        spec_model="VTOL HİBRİT V1",
        specs=[
            ("Kanat Açıklığı", "2200 mm Sandviç"),
            ("İtki Düzeni", "4x Lift + 1x Pusher"),
            ("Faydalı Yük", "2.5 kg Kargo Bölmesi"),
            ("Menzil", "60 km // 75 Dakika")
        ],
        ribbon1_img="public/media/galeri-ashina-saha.jpg",
        ribbon1_pos="center 25%",
        ribbon1_zoom="1.0",
        ribbon1_tag="UÇUŞ DOĞRULAMA",
        ribbon1_caption="Açık hava pistinde otonom mod geçişi (hover to cruise) telemetri takibi",
        ribbon2_img="public/media/galeri-ashina-teknofest-grup.jpg",
        ribbon2_pos="center 40%",
        ribbon2_zoom="1.05",
        ribbon2_tag="HAVACILIK EKİBİ",
        ribbon2_caption="TÜBİTAK yarışma pistinde ASHİNA havacılık ekibimiz"
    )

def p18():
    # FİKİRDEN GİRİŞİME (Şirketleşme & Girişimcilik 1.liği)
    return render_page_18()

def p19():
    return generate_page_19()

def p20():
    return generate_page_20()

def p21():
    return generate_page_21()

def p22():
    return generate_page_22()

def p23():
    return generate_page_23()

def p24():
    return generate_page_24()

def p25():
    return generate_page_25()

def p26():
    return generate_page_26()

def p27():
    return generate_page_27()

def p28():
    return generate_page_28()

# ==============================================================================
# TÜM 28 SAYFA KAYITLARI
# ==============================================================================
PAGES_REGISTRY = {
    1: ("sayfa-01-kapak", p01),
    2: ("sayfa-02-topluluk", p02),
    3: ("sayfa-03-surec", p03),
    4: ("sayfa-04-roller", p04),
    5: ("sayfa-05-alanlar", p05),
    6: ("sayfa-06-ashina", p06),
    7: ("sayfa-07-matrover-luna", p07),
    8: ("sayfa-08-lodos-ida", p08),
    9: ("sayfa-09-prusa-iss", p09),
    10: ("sayfa-10-zemheri-sara", p10),
    11: ("sayfa-11-matris", p11),
    12: ("sayfa-12-pusula", p12),
    13: ("sayfa-13-goksav", p13),
    14: ("sayfa-14-burkut", p14),
    15: ("sayfa-15-cagri", p15),
    16: ("sayfa-16-alhazen", p16),
    17: ("sayfa-17-ashina-inovasyon", p17),
    18: ("sayfa-18-girisimcilik", p18),
    19: ("sayfa-19-basarilar", p19),
    20: ("sayfa-20-sezon", p20),
    21: ("sayfa-21-egitim", p21),
    22: ("sayfa-22-geziler", p22),
    23: ("sayfa-23-sosyal", p23),
    24: ("sayfa-24-organizasyon", p24),
    25: ("sayfa-25-sponsorlar", p25),
    26: ("sayfa-26-paketler", p26),
    27: ("sayfa-27-katilim", p27),
    28: ("sayfa-28-kapanis", p28),
}

def render_single(num):
    name, fn = PAGES_REGISTRY[num]
    html_content = fn()
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
    print(f"✓ Sayfa {num:02d} ({name}) -> {png_path} ({size_kb:.1f} KB)")

def main():
    print("=== MATRO V12 — 28 Sayfalık Portföy Derleme Motoru Başlatılıyor ===")
    for num in sorted(PAGES_REGISTRY.keys()):
        render_single(num)
    print("=== 28 SAYFANIN TÜMÜ HATASIZ VE ÖZGÜN MİZANPAJLA DERLENDİ! ===")

if __name__ == '__main__':
    main()
