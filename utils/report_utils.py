from models.results import RuleResult

def print_report(person, results):
    """Pretty-print citizenship evaluation results."""
    print(f"\nCitizenship Eligibility Report for {person.name}:")
    print(f"Date of Birth: {person.date_of_birth} | Country of Birth: {person.country_of_birth}\n")

    for country, result in results.items():
        status = "✅ Eligible" if result.eligible else "❌ Not eligible"
        print(f"{country}: {status}")
        for reason in result.reasons:
            print(f"  - {reason}")

# def print_report(name, results):
#     print(f"\nEligibility Report for {name}:")
#     for country, result in results.items():
#         print(f" - {country}: {'Eligible' if result.eligible else 'Not eligible'}")
#         for reason in result.reasons:
#             print(f"    - {reason}")

# def print_report(name: str, results: Dict[str, RuleResult]) -> None:
#     print(f"\n---- Eligibility report for: {name} ----")
#     for country, rr in results.items():
#         status = "ELIGIBLE" if rr.eligible else "NOT ELIGIBLE"
#         print(f"* {country}: {status}")
#         for r in rr.reasons:
#             print(f"    - {r}")

# def print_report(name: str, results: Dict[str, RuleResult]) -> None:
#     print(f"\n--- Citizenship eligibility report for {name} ---")
#     for country, rr in results.items():
#         print(f"{country}: {'ELIGIBLE' if rr.eligible else 'NOT ELIGIBLE'}")
#         for reason in rr.reasons:
#             print(f"  - {reason}")

# def print_report(name: str, results: Dict[str, RuleResult]) -> None:
#     print(f"\nCitizenship Eligibility Report for {name}:")
#     for country, result in results.items():
#         print(f" - {country}: {'Eligible' if result.eligible else 'Not eligible'}")
#         for reason in result.reasons:
#             print(f"    - {reason}")