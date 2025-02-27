import sqlalchemy
import pytest
from unittest import mock


from fidesctl.core import generate_dataset
from fideslang.models import Dataset, DatasetCollection, DatasetField


# Unit
@pytest.mark.unit
def test_generate_dataset_collections():
    test_resource = {"ds": {"foo": ["1", "2"], "bar": ["4", "5"]}}
    expected_result = [
        Dataset(
            name="ds",
            fides_key="ds",
            description="Fides Generated Description for Schema: ds",
            collections=[
                DatasetCollection(
                    name="foo",
                    description="Fides Generated Description for Table: foo",
                    fields=[
                        DatasetField(
                            name=1,
                            description="Fides Generated Description for Column: 1",
                            data_categories=[],
                        ),
                        DatasetField(
                            name=2,
                            description="Fides Generated Description for Column: 2",
                            data_categories=[],
                        ),
                    ],
                ),
                DatasetCollection(
                    name="bar",
                    description="Fides Generated Description for Table: bar",
                    fields=[
                        DatasetField(
                            name=4,
                            description="Fides Generated Description for Column: 4",
                            data_categories=[],
                        ),
                        DatasetField(
                            name=5,
                            description="Fides Generated Description for Column: 5",
                            data_categories=[],
                        ),
                    ],
                ),
            ],
        )
    ]
    actual_result = generate_dataset.create_dataset_collections(test_resource)
    assert actual_result == expected_result


# Integration
@pytest.mark.integration
def test_generate_dataset_info():
    test_url = "postgresql+psycopg2://fidesdb:fidesdb@fidesdb:5432/fidesdb"
    test_engine = sqlalchemy.create_engine(test_url)
    expected_collection = [
        DatasetCollection(
            name="bar",
            description="Fides Generated Description for Table: bar",
            fields=[
                DatasetField(
                    name=4,
                    description="Fides Generated Description for Column: 4",
                    data_categories=[],
                ),
            ],
        )
    ]
    expected_result = Dataset(
        fides_key="fidesdb",
        name="fidesdb",
        description="Fides Generated Description for Dataset: fidesdb",
        collections=expected_collection,
    )
    actual_result = generate_dataset.create_dataset(test_engine, expected_collection)
    assert actual_result == expected_result


@pytest.mark.integration
def test_get_db_tables():
    # Test Setup
    inspector = mock.Mock()
    inspector.get_table_names = lambda schema: test_tables
    inspector.get_columns = lambda x, schema: {
        "foo": [{"name": "1"}, {"name": "2"}],
        "bar": [{"name": "3"}, {"name": "4"}],
    }.get(x)
    inspector.get_schema_names = lambda: ["test_db", "information_schema"]

    engine = mock.Mock()
    sqlalchemy.inspect = mock.Mock(return_value=inspector)
    test_tables = ["foo", "bar"]

    expected_result = {
        "test_db": {"test_db.foo": ["1", "2"], "test_db.bar": ["3", "4"]}
    }
    actual_result = generate_dataset.get_db_collections_and_fields(engine)
    assert actual_result == expected_result
