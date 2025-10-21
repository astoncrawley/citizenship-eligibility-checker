from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class CzechCitizenshipRule(BaseRule):
    country = "Czech Republic"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []
        
        for parent in person.parents:
            if "czech republic" in [c.country.lower() for c in parent.citizenships]:
                return RuleResult(True, ["Has a Czech parent"])
    
        # Default not eligible
        if not reasons:
            reasons.append("No Czech citizen parent or qualifying birth conditions met.")
            # reasons.append("No qualifying Czech parent found.")
            # reasons.append("No qualifying Czech citizenship found in parents.")
            # reasons.append("No Czech parents")
        return RuleResult(False, reasons)