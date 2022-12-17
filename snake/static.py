from pathlib import Path
from typing import List, Union

from settings import BASE_DIR, STATIC_URL


class StaticFiles:
    def __init__(self):
        self.static_files_list: List[Path] = []
        self._make_static_files_list(Path(BASE_DIR, STATIC_URL))

    def _make_static_files_list(self, directory: Path):
        """наполняет static_files_list файлами из директории STATIC_URL"""
        for currentFile in directory.iterdir():
            if currentFile.is_dir():
                self._make_static_files_list(currentFile)
            else:
                self.static_files_list.append(currentFile)

    def get_static_file(self, filename: str) -> Union[Path, None]:
        for file in self.static_files_list:
            if file.name == filename:
                return file
        return None
