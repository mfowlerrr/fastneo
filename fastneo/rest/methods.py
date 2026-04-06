from fastneo.exceptions.exceptions import (
    UnknownPropertyError,
    MissingPropertyError,
    ValidationError,
)
from neomodel.sync_.node import StructuredNode
from neomodel import DoesNotExist
from fastneo.models import APINode
from typing import TypeVar, Any

T = TypeVar("T", bound=APINode)


class NodeRestMethods[T]:
    def __init__(self, node):
        self.node: APINode = node

    def list(self) -> list[T]:
        return self.node.nodes.all()

    def get(self, key_value: Any) -> T | None:
        try:
            node = self.node.nodes.get(**{self.node.primary_key: key_value})
            return node
        except DoesNotExist:
            return None

    def delete(self, key_value: Any) -> bool:
        try:
            node: StructuredNode = self.node.nodes.get(
                **{self.node.primary_key: key_value}
            )
            node.delete()
            return True
        except DoesNotExist:
            return False

    def update(self, key_value: Any, data: dict) -> T:
        self._validate_update_data(data)

        try:
            node: StructuredNode = self.node.nodes.get(
                **{self.node.primary_key: key_value}
            )

            for key, value in data.items():
                setattr(node, key, value)

            node.save()

            return node
        except DoesNotExist:
            msg = "Unable to update node, does not exist."
            raise DoesNotExist(msg)

    def _validate_update_data(self, data: dict):
        props = dict(self.node.__all_properties__)

        allowed_fields = set(props.keys())
        data_fields = set(data.keys())

        # 1️⃣ Unknown fields (same as create)
        unknown = data_fields - allowed_fields
        if unknown:
            raise UnknownPropertyError(f"Unknown fields {unknown}")

        # 2️⃣ Prevent updating primary key
        primary_key = self.node.primary_key
        if primary_key in data_fields:
            raise ValidationError(f"Cannot update primary key '{primary_key}'")

        # 3️⃣ Optional: prevent empty updates
        if not data:
            raise ValidationError("Update data cannot be empty")

    def _validate_data(self, data: dict):
        props = dict(self.node.__all_properties__)
        allowed_fields = {name for name in props}

        required_fields = {name for name, prop in props.items() if prop.required}

        data_fields = set(data.keys())

        unknown = data_fields - allowed_fields
        if unknown:
            raise UnknownPropertyError(f"Unknown fields {unknown}")

        missing = required_fields - data_fields
        if missing:
            raise MissingPropertyError(f"Missing requred fields: {missing}")

    def create(self, data: dict) -> T:
        self._validate_data(data)
        node = self.node(**data)
        node.save()
        return node
