from datetime import date
from typing import List
from engine.base_rule import BaseRule
from models.person import Person
from models.results import RuleResult

class DutchCitizenshipRule(BaseRule):
    country = "Netherlands"

    def check(self, person: Person) -> RuleResult:
        # Example simplified logic:
        reasons = []
        for parent in person.parents:
            if "netherlands" in [c.country.lower() for c in parent.citizenships] or parent.country_of_birth.lower() == "netherlands":
                reasons.append(f"Parent {parent.name} has Italian citizenship or was born in Italy.")
                # a more complex implementation would verify unbroken lineage and date constraints
                return RuleResult(True, reasons)
        reasons.append("No qualifying Dutch ancestor found in immediate parents (simplified check).")
        return RuleResult(False, reasons)
