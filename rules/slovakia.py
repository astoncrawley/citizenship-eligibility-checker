from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class SlovakianCitizenshipRule(BaseRule):
    country = "Slovakia"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []
        
        for parent in person.parents:
            if "slovakia" in [c.country.lower() for c in parent.citizenships]:
                return RuleResult(True, ["Has a Slovakian parent"])
        
        # Default not eligible
        if not reasons:
            reasons.append("No Slovakian citizen parent or qualifying birth conditions met.")
            # reasons.append("No qualifying Slovakian parent found.")
            # reasons.append("No qualifying Slovakian citizenship found in parents.")
            # reasons.append("No Slovakian parents")
        return RuleResult(False, reasons)
