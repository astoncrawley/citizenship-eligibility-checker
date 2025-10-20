from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class RomanianCitizenshipRule(BaseRule):
    country = "Romania"

    def check(self, person: Person) -> RuleResult:
        # simple example
        for parent in person.parents:
            if "romania" in [c.country.lower() for c in parent.citizenships]:
                return RuleResult(True, ["Has a Romanian parent"])
        return RuleResult(False, ["No Romanian parents"])