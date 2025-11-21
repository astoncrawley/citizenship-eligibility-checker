from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class AngolanCitizenshipRule(BaseRule):
    country = "Angola"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []

        # Check descent
        # TODO Include marriage conditions
        for parent in person.parents:
            for citizenship in parent.citizenships:
                if citizenship.country.lower() == "angola" and citizenship.is_active_on(person.date_of_birth):
                    if person.country_of_birth != "Angola":  
                        return RuleResult(True, reasons + ["At least one Angolan parent at the time of birth abroad (requires registration for Angolan citizenship)"])
                return RuleResult(True, reasons + ["At least one Angolan parent at the time of birth in Angola (automatically considered Angolan national)"])
    
        # Default not eligible
        if not reasons:
            reasons.append("No Angolan citizen parent or qualifying birth conditions met.")
        return RuleResult(False, reasons)
