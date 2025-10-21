from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class DanishCitizenshipRule(BaseRule):
    country = "Denmark"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []
        
        for parent in person.parents:
            if "denmark" in [c.country.lower() for c in parent.citizenships]:
                return RuleResult(True, ["Has a Danish parent"])
        
        # Default not eligible
        if not reasons:
            reasons.append("No Danish citizen parent or qualifying birth conditions met.")
            # reasons.append("No qualifying Danish parent found.")
            # return RuleResult(False, ["No qualifying Danish citizenship found in parents."])
            # return RuleResult(False, ["No qualifying Danish parent found."])
        return RuleResult(False, reasons)
