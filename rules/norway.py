from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class NorwegianCitizenshipRule(BaseRule):
    country = "Norway"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []
        
        for parent in person.parents:
            if "norway" in [c.country.lower() for c in parent.citizenships]:
                return RuleResult(True, ["Has a Norwegian parent"])
        
        # Default not eligible
        if not reasons:
            reasons.append("No Norwegian citizen parent or qualifying birth conditions met.")
            # reasons.append("No qualifying Norwegian parent found.")
            # reasons.append("No qualifying Norwegian citizenship found in parents.")
            # reasons.append("No Norwegian parents")
        return RuleResult(False, reasons)
