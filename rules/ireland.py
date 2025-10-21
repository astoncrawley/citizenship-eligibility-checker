from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class IrishCitizenshipRule(BaseRule):
    country = "Ireland"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []
        
        for parent in person.parents:
            if parent.country_of_birth.lower() in ("ireland", "republic of ireland"):
                reasons.append(f"Parent {parent.name} was born in {parent.country_of_birth}.")
                return RuleResult(True, reasons)
        
        # Check jus soli (born on island of Ireland before January 1st 2005)
        if person.country_of_birth.lower() == "ireland" and person.date_of_birth < date(2005, 1, 1):
            reasons.append("Born in Ireland before 2005 - automatically irish citizen.")
            return RuleResult(True, reasons)
        
        # Default not eligible
        if not reasons:
            reasons.append("No Irish citizen parent or qualifying birth conditions met.")
            # reasons.append("No qualifying Irish parent found.")
            # reasons.append("No qualifying Irish citizenship found in parents.")
            # reasons.append("No Irish parents")
            # reasons.append("No parent born in Ireland found.")
            # reasons.append("No qualifying Irish ancestor found in immediate parents (simplified check).")
        return RuleResult(False, reasons)
