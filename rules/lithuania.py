from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class LithuanianCitizenshipRule(BaseRule):
    country = "Lithuania"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []
        
        for parent in person.parents:
            if "lithuania" in [c.country.lower() for c in parent.citizenships]:
                return RuleResult(True, ["Has a Lithuanian parent"])
        
        # Default not eligible
        if not reasons:
            reasons.append("No Lithuanian citizen parent or qualifying birth conditions met.")
            # reasons.append("No qualifying Lithuanian parent found.")
            # reasons.append("No qualifying Lithuanian citizenship found in parents.")
            # reasons.append("No Lithuanian parents")
            # reasons.append("No qualifying Lithuanian ancestor found in immediate parents (simplified check).")
        return RuleResult(False, reasons)
