#!/usr/bin/env python3
"""İlk editoryal taslağın üretim kaydı. Mevcut taslağın üzerine yazmaz.
Sonraki düzeltmeler docs/kitapcik-hazirlik/yayin-plani.json içinde yapılır.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/kitapcik-hazirlik'
OUT.mkdir(parents=True, exist_ok=True)
TARGET = OUT / 'yayin-plani.json'
if TARGET.exists():
    raise SystemExit('Taslak mevcut. Üzerine yazılmadı; JSON kaynağını düzenleyin.')


def visual(file, caption, role='ana', note='Orijinal kaynak ve kullanım bağlamı yayın öncesi teyit edilecek.'):
    return {'file': '/media/' + file + '.jpg', 'role': role, 'captionDraft': caption,
            'verification': 'ön_inceleme', 'verificationNote': note, 'originalFile': None,
            'targetWidthMm': 180 if role == 'ana' else 85, 'crop': 'konu_ve_yazıları_koru'}


def page(n, title, purpose, body, bullets, visuals, sources, layout='fotoğraf_ve_metin', missing=None, claims=None):
    return {'id': f'T{n:02}', 'page': n, 'edition': 'tanitim', 'title': title,
            'purpose': purpose, 'copy': {'lead': body[0], 'paragraphs': body[1:], 'bullets': bullets},
            'layout': layout, 'visuals': visuals, 'sourceFiles': sources,
            'claimIds': claims or [], 'missing': missing or [], 'status': 'editoryal_taslak',
            'approvedBy': None, 'approvedAt': None, 'renderReady': False}


pages = [
    page(1, 'MATRO / Atölyeden sahaya', 'İlk bakışta gerçek bir mühendislik topluluğunun portföyünü tanıtmak.',
         ['Bursa Teknik Üniversitesi · Makine Teknolojileri Robot ve Otomasyon Topluluğu',
          'Birlikte tasarlıyor, üretiyor ve yarışıyoruz.'], [],
         [visual('mavi-vatan-ekipler', 'Mavi Vatan etkinliğinde MATRO ekipleri.')], ['src/data/home.json', 'src/data/site.json'], 'kapak',
         ['Dikey kapak için yüksek çözünürlüklü ana kare seçimi.', 'Yayın dönemi ve Tanıtım Günleri tarihi.']),
    page(2, 'Birlikte üreten bir topluluk', 'MATRO’nun kimliğini ve öğrenciye sunduğu ortamı anlatmak.',
         ['MATRO, Bursa Teknik Üniversitesi öğrencilerinin mühendislik fikirlerini ekip çalışmasıyla geliştirdiği bir topluluktur.',
          'Hava, kara, deniz ve sualtı araçlarından endüstriyel otomasyona uzanan projelerde mekanik, elektronik ve yazılım bir araya gelir. Atölye çalışmaları, yarışmalar, eğitimler ve teknik geziler bu deneyimin parçalarıdır.',
          '2013’te başlayan topluluk hikâyesini, farklı dönemlerde görev alan ekiplerin biriktirdiği bilgi ve deneyim sürdürüyor.'],
         ['Birden fazla disiplinde çalışma', 'Bilgiyi projede kullanma', 'Deneyimi yeni üyelere aktarma'],
         [visual('topluluk-ekip-selfie', 'MATRO üyelerinden bir grup.')], ['src/data/about.json', 'src/data/site.json'], claims=['kurulus']),
    page(3, 'Bir fikir nasıl projeye dönüşür?', 'Sonuç kadar üretim sürecinin de görünmesini sağlamak.',
         ['Bir aracın yarışma alanına çıkması, birbirini izleyen tasarım ve deneme adımlarının sonucudur.',
          'İhtiyaç ve görev tanımlanır; mekanik tasarım, elektronik altyapı ve yazılım birlikte geliştirilir. Üretimden çıkan parçalar bir araya getirilir, testlerde görülen sorunlar tasarıma geri taşınır. Her yeni deneme ekibin bir sonraki kararını besler.'],
         ['Problemi tanımla', 'Tasarla ve üret', 'Birleştir ve dene', 'Sonuçları kaydet ve geliştir'],
         [visual('galeri-ashina-kompozit-uretim', 'Kompozit parça üretiminden bir çalışma.'), visual('galeri-ashina-uretim', 'Atölyede bir hava aracı.', 'detay')],
         ['src/content/teams/ashina.md', 'src/content/activities/egitim-kampi-2025-2026.md'], 'süreç', ['Dört aşamaya ait farklı, doğrulanmış kareler.']),
    page(4, 'Sen hangi işi üstlenmek istersin?', 'Teknik ve teknik olmayan katkı yollarını görünür kılmak.',
         ['Bir projenin çalışması yalnızca yazılıma veya mekanik tasarıma bağlı değildir; farklı görevlerin birlikte yürütülmesine ihtiyaç duyar.',
          'Mekanik tasarım ve üretim, elektrik-elektronik, yazılım, analiz, görsel iletişim ve organizasyon alanları arasından ilgine uygun bir başlangıç yapabilirsin. Başvuru ve tanışma sürecinde beklentilerini, deneyimini ve öğrenmek istediklerini paylaşırsın.'],
         ['Mekanik ve üretim', 'Elektronik ve yazılım', 'Analiz ve tasarım', 'Sponsorluk, organizasyon ve iletişim'],
         [visual('webmedya-sanayide-dijital-31', 'Araç üzerinde birlikte çalışan ekip üyeleri.')], ['src/data/join.json', 'src/data/ekibimiz.json'], 'rol_haritası'),
    page(5, 'Çalışma alanlarımız', 'Takım, alt araç ve başvuru kategorisi kavramlarını ayırmak.',
         ['MATRO portföyü farklı dönemlerde geliştirilen araçları, ekipleri ve araştırma alanlarını bir araya getirir.',
          'Bir takım çatısı altında birden fazla araç veya alt ekip adı bulunabilir. Aşağıdaki sayfalar bu birikimi anlatır. Yeni dönem başvurusuna açık kategoriler ise katılım sayfasında ayrıca gösterilir; portföyde yer almak tek başına açık alım olduğu anlamına gelmez.'],
         ['Hava ve savunma', 'Kara, deniz ve sualtı', 'Sanayi ve haberleşme', 'Çevre, tarım ve girişimcilik'],
         [], ['src/content/teams', 'src/data/about.json', 'src/data/join.json'], 'portföy_haritası', ['13 başlığın 2026–2027 aktif/arşiv/alım durumu.', 'Alanları bağlayan düzenlenebilir vektör diyagram.'], ['takim_kapsami']),
]

team_rows = [
    (6, 'ASHİNA', 'ashina', 'Havacılıkta tasarımdan uçuşa',
     'ASHİNA, insansız hava araçlarının tasarımı ve görev otonomisi üzerinde çalışan havacılık ekibimizdir. Mekanik yapı, uçuş elektroniği, görüntü işleme ve yer istasyonu çalışmaları aynı proje içinde buluşur.',
     'Üretim aşamasındaki bir parçadan uçuşa hazır araca uzanan süreci, gerçek atölye fotoğrafları ve ekibin tasarım çizimleriyle anlatacağız. LAGARİ, FIRAT ve YELKOVAN adlarının dönem ve proje ilişkileri tarihli açıklamalarla gösterilecek.',
     ['Hava aracı tasarımı ve üretimi', 'Uçuş yazılımı ve görüntü işleme', 'Yer istasyonu ve sistem bütünleştirme'],
     [visual('galeri-ashina-teknofest-grup', 'Yarışma alanında ASHİNA ekibi.'), visual('tasarim-ashina-iha', 'Arşivdeki sabit kanat araç tasarımı.', 'teknik'), visual('galeri-ashina-kompozit-uretim', 'Atölyede kompozit üretimi.', 'detay')], ['Alt ekiplerin sezonları ve kullanılacak aracın adı.', 'CAD çiziminin hangi araca ait olduğu.']),
    (7, 'MATROVER & LUNA', 'tika-ika', 'Arazide çalışan robotlar',
     'Kara araçları çalışmalarımız, otonom sürüş ve tarımsal görevler için geliştirilen farklı platformları kapsar. MATROVER ve LUNA adları, bu portföydeki ayrı ekip ve araç çalışmalarını temsil eder.',
     'Mekanik gövde, algılama, hareket kontrolü ve görev planlama birlikte ele alınır. Tarımsal araç geçmişi ile insansız kara aracı yarışma projeleri, araç adı ve sezonuyla ayrı satırlarda anlatılacak.',
     ['Mekanik platform ve hareket sistemi', 'Algılama ve rota planlama', 'Görev odaklı araç geliştirme'],
     [visual('takim-matrover', 'MATROVER standında ekip ve araç.'), visual('takim-luna', 'LUNA İKA standında ekip ve araç.', 'detay'), visual('galeri-tika-tarimsal-ika', 'Tarımsal araç yarışmasından ekip fotoğrafı.', 'detay')], ['LUNAROV ve diğer adların üst ekip/dönem ilişkisi.', 'Kesintisiz her yıl derece ve altı derece ifadeleri kullanılmayacak.']),
    (8, 'İDA / LODOS', 'insansiz-deniz-araci', 'Su üstünde otonom hareket',
     'LODOS, insansız deniz aracı çalışmalarımızın ekip adıdır. Gövde ve elektronik sistemler, su üstünde seyir ve görev yazılımıyla birlikte geliştirilir.',
     'Sayfada gerçek tekne fotoğrafı ve gövde ayrıntısı yer alacak. Yarışma geçmişi tarihli bir bilgi satırında gösterilirken, kısa tanıtım klibine takım sayfasındaki QR üzerinden ulaşılacak.',
     ['Deniz aracı gövdesi ve sistem bütünleştirme', 'Seyir ve görev yazılımı', 'Elektronik donanım ve test'],
     [visual('takim-lodos', 'LODOS ekibi ve teknesi.'), visual('galeri-lodos-detay', 'Tekne içindeki elektronik ve bağlantılar.', 'detay')], ['2026–2027 proje hedefi ve gerçek test fotoğrafı.']),
    (9, 'İSS / PRUSA', 'insansiz-su-alti', 'Suyun altında mühendislik',
     'İnsansız Su Altı Sistemleri ekibimiz, mekanik, elektronik ve yazılımı sualtı görevleri için bir araya getirir. PRUSA, güncel yarışma anlatısında yer alan ekip adıdır.',
     'Sızdırmaz gövde, itki düzeni ve görev algılama gibi çalışma alanları gerçek araç görüntüsü üzerinden açıklanacak. Arşivdeki CAD görselleri ile fotoğrafın aynı araç nesline ait olup olmadığı belirtilmeden yan yana karşılaştırma yapılmayacak.',
     ['Gövde ve sızdırmazlık', 'İtki ve kontrol', 'Görüntü işleme ve görev yazılımı'],
     [visual('takim-iss-sualti-araci', 'Havuz kenarında bir İSS sualtı aracı.'), visual('tasarim-iss-auv-izometrik', 'Arşivden sualtı aracı tasarımı.', 'teknik')], ['PRUSA / BTU AUV / BTU DALAY adlarının araç nesilleri.', 'Uluslararası başarı kaydının birincil belgesi.']),
    (10, 'ZEMHERİ / SARA', 'su-alti-roketi', 'Yeni bir çalışma alanı',
     'ZEMHERİ, MATRO’nun sualtı roket sistemleri alanındaki takımını temsil eder. SARA adı arşivde yer alan araç görselinde kullanılır.',
     'Takımın ilk sezon deneyimi; tasarım, üretim ve ekip çalışması üzerinden anlatılacak. Yarışma sonucu finalistlik olarak açıkça belirtilecek; derece veya ödül kazanıldığı ima edilmeyecek.',
     ['Gövde ve malzeme çalışmaları', 'Sistem bütünleştirme', 'Takımın ilk sezon deneyimi'],
     [visual('galeri-zemheri-sara', 'Arşivde SARA adıyla kaydedilmiş araç.'), visual('galeri-zemheri-takim', 'Yarışma ortamında ekip üyeleri.', 'detay')], ['SARA adının güncel araçla ilişkisinin teyidi.', 'İlk katılım sezonunun açık yılı.']),
    (11, 'MATRİS', 'suru-iha', 'Birlikte hareket eden hava araçları',
     'MATRİS, birden fazla insansız hava aracının koordineli görev yapması üzerine çalışan ekibimizdir. Sürü yaklaşımı, tek bir aracı yönetmenin ötesinde araçlar arası haberleşme ve görev paylaşımını da kapsar.',
     'Gerçek hava aracı fotoğrafına, çoklu araç koordinasyonunu açıklayan sade bir şema eşlik edecek. Şema bir anlatım aracı olacak; ekibin ölçülmüş uçuş kaydı veya gerçek filo büyüklüğü gibi sunulmayacak.',
     ['Çoklu araç koordinasyonu', 'Haberleşme ve görev paylaşımı', 'Uçuş kontrolü ve yazılım'],
     [visual('takim-matris-iha', 'MATRİS portföyündeki hava aracı.')], ['Gerçek çoklu araç/test fotoğrafı.', 'Filo fotoğrafı diye etiketlenmiş özçekim kullanılmayacak.']),
    (12, 'PUSULA / ANDROMEDA', 'sanayide-dijital', 'Üretim süreçleri için akıllı sistemler',
     'Sanayide Dijital Teknolojiler çatısında üretim ve otomasyon problemleri üzerinde çalışıyoruz. PUSULA ile ANDROMEDA, farklı yarışma ve uygulama hatları olarak ayrı anlatılacak.',
     'PUSULA için araç ve atölye çalışmaları; ANDROMEDA için doğrulanmış programlama veya üretim senaryosu gösterilecek. İki ekibin çıktıları tek bir aracın özelliği gibi birleştirilmeyecek.',
     ['Endüstriyel otomasyon', 'Sensörler ve veri toplama', 'Görev programlama ve bütünleştirme'],
     [visual('galeri-pusula-atolye', 'PUSULA aracının yanında ekip üyeleri.'), visual('webmedya-sanayide-dijital-31', 'PUSULA aracı üzerinde çalışma.', 'detay')], ['ANDROMEDA için gerçek görsel ve kısa proje açıklaması.', '2021 üçüncülüğündeki teknik destek ilişkisi.']),
    (13, 'GÖKSAV / ASHİNA-H', 'ashina-h', 'Takip ve kontrol sistemleri',
     'GÖKSAV, hava savunma sistemleri alanındaki takım başlığıdır; ASHİNA-H adı da mevcut arşivde kullanılır. Proje anlatısı sensör, takip, kontrol ve sistem bütünleştirme çalışmalarına odaklanacak.',
     '2025 rapor değerlendirmesi sonucu, yarışma final sıralamasından açık biçimde ayrılacak. MERGEN adının bu ekiple ilişkisi teyit edilmeden görsel kesin alt araç başlığıyla sunulmayacak.',
     ['Algılama ve takip', 'Kontrol yazılımı', 'Sistem bütünleştirme'],
     [visual('galeri-mergen-hss', 'Arşivde MERGEN HSS adıyla kayıtlı sistem.', note='Görselde sistem görülüyor; GÖKSAV üst ekip ilişkisi henüz teyitsiz.')], ['GÖKSAV / ASHİNA-H / MERGEN ilişkisi.', 'Kapak ve mevcut test fotoğraflarının projeyle eşleşmesi.']),
    (14, 'BÜRKÜT', 'burkut', 'Simülasyonda geliştirmek',
     'BÜRKÜT, uçan araba ve otonom hareket senaryolarını simülasyon ortamında ele alan proje ekibimizdir. Yazılım geliştirme, görev planlama ve kontrol yaklaşımları bu çalışmanın merkezindedir.',
     'Bu sayfada simülasyon ekranı, senaryo akışı ve ekip fotoğrafı birlikte kullanılacak. Twizy geçmişindeki EMİZY ve MATROBOT adları, yıl ve takım ilişkisi doğrulandıktan sonra ayrı tarihçe kutusuna alınacak.',
     ['Kontrol ve durum kestirimi', 'Görev planlama', 'Simülasyonda deneme'],
     [visual('galeri-burkut-simulasyon-ekip', 'BÜRKÜT arşivindeki etkinlik ve ekip fotoğrafı.')], ['Gerçek simülasyon ekran görüntüsü.', '2020/2021 Twizy sezon ve sonuç tarihleri.']),
    (15, 'ÇAĞRI', 'cagri', 'Bağlantıyı sürdürebilmek',
     'ÇAĞRI, kablosuz haberleşme problemleri üzerinde çalışan ekibimizdir. Sinyal işleme, yazılım tabanlı radyo ve veri aktarımının güvenilirliği çalışma alanları arasında yer alır.',
     'Haberleşme sürecini anlatan düzenlenebilir bir verici–kanal–alıcı şemasına gerçek ekipman ve çalışma fotoğrafı eşlik etmeli. Şema temsili olacak; ölçülmemiş menzil veya veri hızı eklenmeyecek.',
     ['Sinyal işleme', 'Yazılım tabanlı radyo', 'Veri aktarımı ve doğrulama'], [],
     ['Takım/cihaz fotoğrafı şu an site kaydında yok.', '2026–2027 faaliyet ve alım durumu.']),
    (16, 'ALHAZEN', 'cevre-enerji', 'Enerji ve malzemeye odaklanmak',
     'ALHAZEN, çevre ve enerji teknolojileri üzerine çalışan ekibimizdir. Mevcut içerik yakıt pili, hidrojen enerjisi ve enerji verimliliği çalışmalarını anlatıyor.',
     'Sayfada gerçek laboratuvar çalışması ile yarışma katılımı iki ayrı bağlam olarak gösterilecek. Yarışma özçekimleri analiz deneyi gibi etiketlenmeyecek. Projenin adı, kullanılan yaklaşım ve elde edilen çıktı ekip tarafından teyit edilecek.',
     ['Enerji dönüşümü', 'Malzeme ve sistem çalışmaları', 'Çevre odaklı mühendislik'],
     [visual('takim-alhazen', 'Laboratuvarda malzeme üzerinde çalışma.'), visual('webmedya-cevre-enerji-9', 'Çevre ve enerji yarışması standında ekip.', 'detay')], ['Proje adı, laboratuvar fotoğrafının bağlamı ve çalışma sonucu.']),
    (17, 'ASHİNA İNOVASYON', 'ashina-inovasyon', 'Tarım için araştırmak',
     'ASHİNA İNOVASYON, tarımın saha ihtiyaçlarına yönelik araştırma ve proje geliştirme alanıdır. Mevcut takım kaydı literatür taraması, saha analizi ve prototipleme çalışmalarını tanımlar.',
     'Bu sayfa araştırma sorusunu, ele alınan ihtiyacı ve planlanan çalışma adımlarını anlatacak. Henüz belgelenmemiş bir araç veya tamamlanmış sonuç varmış gibi tanıtılmayacak.',
     ['Saha ihtiyacını anlamak', 'Araştırma ve kavram geliştirme', 'Deneme ve prototipleme'], [],
     ['Gerçek çalışma fotoğrafı.', 'Güncel araştırma konusu ve proje aşaması.', 'Sayfa tek başına yeterli içerik taşımazsa araştırma alanlarıyla birleştirilecek.']),
    (18, 'Fikirden girişime', 'girisimcilik', 'Teknik üretimin ürün ve girişim boyutunu anlatmak.',
     'Girişimcilik ve İnovasyon çalışmalarında teknik fikrin kullanıcı ihtiyacına, ürüne ve iş modeline dönüşmesi ele alınır. Hackathonlar ve proje yarışmaları bu deneyimin farklı yollarıdır.',
     'INNOSENS, SYNTAX ve SCENDERS adları ayrı ekip/çalışma kayıtları olarak sunulacak. Yarışma adı, yıl ve sonuç türü her kayıtla birlikte gösterilecek; bölgesel başarı ulusal veya dünya derecesine dönüştürülmeyecek.',
     ['Problem ve kullanıcı ihtiyacı', 'Ürün ve iş modeli', 'Hackathon ve proje deneyimi'],
     [visual('odul-girisimcilik', 'Girişimcilik ödül töreninden bir kare.'), visual('galeri-advance-up-syntax', 'Advance-Up Hackathon üçüncülük duyurusu.', 'belge')], ['Ekip adları ve başarıların birincil kayıtları.']),
]
for n, title, slug, subtitle, lead, body, bullets, visuals, missing in team_rows:
    p = page(n, title, subtitle, [lead, body], bullets, visuals,
             [f'src/content/teams/{slug}.md', 'src/data/achievements.json'], 'takım_profili', missing, ['takim_kapsami'])
    p['teamSlug'] = slug
    p['targetUrl'] = f'https://btumatro.com/takimlarimiz/{slug}/'
    p['layoutNotes'] = 'Üstte alan adı ve takım; ortada tek büyük gerçek görsel; altta 80–140 kelimelik anlatı, üç çalışma alanı, tarihli sonuç satırı. İkinci görsel veya teknik şema mümkünse karşı sütunda. Alt ekipler sezonla etiketlenir.'
    pages.append(p)

pages += [
    page(19, 'Emek, deneyim ve sonuç', 'Başarıları doğru ölçek ve bağlamla sunmak.',
         ['Her sonuç, farklı bir ekibin çalışma sürecinin bir parçasıdır. Bu seçki yarışma derecelerini, özel ödülleri ve finalistlikleri kendi adlarıyla gösterir.',
          'Yayın anındaki veri tabanında {{basari_kaydi}} kayıt ve {{birincilik}} birincilik kaydı bulunuyor. Sayıların yanında kapsadıkları dönem ve sonuç türü yazılacak; tüm kayıtlar aynı düzeyde bir ödül gibi gösterilmeyecek.'],
         ['Yıl / yarışma / takım / sonuç', 'Finalistlik ve derece ayrı gösterilir', 'Tam listeye QR bağlantısı'],
         [visual('odul-toreni', 'Bir ödül töreninden MATRO ekibi.')], ['src/data/achievements.json'], 'başarı_çizelgesi', ['6–8 birincil kaynaklı sonuç seçimi.'], ['basari_kaydi', 'birincilik', 'tarihsel_sayilar', 'pusula_2021', 'twizy']),
    page(20, '2026 sezonundan', 'Sezon kapsamını dört şehir haberiyle karıştırmadan göstermek.',
         ['2026 başarı listesinde sekiz finalist ekip kaydı bulunuyor. Sezonu, ekip adı ve yarışma kategorisiyle birlikte anlatıyoruz.',
          'Malatya’da ASHİNA, Diyarbakır’da PUSULA, Mardin’de LUNA İKA ve Gaziantep’te MATRİS aynı tarihli dört şehir haberinde yer alıyor. LODOS, PRUSA ve ZEMHERİ Mavi Vatan anlatısında; ANDROMEDA ise kendi yarışma kategorisinde ele alınacak.'],
         ['Dört şehirdeki haber: ASHİNA / PUSULA / LUNA İKA / MATRİS', 'Mavi Vatan: LODOS / PRUSA / ZEMHERİ', 'ANDROMEDA: ayrı yarışma kaydı'],
         [visual('haber-teknofest-2026-finalleri', 'Malatya / ASHİNA finalist duyurusu.', 'belge'), visual('haber-teknofest-2026-diyarbakir', 'Diyarbakır / PUSULA finalist duyurusu.', 'belge'), visual('haber-teknofest-2026-mardin', 'Mardin / LUNA İKA finalist duyurusu.', 'belge'), visual('haber-teknofest-2026-gaziantep', 'Gaziantep / MATRİS finalist duyurusu.', 'belge')],
         ['src/data/achievements.json', 'src/content/haberler/teknofest-2026-finalleri.md', 'src/content/haberler/mavi-vatan-finalistlerimiz-2026.md'], 'sezon_haritası', ['Haritada yalnız doğrulanmış şehirler işaretlenecek.', 'Ham fotoğraflar bulunduğunda afiş yerine fotoğraf seçimi.'], ['finalistler_2026']),
    page(21, 'Öğrenerek üretmek', 'Yeni üyeye somut öğrenme deneyimi göstermek.',
         ['Atölyeye katılan bir öğrencinin ilk ihtiyacı, birlikte çalışacağı alanları tanımaktır. Eğitim programları bu başlangıç için ortak bir temel oluşturur.',
          '2025–2026 birinci eğitim kampı kaydında 32 ders saati ve belge almaya hak kazanan 61 katılımcı yer alıyor. Bu geçmiş program, yeni dönemde aynı takvim veya aynı içeriğin kesin açılacağı sözü olarak sunulmayacak.'],
         ['Mekanik, elektronik ve yazılım temeli', 'Uygulama ve ekip çalışması', 'Geçmiş programdan ölçülebilir örnek'],
         [visual('haber-ikinci-egitim', 'Eğitim çalışmalarından duyuru kolajı.', 'belge'), visual('galeri-turkish-technic-sinif', 'Turkish Technic çalıştayından ders ortamı.', 'detay')], ['src/content/activities/egitim-kampi-2025-2026.md', 'src/content/haberler/ikinci-egitim-etabi-tamamlandi.md'], 'eğitim', ['Eğitim kampına ait doğrudan sınıf/uygulama kareleri; başka çalıştayın fotoğrafı kamp diye etiketlenmeyecek.'], ['egitim_kampi']),
    page(22, 'Mühendisliği yerinde görmek', 'Teknik gezi, ziyaret ve sponsor ilişkisinin farkını korumak.',
         ['Teknik geziler ve çalıştaylar, öğrencilerin mühendisliğin üretim ortamındaki karşılığını görmesini sağlar.',
          'Turkish Technic ve HKTM gibi kurumlara yapılan ziyaretlerden seçilen kareler; görülen çalışma alanı ve etkinlik adıyla anlatılacak. Kurum logosunun bu sayfada bulunması sponsorluk ilişkisi anlamına gelmeyecek.'],
         ['Üretim ve bakım ortamlarını tanımak', 'Mühendislerle doğrudan temas', 'Atölyedeki soruları sahaya taşımak'],
         [visual('galeri-turkish-technic-hangar', 'Turkish Technic ziyaretinde hangarda MATRO grubu.'), visual('galeri-hktm-grup', 'HKTM ziyaretinden grup fotoğrafı.', 'detay')], ['src/content/activities/teknik-geziler.md', 'src/content/haberler/turkish-technic-muhendislik-calistayi.md'], 'fotoğraf_yazısı', ['Etkinlik tarihleri, fotoğraf açıklamaları ve yüksek çözünürlüklü kaynaklar.']),
    page(23, 'Birlikte öğrenmenin ötesinde', 'Topluluk deneyiminin sosyal tarafını anlatmak.',
         ['MATRO’da ortak üretim; tanışma, paylaşma ve birbirine destek olma kültürüyle birlikte gelişir.',
          'Sosyal etkinlikler üyelerin birbirini tanımasını sağlar. Mentorluk ve Kardeş Okul çalışmaları ise teknoloji deneyiminin farklı yaş gruplarıyla paylaşılmasına alan açar. Her faaliyet gerçek tarih ve kendi görselleriyle anlatılacak.'],
         ['Topluluk etkinlikleri', 'Öğrencilere mentorluk', 'Kardeş Okul çalışmaları'],
         [visual('topluluk-ekip-selfie', 'Topluluk üyelerinden bir grup.', 'geçici')], ['src/content/activities/kardes-okul.md', 'src/content/activities/mentorluk.md', 'src/data/gallery.json'], 'insan_hikâyesi', ['Kapakta/ikinci sayfada kullanılan kare yerine farklı bir etkinlik fotoğrafı.', 'Sosyal sorumluluk için tarihli etki kaydı.']),
    page(24, 'Topluluğu birlikte yürütüyoruz', 'Yönetim görevlerini teknik takım çalışmasından ayırmak.',
         ['Bir topluluğun sürdürülebilmesi, teknik projelerin yanında düzenli organizasyon ve iletişim çalışmasına da ihtiyaç duyar.',
          'Atölye, sponsorluk, organizasyon ve sosyal medya birimleri farklı sorumluluklar üstlenir. Bu alanlarda görev almak, yarışma takımına başvurmaktan ayrı bir katılım yoludur. Sayfada kişilerden önce birimlerin yaptığı işler anlatılacak.'],
         ['Atölye: çalışma ortamı ve koordinasyon', 'Sponsorluk: iş birlikleri', 'Organizasyon: etkinlik süreçleri', 'Sosyal medya: içerik ve iletişim'],
         [], ['src/data/ekibimiz.json', 'src/data/join.json'], 'organizasyon_şeması', ['2026–2027 yönetim yapısı teyidi; isim kullanılacaksa dönem ve onay.']),
    page(25, 'Üretimin arkasındaki destek', 'Sponsorları dönemleri ve katkılarıyla doğru temsil etmek.',
         ['Projelerin gelişmesine katkı sağlayan destekçilerimiz, ekiplerin üretim ve çalışma olanaklarının güçlenmesine yardımcı olur.',
          'Bu sayfada yalnız dönemi, adı ve kademesi doğrulanmış sponsorlar yer alacak. Geçmiş dönem destekleri ayrı etiketlenecek; sponsorluk ile teknik gezi ilişkisi birbirine karıştırılmayacak.'],
         ['Onaylı firma adı', 'Destek dönemi ve türü', 'Oranları korunmuş logo yerleşimi'], [],
         ['src/data/sponsors.json', 'src/data/sponsorship.json'], 'sponsor_logoları', ['A.VET / A.NET kaynak düzeltmesi.', 'AKKUŞ ve diğer kademelerin dönem teyidi.', 'Vektör logolar.'], ['sponsorlar']),
    page(26, 'Bir projenin ihtiyaçları', 'Somut destek çeşitlerini görünür kılmak.',
         ['Bir proje, yalnızca fikirden oluşmaz. Malzeme, üretim olanağı, test ekipmanı ve çalışma araçları da geliştirme sürecinin parçasıdır.',
          'Bir iş birliği nakit katkı, malzeme temini, üretim hizmeti veya yazılım desteği şeklinde kurulabilir. İhtiyaçlar ekiplerle birlikte belirlenir; kapsam ve resmi süreç görüşmede netleştirilir.'],
         ['Malzeme ve bileşen', 'Üretim ve hizmet', 'Yazılım ve ekipman', 'Nakit destek'],
         [visual('galeri-ashina-kompozit-uretim', 'Üretim aşamasından bir örnek.', 'geçici')], ['src/data/sponsorship.json'], 'destek_akışı', ['Güncel ihtiyaç listesinden somut, onaylı örnekler.', 'Sayfa 3/6 ile tekrar etmeyen üretim görseli.']),
    page(27, 'MATRO’da kendi yolunu seç', 'Üç ayrı başvuru işlemini anlaşılır biçimde sunmak.',
         ['Topluluğa katılmak, bir yarışma ekibinde çalışmak ve yönetimde sorumluluk almak farklı katılım yollarıdır.',
          'Topluluk kaydı genel üyelik içindir. Yarışma takımlarında görev almak isteyenler takım ön başvurusuyla tercihlerini bildirir. Atölye, sponsorluk, organizasyon ve sosyal medya çalışmalarında sorumluluk almak isteyenler yönetim başvurusunu kullanır.'],
         ['Topluluk kaydı', 'Takım ön başvurusu', 'Yönetim kurulu başvurusu'], [], ['src/data/join.json'], 'katılım',
         ['Açık formlar ve dönem son kez kontrol edilecek.', 'Tanıtım Günleri tarih ve stand yeri.', 'Üç ayrı QR ve okunabilir hedef bağlantıları.'], ['basvuru']),
    page(28, 'Bir sonraki projede görüşmek üzere', 'Kolay ve kalıcı iletişim hedefi vermek.',
         ['MATRO · Bursa Teknik Üniversitesi', 'Projelerimizi, güncel duyuruları ve katılım yollarını web sitemizden takip edebilirsiniz.'],
         ['btumatro.com', 'matroiletisim@gmail.com', 'Instagram: @btumatro'], [], ['src/data/site.json'], 'arka_kapak', ['Son iletişim ve QR testi.']),
]

sponsor_specs = [
    ('S27', 27, 'Bu dönem neyi üretmek istiyoruz?', 'Her proje için hedef, mevcut aşama, beklenen çıktı ve sezon yazılır.', ['Takım kaptanlarından tarihli proje hedefleri.', 'Hedefe ait gerçek araç/çizim.']),
    ('S28', 28, 'Desteğin projeye dönüşeceği kalemler', 'İhtiyaç, adet, nakit/ayni destek, teklif tarihi ve öncelik birlikte gösterilir. Henüz teyitli bütçe verisi bulunmadığı için rakam doldurulmaz.', ['Güncel teklif ve ihtiyaç tablosu.', 'Destek kalemini gösteren gerçek üretim fotoğrafı.']),
    ('S29', 29, 'Birlikte görünür olmak', 'Araç, forma, stant ve dijital mecralardaki destekçi görünürlüğü, onaylanmış kapsamla anlatılır.', ['İzin verilen logo alanları ve kullanım örnekleri.', 'Üniversite ve yönetimce teyit edilen haklar.']),
    ('S30', 30, 'Destek seçenekleri', 'Nakdi ve ayni katkı için geçerli dönem ve kademe matrisi hazırlanır. Eski tutarlar yeni sezonun onaylı koşulu gibi sunulmaz.', ['Yürürlükteki sponsorluk kademeleri ve hakları.', 'Ayni desteğin değerlendirme usulü.']),
    ('S31', 31, 'İş birliğini birlikte yürütelim', 'İlk görüşme, ihtiyaç eşleştirme, üniversite süreci ve çıktı paylaşımı birbirini izler. Raporlama sıklığı yönetimle kararlaştırılır.', ['İş birliği sorumlusu ve süreç teyidi.', 'Teslim/raporlama kapsamı; garanti verilmeyecek.']),
    ('S32', 32, 'Ortak bir projeyi konuşalım', 'Sponsorluk ve proje iş birlikleri için kurumsal iletişim kanallarımızdan bize ulaşabilirsiniz.', ['Kurumsal e-posta ve sponsorluk sayfasına QR.', 'Yayın dönemi ve belge sürümü.']),
]
sponsor = []
for id_, n, title, lead, missing in sponsor_specs:
    p = page(n, title, 'Sponsor görüşmesine yönelik ek modül.', [lead], [], [], ['src/data/sponsorship.json'], 'sponsor_modülü', missing, ['sponsorlar'])
    p.update(id=id_, edition='sponsorluk')
    sponsor.append(p)

plan = {'schemaVersion': 1, 'revision': '0.1', 'language': 'tr', 'status': 'yönetim_değerlendirmesi_için_taslak',
        'reviewedCommit': '2708626db9c683113531a1ecfae54e9d8f680cd7', 'updatedAt': '2026-09-11',
        'format': {'widthMm': 210, 'heightMm': 297, 'orientation': 'portrait', 'pageLimit': None},
        'editingRule': 'Metin, görsel ve kaynak değişikliklerini bu dosyada yapın; üretilen Markdown/CSV tekrar üretilebilir.',
        'brandFiles': ['public/matro-logo-siyah.svg', 'public/matro-logo-mavi.svg', 'public/logo-matro-beyaz.png'],
        'pages': pages, 'sponsorModule': sponsor,
        'editions': {'tanitim': [p['id'] for p in pages], 'sponsorluk': [p['id'] for p in pages[:26]] + [p['id'] for p in sponsor]},
        'editionOverrides': {'sponsorluk': {'T01': {'title': 'MATRO / Projeler ve iş birlikleri', 'note': 'Tanıtım kapağı yerine sponsor görüşmesine uygun kapak.'}}}}
TARGET.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + '\n')
print(TARGET)
