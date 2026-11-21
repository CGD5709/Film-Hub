"""Repository-level tests for the filmdataset feature.

These exercise the repository in isolation against a real database — no
service orchestration, no HTTP. Use the ``test_app`` fixture from
splent_framework for the app context and a fresh DB.
"""
import pytest

pytestmark = pytest.mark.repository


def test_filmdataset_repository_placeholder(test_app):
    with test_app.app_context():
        assert True
