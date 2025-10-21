from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class TurkishCitizenshipRule(BaseRule):
    country = "Turkey"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []
        
        for parent in person.parents:
            if "turkey" in [c.country.lower() for c in parent.citizenships]:
                return RuleResult(True, ["Has a Turkish parent"])
        
        # Default not eligible
        if not reasons:
            reasons.append("No Turkish citizen parent or qualifying birth conditions met.")
            # reasons.append("No qualifying Turkish parent found.")
            # reasons.append("No qualifying Turkish citizenship found in parents.")
            # reasons.append("No Turkish parents")
        return RuleResult(False, reasons)