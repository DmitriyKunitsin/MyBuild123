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
'Общий внешний радиус верхней части переходника (верхняя вставляется в старую трубу)'
TotalRadiusAdapterUp = 90
'Общий внешний радиус нижней части переходника'
TotalRadiusAdapterDown = 98 
'Внутренний радиус'
InnerRadius = TotalRadiusAdapterUp - 20 # по сути эта цифра и есть толщина стенки
'Толщина стенки'
WallThickness = TotalRadiusAdapterUp - InnerRadius
'Толщина стенки юбочки'
ThicknessSkirt = 45
'Кольцо для выреза стыковоччной конавки'
'Радиус Внутрениий стыковочной конавки'
InnerRadiusDitch = TotalRadiusAdapterUp + 15
'Толщина конавки'
ThinknessDitch = 15
# Параметры стыковочной канавки
'Глубина канавки (вертикальный размер)'
GrooveDepth = 50
'Ширина канавки (радиальное углубление)'
GrooveWidth = 15
'Положение канавки относительно центра юбки (по Z)'
GroovePositionZ = 0  # По центру юбки
try:
    with BuildPart() as Adapter:
        'Верхняя часть переходника'
        Cylinder(radius=TotalRadiusAdapterUp, height=TotalHeightAdapter / 2, align=(Align.CENTER, Align.CENTER, Align.MIN))
        Cylinder(radius=InnerRadius, height=TotalHeightAdapter / 2, align=(Align.CENTER, Align.CENTER, Align.MIN), mode= Mode.SUBTRACT)
        
        'Центральная юбочка'
        with Locations(Pos(X=0, Y=0, Z=-25)) :
            Cylinder(radius=(TotalRadiusAdapterUp + ThicknessSkirt), height=50, align=(Align.CENTER, Align.CENTER, Align.MIN))
            Cylinder(radius=InnerRadius, height=50, align=(Align.CENTER, Align.CENTER, Align.MIN), mode= Mode.SUBTRACT)
            with Locations(Pos(X=0, Y=0 , Z=35)):
                Torus(
                    major_radius=InnerRadiusDitch,
                    minor_radius=15,
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