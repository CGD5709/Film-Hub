"""Unit tests for the filmdataset feature.

Pure logic only — no Flask app, no database. Anything that needs persistence
or the test client belongs in test_service.py or test_integration.py.
"""
import pytest

pytestmark = pytest.mark.unit


def test_filmdataset_placeholder():
    assert True
