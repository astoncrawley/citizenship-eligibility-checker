from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional, Dict, Tuple, Any

@dataclass
class RuleResult:
    eligible: bool
    reasons: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {"eligible": self.eligible, "reasons": self.reasons}
