from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional

from models.person import Person

@dataclass
class MarriageRecord:
    spouse: Person
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
