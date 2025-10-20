from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class DutchCitizenshipRule(BaseRule):
    country = "Netherlands"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []
        
        
        # Check descent
        for parent in person.parents:
            for citizenship in parent.citizenships:
                if citizenship.country.lower() == "netherlands" and citizenship.is_active_on(person.date_of_birth):
                    reasons.append(f"Parent {parent.name} was a Dutch citizen at time of birth.")
                    # Historical rules pre-1985
                    if person.date_of_birth < date(1985, 1, 1):
                        if parent.gender == "male":
                            return RuleResult(True, reasons + [f"Born to Dutch father {parent.name} before 1985, eligible for Dutch citizenship."])
                        else:
                            reasons.append(f"Born to Dutch mother {parent.name} before 1985, eligible to claim Dutch citizenship.")     
                    else:
                        if parent.gender == "female":
                            return RuleResult(True, reasons + [f"Born to Dutch mother {parent.name} after 1984, eligible for Dutch citizenship."])
                        else:
                            if person.parents_married_at_birth():
                                return RuleResult(True, reasons + [f"Born to Dutch father {parent.name} who was married to mother at birth, eligible for Dutch citizenship."])
                            else:
                                reasons.append(f"Born to Dutch father {parent.name}, but parents were not married at birth.")
                                continue
                    
        #     if "netherlands" in [c.country.lower() for c in parent.citizenships] or parent.country_of_birth.lower() == "netherlands":
        #         reasons.append(f"Parent {parent.name} has Italian citizenship or was born in Italy.")
        #         # a more complex implementation would verify unbroken lineage and date constraints
        #         return RuleResult(True, reasons)



        # Default not eligible
        if not reasons:
            reasons.append("No Dutch citizen parent or qualifying birth conditions met.")
            # reasons.append("No qualifying Dutch parent found.")
            # reasons.append("No qualifying Dutch citizenship found in parents.")
            # reasons.append("No Dutch parents")
            # reasons.append("No qualifying Dutch ancestor found in immediate parents (simplified check).")
        return RuleResult(False, reasons)