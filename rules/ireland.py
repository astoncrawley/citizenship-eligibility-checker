from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class IrishCitizenshipRule(BaseRule):
    country = "Ireland"

    def check(self, person: Person) -> RuleResult:
        # Simplified: child of an Irish-born parent -> eligible
        reasons: List[str] = []
        for parent in person.parents:
            if parent.country_of_birth.lower() in ("ireland", "republic of ireland"):
                reasons.append(f"Parent {parent.name} was born in {parent.country_of_birth}.")
                return RuleResult(True, reasons)
        # Could add other Irish rules (grandparent, registration, etc.)
        reasons.append("No parent born in Ireland found.")
        return RuleResult(False, reasons)
