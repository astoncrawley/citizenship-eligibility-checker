from fastapi import APIRouter
from engine.citizenship_engine import CitizenshipEngine
from models.person import Person
from models.citizenship import AcquisitionMethod
from api.schemas.person_schema import PersonSchema

router = APIRouter()
engine = CitizenshipEngine()
engine.auto_discover_rules()

@router.post("/evaluate")
def evaluate_citizenship(person_data: PersonSchema):
    """Evaluate citizenship eligibility for a given person."""

    # ✅ Use the recursive builder so parents are properly converted
    person = from_schema(person_data)

    # --- DEBUG BLOCK ---
    print("DEBUG: Main person:", person.name)
    for parent in person.parents:
        print(f"Parent: {parent.name}, Citizenship objects:")
        for c in parent.citizenships:
            print("   ", c, type(c))
    # -------------------

    results = engine.evaluate(person)
    return {country: r for country, r in results.items()}

# @router.post("/evaluate")
# def evaluate_citizenship(person_data: PersonSchema):
#     """Evaluate citizenship eligibility for a given person."""
#     person = Person(
#         name=person_data.name,
#         date_of_birth=person_data.date_of_birth,
#         country_of_birth=person_data.country_of_birth,
#         gender=person_data.gender
#     )

#     for c in person_data.citizenships:
#         person.add_citizenship(c.country, AcquisitionMethod[c.method])

#     results = engine.evaluate(person)
#     return {country: r for country, r in results.items()}

# def from_schema(schema: PersonSchema) -> Person:
#     person = Person(
#         name=schema.name,
#         date_of_birth=schema.date_of_birth,
#         country_of_birth=schema.country_of_birth,
#         gender=schema.gender
#     )
#     # Add citizenships
#     for c in schema.citizenships:
#         person.add_citizenship(c.country, AcquisitionMethod[c.method], c.date_acquired)

#     # Recursively add parents
#     for p in schema.parents:
#         parent_obj = from_schema(p)
#         person.add_parent(parent_obj)

#     return person

def from_schema(schema: PersonSchema) -> Person:
    """Recursively convert PersonSchema → Person."""
    person = Person(
        name=schema.name,
        date_of_birth=schema.date_of_birth,
        country_of_birth=schema.country_of_birth,
        gender=schema.gender,
    )

    # Add citizenships
    for c in schema.citizenships:
        try:
            method = AcquisitionMethod[c.method.upper()]
        except KeyError:
            # fallback if enum uses lowercase values instead of uppercase names
            method = AcquisitionMethod(c.method)

        person.add_citizenship(
            c.country,
            method,
            c.date_acquired,
        )
        
        # person.add_citizenship(
        #     c.country,
        #     AcquisitionMethod[c.method],
        #     c.date_acquired,
        # )

    # Recursively add parents
    for p in schema.parents:
        parent_obj = from_schema(p)
        person.add_parent(parent_obj)

    # TODO: Add marriages if schema supports them
    return person
