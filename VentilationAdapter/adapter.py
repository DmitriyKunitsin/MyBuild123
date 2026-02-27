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

TotalHeightAdapter = 120
'Общая высота переходника'
TotalRadiusAdapterUp = 48
'Общий внешний радиус верхней части переходника (верхняя вставляется в старую трубу)'
TotalRadiusAdapterDown = 44 
'Общий внешний радиус нижней части переходника'
InnerRadius = TotalRadiusAdapterUp - 5 # по сути эта цифра и есть толщина стенки 
'Внутренний радиус'
WallThickness = TotalRadiusAdapterUp - InnerRadius
'Толщина стенки'
ThicknessSkirt = 25 
'Толщина юбочки'
HeightSkirt = 15
'Высота юбки'
InnerRadiusDitch = TotalRadiusAdapterUp + 5
'Внутренний радиус стыковочного кольца'
RadiusPipe = 5
'Радиус трубы стыковочного кольца'
try:
    with BuildPart() as Adapter:
        'Верхняя часть переходника'
        Cylinder(radius=TotalRadiusAdapterUp, height=TotalHeightAdapter / 2, align=(Align.CENTER, Align.CENTER, Align.MIN))
        Cylinder(radius=InnerRadius, height=TotalHeightAdapter / 2, align=(Align.CENTER, Align.CENTER, Align.MIN), mode= Mode.SUBTRACT)
        
        'Центральная юбочка верх'
        with Locations(Pos(X=0, Y=0, Z=0)) :
            Cylinder(radius=(TotalRadiusAdapterUp + ThicknessSkirt), height=25, align=(Align.CENTER, Align.CENTER, Align.MIN))
            Cylinder(radius=InnerRadius, height=25, align=(Align.CENTER, Align.CENTER, Align.MIN), mode= Mode.SUBTRACT)
            'Верхняя стыковка'
            with Locations(Pos(X=0, Y=0 , Z=20)):
                Torus(
                    major_radius=InnerRadiusDitch,
                    minor_radius=RadiusPipe,
                    align=(Align.CENTER, Align.CENTER, Align.MIN),
                    mode=Mode.SUBTRACT)
            'Нижняя стыковка'
            with Locations(Pos(X=0, Y=0 , Z=-5)):
                Torus(
                    major_radius=InnerRadiusDitch,
                    minor_radius=RadiusPipe,
                    align=(Align.CENTER, Align.CENTER, Align.MIN),
                    mode=Mode.SUBTRACT)
        'Нижняя часть переходника'
        Cylinder(radius=TotalRadiusAdapterDown, height=TotalHeightAdapter / 2, align=(Align.CENTER, Align.CENTER, Align.MAX))
        Cylinder(radius=InnerRadius, height=TotalHeightAdapter / 2, align=(Align.CENTER, Align.CENTER, Align.MAX), mode= Mode.SUBTRACT)
        export_step(Adapter.part, "./Steps/AdapterVetnilaton.step")
    set_port(3939)
    show(Adapter, port=3939)
except Exception as e:
    logging.error(f"Произошла ошибка: {str(e)}")
    logging.error(traceback.format_exc())
    print(f"Ошибка: {str(e)}. Проверьте лог в 'error_log.txt' для деталей.")
    input("Нажмите Enter для выхода...")  # Чтобы скрипт не закрывался сразу