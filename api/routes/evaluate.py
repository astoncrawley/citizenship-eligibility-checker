from fastapi import APIRouter, HTTPException
from models.person import Person
from models.citizenship import AcquisitionMethod
from api.schemas.person_schema import PersonSchema
from engine.citizenship_engine import CitizenshipEngine

router = APIRouter()

# Load the citizenship engine once (auto-discovers rule files)
engine = CitizenshipEngine()
engine.auto_discover_rules()


def build_person_from_schema(schema: PersonSchema) -> Person:
    """
    Recursively converts incoming PersonSchema (raw JSON) into Person model objects,
    including parents, marriages, and citizenship records.
    """
    person = Person(
        name=schema.name,
        date_of_birth=schema.date_of_birth,
        country_of_birth=schema.country_of_birth,
        gender=schema.gender,
        parents=[],        # will fill in below
        citizenships=[],
        marriages=[]
    )
    
    # Add applicant's citizenships
    for c in schema.citizenships:
        # person.add_citizenship(c.country, AcquisitionMethod(c.method), c.date_acquired)
        try:
            # method = AcquisitionMethod[c.method.upper()]
            method = AcquisitionMethod(c.method)
        except KeyError:
            # # fallback if enum uses lowercase values instead of uppercase names
            # method = AcquisitionMethod(c.method)
            raise HTTPException(status_code=400, detail=f"Invalid acquisition method: {c.method}")
        
        person.add_citizenship(
            country=c.country,
            method=method, #AcquisitionMethod[c.method],
            date_acquired=c.date_acquired
        )
    
    # Recursively add parents
    for p_schema in schema.parents:
        parent_obj = build_person_from_schema(p_schema)
        person.add_parent(parent_obj)

    # TODO: Add marriage mapping if UI later supports spouse input
    # TODO: Add marriages if schema supports them
    return person


@router.post("/evaluate")
def evaluate_citizenship(person_data: PersonSchema):
    """
    Evaluate citizenship eligibility for a given person.
    Public endpoint (no login required).
    Accepts a PersonSchema JSON, builds a Person object, runs rules, returns result.
    """
    try:
        person = build_person_from_schema(person_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    results = engine.evaluate(person)

    # Convert RuleResult objects to JSON-safe output
    output = {
        country: {
            "eligible": result.eligible,
            "reasons": result.reasons
        }
        for country, result in results.items()
    }

    return output
    # return {country: r for country, r in results.items()}



#     # ✅ Use the recursive builder so parents are properly converted
#     person = from_schema(person_data)

#     # --- DEBUG BLOCK ---
#     print("DEBUG: Main person:", person.name)
#     for parent in person.parents:
#         print(f"Parent: {parent.name}, Citizenship objects:")
#         for c in parent.citizenships:
#             print("   ", c, type(c))
#     # -------------------



#     person = Person(
#         name=person_data.name,
#         date_of_birth=person_data.date_of_birth,
#         country_of_birth=person_data.country_of_birth,
#         gender=person_data.gender
#     )

#     for c in person_data.citizenships:
#         person.add_citizenship(c.country, AcquisitionMethod[c.method])
