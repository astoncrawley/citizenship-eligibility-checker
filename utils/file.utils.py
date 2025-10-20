# saving/loading data, file paths

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional, Dict, Tuple, Any

from models.person import Person
from utils.date_utils import parse_date


# Example: load person data from a simple JSON structure
def person_from_dict(d: Dict[str, Any], persons_cache: Dict[str, Person] = None) -> Person:
    # persons_cache helps resolve references (parents/spouse) by name in the same payload
    if persons_cache is None:
        persons_cache = {}

    if d.get("name") in persons_cache:
        return persons_cache[d["name"]]

    p = Person(
        name=d.get("name"),
        date_of_birth=parse_date(d.get("date_of_birth")),
        country_of_birth=d.get("country_of_birth"),
        gender=d.get("gender"),
        citizenships=d.get("citizenships", []),
    )
    persons_cache[p.name] = p

    # Attach parents if provided as dicts
    parents = []
    for pd in d.get("parents", []):
        if isinstance(pd, dict):
            parents.append(person_from_dict(pd, persons_cache))
        elif isinstance(pd, str):
            # reference by name; will be resolved if present in cache
            if pd in persons_cache:
                parents.append(persons_cache[pd])
            else:
                # create placeholder with minimal info
                placeholder = Person(name=pd, date_of_birth=parse_date("1900-01-01"), country_of_birth="")
                persons_cache[pd] = placeholder
                parents.append(placeholder)
    p.parents = parents

    # Spouse
    spouse = d.get("spouse")
    if spouse:
        if isinstance(spouse, dict):
            p.spouse = person_from_dict(spouse, persons_cache)
        elif isinstance(spouse, str):
            p.spouse = persons_cache.get(spouse)

    return p