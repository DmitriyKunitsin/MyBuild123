from build123d import *
from ocp_vscode import show, set_port
import logging
import traceback
import math


# Настройка логирования: ошибки будут писаться в файл 'error_log.txt' и выводиться в консоль
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('error_log.txt'),  # Лог в файл
        logging.StreamHandler()  # Лог в консоль
    ]
)

'Общая высота переходника'
TotalHeightAdapter = 200
'Общий внешний радиус'
TotalRadiusAdapter = 95
'Внутренний радиус'
InnerRadius = TotalRadiusAdapter - 10 # по сути эта цифра и есть толщина стенки
'Толщина стенки'
WallThickness = TotalRadiusAdapter - InnerRadius
'Толщина стенки юбочки'
ThicknessSkirt = 15
try:
    with BuildPart() as Adapter:
        'Верхняя часть переходника'
        Cylinder(radius=TotalRadiusAdapter, height=TotalHeightAdapter / 2, align=(Align.CENTER, Align.CENTER, Align.MIN))
        Cylinder(radius=InnerRadius, height=TotalHeightAdapter / 2, align=(Align.CENTER, Align.CENTER, Align.MIN), mode= Mode.SUBTRACT)
        'Центральная юбочка'
        with Locations(Pos(X=0, Y=0, Z=-25)) :
            Cylinder(radius=(TotalRadiusAdapter + ThicknessSkirt), height=50, align=(Align.CENTER, Align.CENTER, Align.MIN))
            Cylinder(radius=InnerRadius, height=50, align=(Align.CENTER, Align.CENTER, Align.MIN), mode= Mode.SUBTRACT)
        'Нижняя часть переходника'
        Cylinder(radius=TotalRadiusAdapter, height=TotalHeightAdapter / 2, align=(Align.CENTER, Align.CENTER, Align.MAX))
        Cylinder(radius=InnerRadius, height=TotalHeightAdapter / 2, align=(Align.CENTER, Align.CENTER, Align.MAX), mode= Mode.SUBTRACT)
    set_port(3939)
    show(Adapter, port=3939)
except Exception as e:
    logging.error(f"Произошла ошибка: {str(e)}")
    logging.error(traceback.format_exc())
    print(f"Ошибка: {str(e)}. Проверьте лог в 'error_log.txt' для деталей.")
    input("Нажмите Enter для выхода...")  # Чтобы скрипт не закрывался сразу