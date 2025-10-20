import json
import os
from typing import List, Dict

DATA_DIR = os.path.dirname(__file__)

def load_json(filename: str) -> List[Dict]:
    path = os.path.join(DATA_DIR, filename)
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def get_countries() -> List[Dict]:
    return load_json("countries.json")

def get_country_names() -> List[str]:
    return [entry["country"] for entry in get_countries()]

def get_nationalities() -> List[str]:
    return [entry["nationality"] for entry in get_countries()]
