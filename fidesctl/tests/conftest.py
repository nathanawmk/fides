"""Common fixtures to be used across tests."""
from typing import Any, Dict

import pytest
import yaml
import os

from fideslang import models
from fidesctl.core.config import get_config
from fidesapi import database

TEST_CONFIG_PATH = "tests/test_config.toml"


@pytest.fixture(scope="session")
def test_config_path():
    yield TEST_CONFIG_PATH


@pytest.fixture(scope="session")
def test_config(test_config_path):
    yield get_config(test_config_path)


@pytest.fixture(scope="session", autouse=True)
def setup_db(test_config):
    "Sets up the database for testing."
    database_url = test_config.api.database_url
    database.reset_db(database_url)
    database.init_db(database_url, test_config)
    yield


@pytest.fixture(scope="session")
def resources_dict():
    """
    Yields an resource containing sample representations of different
    Fides resources.
    """
    resources_dict: Dict[str, Any] = {
        "data_category": models.DataCategory(
            organization_fides_key=1,
            fides_key="user.provided.identifiable.custom",
            parent_key="user.provided.identifiable",
            name="Custom Data Category",
            description="Custom Data Category",
        ),
        "data_qualifier": models.DataQualifier(
            organization_fides_key=1,
            fides_key="custom_data_qualifier",
            name="Custom Data Qualifier",
            description="Custom Data Qualifier",
        ),
        "dataset": models.Dataset(
            organization_fides_key=1,
            fides_key="test_sample_db_dataset",
            name="Sample DB Dataset",
            description="This is a Sample Database Dataset",
            collections=[
                models.DatasetCollection(
                    name="user",
                    fields=[
                        models.DatasetField(
                            name="Food_Preference",
                            description="User's favorite food",
                            path="some.path",
                        ),
                        models.DatasetField(
                            name="First_Name",
                            description="A First Name Field",
                            path="another.path",
                            data_categories=["user.provided.identifiable.name"],
                            data_qualifier="aggregated.anonymized.unlinked_pseudonymized.pseudonymized.identified",
                        ),
                        models.DatasetField(
                            name="Email",
                            description="User's Email",
                            path="another.another.path",
                            data_categories=[
                                "user.provided.identifiable.contact.email"
                            ],
                            data_qualifier="aggregated.anonymized.unlinked_pseudonymized.pseudonymized.identified",
                        ),
                    ],
                )
            ],
        ),
        "data_subject": models.DataSubject(
            organization_fides_key=1,
            fides_key="custom_subject",
            name="Custom Data Subject",
            description="Custom Data Subject",
        ),
        "data_use": models.DataUse(
            organization_fides_key=1,
            fides_key="custom_data_use",
            name="Custom Data Use",
            description="Custom Data Use",
        ),
        "evaluation": models.Evaluation(
            fides_key="test_evaluation", status="PASS", details=["foo"], message="bar"
        ),
        "organization": models.Organization(
            fides_key="test_organization",
            name="Test Organization",
            description="Test Organization",
        ),
        "policy": models.Policy(
            organization_fides_key=1,
            fides_key="test_policy",
            name="Test Policy",
            version="1.3",
            description="Test Policy",
            rules=[],
        ),
        "policy_rule": models.PolicyRule(
            organization_fides_key=1,
            policyId=1,
            fides_key="test_policy",
            name="Test Policy",
            description="Test Policy",
            data_categories=models.PrivacyRule(inclusion="NONE", values=[]),
            data_uses=models.PrivacyRule(inclusion="NONE", values=["provide.system"]),
            data_subjects=models.PrivacyRule(inclusion="ANY", values=[]),
            data_qualifier="aggregated.anonymized.unlinked_pseudonymized.pseudonymized",
            action="REJECT",
        ),
        "registry": models.Registry(
            organization_fides_key=1,
            fides_key="test_registry",
            name="Test Registry",
            description="Test Regsitry",
            systems=[],
        ),
        "system": models.System(
            organization_fides_key=1,
            registryId=1,
            fides_key="test_system",
            system_type="SYSTEM",
            name="Test System",
            description="Test Policy",
            privacy_declarations=[
                models.PrivacyDeclaration(
                    name="declaration-name",
                    data_categories=[],
                    data_use="provide",
                    data_subjects=[],
                    data_qualifier="aggregated_data",
                    dataset_references=[],
                )
            ],
            system_dependencies=[],
        ),
    }
    yield resources_dict


@pytest.fixture()
def test_manifests():
    test_manifests = {
        "manifest_1": {
            "dataset": [
                {
                    "name": "Test Dataset 1",
                    "organization_fides_key": 1,
                    "datasetType": {},
                    "datasetLocation": "somedb:3306",
                    "description": "Test Dataset 1",
                    "fides_key": "some_dataset",
                    "datasetTables": [],
                }
            ],
            "system": [
                {
                    "name": "Test System 1",
                    "organization_fides_key": 1,
                    "systemType": "mysql",
                    "description": "Test System 1",
                    "fides_key": "some_system",
                }
            ],
        },
        "manifest_2": {
            "dataset": [
                {
                    "name": "Test Dataset 2",
                    "description": "Test Dataset 2",
                    "organization_fides_key": 1,
                    "datasetType": {},
                    "datasetLocation": "somedb:3306",
                    "fides_key": "another_dataset",
                    "datasetTables": [],
                }
            ],
            "system": [
                {
                    "name": "Test System 2",
                    "organization_fides_key": 1,
                    "systemType": "mysql",
                    "description": "Test System 2",
                    "fides_key": "another_system",
                }
            ],
        },
    }
    yield test_manifests


@pytest.fixture()
def populated_manifest_dir(test_manifests, tmp_path):
    manifest_dir = f"{tmp_path}/populated_manifest"
    os.mkdir(manifest_dir)
    for manifest in test_manifests.keys():
        with open(f"{manifest_dir}/{manifest}.yml", "w") as manifest_file:
            yaml.dump(test_manifests[manifest], manifest_file)
    return manifest_dir


@pytest.fixture()
def populated_nested_manifest_dir(test_manifests, tmp_path):
    manifest_dir = f"{tmp_path}/populated_nested_manifest"
    os.mkdir(manifest_dir)
    for manifest in test_manifests.keys():
        nested_manifest_dir = f"{manifest_dir}/{manifest}"
        os.mkdir(nested_manifest_dir)
        with open(f"{nested_manifest_dir}/{manifest}.yml", "w") as manifest_file:
            yaml.dump(test_manifests[manifest], manifest_file)
    return manifest_dir
