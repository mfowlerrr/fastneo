from testcontainers.neo4j import Neo4jContainer
import pytest
from neomodel import config


def create_custom_neo4j():
    return (
        Neo4jContainer(
            "neo4j:5.18", username="neo4j", password="testpassword"
        )  # 👈 not default
        .with_env("NEO4J_dbms_memory_heap_max__size", "512m")
        .with_env("NEO4JLABS_PLUGINS", '["apoc"]')
        .with_env("NEO4J_dbms_security_procedures_unrestricted", "apoc.*")
    )


@pytest.fixture(scope="session")
def neo4j_container():
    container = create_custom_neo4j()
    container.start()
    yield container
    container.stop()


@pytest.fixture(scope="session")
def neomodel_db(neo4j_container: Neo4jContainer):
    host = neo4j_container.get_container_host_ip()
    port = neo4j_container.get_exposed_port(7687)
    print(neo4j_container.username, " + ", neo4j_container.password)

    conf = config.get_config()
    conf.database_url = f"bolt://neo4j:testpassword@{host}:{port}"
    from neomodel import db

    return db
