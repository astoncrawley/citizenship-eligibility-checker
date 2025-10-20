from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class GreekCitizenshipRule(BaseRule):
    country = "Greece"

    def check(self, person: Person) -> RuleResult:
        # simple example
        for parent in person.parents:
            if "greece" in [c.country.lower() for c in parent.citizenships]:
                return RuleResult(True, ["Has an Greek parent"])
        return RuleResult(False, ["No Greek parents"])