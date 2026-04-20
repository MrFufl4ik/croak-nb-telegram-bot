import os
from pathlib import Path

import yaml

__config_folder_path = Path(os.getcwd()) / "dynamic" / "config"
with open(__config_folder_path / "localisation.yml", 'r', encoding="utf-8") as f:
    localisation_config: dict = yaml.safe_load(f)
with open(__config_folder_path / "main.yml", 'r', encoding="utf-8") as f:
    main_config: dict = yaml.safe_load(f)

database_config: dict = {
    "user": os.environ["DATABASE_USER"],
    "password": os.environ["DATABASE_PASSWORD"],
    "port": 5432,
    "name": os.environ["DATABASE_NAME"]
}

redis_config: dict = {
    "password": os.environ["REDIS_PASSWORD"],
    "port": 6379,
    "logic_database": os.environ["REDIS_LOGIC_DATABASE"],
}