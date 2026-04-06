import pytest
from fastneo.rest import NodeRestMethods
from tests.utils import MyNode


@pytest.fixture(scope="function", autouse=True)
def setup_nodes_to_read(node_rest_methods: NodeRestMethods[MyNode]):
    node_rest_methods.create({"my_uuid": "uuid1"})
    node_rest_methods.create({"my_uuid": "uuid2"})
    node_rest_methods.create({"my_uuid": "uuid3"})
    yield

    node_rest_methods.delete("uuid1")
    node_rest_methods.delete("uuid2")
    node_rest_methods.delete("uuid3")


def test_get_all(node_rest_methods: NodeRestMethods[MyNode]):
    my_nodes: list = node_rest_methods.list()

    assert isinstance(my_nodes, list)
    assert len(my_nodes) == 3
    for i, node in enumerate(my_nodes):
        assert node.my_uuid == f"uuid{i + 1}"


def test_get_1(node_rest_methods: NodeRestMethods[MyNode]):
    """Happy test, get one node"""
    node = node_rest_methods.get("uuid1")

    assert node is not None
    assert node.my_uuid == "uuid1"


def test_get_2(node_rest_methods: NodeRestMethods[MyNode]):
    """Get node with invalid uuid"""
    node = node_rest_methods.get("this is not a real uuid")

    assert node is None


def test_get_3(node_rest_methods: NodeRestMethods[MyNode]):
    """Get node with None uuid"""
    node = node_rest_methods.get(None)

    assert node is None


def test_get_4(node_rest_methods: NodeRestMethods[MyNode]):
    """Get node with nothing passed"""
    with pytest.raises(TypeError):
        node_rest_methods.get()  # ty:ignore[missing-argument]
