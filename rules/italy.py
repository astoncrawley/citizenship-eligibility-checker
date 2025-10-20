from datetime import date
from typing import List
from engine.base_rule import BaseRule
from models.person import Person
from models.results import RuleResult

def parents_were_married_at_birth(child: Person, parent1: Person, parent2: Person) -> bool:
    for marriage in parent1.marriages:
        if marriage.spouse == parent2 and marriage.is_active_on(child.date_of_birth):
            return True
    for marriage in parent2.marriages:
        if marriage.spouse == parent1 and marriage.is_active_on(child.date_of_birth):
            return True
    return False

class ItalianCitizenshipRule(BaseRule):
    country = "Italy"

    def check(self, person: Person) -> RuleResult:
        # Very simplified: if any parent has Italian citizenship, mark eligible.
        # Real rules are more complex (dates, interrupted lines, 1948 rule for maternal descent, etc.)
        reasons = []
        for parent in person.parents:
            if "italy" in [c.country.lower() for c in parent.citizenships] or parent.country_of_birth.lower() == "italy":
                reasons.append(f"Parent {parent.name} has Italian citizenship or was born in Italy.")
                # a more complex implementation would verify unbroken lineage and date constraints
                return RuleResult(True, reasons)
        reasons.append("No qualifying Italian ancestor found in immediate parents (simplified check).")
        return RuleResult(False, reasons)
