from datetime import date
from models.person import Person
from models.citizenship import AcquisitionMethod
from engine.citizenship_engine import CitizenshipEngine
from rules.germany import GermanCitizenshipRule
from rules.ireland import IrishCitizenshipRule
from rules.uk import BritishCitizenshipRule
from utils.report_utils import print_report
from utils.date_utils import parse_date

# # Demo/Example data and run
# if __name__ == "__main__":
#     # Create a small family
#     parent = Person(
#         name="John O'Reilly",
#         date_of_birth=date(1960, 5, 10),
#         country_of_birth="Ireland",
#         citizenships=["Ireland"],
#     )

#     italian_parent = Person(
#         name="Maria Rossi",
#         date_of_birth=date(1962, 8, 20),
#         country_of_birth="Italy",
#         citizenships=["Italy"],
#     )

#     user = Person(
#         name="Sarah O'Reilly",
#         date_of_birth=date(1995, 3, 15),
#         country_of_birth="United States",
#         parents=[parent, italian_parent],
#     )

#     # Register rules
#     engine = CitizenshipEngine()
#     engine.register_rule(IrishCitizenshipRule())
#     engine.register_rule(ItalianCitizenshipRule())

#     # Evaluate
#     results = engine.evaluate(user)
#     print_report(user.name, results)

#     # Example: batch evaluation
#     people = [user, parent, italian_parent]
#     batch = engine.evaluate_all(people)
#     for name, res in batch.items():
#         print_report(name, res)

#     # Example: load from JSON payload
#     payload = {
#         "name": "Alex Example",
#         "date_of_birth": "1990-07-01",
#         "country_of_birth": "Canada",
#         "parents": [
#             {"name": "Paolo Example", "date_of_birth": "1960-02-02", "country_of_birth": "Italy", "citizenships": ["Italy"]},
#             {"name": "Jane Example", "date_of_birth": "1965-06-06", "country_of_birth": "Canada"}
#         ]
#     }
#     alex = person_from_dict(payload)
#     print_report(alex.name, engine.evaluate(alex))



# if __name__ == "__main__":
#     father = Person(
#         name="Hans",
#         date_of_birth=date(1950, 5, 5),
#         country_of_birth="Germany",
#         gender="male"
#     )
#     # Add a citizenship using the Enum
#     father.add_citizenship("Germany", AcquisitionMethod.BY_BIRTH, date(1950, 5, 5))

#     mother = Person(
#         name="Jane",
#         date_of_birth=date(1955, 5, 5),
#         country_of_birth="UK",
#         gender="female"
#     )
#     mother.add_citizenship("United Kingdom", AcquisitionMethod.BY_BIRTH, date(1955, 5, 5))

#     child = Person(
#         name="Anna",
#         date_of_birth=date(1970, 1, 1),
#         country_of_birth="France",
#         parents=[father, mother]
#     )

#     engine = CitizenshipEngine()
#     engine.auto_discover_rules()
#     results = engine.evaluate(child)

#     for country, result in results.items():
#         print(f"{country}: {'Eligible' if result.eligible else 'Not eligible'}")
#         for reason in result.reasons:
#             print(f"  - {reason}")



# if __name__ == "__main__":
#     # Example people
#     parent = Person(
#         name="John O'Reilly",
#         date_of_birth=date(1960, 5, 10),
#         country_of_birth="Ireland",
#         citizenships=["Ireland"]
#     )

#     user = Person(
#         name="Sarah O'Reilly",
#         date_of_birth=date(1995, 3, 15),
#         country_of_birth="United States",
#         parents=[parent]
#     )

#     # Register rules
#     rules = [IrishCitizenshipRule(), ItalianCitizenshipRule()]
#     engine = CitizenshipEngine(rules)

#     # Run checks
#     results = engine.evaluate(user)

#     print("Citizenship eligibility:")
#     for country, eligible in results.items():
#         print(f" - {country}: {'Eligible' if eligible else 'Not eligible'}")


# # User inputs
# birth_country = input("Country of birth: ")
# date_of_birth = input("Date of birth: ")
# gender = input("Gender: ")

# father_birth_country = input("Father's country of birth: ")
# father_nationality = input("Father's nationality: ")

# mother_birth_country = input("Mother's country of birth: ")
# mother_nationality = input("Mother's nationality: ")

# parents_marital_status = input("Parents' marital status: ")
# parents_marriage_date = input("Parents' marriage date: ")


# if date_of_birth > parents_marriage_date:
#     married_at_time_of_birth = True
# else:
#     married_at_time_of_birth = False


# """
# Citizenship Engine Prototype
# - Data model: Person (dataclass)
# - Rules: BaseRule -> concrete CountryRule classes
# - Engine: CitizenshipEngine with dynamic rule registration
# - RuleResult: carries eligibility boolean and reasons (helpful for reporting)

# To run: open this file in Python 3.9+ and run `python citizenship_engine_prototype.py`

# This is a compact but extensible starting point. Add more country rules by
# subclassing BaseRule and registering them with the engine.
# """


# import pkgutil, importlib, inspect
# from engine.base_rule import BaseRule

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




if __name__ == "__main__":
    # Example data
    father = Person(name="Hans Müller", date_of_birth=parse_date("1950-05-05"), country_of_birth="Germany", gender="male")
    father.add_citizenship("Germany", AcquisitionMethod.BY_BIRTH)

    mother = Person(name="Jane Smith", date_of_birth=parse_date("1955-05-05"), country_of_birth="UK", gender="female")
    mother.add_citizenship("United Kingdom", AcquisitionMethod.BY_BIRTH)

    father.add_marriage(mother, start_date=date(1968, 1, 1))

    child = Person("Anna Müller", parse_date("1970-01-01"), "France", parents=[father, mother])

    # Create engine and automatically load all rules from /rules/
    engine = CitizenshipEngine()
    engine.auto_discover_rules()
    
    # Evaluate eligibility
    results = engine.evaluate(child)

    print_report(child, results)
    
    


    # father = Person(name="Hans Müller", date_of_birth=date(1950, 6, 1), country_of_birth="Germany", citizenships=["Germany"], gender="male")
    # mother = Person(name="Jane Smith", date_of_birth=date(1955, 8, 10), country_of_birth="USA", citizenships=["United States"], gender="female")

    # child = Person(name="Anna Müller", date_of_birth=date(1970, 3, 20), country_of_birth="France", parents=[father, mother])
    # child2 = Person(name="Ben Müller", date_of_birth=date(1980, 3, 20), country_of_birth="France", parents=[mother, father])
    # child3 = Person(name="Lena Müller", date_of_birth=date(2005, 3, 20), country_of_birth="Germany", parents=[mother, father])

    # engine = CitizenshipEngine()
    # engine.register_rule(GermanCitizenshipRule())
    # engine.register_rule(IrishCitizenshipRule())

    # for person in [child, child2, child3]:
    #     results = engine.evaluate(person)
    #     print_report(person.name, results)




    # father = Person("Hans", date(1950, 5, 5), "Germany", gender="male", citizenships=["Germany"])
    # mother = Person("Jane", date(1955, 5, 5), "UK", gender="female", citizenships=["United Kingdom"])
    # father.add_marriage(mother, start_date=date(1968, 1, 1))

    # child = Person("Anna", date(1970, 1, 1), "France", parents=[father, mother])





    # father = Person(name="Hans", date_of_birth=date(1950, 6, 1), gender="male", country_of_birth="Germany")
    # father.add_citizenship("Germany", "by_birth", date(1950, 6, 1))
    # father.add_citizenship("Canada", "by_naturalization", date(1980, 1, 1))

    # child = Person(name="Anna", date_of_birth=date(1985, 5, 1), parents=[father])




    # father = Person("Hans Müller", date(1950, 6, 1), "Germany", gender="male", citizenships=["Germany"])
    # mother = Person("Jane Smith", date(1955, 8, 10), "USA", gender="female", citizenships=["United States"])
    # father.add_marriage(mother, date(1968, 1, 1))

    # child = Person("Anna Müller", date(1970, 3, 20), "France", parents=[father, mother])

    # engine = CitizenshipEngine()
    # engine.register_rule(GermanCitizenshipRule())
    # engine.register_rule(IrishCitizenshipRule())




    # father = Person(name="Hans", date_of_birth=date(1950, 5, 5), country_of_birth="Germany", citizenships=["Germany"], gender="male")
    # mother = Person(name="Jane", date_of_birth=date(1955, 5, 5), country_of_birth="UK", citizenships=["United Kingdom"], gender="female")

    # # Married in 1968, child born 1970
    # father.add_marriage(mother, start_date=date(1968, 1, 1))

    # child = Person(name="Anna", date_of_birth=date(1970, 1, 1), country_of_birth="France", parents=[father, mother])




    # father = Person("Hans", date(1950, 5, 5), "Germany", gender="male")
    # father.add_citizenship("Germany", AcquisitionMethod.BY_BIRTH, date(1950, 5, 5))

    # mother = Person("Jane", date(1955, 5, 5), "UK", gender="female")
    # mother.add_citizenship("United Kingdom", AcquisitionMethod.BY_BIRTH)

    # father.add_marriage(mother, start_date=date(1968, 1, 1))

    # child = Person("Anna", date(1970, 1, 1), "France", parents=[father, mother])

    # print(child.was_parents_married_at_birth())  # True ✅




    # # Parent British by birth
    # parent = Person("John", date(1970, 5, 5), "United Kingdom")
    # parent.add_citizenship("United Kingdom", AcquisitionMethod.BY_BIRTH)

    # # Child born abroad after 2000
    # child = Person("Emma", date(2002, 3, 10), "France", parents=[parent])

    # rule = BritishCitizenshipRule()
    # result = rule.evaluate(child)

    # print(result.country, result.eligible)
    # print(result.reasons)
