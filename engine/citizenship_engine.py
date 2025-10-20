import importlib
import inspect
import pkgutil
from typing import List, Dict

from models.person import Person
from models.results import RuleResult
from engine.base_rule import BaseRule

class CitizenshipEngine:
    """Central engine that holds and evaluates citizenship rules."""
    
    def __init__(self) -> None:
        self._rules: Dict[str, BaseRule] = {}
    
    # def __init__(self, rules: List[BaseRule]):
    #     self.rules = rules

    def register_rule(self, rule: BaseRule) -> None:
        """Manually register a rule instance for a country."""
        self._rules[rule.country] = rule

    def unregister_rule(self, country: str) -> None:
        if country in self._rules:
            del self._rules[country]

    def auto_discover_rules(self, rules_package: str = "rules") -> None:
        """Dynamically import and register all rule classes from the given package."""
        package = importlib.import_module(rules_package)
        for _, module_name, _ in pkgutil.iter_modules(package.__path__):
            if module_name.startswith("_"):
                continue  # Skip templates or hidden modules
            module = importlib.import_module(f"{rules_package}.{module_name}")
            for _, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, BaseRule) and obj is not BaseRule:
                    instance = obj()
                    self.register_rule(instance)

    # def _discover_rules(self):
    #     from rules import __path__ as rules_path

    #     for _, module_name, _ in pkgutil.iter_modules(rules_path):
    #         if module_name.startswith("_"):
    #             continue  # Skip templates or hidden modules

    #         module = importlib.import_module(f"rules.{module_name}")

    #         for attr_name in dir(module):
    #             cls = getattr(module, attr_name)
    #             if (
    #                 isinstance(cls, type)
    #                 and issubclass(cls, BaseRule)
    #                 and cls is not BaseRule
    #                 and not cls.__name__.startswith("Template")
    #             ):
    #                 self.register_rule(cls())

    def evaluate(self, person: Person) -> Dict[str, RuleResult]:
        """Run all registered rules against a given person."""
        results: Dict[str, RuleResult] = {}
        for country, rule in self._rules.items():
            # results[country] = rule.check(person)
            try:
                results[country] = rule.check(person)
            except Exception as e:
                # Fail-safe: return not eligible with an error reason
                results[country] = RuleResult(False, [f"Rule error: {e}"])
        return results

    # def evaluate(self, person: Person) -> Dict[str, RuleResult]:
    #     """Run all registered rules against a given person."""
    #     return {country: rule.check(person) for country, rule in self._rules.items()}

    # def evaluate(self, person: Person):
    #     results = {}
    #     for rule in self.rules:
    #         results[rule.country] = rule.check(person)
    #     return results

    def evaluate_all(self, people: List[Person]) -> Dict[str, Dict[str, RuleResult]]:
        return {p.name: self.evaluate(p) for p in people}



    # def load_all_rules():
    #     rules = []
    #     for _, modname, _ in pkgutil.iter_modules(['rules']):
    #         module = importlib.import_module(f"rules.{modname}")
    #         for _, cls in inspect.getmembers(module, inspect.isclass):
    #             if issubclass(cls, BaseRule) and cls is not BaseRule:
    #                 rules.append(cls())
    #     return rules

    # for rule in load_all_rules():
    #     engine.register_rule(rule)
