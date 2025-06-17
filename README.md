# BentoML_YOLO
Работа с YOLO, обученной на детекцию куриц, в bentoML

---

## Этапы работы

1. **Обучение модели**
   - Обучаю YOLOv8-s детектировать куриц на размеченном датасете из kaggle (Chicken Object Detection/Segmentation)
   - Обучение сделал в ноутбуке в kaggle`TrainYolo/chicken-detect.ipynb`

2. **Сохранение модели**
   - Веса модели сохранил и добавил в проект
   - Скрипт `BentoYoloCheck/save_model_to_bento.py` добавляет веса в Bento

3. **Создание API**
   - В `BentoYoloCheck/service/service.py` реализовал два метода:
     - `count` - возвращает количество куриц на изображении
     - `annotate` - возвращает количество и изображение с боксами
     - Пытался добавить логирование запросов, но не до конца получилось
   - `BentoYoloCheck/service/bentofile.yaml` - Bento спецификация (для containerize/build)
   - `BentoYoloCheck/service/bento-settings.yaml` - Конфигурация сервиса
   - Дальше bentoml build и bentoml serve chicken_service:latest


4. **Тестирование API**
   - `BentoYoloCheck/client.py` - пример отправки запроса по апи
   - `BentoYoloCheck/chicken_test.jpg` и `BentoYoloCheck/annotated.jpg`-  пример отправленной фотки и полученной с боксами
   

5. **containerize**
   - Дальше хотел запаковать через bentoml containerize, но проблема с docker, поэтому пока отложил




