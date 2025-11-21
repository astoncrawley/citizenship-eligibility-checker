from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class AfghanCitizenshipRule(BaseRule):
    country = "Afghanistan"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []

        # Check jus sanguinis (at least one parent with Afghan citizenship)
        # TODO Include marriage conditions
        for parent in person.parents:
            for citizenship in parent.citizenships:
                if citizenship.country.lower() == "afghanistan" and citizenship.is_active_on(person.date_of_birth):
                    return RuleResult(True, ["Has an Afghan parent"])

        # Default not eligible
        if not reasons:
            reasons.append("No Afghan citizen parent or qualifying birth conditions met.")
        return RuleResult(False, reasons)
