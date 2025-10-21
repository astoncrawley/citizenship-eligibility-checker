from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class PolishCitizenshipRule(BaseRule):
    """
    Evaluate eligibility for Polish citizenship based on:
    - Descent from a Polish parent (jus sanguinis)
    """
    country = "Poland"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []
        
        for parent in person.parents:
            if "poland" in [c.country.lower() for c in parent.citizenships]:
                return RuleResult(True, ["Has a Polish parent"])
        
        # Default not eligible
        if not reasons:
            reasons.append("No Polish citizen parent or qualifying birth conditions met.")
            # reasons.append("No qualifying Polish parent found.")
            # reasons.append("No qualifying Polish citizenship found in parents.")
            # reasons.append("No Polish parents")
        return RuleResult(False, reasons)
