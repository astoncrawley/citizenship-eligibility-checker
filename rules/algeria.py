from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class AlgerianCitizenshipRule(BaseRule):
    country = "Algeria"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []

        # Check jus sanguinis (at least one parent with Algerian citizenship)
        # TODO Include marriage conditions
        for parent in person.parents:
            for citizenship in parent.citizenships:
                if citizenship.country.lower() == "algeria" and citizenship.is_active_on(person.date_of_birth):
                    return RuleResult(True, ["Has an Algerian parent"])

        # Default not eligible
        if not reasons:
            reasons.append("No Algerian citizen parent or qualifying birth conditions met.")
        return RuleResult(False, reasons)
