from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class ArgentineCitizenshipRule(BaseRule):
    country = "Argentina"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []

        # Check jus soli (born in Argentina)
        if person.country_of_birth.lower() == "argentina":
            reasons.append("Born in Argentina (automatically considered Argentine national)")
            return RuleResult(True, reasons)

        # Check descent
        # TODO Include parent marriage and birthplace conditions
        for parent in person.parents:
            for citizenship in parent.citizenships:
                if citizenship.country.lower() == "argentina" and citizenship.is_active_on(person.date_of_birth):
                    return RuleResult(True, reasons + ["At least one Argentine parent at the time of birth abroad (requires registration for Argentine citizenship)"])

        # Default not eligible
        if not reasons:
            reasons.append("No Argentine citizen parent or qualifying birth conditions met.")
        return RuleResult(False, reasons)
