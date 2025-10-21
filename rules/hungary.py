from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class HungarianCitizenshipRule(BaseRule):
    country = "Hungary"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []
        
        for parent in person.parents:
            if "hungary" in [c.country.lower() for c in parent.citizenships]:
                return RuleResult(True, ["Has a Hungarian parent"])
        
        # Default not eligible
        if not reasons:
            reasons.append("No Hungarian citizen parent or qualifying birth conditions met.")
            # reasons.append("No qualifying Hungarian parent found.")
            # return RuleResult(False, ["No qualifying Hungarian citizenship found in parents."])
            # return RuleResult(False, ["No qualifying Hungarian parent found."])
        return RuleResult(False, reasons)
