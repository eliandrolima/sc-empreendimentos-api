from bson import ObjectId

from app.database import enterprise_collection
from app.schemas.enterprise import EnterpriseCreate
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
    if not ObjectId.is_valid(enterprise_id):
        raise ValueError("Invalid enterprise id")

    enterprise = enterprise_collection.find_one({"_id": ObjectId(enterprise_id)})
    if enterprise is None:
        raise LookupError("Enterprise not found")

    return serialize_enterprise(enterprise)
