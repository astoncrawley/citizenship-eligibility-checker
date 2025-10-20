from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class FrenchCitizenshipRule(BaseRule):
    country = "France"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []
        citizenship_counter = 0
        
        # Check descent
        for parent in person.parents:
            for citizenship in parent.citizenships:
                if citizenship.country.lower() == "france" and citizenship.is_active_on(person.date_of_birth):
                    citizenship_counter += 1
                    if citizenship_counter == 2:
                        return RuleResult(True, reasons + ["Both parents French at the time of birth (automatically considered French national)"])
                elif parent.country_of_birth.lower() == "france" and person.country_of_birth == "france":
                    return RuleResult(True, reasons + ["At least one parent born in France at the time of birth in France (automatically considered French national)"])
            if citizenship_counter > 0: 
                if person.country_of_birth != "France":  
                    return RuleResult(True, reasons + ["At least one French parent at the time of birth abroad (requires registration for French citizenship)"])
                return RuleResult(True, reasons + ["At least one French parent at the time of birth in France (automatically considered French national)"])
    
        # Default not eligible
        if not reasons:
            reasons.append("No French citizen parent or qualifying birth conditions met.")
            # reasons.append("No qualifying French parent found.")
            # reasons.append("No qualifying French citizenship found in parents.")
            # reasons.append("No French parents")
        return RuleResult(False, reasons)
