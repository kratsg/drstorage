import drstorage
import pytest

testdata = {
    "F1_600": {
        "data": bytearray.fromhex(
            "abab00471200c5120901000000000000000a10025810000000000000140d0a"
        ),
        "temperature": 19.7,
        "humidity": 7.1,
    },
    "X2M_157": {
        "data": bytearray.fromhex(
            "abab004d1200cf120a3b000000000000000a10009d10000000000000a20d0a"
        ),
        "temperature": 20.7,
        "humidity": 7.7,
    },
}


@pytest.fixture(scope="function")
def data():
    return testdata


@pytest.mark.parametrize("data", testdata.values(), ids=testdata.keys())
def test_parse(data):
    result = drstorage.models.generic.parse(data["data"])
    assert result
    assert result.temperature == data["temperature"]
    assert result.humidity == data["humidity"]


def test_parse_F1_600():
    data = testdata["F1_600"]
    result = drstorage.models.F1_600.parse(data["data"])
    assert result
    assert result.temperature == data["temperature"]
    assert result.humidity == data["humidity"]


def test_parse_X2M_157(data):
    data = testdata["X2M_157"]
    result = drstorage.models.X2M_157.parse(data["data"])
    assert result
    assert result.temperature == data["temperature"]
    assert result.humidity == data["humidity"]
