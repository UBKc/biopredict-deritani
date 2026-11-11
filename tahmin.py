import sys
import cv2
import torch
import logging

logging.basicConfig(level=logging.INFO)

# egitilen modelle tek bir fotograf uzerinde tahmin
# kullanim: python tahmin.py foto.jpg
yolov5_klasoru = "yolov5"
agirlik = "yolov5/runs/train/deritani/weights/best.pt"

model = torch.hub.load(yolov5_klasoru, "custom", path=agirlik, source="local")
model.conf = 0.4     # bunun altindaki tespitleri almiyorum
model.iou = 0.45

resim = cv2.imread(sys.argv[1])
sonuc = model(resim[..., ::-1], size=640)   # model rgb bekliyor

tespitler = sonuc.pandas().xyxy[0]
if len(tespitler) == 0:
    logging.info("tespit yok")
for _, t in tespitler.iterrows():
    logging.info(f"{t['name']}: %{t['confidence'] * 100:.1f}")

cizili = sonuc.render()[0][..., ::-1]
cv2.imwrite("tahmin_sonuc.jpg", cizili)
