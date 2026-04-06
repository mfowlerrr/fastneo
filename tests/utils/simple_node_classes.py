from neomodel.properties import StringProperty
from fastneo.models import APINode


class MyNode2(APINode):
    primary_key = "my_uuid"

    my_uuid = StringProperty(required=True)
    prop2 = StringProperty()


class MyNode(APINode):
    primary_key = "my_uuid"

    my_uuid = StringProperty(required=True)
