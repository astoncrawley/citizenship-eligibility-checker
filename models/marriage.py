from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.person import Person

@dataclass
class MarriageRecord:
    spouse: Person #'Person'
    start_date: date
    end_date: Optional[date] = None
    country: Optional[str] = None
    legally_recognized: bool = True

    def is_active_on(self, when: date) -> bool:
        """Check if the marriage was active at a given time."""
        if self.start_date > when:
            return False
        if self.end_date and self.end_date <= when:
            return False
        return True

        # """Check if marriage was active at a given date."""
        # if self.end_date and self.end_date < when:
        #     return False
        # return self.start_date <= when


    # def married_at_time_of_birth(date_of_birth, parents_marriage_date):
    #     if date_of_birth > parents_marriage_date:
    #         return True
    #     else:
    #         return False

    # def parents_were_married_at_birth(child: Person, parent1: Person, parent2: Person) -> bool:
    #     for marriage in parent1.marriages:
    #         if marriage.partner == parent2 and marriage.is_active_on(child.date_of_birth):
    #             return True
    #     for marriage in parent2.marriages:
    #         if marriage.partner == parent1 and marriage.is_active_on(child.date_of_birth):
    #             return True
    #     return False
    
    
    # def parents_were_married_at_birth(child: Person, parent1: Person, parent2: Person) -> bool:
    #     for marriage in parent1.marriages:
    #         if marriage.spouse == parent2 and marriage.is_active_on(child.date_of_birth):
    #             return True
    #     for marriage in parent2.marriages:
    #         if marriage.spouse == parent1 and marriage.is_active_on(child.date_of_birth):
    #             return True
    #     return False
