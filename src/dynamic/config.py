import os
from pathlib import Path

import yaml

__config_folder_path = Path(os.getcwd()) / "dynamic" / "config"
with open(__config_folder_path / "localisation.yml", 'r', encoding="utf-8") as f:
    localisation_config: dict = yaml.safe_load(f)
with open(__config_folder_path / "main.yml", 'r', encoding="utf-8") as f:
    main_config: dict = yaml.safe_load(f)