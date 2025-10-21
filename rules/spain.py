from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class SpanishCitizenshipRule(BaseRule):
    country = "Spain"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []
        
        for parent in person.parents:
            if "spain" in [c.country.lower() for c in parent.citizenships]:
                return RuleResult(True, ["Has a Spanish parent"])
        
        # Default not eligible
        if not reasons:
            reasons.append("No Spanish citizen parent or qualifying birth conditions met.")
            # reasons.append("No qualifying Spanish parent found.")
            # reasons.append("No qualifying Spanish citizenship found in parents.")
            # reasons.append("No Spanish parents")
        return RuleResult(False, reasons)
