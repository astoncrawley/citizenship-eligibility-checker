from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class ItalianCitizenshipRule(BaseRule):
    country = "Italy"

    def check(self, person: Person) -> RuleResult:
        # Very simplified: if any parent has Italian citizenship, mark eligible.
        # Real rules are more complex (dates, interrupted lines, 1948 rule for maternal descent, etc.)
        reasons: List[str] = []
        
        for parent in person.parents:
            if "italy" in [c.country.lower() for c in parent.citizenships] or parent.country_of_birth.lower() == "italy":
                reasons.append(f"Parent {parent.name} has Italian citizenship or was born in Italy.")
                # a more complex implementation would verify unbroken lineage and date constraints
                return RuleResult(True, reasons)
        
        # Default not eligible
        if not reasons:
            reasons.append("No Italian citizen parent or qualifying birth conditions met.")
            # reasons.append("No qualifying Italian parent found.")
            # reasons.append("No qualifying Italian citizenship found in parents.")
            # reasons.append("No Italian parents")
            # reasons.append("No qualifying Italian ancestor found in immediate parents (simplified check).")
        return RuleResult(False, reasons)
