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
            
            
            # Уступ для механизма: ещё один offset внутрь на -wall_thickness = -30 мм
            # offset_amount_mechanism = -wall_thickness
            # offset(frame, offset_amount_mechanism, kind=Kind.ARC, mode=Mode.SUBTRACT)
        
        # Экструзия всего эскиза на толщину — создаёт рамку с уступами (ступеньками)
        extrude(amount=thickness)        
        print("Вторая рамка для образования ступеньки")
        with BuildSketch() as pl:
            print(f"Создание прямоугольника с размерами len : {main_length}, widg : {main_width}")  # Для отладки
            frame = Rectangle(main_length, main_width)
            hole_radius = 6.0  # Радиус отверстий
            # Вычитаем круглые отверстия в углах (диаметр 6 мм, радиус 3 мм)
            with Locations(Pos(-60, 135)):
                Circle(hole_radius, mode=Mode.SUBTRACT)  # Левый верхний угол
            with Locations(Pos(60, 135)):
                Circle(hole_radius, mode=Mode.SUBTRACT)   # Правый верхний угол
            with Locations(Pos(-60, -135)):
                Circle(hole_radius, mode=Mode.SUBTRACT) # Левый нижний угол
            with Locations(Pos(60, -135)):
                Circle(hole_radius, mode=Mode.SUBTRACT)  # Правый нижний угол
            
            offset_amount_mechanism = -wall_thickness # -15
            offset(frame, offset_amount_mechanism, kind=Kind.ARC, mode=Mode.SUBTRACT)
            
        extrude(amount=thickness-5)
        # Фаска на верхние края (как в предыдущем)
        fillet(Clock.edges(Select.LAST).group_by(Axis.Z)[-1], radius=2)
        
        # сквозные отверстия по углам ВТОРОГО прямоугольника (для механизма)
        # Размеры внутреннего прямоугольника после offset
        # inner_length = main_length - 2 * wall_thickness
        # inner_width = main_width - 2 * wall_thickness
        # # Позиции углов внутреннего прямоугольника
        # corner_positions = [
        #     (-inner_length / 2, inner_width / 2),   # Левый верхний
        #     (inner_length / 2, inner_width / 2),    # Правый верхний
        #     (-inner_length / 2, -inner_width / 2),  # Левый нижний
        #     (inner_length / 2, -inner_width / 2)    # Правый нижний
        # ]
        
        # hole_radius = 6.0  # Радиус отверстий
        # for pos in corner_positions:
        #     print(f"Создаём отверстие в позиции: {pos} и глубиной : {thickness}")  # Для отладки
            # with Locations(pos):  
            #     with BuildSketch() as holes:
                    #Circle(radius=hole_radius)
                #extrude(amount=thickness, mode=Mode.SUBTRACT)  # Вычитаем цилиндр для сквозного отверстия
        #input("Нажмите Enter для выхода...")  # Чтобы скрипт не закрывался сразу
        # Фаска на верхние края (как в предыдущем)
        #fillet(Clock.edges(Select.LAST).group_by(Axis.Z)[-1], radius=2)
    
    #     # основная коробку
    #     Box(main_length, main_width, thickness)
    #     # фаска на верхние края
    #     fillet(Clock.edges(Select.LAST).group_by(Axis.Z)[1], radius=2)
        
    #     # впадина для элементов часов
    #     # with Locations((0, 0, 5)): # перемещает плоскость эскиза на верхнюю грань (Z = thickness). 
    #     with BuildSketch() as recess_sketch:
    #         logging.error(f"Length recess {main_length-4*wall_thickness}") # 260
    #         logging.error(f"Width recess {main_width-4*wall_thickness}") # 110
    #         Rectangle(main_length - 4 * wall_thickness, main_width - 4 * wall_thickness)
    #     extrude(amount=25.0, mode=Mode.SUBTRACT)  
        
    #     # # # # впадина под стекло
    #     # with Locations((0, 0, thickness)):
    #     with BuildSketch() as cut_glass:
    #         logging.error(f"Length glass {main_length-2*wall_thickness}") # 280
    #         logging.error(f"Width glass {main_width-2*wall_thickness}") # 130
    #         Rectangle(main_length - 2 * wall_thickness, main_width - 2 * wall_thickness)
    #     extrude(amount=15.0, mode=Mode.SUBTRACT)
        
    show(Clock, port=3939)

except Exception as e:
    # Логируем ошибку
    logging.error(f"Произошла ошибка: {str(e)}")
    logging.error(traceback.format_exc())
    print(f"Ошибка: {str(e)}. Проверьте лог в 'error_log.txt' для деталей.")
    input("Нажмите Enter для выхода...")  # Чтобы скрипт не закрывался сразу