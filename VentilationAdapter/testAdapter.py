from build123d import *
from ocp_vscode import show, set_port
import logging
import traceback
import math
import adapter

# Настройка логирования: ошибки будут писаться в файл 'error_log.txt' и выводиться в консоль
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('error_log.txt'),  # Лог в файл
        logging.StreamHandler()  # Лог в консоль
    ]
)
HeightForTest = 30
InnerRadius = adapter.InnerRadius
RadiusAdapterDown = adapter.TotalRadiusAdapterDown
""" Тестовое кольцо для проверки правильности диаметра окружности ( вставляется в трубу или нет )"""
try:
    with BuildPart() as Adapter:
        'Тестовое кольцо для вставки в старую металлическую трубу'
        print(f"Радиус(диаметр) внешний : {RadiusAdapterDown}({RadiusAdapterDown*2})\nРадиус(диаметр) внутренний : {InnerRadius}({InnerRadius*2})\nТолищна стенки : {RadiusAdapterDown - InnerRadius}")
        Cylinder(radius=RadiusAdapterDown, height=HeightForTest, align=(Align.CENTER, Align.CENTER, Align.MIN))
        Cylinder(radius=InnerRadius, height=HeightForTest, align=(Align.CENTER, Align.CENTER, Align.MIN), mode= Mode.SUBTRACT)
        'Тестовое кольцо для вставки в новую нержу трубу'
    export_step(Adapter.part, "./Steps/TestOldPipeConnector.step")
    set_port(3939)
    show(Adapter, port=3939)
# В нержу труба вошла. радиус  TotalRadiusAdapterDown ( 48 ), можно даже 49 попробовать 

except Exception as e:
    logging.error(f"Произошла ошибка: {str(e)}")
    logging.error(traceback.format_exc())
    print(f"Ошибка: {str(e)}. Проверьте лог в 'error_log.txt' для деталей.")
    input("Нажмите Enter для выхода...")  # Чтобы скрипт не закрывался сразу