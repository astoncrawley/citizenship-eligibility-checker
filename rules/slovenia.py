from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class SlovenianCitizenshipRule(BaseRule):
    country = "Slovenia"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []
        
        for parent in person.parents:
            if "slovenia" in [c.country.lower() for c in parent.citizenships]:
                return RuleResult(True, ["Has an Slovenian parent"])
        
        # Default not eligible
        if not reasons:
            reasons.append("No Slovenian citizen parent or qualifying birth conditions met.")
            # reasons.append("No qualifying Slovenian parent found.")
            # reasons.append("No qualifying Slovenian citizenship found in parents.")
            # reasons.append("No Slovenian parents")
        return RuleResult(False, reasons)
