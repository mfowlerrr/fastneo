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

    def create(self, data: dict) -> T:
        node = self.node(**data)
        node.save()
        return node
