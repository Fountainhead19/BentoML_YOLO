import bentoml
from ultralytics import YOLO


model = YOLO("yolov8_chicken_best.pt")

#Picklable потому что ultralistic не входит в поддерживаемые фреймворки bento
bento_model = bentoml.picklable_model.save_model(
    name="yolov8_chicken",   #имя модели в BentoML
    model=model,
    metadata={"framework": "ultralytics", "task": "object_detection"}
)
# bentoml models - команды
print(f"Модель сохранена в Bento {bento_model.tag}")
