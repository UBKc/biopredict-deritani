@echo off
cd /d "%~dp0yolov5"
rem mobilde kullanmak icin onnx ve tflite'a ceviriyorum
python export.py --weights runs/train/deritani/weights/best.pt --img 640 --include onnx tflite
