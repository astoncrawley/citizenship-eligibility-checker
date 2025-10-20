from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class SlovenianCitizenshipRule(BaseRule):
    country = "Slovenia"

    def check(self, person: Person) -> RuleResult:
        # simple example
        for parent in person.parents:
            if "slovenia" in [c.country.lower() for c in parent.citizenships]:
                return RuleResult(True, ["Has an Slovenian parent"])
        return RuleResult(False, ["No Slovenian parents"])