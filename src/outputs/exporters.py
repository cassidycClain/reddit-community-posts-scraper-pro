thonpython
import json
from pathlib import Path

class Exporter:
    @staticmethod
    def save_json(data: dict, file_path: str):
        path = Path(file_path)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)