from fastapi import APIRouter, HTTPException, status

from app.schemas.enterprise import EnterpriseCreate, EnterpriseUpdate
from app.services.enterprise_service import (
    create_enterprise,
    delete_enterprise,
    get_enterprise_by_id,
    list_enterprises,
    update_enterprise,
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


@router.put("/{enterprise_id}")
def update_enterprise_route(enterprise_id: str, payload: EnterpriseUpdate) -> dict:
    try:
        enterprise = update_enterprise(enterprise_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return {
        "success": True,
        "message": "Enterprise updated successfully",
        "data": enterprise,
    }


@router.delete("/{enterprise_id}")
def delete_enterprise_route(enterprise_id: str) -> dict:
    try:
        enterprise = delete_enterprise(enterprise_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return {
        "success": True,
        "message": "Enterprise deleted successfully",
        "data": enterprise,
    }
