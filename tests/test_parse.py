from __future__ import annotations

import pytest

import drstorage

testdata = {
    "F1_600": [
        {
            "data": bytearray.fromhex(
                "abab00471200c5120901000000000000000a10025810000000000000140d0a"
            ),
            "temperature": 19.7,
            "humidity": 7.1,
        },
        {
            "data": bytearray.fromhex(
                "abab000b1000ce12093a000000000000000a10025810000000000000180d0a"
            ),
            "temperature": 20.6,
            "humidity": 1.1,
        },
    ],
    "F1_1200": [
        {
            "data": bytearray.fromhex(
                "abab001d1200de1209b7000000000000000a1000ad100000000000000c0d0a"
            ),
            "temperature": 22.2,
            "humidity": 2.9,
        }
    ],
    "X2M_157": [
        {
            "data": bytearray.fromhex(
                "abab004d1200cf120a3b000000000000000a10009d10000000000000a20d0a"
            ),
            "temperature": 20.7,
            "humidity": 7.7,
        }
    ],
}


@pytest.fixture
def data():
    return testdata


@pytest.mark.parametrize("dataset", testdata.values(), ids=testdata.keys())
def test_parse(dataset):
    for data in dataset:
        result = drstorage.models.generic.parse(data["data"])
        assert result
        assert result.temperature == data["temperature"]
        assert result.humidity == data["humidity"]


def test_parse_F1_600():
    dataset = testdata["F1_600"]
    for data in dataset:
        result = drstorage.models.F1_600.parse(data["data"])
        assert result
        assert result.temperature == data["temperature"]
        assert result.humidity == data["humidity"]


def test_parse_F1_1200():
    dataset = testdata["F1_1200"]
    for data in dataset:
        result = drstorage.models.F1_1200.parse(data["data"])
        assert result
        assert result.temperature == data["temperature"]
        assert result.humidity == data["humidity"]


def test_parse_X2M_157(data):
    datasets = data["X2M_157"]
    for dataset in datasets:
        result = drstorage.models.X2M_157.parse(dataset["data"])
        assert result
        assert result.temperature == dataset["temperature"]
        assert result.humidity == dataset["humidity"]
