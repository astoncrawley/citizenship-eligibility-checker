"""
TEMPLATE CITIZENSHIP RULE
-------------------------
This file serves as a template for creating new country-specific citizenship rules.

To add a new country:
1. Copy this file and rename it, e.g. `rules/france.py`
2. Change the class name (e.g. `FrenchCitizenshipRule`)
3. Update `country = "France"`
4. Implement your logic inside `evaluate(self, person)`
"""

from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult


class TemplateCitizenshipRule(BaseRule):
    """Example template for new citizenship rules."""

    country = "Exampleland"

    def check(self, person: Person) -> RuleResult:
        """
        Evaluates eligibility for citizenship of Exampleland.

        Add conditions based on:
        - Birthplace and date
        - Parental citizenship
        - Marriage
        - Naturalisation or registration
        """

        reasons: List[str] = []
        eligible = False

        # --- Example 1: Birth in the country before a certain date ---
        if person.country_of_birth.lower() == "exampleland":
            if person.date_of_birth < date(2000, 1, 1):
                eligible = True
                reasons.append("Born in Exampleland before 2000 — automatic citizenship by birth.")
            else:
                reasons.append("Born in Exampleland after 2000 — further checks required.")

        # # Check jus soli (born in New Zealand before January 1st 2006)
        # if person.country_of_birth.lower() == "new zealand" and person.date_of_birth < date(2006, 1, 1):
        #     reasons.append("Born in New Zealand before 2006 - automatically New Zealand citizen.")
        #     return RuleResult(True, reasons)

        # --- Example 2: Parent is a citizen by birth ---
        for parent in person.parents:
            for record in parent.citizenships:
                if record.country == "Exampleland" and record.method == AcquisitionMethod.BY_BIRTH:
                    eligible = True
                    reasons.append("Parent is an Exampleland citizen by birth — citizenship by descent.")
                    break

        # --- Example 3: Marriage to a citizen ---
        for marriage in person.marriages:
            for record in marriage.spouse.citizenships:
                if record.country == "Exampleland":
                    reasons.append("Married to an Exampleland citizen — may qualify by naturalisation.")

        # --- Example 4: Naturalisation check ---
        for record in person.citizenships:
            if record.country == "Exampleland" and record.method == AcquisitionMethod.NATURALISATION:
                eligible = True
                reasons.append("Already acquired Exampleland citizenship by naturalisation.")

        return RuleResult(self.country, eligible, reasons)
