import pytest
from fastneo.exceptions.exceptions import UnknownPropertyError, MissingPropertyError
from neomodel.sync_.database import db
from fastneo.rest import NodeRestMethods
from tests.utils import MyNode


def _delete_node(my_uuid: str):
    db.cypher_query(
        """
        MATCH(n:MyNode {my_uuid: $value})
        DETACH DELETE n
        """,
        {"value": my_uuid},
    )


def test_create_1(node_rest_methods: NodeRestMethods[MyNode]):
    """Happy Test 1"""
    try:
        my_node = node_rest_methods.create({"my_uuid": "this is my uuid"})
        assert my_node
        assert my_node.my_uuid
        assert my_node.my_uuid == "this is my uuid"

    finally:
        _delete_node("this is my uuid")


def test_create_bad_1(node_rest_methods: NodeRestMethods[MyNode]):
    """Bad test 1, add property to data not present on API Node definition"""
    with pytest.raises(UnknownPropertyError):
        node_rest_methods.create(
            {"my_uuid": "some_uuid", "name": "This is a fake property"}
        )


def test_create_bad_2(node_rest_methods: NodeRestMethods[MyNode]):
    """Bad test 2, add property to data not present on API Node definition"""
    with pytest.raises(UnknownPropertyError):
        node_rest_methods.create({"name": "This is a fake property"})


def test_create_bad_3(node_rest_methods: NodeRestMethods[MyNode]):
    """Bad test 3, don't provide required property on API Node definition"""
    with pytest.raises(MissingPropertyError):
        node_rest_methods.create({})
