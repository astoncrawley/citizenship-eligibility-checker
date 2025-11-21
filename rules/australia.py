from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class AustralianCitizenshipRule(BaseRule):
    country = "Australia"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []

        # Check descent
        # TODO Include parent marriage and birthplace conditions
        for parent in person.parents:
            for citizenship in parent.citizenships:
                if citizenship.country.lower() == "australia" and citizenship.is_active_on(person.date_of_birth):
                    if person.country_of_birth != "Australia":
                        if person.date_of_birth > date(1949, 1, 26):
                            return RuleResult(True, reasons + ["Born before 26th January 1949 to at least one Australian parent at the time of birth abroad (requires registration for Australian citizenship)"])
                        else:
                            return RuleResult(False, reasons + ["Born before 26th January 1949 to at least one Australian parent at the time of birth abroad"])
                    return RuleResult(True, reasons + ["At least one Australian parent at the time of birth in Australia (automatically considered Australian national)"])
    
        # Default not eligible
        if not reasons:
            reasons.append("No Australian citizen parent or qualifying birth conditions met.")
        return RuleResult(False, reasons)
