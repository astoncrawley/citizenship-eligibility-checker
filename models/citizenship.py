from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional

class AcquisitionMethod(str, Enum):
    """Represents the way a citizenship was acquired."""
    BY_BIRTH = "by_birth" # "jus soli"
    BY_DESCENT = "by_descent" # "jus sanguinis"
    BY_NATURALIZATION = "by_naturalization"
    BY_MARRIAGE = "by_marriage"
    BY_ADOPTION = "by_adoption"
    BY_INVESTMENT = "by_investment"
    OTHER = "other"

@dataclass
class CitizenshipRecord:
    country: str
    acquisition_method: AcquisitionMethod
    acquisition_date: Optional[date] = None
    renounced: bool = False
    renunciation_date: Optional[date] = None

    def is_active_on(self, when: date) -> bool:
        """Return whether this citizenship was active at a specific time."""
        # """Check if citizenship was active at a particular time."""
        if self.renounced and self.renunciation_date and self.renunciation_date <= when:
            return False
        if self.acquisition_date and self.acquisition_date > when:
            return False
        return True
