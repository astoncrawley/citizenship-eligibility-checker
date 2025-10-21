from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class RomanianCitizenshipRule(BaseRule):
    country = "Romania"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []
        
        for parent in person.parents:
            if "romania" in [c.country.lower() for c in parent.citizenships]:
                return RuleResult(True, ["Has a Romanian parent"])
        
        # Default not eligible
        if not reasons:
            reasons.append("No Romanian citizen parent or qualifying birth conditions met.")
            # reasons.append("No qualifying Romanian parent found.")
            # reasons.append("No qualifying Romanian citizenship found in parents.")
            # reasons.append("No Romanian parents")
        return RuleResult(False, reasons)
