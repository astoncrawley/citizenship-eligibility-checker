from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class SpanishCitizenshipRule(BaseRule):
    country = "Spain"

    def check(self, person: Person) -> RuleResult:
        # simple example
        for parent in person.parents:
            if "spain" in [c.country.lower() for c in parent.citizenships]:
                return RuleResult(True, ["Has a Spanish parent"])
        return RuleResult(False, ["No Spanish parents"])