from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class SwissCitizenshipRule(BaseRule):
    country = "Switzerland"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []
        
        for parent in person.parents:
            if "switzerland" in [c.country.lower() for c in parent.citizenships]:
                return RuleResult(True, ["Has a Swiss parent"])
        
        # Default not eligible
        if not reasons:
            reasons.append("No Swiss citizen parent or qualifying birth conditions met.")
            # reasons.append("No qualifying Swiss parent found.")
            # reasons.append("No qualifying Swiss citizenship found in parents.")
            # reasons.append("No Swiss parents")
        return RuleResult(False, reasons)
