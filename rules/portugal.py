from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class PortugueseCitizenshipRule(BaseRule):
    country = "Portugal"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []
        
        for parent in person.parents:
            if "portugal" in [c.country.lower() for c in parent.citizenships]:
                return RuleResult(True, ["Has a Portuguese parent"])
        
        # Default not eligible
        if not reasons:
            reasons.append("No Portuguese citizen parent or qualifying birth conditions met.")
            # reasons.append("No qualifying Portuguese parent found.")
            # reasons.append("No qualifying Portuguese citizenship found in parents.")
            # reasons.append("No Portuguese parents")
        return RuleResult(False, reasons)
