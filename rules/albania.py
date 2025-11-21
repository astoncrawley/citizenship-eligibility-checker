from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class AlbanianCitizenshipRule(BaseRule):
    country = "Albania"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []

        # Check descent
        # TODO Include marriage conditions
        for parent in person.parents:
            for citizenship in parent.citizenships:
                if citizenship.country.lower() == "albania" and citizenship.is_active_on(person.date_of_birth):
                    citizenship_counter += 1
                    if citizenship_counter == 2:
                        return RuleResult(True, reasons + ["Both parents Albanian at the time of birth (automatically considered Albanian national)"])
            if citizenship_counter > 0: 
                if person.country_of_birth != "Albania":  
                    return RuleResult(True, reasons + ["At least one Albanian parent at the time of birth abroad (requires registration for Albanian citizenship)"])
                return RuleResult(True, reasons + ["At least one Albanian parent at the time of birth in Albania (automatically considered Albanian national)"])
    
        # Default not eligible
        if not reasons:
            reasons.append("No Albanian citizen parent or qualifying birth conditions met.")
        return RuleResult(False, reasons)
