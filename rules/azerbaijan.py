from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class AzerbaijaniCitizenshipRule(BaseRule):
    country = "Azerbaijan"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []

        # Check descent
        # TODO Include parent marriage and birthplace conditions
        for parent in person.parents:
            for citizenship in parent.citizenships:
                if citizenship.country.lower() == "azerbaijan" and citizenship.is_active_on(person.date_of_birth):
                    return RuleResult(True, reasons + ["At least one Azerbaijani parent at the time of birth (automatically considered Azerbaijani national)"])
    
        # Check historic jus soli (born in Azerbaijan)
        if person.country_of_birth.lower() == "azerbaijan":
            if person.date_of_birth < date(2014, 7, 1):
                RuleResult(True, reasons + ["Born before 1st July 2014 in Azerbaijan (automatically considered Azerbaijani national)"])
            else:
                reasons.append("Born on or after 1st July 2014 to foreign parents at the time of birth in Azerbaijan")        
    
        # Default not eligible
        if not reasons:
            reasons.append("No Azerbaijani citizen parent or qualifying birth conditions met.")
        return RuleResult(False, reasons)
