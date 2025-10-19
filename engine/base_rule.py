from abc import ABC, abstractmethod
from models.person import Person
from models.results import RuleResult

class BaseRule(ABC):
    """Abstract base for citizenship rules"""
    # """Abstract base for all citizenship rule sets."""

    @property
    @abstractmethod
    def country(self) -> str:
        """Country name for this rule."""
        pass

    @abstractmethod
    def check(self, person: Person) -> RuleResult:
        """Return RuleResult explaining why the person is or is not eligible."""
        # """Returns True if the person is eligible."""
        pass
