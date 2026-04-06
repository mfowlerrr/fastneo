from neomodel.sync_.database import db
import pytest
from fastneo.rest import NodeRestMethods
from tests.utils import MyNode, MyNode2


@pytest.fixture()
def my_node():
    return MyNode


@pytest.fixture()
def node_rest_methods():
    my_class = NodeRestMethods[MyNode](MyNode)
    yield my_class
    # Cleanup nodes
    db.cypher_query(
        """
            MATCH(n:MyNode)
            DETACH DELETE n
        """
    )


@pytest.fixture()
def node_rest_methods2():
    my_class = NodeRestMethods[MyNode2](MyNode2)
    yield my_class
    # Cleanup nodes
    db.cypher_query(
        """
            MATCH(n:MyNode2)
            DETACH DELETE n
        """
    )
