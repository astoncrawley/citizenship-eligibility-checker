from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class LuxembourgishCitizenshipRule(BaseRule):
    country = "Luxembourg"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []
        
        for parent in person.parents:
            if "luxembourg" in [c.country.lower() for c in parent.citizenships]:
                return RuleResult(True, ["Has an Luxembourgish parent"])
        
        # Default not eligible
        if not reasons:
            reasons.append("No Luxembourgish citizen parent or qualifying birth conditions met.")
            # reasons.append("No qualifying Luxembourgish parent found.")
            # reasons.append("No qualifying Luxembourgish citizenship found in parents.")
            # reasons.append("No Luxembourgish parents")
            # reasons.append("No qualifying Luxembourgish ancestor found in immediate parents (simplified check).")
        return RuleResult(False, reasons)
