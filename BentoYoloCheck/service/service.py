import io
import json
import base64
from pathlib import Path
from typing import Annotated
from PIL import Image as PILImage
from pydantic import BaseModel, Field

import bentoml
import yaml
from bentoml.validators import ContentType
from ultralytics import YOLO
import logging
import json
from datetime import datetime

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log["error"] = self.formatException(record.exc_info)
        return json.dumps(log)

#Подключаем логгер бенто
bento_logger = logging.getLogger("bentoml")
bento_logger.setLevel(logging.INFO)

#Добавляем запись в файл
file_handler = logging.FileHandler("bentoml_access.log", encoding="utf-8")
file_handler.setFormatter(JsonFormatter())
bento_logger.addHandler(file_handler)

#Загрузка настроек из YAML
with open("bento-settings.yaml", "r") as cfg:
    settings = yaml.load(cfg, yaml.SafeLoader)

#Типы входных данных
Image = Annotated[Path, ContentType("image/*")]

class InputParams(BaseModel):
    conf: float = Field(0.25, gt=0, lt=1.0)


@bentoml.service(**settings["service"])
class chicken_service:
    def __init__(self):
        self.model: YOLO = bentoml.picklable_model.load_model("yolov8_chicken:latest") #загрузка модели из бенто

    @bentoml.api()
    def count(self, image: Image, parameters: InputParams) -> dict: #возврат кол-во куриц
        results = self.model.predict(image, conf=parameters.conf, verbose=False)
        count = len(results[0].boxes)
        return {"count": count}

    @bentoml.api()
    def annotate(self, image: Image, parameters: InputParams) -> dict: #возврат кол-во куриц и боксы
        results = self.model.predict(image, conf=parameters.conf, verbose=False)
        count = len(results[0].boxes)

        annotated_np = results[0].plot()
        annotated_img = PILImage.fromarray(annotated_np)
        buffer = io.BytesIO()
        annotated_img.save(buffer, format="JPEG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return {
            "count": count,
            "image_base64": img_base64
        }
