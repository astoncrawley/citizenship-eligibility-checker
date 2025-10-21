from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class AustrianCitizenshipRule(BaseRule):
    country = "Austria"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []

        for parent in person.parents:
            if "austria" in [c.country.lower() for c in parent.citizenships]:
                return RuleResult(True, ["Has an Austrian parent"])

        # Default not eligible
        if not reasons:
            reasons.append("No Austrian citizen parent or qualifying birth conditions met.")
            # reasons.append("No qualifying Austrian parent found.")
            # reasons.append("No qualifying Austrian citizenship found in parents.")
            # reasons.append("No Austrian parents")
        return RuleResult(False, reasons)