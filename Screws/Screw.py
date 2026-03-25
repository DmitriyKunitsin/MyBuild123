# Конфигурация для метрических гаек (стандартные размеры)
NUT_CONFIG = {
    'M3': {'nut': 3,  'width': 5.5, 'height': 2.4, 'hole': 3.5},
    'M4': {'nut': 4,  'width': 7,   'height': 3.2, 'hole': 4.5},
    'M5': {'nut': 5,  'width': 8,   'height': 4,   'hole': 5.5},
    'M6': {'nut': 6,  'width': 10,  'height': 5,   'hole': 6.5},
    'M8': {'nut': 8,  'width': 13,  'height': 6.5, 'hole': 8.5},
    'M10': {'nut': 10, 'width': 16,  'height': 8,   'hole': 10.5},
    'M12': {'nut': 12, 'width': 18,  'height': 10,  'hole': 13},
}

class ScrewManager:
    """
    Класс-помощник для хранения размеров метрической гайки.
    
    Аргументы:
        thread_diameter (int): номинальный диаметр резьбы (6 для M6, 8 для M8 и т.д.)
    
    Атрибуты:
        nut: диаметр резьбы
        width:  размер под ключ (мм)
        height: высота гайки (мм)
        hole:   диаметр отверстия под болт (мм)
    
    Пример:
        nut_m6 = Screw(6)
        print(nut_m6.width)  # 10
        print(nut_m6.height) # 5
    """
    
    def __init__(self, nut_m: int):
        """
        Args:
            nut_m: номинальный диаметр резьбы (например, 6 для M6)
            config: словарь с размерами, если None – берётся из NUT_CONFIG
        """
        key = f'M{nut_m}'        
        if key not in NUT_CONFIG:
            raise ValueError(f"Нет конфигурации для гайки M{nut_m}")
        cfg = NUT_CONFIG[key]
        self.nut = cfg['nut']    # диаметр отверстия под болт
        self.width = cfg['width']      # размер под ключ
        self.height = cfg['height']    # высота гайки
        self.hole_dia = cfg['hole']    # диаметр отверстия под болт
        
    def __repr__(self):
        return f"Гайка(M{self.nut})"
    
    @property
    def hex_radius(self):
        return self.width / ( 2 * 0.866)