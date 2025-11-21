from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class AntiguanAndBarbudanCitizenshipRule(BaseRule):
    country = "Antigua and Barbuda"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []

        # Check jus soli (born in Antigua and Barbuda)
        if person.country_of_birth.lower() == "antigua and barbuda":
            reasons.append("Born in Antigua and Barbuda (automatically considered Antiguan and Barbudan national)")
            return RuleResult(True, reasons)

        # Check descent
        # TODO Include marriage conditions
        for parent in person.parents:
            for citizenship in parent.citizenships:
                if citizenship.country.lower() == "antigua and barbuda" and citizenship.is_active_on(person.date_of_birth):
                    return RuleResult(True, reasons + ["At least one Antiguan and Barbudan parent at the time of birth abroad (requires registration for Antiguan and Barbudan citizenship)"])
    
        # Default not eligible
        if not reasons:
            reasons.append("No Antiguan and Barbudan citizen parent or qualifying birth conditions met.")
        return RuleResult(False, reasons)
