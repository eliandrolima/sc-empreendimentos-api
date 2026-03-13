from datetime import datetime, timezone

from bson import ObjectId
from pymongo import ReturnDocument

from app.database import enterprise_collection
from app.schemas.enterprise import EnterpriseCreate, EnterpriseUpdate
from app.utils.serializer import serialize_enterprise, serialize_enterprise_list


def create_enterprise(payload: EnterpriseCreate) -> dict:
    enterprise_data = payload.model_dump(exclude_none=True)
    result = enterprise_collection.insert_one(enterprise_data)
    created_enterprise = enterprise_collection.find_one({"_id": result.inserted_id})
    return serialize_enterprise(created_enterprise)


def list_enterprises() -> list[dict]:
    enterprises = enterprise_collection.find()
    return serialize_enterprise_list(list(enterprises))


def get_enterprise_by_id(enterprise_id: str) -> dict:
    object_id = validate_enterprise_id(enterprise_id)
    enterprise = enterprise_collection.find_one({"_id": object_id})
    if enterprise is None:
        raise LookupError("Enterprise not found")

    return serialize_enterprise(enterprise)


def update_enterprise(enterprise_id: str, payload: EnterpriseUpdate) -> dict:
    object_id = validate_enterprise_id(enterprise_id)
    update_data = payload.model_dump(exclude_none=True)
    update_data["updated_at"] = datetime.now(timezone.utc)

    updated_enterprise = enterprise_collection.find_one_and_update(
        {"_id": object_id},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER,
    )
    if updated_enterprise is None:
        raise LookupError("Enterprise not found")

    return serialize_enterprise(updated_enterprise)


def delete_enterprise(enterprise_id: str) -> dict:
    object_id = validate_enterprise_id(enterprise_id)
    deleted_enterprise = enterprise_collection.find_one_and_delete({"_id": object_id})
    if deleted_enterprise is None:
        raise LookupError("Enterprise not found")

    return serialize_enterprise(deleted_enterprise)


def validate_enterprise_id(enterprise_id: str) -> ObjectId:
    if not ObjectId.is_valid(enterprise_id):
        raise ValueError("Invalid enterprise id")

    return ObjectId(enterprise_id)
