from build123d import *
from ocp_vscode import show, set_port
import logging
import traceback
import math

from Screw import ScrewManager

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from path_manager import path_mgr  

# Настройка логирования: ошибки будут писаться в файл 'error_log.txt' и выводиться в консоль
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('error_log.txt'),  # Лог в файл
        logging.StreamHandler()  # Лог в консоль
    ]
)
try: 
    with BuildPart() as Screw:
        # Шестиугольное отверстие под гайку M6
        nut = ScrewManager(6)
        print(repr(nut))
        Cylinder(radius=nut.hole_dia, height=6)
        with BuildSketch(Screw.faces().sort_by(Axis.Z)[-1]):
            RegularPolygon(radius=nut.hex_radius, side_count=6)
            #Circle(radius=4, mode=Mode.SUBTRACT)
        extrude(amount=-5, mode=Mode.SUBTRACT)
    set_port(3939)
    show(Screw, port=3939)
except Exception as ex:
    logging.error(f"Произошла ошибка: {str(e)}")
    logging.error(traceback.format_exc())
    print(f"Ошибка: {str(e)}. Проверьте лог в 'error_log.txt' для деталей.")
    input("Нажмите Enter для выхода...")  # Чтобы скрипт не закрывался сразу