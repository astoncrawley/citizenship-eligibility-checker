from datetime import date
from typing import List
from engine.base_rule import BaseRule
from models.person import Person
from models.results import RuleResult
from models.person import Marriage

class DutchCitizenshipRule(BaseRule):
    country = "Netherlands"

    def check(self, person: Person) -> bool:
        # Example simplified logic:
        for parent in person.parents:
            if parent.country_of_birth == "Netherlands":
                return True
        return False