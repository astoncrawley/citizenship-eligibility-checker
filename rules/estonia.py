from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class EstonianCitizenshipRule(BaseRule):
    country = "Estonia"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []
        
        for parent in person.parents:
            if "Estonia" in [c.country.lower() for c in parent.citizenships]:
                return RuleResult(True, ["Has an Estonian parent"])
        
        # Default not eligible
        if not reasons:
            reasons.append("No Estonian citizen parent or qualifying birth conditions met.")
            # reasons.append("No qualifying Estonian parent found.")
            # return RuleResult(False, ["No qualifying Estonian citizenship found in parents."])
            # return RuleResult(False, ["No qualifying Estonian parent found."])
        return RuleResult(False, reasons)
