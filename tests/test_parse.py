import drstorage
import pytest


@pytest.fixture(scope="function")
def data():
    return bytearray.fromhex(
        "abab00471200c5120901000000000000000a10025810000000000000140d0a"
    )


def test_parse(data):
    assert drstorage.F1_600.parse(data)
