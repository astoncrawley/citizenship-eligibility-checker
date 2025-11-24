from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class BahamianCitizenshipRule(BaseRule):
    """
    https://www.immigration.gov.bs/applying-to-stay/applying-for-citizenship/
    """
    country = "Bahamas"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []

        # Check descent
        # TODO Include parent marriage and birthplace conditions based on citizenship application
        for parent in person.parents:
            for citizenship in parent.citizenships:
                if citizenship.country.lower() == "Bahamas" and citizenship.is_active_on(person.date_of_birth):
                    if person.country_of_birth != "Bahamas":
                        return RuleResult(True, reasons + ["At least one Bahamian parent at the time of birth abroad (requires registration for Bahamian citizenship)"])
                    else:
                        return RuleResult(True, reasons + ["At least one Bahamian parent at the time of birth in Bahamas (automatically considered Bahamian national)"])
    
        # Default not eligible
        if not reasons:
            reasons.append("No Bahamian citizen parent or qualifying birth conditions met.")
        return RuleResult(False, reasons)
