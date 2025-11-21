from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class AndorranCitizenshipRule(BaseRule):
    country = "Andorra"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []

        # Check descent
        # TODO Include marriage conditions
        for parent in person.parents:
            for citizenship in parent.citizenships:
                if citizenship.country.lower() == "andorra" and citizenship.is_active_on(person.date_of_birth):
                    citizenship_counter += 1
                    if citizenship_counter == 2:
                        return RuleResult(True, reasons + ["Both parents Andorran at the time of birth (automatically considered Andorran national)"])
            if citizenship_counter > 0: 
                if person.country_of_birth != "Andorra":  
                    return RuleResult(True, reasons + ["At least one Andorran parent at the time of birth abroad (requires registration for Andorran citizenship)"])
                return RuleResult(True, reasons + ["At least one Andorran parent at the time of birth in Andorra (automatically considered Andorran national)"])
    
        # Default not eligible
        if not reasons:
            reasons.append("No Andorran citizen parent or qualifying birth conditions met.")
        return RuleResult(False, reasons)
