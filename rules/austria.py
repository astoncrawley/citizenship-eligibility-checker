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
        
        # Check descent
        # TODO Include parent marriage and birthplace conditions
        for parent in person.parents:
            for citizenship in parent.citizenships:
                if citizenship.country.lower() == "austria" and citizenship.is_active_on(person.date_of_birth):
                    # Historical rule pre-1st September 1983 (only father passes on if married)
                    if person.date_of_birth < date(1983, 9, 1):
                        if parent.gender == "male":
                            if person.parents_married_at_birth():
                                return RuleResult(True, reasons + ["Born before September 1st 1983: Austrian father married to mother at birth (automatically considered Austrian national)"])
                            else:
                                reasons.append("Born before September 1st 1983: Austrian father but parents not married at birth.")
                                continue
                        elif parent.gender == "female":
                            if person.parents_married_at_birth():
                                reasons.append("Born before September 1st 1983: Austrian mother married to father at birth.")
                            else:
                                return RuleResult(True, reasons + ["Austrian mother unmarried to father at the time of birth (automatically considered Austrian national)"])
                    else:
                        if person.parents_married_at_birth():
                            return RuleResult(True, reasons + ["Born on or after September 1st 1983: At least one Austrian parent married to partner at the time of birth (automatically considered Austrian national)"])
                        elif parent.gender == "female":
                            return RuleResult(True, reasons + ["Austrian mother unmarried to father at the time of birth (automatically considered Austrian national)"])
                        elif person.date_of_birth > date(2013, 8, 1):
                            if parent.gender == "male":
                                return RuleResult(True, reasons + ["Born on or after August 1st 2013: Austrian father unmarried to mother at the time of birth (automatically considered Austrian national)"])
        
        # Default not eligible
        if not reasons:
            reasons.append("No Austrian citizen parent or qualifying birth conditions met.")
        return RuleResult(False, reasons)
