from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class MalteseCitizenshipRule(BaseRule):
    country = "Malta"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []
        
        # Check descent
        for parent in person.parents:
            for citizenship in parent.citizenships:
                if citizenship.country.lower() == "malta" and citizenship.is_active_on(person.date_of_birth):
                    reasons.append(f"Parent {parent.name} was a Dutch citizen at time of birth.")
                    # Historical rules pre-1985
                    if person.date_of_birth < date(1985, 1, 1):
                        if parent.gender == "male":
                            return RuleResult(True, reasons + [f"Born to Maltese father {parent.name} before 1985, eligible for Dutch citizenship."])
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

        # Check jus soli (born in Malta before August 1st 1989)
        if person.country_of_birth.lower() == "malta" and person.date_of_birth < date(1989, 8, 1):
            reasons.append("Born in Malta before August 1st, 1989 - automatically maltese citizen.")
            return RuleResult(True, reasons)

        # Default not eligible
        if not reasons:
            reasons.append("No Maltese citizen parent or qualifying birth conditions met.")
            # reasons.append("No qualifying Maltese parent found.")
            # reasons.append("No qualifying Maltese citizenship found in parents.")
            # reasons.append("No qualifying Maltese ancestor found in immediate parents (simplified check).")
        return RuleResult(False, reasons)