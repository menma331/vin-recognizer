import logging
import re
import cv2
import math
from PIL import Image
import numpy as np

def is_valid_vin(vin: str) -> bool:
    """Проверяем, что строка состоит из 17 символов и только из цифр и букв (кроме I, O, Q)"""
    if len(vin) != 17:
        return False

    # Регулярное выражение для проверки VIN
    vin_regex = r'^[A-HJ-NPR-Z0-9]{17}$'

    # Проверяем, соответствует ли VIN шаблону
    return bool(re.match(vin_regex, vin))




def rotate_image(image_path, output_path, rotate=0):
    """Предобработка фотографии для улучшения распознавания"""
    img = Image.open(image_path)

    if rotate > 0:
        # Поворот с расширением холста (expand=True)
        img = img.rotate(rotate, resample=Image.BILINEAR, expand=True)

    # Сохранение без потерь (для PNG)
    img.save(output_path, format="PNG", compress_level=0)

    return output_path


def determine_image_rotation(image_path):
    """Определение угла, на который нужно повернуть фотографию для центрирования."""
    # 1. Загрузка изображения
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Не удалось загрузить изображение")

    # 2. Предварительная обработка
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # 3. Обнаружение особенностей (используем детектор границ Canny + HoughLines)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

    if lines is None or len(lines) < 5:
        logging.info("Не удалось обнаружить достаточное количество линий для определения ориентации")
        return 0

    # 4. Определение угла поворота
    angles = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        angles.append(angle)

    # Фильтрация углов (игнорируем вертикальные/горизонтальные линии)
    filtered_angles = [a for a in angles if abs(a) > 10 and abs(a) < 80]

    if not filtered_angles:
        logging.info("Не удалось определить значимый угол поворота")
        return 0

    # Вычисляем медианный угол для устойчивости к выбросам
    median_angle = np.median(filtered_angles)

    # 5. Определение необходимого вращения для коррекции
    if abs(median_angle) < 45:
        correction_angle = -median_angle
    else:
        # Если угол близок к 90 градусам, возможно изображение повернуто на 90/180/270
        correction_angle = 90 - median_angle if median_angle > 0 else -90 - median_angle

    # Ограничиваем угол коррекции разумными пределами
    correction_angle = max(-45, min(45, correction_angle))

    logging.info(f'Требуется повернуть на {correction_angle} градусов')
    return correction_angle
