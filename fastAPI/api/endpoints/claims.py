from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Claim
from database import get_session
from typing import List
from uuid import uuid4

from ratelimit import limits, RateLimitException

router = APIRouter()


@router.post("/claims/")
async def process_claim(claim: Claim, session: Session = Depends(get_session)):
    claim_id = str(uuid4())

    claim.claim_id = claim_id
    claim.net_fee = (
        claim.provider_fees
        + claim.member_coinsurance
        + claim.member_copay
        - claim.allowed_fees
    )

    session.add(claim)
    session.commit()
    session.refresh(claim)
    return claim


@router.get("/top_providers/")
@limits(calls=10, period=60)
async def get_top_providers(session: Session = Depends(get_session)):
    result = session.exec(
        select(Claim.provider_npi, Claim.net_fee, Claim.claim_id)
    ).all()

    # reverse sorted the result
    top_providers = sorted(result, key=lambda x: x.net_fee, reverse=True)

    # Get the top 10 providers
    top_providers = top_providers[:10]
    top_providers_dict = [
        {
            "provider_npi": provider.provider_npi,
            "net_fee": provider.net_fee,
            "claim_id": provider.claim_id,
        }
        for provider in top_providers
    ]
    return top_providers_dict
