import os
S='/private/tmp/claude-501/-Users-wildgenie-Projects-btu-matro/c4790c33-2952-44d6-b402-a148a7fb5c92/scratchpad'
K=[("Muhammed Ataman","muhammed-ataman"),("Irmak Karaağaç","irmak-karaagac"),("Gülsiye Begüm Gümüş","gulsiye-begum-gumus"),("Ömer Cihan Demir","omer-cihan-demir"),
("Yusuf Sarsıcı","yusuf-sarsici"),("Feyza Karabıçak","feyza-karabicak"),("Nusret Bircan Keser","nusret-bircan-keser"),("Rumeysa Akarsu","rumeysa-akarsu"),
("Zeynep Seher Yolasığmaz","zeynep-seher-yolasigmaz"),("Berat Eren Karakaş","berat-eren-karakas"),("Zehra Bulut","zehra-bulut"),("Aslıhan Okumuş","aslihan-okumus"),
("Melek Özkeser","melek-ozkeser"),("Emine Sultan Güneş","emine-sultan-gunes"),("Melisa Aydirek","melisa-aydirek"),("Eslem Kılıç","eslem-kilic"),
("Esma Demirkıyık","esma-demirkiyik"),("Muhammed Efe Coşkunpınar","muhammed-efe-coskunpinar"),("Adem Bağlan","adem-baglan"),("Bilgehan Zeki Özaytaç","bilgehan-zeki-ozaytac")]
def gercek(s):
    for p in (f'{S}/ref/{s}.jpg', f'public/media/ekip/{s}.jpg'):
        if os.path.exists(p): return p
    if s=='bilgehan-zeki-ozaytac': return 'docs/ekip/orijinal/bilgehan-zeki-ozaytac.jpg'
