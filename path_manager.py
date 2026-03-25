"""
Модуль для управления путями к директориям.
Синглтон для работы с путями файловой системы.
"""

import os
from pathlib import Path
from typing import Union, Optional


class PathManager:
    """Менеджер для работы с путями файловой системы (синглтон)"""
    
    _instance = None
    TARGET_PATH = r"C:\3D_Models"
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, path: Optional[Union[str, Path]] = None):
        """Инициализация менеджера путей (выполняется только один раз)"""
        if not hasattr(self, '_initialized'):
            self.path = Path(path) if path else Path(self.TARGET_PATH)
            self._validate_path()
            self._initialized = True
    
    def _validate_path(self) -> None:
        """Проверка существования пути"""
        try:
            if not self.path.exists():
                raise FileNotFoundError(f"Путь не существует: {self.path}")
            
            if not self.path.is_dir():
                raise NotADirectoryError(f"Путь не является директорией: {self.path}")
            
            if not os.access(self.path, os.R_OK):
                raise PermissionError(f"Нет прав на чтение: {self.path}")
                
        except Exception as e:
            raise RuntimeError(f"Ошибка при проверке пути {self.path}: {e}")
    
    def get_path(self) -> Path:
        """Возвращает проверенный путь"""
        return self.path
    
    def get_file_path(self, filename: str) -> Path:
        """Возвращает полный путь к файлу"""
        step_path = self.path / filename
        print(f"Сохраняю в {step_path}")
        return step_path
    
    @property
    def exists(self) -> bool:
        """Проверяет существует ли путь"""
        return self.path.exists()
    
    @property
    def is_valid(self) -> bool:
        """Проверяет валидность пути"""
        try:
            self._validate_path()
            return True
        except:
            return False


# Простой импорт - сразу готов к использованию
path_mgr = PathManager()