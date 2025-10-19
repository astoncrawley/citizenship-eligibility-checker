from datetime import date
from typing import List
from engine.base_rule import BaseRule
from models.person import Person
from models.results import RuleResult

def parents_were_married_at_birth(child: Person, parent1: Person, parent2: Person) -> bool:
    for marriage in parent1.marriages:
        if marriage.partner == parent2 and marriage.is_active_on(child.date_of_birth):
            return True
    for marriage in parent2.marriages:
        if marriage.partner == parent1 and marriage.is_active_on(child.date_of_birth):
            return True
    return False

class IrishCitizenshipRule(BaseRule):
    country = "Ireland"

    def check(self, person: Person) -> RuleResult:
        # Simplified: child of an Irish-born parent -> eligible
        reasons = []
        for parent in person.parents:
            if parent.country_of_birth.lower() in ("ireland", "republic of ireland"):
                reasons.append(f"Parent {parent.name} was born in {parent.country_of_birth}.")
                return RuleResult(True, reasons)
        # Could add other Irish rules (grandparent, registration, etc.)
        reasons.append("No parent born in Ireland found.")
        return RuleResult(False, reasons)
