import os
import random
import shutil
import logging

logging.basicConfig(level=logging.INFO)

# etiketlenmis butun goruntuler tek klasorde, bunlari train ve val olarak ayiriyorum
kaynak_resim = "veri/hepsi/images"
kaynak_etiket = "veri/hepsi/labels"
hedef = "veri"
val_orani = 0.2

random.seed(42)   # her calistirmada ayni bolme olsun

dosyalar = []
for f in os.listdir(kaynak_resim):
    if f.lower().endswith((".jpg", ".jpeg", ".png")):
        dosyalar.append(f)
dosyalar.sort()
random.shuffle(dosyalar)

val_sayisi = int(len(dosyalar) * val_orani)
bolumler = {"val": dosyalar[:val_sayisi], "train": dosyalar[val_sayisi:]}

for bolum, liste in bolumler.items():
    os.makedirs(f"{hedef}/images/{bolum}", exist_ok=True)
    os.makedirs(f"{hedef}/labels/{bolum}", exist_ok=True)
    for dosya in liste:
        ad = os.path.splitext(dosya)[0]
        shutil.copy(f"{kaynak_resim}/{dosya}", f"{hedef}/images/{bolum}/{dosya}")
        etiket = f"{kaynak_etiket}/{ad}.txt"
        if os.path.exists(etiket):
            shutil.copy(etiket, f"{hedef}/labels/{bolum}/{ad}.txt")
    logging.info(f"{bolum}: {len(liste)} goruntu")
