from fastneo.exceptions.exceptions import ValidationError, UnknownPropertyError
from fastneo.rest import NodeRestMethods
import pytest
from tests.utils.simple_node_classes import MyNode2


@pytest.fixture(scope="function", autouse=True)
def setup_nodes_to_read(node_rest_methods2: NodeRestMethods[MyNode2]):
    node_rest_methods2.create({"my_uuid": "uuid1", "prop2": "MyProp2"})
    node_rest_methods2.create({"my_uuid": "uuid2", "prop2": "this is prop2"})
    node_rest_methods2.create({"my_uuid": "uuid3"})
    yield

    node_rest_methods2.delete("uuid1")
    node_rest_methods2.delete("uuid2")
    node_rest_methods2.delete("uuid3")


def test_update_1(node_rest_methods2: NodeRestMethods[MyNode2]):
    """Happy case: update works"""
    new_node = node_rest_methods2.update("uuid1", {"prop2": "This is my updated prop"})

    assert new_node
    assert new_node.my_uuid and new_node.prop2
    assert new_node.prop2 == "This is my updated prop"


def test_update_2(node_rest_methods2: NodeRestMethods[MyNode2]):
    """Happy case: update works"""
    new_node = node_rest_methods2.update("uuid3", {"prop2": "Now it has some value"})

    assert new_node
    assert new_node.my_uuid and new_node.prop2
    assert new_node.prop2 == "Now it has some value"


def test_update_3(node_rest_methods2: NodeRestMethods[MyNode2]):
    """Happy case: update works"""
    new_node = node_rest_methods2.update("uuid2", {"prop2": None})

    assert new_node
    assert new_node.my_uuid
    assert not new_node.prop2


def test_update_bad_1(node_rest_methods2: NodeRestMethods[MyNode2]):
    """bad case: update works"""
    with pytest.raises(UnknownPropertyError):
        node_rest_methods2.update("uuid1", {"non-existent-prop": "some-value"})


def test_update_bad_2(node_rest_methods2: NodeRestMethods[MyNode2]):
    """Bad case: trying to update the primary key"""
    with pytest.raises(ValidationError):
        node_rest_methods2.update("uuid1", {"my_uuid": "uuid2"})
