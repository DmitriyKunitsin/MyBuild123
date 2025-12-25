from build123d import *
from ocp_vscode import show, set_port
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

case_width = 80.0 # ширина корпуса
case_lenght = 150.0 # длина корпуса
case_thickness = 25.0 # Высота корпуса
wall_thickness = 5.0 # толщина стенки
bottom_thickness = 5.0 # толщина пола
try:
    with BuildPart() as Clock:
        # стенки
        with BuildSketch() as plan:
            perimetr = Rectangle(height=case_width, width=case_lenght)
            offset(perimetr, -wall_thickness, kind=Kind.INTERSECTION, mode=Mode.SUBTRACT)
        extrude(amount=case_thickness)
        # Пол
        with Locations((0, 0, Clock.vertices().sort_by(Axis.Z)[0].Z)):
            Box(
                length=case_lenght,
                width=case_width,
                height=bottom_thickness,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            )
        # отверстия под винты сборки
        hole_radius = 2.0  # Радиус отверстий
        multipliers = [
            (1, 1),# правое верх
            (1, -1),# правое нижн
            (-1,-1),# лев ниж
            (-1, 1)# лев верх
        ]
        z_coord = Clock.vertices().sort_by(Axis.Z)[0].Z
        for mult_x, mult_y in multipliers:
            x_pos = mult_x * ((case_lenght / 2) - (wall_thickness * hole_radius))
            y_pos = mult_y * ((case_width / 2) - (wall_thickness * hole_radius))
            height_cylinder = case_thickness 
            with Locations(Pos(X=x_pos, Y=y_pos, Z=z_coord)) :
                Cylinder(radius=hole_radius, height=height_cylinder, align=(Align.CENTER, Align.CENTER, Align.MIN))
                with Locations(Pos(X=0,Y=0, Z=z_coord+(bottom_thickness))):
                    Cylinder(radius=hole_radius/2, height=height_cylinder, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)
        
        lamp_diametr = 14.0
        spacing_x_lamp = 16.0
        lamp_radius = lamp_diametr/ 2
        offset_from_board = 6.0 # отступ под плату
        # Отверстия под лампы
        with Locations(Pos(X=0, Y= ((case_width / 2) - lamp_diametr) - offset_from_board, Z=0)):
            with GridLocations(x_spacing=spacing_x_lamp, y_spacing=0, x_count=5, y_count=1 ) as circles_to_row:
                Cylinder(radius=lamp_radius,height=height_cylinder, mode=Mode.SUBTRACT)
                
        # Посадочные места под клату
        multipliers = [
            (1, 1),# правое верх
            (1, -1),# правое нижн
            (-1,-1),# лев ниж
            (-1, 1)# лев верх
        ]
        z_coord = Clock.vertices().sort_by(Axis.Z)[0].Z
        # размеры платы
        plat_height = 60.0 # высота платы
        plat_width = 90.0 # ширина платы
        distance_screw_center_width = 80 # растояние между центрами отверстий по горизонтали
        distance_between_screw = 32 # растояние между центрами отверстий по вертикали
        plat_mounting_height = bottom_thickness + 5 # высота крепления платы
        with Locations(Pos(X=0.0, Y=-offset_from_board, Z=z_coord)):
            for mult_x, mult_y in multipliers:
                x_pos = mult_x * ((distance_screw_center_width / 2) )
                y_pos = mult_y * ((distance_between_screw / 2))
                with Locations(Pos(X=x_pos,Y=y_pos,Z=z_coord)):
                    Cylinder(radius=hole_radius, height=plat_mounting_height, align=(Align.CENTER, Align.CENTER, Align.MIN))
                    with Locations(Pos(X=0,Y=0, Z=z_coord+(bottom_thickness))):
                        Cylinder(radius=hole_radius/2, height=plat_mounting_height, align=(Align.CENTER, Align.CENTER, Align.MIN), mode=Mode.SUBTRACT)
        # Два цилиндра подпорки под лампы, чтобы плату тоже держало
        with Locations(Pos(X=0, Y=0, Z=z_coord)):
            with Locations(Pos(X=distance_screw_center_width / 2, Y=((case_width / 2) - (wall_thickness * 2)), Z=z_coord)):
                Cylinder(radius=hole_radius, height=plat_mounting_height, align=(Align.CENTER, Align.CENTER, Align.MIN))
            with Locations(Pos(X=-distance_screw_center_width / 2, Y=((case_width / 2) - (wall_thickness * 2)), Z=z_coord)):                
                Cylinder(radius=hole_radius, height=plat_mounting_height, align=(Align.CENTER, Align.CENTER, Align.MIN))
    export_step(Clock.part, "digital_clock_top_case.step")
    
    set_port(3939)
    show(Clock, port=3939)
except Exception as e:
    # Логируем ошибку
    logging.error(f"Произошла ошибка: {str(e)}")
    logging.error(traceback.format_exc())
    print(f"Ошибка: {str(e)}. Проверьте лог в 'error_log.txt' для деталей.")
    input("Нажмите Enter для выхода...")  # Чтобы скрипт не закрывался сразу