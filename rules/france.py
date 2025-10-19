from datetime import date
from engine.base_rule import BaseRule
from models.person import Person
from models.results import RuleResult

class FrenchCitizenshipRule(BaseRule):
    country = "France"

    def check(self, person: Person) -> RuleResult:
        # simple example
        for parent in person.parents:
            if "france" in [c.lower() for c in parent.citizenships]:
                return RuleResult(True, ["Has a French parent"])
        return RuleResult(False, ["No French parents"])
