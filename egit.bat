@echo off
cd /d "%~dp0yolov5"
rem yolov5l, 640 boyut, coco on egitimli agirliklardan transfer ogrenme
python train.py --img 640 --batch 16 --epochs 100 --data ../veri.yaml --weights yolov5l.pt --name deritani
