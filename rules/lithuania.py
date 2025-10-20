from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class LithuanianCitizenshipRule(BaseRule):
    country = "Lithuania"

    def check(self, person: Person) -> RuleResult:
        # simple example
        for parent in person.parents:
            if "lithuania" in [c.country.lower() for c in parent.citizenships]:
                return RuleResult(True, ["Has a Lithuanian parent"])
        return RuleResult(False, ["No Lithuanian parents"])