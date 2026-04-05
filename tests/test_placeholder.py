from neomodel.sync_.database import Database


def test_placeholder(neomodel_db: Database):
    result = neomodel_db.cypher_query("""
    MATCH (n)
    RETURN n
    """)
    print(result)
    assert True
