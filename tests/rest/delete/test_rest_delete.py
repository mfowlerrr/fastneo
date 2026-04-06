from fastneo.rest import NodeRestMethods
from tests.utils import MyNode
import pytest


@pytest.fixture(scope="function", autouse=True)
def setup_nodes_to_read(node_rest_methods: NodeRestMethods[MyNode]):
    node_rest_methods.create({"my_uuid": "uuid1"})


def test_delete_1(node_rest_methods: NodeRestMethods[MyNode]):
    """Happy case, delete node that exists"""
    worked = node_rest_methods.delete("uuid1")
    assert worked


def test_delete_2(node_rest_methods: NodeRestMethods[MyNode]):
    """Bad case, try delete node that doesn't exist"""
    try:
        worked = node_rest_methods.delete("non-existent-node")
        assert not worked
    finally:
        # Cleanup hanging node
        node_rest_methods.delete("uuid1")


def test_delete_3(node_rest_methods: NodeRestMethods[MyNode]):
    """Bad case, test with no input value (should raise an error)"""
    try:
        with pytest.raises(TypeError):
            node_rest_methods.delete()  # ty:ignore[missing-argument]
    finally:
        # Cleanup hanging node
        node_rest_methods.delete("uuid1")
