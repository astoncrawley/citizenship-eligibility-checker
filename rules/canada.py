from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class CanadianCitizenshipRule(BaseRule):
    country = "Canada"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []
        
        # Check jus soli (born in Canada)
        if person.country_of_birth.lower() == "canada":
            reasons.append("Born in Canada - automatically canadian citizen.")
            return RuleResult(True, reasons)
        
        # Default not eligible
        if not reasons:
            reasons.append("No Canadian citizen parent or qualifying birth conditions met.")
            # reasons.append("No qualifying Canadian parent found.")
            # reasons.append("No qualifying Canadian citizenship found in parents.")
            # reasons.append("No Canadian parents")
        return RuleResult(False, reasons)
