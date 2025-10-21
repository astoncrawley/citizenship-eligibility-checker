from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class AmericanCitizenshipRule(BaseRule):
    country = "United States"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []
        
        # Check jus soli (born in United States)
        if person.country_of_birth.lower() == "united states":
            reasons.append("Born in United States - automatically american citizen.")
            return RuleResult(True, reasons)
        
        # Default not eligible
        if not reasons:
            reasons.append("No American citizen parent or qualifying birth conditions met.")
            # reasons.append("No qualifying American parent found.")
            # reasons.append("No qualifying American citizenship found in parents.")
            # reasons.append("No American parents")
        return RuleResult(False, reasons)
