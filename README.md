# BioPredict – DeriTanı: Cilt Hastalığı Tespiti

TEKNOFEST 2025 İnsanlık Yararına Teknoloji Yarışması, Sağlık Teknolojileri kategorisinde finale kalan ve Türkiye 13.'sü olan projemizin yapay zekâ kısmı.

Uygulama, kullanıcının çektiği cilt fotoğrafında 4 yaygın, kanser olmayan cilt hastalığını tespit edip ön değerlendirme sunuyor. Amaç teşhis koymak değil, dermatoloğa erişimi zor olan kişilerin doktora gitme kararını kolaylaştırmak.

## Projede benim kısmım

Takımda yapay zekâ modelinden ben sorumluydum: veri setini hazırlama, etiketleme, model eğitimi, doğrulama ve modeli mobile uygun hale getirme. Mobil uygulama (React Native), backend (Node.js) ve veritabanı (MongoDB) tarafını takım arkadaşlarım geliştirdi, o kodlar bu repoda yok.

Yarışma sürecinde kullandığım dosyalar elimde kalmadığı için eğitim hattını düzenleyip yeniden yazdım.

## Sınıflar

| ID | Sınıf |
|---|---|
| 0 | Akne |
| 1 | Egzama |
| 2 | Sedef |
| 3 | Gül hastalığı (rozasea) |

## Veri seti

- Eğitim: 8.931 görüntü
- Doğrulama: 2.218 görüntü
- Etiketleme MakeSense.ai ile yapıldı, YOLO formatında (`sinif x_merkez y_merkez genislik yukseklik`, 0-1 arası).

Veri seti sağlık verisi olduğu için paylaşılmıyor. Klasör yapısı şöyle olmalı:

```
veri/
├── images/train/   images/val/
└── labels/train/   labels/val/
```

## Neden YOLOv5l

Sınıflandırma yerine nesne tespiti seçtik çünkü fotoğrafta hastalıklı bölgenin yerini de göstermek istedik. YOLOv8 o dönem daha yaygındı ama mobile aktarırken uyumluluk sorunları yaşanabiliyordu. YOLOv5l mobil tarafta daha stabil çalıştığı için onu kullandık.

## Dosyalar

| Dosya | Ne işe yarıyor |
|---|---|
| `veri_bol.py` | etiketli bütün görüntüleri %80 eğitim, %20 doğrulama olarak ayırıyor (sabit seed) |
| `veri_kontrol.py` | eğitimden önce etiketleri kontrol ediyor: etiketsiz görüntü, yanlış sınıf numarası, 0-1 dışına taşan kutu, sınıf başına kutu sayısı |
| `veri.yaml` | YOLOv5'in veri seti ayarı |
| `on_isleme.py` | 640x640 letterbox ön işleme ve kutuları orijinal resme geri çevirme |
| `egit.bat` | YOLOv5l eğitimi (640, COCO ağırlıklarından transfer öğrenme) |
| `tahmin.py` | eğitilen modelle tek fotoğrafta tahmin |
| `disa_aktar.bat` | modeli mobil için ONNX ve TFLite'a çevirme |

## Kurulum

```
git clone https://github.com/ultralytics/yolov5
pip install -r yolov5/requirements.txt
pip install -r requirements.txt
```

## Çalıştırma sırası

```
python veri_bol.py
python veri_kontrol.py
egit.bat
python tahmin.py foto.jpg
disa_aktar.bat
```

## Ön işleme

Fotoğraflar farklı telefonlardan, farklı boyutlarda geliyor. Modele 640x640 veriliyor ama resmi direkt 640x640'a germek lezyonların şeklini bozuyor. Bu yüzden letterbox kullandım: resim en-boy oranı korunarak küçültülüyor, boş kalan yer griyle dolduruluyor. Mobilde de aynı ön işlemenin yapılması gerekiyor, yoksa eğitimdekiyle aynı sonuç alınmıyor.

## Mobile aktarma

Modeli telefonda çalıştırmak için ONNX ve TFLite formatlarını denedik. `disa_aktar.bat` ikisini birden üretiyor.

## Eksikler ve geliştirilebilecekler

- Veri setinin çeşitliliği artırılmalı, farklı cilt tiplerinden ve hastalık evrelerinden daha fazla örnek eklenmeli.
- Model, dermatologlarla birlikte gerçek klinik ortamda test edilmedi.
- Telefonlardaki performans daha fazla cihazda ölçülmeli.

## Lisans

YOLOv5 AGPL-3.0 lisanslı olduğu için bu repo da AGPL-3.0 ile lisanslandı.
