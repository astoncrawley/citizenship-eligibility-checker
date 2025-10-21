from __future__ import annotations
from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field

class CitizenshipRecordSchema(BaseModel):
    """Represents a record of a citizenship and how it was acquired."""
    country: str = Field(..., description="Country of citizenship")
    method: str = Field(..., description="Method of acquisition (e.g., BY_BIRTH, BY_DESCENT)")
    date_acquired: Optional[date] = Field(None, description="Date citizenship was acquired")

class MarriageSchema(BaseModel):
    """Represents a marriage record."""
    spouse_name: str = Field(..., description="Name of the spouse")
    start_date: date = Field(..., description="Date when marriage started")
    end_date: Optional[date] = Field(None, description="Date when marriage ended, if applicable")
    country: Optional[str] = Field(None, description="Country where the marriage was registered")

class PersonSchema(BaseModel):
    """Recursive schema for a person and their relationships."""
    name: str
    date_of_birth: date
    country_of_birth: str
    gender: Optional[str] = None

    citizenships: Optional[List[CitizenshipRecordSchema]] = Field(default_factory=list)
    marriages: Optional[List[MarriageSchema]] = Field(default_factory=list)
    
    # Recursive reference — a person can have parents, who are also PersonSchema objects
    parents: Optional[List[PersonSchema]] = Field(default_factory=list)

    class Config:
        # allow recursive references and forward declarations
        orm_mode = True
