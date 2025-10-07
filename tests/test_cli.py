from __future__ import annotations

import shlex
import subprocess
import time

import pytest

import drstorage


@pytest.fixture(
    params=[
        (
            "F1_600",
            "abab00471200c5120901000000000000000a10025810000000000000140d0a",
            "humidity = 7.1    temperature = 19.7    model = 600",
        ),
        (
            "X2M_157",
            "abab004d1200cf120a3b000000000000000a10009d10000000000000a20d0a",
            "humidity = 7.7    temperature = 20.7    model = 157",
        ),
    ],
    ids=["F1_600", "X2M_157"],
)
def data(tmp_path, request):
    model, input_data, stdout = request.param
    temp = tmp_path / "data"
    temp.write_bytes(bytearray.fromhex(input_data) * 3)
    return temp, model, stdout


def test_version(script_runner):
    command = "drstorage --version"
    start = time.time()
    ret = script_runner.run(*shlex.split(command))
    end = time.time()
    elapsed = end - start
    assert ret.success
    assert drstorage.__version__ in ret.stdout
    assert ret.stderr == ""
    # make sure it took less than a second
    assert elapsed < 1.0


def test_delayed_pipe_parse(data):
    fpath, model, stdout = data
    command_in = f"""perl -pe "system 'sleep 1'" {fpath}"""
    command = f"drstorage parse --model {model}"
    ps = subprocess.Popen(shlex.split(command_in), stdout=subprocess.PIPE)
    output = subprocess.check_output(shlex.split(command), stdin=ps.stdout)
    assert ps.stdout.read() == b"", "All of the piped input was not read in"
    assert len(output) > 100, "More output was expected"
    assert stdout in output.decode("utf-8")


def test_parse(script_runner, data):
    fpath, model, stdout = data
    command = f"drstorage parse --model {model} {fpath}"
    ret = script_runner.run(*shlex.split(command))
    assert ret.success
    assert len(ret.stdout) > 100
    assert stdout in ret.stdout
    assert ret.stderr == ""


def test_parse_generic(script_runner, data):
    fpath, _, stdout = data
    command = f"drstorage parse --model generic {fpath}"
    ret = script_runner.run(*shlex.split(command))
    assert ret.success
    assert len(ret.stdout) > 100
    assert stdout in ret.stdout
    assert ret.stderr == ""
