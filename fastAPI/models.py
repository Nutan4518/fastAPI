from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import validator
import re


class Claim(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    claim_id: str
    provider_npi: str
    submitted_procedure: str
    provider_fees: float
    member_coinsurance: float
    member_copay: float
    allowed_fees: float
    net_fee: Optional[float] = None

    @validator("provider_npi")
    def validate_provider_npi(cls, value):
        if not re.match(r"^\d{10}$", value):
            raise ValueError("Provider NPI must be a 10 digit number.")
        return value

    @validator("submitted_procedure")
    def validate_submitted_procedure(cls, value):
        if not value.startswith("D"):
            raise ValueError("Submitted procedure must begin with the letter D.")
        return value
