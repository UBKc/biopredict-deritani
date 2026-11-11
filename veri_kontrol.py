import os
import logging
from collections import Counter

logging.basicConfig(level=logging.INFO)

# makesense.ai'dan yolo formatinda aldigim etiketleri egitimden once kontrol ediyorum:
# etiketsiz goruntu, bos etiket, yanlis sinif numarasi, 0-1 disina tasan kutu var mi

siniflar = ["akne", "egzama", "sedef", "gul_hastaligi"]

for bolum in ["train", "val"]:
    resim_klasoru = f"veri/images/{bolum}"
    etiket_klasoru = f"veri/labels/{bolum}"

    sinif_sayilari = Counter()
    etiketsiz = []
    hatali = []

    for dosya in sorted(os.listdir(resim_klasoru)):
        ad = os.path.splitext(dosya)[0]
        etiket = f"{etiket_klasoru}/{ad}.txt"
        if not os.path.exists(etiket):
            etiketsiz.append(dosya)
            continue

        with open(etiket) as f:
            satirlar = [s.split() for s in f.read().strip().splitlines()]
        if len(satirlar) == 0:
            etiketsiz.append(dosya)
            continue

        for satir in satirlar:
            # her satir: sinif x_merkez y_merkez genislik yukseklik
            if len(satir) != 5:
                hatali.append(f"{ad}: {len(satir)} deger var, 5 olmali")
                continue
            sinif = int(satir[0])
            x, y, w, h = map(float, satir[1:])
            if sinif < 0 or sinif >= len(siniflar):
                hatali.append(f"{ad}: sinif {sinif} yok")
            elif not (0 <= x <= 1 and 0 <= y <= 1 and 0 < w <= 1 and 0 < h <= 1):
                hatali.append(f"{ad}: kutu 0-1 araliginda degil")
            else:
                sinif_sayilari[siniflar[sinif]] += 1

    logging.info(f"--- {bolum}: {len(os.listdir(resim_klasoru))} goruntu")
    for sinif in siniflar:
        logging.info(f"{sinif}: {sinif_sayilari[sinif]} kutu")
    logging.info(f"etiketsiz goruntu: {len(etiketsiz)}")
    logging.info(f"hatali satir: {len(hatali)}")
    for h in hatali[:10]:
        logging.info(f"  {h}")
