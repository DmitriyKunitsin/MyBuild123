from build123d import *
from ocp_vscode import show
import logging
import traceback

# Настройка логирования: ошибки будут писаться в файл 'error_log.txt' и выводиться в консоль
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('error_log.txt'),  # Лог в файл
        logging.StreamHandler()  # Лог в консоль
    ]
)

main_length, main_width, thickness = 150.0, 300.0, 30.0
wall_thickness = 15.0  # Толщина стенок рамки
recess_depth = 25.0 # Глубина впадины для механизма часов
cut_glass_depth = 10.0 # Глубина впадины для стекла 

# Дабы рамка не оказалась сквозной
if recess_depth > thickness:
    recess_depth = thickness - 1
if cut_glass_depth > thickness:
    cut_glass_depth = thickness - 1
try:

    with BuildPart() as Clock:
        Box(main_length, main_width, thickness)
        with BuildSketch() as plan:
            # Внешний прямоугольник
            frame = Rectangle(main_length, main_width)
            # Уступ для стекла: offset внутрь на -(wall_thickness - cut_glass_depth) = -10 мм
            offset_amount_glass = -(wall_thickness - cut_glass_depth)
            offset(frame, offset_amount_glass, kind=Kind.ARC, mode=Mode.SUBTRACT)
            
        # Экструзия всего эскиза на толщину — создаёт рамку с уступами (ступеньками)
        extrude(amount=thickness)        
        with BuildSketch() as pl:
            frame = Rectangle(main_length, main_width) # прямоугольник ступеньки

            hole_radius = 6.0  # Радиус отверстий

            with Locations(Pos(-60, 135)):
                Circle(hole_radius, mode=Mode.SUBTRACT)  # Левый верхний угол
            with Locations(Pos(60, 135)):
                Circle(hole_radius, mode=Mode.SUBTRACT)   # Правый верхний угол
            with Locations(Pos(-60, -135)):
                Circle(hole_radius, mode=Mode.SUBTRACT) # Левый нижний угол
            with Locations(Pos(60, -135)):
                Circle(hole_radius, mode=Mode.SUBTRACT)  # Правый нижний угол
            
            offset_amount_mechanism = -wall_thickness # -15
            # выдавливаю её
            offset(frame, offset_amount_mechanism, kind=Kind.ARC, mode=Mode.SUBTRACT)
            
        extrude(amount=thickness-5)
        # Фаска на верхние края (как в предыдущем)
        fillet(Clock.edges(Select.LAST).group_by(Axis.Z)[-1], radius=2)
        
    show(Clock, port=3939)

except Exception as e:
    # Логируем ошибку
    logging.error(f"Произошла ошибка: {str(e)}")
    logging.error(traceback.format_exc())
    print(f"Ошибка: {str(e)}. Проверьте лог в 'error_log.txt' для деталей.")
    input("Нажмите Enter для выхода...")  # Чтобы скрипт не закрывался сразу