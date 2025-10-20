from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class TurkishCitizenshipRule(BaseRule):
    country = "Turkey"

    def check(self, person: Person) -> RuleResult:
        # simple example
        for parent in person.parents:
            if "turkey" in [c.country.lower() for c in parent.citizenships]:
                return RuleResult(True, ["Has a Turkish parent"])
        return RuleResult(False, ["No Turkish parents"])