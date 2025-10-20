from datetime import date
from typing import List

from engine.base_rule import BaseRule
from models.citizenship import AcquisitionMethod
from models.person import Person
from models.results import RuleResult

class BritishCitizenshipRule(BaseRule):
    country = "United Kingdom"

    def check(self, person: Person) -> RuleResult:
        """
        Evaluate eligibility for British citizenship based on:
        - Birth in the UK (jus soli)
        - Descent from a British parent (jus sanguinis)
        - Historical and marriage-based variations
        - Registration and naturalisation cases (simplified)
        """
        reasons: List[str] = []
        eligible = False

        # --- 1️⃣ Born in the UK ---
        if person.country_of_birth.lower() == "united kingdom":
            # After 1 January 1983, at least one parent must be a British citizen or settled
            if person.date_of_birth >= date(1983, 1, 1):
                for parent in person.parents:
                    if any(c.country == "United Kingdom" for c in parent.citizenships):
                        eligible = True
                        reasons.append(
                            "Born in the UK after 1983 to a British parent."
                        )
                        break
                else:
                    reasons.append(
                        "Born in the UK after 1983, but no parent was British or settled."
                    )
            else:
                # Before 1983, automatic citizenship by birth
                eligible = True
                reasons.append("Born in the UK before 1983 — automatic citizenship by birth.")

        # --- 2️⃣ Descent from British parents ---
        elif person.parents:
            for parent in person.parents:
                for record in parent.citizenships:
                    if record.country == "United Kingdom":
                        if record.acquisition_method == AcquisitionMethod.BY_BIRTH:
                            eligible = True
                            reasons.append("Born abroad to a British parent by birth (citizenship by descent).")
                        else:
                            reasons.append(
                                "Parent is British by descent — child may not automatically inherit citizenship."
                            )
                        break

        # --- 3️⃣ Marriage to a British citizen ---
        if person.marriages:
            for marriage in person.marriages:
                if any(c.country == "United Kingdom" for c in marriage.spouse.citizenships):
                    if marriage.is_active_on(person.date_of_birth):
                        reasons.append("Married to a British citizen — may qualify for naturalisation.")
                        # not automatic, but worth noting for eligibility tracking

        # --- 4️⃣ Simplified naturalisation rule ---
        if not eligible and person.country_of_birth.lower() != "united kingdom":
            for record in person.citizenships:
                if record.country != "United Kingdom" and record.acquisition_method == AcquisitionMethod.BY_NATURALIZATION:
                    eligible = True
                    reasons.append("Acquired British citizenship by naturalisation.")

        # --- 5️⃣ Registration (e.g. children under 18 with British parents) ---
        if not eligible and person.parents:
            for parent in person.parents:
                if any(c.country == "United Kingdom" for c in parent.citizenships):
                    if person.date_of_birth >= date(2003, 1, 1):
                        eligible = True
                        reasons.append("Eligible for registration as a British citizen (child under 18 with British parent).")
                        break

        return RuleResult(eligible, reasons)
