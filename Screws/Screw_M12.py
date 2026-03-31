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
        nut = ScrewManager(12)
        print(repr(nut))
        with BuildSketch() as hex_sketch:
            RegularPolygon(radius=nut.hex_radius, side_count=6)  
        extrude(amount=nut.height) 
        export_step(Screw.part, path_mgr.get_file_path(f"screw_m{nut.nut}.step"))
    set_port(3939)
    show(Screw, port=3939)
except Exception as ex:
    logging.error(f"Произошла ошибка: {str(ex)}")
    logging.error(traceback.format_exc())
    print(f"Ошибка: {str(ex)}. Проверьте лог в 'error_log.txt' для деталей.")
    input("Нажмите Enter для выхода...")  # Чтобы скрипт не закрывался сразу