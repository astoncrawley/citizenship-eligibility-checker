from __future__ import annotations
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field

from models.citizenship import CitizenshipRecord, AcquisitionMethod
from models.marriage import MarriageRecord

class Person(BaseModel):
    name: str
    date_of_birth: date
    country_of_birth: str
    gender: Optional[str] = None
    
    parents: List['Person'] = Field(default_factory=list)
    # spouse: Optional['Person'] = None
    citizenships: List[CitizenshipRecord] = Field(default_factory=list)
    marriages: List[MarriageRecord] = Field(default_factory=list)

    def add_parent(self, parent: 'Person') -> None:
        self.parents.append(parent)
    
    # def add_citizenship(self, citizenship: str) -> None:
    #     if citizenship not in self.citizenships:
    #         self.citizenships.append(citizenship)
    
    def add_citizenship(
        self,
        country: str,
        method: AcquisitionMethod,
        date_acquired: Optional[date] = None,
        renounced: bool = False,
        renunciation_date: Optional[date] = None
    ) -> None:
        self.citizenships.append(
            CitizenshipRecord(
                country=country,
                acquisition_method=method,
                acquisition_date=date_acquired,
                renounced=renounced,
                renunciation_date=renunciation_date,
            )
        )

    def add_marriage(self, spouse: 'Person', start_date: date, end_date: Optional[date] = None, country: Optional[str] = None):
        """Adds a marriage record and reciprocates it for the spouse."""
        self.marriages.append(MarriageRecord(spouse=spouse, start_date=start_date, end_date=end_date, country=country))

        # Add reciprocal link
        reciprocal = MarriageRecord(spouse=self, start_date=start_date, end_date=end_date, country=country)
        spouse.marriages.append(reciprocal)

    def parents_married_at_birth(self) -> bool:
        """Check if parents were married when this person was born."""
        if len(self.parents) != 2:
            return False
        parent1, parent2 = self.parents
        for marriage in parent1.marriages:
            if marriage.spouse == parent2 and marriage.is_active_on(self.date_of_birth):
                return True
        return False

    def age_on(self, when: date) -> int:
        # Accurate age calculation
        born = self.date_of_birth
        years = when.year - born.year - ((when.month, when.day) < (born.month, born.day))
        return years

    def __repr__(self):
        return f"<Person: {self.name}, born {self.country_of_birth}>"


# Fix forward references
Person.model_rebuild()
