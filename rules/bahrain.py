from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class BahrainiCitizenshipRule(BaseRule):
    country = "Bahrain"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []

        # Check descent
        # TODO Include parent marriage and birthplace conditions based on citizenship application
        for parent in person.parents:
            for citizenship in parent.citizenships:
                if citizenship.country.lower() == "bahrain" and citizenship.is_active_on(person.date_of_birth):
                    if person.date_of_birth > date(1963, 9, 16):
                        if parent.gender == "male":
                            if person.country_of_birth != "Bahrain":
                                return RuleResult(True, reasons + ["Bahraini father at the time of birth abroad (requires registration for Bahraini citizenship)"])
                            else:
                                return RuleResult(True, reasons + ["Bahraini father at the time of birth in Bahrain (automatically considered Bahraini national)"])
    
        # Default not eligible
        if not reasons:
            reasons.append("No Bahriani citizen parent or qualifying birth conditions met.")
        return RuleResult(False, reasons)
