from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class ArmenianCitizenshipRule(BaseRule):
    country = "Armenia"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []

        # Check descent
        # TODO Include parent marriage and birthplace conditions
        for parent in person.parents:
            for citizenship in parent.citizenships:
                if citizenship.country.lower() == "armenia" and citizenship.is_active_on(person.date_of_birth):
                    citizenship_counter += 1
                    if citizenship_counter == 2:
                        return RuleResult(True, reasons + ["Both parents Armenian at the time of birth (automatically considered Armenian national)"])
            if citizenship_counter > 0: 
                if person.country_of_birth != "Armenia":  
                    return RuleResult(True, reasons + ["At least one Armenian parent at the time of birth abroad (requires registration for Armenian citizenship)"])
                return RuleResult(True, reasons + ["At least one Armenian parent at the time of birth in Armenia (automatically considered Armenian national)"])
    
        # Default not eligible
        if not reasons:
            reasons.append("No Armenian citizen parent or qualifying birth conditions met.")
        return RuleResult(False, reasons)
