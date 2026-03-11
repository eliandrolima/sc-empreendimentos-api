from fastapi import APIRouter, HTTPException, status

from app.schemas.enterprise import EnterpriseCreate
from app.services.enterprise_service import (
    create_enterprise,
    get_enterprise_by_id,
    list_enterprises,
)


router = APIRouter(prefix="/enterprises", tags=["enterprises"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_enterprise_route(payload: EnterpriseCreate) -> dict:
    enterprise = create_enterprise(payload)
    return {
        "success": True,
        "message": "Enterprise created successfully",
        "data": enterprise,
    }


@router.get("")
def list_enterprises_route() -> dict:
    enterprises = list_enterprises()
    return {
        "success": True,
        "message": "Enterprises retrieved successfully",
        "data": enterprises,
    }


@router.get("/{enterprise_id}")
def get_enterprise_by_id_route(enterprise_id: str) -> dict:
    try:
        enterprise = get_enterprise_by_id(enterprise_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return {
        "success": True,
        "message": "Enterprise retrieved successfully",
        "data": enterprise,
    }
