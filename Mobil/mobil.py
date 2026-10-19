from build123d import *
from ocp_vscode import show, set_port
import logging
import traceback
import math

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from path_manager import path_mgr

# Настройка логирования: ошибки будут писаться в файл 'error_log.txt' и выводиться в консоль
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("error_log.txt"),  # Лог в файл
        logging.StreamHandler(),  # Лог в консоль
    ],
)

# Параметры пластины (мм)
plate_length = 150.0   # длина
plate_width = 100.0    # ширина
plate_thickness = 3.0   # глубина (толщина)
hole_diameter = 25.0    # диаметр сквозного отверстия без резьбы

try:
    with BuildPart() as Plate:
        # Пластина (Box центрирован по умолчанию → центр в начале координат)
        Box(plate_length, plate_width, plate_thickness)
        # Сквозное отверстие строго по центру, без резьбы
        Cylinder(radius=hole_diameter / 2, height=plate_thickness, mode=Mode.SUBTRACT)
    export_step(Plate.part, path_mgr.get_file_path("mobil.step"))
    set_port(3939)
    show(Plate, port=3939)
except Exception as ex:
    logging.error(f"Произошла ошибка: {str(ex)}")
    logging.error(traceback.format_exc())
    print(f"Ошибка: {str(ex)}. Проверьте лог в 'error_log.txt' для деталей.")
    input("Нажмите Enter для выхода...")  # Чтобы скрипт не закрывался сразу
