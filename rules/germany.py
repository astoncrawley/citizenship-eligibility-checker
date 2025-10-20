from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class GermanCitizenshipRule(BaseRule):
    """
    Implements German nationality law (simplified but realistic logic):
    Key principles:
    1. **By descent (jus sanguinis)**: A child automatically becomes a German citizen if at least one parent
    was a German citizen at the time of birth. Before 1975, only the father could transmit citizenship if
    parents were married; since 1975, either parent can.
    2. **By birth in Germany (jus soli, since 2000)**: If a child is born in Germany after 1 Jan 2000 and at least
    one parent has been legally resident for 8+ years *and* holds permanent residency, the child gains citizenship.
    3. **By naturalization**: Not modeled here, but we acknowledge it could be added later.
    """
    country = "Germany"

    def check(self, person: Person) -> RuleResult:
        reasons: List[str] = []
                
        # Check descent
        for parent in person.parents:
            for citizenship in parent.citizenships:
                if citizenship.country.lower() == "germany" and citizenship.is_active_on(person.date_of_birth):
                    reasons.append(f"Parent {parent.name} was a German citizen at birth.")
                    # Historical rule pre-1975 (only father passes on if married)
                    # Pre-1975 rule: only fathers could pass citizenship if married to mother
                    if person.date_of_birth < date(1975, 1, 1):
                        # Before 1975: citizenship only passed by father *if married to mother*
                        
      
            # #         if citizenship.acquisition_method == "by_birth":
            #         if citizenship.acquisition_method in [AcquisitionMethod.BY_BIRTH, AcquisitionMethod.BY_DESCENT]:
            #             return RuleResult(True, ["Parent was German citizen by birth or descent at time of birth."])
            #             # return RuleResult(True, ["Parent was German citizen by birth at child's birth."])

            #         elif citizenship.acquisition_method == AcquisitionMethod.BY_NATURALIZATION:
            #             if person.date_of_birth < date(1975, 1, 1):
            #                 return RuleResult(False, ["Before 1975, naturalized Germans could not always pass citizenship to children born abroad."])
            #             else:
            #                 return RuleResult(True, ["Parent was naturalized German before birth."])
            

            #         if citizenship.acquisition_method == "by_naturalization" and person.date_of_birth < date(1975, 1, 1):
            #             reasons.append("Parent was a naturalized citizen before 1975; transmission may be restricted.")
            #             continue


            
            
                        if parent.gender == "male":
                            if person.parents_married_at_birth():
                                # return RuleResult(True, ["Born before 1975 to married German father."])
                                return RuleResult(True, reasons + ["Born before 1975: German father married to mother at birth → eligible and passes citizenship."])
                                # return RuleResult(True, [f"Pre-1975: German father married at birth."])
                            else:
                                reasons.append("Born before 1975: German father, but parents not married at birth.")
                                # reasons.append("Pre-1975: German father, but parents not married at birth.")
                                # reasons.append("Pre-1975: Mother cannot transmit citizenship if unmarried.")
                                # return RuleResult(False, ["Born before 1975, but parents not married at birth."])
                                continue
                        else:
                            reasons.append("Born before 1975: only father could pass citizenship; mother cannot.")
                            # reasons.append("Born before 1975: mother cannot transmit citizenship if unmarried.")
                            continue
                    else:
                        return RuleResult(True, reasons + ["Born after 1975: either parent can transmit citizenship."])
                        # return RuleResult(True, ["Post-1975: Either parent can transmit citizenship."])
                        # return RuleResult(True, ["Born after 1975 to a German parent."])
        
        # Check jus soli (born in Germany after 2000)
        if person.country_of_birth.lower() == "germany" and person.date_of_birth >= date(2000, 1, 1):
            # simplified: assume parents have long-term residence if any parent has lived in Germany
            for parent in person.parents:
                if parent.country_of_birth.lower() == "germany":
                    reasons.append("Born in Germany after 2000 with at least one parent resident in Germany.")
                    return RuleResult(True, reasons)
            reasons.append("Born in Germany after 2000 but no parent appears resident.")
        
        # Default not eligible
        if not reasons:
            reasons.append("No German citizen parent or qualifying birth conditions met.")
            # reasons.append("No qualifying German parent found.")
            # return RuleResult(False, ["No qualifying German citizenship found in parents."])
            # return RuleResult(False, ["No qualifying German parent found."])
        return RuleResult(False, reasons)


# # Gender-discriminatory exclusion
# if date_of_birth > "23.05.1949" and father_nationality != "German" and mother_nationality == "German":
#     if citizenship == "German":
#         citizenship = "By birth (jus soli)"
#     else:
#         citizenship = "By descent (jus sanguinis)"


# class GermanCitizenshipRule(BaseRule):
#     """
#     Implements German nationality law (simplified but realistic logic):
    
#     Key principles:
#     1. **By descent (jus sanguinis)**: A child automatically becomes a German citizen if at least one parent
#        was a German citizen at the time of birth. Before 1975, only the father could transmit citizenship if
#        parents were married; since 1975, either parent can.
#     2. **By birth in Germany (jus soli, since 2000)**: If a child is born in Germany after 1 Jan 2000 and at least
#        one parent has been legally resident for 8+ years *and* holds permanent residency, the child gains citizenship.
#     3. **By naturalization**: Not modeled here, but we acknowledge it could be added later.
#     """

#     country = "Germany"

#     def check(self, person: Person) -> RuleResult:
#         reasons: List[str] = []

#         # Check descent
#         for parent in person.parents:
#             if "germany" in [c.lower() for c in parent.citizenships]:
#                 reasons.append(f"Parent {parent.name} was a German citizen at birth.")
#                 # Historical rule pre-1975 (only father passes on if married)
#                 if person.date_of_birth < date(1975, 1, 1):
#                     if parent.gender == 'male':
#                         return RuleResult(True, reasons + ["Born before 1975: German father passes citizenship."])
#                     else:
#                         reasons.append("Born before 1975: only father could pass citizenship; mother cannot.")
#                         continue
#                 else:
#                     return RuleResult(True, reasons + ["Born after 1975: either parent can transmit citizenship."])

#         # Check jus soli (born in Germany after 2000)
#         if person.country_of_birth.lower() == "germany" and person.date_of_birth >= date(2000, 1, 1):
#             # simplified: assume parents have long-term residence if any parent has lived in Germany
#             for parent in person.parents:
#                 if parent.country_of_birth.lower() == "germany":
#                     reasons.append("Born in Germany after 2000 with at least one parent resident in Germany.")
#                     return RuleResult(True, reasons)
#             reasons.append("Born in Germany after 2000 but no parent appears resident.")

#         # Default not eligible
#         if not reasons:
#             reasons.append("No German citizen parent or qualifying birth conditions met.")
#         return RuleResult(False, reasons)