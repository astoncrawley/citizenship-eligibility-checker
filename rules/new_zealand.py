from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class NewZealandCitizenshipRule(BaseRule):
    country = "New Zealand"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []
        
        for parent in person.parents:
            if "new zealand" in [c.country.lower() for c in parent.citizenships]:
                return RuleResult(True, ["Has a New Zealander parent"])
        
        # Check jus soli (born in New Zealand before January 1st 2006)
        if person.country_of_birth.lower() == "new zealand" and person.date_of_birth < date(2006, 1, 1):
            reasons.append("Born in New Zealand before 2006 - automatically New Zealand citizen.")
            return RuleResult(True, reasons)
        
        # Default not eligible
        if not reasons:
            reasons.append("No New Zealand citizen parent or qualifying birth conditions met.")
            # reasons.append("No qualifying New Zealand parent found.")
            # reasons.append("No qualifying New Zealand citizenship found in parents.")
            # reasons.append("No New Zealand parents")
            # reasons.append("No parent born in New Zealand found.")
        return RuleResult(False, reasons)
