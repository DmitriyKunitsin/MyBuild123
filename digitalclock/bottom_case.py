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
        # разъём
        height_size_case_bate = 56.0
        width_case_bat = 32.0
        wall_bat_case_thickness = 2.0
        usb_len = 12
        usb_widght = 6
        usb_height = bottom_thickness
        # посадочное батарейки
        with BuildSketch() as bat_box:
            with Locations(
                Pos(
                    X=((-case_lenght / 2) + wall_thickness) + (height_size_case_bate / 2) - wall_bat_case_thickness ,
                    Y=((case_width / 2) - wall_thickness) - (width_case_bat / 2) + wall_bat_case_thickness)):
                case_battary = Rectangle(height=height_size_case_bate, width=width_case_bat, rotation=90)
                offset(case_battary, -wall_bat_case_thickness, kind=Kind.INTERSECTION, mode=Mode.SUBTRACT)  
        extrude(amount=10)
        with Locations(Pos(
            X=-((case_lenght / 2) - (wall_thickness / 2)), 
            Y=((case_width / 2) - wall_thickness) - (width_case_bat / 2) + wall_bat_case_thickness, 
            Z=(bottom_thickness) + (usb_widght / 2)
            )) as usb:
            Box(
                length=usb_height,
                width=usb_len,
                height=usb_widght,
                mode=Mode.SUBTRACT
            )
    set_port(3939)
    show(Clock, port=3939)
except Exception as e:
    # Логируем ошибку
    logging.error(f"Произошла ошибка: {str(e)}")
    logging.error(traceback.format_exc())
    print(f"Ошибка: {str(e)}. Проверьте лог в 'error_log.txt' для деталей.")
    input("Нажмите Enter для выхода...")  # Чтобы скрипт не закрывался сразу