from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class FinnishCitizenshipRule(BaseRule):
    country = "Finland"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []
        
        for parent in person.parents:
            if "finland" in [c.country.lower() for c in parent.citizenships]:
                return RuleResult(True, ["Has an Finnish parent"])
        
        # Default not eligible
        if not reasons:
            reasons.append("No Finnish citizen parent or qualifying birth conditions met.")
            # reasons.append("No qualifying Finnish parent found.")
            # return RuleResult(False, ["No qualifying Finnish citizenship found in parents."])
            # return RuleResult(False, ["No qualifying Finnish parent found."])
        return RuleResult(False, reasons)
