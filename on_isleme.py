import cv2
import numpy as np


def letterbox(resim, boyut=640, renk=(114, 114, 114)):
    # resmi en-boy oranini bozmadan 640x640'a sigdiriyor, kalan yeri griyle dolduruyor
    # yolov5 egitimde ve tahminde ayni seyi yapiyor, mobilde de ayni on islemenin
    # yapilmasi lazim yoksa sonuclar degisiyor
    h, w = resim.shape[:2]
    olcek = min(boyut / h, boyut / w)
    yeni_w, yeni_h = int(round(w * olcek)), int(round(h * olcek))
    kucuk = cv2.resize(resim, (yeni_w, yeni_h), interpolation=cv2.INTER_LINEAR)

    ust = (boyut - yeni_h) // 2
    sol = (boyut - yeni_w) // 2
    tuval = np.full((boyut, boyut, 3), renk, dtype=np.uint8)
    tuval[ust:ust + yeni_h, sol:sol + yeni_w] = kucuk
    return tuval, olcek, (sol, ust)


def kutuyu_geri_cevir(kutu, olcek, kayma):
    # 640x640 uzerindeki kutuyu orijinal resmin koordinatina geri ceviriyor
    x1, y1, x2, y2 = kutu
    sol, ust = kayma
    return [(x1 - sol) / olcek, (y1 - ust) / olcek, (x2 - sol) / olcek, (y2 - ust) / olcek]


if __name__ == "__main__":
    import sys
    resim = cv2.imread(sys.argv[1])
    sonuc, olcek, kayma = letterbox(resim)
    cv2.imwrite("letterbox_ornek.jpg", sonuc)
    print(f"olcek {olcek:.3f}, kayma {kayma}")
