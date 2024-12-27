import pytest


@pytest.fixture
def sample_dt():
    return {'name': 'alex', 'age': 20}


def test_name(sample_dt):
    assert sample_dt['name'] == 'alex'


def test_age(sample_dt):
    assert sample_dt['age'] == 20
