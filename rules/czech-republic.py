from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class CzechCitizenshipRule(BaseRule):
    country = "Czech Republic"

    def check(self, person: Person) -> RuleResult:
        # simple example
        for parent in person.parents:
            if "czech republic" in [c.country.lower() for c in parent.citizenships]:
                return RuleResult(True, ["Has a Czech parent"])
        return RuleResult(False, ["No Czech parents"])