from neomodel.sync_.node import StructuredNode


class APINodeMetaclass(type(StructuredNode)):
    def __new__(cls, name, bases, dct):
        primary_key = dct.get("primary_key")
        if primary_key:
            if primary_key not in dct:
                raise AttributeError(
                    f"Primary key '{primary_key}' is not defined as a property in class '{name}'"
                )

            prop = dct[primary_key]
            prop.unique_index = True

        return super().__new__(cls, name, bases, dct)


class APINode(StructuredNode, metaclass=APINodeMetaclass):
    primary_key: str = ""

    @classmethod
    def _get_properties(cls) -> dict:
        return dict(cls.__all_properties__)

    @classmethod
    def _get_relationships(cls) -> dict:
        return dict(cls.__all_relationships__)
