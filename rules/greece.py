from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class GreekCitizenshipRule(BaseRule):
    country = "Greece"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []
        
        for parent in person.parents:
            if "greece" in [c.country.lower() for c in parent.citizenships]:
                return RuleResult(True, ["Has an Greek parent"])
        
        # Default not eligible
        if not reasons:
            reasons.append("No Greek citizen parent or qualifying birth conditions met.")
            # reasons.append("No qualifying Greek parent found.")
            # return RuleResult(False, ["No qualifying Greek citizenship found in parents."])
            # return RuleResult(False, ["No qualifying Greek parent found."])
        return RuleResult(False, reasons)
